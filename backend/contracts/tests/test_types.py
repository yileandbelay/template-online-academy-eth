from datetime import UTC, datetime
from decimal import Decimal

import pytest
from hulu_contracts.events import EventEnvelope, event_type
from hulu_contracts.types import DocumentRef, Money, TranslatableText
from pydantic import ValidationError


def test_money_is_decimal_and_serialises_as_string():
    m = Money(amount="1250.00")
    assert m.currency == "ETB"
    assert m.model_dump()["amount"] == "1250.00"
    assert m.model_dump_json() == '{"amount":"1250.00","currency":"ETB"}'


def test_money_rejects_float_and_bad_currency():
    with pytest.raises(ValidationError):
        Money(amount=12.5)
    with pytest.raises(ValidationError):
        Money(amount="1", currency="birr")


def test_money_arithmetic_and_currency_mismatch():
    assert (Money(amount="10.10") + Money(amount="0.20")).amount == Decimal("10.30")
    assert (Money(amount="10") - Money(amount="4")).amount == Decimal("6")
    with pytest.raises(ValueError, match="cannot combine"):
        Money(amount="1") + Money(amount="1", currency="USD")


def test_translatable_text_falls_back_to_english():
    t = TranslatableText({"en": "Course", "am": "ኮርስ"})
    assert t.get("am") == "ኮርስ" and t.get("om") == "Course"
    with pytest.raises(ValidationError):
        TranslatableText({"am": "ኮርስ"})


def test_document_ref():
    assert str(DocumentRef(block="business.lms", type="course", id="42")) == "business.lms/course/42"


def test_event_type_and_envelope():
    assert event_type("sale", "completed", 1) == "et.hulu.sale.completed.v1"
    e = EventEnvelope.new(
        id="01J",
        entity="enrollment",
        verb="activated",
        major=1,
        tenant="mek",
        block="business.lms",
        subject_id="7",
        data={"course": "business.lms/course/42"},
    )
    assert e.type == "et.hulu.enrollment.activated.v1"
    assert e.subject == "lms/enrollment/7"
    assert e.time.tzinfo is not None


def test_envelope_rejects_local_time_and_bad_type():
    base = dict(id="1", type="et.hulu.a.b.v1", source="/s", subject="s", dataschema="x", tenant="t", data={})
    with pytest.raises(ValidationError):
        EventEnvelope(**base, time=datetime(2026, 1, 1))  # naive
    with pytest.raises(ValidationError):
        EventEnvelope(**{**base, "type": "sale.completed"}, time=datetime.now(UTC))
