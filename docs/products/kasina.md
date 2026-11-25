# Kasina

The second client: **Kasina Pastry Academy**, an online academy built by Hulu Software Labs PLC on this template (ADR-023).
It starts from `templates/elearning/online_academy.yaml`; its pack is `products/kasina/`.

**Specification:** [`docs/products/kasina/`](kasina/README.md). For UI/UX the owner's
[KPA-04 PDF](kasina/source/KPA-04_UI_UX_Design_v1.1.pdf) governs (D-08). Decisions are in
[DECISIONS.md](kasina/DECISIONS.md); conflicts with this template are K-01 to K-15 in
[DISCREPANCIES.md](kasina/DISCREPANCIES.md). K-02 (8-week plan vs roadmap M8) must be decided before planning.

Most questions below are now answered by the pack; the open ones are tracked in its DECISIONS "Still open" table.

## To confirm with the owner
- Exact product name, domain and whether a www redirect scheme like Mek Academy's is wanted
- Languages and default language; Ethiopian or Gregorian calendar by default; currency
- Payment channels (online gateway, bank transfer, Telebirr), and whether partial payments are allowed
- Video host (Bunny, VdoCipher, external links)
- Enrolment policy: public catalogue with locked lessons (as Mek Academy), or invitation only
- Certificate wording, signatures and verification page
- Course categories, first courses and instructors; who provides the content
- Reviews, announcements and discussion: on or off
- Anything Kasina needs that Mek Academy does not (this decides whether it is a setting, a block feature or an extension)
- Launch date, which sets the priority of milestones

## Why it matters
Kasina is the proof of reuse (M8): it should launch from the template with manifest, settings, theme, pages and content
only. Any change to a shared block that Kasina forces is counted and reviewed.
