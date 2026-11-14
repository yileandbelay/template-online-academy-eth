# Development guide

Local development only; there is no server to deploy to (ADR-016).

## Set up
Install [uv](https://docs.astral.sh/uv/); it installs Python 3.12 for you. Node 22 and pnpm are needed for the web apps
(from M0 week 3). Docker is only needed for local services.

```bash
make setup                                  # uv sync --all-packages
make check                                  # lint, types, import boundaries, tests: what CI runs
make test                                   # tests only
make fmt                                    # format and fix imports
uv run mek-kernel validate products/mek-academy/product.yaml --blocks backend/blocks
uv run mek-kernel catalogue                # regenerate docs/architecture/block-catalogue.md
docker compose -f docker-compose.dev.yml up -d    # local PostgreSQL when a task needs it
```

## Renaming the platform brand
The brand word is provisional (ADR-022). To change it everywhere (packages, folders, commands, event namespace, prose):

```bash
uv run python tools/rebrand.py --old mek --new <word> --dry-run    # preview
uv run python tools/rebrand.py --old mek --new <word>
uv sync --all-packages && make check
```
Do this before the first deployment; stored events carry the namespace.

## Workflow
1. The owner gives a **green light** for a task or milestone.
2. Work on a branch named `claude/<topic>`, in small slices. Never push to `main`.
3. Every slice has tests and passes `make check`. Regenerate the catalogue if a manifest changed (a test fails otherwise).
4. Open a pull request with what changed, what is not included and the test results. CI must be green.
5. The owner says **merge**. Then the next slice starts.

## Definition of done (for a slice)
- Checks green on Python 3.12 and 3.13; tests added for every behaviour.
- Manifest, README and CHANGELOG updated for any block touched; catalogue regenerated.
- A decision that was not obvious has an ADR.
- No untranslated strings in enabled language packs; glossary terms respected.
- No personal data in events or logs; permissions declared for every route.

## Where things live
See the table in the repository `README.md`. Architecture is in `docs/architecture/`; the plan in `docs/plan/`.
