# 015. Template scope and Mek Academy parity

- Status: Accepted
- Date: 2026-11-14

## Context
The owner wants a reusable online-learning template on the Mek stack, with Mek Academy as the example product. Mek Academy is live on Flask.

## Decision
- A new repository holds the template. It implements the full block architecture structure, and builds only the blocks online learning needs (see the plan, section 6).
- Mek Academy stays on its Flask server, maintained, until the template reaches parity on a copy of its data. Mek Academy is the reference for parity tests, not the first production client of the new stack.
- Product-specific parts (name, theme, pages, content, extensions) live in a separate product pack repository.
- The second client is Kasina; its product type is to be confirmed.

## Consequences
Two codebases are maintained for a period. New Mek Academy features go to the template once milestone M2 is reached, except urgent fixes.
