"""Rename the platform brand everywhere: package names, folders, identifiers, event namespaces and prose.

The platform name is provisional until the company name is settled (ADR-022). Run this to change it again:

    uv run python tools/rebrand.py --old mek --new acme --dry-run     # show what would change
    uv run python tools/rebrand.py --old mek --new acme               # do it
    uv sync --all-packages && uv run acme-kernel catalogue && make check   # then rebuild and verify

Three spellings are replaced: lower case (`mek_kernel`, `mek-kernel`, `et.mek.sale.completed.v1`), Capitalised (`Mek`
in prose; override with --display) and UPPER CASE. Product names are not touched unless they contain the old word
(the product "Mek Academy" is a product, so rename it by hand if the platform brand changes and it should not follow).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    ".import_linter_cache",
    "dist",
    "build",
}
SKIP_FILES = {"uv.lock"}
TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".yaml",
    ".yml",
    ".toml",
    ".json",
    ".txt",
    ".cfg",
    ".ini",
    ".html",
    ".css",
    ".ts",
    ".tsx",
    ".js",
    ".mjs",
    ".sh",
    ".mako",
    "",
}
IDENT = re.compile(r"^[a-z][a-z0-9]*$")


@dataclass
class Result:
    files_changed: list[str] = field(default_factory=list)
    paths_renamed: list[str] = field(default_factory=list)


def _is_text(path: Path) -> bool:
    return path.name not in SKIP_FILES and (path.suffix in TEXT_SUFFIXES or path.name in {"Makefile", "CODEOWNERS"})


def rebrand(root: Path, old: str, new: str, display: str | None = None, dry_run: bool = False) -> Result:
    if not IDENT.match(old) or not IDENT.match(new):
        raise ValueError("--old and --new must be one lower-case word (letters and digits), for example mek")
    if old == new:
        raise ValueError("old and new are the same")
    display = display or new.capitalize()
    pairs = [(old.upper(), new.upper()), (old.capitalize(), display), (old, new)]

    def swap(text: str) -> str:
        for a, b in pairs:
            text = text.replace(a, b)
        return text

    result = Result()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            path = Path(dirpath) / name
            if not _is_text(path):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            updated = swap(text)
            if updated != text:
                result.files_changed.append(str(path.relative_to(root)))
                if not dry_run:
                    path.write_text(updated, encoding="utf-8")

    # Rename files and folders whose names contain the old word, deepest first so parents stay valid.
    entries: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        entries += [Path(dirpath) / n for n in [*dirnames, *filenames] if old in n.lower()]
    for path in sorted(entries, key=lambda p: len(p.parts), reverse=True):
        target = path.with_name(swap(path.name))
        result.paths_renamed.append(f"{path.relative_to(root)} -> {target.name}")
        if not dry_run:
            path.rename(target)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--old", required=True, help="current brand word, lower case")
    parser.add_argument("--new", required=True, help="new brand word, lower case")
    parser.add_argument("--display", help="how the new name is written in prose (default: Capitalised)")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = rebrand(args.root, args.old, args.new, args.display, args.dry_run)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    verb = "would change" if args.dry_run else "changed"
    print(f"{verb} {len(result.files_changed)} files and renamed {len(result.paths_renamed)} paths")
    if not args.dry_run:
        print(f"Next: uv sync --all-packages && uv run {args.new}-kernel catalogue && make check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
