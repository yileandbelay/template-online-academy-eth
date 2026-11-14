from pathlib import Path

from mek_kernel.cli import validate
from mek_kernel.registry import load_product_manifest

TEMPLATES = Path(__file__).resolve().parents[3] / "templates"


def test_every_product_template_is_valid():
    files = sorted(TEMPLATES.glob("*/*.yaml"))
    assert files, "no product templates found"
    for f in files:
        load_product_manifest(f)


def test_validate_command(capsys):
    assert validate(TEMPLATES / "elearning" / "online_academy.yaml", None) == 0
    assert "valid" in capsys.readouterr().out


def test_validate_reports_unknown_blocks(capsys):
    # Blocks are planned, not built yet: resolving against an empty library must fail with a clear message.
    assert validate(TEMPLATES / "elearning" / "online_academy.yaml", TEMPLATES) == 1
    assert "not in the block library" in capsys.readouterr().err
