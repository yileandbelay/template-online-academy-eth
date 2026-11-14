"""Public HTTP API, version 1. Every route requires a permission declared in the manifest."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/exams/v1", tags=["exams"])
