import importlib.util
import sys
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location("rebrand", Path(__file__).resolve().parents[1] / "rebrand.py")
rebrand_module = importlib.util.module_from_spec(SPEC)
sys.modules["rebrand"] = rebrand_module  # dataclasses look the module up by name
SPEC.loader.exec_module(rebrand_module)
rebrand = rebrand_module.rebrand


def make_tree(root: Path) -> None:
    (root / "backend" / "kernel" / "acme_kernel").mkdir(parents=True)
    (root / "backend" / "kernel" / "acme_kernel" / "__init__.py").write_text(
        '"""Acme kernel. ACME_HOME; acme-kernel; et.acme.sale.completed.v1"""\n'
    )
    (root / "pyproject.toml").write_text('name = "acme-kernel"\n')
    (root / "README.md").write_text("The Acme platform. Mek Academy is a product.\n")
    (root / "uv.lock").write_text("acme-kernel\n")
    (root / ".venv").mkdir()
    (root / ".venv" / "x.py").write_text("acme\n")
    (root / "logo.png").write_bytes(b"\x89PNG acme \xff\xfe")


def test_rebrand_changes_text_names_and_folders(tmp_path):
    make_tree(tmp_path)
    result = rebrand(tmp_path, "acme", "zeta")
    init = tmp_path / "backend" / "kernel" / "zeta_kernel" / "__init__.py"
    assert init.read_text() == '"""Zeta kernel. ZETA_HOME; zeta-kernel; et.zeta.sale.completed.v1"""\n'
    assert not (tmp_path / "backend" / "kernel" / "acme_kernel").exists()
    assert (tmp_path / "pyproject.toml").read_text() == 'name = "zeta-kernel"\n'
    assert "Mek Academy is a product" in (tmp_path / "README.md").read_text()  # unrelated product name untouched
    assert result.paths_renamed


def test_rebrand_skips_lockfile_venv_and_binary(tmp_path):
    make_tree(tmp_path)
    rebrand(tmp_path, "acme", "zeta")
    assert (tmp_path / "uv.lock").read_text() == "acme-kernel\n"
    assert (tmp_path / ".venv" / "x.py").read_text() == "acme\n"
    assert (tmp_path / "logo.png").read_bytes().startswith(b"\x89PNG acme")


def test_dry_run_changes_nothing(tmp_path):
    make_tree(tmp_path)
    result = rebrand(tmp_path, "acme", "zeta", dry_run=True)
    assert result.files_changed and (tmp_path / "backend" / "kernel" / "acme_kernel").exists()
    assert (tmp_path / "pyproject.toml").read_text() == 'name = "acme-kernel"\n'


def test_display_name_override(tmp_path):
    (tmp_path / "README.md").write_text("Acme platform\n")
    rebrand(tmp_path, "acme", "mek", display="MEK Software")
    assert (tmp_path / "README.md").read_text() == "MEK Software platform\n"


@pytest.mark.parametrize("old,new", [("Acme", "zeta"), ("acme", "zeta co"), ("acme", "acme")])
def test_rejects_bad_names(tmp_path, old, new):
    with pytest.raises(ValueError):
        rebrand(tmp_path, old, new)
