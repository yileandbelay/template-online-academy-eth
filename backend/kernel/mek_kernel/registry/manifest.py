"""Block and product manifests (spec 6.1 and 12). The manifest is the only file the registry reads."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

import yaml
from pydantic import Field, field_validator, model_validator

from mek_kernel.types import StrictModel

FAMILIES = ("compliance", "integrations", "automation", "ai", "business")
BLOCK_ID = re.compile(r"^(?P<family>compliance|integrations|automation|ai|business)\.(?P<name>[a-z][a-z0-9_]*)$")
CLIENT_BLOCK_ID = re.compile(r"^client\.[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
CAPABILITY = re.compile(r"^[A-Z][A-Za-z0-9]*V\d+$")  # PaymentProviderV1
EVENT_REF = re.compile(r"^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*@\d+$")  # sale.completed@1
PERMISSION = re.compile(r"^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$")  # pos.bill.close
BLOCK_REF = re.compile(r"^(?P<id>[a-z][a-z0-9_.]*)@(?P<major>\d+)$")  # business.lms@1

Status = Literal["proposed", "incubating", "beta", "stable", "deprecated", "retired"]
Tier = Literal["dedicated_hosted", "on_premise", "shared_saas"]


class BlockManifest(StrictModel):
    id: str
    version: str
    status: Status = "incubating"
    steward: str
    summary: str = Field(min_length=10)
    provides: list[str] = []  # capabilities this block offers, e.g. PartyQueryV1
    requires: list[str] = []  # capabilities it needs; the installer picks the provider
    events_emitted: list[str] = []
    events_consumed: list[str] = []
    permissions: list[str] = []
    settings_model: str | None = None
    offline: bool = False
    tiers: list[Tier] = ["dedicated_hosted", "on_premise", "shared_saas"]

    @field_validator("id")
    @classmethod
    def _check_id(cls, v: str) -> str:
        if not (BLOCK_ID.match(v) or CLIENT_BLOCK_ID.match(v)):
            raise ValueError("block id must look like <family>.<name> (spec 6.3), e.g. business.lms")
        return v

    @field_validator("version")
    @classmethod
    def _check_version(cls, v: str) -> str:
        if not SEMVER.match(v):
            raise ValueError("version must be semantic: MAJOR.MINOR.PATCH")
        return v

    @field_validator("provides", "requires")
    @classmethod
    def _check_capabilities(cls, v: list[str]) -> list[str]:
        for cap in v:
            if not CAPABILITY.match(cap):
                raise ValueError(f"capability {cap!r} must be PascalCase with a major version, e.g. PaymentProviderV1")
        return v

    @field_validator("events_emitted", "events_consumed")
    @classmethod
    def _check_events(cls, v: list[str]) -> list[str]:
        for ev in v:
            if not EVENT_REF.match(ev):
                raise ValueError(
                    f"event {ev!r} must look like <entity>.<past_tense_verb>@<major>, e.g. sale.completed@1"
                )
        return v

    @model_validator(mode="after")
    def _check_permissions_and_events(self) -> BlockManifest:
        name = self.id.split(".")[-1] if BLOCK_ID.match(self.id) else self.id.split(".")[2]
        for perm in self.permissions:
            if not PERMISSION.match(perm) or perm.split(".")[0] != name:
                raise ValueError(f"permission {perm!r} must be <block name>.<entity>.<action> and start with {name!r}")
        if set(self.events_emitted) & set(self.events_consumed):
            raise ValueError("a block may not both emit and consume the same event")
        return self

    @property
    def major(self) -> int:
        return int(self.version.split(".")[0])

    @property
    def family(self) -> str:
        return self.id.split(".")[0]


class Locale(StrictModel):
    country: str = Field(pattern=r"^[A-Z]{2}$")
    languages: list[str] = Field(min_length=1)
    default_language: str
    calendar_defaults: dict[str, Literal["ethiopian", "gregorian"]] = {}
    currency: str = Field(default="ETB", pattern=r"^[A-Z]{3}$")
    extra_currencies: list[str] = []

    @model_validator(mode="after")
    def _check_languages(self) -> Locale:
        if self.default_language not in self.languages:
            raise ValueError("default_language must be one of languages")
        unknown = set(self.calendar_defaults) - set(self.languages)
        if unknown:
            raise ValueError(f"calendar_defaults names languages that are not enabled: {sorted(unknown)}")
        return self


class DomainConfig(StrictModel):
    main: str
    redirect_from: list[str] = []


class ProductManifest(StrictModel):
    """A product is a configuration of blocks (spec 1 and 12)."""

    product: str
    segment: str
    type: str
    tier: Tier = "dedicated_hosted"
    engine: Literal["none", "erpnext"] = "none"
    domain: DomainConfig | None = None
    locale: Locale
    blocks: list[str] = Field(min_length=1)
    settings: dict[str, dict[str, object]] = {}
    theme: str | None = None
    pages: str | None = None
    content: str | None = None
    extensions: list[str] = []

    @field_validator("blocks", "extensions")
    @classmethod
    def _check_block_refs(cls, v: list[str]) -> list[str]:
        seen: set[str] = set()
        for ref in v:
            m = BLOCK_REF.match(ref)
            if not m:
                raise ValueError(f"{ref!r} must look like <block id>@<major>, e.g. business.lms@1")
            if m["id"] in seen:
                raise ValueError(f"{m['id']} is listed twice")
            seen.add(m["id"])
        return v

    @model_validator(mode="after")
    def _check_compliance(self) -> ProductManifest:
        # Spec 10: Ethiopia compliance is mandatory for Ethiopian tenants; the installer refuses a product without it.
        if self.locale.country == "ET" and not any(b.startswith("compliance.") for b in self.blocks):
            raise ValueError("an Ethiopian product must include a compliance block (for example compliance.tax@1)")
        return self

    def block_refs(self) -> dict[str, int]:
        """{block id: major version} for blocks and extensions."""
        return {m["id"]: int(m["major"]) for ref in [*self.blocks, *self.extensions] if (m := BLOCK_REF.match(ref))}


def _load_yaml(path: Path) -> dict[str, object]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def load_block_manifest(path: Path) -> BlockManifest:
    return BlockManifest.model_validate(_load_yaml(path))


def load_product_manifest(path: Path) -> ProductManifest:
    return ProductManifest.model_validate(_load_yaml(path))
