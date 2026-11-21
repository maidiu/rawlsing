"""PRE-FF C0/C1: one physical read, source-independent mapping, cold recovery.

Tests are sourcefree SAV/DTA or synthetic physical carrier only. They do not
authorize original-source retention or issue scientific interpretation.
"""
from copy import deepcopy
from pathlib import Path

import pytest

from rawlsing_next.pre553_physical_cell_journal import (
    PhysicalCellJournal, PhysicalCellJournalError,
    PhysicalCellJournalReceipt, read_physical_cells,
    reproject_sourcefree_c11_from_physical_journal,
)
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState
from rawlsing_next.pre553_r157_projection_adapter import (
    SourceConfig, build_governed_c11_projection,
)
from rawlsing_next.tests.test_pyat960_s1e_support import (
    RecordingBodySink, build, source_fixture,
)


@pytest.mark.parametrize("source_format", ("SAV", "DTA"))
def test_one_source_read_retains_every_cell_and_reprojects_new_mapping_cold(
    tmp_path, source_format,
):
    root = tmp_path / source_format
    root.mkdir()
    fixture = source_fixture(
        root / "source", source_format=source_format,
        values=(0.0, 1.0, 2.0, 0.0, 1.0),
    )
    # Construct first semantic estate under mapping A which cannot interpret
    # the observed code 2.0. All physical cells are retained independently.
    a = deepcopy(fixture["document"])
    a["response_slots"][0]["values"] = [
        rule for rule in a["response_slots"][0]["values"]
        if rule["raw_value"] != 2.0
    ]
    private = root / "physical-private"
    private.mkdir(mode=0o700)
    journal = PhysicalCellJournal(private)
    first = build(
        root, fixture, name="mapping-a.sqlite",
        config=SourceConfig(a), physical_journal=journal,
    )
    receipt = first.physical_cell_journal
    assert type(receipt) is PhysicalCellJournalReceipt
    assert receipt.source_sha256 == fixture["source_sha"]
    assert receipt.cell_count == fixture["rows"] * len(receipt.variables)
    assert set(receipt.variables) == {(1, "q101"), (2, "country")}

    cold = list(read_physical_cells(receipt, authorized_private_root=private))
    assert len(cold) == receipt.cell_count
    assert sum(c.variable_name == "q101" and c.raw_value == 2.0
               and c.missing_state == PhysicalMissingState.OBSERVED_STORAGE_VALUE
               for c in cold) == 1
    assert sum(c.variable_name == "country" for c in cold) == fixture["rows"]

    # Eliminate the source path. Mapping B must work from the single retained
    # physical estate without any disguised SAV/DTA reread.
    vanished = fixture["path"].with_name("not-the-original-source-anymore")
    fixture["path"].rename(vanished)
    b_projection = build_governed_c11_projection(
        fixture["config"], source_sha256=fixture["source_sha"],
        row_count=fixture["rows"],
    )
    b = reproject_sourcefree_c11_from_physical_journal(
        receipt, authorized_private_root=private, projection=b_projection,
    )
    events = [obj for obj in b.public_objects if type(obj).__name__ == "RespondentEvent"]
    assert len(events) == fixture["rows"]
    assert all(obj.typed_state != "INVALID_UNRESOLVED" for obj in events)
    assert b.source_artifact_ref.content_hash == fixture["source_sha"]


@pytest.mark.parametrize("source_format", ("SAV", "DTA"))
def test_physical_journal_refuses_corruption_before_yielding_first_cell(
    tmp_path, source_format,
):
    fixture = source_fixture(
        tmp_path / "source", source_format=source_format,
        values=(0.0, 1.0, 2.0),
    )
    private = tmp_path / "private"
    private.mkdir(mode=0o700)
    handoff = build(
        tmp_path, fixture,
        physical_journal=PhysicalCellJournal(private),
    )
    receipt = handoff.physical_cell_journal
    body = Path(receipt.path) / "physical_cells.jsonl.gz"
    original = body.read_bytes()
    body.write_bytes(original[:-7] + b"CORRUPT")
    with pytest.raises(PhysicalCellJournalError, match="compressed hash"):
        # Must fail before returning even the first apparently-valid value.
        next(read_physical_cells(receipt, authorized_private_root=private))


def test_source_i02_failure_rolls_back_its_own_physical_journal(tmp_path):
    fixture = source_fixture(
        tmp_path / "source", source_format="SAV",
        values=(0.0, 1.0, 2.0),
    )
    private = tmp_path / "private"
    private.mkdir(mode=0o700)
    sink = RecordingBodySink(fail_at="finish")
    journal = PhysicalCellJournal(private)
    with pytest.raises(RuntimeError, match="test sink finish failure"):
        build(
            tmp_path, fixture, name="failure.sqlite",
            physical_journal=journal, body_sink=sink,
        )
    assert journal.state == "aborted"
    assert not list(private.glob(".preff-physical-stage-*"))
    releases = private / "releases"
    assert not releases.exists() or not list(releases.iterdir())
    assert not (tmp_path / "failure.sqlite").exists()


