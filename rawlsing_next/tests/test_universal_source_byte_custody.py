import hashlib
import json
import mmap
import os
from dataclasses import replace
from pathlib import Path
import subprocess
import sys

import pandas as pd
import pyreadstat
import pytest

from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import ExactRef, RespondentEvent
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_physical_decoder import (
    DecoderError,
    PhysicalMissingState,
    decode_dta,
    decode_sav,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    build_validated_source_backed_c11_release,
    physical_value_binding_key,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate,
    _cell_map,
    _query,
    _query_authority,
)
from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture


_ROWS = {
    "X": [1, 0, None],
    "Y": [1, 0, 1],
    "M": ["AB", "A", ""],
    "O": ["AB", "BA", "AB"],
    "R": ["XY", "XZ", "XY"],
    "G": ["A", "B", "A"],
    "W": [2, 1, 3],
}
_ALTERNATE_ROWS = {
    "X": [0, 1, None],
    "Y": [1, 1, 0],
    "M": ["A", "AB", ""],
    "O": ["BA", "AB", "BA"],
    "R": ["XZ", "XY", "XZ"],
    "G": ["B", "A", "B"],
    "W": [1, 2, 3],
}
_REPO_ROOT = Path(__file__).resolve().parents[2]


def _write_source(path, source_format, rows=None):
    frame = pd.DataFrame(_ROWS if rows is None else rows)
    writer = pyreadstat.write_sav if source_format == "sav" else pyreadstat.write_dta
    writer(frame, str(path))
    return path


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _decode(path, source_format, expected_sha):
    decoder = decode_sav if source_format == "sav" else decode_dta
    return decoder(path, expected_source_sha256=expected_sha)


def _same_declared_value(raw, canonical):
    if raw is None or canonical is None:
        return raw == canonical
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        try:
            return float(raw) == float(canonical)
        except (TypeError, ValueError):
            return False
    return raw == canonical


def _bind_projection(projection, incidence):
    cells = list(incidence.iter_cells(batch_size=64))
    slots = []
    for slot in projection.response_slots:
        values = []
        for rule in slot.values:
            if rule.response_state == "MISSING":
                cell = next(
                    cell for cell in cells
                    if cell.variable_name == slot.slot.name
                    and cell.missing_state is PhysicalMissingState.SYSTEM_MISSING
                )
            else:
                cell = next(
                    cell for cell in cells
                    if cell.variable_name == slot.slot.name
                    and cell.missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE
                    and _same_declared_value(cell.raw_value, rule.canonical_value)
                )
            values.append(replace(
                rule,
                physical_key=physical_value_binding_key(
                    cell.raw_value, cell.missing_state, cell.source_missing_declaration
                ),
            ))
        slots.append(replace(slot, values=tuple(values)))
    return replace(
        projection,
        expected_source_sha256=incidence.source_sha256,
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT", f"urn:test:r04byte:{incidence.source_sha256}", incidence.source_sha256
        ),
        source_artifact_id=f"SOURCE-R04BYTE-{incidence.source_sha256[:12]}",
        response_slots=tuple(slots),
    )


def _cell_signature(cells):
    return [
        (
            cell.row_ordinal,
            cell.variable_ordinal,
            cell.variable_name,
            cell.raw_value,
            cell.missing_state.value,
            repr(cell.source_missing_declaration),
        )
        for cell in cells
    ]


def _facts_from_incidence(incidence, source_format):
    fixture = _fixture(f"r04byte-{source_format}")
    projection = _bind_projection(fixture["projection"], incidence)
    release = build_validated_source_backed_c11_release(incidence, projection, batch_size=4)
    source = {
        **fixture,
        "source_sha": incidence.source_sha256,
        "projection": projection,
        "repo": C11Repository((release,)),
        "release_ref": release.release_ref,
    }
    query_authority = _query_authority(f"r04byte-{source_format}")
    predicate = _branch_predicate(source, query_authority)
    query = _query(source, query_authority, predicate, ("Y",), tag=f"r04byte-{source_format}")
    result = execute_empirical_query(
        repository=source["repo"],
        query=query,
        predicate=predicate,
        authority_registry=AuthorityRegistry((*fixture["authorities"], query_authority)),
        release_refs=(release.release_ref,),
    )
    fact = result.facts[0]
    custody = incidence.source_custody
    return {
        "source_sha256": incidence.source_sha256,
        "snapshot_sha256": custody["snapshot_sha256"],
        "release_content_hash": release.release_ref.content_hash,
        "respondent_event_count": sum(isinstance(obj, RespondentEvent) for obj in release.public_objects),
        "i03_fact_ref": fact.ref.content_hash,
        "i03_typed_state": fact.typed_state,
        "i03_raw_numerator_support": fact.raw_numerator_support,
        "i03_raw_denominator_support": fact.raw_denominator_support,
        "i03_y_cells": {
            key: value["raw_numerator_support"]
            for key, value in _cell_map(fact).items()
        },
        "cell_digest": hashlib.sha256(
            repr(_cell_signature(incidence.iter_cells(4))).encode("utf-8")
        ).hexdigest(),
    }


