"""Independent #1006 fixture/oracle/hostile tests.

These tests use only synthetic sourcefree objects through accepted S2-C/S2-D
interfaces.  They do not establish original35, production CURRENT or #1001.
"""
from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
from types import MappingProxyType

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next._pre553_direct_i02_sourcefree import SourcefreeDirectI02Sections
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError,
    VerifiedDirectEstate,
    _key,
    write_direct_estate,
)

from fixture_1006 import ShapeSpec, build_context
from query_1006 import build_query_bundle, execute_bundle_oracle

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def _write(tmp_path: Path, shape: ShapeSpec, *, chunk_rows: int = 16):
    root = tmp_path / shape.name
    root.mkdir(parents=True, mode=0o700)
    ctx = build_context(shape)
    bundle = build_query_bundle(ctx)
    receipt = write_direct_estate(
        ctx.direct_sections(), ctx.universe.ref, root, chunk_rows=chunk_rows,
    )
    return root, ctx, bundle, receipt


def _open_with(root: Path, receipt, bundle, *, authorizer=lambda _roots: True):
    return SavedC11Admission.open(
        root=root,
        exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        release_ref=receipt.reconstructed_v1_release_ref,
        runtime_catalog=bundle.catalog,
        current_authorizer=authorizer,
    )


def _facts_equal(left, right):
    assert tuple(f.ref for f in left.facts) == tuple(f.ref for f in right.facts)
    assert tuple(
        canonical_json(f.semantic_projection()) for f in left.facts
    ) == tuple(canonical_json(f.semantic_projection()) for f in right.facts)


def test_small_oracle_full_family_fact_and_replay_parity(tmp_path):
    shape = ShapeSpec("oracle", 48, include_weights=True, tag="PYAT1006-ORACLE")
    root, ctx, bundle, receipt = _write(tmp_path, shape)
    assert len(receipt.family_counts) == 13
    declared = dict(ctx.manifest.declared_record_counts_by_logical_family)
    declared.pop("ReplayManifest", None)
    assert dict(receipt.family_counts) == declared
    native_repo, native_release = ctx.native_oracle()
    oracle = execute_bundle_oracle(
        native_repo, native_release, bundle,
        qa=bundle.catalog.authorities[-2],
        dauth=bundle.catalog.authorities[-1],
    )
    admission = _open_with(root, receipt, bundle)
    for name in (
        "selected", "f2_forward", "f2_reverse", "f4_three", "f4_four",
        "weighted", "repeated",
    ):
        query, predicate = bundle.by_name(name)
        saved = admission.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
        _facts_equal(saved, oracle[name])
        assert saved.release_refs == oracle[name].release_refs
    saved_i05 = admission.execute_i05(
        discovery_authority_ref=bundle.discovery_authority.ref,
    )
    assert tuple(r.ref for r in saved_i05.receipts) == tuple(
        r.ref for r in oracle["i05"].receipts
    )
    assert tuple(f.ref for f in saved_i05.empirical_facts) == tuple(
        f.ref for f in oracle["i05"].empirical_facts
    )
    for family, count in receipt.family_counts.items():
        assert len(tuple(admission._estate.iter_family(family))) == count
    events = tuple(admission._estate.iter_family("RespondentEvent"))
    repeated = [
        event for event in events
        if _key(event.native_question_ref) == ctx.qrefs["MR"].key
    ]
    assert repeated
    for event in repeated:
        assert event.multiplicity_order_rank_fields["kind"] == "REPEATED_EVENT"
        assert "multiplicity_index" in event.multiplicity_order_rank_fields
    assert any(event.typed_state == "MISSING" for event in events)
    routing = tuple(admission._estate.iter_family("RoutingEligibilityFact"))
    assert any(fact.typed_state == "NOT_ELIGIBLE" for fact in routing)
    assert not list(Path(receipt.path).glob("*.sqlite"))
    assert not list(Path(receipt.path).glob("*.pkl"))


