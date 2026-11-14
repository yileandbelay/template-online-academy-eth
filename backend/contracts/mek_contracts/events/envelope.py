"""CloudEvents 1.0 envelope used on the outbox (spec 8.1).

Payloads carry ids and amounts, never personal data: details are read through query interfaces.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any

from mek_kernel.types import StrictModel
from pydantic import Field, field_validator

EVENT_TYPE = re.compile(r"^et\.mek\.[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*\.v\d+$")


def event_type(entity: str, verb: str, major: int) -> str:
    """event_type("sale", "completed", 1) == "et.mek.sale.completed.v1" (spec 6.3)."""
    return f"et.mek.{entity}.{verb}.v{major}"


class EventEnvelope(StrictModel):
    specversion: str = "1.0"
    id: str = Field(min_length=1)  # unique; the inbox key
    type: str
    source: str  # /tenants/<tenant>/blocks/<block>
    subject: str  # <block>/<entity>/<id>
    time: datetime
    datacontenttype: str = "application/json"
    dataschema: str  # mek:contracts/events/<name>/<major>
    tenant: str
    traceparent: str | None = None
    data: dict[str, Any]

    @field_validator("type")
    @classmethod
    def _check_type(cls, v: str) -> str:
        if not EVENT_TYPE.match(v):
            raise ValueError("type must look like et.mek.<entity>.<verb>.v<major>")
        return v

    @field_validator("time")
    @classmethod
    def _utc(cls, v: datetime) -> datetime:
        if v.tzinfo is None or v.utcoffset() != UTC.utcoffset(None):
            raise ValueError("event time must be UTC")
        return v

    @classmethod
    def new(
        cls,
        *,
        id: str,
        entity: str,
        verb: str,
        major: int,
        tenant: str,
        block: str,
        subject_id: str,
        data: dict[str, Any],
    ) -> EventEnvelope:
        return cls(
            id=id,
            type=event_type(entity, verb, major),
            source=f"/tenants/{tenant}/blocks/{block}",
            subject=f"{block.split('.')[-1]}/{entity}/{subject_id}",
            time=datetime.now(UTC),
            dataschema=f"mek:contracts/events/{entity}.{verb}/{major}",
            tenant=tenant,
            data=data,
        )
