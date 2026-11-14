# Adding a block

A new block needs a clear use by at least two sectors or products and a narrow contract. If only one client needs it, it is
a setting or a client extension instead (see [Product packs](product-pack.md)). Discussion and announcements, for example,
stay inside `business.lms` until a second sector needs them.

## Steps
1. Create it: `make new-block ID=business.example` (family one of `compliance`, `integrations`, `automation`, `ai`, `business`).
2. Fill in `manifest.yaml`: summary, what it provides and requires, events emitted and consumed, permissions, settings model.
   Use `status: proposed` until code exists, `incubating` once it is being built.
3. Write the README (purpose, interfaces, settings, permissions, security, known limits).
4. Add contracts it publishes under `backend/contracts/mek_contracts/` (events, ports, queries) in the same pull request.
5. Implement in this order: domain rules (plain Python) → services → models and migration with row-level security →
   handlers → API router (every route requires a permission) → adapters → UI package.
6. Tests: unit (rules, milliseconds), contract (events and API match the published contract), security (tenant isolation,
   permissions, boundaries). Handle `account.erased@1` if the block stores personal data.
7. Run `uv sync --all-packages`, `make check`, and `uv run mek-kernel catalogue`.
8. Add the block to the product templates that should include it and check they still resolve.

## What the build checks for you
- Block id, version, capability, event and permission names (manifest validators).
- The block imports only `mek_kernel`, `mek_contracts` and its own package.
- Every required capability has a provider; no dependency cycles; every consumed event has an emitter.
- The block has its README, changelog, tests and UI folder, and its settings model imports.
- The catalogue page is up to date.
