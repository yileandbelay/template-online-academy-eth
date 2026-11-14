# Spike C: row-level security with SET LOCAL through a pooler

Throwaway spike code (not part of the build). Result: **GO**. See `docs/spikes/m0-report.md`.

## Run it yourself
Needs PostgreSQL 16 and PgBouncer (`sudo apt install postgresql-16 pgbouncer`), or the services from `docker-compose.dev.yml`.

```bash
# a scratch cluster (as a non-root user), port 5544, socket in /tmp/pgspike
initdb -D /tmp/pgspike/data -A trust -E UTF8
pg_ctl -D /tmp/pgspike/data -o "-p 5544 -k /tmp/pgspike" -l /tmp/pgspike/log start
# PgBouncer in transaction mode with ONE server connection (worst case for leaks)
cp pgbouncer.ini.example /tmp/pgspike/pgbouncer.ini
printf '"mek_app" ""\n"mek_owner" ""\n"postgres" ""\n' > /tmp/pgspike/userlist.txt
pgbouncer -d /tmp/pgspike/pgbouncer.ini
# the checks
uv run --with 'psycopg[binary]' --with sqlalchemy python spikes/c_rls/rls_spike.py
```

## What it proves
1. Forced RLS isolates tenants for reads, updates and deletes; `WITH CHECK` blocks writing another tenant's row; with no tenant
   set the app sees nothing and cannot write (fails closed).
2. A table owner bypasses RLS unless the table is `FORCE`d, and a superuser always bypasses it: the application must connect as
   a role that owns nothing and has no `BYPASSRLS`; migrations run as a separate owner role.
3. Tenant set with `set_config('app.tenant_id', :t, true)` (SET LOCAL) ends with the transaction.
4. Behind PgBouncer in transaction mode a plain `SET` **leaks** to the next client (demonstrated); the per-transaction form does not.
5. A SQLAlchemy `after_begin` hook that reads the tenant from a context variable keeps three tenants apart under parallel load
   through the pooler.
6. Cost: about 0.2 ms extra per request on an indexed 200k-row table, including the `set_config` round trip.

## Rules this gives the kernel (`mek_kernel.db`, milestone M1)
- Tenant comes only from the verified token, never from request data.
- Set it with `set_config(..., true)` at the start of every transaction (a session `after_begin` hook), never with plain `SET`.
- App role: not owner, no `BYPASSRLS`. Owner role only for migrations. Tables: `ENABLE` and `FORCE` row-level security; one
  `tenant_isolation` policy with `USING` and `WITH CHECK`; an index starting with `tenant_id`.
- Behind a transaction pooler disable server-side prepared statements (`prepare_threshold=None` for psycopg) or use PgBouncer 1.21+
  `max_prepared_statements`.
- Every block gets an isolation test (the generated security test folder is where it goes).
