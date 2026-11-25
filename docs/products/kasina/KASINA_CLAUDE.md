# CLAUDE.md — Kasina Pastry Academy platform

Hulu Software Labs PLC is building Kasina Pastry Academy's online learning platform from scratch. Phase 1 (weeks 1–4) is a bilingual web app and installable PWA with a public site and Student, Instructor and Admin portals. Phase 2 (weeks 5–8) adds the Telegram Mini App and online payment (Chapa). The owner (Yilkal, Hulu) reviews every week.

## Read before any work

1. `docs/DECISIONS.md` — owner decisions; they override everything else.
2. `docs/KPA-04_UI_UX.md` — **master product specification** (screens, rules), with pictures in `docs/screens/<ID>.png`.
3. `docs/KPA-01_SRS.md` — formal requirements (R-CORE, R-<screen ID>, R-P2).
4. `docs/KPA-02_Architecture.md` — technical design, data model, transactions, API, security, operations.
5. `docs/BUILD_PLAN.md` — what is built which week.
6. `docs/FRONTEND_BRIEF.md` — frontend rules, fixtures and review controls.
7. `docs/TRACEABILITY.md` — screen → requirement → route → status. Keep it current.

For a task, read the relevant screen sections in full and the R-CORE rules they depend on. The PDFs in `docs/source/` are originals for reference only; do not use them as requirements.

**Authority when documents conflict:** DECISIONS > KPA-04 (for UI/UX: the PDF in `source/`, D-08) > KPA-01 > KPA-02 > FRONTEND_BRIEF > pictures. In this repository, `KASINA_CLAUDE.md` is read for product rules only; the repository `CLAUDE.md` and ADR-023 govern stack and layout (D-07). Never resolve a conflict silently. Add it to `docs/DISCREPANCIES.md` (date, documents, the conflicting text, the option you propose), then follow the higher authority or stop if it blocks.

## Non-negotiables

- **No invented features.** Implement only what the documents specify. "Proposed", "pending" and "validation / configuration" items get a configurable default (see DECISIONS "Still open") and an entry in the README's unresolved decisions, never extra functionality.
- **No MFA in Phase 1** (D-04). Everyone signs in with phone + SMS OTP. A step-up OTP is required for bank-account changes. Keep auth in one module so MFA can be added later.
- **One administrator is enough** (D-03). No feature may require a second admin. Keep the last-active-admin guard.
- **Business rules live once** (D-06): in `packages/domain`, executed by the API. That covers progress, 90% merged playback coverage, quiz grading, completion, renewal expiry, revenue and cohort queries. The frontend displays server results. Mock adapters return fixtures through the same contracts and are deleted when the real endpoint exists.
- **Server-side authorization on every request and object** (role, course scope, ownership, state). Never trust the client's role, price, amount or course ID.
- **Money and time:** integer ETB minor units; ISO UTC in storage and API; Africa/Addis_Ababa for reporting dates and display; Gregorian display baseline.
- **Payments:** confirmation is one atomic, idempotent transaction (lock order, then enrollment). Duplicate references are blocked. A rejection needs a reason. History is never edited; corrections are separate records. Notifications are sent outside the transaction, via the outbox.
- **Media:** Bunny private library, signed short-lived links, allowed domains, MediaCage, visible student-code watermark. No permanent provider keys in the browser. Practical videos and receipts are private, separate from teaching media, and served by short-lived signed reads only. Never cache private media, receipts or authenticated API responses in the service worker.
- **Secrets** stay out of the repo, logs and frontend. Never log full receipts or OTPs.
- **Language:** Amharic default, English optional. The gold አማ / EN pill sits at the far right of every header and keeps the route and unsaved state. Every string uses an i18n key. Content language is independent of interface language.
- **UI states:** every list has loading, empty, filtered-empty and error/retry states; every form has validation, saving, success, failure and unsaved-change warnings. Accessible labels, keyboard use, contrast and touch targets. Test at 360px width. No horizontal page overflow; on mobile, tables become cards.
- **Explicitly not wanted:** carousels, autoplay, popups, fake statistics, ratings, countdowns, gamification, cart, live chat, a website builder, a question bank, timed exams, QR certificate verification, retail ordering, a separate Telegram app.

## Stack and layout (D-02)

React + TypeScript + Vite PWA; TypeScript Fastify API under `/api/v1`; PostgreSQL 16 with migrations; PostgreSQL-backed job queue; Docker; Caddy or equivalent for TLS; Cloudflare DNS; OVH VPS (Europe).

```
apps/web            React PWA (public site, student, instructor, admin; Telegram shell in Phase 2)
apps/api            Fastify modular monolith: identity, catalog/content, learning/assessments,
                    payments/access, certificates, messaging/notifications, reporting/settings/audit
packages/contracts  Zod schemas + OpenAPI; shared request/response types
packages/domain     Pure business rules (no I/O), fully unit-tested
packages/ui         Design tokens and shared components
packages/i18n       Translation keys (am default, en)
migrations/         SQL migrations
tests/              Integration, permission-matrix, e2e
docs/               Specifications (this pack), spikes/, DISCREPANCIES.md, runbook
```

Set up the commands in week 1 and record them here: install, dev, typecheck, lint, test, build, migrate, seed demo data, e2e.

## Workflow

- One task = one short brief: which screen IDs and requirements, acceptance checks, out of scope. Keep each change small enough to review. Commit in small steps with messages that cite the screen or requirement IDs.
- Before marking work done, run typecheck, lint, unit, integration and permission tests and the build. Check the screen at 360px, tablet and desktop, in Amharic and English. Update `docs/TRACEABILITY.md`.
- At the end of every week (BUILD_PLAN), stop for owner review on staging. Show the week's screen IDs on desktop and mobile, the test results and the known gaps.
- Write spike results to `docs/spikes/<topic>.md` with what was measured, on which device and network, and the result.
- Never claim production readiness, exact visual fidelity, or that a provider or limit works without a test showing it.
- If a week's plan cannot be met, say so at the review and propose what moves (BUILD_PLAN lists the suggested order). Do not cut scope silently.

## Design tokens

Gold #CF8F11 · deep gold #946309 · champagne #F8EDD3 · warm white #FFFDF8 · white #FFFFFF · charcoal #252525. Gold buttons use dark text; links are deep gold; no gradients; roughly 75/15/10 balance. Fonts: Playfair Display for English marketing headings, Inter for UI, Noto Sans Ethiopic for Amharic. Lucide icons. Breakpoints 640/1024/1440. Public pages are photographic, the student portal calm, the instructor portal a light sidebar, the admin portal a charcoal sidebar.

## Demo and test data

Use one deterministic fixture set (FRONTEND_BRIEF "Mock scenarios"):
- two certificate courses and two short courses, one of them free
- an admin and assigned instructors
- students with active, expired and completed enrollments
- pending, rejected and confirmed payments, a renewal and a complimentary grant
- quiz attempts, and practicals pending, passed and resubmit

Totals always derive from the data. Include a demo reset and a test-only role switch that is never available in production.
