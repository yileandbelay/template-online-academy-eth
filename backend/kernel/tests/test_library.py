"""Checks on the whole block library and the product packs, so a manifest mistake fails the build."""

import importlib
from pathlib import Path

from mek_kernel.cli import catalogue
from mek_kernel.registry import KERNEL_CAPABILITIES, load_block_manifest, load_product_manifest, resolve
from mek_kernel.registry.manifest import ProductManifest

ROOT = Path(__file__).resolve().parents[3]
BLOCKS = ROOT / "backend" / "blocks"
manifests = [load_block_manifest(p) for p in sorted(BLOCKS.glob("*/*/manifest.yaml"))]


def test_library_is_not_empty_and_ids_are_unique():
    ids = [m.id for m in manifests]
    assert len(ids) >= 11 and len(ids) == len(set(ids))


def test_each_block_sits_in_its_family_folder_with_its_files():
    for p in sorted(BLOCKS.glob("*/*/manifest.yaml")):
        m = load_block_manifest(p)
        assert p.parent.parent.name == m.family and p.parent.name == m.id.split(".")[1]
        for rel in ["README.md", "CHANGELOG.md", "pyproject.toml", "tests", "ui"]:
            assert (p.parent / rel).exists(), f"{m.id} lacks {rel}"


def test_each_settings_model_can_be_imported():
    for m in manifests:
        assert m.settings_model
        module, _, attr = m.settings_model.partition(":")
        assert hasattr(importlib.import_module(module), attr), m.id


def test_every_required_capability_has_a_provider():
    provided = {c for m in manifests for c in m.provides} | set(KERNEL_CAPABILITIES)
    for m in manifests:
        missing = [c for c in m.requires if c not in provided]
        assert not missing, f"{m.id} requires {missing}, which nothing provides"


def test_every_consumed_event_has_an_emitter_or_is_a_kernel_event():
    emitted = {e for m in manifests for e in m.events_emitted}
    kernel_events = {"account.erased@1"}  # emitted by the kernel's identity service
    for m in manifests:
        missing = [e for e in m.events_consumed if e not in emitted | kernel_events]
        assert not missing, f"{m.id} consumes {missing}, which no block emits"


def test_whole_library_assembles_without_cycles():
    refs = [f"{m.id}@{m.major}" for m in manifests]
    product = ProductManifest.model_validate(
        {
            "product": "All",
            "segment": "elearning",
            "type": "online_academy",
            "locale": {"country": "ET", "languages": ["en"], "default_language": "en"},
            "blocks": refs,
        }
    )
    assert len(resolve(product, manifests, kernel_provides=KERNEL_CAPABILITIES)) == len(manifests)


def test_every_product_and_template_resolves_against_the_library():
    files = sorted((ROOT / "products").glob("*/product.yaml")) + sorted((ROOT / "templates").glob("*/*.yaml"))
    assert len(files) >= 3
    for f in files:
        product = load_product_manifest(f)
        resolve(product, manifests, kernel_provides=KERNEL_CAPABILITIES)


def test_block_catalogue_page_is_up_to_date():
    assert catalogue(BLOCKS, ROOT / "docs" / "architecture" / "block-catalogue.md", check=True) == 0
