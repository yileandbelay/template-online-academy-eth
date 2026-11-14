"""The files of a new block. Text uses {{id}}, {{family}}, {{name}}, {{package}}, {{steward}}, {{Title}}."""

FILES: dict[str, str] = {
    "pyproject.toml": """[project]
name = "{{package}}"
version = "0.1.0"
description = "{{id}}: {{Title}} block."
requires-python = ">=3.12"
dependencies = ["mek-kernel", "mek-contracts"]

[tool.uv.sources]
mek-kernel = { workspace = true }
mek-contracts = { workspace = true }

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["{{package}}"]
""",
    "manifest.yaml": """# The only file the registry reads (spec 6.1). Keep it accurate: CI checks it against the code.
id: {{id}}
version: 0.1.0
status: incubating          # proposed | incubating | beta | stable | deprecated | retired
steward: {{steward}}
summary: TODO one sentence on what this block does and for whom.
provides: []                # capabilities offered, e.g. PartyQueryV1
requires: []                # capabilities needed, e.g. NotifierV1; the installer picks the provider
events_emitted: []          # <entity>.<past_tense_verb>@<major>, e.g. enrollment.activated@1
events_consumed: []
permissions: []             # {{name}}.<entity>.<action>, e.g. {{name}}.item.edit
settings_model: {{package}}.settings:Settings
offline: false
tiers: [dedicated_hosted, on_premise, shared_saas]
""",
    "README.md": """# {{id}}

**Purpose.** TODO: what this block does and who uses it.

| | |
|---|---|
| Steward | {{steward}} |
| Status | incubating |
| Own schema | `{{name}}` |

## Interfaces
- **Provides:** (none yet) · **Requires:** (none yet)
- **Events emitted / consumed:** (none yet)
- **HTTP API:** `/api/{{name}}/v1/...`

## Settings
See `{{package}}/settings.py`. Every non-code difference between clients is a bounded setting with a safe default.

## Permissions
Declared in `manifest.yaml`; every route must require one (startup fails otherwise).

## Security
Tenant isolation test in `tests/security`; no personal data in events; handle `account.erased@1` if this block holds personal data.

## Known limits
TODO
""",
    "CHANGELOG.md": "# Changelog\n\n## 0.1.0\n- Block created from the template.\n",
    "{{package}}/__init__.py": '"""{{id}}: {{Title}} block."""\n',
    "{{package}}/block.py": '''"""Registers this block with the platform. The manifest is the single source of truth."""

from pathlib import Path

from mek_kernel.registry import BlockManifest, load_block_manifest

MANIFEST_PATH = Path(__file__).resolve().parent.parent / "manifest.yaml"


def manifest() -> BlockManifest:
    return load_block_manifest(MANIFEST_PATH)
''',
    "{{package}}/settings.py": '''"""Settings model (spec 6.1): bounded, validated, safe defaults. Secrets never live here."""

from mek_kernel.types import StrictModel


class Settings(StrictModel):
    enabled: bool = True
''',
    "{{package}}/domain/__init__.py": '"""Rules only: no FastAPI, no SQLAlchemy. Testable in milliseconds."""\n',
    "{{package}}/models.py": '"""Tables in schema \\"{{name}}\\". Only this block writes them."""\n',
    "{{package}}/services/__init__.py": '"""Use cases: check scope, change data, publish events in the same transaction."""\n',
    "{{package}}/handlers.py": '"""Event subscribers. Idempotent: the inbox records processed event ids."""\n',
    "{{package}}/queries.py": '"""Implementation of the query interfaces this block provides, if any (read models only)."""\n',
    "{{package}}/api/__init__.py": "",
    "{{package}}/api/v1/__init__.py": "",
    "{{package}}/api/v1/router.py": '''"""Public HTTP API, version 1. Every route requires a permission declared in the manifest."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/{{name}}/v1", tags=["{{name}}"])
''',
    "{{package}}/adapters/__init__.py": '"""Adapters for ports this block provides. Only if it provides a port."""\n',
    "{{package}}/migrations/README.md": "Alembic branch `{{name}}`: forward-only, expand/contract, row-level security on every new table.\n",
    "{{package}}/demo/README.md": "Demo data that lets this block be shown on its own.\n",
    "ui/README.md": "React package `@mek/{{name}}-ui`: the screens of this block. Added with the first screen.\n",
    "tests/unit/test_{{name}}_smoke.py": """def test_package_imports():
    import {{package}}  # noqa: F401
""",
    "tests/contract/test_{{name}}_manifest.py": """from {{package}}.block import manifest


def test_manifest_is_valid_and_matches_the_block():
    m = manifest()
    assert m.id == "{{id}}"
    assert m.settings_model == "{{package}}.settings:Settings"
""",
    "tests/security/test_{{name}}_boundaries.py": """from pathlib import Path

from mek_kernel.registry.boundaries import foreign_imports

BLOCK_DIR = Path(__file__).resolve().parents[2]


def test_block_imports_only_kernel_and_contracts():
    assert foreign_imports(BLOCK_DIR, "{{package}}") == []
""",
}
