"""new-block <family>.<name> --steward <team>: create a block with the full structure of spec 7.1."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from hulu_kernel.registry.manifest import BLOCK_ID

from new_block.scaffold import FILES


def generate(block_id: str, steward: str, blocks_root: Path) -> Path:
    m = BLOCK_ID.match(block_id)
    if not m:
        raise ValueError(
            f"{block_id!r}: a block id is <family>.<name> in lower case, family one of "
            "compliance, integrations, automation, ai, business (client extensions live in the client's repository)"
        )
    family, name = m["family"], m["name"]
    target = blocks_root / family / name
    if target.exists():
        raise FileExistsError(f"{target} already exists")
    values = {
        "{{id}}": block_id,
        "{{family}}": family,
        "{{name}}": name,
        "{{package}}": f"hulu_{name}",
        "{{steward}}": steward,
        "{{Title}}": name.replace("_", " ").title(),
    }

    def fill(text: str) -> str:
        for key, value in values.items():
            text = text.replace(key, value)
        return text

    for rel, content in FILES.items():
        path = target / fill(rel)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(fill(content), encoding="utf-8")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="new-block", description=__doc__)
    parser.add_argument("block_id", help="for example business.lms")
    parser.add_argument("--steward", default="platform-leads", help="team that reviews this block")
    parser.add_argument(
        "--root", type=Path, default=Path("backend/blocks"), help="blocks folder (default backend/blocks)"
    )
    args = parser.parse_args(argv)
    try:
        target = generate(args.block_id, args.steward, args.root)
    except (ValueError, FileExistsError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"Created {target}. Next: fill in manifest.yaml, then run `uv sync` and `uv run pytest {target}`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
