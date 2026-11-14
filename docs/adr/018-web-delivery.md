# 018. Web delivery and page-weight budget

- Status: Proposed (spike B in M0)

## Context
Learners are mostly on phones with weak connections. Course pages must also be searchable and shareable with previews.

## Decision
Pending spike B. Next.js with server rendering and mostly static public pages; a proposed budget of about 150 KB of JavaScript on public pages, measured on a throttled mid-range Android profile and enforced in CI.

## Consequences
Interactivity moves to small islands if the budget does not hold.
