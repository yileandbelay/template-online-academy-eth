# M0 spike report (for Gate 0)

Date: 14 November 2026. Four spikes, run locally; nothing was deployed (ADR-016). Spike code is in `spikes/` (throwaway, not part
of the build; each folder has a README to repeat it). All numbers are from this one machine (4 cores, 16 GB, Linux) unless
stated; treat them as orders of magnitude, not guarantees.

## Summary

| Spike | Verdict | Headline |
|---|---|---|
| **C** Row-level security through a pooler | **GO** | 12 of 12 checks pass. Isolation, fail-closed and the owner-bypass trap are proven; a plain `SET` leaks behind PgBouncer, `SET LOCAL` does not. About 0.2 ms per request |
| **A** Keycloak | **GO, with conditions** | Sign-up (with phone and city), return to the chosen course, reset and staff invitation all work. About 0.5 to 0.7 GB RAM, 8.5 s warm start, 66 logins/s. Needs a branded theme, an Amharic bundle, and a decision on password migration |
| **B** Page weight | **DECISION NEEDED** | Next.js works but its floor is about 138 KB of JavaScript on every page (Mek Academy today ships none). An islands approach for the public pages is about half that and zero on static pages |
| **D** Footprint | **Measured; host size is a later decision** | About 1.2 GB for the seven components running here, about half of it Keycloak. A 4 GB host is the sensible minimum to plan for |

Decisions I need from you are at the end (section "Gate 0").

---

## Spike C: tenant isolation with PostgreSQL row-level security

PostgreSQL 16.15 and PgBouncer 1.22 in transaction-pooling mode with a pool of **one** server connection (the worst case for leaks).
`spikes/c_rls/rls_spike.py`.

| Check | Result |
|---|---|
| Each tenant sees only its own rows; cannot update or delete another tenant's rows | Pass |
| `WITH CHECK` blocks writing a row for another tenant | Pass |
| No tenant set means no rows and no writes (fails closed) | Pass |
| A table owner **bypasses** RLS unless the table is `FORCE`d; a superuser always does | Pass (demonstrated) |
| Tenant set with `set_config(..., true)` (SET LOCAL) ends with the transaction | Pass |
| **A plain `SET` leaks to the next client behind the pooler** | Demonstrated: a client that set no tenant saw another tenant's rows |
| `SET LOCAL` through the pooler does not leak | Pass |
| SQLAlchemy `after_begin` hook, 3 tenants x 150 transactions in parallel through the pooler | No crossing |
| Cost on an indexed 200k-row table | 0.23 ms without RLS, 0.45 ms with RLS and `set_config`: about +0.2 ms |

**Rules for the kernel (M1)**: tenant only from the verified token; set per transaction with `set_config(..., true)`; the app role
owns nothing and has no `BYPASSRLS`; owner role only for migrations; every tenant table `ENABLE` and `FORCE` RLS with one policy
(`USING` and `WITH CHECK`) and an index starting with `tenant_id`; disable server-side prepared statements behind a transaction
pooler (or use PgBouncer 1.21+ prepared-statement support, which I did not test); an isolation test in every block.

Not tested: a failure of the policy itself under concurrent migrations; PgBouncer `max_prepared_statements`.

---

## Spike A: Keycloak

Keycloak 26.8.2 (from Maven Central), production mode, PostgreSQL backend, Java 21. `spikes/a_keycloak/`.

### Footprint
| Measure | Result |
|---|---|
| Start, first run (creates the schema) | 30 s |
| Start, warm | 8.5 to 8.8 s |
| Memory, idle (RSS / PSS) | 498 to 520 MB / about 550 MB |
| After 600 logins | 704 MB RSS |
| Throughput, 8 concurrent password logins, 4 cores | **66 logins/s**, median 113 ms, p95 195 ms, 0 failures |
| Disk (unpacked distribution) | 185 MB |

For a learning site, 66 logins per second is far above any realistic need; the cost is memory, not CPU.

### What worked (phone viewport, 390 px; screenshots in `spikes/a_keycloak/results/`)
- **Sign-up with phone and city**, email as username. The learner lands back on the page they came from: the course they pressed
  "Enrol" on (OIDC `state`), in 3 navigations and 257 ms. The token carries email, name, phone and city.
- **Login**, **forgot password** (email with a link, new password works) and a **staff invitation** ("set your password" email, 7-day
  lifetime) all work, including the email contents.
