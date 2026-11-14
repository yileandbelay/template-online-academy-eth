# Kasina

The second client: an **online academy**. It starts from `templates/elearning/online_academy.yaml`. Only the name and the type
are known so far; this page collects what is needed to configure its pack (`products/kasina/`).

## To confirm with the owner
- Exact product name, domain and whether a www redirect scheme like Mek's is wanted
- Languages and default language; Ethiopian or Gregorian calendar by default; currency
- Payment channels (online gateway, bank transfer, Telebirr), and whether partial payments are allowed
- Video host (Bunny, VdoCipher, external links)
- Enrolment policy: public catalogue with locked lessons (as Mek), or invitation only
- Certificate wording, signatures and verification page
- Course categories, first courses and instructors; who provides the content
- Reviews, announcements and discussion: on or off
- Anything Kasina needs that Mek does not (this decides whether it is a setting, a block feature or an extension)
- Launch date, which sets the priority of milestones

## Why it matters
Kasina is the proof of reuse (M8): it should launch from the template with manifest, settings, theme, pages and content
only. Any change to a shared block that Kasina forces is counted and reviewed.
