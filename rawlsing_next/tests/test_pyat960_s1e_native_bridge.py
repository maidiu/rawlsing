"""Q2 B-role native selector bridge: real on Linux, typed host hold on Darwin.

The body repository is the sealed C11 release reconstructed directly from the
Q2 body tee.  No second source decode and no legacy full-object comparator are
used; the existing direct certificate selectors are installed over the same Q2
bodies.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from rawlsing_next._pre553_external_i02_certificate import (
    ExternalI02IntegrityError,
)
from rawlsing_next.pre553_empirical_objects import RespondentEvent
from rawlsing_next.pre553_source_i02_handoff import open_direct_native_i03
from rawlsing_next.tests.test_pyat960_s1e_native_fact import (
    _build_native,
    _native_fixture,
)
from rawlsing_next.tests.test_pyat960_s1e_support import (
    event_refs_from_certificate,
)


def test_s1e_q2_certificate_drives_native_selector_when_host_capable(tmp_path):
    fixture = _native_fixture(tmp_path / "native")
    handoff, release, source = _build_native(
        tmp_path / "native", fixture, fixture["document"], "native.sqlite")
    assert handoff.body_transport is not None
    assert source["body_release_built_from_q2_tee"] is True
    assert handoff.stats.source_reads == 1
    assert handoff.stats.decode_calls == 1
    assert handoff.stats.full_c11_builds == 0

    repository = source["repo"]
    if not os.path.isdir("/proc/self/fd"):
        with pytest.raises(
            ExternalI02IntegrityError,
            match="Linux /proc/self/fd|descriptor-pinned",
        ):
            open_direct_native_i03(
                handoff, repository, release.release_ref)
        return

    reader = open_direct_native_i03(
        handoff, repository, release.release_ref)
    try:
        key = (release.release_ref, handoff.universe_ref)
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
