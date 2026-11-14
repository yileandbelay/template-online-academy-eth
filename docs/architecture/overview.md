# Architecture overview

The template is a **modular monolith** on the Mek platform architecture: one deployable application made of strictly
separated blocks. A product is a configuration of blocks.

## Layers

```
Product pack      manifest · theme · pages · content · extensions         (per client)
Blocks            business · integrations · automation · compliance       (as products need)
Contracts         events · ports · queries · shared types                 (slow, versioned)
Kernel            tenancy · identity · permissions · audit · settings ... (slowest)
```

Each layer depends only on layers below it. Products contain no shared code. **Blocks meet only through contracts.**
Dependencies are enforced by `import-linter` (layers) and an AST check (blocks never import each other); see
`backend/kernel/mek_kernel/registry/boundaries.py`.

## The kernel

Platform services every block uses. The kernel only gains a capability when at least three blocks need it.

| Component | Status for v1 | Folder |
|---|---|---|
| Tenancy, identity, authorization, audit | Build (M1) | `tenancy/`, `auth/`, `audit/` |
| Settings, numbering, documents, localization, calendar, money | Build (M1) | `settings/`, `numbering/`, `documents/`, `i18n/`, `calendar/`, `money/` |
| Events (outbox and inbox), jobs, files, search | Build (M1) | `events/`, `jobs/`, `files/` |
| Module registry, gateway, administration, observability | Build (M1); registry exists | `registry/`, `http/`, `api/` |
| Custom fields, workflows, licensing, offline sync | Later | `customfields/`, `workflows/`, `licensing/`, `sync/` |

Folders exist now with a note saying which milestone fills them.

## Blocks

A block has the same structure every time (the generator creates it): `manifest.yaml`, README, its own schema, settings,
HTTP API, event handlers, query interface, adapters, migrations, UI package, and unit, contract and security tests. A
developer connects blocks by reading manifests and READMEs, not code. See the [block catalogue](block-catalogue.md).

Families: `compliance.*`, `integrations.*`, `automation.*`, `ai.*`, `business.*`, and `client.*` for one client's extensions
(in that client's repository). The online-learning template uses eleven blocks.

## How blocks talk

| Mechanism | Use when | Example |
|---|---|---|
| **Event** | Something happened and the sender needs no answer | `payment.confirmed@1`: the learning block enrols the student, notifications sends the receipt, reports updates revenue |
| **Port** | A capability with an answer from a provider that may vary | `PaymentProviderV1` served by the manual or the Chapa adapter |
| **Query interface** | Reading another block's data | `PartyQueryV1.get()` for a student's name |
| **HTTP API** | Front ends, extensions and outside systems | The web app lists courses |

Inside one installation, blocks never call each other over HTTP, never join each other's tables and never import each
other's code.

### Events
Written to an **outbox** table in the same transaction as the business change, so nothing is lost and nothing is sent for a
change that rolled back. A relay delivers to handlers, which record processed ids in an **inbox** (idempotent). Delivery is
at least once; order is guaranteed per subject only. Payloads carry ids and amounts, **never personal data**. The envelope
is CloudEvents 1.0 (`mek_contracts.events.EventEnvelope`).

## Data
- Each block owns one PostgreSQL schema; only that block's code writes it. Blocks refer to other blocks' records by
  `DocumentRef`, never by foreign key.
- Every tenant table has a `tenant_id` and forced row-level security.
- Money is `Decimal` with an ISO 4217 currency, never a float. ETB is the default. Time is stored in UTC; the calendar
  (Gregorian or Ethiopian) is chosen at display time.

## Security by default
Tenant taken only from the verified token; deny by default (every route requires a declared permission, startup fails
otherwise); strict input (unknown fields rejected); no raw SQL; sensitive fields encrypted and never in events; secrets out
of code; idempotency keys on money operations; verified webhooks (payment confirmed by a server-side status call, never by a
redirect); audit of money, roles, prices, exports and erasure.

## Products
A product is a **manifest**: product name, domains, languages, calendar, currency, blocks and settings, plus a theme, pages,
content and optional extensions. The installer (M6) turns it into a running system; until then `mek-kernel validate`
checks it and `resolve` orders the blocks. See [Product packs](../guides/product-pack.md).

## Technology
Python 3.12+, FastAPI, Pydantic, SQLAlchemy 2, Alembic, PostgreSQL; Keycloak for identity (spike A); React and Next.js for
the web (spike B); MinIO for files; Jinja2 and WeasyPrint for documents; Traefik; Docker Compose; OpenTelemetry. Tooling: uv,
Ruff, mypy, pytest, pnpm, ESLint, Playwright. Decisions are in the [ADRs](../adr/README.md).
