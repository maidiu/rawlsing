"""Execute the existing C11 ingest/repository owner on a sourcefree fixture."""
from __future__ import annotations

from native_c11_case import build_candidate
from rawlsing_next.pre553_c11_ingest import ingest_c11_source_release
from rawlsing_next.pre553_c11_repository import C11Repository


def run_native() -> dict:
    candidate = build_candidate("R09")
    repository = C11Repository()
    result = ingest_c11_source_release(candidate, repository)
    release = repository.resolve_release_exact(result.release_ref)
    return {
        "accepted": result.accepted,
        "disposition": result.disposition.value,
        "event_count": len(candidate.respondent_events),
        "release_id": release.release_id,
        "repository_length": len(repository),
        "m01_m18_count": len(result.m01_m18_coverage),
    }


RESULT = run_native()