def test_changed_value_changes_fact_and_exact_restore(tmp_path):
    original = ShapeSpec(
        "restore-original", 64, include_weights=True, tag="PYAT1006-RESTORE",
    )
    changed = replace(
        original, name="restore-changed", mutate_respondent=3,
        mutate_question="C",
    )
    root_a, ctx_a, bundle_a, receipt_a = _write(tmp_path, original)
    root_b, ctx_b, bundle_b, receipt_b = _write(tmp_path, changed)
    assert receipt_a.reconstructed_v1_release_ref != (
        receipt_b.reconstructed_v1_release_ref
    )
    admission_a = _open_with(root_a, receipt_a, bundle_a)
    admission_b = _open_with(root_b, receipt_b, bundle_b)
    query = bundle_a.selected
    predicate = bundle_a.selected_predicate
    first = admission_a.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
    second = admission_b.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
    assert first.facts[0].ref != second.facts[0].ref
    native_b, release_b = ctx_b.native_oracle()
    oracle_b = execute_bundle_oracle(
        native_b, release_b, bundle_b,
        qa=bundle_b.catalog.authorities[-2],
        dauth=bundle_b.catalog.authorities[-1],
    )
    _facts_equal(second, oracle_b["selected"])
    restored = admission_a.execute_i03(
        query_ref=query.ref, predicate_ref=predicate.ref,
    )
    assert restored.facts[0].ref == first.facts[0].ref
    assert canonical_json(restored.facts[0].semantic_projection()) == canonical_json(
        first.facts[0].semantic_projection()
    )


def test_false_empty_tamper_denied_current_and_wrong_root_refuse(tmp_path):
    shape = ShapeSpec("hostile", 32, include_weights=False, tag="PYAT1006-HOSTILE")
    root, ctx, bundle, receipt = _write(tmp_path, shape)
    admission = _open_with(root, receipt, bundle)
    assert admission.execute_i03(
        query_ref=bundle.selected.ref,
        predicate_ref=bundle.selected_predicate.ref,
    ).facts

    with pytest.raises(Exception):
        SavedC11Admission.open(
            root=root, exact_path=receipt.path,
            independently_held_manifest_sha256=receipt.manifest_sha256,
            independently_held_i02=receipt.i02,
            release_ref=receipt.reconstructed_v1_release_ref,
            runtime_catalog=bundle.catalog,
            current_authorizer=lambda _roots: False,
        )
    wrong = replace(receipt.i02, source="SOURCE_ARTIFACT:forged:0")
    with pytest.raises(Exception):
        SavedC11Admission.open(
            root=root, exact_path=receipt.path,
            independently_held_manifest_sha256=receipt.manifest_sha256,
            independently_held_i02=wrong,
            release_ref=receipt.reconstructed_v1_release_ref,
            runtime_catalog=bundle.catalog,
            current_authorizer=lambda _roots: True,
        )

    missing_root, missing_ctx, missing_bundle, missing_receipt = _write(
        tmp_path / "missing", replace(shape, name="missing", tag="PYAT1006-MISSING"),
    )
    (Path(missing_receipt.path) / "event_locator.parquet").unlink()
    with pytest.raises(DirectEstateError):
        VerifiedDirectEstate(
            missing_root, exact_path=missing_receipt.path,
            independently_held_manifest_sha256=missing_receipt.manifest_sha256,
            independently_held_i02=missing_receipt.i02,
            current_authorizer=lambda _roots: True,
        )

    tamper_root, tamper_ctx, tamper_bundle, tamper_receipt = _write(
        tmp_path / "tamper", replace(shape, name="tamper", tag="PYAT1006-TAMPER"),
    )
    import pyarrow as pa
    import pyarrow.parquet as pq
    body_path = Path(tamper_receipt.path) / "RespondentEvent.parquet"
    table = pq.read_table(body_path)
    rows = table.to_pylist()
    rows[0]["body_json"] = rows[1]["body_json"]
    pq.write_table(
        pa.Table.from_pylist(rows, schema=table.schema), body_path,
        compression="zstd", row_group_size=8,
    )
    manifest_path = Path(tamper_receipt.path) / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["members"]["RespondentEvent.parquet"] = hashlib.sha256(
        body_path.read_bytes()
    ).hexdigest()
    manifest_path.write_text(canonical_json(manifest) + "\n", encoding="utf-8")
    held = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    with pytest.raises(Exception):
        cold = VerifiedDirectEstate(
            tamper_root, exact_path=tamper_receipt.path,
            independently_held_manifest_sha256=held,
            independently_held_i02=tamper_receipt.i02,
            current_authorizer=lambda _roots: True,
        )
        tuple(cold.iter_family("RespondentEvent"))


