from pathlib import Path

from hulu_kernel.registry.boundaries import foreign_imports

BLOCKS = Path(__file__).resolve().parents[2] / "blocks"


def test_no_block_imports_another_block(tmp_path):
    pkg = tmp_path / "hulu_a"
    pkg.mkdir()
    (pkg / "x.py").write_text(
        "import hulu_b.models\nfrom hulu_kernel import types\nfrom hulu_contracts.types import Money\n"
    )
    assert foreign_imports(tmp_path, "hulu_a") == ["hulu_a/x.py:1 imports hulu_b.models"]


def test_every_real_block_respects_boundaries():
    for manifest in BLOCKS.glob("*/*/manifest.yaml"):
        block_dir = manifest.parent
        package = f"hulu_{block_dir.name}"
        assert foreign_imports(block_dir, package) == [], block_dir
