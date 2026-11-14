# What Mek Academy taught us

Mek Academy is the first online-learning product (Flask, live at www.mek-academy.com). Each lesson from building and running
it became a rule for this template. When a rule and a convenient shortcut disagree, the rule wins.

| # | What happened on Mek Academy | Rule for the template |
|---|---|---|
| 1 | The course-visibility model had to be rethought: every course and its lesson titles are shown to everyone, lessons are locked by default, and an admin can make a lesson public. | Access is an explicit **policy**: course state × lesson state (locked, free preview, public) × viewer (guest, student, enrolled, staff), tested as a full matrix. |
| 2 | Bank transfer and Telebirr deposits with receipt upload and admin approval mattered as much as the gateway. Partial payments and admin-recorded payments appeared in real use. | `PaymentProviderV1` covers online **and** offline channels. The manual adapter is first-class: review queue, partial payments, receipts. |
| 3 | Settings drifted: old defaults had to be patched in code so older servers kept working. | Settings are typed, versioned and migrated. The manifest is the one source of truth. No brand text in shared code. |
| 4 | The admin course editor was one long page; a step-by-step editor (Details, Lessons, Quizzes, Students, Announcements, Reviews) with ticks and "Save and continue" was clearly better. | The admin is its own app with its own language policy; a reusable stepper is part of the UI library. |
| 5 | Amharic needed consistent wording ("Browse courses" and a bare "Browse" use different words by decision). | Each language pack has a glossary, native-speaker review as a release gate, and coverage checks. |
| 6 | The video host refused to play until the referrer policy and allowed-domains list were right. | `VideoProviderV1` includes allowed-domain checks; a smoke test plays a real sample video. |
| 7 | Much time went on DNS (www and bare domain), certificates, a stray line in the settings file, and a backup script with an unfilled placeholder. | When deployment comes (M6): validate DNS before certificates, a `doctor` command, backup and restore tested in CI and rehearsed. |
| 8 | A query audit found N+1 patterns. | Query-count budgets per endpoint, tested in CI. |
| 9 | Teachers manage only their own courses; price, lesson lock and payments are admin-only. | Named permissions with object-level scope from the start. |
| 10 | Certificates carry a verification code and QR; printed certificates keep pointing at their URL. | Certificate numbers come from the numbering series; public verification URLs are frozen. Mek Academy's `/certificates/<code>` must keep working after migration. |
| 11 | Account export and erasure were added late and touch every feature. | `account.erased@1` is in the contract from day one; every block holding personal data handles it. |
| 12 | 537 tests made big changes safe; layout checks at phone and desktop widths caught real overflow. | Tests are the specification. Responsive screenshots at 390 px and 1100 px in CI. |
| 13 | The colour theme was locked after discussion. | Products customise through design tokens and page slots only. |
| 14 | Work moved fastest in small pull requests with a "green light" before building and "merge" before releasing. | Keep that rhythm. |

Mek Academy's own test suite becomes the first set of scenarios in `qa/scenarios/` (areas and counts are in the plan, appendix D).
