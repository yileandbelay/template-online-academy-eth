# 022. Platform brand name

- Status: Accepted (provisional)
- Date: 2026-11-14

## Context
The platform was first named after the owner's company. Whether the company can use that name is still to be decided, and a
new company may be created under another name. Meanwhile the first product is called Mek Academy.

## Decision
- The code brand is **Mek** for now: packages `mek_kernel`, `mek_contracts`, `mek_<block>`; command line `mek-kernel`; event
  namespace `et.mek.*`; schema URIs `mek:contracts/...`.
- **Mek** is the platform and brand; **Mek Academy** is the first product, configured by `products/mek-academy/`. The
  template itself still contains nothing specific to one product.
- Renaming is one command: `uv run python tools/rebrand.py --old mek --new <word>` (tested), followed by `uv sync
  --all-packages`, regenerating the catalogue and `make check`.

## Consequences
- Rebrand **before the first deployment**. The event namespace is stored in the outbox and in event schemas, so after real
  data exists a rename needs a migration of stored events.
- If the platform brand changes, the product name "Mek Academy" is not renamed automatically; decide that separately.
- Documents that name the old brand (for example the internal architecture specification) are not copied here, so nothing in
  this repository depends on them.
