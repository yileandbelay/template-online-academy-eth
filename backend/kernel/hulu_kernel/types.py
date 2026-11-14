"""Base types every block uses. Strict by default: unknown fields are rejected (spec 15, rule 3)."""

from pydantic import BaseModel, ConfigDict


class StrictModel(BaseModel):
    """Base class for all API, event, port and settings models."""

    model_config = ConfigDict(extra="forbid", frozen=False, str_strip_whitespace=True)
