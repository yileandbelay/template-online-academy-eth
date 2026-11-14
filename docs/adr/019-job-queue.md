# 019. Background jobs

- Status: Proposed (settles spec ADR-003)

## Context
Emails, reminders and reports need a job queue. The spec proposes Procrastinate on PostgreSQL.

## Decision
Use Procrastinate unless the M1 skeleton shows a blocker. No extra broker for v1.

## Consequences
One fewer service to run; revisit at higher volume.
