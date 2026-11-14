from mek_imports.block import manifest


def test_manifest_is_valid_and_matches_the_block():
    m = manifest()
    assert m.id == "automation.imports"
    assert m.settings_model == "mek_imports.settings:Settings"
