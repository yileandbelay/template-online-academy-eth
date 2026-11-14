"""Command line helpers: `uv run hulu-kernel validate <product.yaml>`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pydantic import ValidationError

from hulu_kernel.registry import ResolutionError, load_block_manifest, load_product_manifest, resolve


def validate(product_path: Path, blocks_root: Path | None) -> int:
    try:
        product = load_product_manifest(product_path)
    except (ValidationError, ValueError, OSError) as exc:
        print(f"{product_path}: invalid\n{exc}", file=sys.stderr)
        return 1
    if blocks_root is not None:
        available = [load_block_manifest(p) for p in sorted(blocks_root.glob("*/*/manifest.yaml"))]
        try:
            order = resolve(product, available)
        except ResolutionError as exc:
            print(f"{product_path}: cannot be assembled: {exc}", file=sys.stderr)
            return 1
        print(f"{product_path}: valid; load order: {', '.join(m.id for m in order)}")
    else:
        print(f"{product_path}: valid (schema only; pass --blocks to also resolve blocks)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="hulu-kernel")
    sub = parser.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate", help="validate a product manifest")
    v.add_argument("product", type=Path)
    v.add_argument("--blocks", type=Path, default=None, help="blocks folder, to also resolve blocks and capabilities")
    args = parser.parse_args(argv)
    return validate(args.product, args.blocks)


if __name__ == "__main__":
    raise SystemExit(main())
