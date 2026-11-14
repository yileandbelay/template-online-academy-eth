from mek_feedback.block import manifest


def test_manifest_is_valid_and_matches_the_block():
    m = manifest()
    assert m.id == "business.feedback"
    assert m.settings_model == "mek_feedback.settings:Settings"
