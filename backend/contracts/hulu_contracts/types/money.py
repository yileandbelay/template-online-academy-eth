"""Money: a decimal amount with an ISO 4217 currency. Never a float (spec 9.1)."""

from __future__ import annotations

from decimal import Decimal
from typing import Annotated

from hulu_kernel.types import StrictModel
from pydantic import Field, field_serializer, field_validator

Currency = Annotated[str, Field(pattern=r"^[A-Z]{3}$")]


class Money(StrictModel):
    amount: Decimal
    currency: Currency = "ETB"  # ETB is the default currency in every language (spec 2, principle 8)

    @field_validator("amount", mode="before")
    @classmethod
    def _no_floats(cls, v: object) -> object:
        if isinstance(v, float):
            raise ValueError("pass money amounts as strings or Decimal, never float")
        return v

    @field_serializer("amount")
    def _amount_as_string(self, v: Decimal) -> str:
        return format(v, "f")

    def _same_currency(self, other: Money) -> None:
        if self.currency != other.currency:
            raise ValueError(f"cannot combine {self.currency} and {other.currency}")

    def __add__(self, other: Money) -> Money:
        self._same_currency(other)
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __sub__(self, other: Money) -> Money:
        self._same_currency(other)
        return Money(amount=self.amount - other.amount, currency=self.currency)

    def is_zero(self) -> bool:
        return self.amount == 0
