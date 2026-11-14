"""Command line helpers: `uv run mek-kernel validate <product.yaml>`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pydantic import ValidationError

from mek_kernel.registry import (
    KERNEL_CAPABILITIES,
    ResolutionError,
    load_block_manifest,
    load_product_manifest,
    resolve,
)
from mek_kernel.registry.catalogue import render_catalogue


def validate(product_path: Path, blocks_root: Path | None) -> int:
    try:
        product = load_product_manifest(product_path)
    except (ValidationError, ValueError, OSError) as exc:
        print(f"{product_path}: invalid\n{exc}", file=sys.stderr)
        return 1
    if blocks_root is not None:
        available = [load_block_manifest(p) for p in sorted(blocks_root.glob("*/*/manifest.yaml"))]
        try:
            order = resolve(product, available, kernel_provides=KERNEL_CAPABILITIES)
        except ResolutionError as exc:
            print(f"{product_path}: cannot be assembled: {exc}", file=sys.stderr)
            return 1
        print(f"{product_path}: valid; load order: {', '.join(m.id for m in order)}")
    else:
        print(f"{product_path}: valid (schema only; pass --blocks to also resolve blocks)")
    return 0


def catalogue(blocks_root: Path, out: Path, *, check: bool) -> int:
    text = render_catalogue(blocks_root)
    if check:
        if not out.exists() or out.read_text(encoding="utf-8") != text:
            print(f"{out} is out of date: run `uv run mek-kernel catalogue`", file=sys.stderr)
            return 1
        print(f"{out} is up to date")
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="mek-kernel")
    sub = parser.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate", help="validate a product manifest")
    v.add_argument("product", type=Path)
    v.add_argument("--blocks", type=Path, default=None, help="blocks folder, to also resolve blocks and capabilities")
    c = sub.add_parser("catalogue", help="generate the block catalogue page from the block manifests")
    c.add_argument("--blocks", type=Path, default=Path("backend/blocks"))
    c.add_argument("--out", type=Path, default=Path("docs/architecture/block-catalogue.md"))
    c.add_argument("--check", action="store_true", help="fail if the page on disk is out of date")
    args = parser.parse_args(argv)
    if args.command == "catalogue":
        return catalogue(args.blocks, args.out, check=args.check)
    return validate(args.product, args.blocks)


if __name__ == "__main__":
    raise SystemExit(main())
