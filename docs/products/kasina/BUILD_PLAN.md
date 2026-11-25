# Build plan — 8 weeks (D-05)

Phase 1 covers all KPA-04 Phase 1 screens (54 screen IDs) on web and PWA, in weeks 1–4. Phase 2 covers Telegram and online payment (TG-001, R-P2-01 to R-P2-09), in weeks 5–8.

Every week ends with an owner review on staging: a desktop and mobile walkthrough of the week's screen IDs, the traceability matrix updated, and known gaps listed. Work proceeds in small commits, one brief per task (see CLAUDE.md).

**Schedule risk:** four weeks for the full Phase 1 scope is tight. If a week slips, raise it at that week's review, with a proposed list of what moves. Never cut silently. The suggested order for moving items (owner decides) is:
1. ADM-008 and ADM-009 charts (keep the tables and CSV)
2. ADM-015 and ADM-016 editors (developer edits the content meanwhile)
3. ADM-010 to ADM-012 messages (phone, Telegram and email links meanwhile)
4. Instructor public profile on About (INS-004 visibility)

## Week 0 (before day 1, owner and Kasina)

Accounts in Kasina's name: domain (.com via Cloudflare), Cloudflare, OVH VPS (or Hetzner/Vultr fallback), Bunny Stream and Storage, SMSEthiopia (sender ID, deposit), email sending, Sentry, uptime monitor, GitHub organization or repository. Collect the logo, photos with consent, bank account details, contacts and social links, the course list with prices and access days, and the first course videos.

## Phase 1

### Week 1: foundations, public site, sign-in, spikes

- **Repository and delivery:**
  - monorepo per KPA-02 (`apps/web`, `apps/api`, `packages/contracts`, `packages/domain`, `packages/ui`, `packages/i18n`, migrations, tests)
  - CI with typecheck, lint, test and build
  - Docker staging on the VPS with HTTPS; Sentry; backups job skeleton
- **Contracts:** OpenAPI/Zod schemas for the week 1–2 endpoints; error envelope; ID/date/money conventions.
- **Database:** migrations for users, roles, sessions, otp_challenges, courses, groups, modules, activities, lesson_content, attachments, videos, orders, payment_attempts, confirmed_payments, enrollments, access_events, activity_progress, audit_log, notifications and outbox; constraints per KPA-02 "Engineering contracts".
- **Design system:** tokens, fonts (Playfair Display, Inter, Noto Sans Ethiopic), Lucide, the gold አማ / EN pill, i18n keys with Amharic default, layout shells for public, student, instructor (light sidebar) and admin (charcoal sidebar).
- **Screens:** PUB-001 to PUB-006 (static content from config until ADM-014 to ADM-016 exist); AUTH-001 with real OTP (SMS adapter + console adapter for dev); AUTH-002 portal selection and switching; step-up OTP endpoint.
- **Tests and spikes (document results in `docs/spikes/`):**
  - Bunny: direct upload with a scoped token, processing callback/polling, signed playback, allowed domains, MediaCage, watermark, and player events sufficient for 90% unique coverage
  - YouTube and Kasina-server playback coverage, if time allows (otherwise later, per DECISIONS)
  - SMSEthiopia delivery to Ethio Telecom and Safaricom numbers
  - 360px Android load on a slow network
- **Review:** the public site and sign-in on staging, plus the test results.

### Week 2: courses, learning, payments (first vertical slice)

- **Course management:** ACD-001 Details (with admin commercial controls), ACD-002 Curriculum, ACD-003 Lesson editor, ACD-004 Video states; ADM-002 Manage courses; course groups.
- **Learning:**
  - STU-001 My Learning, STU-002 Explore (same components as PUB-004/005), STU-005 learning interface
  - progress tracking (90% merged-interval coverage, explicit Mark complete), resume
  - signed media URLs and free preview authorization
