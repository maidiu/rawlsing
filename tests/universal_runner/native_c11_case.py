"""Committed sourcefree C11 fixture built through the existing native owner."""
from __future__ import annotations

from rawlsing_next.tests.test_pre553_c11_repository_ingest import _candidate


def build_candidate(tag: str = "R09"):
    return _candidate(tag, event_order=("e1", "e2"))
