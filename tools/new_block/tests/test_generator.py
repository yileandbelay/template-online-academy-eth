import subprocess
import sys
from pathlib import Path

import pytest
from mek_kernel.registry import load_block_manifest
from new_block.cli import generate, main

REPO = Path(__file__).resolve().parents[3]


def test_generates_full_structure(tmp_path):
    target = generate("business.lms", "stewards-business", tmp_path)
    assert target == tmp_path / "business" / "lms"
    for rel in [
        "manifest.yaml",
        "README.md",
        "CHANGELOG.md",
        "pyproject.toml",
        "mek_lms/block.py",
        "mek_lms/settings.py",
        "mek_lms/api/v1/router.py",
        "mek_lms/migrations/README.md",
        "ui/README.md",
        "tests/unit/test_lms_smoke.py",
        "tests/contract/test_lms_manifest.py",
        "tests/security/test_lms_boundaries.py",
    ]:
        assert (target / rel).exists(), rel
    manifest = load_block_manifest(target / "manifest.yaml")
    assert (manifest.id, manifest.steward, manifest.status) == ("business.lms", "stewards-business", "incubating")
    assert "{{" not in "".join(p.read_text() for p in target.rglob("*") if p.is_file())


@pytest.mark.parametrize("bad", ["lms", "Business.lms", "shop.lms", "business.lms-x", "client.mek.tips"])
def test_rejects_bad_ids(tmp_path, bad):
    with pytest.raises(ValueError):
        generate(bad, "x", tmp_path)


def test_refuses_to_overwrite(tmp_path):
    generate("business.lms", "x", tmp_path)
    with pytest.raises(FileExistsError):
        generate("business.lms", "x", tmp_path)


def test_cli_reports_errors(tmp_path, capsys):
    assert main(["lms", "--root", str(tmp_path)]) == 2
    assert "error" in capsys.readouterr().err


def test_generated_block_passes_its_own_checks(tmp_path):
    """The generated block must be lint-clean, type-clean and its own tests must pass."""
    target = generate("business.lms", "x", tmp_path)
    ruff = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "--config", str(REPO / "pyproject.toml"), str(target)],
        capture_output=True,
        text=True,
    )
    assert ruff.returncode == 0, ruff.stdout + ruff.stderr
    tests = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            str(target / "tests"),
            "-p",
            "no:cacheprovider",
            "--rootdir",
            str(target),
            "-c",
            "/dev/null",
        ],
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(target), "PATH": "/usr/bin:/bin"},
    )
    assert tests.returncode == 0, tests.stdout + tests.stderr


def test_two_blocks_have_distinct_test_files(tmp_path):
    """pytest needs unique test file names across blocks when the whole repository is collected."""
    a = generate("business.alpha", "x", tmp_path)
    b = generate("business.beta", "x", tmp_path)

    def names(d):
        return {p.name for p in (d / "tests").rglob("test_*.py")}

    assert names(a).isdisjoint(names(b))
