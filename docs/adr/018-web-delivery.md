# 018. Web delivery and page-weight budget

- Status: Proposed. Spike B is done: owner decision needed at Gate 0 (hybrid recommended)

## Context
Learners are mostly on phones with weak connections. Course pages must also be searchable and shareable with previews.

## Decision
Spike B result (`docs/spikes/m0-report.md`): Next.js 16 ships about 138 KB of JavaScript on every page (the framework floor); Mek Academy today ships none, and an islands build ships none on static pages and about 70 KB where a component is interactive. Recommended: public pages on an islands framework with the same React components, logged-in apps on Next.js (hybrid). Alternative: Next.js everywhere with progressive enhancement and a CI budget.

Criteria that were set: Next.js with server rendering and mostly static public pages; a proposed budget of about 150 KB of JavaScript on public pages, measured on a throttled mid-range Android profile and enforced in CI.

## Consequences
Interactivity moves to small islands if the budget does not hold.
