#!/usr/bin/env python3
"""B20 bounded qualification court for frozen Route-C CACC1/CACC2 + parity adapter."""
from __future__ import annotations

from dataclasses import replace
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import pandas as pd

from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
from rawlsing_next.pre553_physical_decoder import PhysicalSourceIncidence, PhysicalVariable, PhysicalMissingState
from rawlsing_next.pre553_source_backed_c11_facade import (
    CoordinateSlotRule,
    ExactPhysicalCellStream,
    OccurrenceRule,
    PhysicalSlot,
    ResponseSlotRule,
    ResponseValueRule,
    build_validated_source_backed_c11_release,
    physical_value_binding_key,
)
from rawlsing_next.pre553_route_c_accelerators import (
    CACC2_FROZEN_ROLE_ORDER,
    Cacc1Paths,
    Cacc2AtomBinding,
    Cacc2Determinants,
    RouteCDeterminants,
    RouteCDeterminantMismatch,
    RouteCCorruptAccelerator,
    assert_exact_discovery_identity_parity,
    assert_exact_query_identity_parity,
    build_cacc1,
    build_cacc2,
    cacc1_to_exact_physical_stream,
    cacc2_mask_for_role,
    delete_cacc1,
    delete_cacc2,
    execute_route_c_empirical_query,
    execute_route_c_exact_bounded_discovery,
    mask_member,
    read_cacc1,
    read_cacc2,
)
from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate,
    _h,
    _predicate,
    _query,
    _query_authority,
    _ref,
    _registry,
    _response_leaf,
)
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _atom,
    _d_auth,
    _discovery_authority,
    _grammar,
    _qt,
    _rule,
)


PASS = "AS4I_ROUTE_C_CACC1_CACC2_PARITY_ADAPTER_IMPLEMENTATION_COMPLETE__READY_FOR_COMMON_ABC_HARNESS_INTAKE"


def _sha(path: Path) -> str:
    d = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            d.update(block)
    return d.hexdigest()


def _cjson(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def _route_c_fixture(tag: str = "b20"):
    fx = _fixture(tag)
    old = fx["projection"]
    source_sha = _h(f"route-c-physical:{tag}")
    data = [
        [1, 0, "US", "C1", "R1", "TC1", "TD1"],
        [0, 1, "US", "C2", "R1", "TC2", "TD2"],
        [None, 1, "CA", "C3", "R2", "TC3", "TD3"],
    ]
    names = ("q301_2", "q301_7", "country", "city", "region", "tablec", "tabled")
    variables = tuple(
        PhysicalVariable(i, name, None, f"label-{name}", {}, (), {}, {})
        for i, name in enumerate(names, 1)
    )
    incidence = PhysicalSourceIncidence(
        source_sha256=source_sha,
        source_format="SYNTHETIC",
        row_count=3,
        variables=variables,
        reader_configuration={"fixture": "B20_ROUTE_C", "decoder": "SYNTHETIC_EXACT"},
        file_metadata={"fixture": "B20_ROUTE_C"},
        _frame=pd.DataFrame(data, columns=names, dtype=object),
    )
    by_q = {slot.slot.name: slot for slot in old.response_slots}
    q2_binding = by_q["X"].question_binding
    q7_binding = by_q["M"].question_binding
    scalar = lambda q: OccurrenceRule(
        "0", _ref("TOPOLOGY", f"b20-{q}-SCALAR"), {"kind": "SCALAR_SINGULAR", "index": 0}
    )
    key = lambda raw, state=PhysicalMissingState.OBSERVED_STORAGE_VALUE: physical_value_binding_key(raw, state)
    q2 = ResponseSlotRule(
        PhysicalSlot(1, "q301_2"),
        q2_binding,
        (
            ResponseValueRule(key(1), "SUBSTANTIVE_RESPONSE", (scalar("q301_2"),)),
            ResponseValueRule(key(0), "SUBSTANTIVE_RESPONSE", (scalar("q301_2"),)),
            ResponseValueRule(
                key(None, PhysicalMissingState.SYSTEM_MISSING),
                "MISSING",
                (scalar("q301_2"),),
            ),
        ),
    )
    q7 = ResponseSlotRule(
        PhysicalSlot(2, "q301_7"),
        q7_binding,
        tuple(
            ResponseValueRule(key(value), "SUBSTANTIVE_RESPONSE", (scalar("q301_7"),))
            for value in (0, 1)
        ),
    )
    coords = tuple(
        CoordinateSlotRule(
            PhysicalSlot(i + 3, name),
            _ref("COORDINATE_NATIVE", f"b20-{name}"),
            _ref("UNIT_TAXONOMY", f"b20-{name}"),
            "2026-09-08",
            fx["coord_auth"].authority_ref,
            copy_observed_raw=True,
        )
        for i, name in enumerate(("country", "city", "region", "tablec", "tabled"))
    )
    allowed_qrefs = {q2_binding.native_question_ref, q7_binding.native_question_ref}
    routing = tuple(
        fact for fact in old.routing if fact.question_or_target_ref in allowed_qrefs
    )
    projection = replace(
        old,
        expected_source_sha256=source_sha,
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT", f"urn:test:b20:snapshot:{tag}", source_sha
        ),
        response_slots=(q2, q7),
        coordinate_slots=coords,
        weight_slots=(),
        routing=routing,
    )
    stream = ExactPhysicalCellStream(
        source_sha, 3, lambda: incidence.iter_cells(), "B20_SYNTHETIC_EXACT_STREAM"
    )
    determinants = RouteCDeterminants(
        source_sha256=source_sha,
        decoder_identity={"decoder": "SYNTHETIC_EXACT", "version": "1", "config": {"fixture": tag}},
        projection_authority_hash=_h("b20-projection-authority"),
        slot_ledger_hash=_h("b20-slot-ledger"),
        governed_projection_hash=projection.cache_identity,
        c11_logical_release_hash=_h("b20-c11-logical-release"),
        replay_manifest_hash=_h("b20-replay-manifest"),
        semantic_authority_closure_hash=_h("b20-semantic-authority-closure"),
    )
    return fx, incidence, stream, projection, determinants


