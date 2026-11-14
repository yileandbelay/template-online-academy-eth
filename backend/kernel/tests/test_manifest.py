import pytest
from hulu_kernel.registry import BlockManifest, ProductManifest
from pydantic import ValidationError

BLOCK = {
    "id": "business.lms",
    "version": "0.1.0",
    "steward": "platform-leads",
    "summary": "Courses, lessons, enrolment and progress.",
    "provides": ["CatalogQueryV1"],
    "requires": ["PartyQueryV1"],
    "events_emitted": ["enrollment.activated@1"],
    "permissions": ["lms.course.edit"],
}

PRODUCT = {
    "product": "Test Academy",
    "segment": "elearning",
    "type": "online_academy",
    "locale": {
        "country": "ET",
        "languages": ["en", "am"],
        "default_language": "en",
        "calendar_defaults": {"am": "ethiopian", "en": "gregorian"},
    },
    "blocks": ["business.lms@1", "compliance.tax@1"],
}


def test_valid_block():
    m = BlockManifest.model_validate(BLOCK)
    assert (m.family, m.major, m.status) == ("business", 0, "incubating")


@pytest.mark.parametrize(
    "change",
    [
        {"id": "lms"},  # no family
        {"id": "shop.lms"},  # unknown family
        {"version": "1.0"},  # not semver
        {"provides": ["catalog"]},  # capability must be PascalCase + major
        {"events_emitted": ["enrollment_activated"]},  # no major version
        {"permissions": ["pos.bill.close"]},  # wrong block name prefix
        {"events_consumed": ["enrollment.activated@1"]},  # emits and consumes the same event
        {"unknown_field": 1},  # strict: unknown fields rejected
    ],
)
def test_invalid_block(change):
    with pytest.raises(ValidationError):
        BlockManifest.model_validate({**BLOCK, **change})


def test_valid_product():
    p = ProductManifest.model_validate(PRODUCT)
    assert p.block_refs() == {"business.lms": 1, "compliance.tax": 1}


def test_ethiopian_product_needs_compliance():
    with pytest.raises(ValidationError, match="compliance"):
        ProductManifest.model_validate({**PRODUCT, "blocks": ["business.lms@1"]})


def test_default_language_must_be_enabled():
    bad = {**PRODUCT, "locale": {**PRODUCT["locale"], "default_language": "om"}}
    with pytest.raises(ValidationError, match="default_language"):
        ProductManifest.model_validate(bad)


def test_duplicate_block_rejected():
    with pytest.raises(ValidationError, match="twice"):
        ProductManifest.model_validate({**PRODUCT, "blocks": ["business.lms@1", "business.lms@1", "compliance.tax@1"]})
