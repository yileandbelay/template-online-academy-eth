# Testing

Tests are the specification. Mek Academy's 537 tests describe how an online academy behaves; the same behaviours become
scenarios here.

| Kind | Where | What |
|---|---|---|
| Unit | in each block, `tests/unit/` | Domain rules with no database; milliseconds |
| Contract | in each block, `tests/contract/` | Events, ports and the HTTP API match what the block published |
| Security | in each block, `tests/security/` | Tenant isolation, permission on every route, import boundaries |
| Library | `backend/kernel/tests/test_library.py` | Every manifest, capability, event, product and template is consistent; the catalogue is current |
| Scenarios | `qa/scenarios/` | Behaviour across blocks, such as "learner pays by manual transfer, staff approves, learner is enrolled" |
| End to end | `qa/e2e/` | Browser journeys at 390 px and 1100 px widths (from M5) |
| Performance | `qa/perf/` | Query-count budgets per endpoint; page-weight budget on a throttled phone |

## Fakes
Every external system (Chapa, Bunny, email, identity) has a fake in `qa/fakes/`, built from the provider's documentation and
contract-tested against its sandbox before a release, so a fake that drifts is caught.

## Rules
- Behaviour changes come with a test; a scenario is added or updated for any changed flow.
- Test file names are unique across the repository (generated blocks include their name in the file name).
- Skipping or deleting a test to get a green build is not allowed.
