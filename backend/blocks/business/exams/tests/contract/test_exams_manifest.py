from hulu_exams.block import manifest


def test_manifest_is_valid_and_matches_the_block():
    m = manifest()
    assert m.id == "business.exams"
    assert m.settings_model == "hulu_exams.settings:Settings"