- Replaces Mek's own sign-up, reset and staff-invite code.

### What is not ready out of the box
1. **Amharic is not shipped.** Keycloak has 41 login languages but none for Amharic, Tigrinya or Oromo. A custom theme with
   `messages_am.properties` works (proven with 15 keys and the `ui_locales=am` parameter; the language dropdown shows አማርኛ). The stock
   login bundle has 525 keys and the email bundle 73; the screens a learner meets (sign-in, register, reset, errors, the emails) are
   probably 100 to 150 strings. My test Amharic strings are **not** reviewed by a native speaker.
2. **Branding.** The stock theme is dark with blue buttons. A custom login theme in Mek's tokens is needed (estimated 2 to 3 days).
3. **Sign-up is 7 fields**, against 5 on Mek today: Keycloak has separate first and last name and a confirm-password field. Either
   accept it, or use one "full name" attribute and hide confirm-password in the theme.
4. **Mek's password hashes cannot be imported as they are.** Mek stores Werkzeug 3 hashes (`scrypt:32768:8:1$...`). Keycloak accepts a
   PBKDF2 hash on import (tested: login works with no reset, and Keycloak upgrades the stored hash to argon2 at that first login)
   but cannot verify scrypt (tested: login fails). Options:
   - **(a) Email everyone a reset link at cutover.** No code; costs one support burst. Fine if the number of students is modest.
   - **(b) A small Keycloak extension (Java) that verifies scrypt**, so existing hashes are imported as they are and upgraded at first
     login. About 3 to 4 days with tests; nobody is asked to reset. I did not build this; the estimate is mine.
   I need your user count to recommend between them.

### Verdict
**GO, with conditions**: custom branded theme, Amharic bundle with native review, and the password decision. The cost is mostly
memory (about 0.5 to 0.7 GB), not CPU or complexity of use. Effort to add to M1/M5: about 5 to 9 days (theme 2 to 3, Amharic bundle and
review 1 to 2, realm provisioning and invitation glue 2, optional scrypt extension 3 to 4).

---

## Spike B: page weight on a throttled phone

Chromium emulating a phone (390 px, 4x slower CPU), cold cache, median of 3 runs. Network: **fast 3G** (1.6 Mbps, 150 ms) and
**slow 3G** (400 Kbps, 400 ms). Three builds of the same four page kinds (home, catalogue with filter, course page, lesson page):
Mek Academy today (Flask, behind gzip as nginx would do), a **Next.js 16** prototype, and an **Astro 6 + React islands** prototype.
`spikes/b_pageweight/`; raw tables in `results/`.

Course page, the typical case:

| | Total transferred | JavaScript | First paint, fast 3G | Buttons and filters usable* fast 3G | First paint, slow 3G | Usable* slow 3G |
|---|---|---|---|---|---|---|
| **Today (Flask)** | **15 KB** | **0 KB** | 0.52 s | about 0.4 s (nothing to wait for) | 1.2 s | about 1.1 s |
| **Next.js 16** | 154 KB | 140 KB | 0.42 s | about 1.9 s | 1.0 s | about 5.5 s |
| **Astro + islands** | 74 KB (home: 1.8 KB) | 70 KB (home: 0) | 0.28 s | about 0.8 s | 0.5 s | about 2.4 s |

\* "Network idle" time minus the 0.5 s idle-detection window: the moment the scripts have loaded and hydrated.

What this shows:
- **Next.js's floor is about 138 KB of JavaScript, even on a page with no interactive parts.** I measured a server-only page: 138 KB.
  That is the framework's cost, paid on every page by every first-time visitor. It meets the proposed budget (about 150 KB) with almost
  no headroom, and the real app (sign-in state, language switcher, calendar picker) will add to it.
- The pages are **readable early** with Next.js, because the HTML is static, but the buttons and the filter are dead until scripts
  load: about 2 s on fast 3G and 5.5 s on slow 3G, against effectively instant today.
- **Data cost.** A first visit costs about ten times the bytes of today's pages (154 KB against 15 KB). On metered mobile data this is
  a real cost for learners, and "works on weak connections" is the first eLearning need in the concept note.
- With **islands**, pages with nothing interactive ship no JavaScript at all (the home page is 1.8 KB), and a page with one island ships
  React's 70 KB. The React components are the same ones; only the page shell differs.
- Repeat visits reuse the hashed scripts from cache, which softens the Next.js cost for returning learners. Cold visits are the ones
  that decide whether a newcomer stays.

