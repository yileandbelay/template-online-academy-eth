"""Event envelope and event models (spec 8.1). Concrete events are added per block."""

from mek_contracts.events.envelope import EventEnvelope, event_type

__all__ = ["EventEnvelope", "event_type"]
