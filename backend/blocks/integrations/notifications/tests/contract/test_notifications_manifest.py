from mek_notifications.block import manifest


def test_manifest_is_valid_and_matches_the_block():
    m = manifest()
    assert m.id == "integrations.notifications"
    assert m.settings_model == "mek_notifications.settings:Settings"