def test_no_full_graph_no_whole_table_no_source_open_on_saved_path(tmp_path, monkeypatch):
    shape = ShapeSpec("nofallback", 24, include_weights=True, tag="PYAT1006-NOFALLBACK")
    root, ctx, bundle, receipt = _write(tmp_path, shape)
    admission = _open_with(root, receipt, bundle)
    opens: list[str] = []

    def audit(event, args):
        if event == "open" and args:
            text = str(args[0]).lower()
            if text.endswith((".sav", ".dta", ".csv", ".rda", ".rds")):
                opens.append(str(args[0]))

    sys.addaudithook(audit)

    import pyarrow.parquet as pq
    original_read_table = pq.read_table
    original_init = C11Repository.__init__

    def forbidden(*_args, **_kwargs):
        raise AssertionError("full C11 graph or whole-table fallback")

    try:
        monkeypatch.setattr(C11Repository, "__init__", forbidden)
        monkeypatch.setattr(pq, "read_table", forbidden)
        for name in ("selected", "f2_forward", "f2_reverse", "f4_three", "f4_four"):
            query, predicate = bundle.by_name(name)
            assert admission.execute_i03(
                query_ref=query.ref, predicate_ref=predicate.ref,
            ).facts
        assert admission.execute_i05(
            discovery_authority_ref=bundle.discovery_authority.ref,
        ).receipts
    finally:
        monkeypatch.setattr(C11Repository, "__init__", original_init)
        monkeypatch.setattr(pq, "read_table", original_read_table)
    assert opens == []
    members = sorted(path.name for path in Path(receipt.path).iterdir())
    assert members == sorted([
        "manifest.json",
        *[family + ".parquet" for family in receipt.family_counts],
        "event_locator.parquet",
    ])


def test_high_cardinality_skew_occurrence_is_not_collapsed(tmp_path):
    shape = ShapeSpec(
        "skew", 100, include_weights=True, skew_events=600,
        tag="PYAT1006-SKEW",
    )
    root, ctx, bundle, receipt = _write(tmp_path, shape, chunk_rows=32)
    assert receipt.family_counts["RespondentEvent"] == ctx.shape.event_count
    cold = VerifiedDirectEstate(
        root, exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        current_authorizer=lambda _roots: True,
    )
    respondent = next(iter(cold.iter_family("RespondentIdentity")))
    events = [
        event for event in cold.iter_family("RespondentEvent")
        if _key(event.native_question_ref) == ctx.qrefs["MR"].key
        and _key(event.scoped_respondent_ref) == respondent.ref.key
    ]
    assert len(events) == 602
    keys = {(event.event_group_id, event.response_event_id_or_deterministic_index)
            for event in events}
    assert len(keys) == len(events)
    admission = _open_with(root, receipt, bundle)
    assert admission.execute_i03(
        query_ref=bundle.selected.ref,
        predicate_ref=bundle.selected_predicate.ref,
    ).facts[0].typed_state == "SUPPORTED"


def test_crash_before_commit_has_no_manifest_and_restart_succeeds(tmp_path):
    shape = ShapeSpec("crash", 120, include_weights=True, tag="PYAT1006-CRASH")
    root = tmp_path / "crash-root"
    root.mkdir(mode=0o700)
    child = r"""
import sys
from pathlib import Path
from types import MappingProxyType
import time
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2])
from fixture_1006 import ShapeSpec, build_context
from rawlsing_next._pre553_direct_i02_sourcefree import SourcefreeDirectI02Sections
from rawlsing_next.pre553_source_direct_parquet_estate import write_direct_estate
class Slow:
    def __init__(self, stream):
        self.stream = stream
    def __iter__(self):
        for value in self.stream:
            time.sleep(0.02)
            yield value
ctx = build_context(ShapeSpec('crash', 120, include_weights=True, tag='PYAT1006-CRASH'))
source = ctx.direct_sections()
wrapped = SourcefreeDirectI02Sections(
    manifest=source.manifest,
    sections=MappingProxyType({family: Slow(stream) for family, stream in source.sections.items()}),
    typed_absences=source.typed_absences,
    replay_protocol_authority_ref=source.replay_protocol_authority_ref,
    replay_protocol_version=source.replay_protocol_version,
    deterministic_tie_order_rules_ref=source.deterministic_tie_order_rules_ref,
)
write_direct_estate(wrapped, ctx.universe.ref, Path(sys.argv[3]), chunk_rows=16)
"""
    process = subprocess.Popen(
        [sys.executable, "-c", child, str(REPO), str(HERE), str(root)],
        cwd=str(REPO), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    time.sleep(0.7)
    process.send_signal(signal.SIGKILL)
    process.wait(timeout=10)
    committed = list((root / "releases").glob("*/manifest.json")) if (root / "releases").exists() else []
    assert committed == []
    shutil.rmtree(root)
    root.mkdir(mode=0o700)
    ctx = build_context(shape)
    receipt = write_direct_estate(ctx.direct_sections(), ctx.universe.ref, root, chunk_rows=16)
    assert Path(receipt.path, "manifest.json").is_file()
