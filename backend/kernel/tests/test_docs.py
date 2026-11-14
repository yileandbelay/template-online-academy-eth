"""Documentation hygiene: every relative Markdown link points at something that exists."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LINK = re.compile(r"\]\((?!https?://|mailto:|#)([^)\s]+)\)")


def test_relative_links_resolve():
    files = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md")), *sorted((ROOT / "products").rglob("*.md"))]
    broken = []
    for f in files:
        for target in LINK.findall(f.read_text(encoding="utf-8")):
            path = target.split("#")[0]
            if path and not (f.parent / path).exists():
                broken.append(f"{f.relative_to(ROOT)} -> {target}")
    assert broken == []


def test_every_adr_is_in_the_index():
    index = (ROOT / "docs" / "adr" / "README.md").read_text(encoding="utf-8")
    for adr in sorted((ROOT / "docs" / "adr").glob("0[1-9]*.md")):
        assert adr.name in index, adr.name
