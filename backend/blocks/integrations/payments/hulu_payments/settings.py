"""Settings model (spec 6.1): bounded, validated, safe defaults. Secrets never live here."""

from hulu_kernel.types import StrictModel


class Settings(StrictModel):
    enabled: bool = True
