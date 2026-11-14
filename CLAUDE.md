# Working notes for Claude

This repo is the **Online Academy for Ethiopia template**: reusable blocks for online learning on the Mek platform
architecture. Read `docs/plan/` and `docs/adr/` before changing structure.

## How we work
- **Local development only.** Do not create servers, deployments or cloud accounts. Deployment waits until the product
  matures (ADR-016).
- The owner gives a **green light** before a milestone or task starts and says **merge** before a pull request is merged.
  One small pull request per slice, with tests and a short description. Never push to `main`.
- Never create repositories, hosts or accounts. Never touch the live Mek Academy server or its data (a different repo).
- Report outcomes faithfully: failing tests, skipped steps and estimate changes are stated plainly.

## Commands
`make setup` · `make check` (what CI runs) · `make test` · `make fmt` · `make new-block ID=<family>.<name>`

## Architecture rules (from the Mek spec)
- Layers: product pack → blocks → contracts → kernel. Each depends only on layers below. `mek_kernel` imports no other
  Mek package; blocks import only `mek_kernel` and `mek_contracts`; blocks never import each other.
- Blocks own their schema; refer to other blocks' records by `DocumentRef`, never by foreign key.
- Events go through the outbox in the same transaction; payloads carry ids and amounts, never personal data.
- Money is `Decimal` with an ISO 4217 currency, never a float. Time is UTC; calendar is chosen at display.
- Domain rules are plain Python (no FastAPI, no SQLAlchemy). Every route requires a declared permission.
- English is the code language; Amharic is a language pack with a glossary (`languages/am/glossary.yaml`). Never change a
  glossary term without owner approval.
- Client-specific behaviour is an extension in the client's own repository, never a change to a shared block.
- A new block needs a clear second-sector use; create it with `new-block`, never by hand.

## Style
Ruff (line length 120), mypy strict on source, pytest. Tests for every behaviour. Admin labels are English by default.
