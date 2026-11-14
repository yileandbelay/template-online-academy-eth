# Glossary

| Term | Meaning |
|---|---|
| **Mek** | The platform's code brand (provisional, ADR-022): `mek_*` packages, `mek-kernel` command, `et.mek.*` events. |
| **Mek Academy** | The first product, an online academy, configured on the template by `products/mek-academy/`. Not the same thing as the platform. |
| **Block** | A reusable capability with its own data, API, events, settings, tests and README (for example `business.lms`). |
| **Kernel** | Platform services every block uses: tenancy, identity, permissions, audit, settings, numbering, documents, languages, events, jobs, files. |
| **Contracts** | The shared types, event models, port and query interfaces. The only thing blocks import from each other's world. |
| **Port** | An interface for a capability that has an answer and may be served by different providers, such as `PaymentProviderV1`. |
| **Adapter** | One provider behind a port, such as the Chapa adapter or the manual-payment adapter. |
| **Query interface** | A read-only interface one block publishes so another can read its data without touching its tables. |
| **Event** | A fact that happened, such as `enrollment.activated@1`, published through the outbox in the same transaction as the change. |
| **Manifest** | The YAML file that describes a block (`manifest.yaml`) or a product (`product.yaml`). |
| **Template** | A starting manifest for a type of product, such as `templates/elearning/online_academy.yaml`. |
| **Product pack** | Everything specific to one product: manifest, theme, pages, content, documents, optional extensions. |
| **Extension** | Client-specific code outside the shared blocks, using only the public API (`client.<client>.<name>`). |
| **Tenant** | One organisation's data space. For now one tenant per installation. |
| **Stage** | A block's maturity: proposed, incubating, beta, stable, deprecated, retired. |
| **Gate** | A review point in the plan where the owner decides whether to continue, change or stop. |
| **Parity** | The template can do everything the live Mek Academy does; the condition for moving Mek Academy onto it. |
