"""Q2 B-role native selector bridge: real on Linux, typed host hold on Darwin."""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from rawlsing_next._pre553_external_i02_certificate import (
    ExternalI02IntegrityError,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import RespondentEvent
from rawlsing_next.pre553_r157_projection_adapter import (
    build_validated_c11_release_from_config,
    decode_fixture_config,
)
from rawlsing_next.pre553_source_i02_handoff import open_direct_native_i03
from rawlsing_next.tests.test_pyat960_s1e_support import (
    build,
    event_refs_from_certificate,
    source_fixture,
)


def test_s1e_q2_certificate_drives_native_selector_when_host_capable(tmp_path):
    fixture = source_fixture(tmp_path / "native")
    handoff = build(tmp_path / "native", fixture, name="native.sqlite")
    incidence = decode_fixture_config(fixture["config"], fixture["path"])
    try:
        legacy = build_validated_c11_release_from_config(
            fixture["config"], incidence=incidence, batch_size=4)
    finally:
        incidence.close()
    repository = C11Repository((legacy,))
    if not os.path.isdir("/proc/self/fd"):
        with pytest.raises(
            ExternalI02IntegrityError,
            match="Linux /proc/self/fd|descriptor-pinned",
        ):
            open_direct_native_i03(
                handoff, repository, legacy.release_ref)
        return

    reader = open_direct_native_i03(
        handoff, repository, legacy.release_ref)
    try:
        key = (legacy.release_ref, handoff.universe_ref)
        index = repository._i03_release_indices[key]
        certificate_events = event_refs_from_certificate(
            Path(handoff.destination))
        selected_refs = set()
        selected_rows = 0
        for respondent in index.events_by_respondent.values():
            events = list(respondent)
            selected_rows += len(events)
            for event in events:
                assert isinstance(event, RespondentEvent)
                assert event.ref.key in certificate_events
                selected_refs.add(event.ref.key)
        assert selected_rows == handoff.stats.event_count
        assert selected_refs == certificate_events
    finally:
        reader.close()
