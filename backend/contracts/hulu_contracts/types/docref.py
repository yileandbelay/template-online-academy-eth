"""DocumentRef: how one block refers to another block's record, never by foreign key (spec 9.1)."""

from __future__ import annotations

from hulu_kernel.types import StrictModel
from pydantic import Field


class DocumentRef(StrictModel):
    block: str = Field(pattern=r"^[a-z][a-z0-9_.]*$")  # business.lms
    type: str = Field(pattern=r"^[a-z][a-z0-9_]*$")  # course
    id: str = Field(min_length=1)

    def __str__(self) -> str:
        return f"{self.block}/{self.type}/{self.id}"
