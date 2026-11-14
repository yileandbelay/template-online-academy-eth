"""Spike C: tenant isolation with PostgreSQL row-level security, SET LOCAL and a connection pooler.

Questions (docs/adr, plan section 8):
  1. Does forced RLS isolate tenants, and does it fail closed when no tenant is set?
  2. Why must the application role not own the tables?
  3. Does a per-transaction tenant (set_config(..., true), i.e. SET LOCAL) stay safe behind PgBouncer in transaction
     pooling mode, where a plain SET leaks to the next client?
  4. What does it cost?

Run (needs a local PostgreSQL 16 and PgBouncer; see README.md):
  uv run --with 'psycopg[binary]' --with sqlalchemy python spikes/c_rls/rls_spike.py
"""

from __future__ import annotations

import contextvars
import os
import statistics
import sys
import threading
import time

import psycopg
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import Session

PG_SOCKET = os.environ.get("PG_SOCKET", "/tmp/pgspike")  # noqa: S108
PG_PORT = int(os.environ.get("PG_PORT", "5544"))
POOL_PORT = int(os.environ.get("POOL_PORT", "6544"))
DB = "meksp"

results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))


def admin(sql: str, db: str = "postgres") -> None:
    with psycopg.connect(host=PG_SOCKET, port=PG_PORT, user="postgres", dbname=db, autocommit=True) as c:
        c.execute(sql)  # type: ignore[arg-type]


def setup() -> None:
    admin(f"DROP DATABASE IF EXISTS {DB}")
    for role in ("mek_app", "mek_owner"):
        admin(f"DROP ROLE IF EXISTS {role}")
    admin("CREATE ROLE mek_owner LOGIN")  # runs migrations; owns the tables
    admin("CREATE ROLE mek_app LOGIN")  # the application: not an owner, no BYPASSRLS
    admin(f"CREATE DATABASE {DB} OWNER mek_owner")
    with psycopg.connect(host=PG_SOCKET, port=PG_PORT, user="mek_owner", dbname=DB, autocommit=True) as c:
        c.execute("CREATE SCHEMA lms")
        c.execute("CREATE TABLE lms.course (id bigserial PRIMARY KEY, tenant_id text NOT NULL, title text NOT NULL)")
        c.execute("CREATE INDEX course_tenant_idx ON lms.course (tenant_id, id)")
        # A second table WITHOUT force, to show the owner bypass.
        c.execute("CREATE TABLE lms.lesson (id bigserial PRIMARY KEY, tenant_id text NOT NULL, title text NOT NULL)")
        for table in ("course", "lesson"):
            c.execute(f"ALTER TABLE lms.{table} ENABLE ROW LEVEL SECURITY")
            # current_setting(..., true) returns NULL when unset, so the predicate is NULL: no rows (fail closed).
            c.execute(
                f"CREATE POLICY tenant_isolation ON lms.{table} FOR ALL TO mek_app "
                "USING (tenant_id = current_setting('app.tenant_id', true)) "
                "WITH CHECK (tenant_id = current_setting('app.tenant_id', true))"
            )
        c.execute("ALTER TABLE lms.course FORCE ROW LEVEL SECURITY")  # owner is subject to RLS too
        c.execute("GRANT USAGE ON SCHEMA lms TO mek_app")
        c.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA lms TO mek_app")
        c.execute("GRANT USAGE ON ALL SEQUENCES IN SCHEMA lms TO mek_app")


def app_conn(port: int = PG_PORT, host: str = PG_SOCKET) -> psycopg.Connection:
    # prepare_threshold=None: no server-side prepared statements, required behind transaction pooling.
    return psycopg.connect(host=host, port=port, user="mek_app", dbname=DB, prepare_threshold=None)


def as_tenant(conn: psycopg.Connection, tenant: str) -> None:
    """Start the tenant for THIS transaction only (SET LOCAL semantics)."""
    conn.execute("SELECT set_config('app.tenant_id', %s, true)", (tenant,))


def titles(conn: psycopg.Connection, table: str = "course") -> list[str]:
    return sorted(r[0] for r in conn.execute(f"SELECT title FROM lms.{table}").fetchall())  # type: ignore[arg-type]


