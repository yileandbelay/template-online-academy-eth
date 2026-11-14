# 017. Identity: Keycloak footprint and sign-up experience

- Status: Proposed. Spike A is done: recommendation GO with conditions (owner to confirm at Gate 0)

## Context
The spec chooses Keycloak with Organizations. It is a heavy Java service. Mek Academy users expect a short sign-up (name, email, phone, city) and a return to the course they were enrolling in. Mek Academy stores Werkzeug password hashes.

## Decision
Spike A result (`docs/spikes/m0-report.md`): about 0.5 to 0.7 GB RAM, 8.5 s warm start, 66 logins/s; sign-up with phone and city, return to the chosen course, reset and staff invitation all work. Conditions: a branded theme, an Amharic bundle with native review, and a password-migration decision (Mek's scrypt hashes cannot be imported as they are). Proposed: go.

Criteria that were set: Go if the full stack fits comfortably on a modest host and sign-up needs no more steps than Mek Academy's, in English and Amharic, with invitations, resets and a way to migrate Mek Academy passwords (verify on first login, reset email as fallback). Otherwise a lighter identity option behind the same interface.

## Consequences
Identity is accessed through a kernel interface so the choice can change without changing blocks.
