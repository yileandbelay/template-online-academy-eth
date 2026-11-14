from pathlib import Path

from hulu_kernel.registry.boundaries import foreign_imports

BLOCK_DIR = Path(__file__).resolve().parents[2]


def test_block_imports_only_kernel_and_contracts():
    assert foreign_imports(BLOCK_DIR, "hulu_tax") == []
