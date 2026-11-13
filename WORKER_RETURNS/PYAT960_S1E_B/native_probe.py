#!/usr/bin/env python3
"""Print explicit Q2 direct-certificate native selector evidence on Linux."""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from rawlsing_next.pre553_c11_repository import C11Repository  # noqa: E402
from rawlsing_next.pre553_empirical_objects import RespondentEvent  # noqa: E402
from rawlsing_next.pre553_r157_projection_adapter import (  # noqa: E402
    build_validated_c11_release_from_config,
    decode_fixture_config,
)
from rawlsing_next.pre553_source_i02_handoff import open_direct_native_i03  # noqa: E402
from rawlsing_next.tests.test_pyat960_s1e_support import (  # noqa: E402
    RecordingBodySink,
    build,
    event_refs_from_certificate,
    source_fixture,
)


def main() -> int:
    proof = Path(tempfile.mkdtemp(prefix="pyat960-q2-b-native-"))
    fixture = source_fixture(proof)
    sink = RecordingBodySink()
    handoff = build(
        proof, fixture, name="native.sqlite", body_sink=sink)
    incidence = decode_fixture_config(fixture["config"], fixture["path"])
    try:
        legacy = build_validated_c11_release_from_config(
            fixture["config"], incidence=incidence, batch_size=4)
    finally:
        incidence.close()
    repository = C11Repository((legacy,))
    if not os.path.isdir("/proc/self/fd"):
        print(json.dumps({
            "host": "non_linux",
            "native_selector": "HOLD_DEPENDENCY_LINUX_PROC_SELF_FD",
        }, indent=2))
        return 0
    reader = open_direct_native_i03(handoff, repository, legacy.release_ref)
    try:
        index = repository._i03_release_indices[
            (legacy.release_ref, handoff.universe_ref)]
        certificate_events = event_refs_from_certificate(
            Path(handoff.destination))
        selected = []
        for respondent in index.events_by_respondent.values():
            for event in respondent:
                assert isinstance(event, RespondentEvent)
                selected.append(event.ref.key)
        print(json.dumps({
            "host": "linux_proc_self_fd",
            "certificate_roots": {
                "logical": handoff.roots.logical,
                "physical": handoff.roots.physical,
                "release": handoff.roots.release,
                "source": handoff.roots.source,
                "replay": handoff.roots.replay,
                "universe": handoff.roots.universe,
                "schema": handoff.roots.schema,
            },
            "certificate_event_count": len(certificate_events),
            "native_selected_event_count": len(selected),
            "native_selected_refs_equal_certificate": set(selected) == {
                ref for ref in certificate_events},
            "native_reader_closed": True,
            "body_transport": dict(handoff.body_transport),
        }, indent=2, sort_keys=True))
    finally:
        reader.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
