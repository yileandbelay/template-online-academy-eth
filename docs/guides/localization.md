# Localization

English is the language of code, data and interfaces. Other languages are **language packs** held to a quality bar.
Selecting Amharic switches the whole experience (the admin console can keep English by a per-product setting).

| Area | Rule |
|---|---|
| Language | Developers write English only; every visible string is wrapped for translation. A product without packs is English-only. |
| Packs | `languages/<code>/pack.yaml` plus a glossary and one catalog per block. Amharic is `languages/am/`. |
| Glossary | `languages/am/glossary.yaml` lists decided terms. A term changes only by a pull request reviewed by a native speaker. |
| Coverage gate | A release needs 100 percent of strings translated in enabled packs (`coverage_gate` in `pack.yaml`). |
| Calendar | A separate setting. Defaults: Amharic uses the Ethiopian calendar, English the Gregorian; tenants and users can override. Storage, APIs, events and bank files are always Gregorian UTC. |
| Printed documents | Use the calendar configured for the template, not the viewer's. |
| Currency | ETB is the default in every language. |
| Fonts | Embedded Ethiopic fonts in PDFs and the web UI. |

## Decided Amharic terms (from Mek Academy)
- "Browse courses" is **ኮርሶችን ይምረጡ**.
- A bare "Browse" (no object) is **ያስሱ**. Never use ይምረጡ for any other "browse" string.

## Adding a language
Add `languages/<code>/pack.yaml` and a glossary, add translations per block, list the code in a product's `locale.languages`.
A native-speaker reviewer must be named in `reviewers` before the pack is enabled for a real product.
