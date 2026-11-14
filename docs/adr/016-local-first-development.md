# 016. Local-first development; deployment deferred

- Status: Accepted
- Date: 2026-11-14

## Context
The owner wants to develop locally and deploy only when the product matures.

## Decision
No host, server or cloud account is created now. Development, tests and spikes run locally and in GitHub Actions with fake data. The installer, backup and restore, and production hosting are scheduled for milestone M6 or later.

## Consequences
The Compose footprint spike runs on a local Docker stack. The host and its location (ADR-020) are decided later. Operations knowledge from Mek Academy (DNS, HTTPS, backups) is kept in the plan and applied in M6.
