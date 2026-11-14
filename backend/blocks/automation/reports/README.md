# automation.reports

**Purpose.** Numbers for the owner. Keeps its own read copy; nobody reads its tables.

| | |
|---|---|
| Steward | platform-leads |
| Status | proposed (skeleton only; built in the milestone named in `docs/roadmap.md`) |
| Own schema | `reports` |

## Interfaces
- **Provides:** (none yet) · **Requires:** (none yet)
- **Events emitted / consumed:** (none yet)
- **HTTP API:** `/api/reports/v1/...`

## Settings
See `hulu_reports/settings.py`. Every non-code difference between clients is a bounded setting with a safe default.

## Permissions
Declared in `manifest.yaml`; every route must require one (startup fails otherwise).

## Security
Tenant isolation test in `tests/security`; no personal data in events; handle `account.erased@1` if this block holds personal data.

## Known limits
TODO
