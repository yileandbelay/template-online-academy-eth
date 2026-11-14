from hulu_payments.block import manifest


def test_manifest_is_valid_and_matches_the_block():
    m = manifest()
    assert m.id == "integrations.payments"
    assert m.settings_model == "hulu_payments.settings:Settings"
