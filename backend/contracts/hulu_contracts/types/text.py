"""TranslatableText: optional per-language values with fallback (spec 9.1)."""

from __future__ import annotations

from pydantic import RootModel, model_validator


class TranslatableText(RootModel[dict[str, str]]):
    """{"en": "Course", "am": "ኮርስ"}. English is required; other languages are optional."""

    @model_validator(mode="after")
    def _english_required(self) -> TranslatableText:
        if not self.root.get("en"):
            raise ValueError("translatable text needs an English value")
        return self

    def get(self, language: str, fallback: str = "en") -> str:
        return self.root.get(language) or self.root[fallback]