def _observe(path, source_format, expected_sha):
    try:
        incidence = _decode(path, source_format, expected_sha)
    except DecoderError as exc:
        return {"ok": False, "refusal": str(exc)}
    try:
        return {"ok": True, "facts": _facts_from_incidence(incidence, source_format)}
    finally:
        incidence.close()


def _cold_observation(path, source_format, expected_sha):
    incidence = _decode(path, source_format, expected_sha)
    try:
        return _facts_from_incidence(incidence, source_format)
    finally:
        incidence.close()


def _run_cold(path, source_format, expected_sha):
    script = (
        "import json, sys\n"
        "from rawlsing_next.tests.test_universal_source_byte_custody import _cold_observation\n"
        "print(json.dumps(_cold_observation(sys.argv[1], sys.argv[2], sys.argv[3]), sort_keys=True))\n"
    )
    return subprocess.run(
        [sys.executable, "-c", script, str(path), source_format, expected_sha],
        cwd=_REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )


@pytest.mark.parametrize("source_format", ("sav", "dta"))
def test_positive_generated_sav_and_dta_reach_unchanged_c11_i03_facts(tmp_path, source_format):
    path = _write_source(tmp_path / f"positive.{source_format}", source_format)
    expected_sha = _sha(path)
    observation = _observe(path, source_format, expected_sha)
    assert observation["ok"] is True
    facts = observation["facts"]
    assert facts["source_sha256"] == expected_sha
    assert facts["snapshot_sha256"] == expected_sha
    assert facts["i03_typed_state"] == "SUPPORTED"
    assert facts["i03_raw_numerator_support"] == 2
    assert facts["i03_raw_denominator_support"] == 2
    assert facts["i03_y_cells"] == {"0": 1, "1": 1}
    assert facts["respondent_event_count"] > 0


@pytest.mark.parametrize("source_format", ("sav", "dta"))
def test_replacement_after_snapshot_acquisition_keeps_original_downstream_facts(
    tmp_path, source_format, monkeypatch
):
    path = _write_source(tmp_path / f"replace.{source_format}", source_format)
    alternate = _write_source(tmp_path / f"alternate.{source_format}", source_format, _ALTERNATE_ROWS)
    original_sha = _sha(path)
    baseline = _observe(path, source_format, original_sha)
    assert baseline["ok"] is True

    import rawlsing_next.pre553_physical_decoder as decoder

    original_acquire = decoder._acquire_source_snapshot

    def acquire_then_replace(source, expected_source_sha256=None):
        snapshot = original_acquire(source, expected_source_sha256)
        os.replace(alternate, path)
        return snapshot

    monkeypatch.setattr(decoder, "_acquire_source_snapshot", acquire_then_replace)
    observed = _observe(path, source_format, original_sha)
    assert _sha(path) != original_sha
    assert observed == baseline
    assert observed["facts"]["snapshot_sha256"] == original_sha


@pytest.mark.parametrize("source_format", ("sav", "dta"))
def test_lazy_value_phase_reopens_only_the_identity_bound_snapshot(
    tmp_path, source_format, monkeypatch
):
    path = _write_source(tmp_path / f"lazy.{source_format}", source_format)
    expected_sha = _sha(path)
    baseline = _decode(path, source_format, expected_sha)
    baseline_cells = _cell_signature(baseline.iter_cells(4))
    baseline.close()

    incidence = _decode(path, source_format, expected_sha)
    snapshot_path = Path(incidence._source_snapshot.reader_path)
    _write_source(path, source_format, _ALTERNATE_ROWS)

    seen_paths = []
    if source_format == "sav":
        original_chunks = pyreadstat.read_file_in_chunks

        def hostile_chunks(reader, source, *args, **kwargs):
            seen_paths.append(Path(source))
            _write_source(path, source_format, _ALTERNATE_ROWS)
            return original_chunks(reader, source, *args, **kwargs)

        monkeypatch.setattr(pyreadstat, "read_file_in_chunks", hostile_chunks)
    else:
        original_read = pyreadstat.read_dta

        def hostile_read(source, *args, **kwargs):
            if not kwargs.get("metadataonly", False):
                seen_paths.append(Path(source))
                _write_source(path, source_format, _ALTERNATE_ROWS)
            return original_read(source, *args, **kwargs)

        monkeypatch.setattr(pyreadstat, "read_dta", hostile_read)
    observed_cells = _cell_signature(incidence.iter_cells(4))
    assert seen_paths == [snapshot_path]
    assert snapshot_path != path
    assert observed_cells == baseline_cells
    incidence.close()


