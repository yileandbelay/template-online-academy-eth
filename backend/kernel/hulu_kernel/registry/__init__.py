"""Module registry: reads manifests, validates products, resolves load order (spec 5, 6, 12)."""

from hulu_kernel.registry.manifest import (
    BlockManifest,
    ProductManifest,
    load_block_manifest,
    load_product_manifest,
)
from hulu_kernel.registry.resolver import ResolutionError, resolve

__all__ = [
    "BlockManifest",
    "ProductManifest",
    "ResolutionError",
    "load_block_manifest",
    "load_product_manifest",
    "resolve",
]
