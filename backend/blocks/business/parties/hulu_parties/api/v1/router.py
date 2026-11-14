"""Public HTTP API, version 1. Every route requires a permission declared in the manifest."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/parties/v1", tags=["parties"])