@pytest.mark.parametrize("source_format", ("sav", "dta"))
def test_replacement_between_hash_gate_and_snapshot_acquisition_is_refused(
    tmp_path, source_format, monkeypatch
):
    path = _write_source(tmp_path / f"hash-gate.{source_format}", source_format)
    alternate = _write_source(tmp_path / f"hash-gate-alt.{source_format}", source_format, _ALTERNATE_ROWS)
    original_sha = _sha(path)

    import rawlsing_next.pre553_physical_decoder as decoder

    original_hash = decoder._sha

    def hash_then_replace(source):
        digest = original_hash(source)
        os.replace(alternate, path)
        return digest

    monkeypatch.setattr(decoder, "_sha", hash_then_replace)
    reader_calls = []
    monkeypatch.setattr(
        pyreadstat,
        "read_sav" if source_format == "sav" else "read_dta",
        lambda *args, **kwargs: reader_calls.append(args) or (_ for _ in ()).throw(
            AssertionError("reader must not run after identity refusal")
        ),
    )
    with pytest.raises(DecoderError, match="source sha256 mismatch before governed decode"):
        _decode(path, source_format, original_sha)
    assert reader_calls == []


@pytest.mark.parametrize("source_format", ("sav", "dta"))
def test_supplied_read_only_fd_denies_in_place_write_and_preserves_facts(
    tmp_path, source_format
):
    path = _write_source(tmp_path / f"altered.{source_format}", source_format)
    alternate = _write_source(tmp_path / f"altered-alt.{source_format}", source_format, _ALTERNATE_ROWS)
    expected_sha = _sha(path)
    incidence = _decode(path, source_format, expected_sha)
    snapshot = incidence._source_snapshot
    alternate_bytes = alternate.read_bytes()
    baseline = _facts_from_incidence(incidence, source_format)
    with pytest.raises(OSError):
        os.write(snapshot.fd, b"x")
    with pytest.raises(OSError):
        os.pwrite(snapshot.fd, alternate_bytes, 0)
    with pytest.raises(OSError):
        os.ftruncate(snapshot.fd, len(alternate_bytes))
    with pytest.raises(OSError):
        os.open(f"/dev/fd/{snapshot.fd}", os.O_RDWR)
    assert snapshot.access_mode == "O_RDONLY"
    assert incidence.source_custody["reader_access_mode"] == "O_RDONLY"
    assert incidence.verify_source_identity() == expected_sha
    assert _facts_from_incidence(incidence, source_format) == baseline
    incidence.close()


@pytest.mark.parametrize("source_format", ("sav", "dta"))
def test_same_path_new_source_is_a_new_identity_and_never_retains_the_old(
    tmp_path, source_format
):
    path = _write_source(tmp_path / f"new-identity.{source_format}", source_format)
    old_incidence = _decode(path, source_format, _sha(path))
    old_sha = old_incidence.source_sha256
    old_cells = _cell_signature(old_incidence.iter_cells(4))
    old_facts = _facts_from_incidence(old_incidence, source_format)

    _write_source(path, source_format, _ALTERNATE_ROWS)
    new_sha = _sha(path)
    assert new_sha != old_sha
    new_observation = _observe(path, source_format, new_sha)
    assert new_observation["ok"] is True
    assert new_observation["facts"]["source_sha256"] == new_sha
    assert new_observation["facts"]["i03_fact_ref"] != old_facts["i03_fact_ref"]
    assert new_observation["facts"]["i03_y_cells"] != old_facts["i03_y_cells"]

    assert old_incidence.source_sha256 == old_sha
    assert _cell_signature(old_incidence.iter_cells(4)) == old_cells
    assert _facts_from_incidence(old_incidence, source_format) == old_facts
    old_incidence.close()

    refused = _observe(path, source_format, old_sha)
    assert refused["ok"] is False
    assert "source sha256 mismatch before governed decode" in refused["refusal"]


