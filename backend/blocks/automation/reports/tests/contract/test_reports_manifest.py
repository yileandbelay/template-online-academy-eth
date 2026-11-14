from hulu_reports.block import manifest


def test_manifest_is_valid_and_matches_the_block():
    m = manifest()
    assert m.id == "automation.reports"
    assert m.settings_model == "hulu_reports.settings:Settings"
