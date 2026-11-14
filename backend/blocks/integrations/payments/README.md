# integrations.payments

**Purpose.** Money in. The manual adapter (bank, Telebirr, cash, receipt upload and review) is as important as the gateway.

| | |
|---|---|
| Steward | platform-leads |
| Status | proposed (skeleton only; built in the milestone named in `docs/roadmap.md`) |
| Own schema | `payments` |

## Interfaces
- **Provides:** (none yet) · **Requires:** (none yet)
- **Events emitted / consumed:** (none yet)
- **HTTP API:** `/api/payments/v1/...`

## Settings
See `hulu_payments/settings.py`. Every non-code difference between clients is a bounded setting with a safe default.

## Permissions
Declared in `manifest.yaml`; every route must require one (startup fails otherwise).

## Security
Tenant isolation test in `tests/security`; no personal data in events; handle `account.erased@1` if this block holds personal data.

## Known limits
TODO