@pytest.mark.parametrize("source_format", ("sav", "dta"))
def test_fresh_process_refuses_changed_bytes_under_old_digest_and_restores_positive(
    tmp_path, source_format
):
    path = _write_source(tmp_path / f"cold.{source_format}", source_format)
    original_bytes = path.read_bytes()
    original_sha = hashlib.sha256(original_bytes).hexdigest()
    baseline = _run_cold(path, source_format, original_sha)
    assert baseline.returncode == 0, baseline.stderr
    baseline_facts = json.loads(baseline.stdout)

    _write_source(path, source_format, _ALTERNATE_ROWS)
    fault = _run_cold(path, source_format, original_sha)
    assert fault.returncode != 0
    assert fault.stdout == ""
    assert "source sha256 mismatch before governed decode" in fault.stderr

    path.write_bytes(original_bytes)
    restored = _run_cold(path, source_format, original_sha)
    assert restored.returncode == 0, restored.stderr
    assert json.loads(restored.stdout) == baseline_facts


def test_snapshot_close_releases_private_source_bytes(tmp_path):
    path = _write_source(tmp_path / "cleanup.sav", "sav")
    incidence = _decode(path, "sav", _sha(path))
    snapshot = incidence._source_snapshot
    snapshot_path = snapshot.path
    snapshot_directory = snapshot.directory
    assert not snapshot_path.exists()
    assert snapshot_directory.exists()
    assert Path(snapshot.reader_path).as_posix().startswith("/dev/fd/")
    incidence.close()
    assert not snapshot_path.exists()
    assert not snapshot_directory.exists()
    assert snapshot.access_mode == "CLOSED"
    with pytest.raises(OSError):
        os.fstat(snapshot.fd)
    with pytest.raises(DecoderError, match="source snapshot is closed"):
        list(incidence.iter_cells())


def test_lazy_value_phase_uses_only_the_content_bound_snapshot(tmp_path, monkeypatch):
    path = _write_source(tmp_path / "lazy-custody.sav", "sav")
    expected_sha = _sha(path)
    baseline = _decode(path, "sav", expected_sha)
    baseline_cells = _cell_signature(baseline.iter_cells(4))
    baseline.close()

    incidence = _decode(path, "sav", expected_sha)
    snapshot_path = Path(incidence._source_snapshot.reader_path)
    _write_source(path, "sav", _ALTERNATE_ROWS)

    seen_paths = []
    original_chunks = pyreadstat.read_file_in_chunks

    def tracked_chunks(reader, source, *args, **kwargs):
        seen_paths.append(Path(source))
        return original_chunks(reader, source, *args, **kwargs)

    monkeypatch.setattr(pyreadstat, "read_file_in_chunks", tracked_chunks)
    observed_cells = _cell_signature(incidence.iter_cells(4))
    assert seen_paths == [snapshot_path]
    assert snapshot_path != path
    assert observed_cells == baseline_cells
    incidence.close()


def test_independent_snapshot_bound_c11_i03_facts_survive_original_path_replacement(tmp_path):
    for source_format in ("sav", "dta"):
        path = _write_source(tmp_path / f"indep-positive.{source_format}", source_format)
        expected_sha = _sha(path)
        incidence = _decode(path, source_format, expected_sha)
        try:
            baseline = _facts_from_incidence(incidence, source_format)
            assert baseline["source_sha256"] == expected_sha
            assert baseline["snapshot_sha256"] == expected_sha
            assert baseline["i03_typed_state"] == "SUPPORTED"
            assert baseline["i03_raw_denominator_support"] == 2
            assert baseline["i03_raw_numerator_support"] == 2
            assert baseline["i03_y_cells"] == {"0": 1, "1": 1}

            _write_source(path, source_format, _ALTERNATE_ROWS)
            assert _sha(path) != expected_sha
            observed = _facts_from_incidence(incidence, source_format)
            assert observed == baseline
            assert incidence.verify_source_identity() == expected_sha
        finally:
            incidence.close()


