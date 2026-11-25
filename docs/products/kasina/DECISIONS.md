# Decision log

Owner decisions override any earlier conflicting text in KPA-01, KPA-02, KPA-04 or the frontend brief. Edited sentences in those documents are tagged `[v1.2: D-xx]`. Claude Code must not change a decision. If a decision blocks something, record it in `docs/DISCREPANCIES.md` and stop for owner review.

Owner: Yilkal (Hulu Software Labs PLC), building for Kasina Pastry Academy.

## Decided

| ID | Date | Decision | Consequences in the documents |
| --- | --- | --- | --- |
| D-01 | 2026-11-25 | *(Superseded by D-07.)* Hulu Software Labs builds the platform **from scratch** in a new repository. No existing codebase is reused or referenced. | All references to earlier code reuse removed. Inspect the repository only for conventions Hulu has already set up in it. |
| D-02 | 2026-11-25 | *(Superseded by D-07.)* Stack: **React + TypeScript + Vite** installable PWA; **TypeScript Fastify** API; PostgreSQL 16 with migrations; PostgreSQL-backed job queue; monorepo as in KPA-02. | The Flask/Jinja option is closed. Shared typed contracts (`packages/contracts`) and UI (`packages/ui`) serve the public site, all three portals and the Phase 2 Telegram Mini App. |
| D-03 | 2026-11-25 | **One administrator is sufficient.** | No feature may require a second administrator. Bank-account changes alert the administrator's own verified phone by SMS and in-app, instead of "notify other owner/admin". The system still supports several admins. Keep: prevent disabling the last active administrator; per-administrator message read state. |
| D-04 | 2026-11-25 | **No MFA in Phase 1.** Staff sign in with phone + SMS OTP, like students. | Removed: TOTP, recovery codes, MFA setup/challenge screens, "Additional authentication" controls (INS-004, ADM-020), mock staff MFA, `/auth/mfa`, MFA tables. Kept: session revocation, active sessions, Sign out of other devices, audit, and a **step-up SMS OTP** for bank-account changes. Staff lost phone: the admin re-points the number (audited, sessions revoked). Only admin lost phone: Hulu operator command on the server (audited, in the runbook). Keep authentication in one module so MFA can be added later. |
| D-05 | 2026-11-25 | **8 weeks in total: Phase 1 in weeks 1–4, Phase 2 in weeks 5–8.** | The KPA-02 "re-estimate" note is replaced. `BUILD_PLAN.md` gives the weekly plan. The frontend brief's "complete mock frontend, then backend" sequence is replaced by weekly vertical increments (see D-06). Phase 2 detail is added as SRS R-P2-01 to R-P2-09 and a KPA-02 Phase 2 section. |
| D-06 | 2026-11-26 | Implementation approach to fit D-05: **contracts first, business rules implemented once, vertical slices weekly.** | Rules (progress, 90% coverage merge, quiz grading, completion, renewal expiry, report queries) live in `packages/domain` and run on the server. Mock adapters return fixture results through the same contracts and never reimplement rules. Mocks exist only for endpoints not yet built and are removed when the real endpoint lands. The owner reviews staging at the end of every week. *(Proposed by the reviewer and adopted in this pack; the owner can revise.)* |
| D-07 | 2026-11-25 | The platform is **built on the Online Academy for Ethiopia template** (`yileandbelay/template-online-academy-eth`, Python, Mek block architecture) instead of from scratch. **Supersedes D-01 and D-02.** | See ADR-023. This pack still specifies what is built; the template's rules govern how. Stack- and layout-specific text in KPA-02, the frontend brief, the build plan and the pack's CLAUDE.md is open until each conflict in `DISCREPANCIES.md` (K-01 onwards) is decided. |
| D-08 | 2026-11-25 | **All frontend UI/UX comes from the owner's `source/KPA-04_UI_UX_Design_v1.1.pdf`** (116 pages: layouts, visuals, controls, copy, states, desktop and mobile). It replaces `KPA-04_UI_UX.md` and `screens/*.png` as the UI/UX authority. | The Markdown and the PNGs (static reconstructions) are convenience copies only; where they differ from the PDF on anything visual or interactive, the PDF governs, and the difference is logged in `DISCREPANCIES.md`. Exception pending owner confirmation (K-14): the PDF still shows staff TOTP MFA, recovery codes, "Additional authentication" and "notify other owner/admin", which D-03/D-04 removed. |

## Still open (do not invent; use a configurable default where the text proposes one)

| Item | Where | Default to implement until decided |
| --- | --- | --- |
| Video options: Bunny, YouTube and Kasina server are all specified. Each needs a playback-coverage test before use on required lessons. The reviewer suggested Bunny only for Phase 1. | ACD-003, ACD-004, ADM-018, KPA-02 Media | Build the provider interface. Bunny first (week 1 test). YouTube and Kasina server are enabled only after their tests pass (ADM-018 toggles). |
| Access day semantics: elapsed 24-hour days vs Addis Ababa calendar days, and how expiry is displayed | R-CORE-04, KPA-02 Renewal | 24-hour periods from the confirmation instant; display the expiry date and time in Africa/Addis_Ababa |
| Session durations (student, staff) | KPA-02 | Configurable; propose student 30 days rolling, staff 12 hours idle / 7 days absolute |
| Practical upload limits, retention period | STU-008, ACD-006, ADM-018 | 3 minutes / 100 MB test envelope, configurable; no automatic deletion until retention is approved |
| Refund and adjustment policy; no-refund wording | R-CORE-05, ADM-006 | Correction records only; no refund UI beyond what is specified |
| Stale open orders: expiry and requote | KPA-02 Renewal | Admin cancels manually; configurable expiry off by default |
| Pass mark, retakes, scoring | STU-007, ACD-005 | 80%, unlimited during access, no timer, equal weights (as specified) |
| Course-group rename/merge/reorder/archive | PUB-004 | Rename, reorder and archive; merge deferred |
| Recipients of announcements, academy-wide announcements | ACD-011 | Students with active access; academy-wide not built |
| Inquiry reply mechanism for public visitors | ADM-011, ADM-012 | Admin replies outside the system and records an internal note (as specified) |
| Legal name, contacts, social links, bank accounts, logo, photos, accreditation wording, certificate artwork, terms/privacy | Release gates | Placeholders clearly marked; release blocked until supplied |
| Native Amharic copy | PUB-001, release gates | Draft keys with English fallback flagged in the UI string report |
| Data hosting in Europe vs Ethiopian personal data law (Proclamation 1321/2024) | Architecture Spec, KPA-02 Deployment | Owner to confirm before production procurement |
| Telegram digital-goods payment rules | R-P2-07 | Gate in week 5 |

## Change log

- v1.3 (2026-11-25): D-07 recorded (build on the template); D-08 recorded (the KPA-04 PDF governs UI/UX); pack moved into the template repository under `docs/products/kasina/`.

- v1.2 (2026-11-26): applied D-01 to D-06; converted KPA-04 to Markdown with per-screen images; added Phase 2 requirements, build plan, traceability matrix and CLAUDE.md.
- v1.1 (2026-11-25): synchronized KPA-01, KPA-02, KPA-04 and the frontend brief (owner package).