- **Payments and access:**
  - STU-003 Enrollment and payment (bank receipt upload, cash), STU-004 Payment status
  - ADM-006 Payments (approve or reject atomically and idempotently, duplicate references blocked)
  - ADM-005 Enrollment management (complimentary grant, renewal from max(expiry, confirmation))
  - in-app and SMS notices through the outbox
- **Review:** the end-to-end slice. Register → preview → pay by receipt → admin approves → watch video → progress → renew.

### Week 3: assessments, completion, certificates, instructor portal

- **Quizzes:** ACD-005 Quiz editor (immutable published versions), STU-007 Quiz and results (server grading, progressive save), ACD-009 Quiz results.
- **Practicals:** ACD-006 Practical editor, STU-008 Practical submission (private upload with progress/retry, quarantine and checks), STU-009 Review status, ACD-007 Assessments overview, ACD-008 Practical review (conditional update, stale review rejected).
- **Course status:** STU-006 Consolidated assessments; completion transaction (serialized with curriculum changes); STU-010 Certificates (server PDF, five fields, Noto Sans Ethiopic, no QR); ADM-007 Certificates (name correction, exceptional invalidation, audited).
- **Instructor portal:** ACD-010 Academic record, ACD-011 Announcements; INS-001 to INS-004 (assigned-course scope enforced server-side; INS-004 without MFA).
- **Review:** an instructor builds a course with a lesson, a quiz and a practical. A student completes it and gets a certificate. An instructor reviews the practical.

### Week 4: admin portal completion, hardening, launch

- **Admin screens:**
  - ADM-001 Dashboard, ADM-003 Manage staff (provision, assign, disable with session revocation, last-admin guard, phone re-point), ADM-004 Manage students
  - ADM-008 Financial and ADM-009 Academic & enrollment reports (shared query for table, totals, chart and CSV; formula-injection-safe CSV)
  - ADM-010 to ADM-012 Messages and contact (rate limit and spam protection)
  - ADM-013 to ADM-020 Settings (academy information, website and homepage content, payment settings with step-up OTP and self-alert, learning settings, notifications, security & activity log)
  - STU-011 Account, history, notifications and support
- **Hardening:**
  - the full test list in KPA-02 "Verification" (permission matrix with cross-course ID attacks, concurrency, idempotency, renewal, versioning, private files)
  - accessibility pass; native Amharic review of strings
  - real-device test on Ethio Telecom and Safaricom
  - backup restore test; runbook including the administrator phone-reset procedure
- **Launch:**
  - production deploy; Kasina staff training; admin guide; handover of accounts and repository
  - TG-001 Phase 1 preparation: self-contained student shell and adapter boundaries (no Telegram code)
- **Phase 1 acceptance:** every Phase 1 screen ID demonstrated on desktop and mobile; release gates in KPA-04 satisfied or explicitly waived by the owner in writing.

## Phase 2

### Week 5: gates, Telegram foundation
Gates: Telegram's current digital-goods payment rules (R-P2-07); Chapa merchant account and test keys; current fees. Build: bot setup, Mini App shell (R-P2-01), init-data authentication (R-P2-02), identity linking with OTP (R-P2-03), STU-011 linking section. Review: an existing web student opens the Mini App and sees the same records.

### Week 6: bot notifications, deep links, media in Telegram
Build: R-P2-04 and R-P2-05. Then R-P2-08 tests on Android and iOS Telegram: playback, watermark, receipt and practical uploads, PDF and certificate download. Fix or document workarounds. Review: notifications with deep links; a full course completed inside Telegram.

### Week 7: online payment
Build: R-P2-06 PaymentProvider interface and Chapa (initialize, hosted checkout, verify, webhook, payment_events, idempotent confirmation through the ADM-006 transaction); STU-003 online method; ADM-017 Online settings; reports with the online method. Apply the R-P2-07 outcome to the Mini App. Review: test-mode payments, repeated webhooks, amount mismatch held for review.

### Week 8: hardening and Phase 2 launch
Regression of all Phase 1 tests; Phase 2 acceptance (R-P2-09); live Chapa keys after the gate; pilot with real students; fixes from Phase 1 real use; documentation update; handover.
