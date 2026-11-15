"""R3 Q2 3-question fixture -> compiler plan -> issued Batch query/F4/resume.

Return-local TEST_ONLY harness. No product/test/issuer edit. The source fixture
is generated nonrespondent SAV bytes; the compiler and saved APIs are the frozen
candidate implementations.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
from collections.abc import Mapping
from dataclasses import asdict, replace
from pathlib import Path
import resource
import sys
import time

import pandas as pd
import pyreadstat

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, BatchManifest, BatchUnitSpec,
)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import exact_ref, semantic_hash
from rawlsing_next.pre553_issued_workload import (
    IssuedWorkloadRecord, NativeWorkload, capture_joined_checkpoint,
    execute_issued_workload, operation_jobs, resume_joined_workloads,
)
from rawlsing_next.pre553_native_workload_binding import (
    TestOnlyDecisionResolver, TestOnlyIssuedWorkload,
)
from rawlsing_next.pre553_r157_projection_adapter import (
    SourceConfig, build_governed_c11_projection,
)
from rawlsing_next.pre553_saved_c11_admission import (
    SavedC11Admission, SavedC11AdmissionError, SavedReleaseIdentity,
)
from rawlsing_next.pre553_saved_workload_integration import (
    execute_saved_batch, execute_saved_i03, execute_saved_i05,
)
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES
from rawlsing_next.pre553_source_native_preimage_adapter import (
    AdministeredItem, NativePreimageBundle,
)
from rawlsing_next.pre553_source_postconsumer_receipts import (
    SourceReceiptJoinError, join_saved_source_operation_fates,
)
from rawlsing_next.pre553_source_saved_body_bridge import SourceSavedBodySink
from rawlsing_next.pre553_source_direct_parquet_estate import DirectEstateError
from rawlsing_next.pre553_universal_workload import compile_governed_frontier
from rawlsing_next.tests.test_pyat940_s1b_support import (
    make_config, ref, sha256_file,
)
from rawlsing_next.tests.test_pyat960_s1e_native_fact import (
    _NATIVE_HOST, _NATIVE_PURPOSE, _native_document,
)
from rawlsing_next.tests.test_pyat960_s1e_support import build
from rawlsing_next.tests.test_pyat_r3_s1c_source_operation_fates import _freeze_packet
from rawlsing_next.tests.test_universal_grammar import (
    _frontier, _inventory, _occurrence, _policy,
)

HOST = _NATIVE_HOST
PURPOSE = _NATIVE_PURPOSE
AS_OF = "2026-11-13"


def _source_rows(values):
    rows = []
    for q101, q102, q103, country in values:
        rows.append({
            "q101": float(q101), "country": float(country),
            "q102": float(q102), "q103": float(q103),
        })
    return rows


def _make_fixture(root: Path, values):
    root.mkdir(parents=True, exist_ok=True)
    source_dir = root / "source"
    source_dir.mkdir(parents=True, exist_ok=True)
    path = source_dir / "three-question.sav"
    rows = _source_rows(values)
    pyreadstat.write_sav(
        pd.DataFrame(rows), str(path),
        variable_value_labels={
            "q101": {1.0: "one"}, "q102": {1.0: "one"},
            "q103": {1.0: "one"},
        },
    )
    source_sha = sha256_file(path)
    document = make_config(
        source_format="SAV", active_source_sha256=source_sha,
        row_count=len(rows), values=tuple(r["q101"] for r in rows),
        keyed=False,
    )
    document["identity"].update({
        "source_column_count": 4, "original_item_count": 3,
        "codebook_rows": 4,
    })
    document["coverage"].update({"physical_slots_total": 4, "items_total": 3})
    q_template = document["questions"][0]
    physical_template = document["physical_slots"][0]
    item_template = document["items"][0]
    response_template = document["response_slots"][0]
    routing_template = document["routing"][0]
    for ordinal, name in ((3, "q102"), (4, "q103")):
        question = copy.deepcopy(q_template)
        question["question_id"] = name
        question["native_question_ref"] = ref(
            "QUESTION_NATIVE", "urn:rawlsing:s1b:question:" + name)
        document["questions"].append(question)
        physical = copy.deepcopy(physical_template)
        physical["ordinal"] = ordinal
        physical["name"] = name
        physical["label"] = name
        document["physical_slots"].append(physical)
        item = copy.deepcopy(item_template)
        item["implementation_id"] = "question_impl.s1b." + name
        item["source_variable_code"] = name
        item["exact_identity_sha256"] = hashlib.sha256(
            f"item:{name}".encode()).hexdigest()
        item["question_text"] = name
        document["items"].append(item)
        response = copy.deepcopy(response_template)
        response["slot"]["ordinal"] = ordinal
        response["slot"]["name"] = name
        response["question_id"] = name
        document["response_slots"].append(response)
        routing = copy.deepcopy(routing_template)
        routing["question_id"] = name
        document["routing"].append(routing)
    document = _native_document(document)
    config = SourceConfig(document)
    projection = build_governed_c11_projection(config)
    qrefs = {}
    for question in projection.questions:
        oid = question.native_question_ref.object_id
        for name in ("q101", "q102", "q103", "country"):
            if oid.endswith(":" + name):
                qrefs[name] = question.native_question_ref
    risk_ref = exact_ref(projection.routing[0].risk_set_ref)
    occurrences = tuple(
        _occurrence(name, domain=(0, 1), risk_set_refs=(risk_ref.key,))
        for name in ("q101", "q102", "q103", "country")
    )
    inventory = replace(
        _inventory(occurrences, complete=True),
        source_id=document["identity"]["source_id"],
        wave=document["identity"]["wave"],
        edition=document["identity"]["instrument_release_id"],
        source_sha256=source_sha,
        inventory_id="PYAT997-R3-THREE-QUESTION",
    )
    policy = _policy(j=3, k=2, d=1)
    frontier = _frontier(inventory, policy)
    census = _freeze_packet(frontier)
    return {
        "path": path, "source_sha": source_sha, "rows": len(rows),
        "document": document, "config": config, "projection": projection,
        "qrefs": qrefs, "inventory": inventory, "policy": policy,
        "frontier": frontier, "census": census,
    }


def _materialize(stage: Path, fixture):
    stage.mkdir(parents=True, exist_ok=True)
    private = stage / "private"
    private.mkdir(mode=0o700, exist_ok=True)
    sink = SourceSavedBodySink(
        certificate_path=stage / "estate.sqlite",
        authorized_private_root=private, chunk_rows=2,
    )
    handoff = build(
        stage, fixture, name="estate.sqlite",
        body_sink=sink, chunk_size=2,
    )
    estate = sink.receipt
    release = SavedReleaseIdentity(estate.reconstructed_v1_release_ref)
    projection = fixture["projection"]
    administered = tuple(
        AdministeredItem(
            "R3-" + name, name, "ADMINISTERED",
            "TEST_ONLY_Q2_THREE_QUESTION", "person", "OUTCOME",
        )
        for name in ("q101", "q102", "q103", "country")
    )
    bundle = NativePreimageBundle(
        schema="PYAT_R56_NATIVE_PREIMAGE_BUNDLE@1.0.0",
        source_sha256=handoff.source_sha256,
        package_hash=semantic_hash({"q2": handoff.source_sha256}),
        projection=projection,
        physical_stream=ExactPhysicalCellStream(
            handoff.source_sha256, handoff.row_count, lambda: ()),
        release=release,
        administered=administered,
        held=(), excluded=(), unknown=(),
        bundle_hash=semantic_hash({
            "q2_source": handoff.source_sha256,
            "release": estate.reconstructed_v1_release_ref.as_dict(),
        }),
        question_refs=dict(fixture["qrefs"]),
        risk_set_ref=exact_ref(projection.routing[0].risk_set_ref),
        respondent_rows=tuple(
            {"respondent_key": row.respondent_key, "ref": row.ref.key}
            for row in projection.respondents
        ),
        occurrence_bindings=(),
    )
    compilation = compile_governed_frontier(
        bundle=bundle, inventory=fixture["inventory"],
        policy=fixture["policy"], frontier=fixture["frontier"],
        as_of=AS_OF, host=HOST, purpose=PURPOSE,
    )
    catalog = compilation.runtime_catalog
    q101 = fixture["qrefs"]["q101"]
    q102 = fixture["qrefs"]["q102"]
    q103 = fixture["qrefs"]["q103"]
    joint_query = None
    for query in catalog.queries:
        targets = [exact_ref(target).object_id for target in query.target_refs]
        if targets == [q101.object_id, q102.object_id, q103.object_id]:
            joint_query = query
            break
    if joint_query is None:
        raise AssertionError("compiler did not expose q101/q102/q103 joint query")
    predicate = catalog.resolve_predicate_exact(joint_query.condition_predicate_ref)
    request = __import__(
        "rawlsing_next.pre553_route_b_production", fromlist=["I03ExecutionRequest"]
    ).I03ExecutionRequest(joint_query.ref, predicate.ref)
    discovery = catalog.discovery_authorities[0]
    base = compilation.issued.workload
    decision_ref = exact_ref(ref(
        "TEST_ONLY_DECISION", "urn:test:pyat997:r3:" + fixture["source_sha"][:16]))
    workload = NativeWorkload(
        decision_ref=decision_ref,
        source_factory_ref=base.source_factory_ref,
        descriptor=base.descriptor,
        projection=projection,
        catalog=catalog,
        requests=(request,),
        discoveries=(discovery.ref,),
        original_u_root=base.original_u_root,
        expected_frontier_root=base.expected_frontier_root,
    )
    record = IssuedWorkloadRecord(
        decision_ref=decision_ref,
        source_permission_ref=exact_ref(ref(
            "TEST_ONLY_SOURCE_PERMISSION", "urn:test:pyat997:r3:source")),
        scientific_permission_refs=(
            exact_ref(ref("TEST_ONLY_SCIENTIFIC_PERMISSION", "urn:test:pyat997:r3:science")),
        ),
        host=HOST, purpose=PURPOSE,
        source_sha256=workload.projection.expected_source_sha256,
        envelope_sha256=semantic_hash(workload.envelope()),
        original_u_root=workload.original_u_root,
        expected_frontier_root=workload.expected_frontier_root,
        expected_jobs=operation_jobs(workload.requests, workload.discoveries),
        currentness="CURRENT_GRANTED", scope="TEST_ONLY_SOURCEFREE",
        native_universe_refs=(projection.universes[0].ref,),
    )
    issued = TestOnlyIssuedWorkload(
        workload=workload, record=record,
        descriptor=json.loads(workload.descriptor.decode()),
        envelope_sha256=record.envelope_sha256,
    )
    compilation = replace(compilation, issued=issued)
    admission = SavedC11Admission.open(
        root=private, exact_path=estate.path,
        independently_held_manifest_sha256=estate.manifest_sha256,
        independently_held_i02=estate.i02,
        release_ref=estate.reconstructed_v1_release_ref,
        runtime_catalog=catalog,
        current_authorizer=lambda _roots: True,
    )
    resolver = TestOnlyDecisionResolver(record)
    return {
        "fixture": fixture, "handoff": handoff, "estate": estate,
        "compilation": compilation, "admission": admission,
        "resolver": resolver, "sink": sink, "joint_query": joint_query,
        "predicate": predicate, "request": request, "discovery": discovery,
        "issued": issued, "private": private,
    }


def _payload(result):
    facts = getattr(result, "facts", ())
    return {
        "facts": [fact.ref.as_dict() for fact in facts],
        "typed_states": [fact.typed_state for fact in facts],
        "receipts": [r.ref.as_dict() for r in getattr(result, "receipts", ())],
        "candidate_count": getattr(result, "candidate_count", None),
        "covered_candidate_count": getattr(result, "covered_candidate_count", None),
    }


def _run(stage: Path, fixture):
    bundle = _materialize(stage, fixture)
    query = bundle["joint_query"]
    predicate = bundle["predicate"]
    admission = bundle["admission"]
    resolver = bundle["resolver"]
    compilation = bundle["compilation"]
    issued = bundle["issued"]
    discovery = bundle["discovery"]

    i03 = execute_saved_i03(
        admission, query_ref=query.ref, predicate_ref=predicate.ref)
    if len(i03.facts) != 1 or i03.facts[0].typed_state != "SUPPORTED":
        raise AssertionError("joint issued query did not produce SUPPORTED fact")
    fact = i03.facts[0]
    topology = fact.target_topology
    cells = topology["complete_cell_semantic_projection"]
    if topology["arity"] != 3 or len(cells) != 8:
        raise AssertionError("F4 did not produce the exact 3-target 8-cell joint")
    if fact.raw_denominator_support != 5:
        raise AssertionError("F4 denominator is not the five generated respondents")
    if sum(int(cell["raw_numerator_support"]) for cell in cells) != 5:
        raise AssertionError("F4 cells do not conserve the joint denominator")

    i05 = execute_saved_i05(
        admission, discovery_authority_ref=discovery.ref)
    query_unit = BatchUnitSpec(
        "QUERY", query.ref,
        (admission.release_ref,), (issued.record.decision_ref,),
    )
    discovery_unit = BatchUnitSpec(
        "DISCOVERY", discovery.ref,
        (admission.release_ref,), (issued.record.decision_ref,),
    )
    manifest = BatchManifest((query_unit, discovery_unit))
    batch = execute_saved_batch(
        admission, manifest=manifest,
        predicate_ref_by_query={query.ref.key: predicate.ref},
    )
    if not all(r.state == "COMPLETED" for r in batch.receipts):
        raise AssertionError("issued Batch did not complete both units")
    joined = join_saved_source_operation_fates(
        handoff=bundle["handoff"], estate_receipt=bundle["estate"],
        admission=admission, compilation=compilation,
        workload=issued.workload, resolver=resolver,
        host=HOST, purpose=PURPOSE, runner=batch,
    )
    if joined.audit["positive_native_linked_operations"] <= 0:
        raise AssertionError("no positive native linked operation")

    normal = execute_issued_workload(
        issued.workload, resolver, saved_admission_factory=lambda: admission,
        source_factory=None, host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    partial = execute_issued_workload(
        issued.workload, resolver, saved_admission_factory=lambda: admission,
        source_factory=None, host=HOST, purpose=PURPOSE,
        allow_test_only=True, max_units=1,
    )
    partial_checkpoint = capture_joined_checkpoint(
        (partial,), saved_binding=admission.binding_receipt())
    resumed_partial = resume_joined_workloads(
        workloads=(issued,), resolver=resolver,
        saved_admission_factory=lambda: admission, source_factory=None,
        host=HOST, purpose=PURPOSE, checkpoint=partial_checkpoint,
        expected_checkpoint_ref=partial_checkpoint.checkpoint_hash,
        allow_test_only=True,
    )
    absent_checkpoint = capture_joined_checkpoint(
        (), saved_binding=admission.binding_receipt())
    resumed_absent = resume_joined_workloads(
        workloads=(issued,), resolver=resolver,
        saved_admission_factory=lambda: admission, source_factory=None,
        host=HOST, purpose=PURPOSE, checkpoint=absent_checkpoint,
        expected_checkpoint_ref=absent_checkpoint.checkpoint_hash,
        allow_test_only=True,
    )
    if not normal.receipts or not all(r.state == "COMPLETED" for r in normal.receipts):
        raise AssertionError("saved NORMAL did not complete")
    if not partial.receipts or any(r.state != "COMPLETED" for r in partial.receipts):
        raise AssertionError("partial prefix did not retain a completed unit")
    if not resumed_partial.resumed_results:
        raise AssertionError("partial resume did not return a resumed result")
    if not resumed_absent.resumed_results:
        raise AssertionError("absent resume did not start exact full prefix")
    full_refs = tuple(sorted(ref.key for ref in normal.output_refs))
    partial_refs = tuple(sorted(ref.key for ref in resumed_partial.output_refs))
    absent_refs = tuple(sorted(ref.key for ref in resumed_absent.output_refs))
    if partial_refs != full_refs or absent_refs != full_refs:
        raise AssertionError("resume output refs do not match the full saved run")
    return {
        "source_sha256": bundle["handoff"].source_sha256,
        "roots": bundle["estate"].i02.__dict__,
        "stats": bundle["handoff"].stats.__dict__,
        "family_counts": dict(bundle["estate"].family_counts),
        "i03": _payload(i03),
        "i05": _payload(i05),
        "batch": {
            "units": len(batch.receipts),
            "states": [r.state for r in batch.receipts],
            "result_refs": [
                ref.as_dict() for receipt in batch.receipts
                for ref in receipt.result_refs
            ],
        },
        "normal": {
            "units": len(normal.receipts),
            "states": [r.state for r in normal.receipts],
            "output_refs": full_refs,
        },
        "partial": {
            "prefix_units": len(partial.receipts),
            "resumed_completed": len(resumed_partial.completed_results),
            "resumed_prefix": len(resumed_partial.resumed_results),
            "output_refs": partial_refs,
        },
        "absent": {
            "resumed_completed": len(resumed_absent.completed_results),
            "resumed_prefix": len(resumed_absent.resumed_results),
            "output_refs": absent_refs,
        },
        "join": {
            "result_hash": joined.result_hash,
            "audit": dict(joined.audit),
            "rows": len(joined.rows),
            "positive_rows": sum(
                1 for row in joined.rows
                if str(row.get("postconsumer_state", "")).startswith(
                    "TEST_ONLY_SAVED_NATIVE")
            ),
        },
        "f4": {
            "query_ref": query.ref.as_dict(),
            "fact_ref": fact.ref.as_dict(),
            "typed_state": fact.typed_state,
            "denominator": fact.raw_denominator_support,
            "arity": topology["arity"],
            "cell_count": len(cells),
            "cells": [
                {
                    "cell": cell["cell"],
                    "raw_numerator_support": cell["raw_numerator_support"],
                    "cell_state": cell["cell_state"],
                }
                for cell in cells
            ],
        },
        "retained_bytes": bundle["estate"].retained_bytes,
        "stage_bytes": sum(
            p.stat().st_size for p in stage.rglob("*") if p.is_file()),
        "parent_maxrss": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "full_c11_builds": bundle["handoff"].stats.full_c11_builds,
        "source_reads": bundle["handoff"].stats.source_reads,
        "decode_calls": bundle["handoff"].stats.decode_calls,
        "cell_passes": bundle["handoff"].stats.cell_passes,
        "parquet_members": len(list(Path(bundle["estate"].path).glob("*.parquet"))),
    }


def _negative_witnesses(bundle) -> dict:
    handoff = bundle["handoff"]
    estate = bundle["estate"]
    private = bundle["private"]
    compilation = bundle["compilation"]
    admission = bundle["admission"]
    resolver = bundle["resolver"]
    issued = bundle["issued"]
    query = bundle["joint_query"]
    predicate = bundle["predicate"]
    discovery = bundle["discovery"]
    query_unit = BatchUnitSpec(
        "QUERY", query.ref, (admission.release_ref,),
        (issued.record.decision_ref,))
    discovery_unit = BatchUnitSpec(
        "DISCOVERY", discovery.ref, (admission.release_ref,),
        (issued.record.decision_ref,))
    manifest = BatchManifest((query_unit, discovery_unit))
    out = {}
    held = next(row for row in handoff.operation_fates
                if row["disposition"] == "HELD")
    altered = tuple(
        {**row, "disposition": "ELIGIBLE"}
        if row["operation_id"] == held["operation_id"] else row
        for row in handoff.operation_fates
    )
    forged = replace(handoff, operation_fates=altered)
    runner = BatchExecutionRunner(
        manifest=manifest, repository=admission, saved_mode=True)
    try:
        join_saved_source_operation_fates(
            handoff=forged, estate_receipt=estate, admission=admission,
            compilation=compilation, workload=issued.workload,
            resolver=resolver, host=HOST, purpose=PURPOSE, runner=runner)
    except SourceReceiptJoinError as exc:
        out["held_refusal"] = str(exc)
    else:
        raise AssertionError("forged HELD promotion was not refused")
    audit = dict(handoff.census_audit)
    audit["frontier_hash"] = "0" * 64
    forged = replace(handoff, census_audit=audit)
    try:
        join_saved_source_operation_fates(
            handoff=forged, estate_receipt=estate, admission=admission,
            compilation=compilation, workload=issued.workload,
            resolver=resolver, host=HOST, purpose=PURPOSE, runner=runner)
    except SourceReceiptJoinError as exc:
        out["frontier_refusal"] = str(exc)
    else:
        raise AssertionError("forged Q2 frontier was not refused")
    missing_runner = BatchExecutionRunner(
        manifest=manifest, repository=admission, saved_mode=True)
    joined = join_saved_source_operation_fates(
        handoff=handoff, estate_receipt=estate, admission=admission,
        compilation=compilation, workload=issued.workload,
        resolver=resolver, host=HOST, purpose=PURPOSE, runner=missing_runner)
    out["missing_receipts_no_positive"] = (
        joined.audit["positive_native_linked_operations"] == 0)
    wrong = replace(
        estate.i02, source="SOURCE_ARTIFACT|forged|" + "0" * 64)
    try:
        SavedC11Admission.open(
            root=private, exact_path=estate.path,
            independently_held_manifest_sha256=estate.manifest_sha256,
            independently_held_i02=wrong,
            release_ref=estate.reconstructed_v1_release_ref,
            runtime_catalog=compilation.runtime_catalog,
            current_authorizer=lambda _roots: True)
    except Exception as exc:
        out["wrong_root_refusal"] = type(exc).__name__
    else:
        raise AssertionError("wrong root was not refused")
    try:
        SavedC11Admission.open(
            root=private, exact_path=estate.path,
            independently_held_manifest_sha256=estate.manifest_sha256,
            independently_held_i02=estate.i02,
            release_ref=estate.reconstructed_v1_release_ref,
            runtime_catalog=compilation.runtime_catalog,
            current_authorizer=lambda _roots: False)
    except (SavedC11AdmissionError, DirectEstateError) as exc:
        out["revoked_refusal"] = type(exc).__name__ + ":" + str(exc)
    else:
        raise AssertionError("revoked current was not refused")
    return out


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    root.mkdir(parents=True, exist_ok=True)
    started = time.time()
    baseline_fixture = _make_fixture(
        root / "baseline-fixture",
        [(0, 0, 0, 1), (1, 1, 1, 1), (0, 1, 0, 2),
         (1, 0, 1, 3), (0, 0, 1, 4)],
    )
    baseline = _run(root / "baseline", baseline_fixture)
    changed_fixture = _make_fixture(
        root / "changed-fixture",
        [(0, 0, 0, 1), (1, 1, 0, 1), (0, 1, 0, 2),
         (1, 0, 1, 3), (0, 0, 1, 4)],
    )
    changed = _run(root / "changed", changed_fixture)
    restored = _run(root / "restored", baseline_fixture)
    negative_bundle = _materialize(root / "negative", baseline_fixture)
    negatives = _negative_witnesses(negative_bundle)
    if baseline["source_sha256"] == changed["source_sha256"]:
        raise AssertionError("changed source did not change")
    if baseline["roots"]["logical"] != restored["roots"]["logical"]:
        raise AssertionError("restored source logical root differs")
    if baseline["f4"]["fact_ref"] == changed["f4"]["fact_ref"]:
        raise AssertionError("changed response did not change F4 fact")
    if baseline["f4"]["fact_ref"] != restored["f4"]["fact_ref"]:
        raise AssertionError("restored F4 fact differs")
    if baseline["join"]["result_hash"] != restored["join"]["result_hash"]:
        raise AssertionError("restored fate join hash differs")
    out = {
        "schema": "PYAT997_R3_ISSUED_BATCH_F4_RESUME@1",
        "status": "PASS",
        "candidate": "2c476e739a263dd0069b54706c6cfa63b07190c1",
        "sourcefree": True,
        "fixture": "TEST_ONLY generated 4-column SAV; no original35",
        "baseline": baseline,
        "changed": changed,
        "restored": restored,
        "negatives": negatives,
        "change_restore": {
            "baseline_fact": baseline["f4"]["fact_ref"],
            "changed_fact": changed["f4"]["fact_ref"],
            "restored_fact": restored["f4"]["fact_ref"],
            "baseline_source": baseline["source_sha256"],
            "changed_source": changed["source_sha256"],
            "baseline_logical": baseline["roots"]["logical"],
            "restored_logical": restored["roots"]["logical"],
            "baseline_join": baseline["join"]["result_hash"],
            "restored_join": restored["join"]["result_hash"],
        },
        "issued_query_batch": {
            "query_units": 1,
            "discovery_units": 1,
            "query_ref": baseline["f4"]["query_ref"],
            "source_cell_changed": True,
        },
        "limits": [
            "Small TEST_ONLY five-respondent fixture, not original35.",
            "Compiler query catalog and existing TEST_ONLY record constructors used; no production issuer.",
            "F4 is the actual 3-target native I03 fact, not marginal multiplication.",
        ],
        "elapsed_seconds": time.time() - started,
    }
    path = root / "issued_batch_f4_resume.json"
    path.write_text(json.dumps(out, indent=2, default=str) + "\n")
    print(json.dumps({
        "status": "PASS",
        "proof": str(path),
        "baseline_f4": baseline["f4"],
        "changed_f4": {"fact_ref": changed["f4"]["fact_ref"],
                       "cells": changed["f4"]["cells"]},
        "restored_f4": restored["f4"]["fact_ref"],
        "batch": baseline["batch"],
        "join": baseline["join"],
        "partial": baseline["partial"],
        "absent": baseline["absent"],
    }, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
