from mek_tax.block import manifest


def test_manifest_is_valid_and_matches_the_block():
    m = manifest()
    assert m.id == "compliance.tax"
    assert m.settings_model == "mek_tax.settings:Settings"
