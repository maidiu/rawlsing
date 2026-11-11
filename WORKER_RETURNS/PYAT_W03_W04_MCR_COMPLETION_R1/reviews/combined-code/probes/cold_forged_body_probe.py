#!/usr/bin/env python3
"""Direct cold-helper forged-body negative through the real C11 repository.

The facade pre-hashes the body; this probe deliberately bypasses that by calling
the internal builder with a mutated semantic projection. It expects materialization
to refuse because object identity is deterministic from the body.
"""
from __future__ import annotations

import json
import os
from dataclasses import replace
from pathlib import Path

from rawlsing_next._pre553_w03_cold_compact import ColdCompactBuilder
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import RespondentEvent
from rawlsing_next.pre553_source_backed_c11_facade import build_validated_source_backed_c11_release_from_stream
from rawlsing_next.tests.test_pre553_route_b_production import _fixture


def main() -> int:
    os.environ.pop("RAWLSING_C11_ACCELERATOR_POLICY", None)
    os.environ.pop("RAWLSING_C11_ACCELERATOR_DIR", None)
    fx = _fixture()
    eager = build_validated_source_backed_c11_release_from_stream(fx["stream"], fx["projection"])
    event = next(obj for obj in eager.public_objects if isinstance(obj, RespondentEvent))
    forged = json.loads(json.dumps(event.semantic_projection()))
    forged["semantic_fields"]["raw_response_value"] = {
        "$raw_physical_value": {
            "codec": "PRE553_R5_TYPED_VALUE_CODEC@1.0.0",
            "schema": "PRE553_EXACT_PHYSICAL_VALUE_MATERIAL@1.0.0",
            "token": {"t": "str", "v": "999"},
        }
    }
    builder = ColdCompactBuilder()
    builder.add_event(event, projection=forged)
    compact = builder.finish(eager.release_ref, eager.replay_manifest.ref)
    sealed = replace(eager, public_objects=compact)
    repository = C11Repository((sealed,))
    refused = False
    error = None
    try:
        repository.resolve_object_exact(event.ref)
    except Exception as exc:  # exact refusal is the expected result
        refused = True
        error = type(exc).__name__
    output = {
        "schema": "W03_W04_COLD_FORGED_BODY_PROBE@1",
        "sourcefree": True,
        "selector_ref": event.ref.key,
        "original_content_hash": event.content_hash,
        "forged_materialization_refused": refused,
        "error_type": error,
        "note": "The facade pre-check is primary; deterministic materialization is the second guard.",
    }
    path = Path(__file__).resolve().parent / "cold_forged_body_probe.json"
    path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