def test_isolation() -> None:
    with app_conn() as c:
        for tenant, name in (("mek", "Excel"), ("kasina", "Baking"), ("kasina", "Icing")):
            as_tenant(c, tenant)
            c.execute("INSERT INTO lms.course (tenant_id, title) VALUES (%s, %s)", (tenant, name))
            c.commit()
        as_tenant(c, "mek")
        mine = titles(c)
        c.commit()
        as_tenant(c, "kasina")
        theirs = titles(c)
        c.commit()
    check(
        "1a tenant sees only its own rows",
        mine == ["Excel"] and theirs == ["Baking", "Icing"],
        f"mek={mine} kasina={theirs}",
    )

    with app_conn() as c:
        as_tenant(c, "mek")
        try:
            c.execute("INSERT INTO lms.course (tenant_id, title) VALUES ('kasina', 'Smuggled')")
            ok = False
        except psycopg.errors.InsufficientPrivilege as exc:
            ok = "row-level security" in str(exc)
            c.rollback()
    check("1b WITH CHECK blocks writing another tenant's row", ok)

    with app_conn() as c:
        sees = titles(c)
        c.rollback()
        try:
            c.execute("INSERT INTO lms.course (tenant_id, title) VALUES ('mek', 'No tenant set')")
            wrote = True
        except psycopg.errors.InsufficientPrivilege:
            wrote = False
            c.rollback()
    check("1c fails closed: no tenant set means no rows and no writes", sees == [] and not wrote)

    with app_conn() as c:
        as_tenant(c, "mek")
        c.execute("UPDATE lms.course SET title = 'hacked' WHERE tenant_id = 'kasina'")
        updated = c.execute("SELECT count(*) FROM lms.course WHERE title = 'hacked'").fetchone()[0]  # type: ignore[index]
        c.rollback()
    check("1d cannot update or delete another tenant's rows", updated == 0)


def test_owner_bypass() -> None:
    with psycopg.connect(host=PG_SOCKET, port=PG_PORT, user="mek_owner", dbname=DB) as c:
        c.execute("INSERT INTO lms.lesson (tenant_id, title) VALUES ('mek', 'L1'), ('kasina', 'L2')")
        c.commit()
        no_force = titles(c, "lesson")
        forced = titles(c, "course")
        c.commit()
    check(
        "2a table owner BYPASSES RLS when the table is not FORCEd (owner sees both tenants)",
        no_force == ["L1", "L2"],
        f"owner sees {no_force}",
    )
    check("2b FORCE ROW LEVEL SECURITY puts the owner under RLS too", forced == [], f"owner sees {forced}")
    with psycopg.connect(host=PG_SOCKET, port=PG_PORT, user="postgres", dbname=DB) as c:
        su = titles(c, "course")
    check("2c a superuser always bypasses RLS (never use one at runtime)", len(su) == 3, f"superuser sees {su}")


def test_set_local_scope() -> None:
    with app_conn() as c:
        as_tenant(c, "mek")
        during = titles(c)
        c.commit()  # the SET LOCAL value ends with the transaction
        after = titles(c)  # new transaction on the SAME connection
        c.rollback()
    check(
        "3a tenant set with SET LOCAL ends with the transaction (next transaction sees nothing)",
        during == ["Excel"] and after == [],
        f"during={during} after={after}",
    )


def pooler_conn() -> psycopg.Connection:
    return app_conn(port=POOL_PORT, host="127.0.0.1")


def test_pooler_leak_and_safety() -> None:
    # pool_size = 1: every client transaction runs on the same server connection.
    with pooler_conn() as a, pooler_conn() as b:
        a.execute("SET app.tenant_id = 'kasina'")  # PLAIN SET: session-level, the wrong way
        a.commit()
        leaked = titles(b)
        b.rollback()
    check(
        "4a DANGER: a plain SET leaks to the next client behind transaction pooling (demonstrated)",
        leaked == ["Baking", "Icing"],
        f"client B, who set no tenant, saw {leaked}",
    )
    with pooler_conn() as c:
        c.execute("RESET app.tenant_id")
        c.commit()

    with pooler_conn() as a, pooler_conn() as b:
        as_tenant(a, "kasina")
        titles(a)
        a.commit()
        safe = titles(b)
        b.rollback()
    check("4b set_config(..., true) / SET LOCAL does not leak behind the pooler", safe == [], f"client B saw {safe}")