def test_private_snapshot_path_replacement_after_verify_cannot_rebind_old_identity_to_new_bytes(
    tmp_path, monkeypatch
):
    for source_format in ("sav", "dta"):
        path = _write_source(tmp_path / f"indep-toctou.{source_format}", source_format)
        alternate = _write_source(
            tmp_path / f"indep-toctou-alt.{source_format}", source_format, _ALTERNATE_ROWS
        )
        expected_sha = _sha(path)
        incidence = _decode(path, source_format, expected_sha)
        snapshot = incidence._source_snapshot
        snapshot_path = snapshot.path
        try:
            baseline = _facts_from_incidence(incidence, source_format)
            assert baseline["source_sha256"] == expected_sha
            assert baseline["i03_y_cells"] == {"0": 1, "1": 1}
            assert not snapshot_path.exists()
            assert Path(snapshot.reader_path).as_posix().startswith("/dev/fd/")
            with monkeypatch.context() as patch:
                calls = {"n": 0}

                def replace_once():
                    if calls["n"] == 0:
                        os.replace(alternate, snapshot_path)
                    calls["n"] += 1

                if source_format == "sav":
                    original_chunks = pyreadstat.read_file_in_chunks

                    def hostile_chunks(reader, source, *args, **kwargs):
                        replace_once()
                        return original_chunks(reader, source, *args, **kwargs)

                    patch.setattr(pyreadstat, "read_file_in_chunks", hostile_chunks)
                else:
                    original_read = pyreadstat.read_dta

                    def hostile_read(source, *args, **kwargs):
                        if not kwargs.get("metadataonly", False):
                            replace_once()
                        return original_read(source, *args, **kwargs)

                    patch.setattr(pyreadstat, "read_dta", hostile_read)
                observed = _facts_from_incidence(incidence, source_format)
            assert observed["source_sha256"] == expected_sha
            assert observed == baseline
            assert snapshot_path.exists()
        finally:
            incidence.close()
            try:
                snapshot_path.unlink()
            except OSError:
                pass
            try:
                snapshot.directory.rmdir()
            except OSError:
                pass


@pytest.mark.parametrize("source_format", ("sav", "dta"))
def test_metadata_phase_reads_bound_fd_not_replaced_private_path(
    tmp_path, source_format, monkeypatch
):
    path = _write_source(tmp_path / f"indep-metadata.{source_format}", source_format)
    metadata_rows = dict(_ROWS)
    metadata_rows["Z"] = metadata_rows.pop("W")
    alternate = _write_source(
        tmp_path / f"indep-metadata-alt.{source_format}", source_format, metadata_rows
    )
    expected_sha = _sha(path)

    import rawlsing_next.pre553_physical_decoder as decoder

    original_acquire = decoder._acquire_source_snapshot

    def acquire_then_replace(source, expected_source_sha256=None):
        snapshot = original_acquire(source, expected_source_sha256)
        os.replace(alternate, snapshot.path)
        return snapshot

    monkeypatch.setattr(decoder, "_acquire_source_snapshot", acquire_then_replace)
    incidence = _decode(path, source_format, expected_sha)
    snapshot = incidence._source_snapshot
    try:
        assert [variable.name for variable in incidence.variables] == list(_ROWS)
        assert incidence.source_sha256 == expected_sha
        facts = _facts_from_incidence(incidence, source_format)
        assert facts["source_sha256"] == expected_sha
        assert facts["snapshot_sha256"] == expected_sha
        assert facts["i03_y_cells"] == {"0": 1, "1": 1}
    finally:
        incidence.close()
        try:
            snapshot.path.unlink()
        except OSError:
            pass
        try:
            snapshot.directory.rmdir()
        except OSError:
            pass


def test_between_lazy_batch_writable_fd_capability_is_denied_and_facts_unchanged(
    tmp_path, monkeypatch
):
    path = _write_source(tmp_path / "indep-between-batch.sav", "sav")
    alternate = _write_source(tmp_path / "indep-between-batch-alt.sav", "sav", _ALTERNATE_ROWS)
    expected_sha = _sha(path)
    baseline = _decode(path, "sav", expected_sha)
    baseline_cells = _cell_signature(baseline.iter_cells(4))
    baseline.close()

    incidence = _decode(path, "sav", expected_sha)
    snapshot = incidence._source_snapshot
    alternate_bytes = alternate.read_bytes()
    original_chunks = pyreadstat.read_file_in_chunks

    def hostile_chunks(reader, source, *args, **kwargs):
        iterator = original_chunks(reader, source, *args, **kwargs)
        first = next(iterator)
        with pytest.raises(OSError):
            os.pwrite(snapshot.fd, alternate_bytes, 0)
        with pytest.raises(OSError):
            os.ftruncate(snapshot.fd, len(alternate_bytes))
        yield first
        yield from iterator

    monkeypatch.setattr(pyreadstat, "read_file_in_chunks", hostile_chunks)
    assert _cell_signature(incidence.iter_cells(4)) == baseline_cells
    incidence.close()


