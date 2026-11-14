from mek_parties.block import manifest


def test_manifest_is_valid_and_matches_the_block():
    m = manifest()
    assert m.id == "business.parties"
    assert m.settings_model == "mek_parties.settings:Settings"