def test_physical_companion_recovers_wholly_unmapped_variable_without_occurrence_guess(
    tmp_path,
):
    import pandas as pd
    import pyreadstat
    from hashlib import sha256
    from rawlsing_next.pre553_physical_decoder import decode_sav

    source = tmp_path / "three-cols.sav"
    pyreadstat.write_sav(
        pd.DataFrame({
            "q101": [0.0, 1.0, 2.0],
            "country": [1.0, 1.0, 1.0],
            "unmapped": [42.0, 84.0, 42.0],
        }), str(source),
    )
    original_sha = sha256(source.read_bytes()).hexdigest()
    private = tmp_path / "private"
    private.mkdir(mode=0o700)
    journal = PhysicalCellJournal(private)
    with decode_sav(source, expected_source_sha256=original_sha) as incidence:
        journal.begin(incidence)
        for cell in incidence.iter_cells(batch_size=2):
            journal.accept(cell)
        receipt = journal.finish()
    source.unlink()
    recovered = list(read_physical_cells(
        receipt, authorized_private_root=private,
    ))
    assert receipt.cell_count == 9
    assert [cell.raw_value for cell in recovered
            if cell.variable_name == "unmapped"] == [42.0, 84.0, 42.0]
    assert all(cell.missing_state == PhysicalMissingState.OBSERVED_STORAGE_VALUE
               for cell in recovered if cell.variable_name == "unmapped")
    # No question id, occurrence index, response polarity or mapping
    # has been invented for these three source-native cells.


def test_cold_read_pins_verified_bytes_against_postverification_replacement(
    tmp_path, monkeypatch,
):
    """The published gzip may change just after preverification: never emit it."""
    import gzip
    import rawlsing_next.pre553_physical_cell_journal as custody
    fixture = source_fixture(
        tmp_path / "source", source_format="SAV",
        values=(0.0, 1.0, 2.0),
    )
    private = tmp_path / "private"
    private.mkdir(mode=0o700)
    receipt = build(
        tmp_path, fixture, physical_journal=PhysicalCellJournal(private),
    ).physical_cell_journal
    physical = Path(receipt.path) / "physical_cells.jsonl.gz"
    untouched = physical.read_bytes()
    ctor = gzip.GzipFile
    calls = {"n": 0}

    def concurrent_mutation(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 2:
            # Simulate a same-user mutation precisely between verification
            # and the beginning of replay. This is NOT an integrity grant.
            physical.write_bytes(b"REPLACED_AFTER_VERIFICATION")
        return ctor(*args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(custody.gzip, "GzipFile", concurrent_mutation)
        recovered = list(read_physical_cells(
            receipt, authorized_private_root=private,
        ))
    assert calls["n"] == 2
    assert len(recovered) == receipt.cell_count
    assert [x.variable_name for x in recovered[:2]] == ["q101", "country"]
    assert physical.read_bytes() != untouched


def test_cold_read_rejects_symlinked_intermediate_release_directory(tmp_path):
    fixture = source_fixture(
        tmp_path / "source", source_format="DTA", values=(0.0, 1.0),
    )
    private = tmp_path / "private"
    private.mkdir(mode=0o700)
    receipt = build(
        tmp_path, fixture, physical_journal=PhysicalCellJournal(private),
    ).physical_cell_journal
    releases = private / "releases"
    relocated = tmp_path / "external-releases"
    releases.rename(relocated)
    releases.symlink_to(relocated, target_is_directory=True)
    with pytest.raises(PhysicalCellJournalError, match="linked"):
        list(read_physical_cells(receipt, authorized_private_root=private))


def test_v2_physical_dictionary_roundtrip_and_corrupt_refusal(tmp_path):
    import hashlib
    import json
    fixture = source_fixture(
        tmp_path / "source-dictionary", source_format="SAV",
        values=(0.0, 1.0, 2.0),
    )
    private = tmp_path / "private-dictionary"
    private.mkdir(mode=0o700)
    receipt = build(
        tmp_path, fixture,
        physical_journal=PhysicalCellJournal(private),
    ).physical_cell_journal
    assert receipt.full_physical_metadata_retained
    metadata = Path(receipt.path) / "physical_metadata.json"
    data = metadata.read_bytes()
    assert hashlib.sha256(data).hexdigest() == receipt.source_metadata_digest
    document = json.loads(data.decode("utf-8"))
    assert document["source_sha256"] == receipt.source_sha256
    assert tuple((x["ordinal"], x["name"]) for x in document["variables"]) == receipt.variables
    assert len(list(read_physical_cells(
        receipt, authorized_private_root=private,
    ))) == receipt.cell_count
    metadata.write_bytes(b"FORGED")
    with pytest.raises(PhysicalCellJournalError, match="dictionary"):
        next(read_physical_cells(receipt, authorized_private_root=private))


def test_v2_dictionary_symlink_refused_before_any_observation(tmp_path):
    fixture = source_fixture(
        tmp_path / "symlink-source", source_format="DTA", values=(0.0, 1.0),
    )
    private = tmp_path / "private-symlink"
    private.mkdir(mode=0o700)
    receipt = build(
        tmp_path, fixture,
        physical_journal=PhysicalCellJournal(private),
    ).physical_cell_journal
    metadata = Path(receipt.path) / "physical_metadata.json"
    alternative = tmp_path / "metadata-alternative"
    metadata.rename(alternative)
    metadata.symlink_to(alternative)
    with pytest.raises((PhysicalCellJournalError, OSError), match="dictionary|linked|regular|symbolic"):
        next(read_physical_cells(receipt, authorized_private_root=private))
