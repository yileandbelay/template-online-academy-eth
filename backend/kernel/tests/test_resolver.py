import pytest
from mek_kernel.registry import BlockManifest, ProductManifest, ResolutionError, resolve


def block(id_, provides=(), requires=(), version="1.0.0", status="stable"):
    name = id_.split(".")[-1]
    return BlockManifest(
        id=id_,
        version=version,
        status=status,
        steward="x",
        summary="A test block for resolving.",
        provides=list(provides),
        requires=list(requires),
        permissions=[f"{name}.thing.read"],
    )


def product(*refs):
    return ProductManifest.model_validate(
        {
            "product": "P",
            "segment": "elearning",
            "type": "online_academy",
            "locale": {"country": "ET", "languages": ["en"], "default_language": "en"},
            "blocks": [*refs, "compliance.tax@1"],
        }
    )


TAX = block("compliance.tax")


def test_providers_load_before_consumers():
    parties = block("business.parties", provides=["PartyQueryV1"])
    lms = block("business.lms", requires=["PartyQueryV1"])
    order = [m.id for m in resolve(product("business.lms@1", "business.parties@1"), [lms, parties, TAX])]
    assert order.index("business.parties") < order.index("business.lms")


def test_missing_block():
    with pytest.raises(ResolutionError, match="not in the block library"):
        resolve(product("business.lms@1"), [TAX])


def test_wrong_major():
    lms = block("business.lms", version="2.0.0")
    with pytest.raises(ResolutionError, match="major version 2"):
        resolve(product("business.lms@1"), [lms, TAX])


def test_missing_capability():
    lms = block("business.lms", requires=["PartyQueryV1"])
    with pytest.raises(ResolutionError, match="no listed block provides"):
        resolve(product("business.lms@1"), [lms, TAX])


def test_kernel_can_provide_capability():
    lms = block("business.lms", requires=["AuditV1"])
    assert resolve(product("business.lms@1"), [lms, TAX], kernel_provides=["AuditV1"])


def test_two_providers_must_be_chosen():
    a = block("integrations.pay_a", provides=["PaymentProviderV1"])
    b = block("integrations.pay_b", provides=["PaymentProviderV1"])
    lms = block("business.lms", requires=["PaymentProviderV1"])
    with pytest.raises(ResolutionError, match="more than one"):
        resolve(product("business.lms@1", "integrations.pay_a@1", "integrations.pay_b@1"), [lms, a, b, TAX])


def test_cycle_is_refused():
    a = block("business.a", provides=["AV1"], requires=["BV1"])
    b = block("business.b", provides=["BV1"], requires=["AV1"])
    with pytest.raises(ResolutionError, match="cycle"):
        resolve(product("business.a@1", "business.b@1"), [a, b, TAX])


def test_retired_block_refused():
    old = block("business.old", status="retired")
    with pytest.raises(ResolutionError, match="retired"):
        resolve(product("business.old@1"), [old, TAX])