def test_sqlalchemy_pattern() -> None:
    """The pattern for mek_kernel.db: tenant from a contextvar, applied at the start of every transaction."""
    tenant_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("tenant", default=None)
    engine = create_engine(
        f"postgresql+psycopg://mek_app@127.0.0.1:{POOL_PORT}/{DB}",
        pool_size=3,
        connect_args={"prepare_threshold": None},
    )

    @event.listens_for(Session, "after_begin")
    def _set_tenant(session: Session, transaction: object, connection: object) -> None:
        tenant = tenant_var.get()
        if tenant:
            connection.execute(text("SELECT set_config('app.tenant_id', :t, true)"), {"t": tenant})  # type: ignore[attr-defined]

    errors: list[str] = []

    def worker(tenant: str, expected: list[str]) -> None:
        tenant_var.set(tenant)
        for _ in range(150):
            with Session(engine) as s:
                got = sorted(r[0] for r in s.execute(text("SELECT title FROM lms.course")))
            if got != expected:
                errors.append(f"{tenant} saw {got}")
                return

    threads = [
        threading.Thread(target=worker, args=("mek", ["Excel"])),
        threading.Thread(target=worker, args=("kasina", ["Baking", "Icing"])),
        threading.Thread(target=worker, args=("nobody", [])),
    ]
    [t.start() for t in threads]
    [t.join() for t in threads]
    check(
        "5 SQLAlchemy after_begin hook: 3 tenants x 150 transactions in parallel through the pooler never cross",
        not errors,
        "; ".join(errors[:2]),
    )
    event.remove(Session, "after_begin", _set_tenant)
    engine.dispose()


def test_cost() -> None:
    with psycopg.connect(host=PG_SOCKET, port=PG_PORT, user="mek_owner", dbname=DB, autocommit=True) as c:
        c.execute("CREATE TABLE lms.bulk (id bigserial PRIMARY KEY, tenant_id text NOT NULL, title text NOT NULL)")
        c.execute(
            "INSERT INTO lms.bulk (tenant_id, title) SELECT 't' || (g % 20), 'course ' || g "
            "FROM generate_series(1, 200000) g"
        )
        c.execute("CREATE INDEX bulk_idx ON lms.bulk (tenant_id, id)")
        c.execute("CREATE TABLE lms.bulk_rls (LIKE lms.bulk INCLUDING ALL)")
        c.execute("INSERT INTO lms.bulk_rls SELECT * FROM lms.bulk")
        c.execute("ALTER TABLE lms.bulk_rls ENABLE ROW LEVEL SECURITY")
        c.execute(
            "CREATE POLICY p ON lms.bulk_rls FOR ALL TO mek_app "
            "USING (tenant_id = current_setting('app.tenant_id', true))"
        )
        c.execute("GRANT SELECT ON lms.bulk, lms.bulk_rls TO mek_app")
        c.execute("ANALYZE lms.bulk")
        c.execute("ANALYZE lms.bulk_rls")

    def bench(table: str, rls: bool) -> float:
        samples = []
        with app_conn() as conn:
            for _ in range(3):  # warm up
                conn.execute(
                    f"SELECT id, title FROM lms.{table} WHERE tenant_id = 't7' AND id > 100000 ORDER BY id LIMIT 20"
                ).fetchall()  # type: ignore[arg-type]
            for _ in range(300):
                t0 = time.perf_counter()
                if rls:
                    as_tenant(conn, "t7")
                conn.execute(
                    f"SELECT id, title FROM lms.{table} WHERE tenant_id = 't7' AND id > 100000 ORDER BY id LIMIT 20"
                ).fetchall()  # type: ignore[arg-type]
                conn.commit()
                samples.append((time.perf_counter() - t0) * 1000)
        return statistics.median(samples)

    plain = bench("bulk", False)
    # The plain table has no policy but the app role must still be able to read it (no RLS enabled).
    rls = bench("bulk_rls", True)
    over = rls - plain
    check(
        "6 cost: indexed tenant query on 200k rows, median ms per request including set_config",
        over < 1.0,
        f"without RLS {plain:.3f} ms; with RLS and set_config {rls:.3f} ms; overhead {over:+.3f} ms",
    )


def main() -> int:
    print("Spike C: PostgreSQL row-level security\n")
    setup()
    test_isolation()
    test_owner_bypass()
    test_set_local_scope()
    test_pooler_leak_and_safety()
    test_sqlalchemy_pattern()
    test_cost()
    failed = [r for r in results if not r[1]]
    print(f"\n{len(results) - len(failed)} of {len(results)} checks as expected")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