def _runtime_source(fx, release):
    return {
        **fx,
        "repo": C11Repository((release,)),
        "release_ref": release.release_ref,
    }


def _atom_bindings(all_predicate, x1_predicate):
    dummy = {}
    for role in CACC2_FROZEN_ROLE_ORDER:
        if role in {"A000", "A1RAPP"}:
            ref = all_predicate.ref
        elif role == "A1V1":
            ref = x1_predicate.ref
        else:
            digest = _h(f"b20-runtime-predicate:{role}")
            ref = ExactRef(
                "EmpiricalPredicate@1.0.0",
                f"urn:test:b20:runtime-predicate:{role}:sha256:{digest}",
                digest,
            )
        dummy[role] = Cacc2AtomBinding(
            role_id=role,
            semantic_atom_content_hash=_h(f"b20-semantic-atom:{role}"),
            runtime_predicate_ref=ref,
        )
    return tuple(dummy.values())


def _run_once(root: Path):
    root.mkdir(parents=True, exist_ok=True)
    fx, incidence, stream, projection, determinants = _route_c_fixture("deterministic")
    paths = Cacc1Paths(root / "cacc1.arrow", root / "cacc1.manifest.json")

    cacheless_release = build_validated_source_backed_c11_release(incidence, projection)
    first = build_cacc1(
        stream=stream,
        projection=projection,
        determinants=determinants,
        paths=paths,
    )
    read_first = read_cacc1(paths=paths, expected_determinants=determinants)
    accelerated_stream = cacc1_to_exact_physical_stream(read_first, projection)
    from rawlsing_next.pre553_source_backed_c11_facade import build_validated_source_backed_c11_release_from_stream
    accelerated_release = build_validated_source_backed_c11_release_from_stream(accelerated_stream, projection)
    assert accelerated_release.release_ref == cacheless_release.release_ref
    assert accelerated_release.replay_manifest.ref == cacheless_release.replay_manifest.ref
    assert tuple(x.ref for x in accelerated_release.public_objects) == tuple(
        x.ref for x in cacheless_release.public_objects
    )
    assert tuple(x.ref for x in accelerated_release.internal_records) == tuple(
        x.ref for x in cacheless_release.internal_records
    )

    source_cacheless = _runtime_source(fx, cacheless_release)
    qauth = _query_authority("b20-route-c-query")
    all_p = _branch_predicate(source_cacheless, qauth, tag="b20-all")
    x1 = _predicate(
        source_cacheless,
        qauth,
        _response_leaf(source_cacheless, qauth, "X", 1),
        tag="b20-x1",
    )
    query = _query(source_cacheless, qauth, all_p, ("M",), tag="b20-query")
    registry = _registry(source_cacheless, qauth)
    cacheless_query = execute_empirical_query(
        repository=source_cacheless["repo"],
        query=query,
        predicate=all_p,
        authority_registry=registry,
        release_refs=(cacheless_release.release_ref,),
    )

    c2dir = root / "cacc2"
    c2det = Cacc2Determinants(
        cacc1_determinant_hash=determinants.content_hash,
        discovery_authority_ref=ExactRef(
            "DiscoveryAuthority@1.0.0",
            f"urn:test:b20:da:{_h('b20-da')}",
            _h("b20-da"),
        ),
        predicate_catalog_hash=_h("b20-predicate-catalog"),
        risk_partition_hash=_h("b20-risk-partition"),
        production_operation_identity="B20_BOUNDED_GOVERNED_FIXTURE_OPERATION",
        candidate_frontier_ref=ExactRef(
            "PRE553_I05_EVALUATED_FRONTIER",
            f"urn:test:b20:frontier:{_h('b20-frontier')}",
            _h("b20-frontier"),
        ),
    )
    c2 = build_cacc2(
        directory=c2dir,
        cacc1=read_first,
        determinants=c2det,
        atom_bindings=_atom_bindings(all_p, x1),
    )
    c2read = read_cacc2(directory=c2dir, expected_determinants=c2det)
    assert c2read == c2
    risk_mask = cacc2_mask_for_role(c2dir, c2read, "A000")
    assert all(mask_member(risk_mask, row, 3) for row in (1, 2, 3))
    assert mask_member(cacc2_mask_for_role(c2dir, c2read, "A1V1"), 1, 3)
    assert not mask_member(cacc2_mask_for_role(c2dir, c2read, "A1V1"), 2, 3)
    assert mask_member(cacc2_mask_for_role(c2dir, c2read, "A1SMIS"), 3, 3)

    accelerated_query = execute_route_c_empirical_query(
        cacc1=read_first,
        projection=projection,
        query=query,
        predicate=all_p,
        authority_registry=registry,
        cacc2_directory=c2dir,
        cacc2_manifest=c2read,
        required_atom_roles=("A000",),
    )
    assert_exact_query_identity_parity(cacheless_query, accelerated_query)

    # One exact I05 candidate is enough to prove DiscoveryResultReceipt identity parity:
    # both paths invoke the same unmodified exact discovery engine over byte-identical C11.
    dauth = _d_auth("b20-route-c-discovery")
    operation = "I03-OP-b20-route-c-discovery"
    dquery = _query(source_cacheless, qauth, all_p, ("M",), tag="b20-discovery-template")
    grammar = _grammar(
        operation=operation,
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("X1", x1, "RESPONSE")],
        templates=[_qt("M", dquery)],
        rules=[_rule(
            "minority",
            "MINORITY_OR_NONMODAL_DEPARTURE",
            "SINGLE_ATOM",
            atom_ids=("X1",),
            baseline_atom_id="ALL",
            query_template_id="M",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
    )
    da = _discovery_authority(source_cacheless, grammar, dauth, tag="b20-da")
    dregistry = _registry(source_cacheless, qauth, dauth)
    cacheless_discovery = execute_exact_bounded_discovery(
        repository=source_cacheless["repo"],
        discovery_authority=da,
        authority_registry=dregistry,
        release_refs=(cacheless_release.release_ref,),
        predicate_catalog=(all_p, x1),
        query_template_catalog=(dquery,),
    )
    accelerated_discovery = execute_route_c_exact_bounded_discovery(
        cacc1=read_first,
        projection=projection,
        discovery_authority=da,
        authority_registry=dregistry,
        predicate_catalog=(all_p, x1),
        query_template_catalog=(dquery,),
        cacc2_directory=c2dir,
        cacc2_manifest=c2read,
    )
    assert_exact_discovery_identity_parity(cacheless_discovery, accelerated_discovery)

    c1_identity = {
        "logical": first.manifest["logical_content_hash"],
        "physical": first.manifest["physical_byte_sha256"],
        "determinant": first.manifest["determinant_hash"],
    }
    c2_identity = {
        "logical": c2read["logical_content_hash"],
        "determinant": c2read["determinant_hash"],
        "mask_hashes": {
            entry["role_id"]: entry["sha256"] for entry in c2read["atom_entries"]
        },
        "risk_sha256": c2read["risk_entry"]["sha256"],
    }

    # Hostile determinant mismatch.
    bad = replace(determinants, replay_manifest_hash=_h("b20-wrong-replay"))
    try:
        read_cacc1(paths=paths, expected_determinants=bad)
    except RouteCDeterminantMismatch:
        stale_cacc1 = "PASS_FAIL_CLOSED"
    else:
        raise AssertionError("stale CACC1 determinant was accepted")

    # Physical corruption.
    good_bytes = paths.arrow_ipc.read_bytes()
    paths.arrow_ipc.write_bytes(good_bytes[:-1] + bytes([good_bytes[-1] ^ 1]))
    try:
        read_cacc1(paths=paths, expected_determinants=determinants)
    except RouteCCorruptAccelerator:
        corrupt_cacc1 = "PASS_FAIL_CLOSED"
    else:
        raise AssertionError("corrupt CACC1 bytes were accepted")
    paths.arrow_ipc.write_bytes(good_bytes)
    read_cacc1(paths=paths, expected_determinants=determinants)

    # CACC2 hostile determinant and corrupt mask.
    bad2 = replace(c2det, risk_partition_hash=_h("b20-wrong-risk"))
    try:
        read_cacc2(directory=c2dir, expected_determinants=bad2)
    except RouteCDeterminantMismatch:
        stale_cacc2 = "PASS_FAIL_CLOSED"
    else:
        raise AssertionError("stale CACC2 determinant was accepted")
    mask_path = c2dir / c2read["atom_entries"][0]["file"]
    good_mask = mask_path.read_bytes()
    mask_path.write_bytes(bytes([good_mask[0] ^ 1]) + good_mask[1:])
    try:
        read_cacc2(directory=c2dir, expected_determinants=c2det)
    except RouteCCorruptAccelerator:
        corrupt_cacc2 = "PASS_FAIL_CLOSED"
    else:
        raise AssertionError("corrupt CACC2 mask was accepted")
    mask_path.write_bytes(good_mask)
    read_cacc2(directory=c2dir, expected_determinants=c2det)

    # Unauthorized extra cache material is a hard failure, preventing a hidden third accelerator.
    extra = c2dir / "unauthorized-third-accelerator.bin"
    extra.write_bytes(b"x")
    try:
        read_cacc2(directory=c2dir, expected_determinants=c2det)
    except RouteCCorruptAccelerator:
        extra_cache = "PASS_FAIL_CLOSED"
    else:
        raise AssertionError("unauthorized extra CACC2 cache material was accepted")
    extra.unlink()

    # Delete both optional accelerators: truth survives cacheless.
    delete_cacc1(paths)
    delete_cacc2(c2dir)
    assert not paths.arrow_ipc.exists() and not paths.manifest.exists() and not c2dir.exists()
    cacheless_after_delete = build_validated_source_backed_c11_release(incidence, projection)
    assert cacheless_after_delete.release_ref == cacheless_release.release_ref
    cacheless_query_after_delete = execute_empirical_query(
        repository=C11Repository((cacheless_after_delete,)),
        query=query,
        predicate=all_p,
        authority_registry=registry,
        release_refs=(cacheless_after_delete.release_ref,),
    )
    assert_exact_query_identity_parity(cacheless_query, cacheless_query_after_delete)

    # Exact regeneration.
    rebuilt = build_cacc1(
        stream=stream,
        projection=projection,
        determinants=determinants,
        paths=paths,
    )
    rebuilt_read = read_cacc1(paths=paths, expected_determinants=determinants)
    rebuilt_c2 = build_cacc2(
        directory=c2dir,
        cacc1=rebuilt_read,
        determinants=c2det,
        atom_bindings=_atom_bindings(all_p, x1),
    )
    rebuilt_c2_read = read_cacc2(directory=c2dir, expected_determinants=c2det)
    assert rebuilt.manifest["logical_content_hash"] == c1_identity["logical"]
    assert rebuilt.manifest["physical_byte_sha256"] == c1_identity["physical"]
    assert rebuilt_c2_read["logical_content_hash"] == c2_identity["logical"]
    assert {
        entry["role_id"]: entry["sha256"] for entry in rebuilt_c2_read["atom_entries"]
    } == c2_identity["mask_hashes"]

    regenerated_query = execute_route_c_empirical_query(
        cacc1=rebuilt_read,
        projection=projection,
        query=query,
        predicate=all_p,
        authority_registry=registry,
        cacc2_directory=c2dir,
        cacc2_manifest=rebuilt_c2_read,
        required_atom_roles=("A000",),
    )
    assert_exact_query_identity_parity(cacheless_query, regenerated_query)

    return {
        "status": "PASS",
        "terminal": PASS,
        "cacc1": c1_identity,
        "cacc2": c2_identity,
        "cacheless_release_ref": cacheless_release.release_ref.as_dict(),
        "cacheless_replay_ref": cacheless_release.replay_manifest.ref.as_dict(),
        "query_fact_refs": [f.ref.as_dict() for f in cacheless_query.facts],
        "discovery_frontier_ref": cacheless_discovery.evaluated_frontier_ref.as_dict(),
        "discovery_receipt_refs": [r.ref.as_dict() for r in cacheless_discovery.receipts],
        "hostile": {
            "stale_cacc1": stale_cacc1,
            "corrupt_cacc1": corrupt_cacc1,
            "stale_cacc2": stale_cacc2,
            "corrupt_cacc2": corrupt_cacc2,
            "unauthorized_extra_cache_material": extra_cache,
        },
        "delete_rebuild": "PASS_EXACT_IDENTITIES_PRESERVED",
        "accelerator_count": 2,
        "candidate_execution_count": 1,
        "real_c09_execution_count": 0,
        "wvs7_execution_count": 0,
        "architecture_ranking_count": 0,
    }


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "rawlsing_next").is_dir() and (parent / "data").is_dir():
            return parent
    raise RuntimeError("cannot locate repository root for fresh-process replay")


