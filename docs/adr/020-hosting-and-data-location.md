# 020. Hosting and data location

- Status: Open (deferred by ADR-016)

## Context
The spec says personal data collected in Ethiopia is stored on servers in Ethiopia (Proclamation 1321/2024) and leaves the Ethiopian production provider open (ADR-004). The owner will choose later.

## Decision
Deferred. Before any real personal data is stored on a host, the owner confirms the rule with their adviser and chooses the provider and region. Local and CI environments use fake data only.

## Consequences
No deployment work until this is decided.
