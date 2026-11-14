# business.parties

**Purpose.** Who is who. Every other block refers to a person by id and reads details through `PartyQueryV1`.

| | |
|---|---|
| Steward | platform-leads |
| Status | proposed (skeleton only; built in the milestone named in `docs/roadmap.md`) |
| Own schema | `parties` |

## Interfaces
- **Provides:** (none yet) · **Requires:** (none yet)
- **Events emitted / consumed:** (none yet)
- **HTTP API:** `/api/parties/v1/...`

## Settings
See `mek_parties/settings.py`. Every non-code difference between clients is a bounded setting with a safe default.

## Permissions
Declared in `manifest.yaml`; every route must require one (startup fails otherwise).

## Security
Tenant isolation test in `tests/security`; no personal data in events; handle `account.erased@1` if this block holds personal data.

## Known limits
TODO
