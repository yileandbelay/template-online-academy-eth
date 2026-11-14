# 017. Identity: Keycloak footprint and sign-up experience

- Status: Proposed (spike A in M0)

## Context
The spec chooses Keycloak with Organizations. It is a heavy Java service. Mek Academy users expect a short sign-up (name, email, phone, city) and a return to the course they were enrolling in. Mek Academy stores Werkzeug password hashes.

## Decision
Pending spike A. Go if the full stack fits comfortably on a modest host and sign-up needs no more steps than Mek Academy's, in English and Amharic, with invitations, resets and a way to migrate Mek Academy passwords (verify on first login, reset email as fallback). Otherwise a lighter identity option behind the same interface.

## Consequences
Identity is accessed through a kernel interface so the choice can change without changing blocks.
