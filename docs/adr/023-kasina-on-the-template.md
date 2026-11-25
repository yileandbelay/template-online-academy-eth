# 023. Kasina Pastry Academy is built on this template

- Status: Accepted (direction); open conflicts listed in `docs/products/kasina/DISCREPANCIES.md`
- Date: 2026-11-25

## Context
Hulu Software Labs' documentation pack for Kasina Pastry Academy (v1.2, in `docs/products/kasina/`) says in D-01 that the
platform is built from scratch in a new repository, and in D-02 that the stack is React + TypeScript + Vite with a
TypeScript Fastify API. This template is Python (uv workspace, `mek_kernel`, blocks) and plans Next.js for the web
(ADR-018, proposed). Kasina is already this template's second client (ADR-015, roadmap M8).

## Decision
The owner chose to build Kasina on this template (2026-11-25). This supersedes Kasina D-01 and D-02 (recorded there as
D-07). The Kasina pack stays the product specification: its screens, rules and requirements still govern *what* is built.
This repository's architecture rules govern *how* (blocks, contracts, kernel, product pack).

## Consequences
- The Kasina pack's stack-specific parts (React/Vite, Fastify, `packages/*` layout, `packages/domain` in TypeScript) no
  longer apply as written. Each affected point is a discrepancy to be decided, not changed silently.
- The template roadmap puts Kasina at M8, after M0 to M7 (rough sum 178 to 270 days). The Kasina pack plans 8 weeks
  (D-05). Both cannot hold; this is discrepancy K-02 and needs an owner decision before M1 work is planned around Kasina.
- Kasina-specific behaviour that no setting covers becomes a block feature (if a second client would use it) or a
  `client.*` extension, per the template rules. Each one is counted (M8 measures reuse).
