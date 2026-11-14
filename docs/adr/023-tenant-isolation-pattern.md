# 023. Tenant isolation with row-level security

- Status: Proposed (from spike C, 12 of 12 checks passed)
- Date: 2026-11-14

## Context
Every tenant table must be isolated even when application code has a bug, and the pattern must survive a connection pooler.
Spike C tested it on PostgreSQL 16 with PgBouncer in transaction mode (`docs/spikes/m0-report.md`).

## Decision
- The tenant comes only from the verified token, never from request data.
- It is set at the start of every transaction with `set_config('app.tenant_id', :t, true)` (SET LOCAL), through a SQLAlchemy
  `after_begin` hook that reads a context variable. A plain `SET` leaks to other clients behind a pooler and is forbidden.
- The application role owns nothing and has no `BYPASSRLS`. A separate owner role runs migrations. A table owner bypasses RLS
  unless the table is `FORCE`d, so tables are both `ENABLE`d and `FORCE`d.
- One `tenant_isolation` policy per table, with `USING` and `WITH CHECK`; no tenant set means no rows and no writes (fails closed).
  An index starting with `tenant_id`.
- Behind a transaction pooler, server-side prepared statements are disabled (or PgBouncer 1.21+ prepared-statement support is used
  and tested).
- Every block has an isolation test.

## Consequences
About 0.2 ms extra per request. Migrations and background jobs must also set the tenant explicitly. Shared SaaS stays possible
without a rewrite.
