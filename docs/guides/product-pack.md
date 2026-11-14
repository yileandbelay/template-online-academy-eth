# Product packs

The template contains nothing named after a client. Everything specific to one product lives in a **product pack**:
`products/<name>/`. While the template is developed locally the packs are in this repository; later each moves to its own
repository (ADR-015) and the platform stays untouched.

```
products/<name>/
├── product.yaml      manifest: name, domains, languages, calendar, currency, blocks, settings
├── theme/            design tokens (colours, fonts), logo, favicon, share image
├── pages/            home page sections, about, contact details, policy pages (English and Amharic)
├── content/          courses, categories, instructors, demo data (loaded through the imports block)
├── documents/        certificate and receipt templates and wording
├── extensions/       client.<name>.* blocks: empty unless the client needs behaviour no block offers
└── env/              environment values; secrets by reference only, never in the repository
```

## Starting a new product
1. Copy a template: `templates/elearning/online_academy.yaml` to `products/<name>/product.yaml`; set the name, domains,
   languages, calendar and currency.
2. List the blocks; remove those the client does not want (a compliance block stays mandatory for Ethiopia).
3. Set block settings in the manifest.
4. Add the theme, pages and content.
5. Check it: `uv run mek-kernel validate products/<name>/product.yaml --blocks backend/blocks`.
   A test also checks every pack and template on every build.

## Where does a difference belong?
| If the difference is... | ...it goes in |
|---|---|
| Name, colours, logo, wording, page layout, content | the product pack (manifest, theme, pages, content) |
| How an existing feature behaves (invite-only enrolment, payment channels, certificate on or off) | a **setting** of the block, set in the manifest |
| A capability only this client needs | a **client extension** in `extensions/`, using only the public SDK |
| A capability a second client also needs | **promoted into the shared block** (stage beta) with a versioned contract |

Never change a shared block for one client. If a setting is missing, add the setting to the block (with a safe default), not
a client-specific branch.

## Packs today
- [Mek Academy](../products/mek-academy.md): the reference product; its parity with the live site is the goal of M7.
- [Kasina](../products/kasina.md): the second client, an online academy; its details are still to be gathered.