def test_dta_writable_fd_capability_is_denied_and_facts_unchanged(tmp_path, monkeypatch):
    path = _write_source(tmp_path / "indep-dta-window.dta", "dta")
    alternate = _write_source(tmp_path / "indep-dta-window-alt.dta", "dta", _ALTERNATE_ROWS)
    expected_sha = _sha(path)
    incidence = _decode(path, "dta", expected_sha)
    snapshot = incidence._source_snapshot
    alternate_bytes = alternate.read_bytes()
    baseline = _facts_from_incidence(incidence, "dta")
    original_read = pyreadstat.read_dta

    def hostile_read(source, *args, **kwargs):
        if not kwargs.get("metadataonly", False):
            with pytest.raises(OSError):
                os.pwrite(snapshot.fd, alternate_bytes, 0)
            with pytest.raises(OSError):
                os.ftruncate(snapshot.fd, len(alternate_bytes))
        return original_read(source, *args, **kwargs)

    monkeypatch.setattr(pyreadstat, "read_dta", hostile_read)
    assert _facts_from_incidence(incidence, "dta") == baseline
    incidence.close()


@pytest.mark.parametrize("source_format", ("sav", "dta"))
def test_compatibility_full_read_uses_bound_fd(tmp_path, source_format, monkeypatch):
    import rawlsing_next.pre553_physical_decoder as decoder

    path = _write_source(tmp_path / f"indep-compat.{source_format}", source_format)
    expected_sha = _sha(path)
    monkeypatch.setitem(decoder.COMPATIBILITY_ALLOWLIST, expected_sha, "latin1")
    decode = decoder.decode_sav if source_format == "sav" else decoder.decode_dta
    incidence = decode(path, encoding="latin1", expected_source_sha256=expected_sha)
    try:
        assert incidence.reader_configuration["authority_status"] == decoder.COMPATIBILITY_ONLY
        facts = _facts_from_incidence(incidence, source_format)
        assert facts["source_sha256"] == expected_sha
        assert facts["snapshot_sha256"] == expected_sha
        assert facts["i03_y_cells"] == {"0": 1, "1": 1}
    finally:
        incidence.close()


def test_r2_mmap_between_batch_change_cannot_release_altered_c11_i03_under_old_identity(
    tmp_path, monkeypatch
):
    path = _write_source(tmp_path / "r2-mmap.sav", "sav")
    alternate = _write_source(tmp_path / "r2-mmap-alt.sav", "sav", _ALTERNATE_ROWS)
    expected_sha = _sha(path)
    baseline = _observe(path, "sav", expected_sha)
    assert baseline["ok"] is True
    baseline_facts = baseline["facts"]
    assert baseline_facts["i03_y_cells"] == {"0": 1, "1": 1}

    incidence = _decode(path, "sav", expected_sha)
    snapshot = incidence._source_snapshot
    alternate_bytes = alternate.read_bytes()
    original_chunks = pyreadstat.read_file_in_chunks

    def hostile_chunks(reader, source, *args, **kwargs):
        iterator = original_chunks(reader, source, *args, **kwargs)
        first = next(iterator)
        with pytest.raises(OSError):
            mmap.mmap(snapshot.fd, 0, access=mmap.ACCESS_WRITE)
        with pytest.raises(OSError):
            os.pwrite(snapshot.fd, alternate_bytes, 0)
        yield first
        yield from iterator

    monkeypatch.setattr(pyreadstat, "read_file_in_chunks", hostile_chunks)
    observed = _facts_from_incidence(incidence, "sav")
    assert observed["source_sha256"] == expected_sha
    assert observed["snapshot_sha256"] == expected_sha
    assert observed == baseline_facts
    assert snapshot.access_mode == "O_RDONLY"
    incidence.close()


def test_posix_dev_fd_unavailable_is_typed_refusal(tmp_path, monkeypatch):
    import types
    import rawlsing_next.pre553_physical_decoder as decoder

    path = _write_source(tmp_path / "no-dev-fd.sav", "sav")
    real_path = decoder.Path

    def fake_path(value):
        if str(value) == "/dev/fd":
            return types.SimpleNamespace(is_dir=lambda: False)
        return real_path(value)

    monkeypatch.setattr(decoder, "Path", fake_path)
    with pytest.raises(DecoderError, match="POSIX /dev/fd"):
        decoder.decode_sav(path)
