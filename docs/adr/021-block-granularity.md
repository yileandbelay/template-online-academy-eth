# 021. Block granularity

- Status: Proposed

## Context
Every block has fixed overhead (manifest, schema, migrations, tests, README, UI package).

## Decision
About twelve blocks for v1 (see the plan, section 6). A new block needs a clear second-sector use and a narrow contract. Discussion and announcements stay inside business.lms until a second sector needs them.

## Consequences
A course stays in business.lms and is referred to elsewhere by DocumentRef; no generic shared catalogue in v1.
