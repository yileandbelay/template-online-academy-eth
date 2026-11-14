# Roadmap

Status as of 14 November 2026. Developed locally; nothing is deployed (ADR-016). Estimates are rough working days for one
stream, mostly written by Claude and reviewed by the owner; they are re-estimated at each gate.

| Milestone | What | Estimate | Status |
|---|---|---|---|
| **M0 Foundations and spikes** | Monorepo, CI, generator, ADRs; spikes: Keycloak, page weight, row-level security, local Compose footprint | 10 to 15 d | **In progress.** Week 1 done: skeleton, contracts, registry, generator, CI. Docs and block skeletons in review |
| **M1 Kernel walking skeleton** | Tenancy, identity, authorization, audit, settings, numbering, i18n, calendar, events, jobs, files, registry | 25 to 35 d | Not started |
| **M2 Shared blocks, wave 1** | Parties, notifications, payments (manual and Chapa), documents, contact, tax | 20 to 30 d | Not started |
| **M3 Online-learning core** | Courses, lessons, enrolment, access policy, progress, search, video | 30 to 40 d | Not started |
| **M4 Exams, certificates, feedback, reports** | Assessments, certificates with frozen URLs, reviews, reports, imports | 18 to 25 d | Not started |
| **M5 Web apps** | Public site, learner area, admin console, component library | 45 to 65 d | Not started |
| **M6 Product layer and operations kit** | Installer, backup and restore, dashboards, security pass | 15 to 25 d | Not started (deployment deferred) |
| **M7 Mek Academy migration and cutover** | Data migration, password strategy, URL compatibility, parity report | 15 to 20 d | Not started |
| **M8 Second product proof** | Kasina on the template with configuration only; measure reuse | 10 to 15 d | Not started |

## Gates
- **Gate 0 (end of M0):** spike results and a go or no-go.
- **Gate 1 (end of M1):** kernel skeleton works end to end locally.
- **Gate 2 (end of M5):** template v1 usable by a new product.
- **Gate 3 (end of M7):** parity report; go or no-go on moving Mek Academy.

## M0 checklist
- [x] Repository, uv workspace, CI (Ruff, mypy, import-linter, pytest on Python 3.12 and 3.13)
- [x] Manifests, registry resolver, event envelope, shared types
- [x] Block generator
- [x] ADRs 015 to 021
- [x] All planned blocks created as proposed skeletons; kernel folders; QA folders; product packs for Mek Academy and Kasina
- [x] Block catalogue generated from manifests; docs
- [ ] Spike A: Keycloak footprint, Amharic sign-up, invitations, Mek Academy password migration
- [ ] Spike B: page weight of catalogue, course and lesson pages (Next.js) on a throttled phone profile
- [ ] Spike C: PostgreSQL row-level security with `SET LOCAL` through a pooler
- [ ] Spike D: local Docker Compose footprint (memory) of the full stack
- [ ] Spike report and Gate 0 recommendation

## Out of scope for the first release
Telegram delivery, installable offline lessons, Telebirr direct, coupons, subscriptions, cohorts and seat licences,
question banks, AI features, on-premise licensing, shared SaaS tenancy, any deployment. See the plan for the reasons.
