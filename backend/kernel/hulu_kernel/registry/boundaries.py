"""Import boundaries between blocks (spec 6.2): a block imports only hulu_kernel, hulu_contracts, its own package
and the SDK. Used by CI for every block under backend/blocks and by each generated block's own security test."""

from __future__ import annotations

import ast
from pathlib import Path

ALLOWED_PREFIXES = ("hulu_kernel", "hulu_contracts", "hulu_sdk")


def foreign_imports(block_dir: Path, own_package: str) -> list[str]:
    """Return 'file:line imports X' for every import of another block's package (any hulu_* not allowed)."""
    problems: list[str] = []
    for path in sorted(block_dir.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names = [node.module]
            else:
                continue
            for name in names:
                top = name.split(".")[0]
                if top.startswith("hulu_") and top != own_package and top not in ALLOWED_PREFIXES:
                    problems.append(f"{path.relative_to(block_dir)}:{node.lineno} imports {name}")
    return problems
