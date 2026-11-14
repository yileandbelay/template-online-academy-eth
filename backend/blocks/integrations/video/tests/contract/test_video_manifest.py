from mek_video.block import manifest


def test_manifest_is_valid_and_matches_the_block():
    m = manifest()
    assert m.id == "integrations.video"
    assert m.settings_model == "mek_video.settings:Settings"
