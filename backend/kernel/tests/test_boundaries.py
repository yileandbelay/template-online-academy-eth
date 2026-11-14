from pathlib import Path

from mek_kernel.registry.boundaries import foreign_imports

BLOCKS = Path(__file__).resolve().parents[2] / "blocks"


def test_no_block_imports_another_block(tmp_path):
    pkg = tmp_path / "mek_a"
    pkg.mkdir()
    (pkg / "x.py").write_text(
        "import mek_b.models\nfrom mek_kernel import types\nfrom mek_contracts.types import Money\n"
    )
    assert foreign_imports(tmp_path, "mek_a") == ["mek_a/x.py:1 imports mek_b.models"]


def test_every_real_block_respects_boundaries():
    for manifest in BLOCKS.glob("*/*/manifest.yaml"):
        block_dir = manifest.parent
        package = f"mek_{block_dir.name}"
        assert foreign_imports(block_dir, package) == [], block_dir
