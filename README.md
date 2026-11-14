# Online Academy for Ethiopia template

A configurable template for building online-learning businesses in Ethiopia (English and Amharic), built from reusable
**blocks** on the Mek platform architecture. Mek Academy is the first product configured on it.

**Naming.** *Mek* is the platform's code brand (provisional; one command renames it, see ADR-022). *Mek Academy* is the first
product built on it.

Status: **M0, foundations and spikes.** Developed locally; nothing is deployed until the product matures (ADR-016).

## What is here

| Folder | Holds |
|---|---|
| `backend/kernel/` | `mek_kernel`: platform services (M0: manifests, registry, app factory) |
| `backend/contracts/` | `mek_contracts`: shared types, event envelope, ports and queries |
| `backend/blocks/` | One folder per block, made with `new-block`: eleven planned blocks as proposed skeletons (see the block catalogue) |
| `tools/new_block/` | The block generator |
| `templates/` | Product templates, for example `elearning/online_academy.yaml` |
| `products/` | Product packs: `mek-academy/` (reference) and `kasina/` (second client) |
| `languages/` | Language packs and glossary (Amharic) |
| `apps/` | Web shell, admin console, UI library (from M0 week 3 and M5) |
| `qa/` | Scenarios, test kit and fakes (grows from M1) |
| `docs/` | Plan, decisions (`docs/adr/`), block catalogue |

## Quick start (local)

Needs [uv](https://docs.astral.sh/uv/) (it installs Python 3.12 for you). Node 22 and pnpm are needed from week 3.

```bash
make setup      # uv sync --all-packages
make check      # lint, types, import boundaries, tests: what CI runs
make new-block ID=business.example      # create a block with the full structure
uv run mek-kernel validate templates/elearning/online_academy.yaml
docker compose -f docker-compose.dev.yml up -d   # local PostgreSQL, when a task needs it
```

## Rules in one paragraph

Blocks own their data and meet only through events, ports, queries and versioned HTTP; a block imports only
`mek_kernel` and `mek_contracts` (CI enforces it). Differences between clients are settings, templates or client
extensions, never changes to shared blocks. Every decision gets an ADR. Work goes in small pull requests; each is merged
only after the owner says "merge".

Start with [`docs/README.md`](docs/README.md) (index), the [roadmap](docs/roadmap.md) and the
[architecture overview](docs/architecture/overview.md). The plan is in `docs/plan/`.