def _fresh_process_replay(base: Path):
    children = []
    repo_root = _repo_root()
    for index in (1, 2):
        root = base / f"fresh_{index}"
        script = Path(__file__).resolve()
        code = (
            "import runpy,sys;"
            f"sys.path.insert(0,{str(repo_root)!r});"
            f"sys.argv=[{str(script)!r},'--child',{str(root)!r}];"
            f"runpy.run_path({str(script)!r},run_name='__main__')"
        )
        cmd = [sys.executable, "-I", "-c", code]
        proc = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"fresh process {index} failed: {proc.stderr}")
        value = json.loads(proc.stdout)
        children.append(value)
    left, right = children
    keys = ("cacc1", "cacc2", "cacheless_release_ref", "cacheless_replay_ref", "query_fact_refs",
            "discovery_frontier_ref", "discovery_receipt_refs")
    if any(left[k] != right[k] for k in keys):
        raise AssertionError("fresh processes did not reproduce content-addressed Route-C outputs")
    return {
        "status": "PASS",
        "process_count": 2,
        "independent_roots": [str(base / "fresh_1"), str(base / "fresh_2")],
        "reproduced_keys": list(keys),
        "cacc1_logical_content_hash": left["cacc1"]["logical"],
        "cacc1_physical_byte_sha256": left["cacc1"]["physical"],
        "cacc2_logical_content_hash": left["cacc2"]["logical"],
        "discovery_frontier_ref": left["discovery_frontier_ref"],
        "query_fact_refs": left["query_fact_refs"],
        "discovery_receipt_refs": left["discovery_receipt_refs"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--child")
    parser.add_argument("--output")
    args = parser.parse_args()
    if args.child:
        result = _run_once(Path(args.child))
        print(_cjson(result))
        return 0
    with tempfile.TemporaryDirectory(prefix="b20-route-c-court-") as td:
        root = Path(td)
        single = _run_once(root / "single")
        replay = _fresh_process_replay(root)
        receipt = {
            "schema": "B20_ROUTE_C_IMPLEMENTATION_QUALIFICATION@1.0.0",
            "status": "PASS",
            "terminal": PASS,
            "single_process": single,
            "fresh_process_replay": replay,
        }
        if args.output:
            Path(args.output).write_text(_cjson(receipt) + "\n", encoding="utf-8")
        print(_cjson(receipt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