**Caveats.** Emulated throttling on a fast machine, not a real handset. No images or web fonts (real course covers and an Amharic font
add weight to every option). My prototype stylesheet is 1 KB against Mek's real 11 KB compressed, which flatters first paint for both
prototypes. The Astro prototype was built to answer "is there an alternative", not tuned.

### Verdict and recommendation
Both options are workable; this is a product decision. My recommendation, in order of preference:
1. **Hybrid (Option 2):** the public pages (home, catalogue, course, lesson preview, policies, contact) on an islands framework (Astro,
   with the same React components), and the logged-in learner and admin apps on Next.js, where JavaScript is expected and cached.
   It matches the concept note's promise for weak connections. Cost: two build systems and a shared component library; about 5 to
   8 more days in M5; spec text names Next.js, so ADR-018 would record the exception.
2. **Next.js everywhere (Option 1)**, with progressive enhancement (forms that work before scripts load), static public pages, a
   CI budget on first-load JavaScript, and a clear off-ramp to Option 1's hybrid if the real pages exceed the budget.

I lean to option 1 only if keeping one framework matters more to you than the first-visit weight.

---

## Spike D: footprint

Each component running natively here, memory as PSS (proportional set size, which does not double-count shared pages).
`spikes/d_footprint/measure_pss.py`. All components are at a "hello world" stage of load except Keycloak (after 600 logins) and
Traefik (after 1,200 proxied requests).

| Component | Memory |
|---|---|
| Keycloak 26.8.2 | about 550 MB |
| PostgreSQL 16 (default settings, 9 processes) | about 105 MB |
| Traefik v3 (after 1,200 requests) | about 118 MB |
| Next.js 16 server | about 60 to 70 MB |
| API (FastAPI, hello world) | about 65 MB |
| PgBouncer | about 2 MB |
| MinIO (after uploading and reading back 100 MB) | about 260 MB |
| **Measured total (7 components)** | **about 1.2 GB** (Keycloak is about half) |

Not measured: the worker and relay processes the architecture adds (each is another Python process, likely similar to the API), and
the real API after all eleven blocks, PDF rendering (WeasyPrint) and a real database working set: **these will be larger than the
hello-world numbers above.** That is my judgement, not a measurement. Keycloak is about half of what is measured; MinIO and the gateway are the next largest.

**Sizing guidance (for ADR-020, when deployment comes):** plan for a **4 GB host as the minimum** for the whole stack on one machine,
8 GB for comfort. A 2 GB host would be too tight: the measured components alone already take about 1.2 GB, before the operating system, the worker and relay processes and real data. This only matters when you choose a host.

`docker-compose.spike.yml` and `measure.sh` let you repeat this in containers on your machine; they are **untested** here because
this environment has no Docker daemon.

---

## What I could not do
- No real handset, no real mobile network; no Docker. The scrypt extension and a production-quality Amharic theme were not built.
- MinIO and Traefik were installed natively (MinIO built from source with Go, Traefik from its release binary), not as containers, so container overhead is not included.
- I did not measure the live Mek site (not reachable from this environment); the "today" baseline is the actual Flask app with its demo data.

## Changes this made to the plan
- **M1 (kernel):** add the row-level-security rules above (no change in size). `uvicorn` was missing from the kernel's dependencies
  and is now added.
- **Identity work** (theme, Amharic bundle, provisioning glue, optional scrypt extension): +5 to 9 days, in M1 and M5.
- **Web delivery:** +5 to 8 days in M5 if you choose the hybrid; otherwise the work moves to performance budgeting.
- Net effect on the programme: about **+10 to +17 days**, so the 188 to 270 working days becomes roughly **200 to 285**. Still rough; I would
  re-estimate again after M1.

## Gate 0: what I need from you
1. **Web delivery (ADR-018):** hybrid (my recommendation) or Next.js everywhere?
2. **Identity (ADR-017):** go ahead with Keycloak under the conditions above?
3. **Password migration:** how many students and staff does Mek Academy have today? (It decides between emailing everyone a reset link
   and building the scrypt extension.)
4. **Sign-up form:** keep first and last name, or one "full name" field as on Mek today?
5. **Amharic reviewer:** who will review the Amharic for the sign-in screens and emails?
6. **Go to M1** (kernel walking skeleton, estimated 25 to 35 days, now 28 to 40 with the identity work)? Or stop or adjust here.
