"""Registers this block with the platform. The manifest is the single source of truth."""

from pathlib import Path

from hulu_kernel.registry import BlockManifest, load_block_manifest

MANIFEST_PATH = Path(__file__).resolve().parent.parent / "manifest.yaml"


def manifest() -> BlockManifest:
    return load_block_manifest(MANIFEST_PATH)
