# Mek Academy

The reference product for the template. Live today on a separate Flask application (repository `aaa_gcp_compute`), which
stays maintained until the template reaches parity (ADR-015).

| | |
|---|---|
| Type | Online academy (`templates/elearning/online_academy.yaml`) |
| Main address | www.mek-academy.com; `mek-academy.com` and `learn.mek-academy.com` redirect to it |
| Languages | English and Amharic; admin console in English |
| Currency | ETB |
| Payments | Chapa and manual transfer with receipt review |
| Video | Bunny Stream (also VdoCipher and external links) |
| Pack | `products/mek-academy/` |

## What it does today
Courses with categories, sections and lessons (video, text, links, materials); every course visible with lessons locked by
default and an admin option to make a lesson public; enrolment by payment, by assignment or by invitation; quizzes and
exams; certificates with a verification link and QR; reviews; announcements; per-lesson discussion; contact form and inbox;
revenue and student reports; account export and erasure; a step-by-step admin course editor; English and Amharic.
The full list, mapped to blocks, is in the plan (appendix A).

## Parity checklist (M7)
- Every "Must" feature in the plan's appendix A works on the template, verified by scenarios.
- Public URLs keep working: `/courses/<slug>`, `/certificates/<code>`, `/policies/<page>`.
- Existing certificate codes and payment references (`MEK-...`) still verify and display.
- Passwords: verify-on-first-login bridge, with a reset email as fallback (spike A).
- Amharic reviewed by a native speaker, glossary respected.
- A rehearsal on a copy of live data matches counts and sample records; rollback is the old application.
