"""J42 E41 isolated driver: fresh E41-native computed slices over the E04 source.

Run inside the E41 staged environment (its own bootstrap); writes one JSON
receipt. No values are copied from the returned artifact bank; the bank is
dereferenced by hash for custody only.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
E41 = PACKET / "vendor/e41"
sys.path.insert(0, str(E41))
import bootstrap  # noqa: E402  (E41 bootstrap)

import rawlsing_next  # noqa: E402

NAME = "rawlsing_next.pre553_n9_n10w_progressive_candidate"
if NAME not in sys.modules:
    spec = importlib.util.spec_from_file_location(
        NAME, E41 / "vendor/aux/pre553_n9_n10w_progressive_candidate.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[NAME] = module
    spec.loader.exec_module(module)
    setattr(rawlsing_next, "pre553_n9_n10w_progressive_candidate", module)
sys.path.insert(0, str(E41 / "vendor"))

from product.empirical import build_source  # noqa: E402
from e41_provider_extension import provide_empirical_possibility_slice_ext  # noqa: E402
from rawlsing_next.tests import c1_at08_at13_fixture as c1  # noqa: E402
from rawlsing_next.tests import test_pre553_empirical_query as fx  # noqa: E402
from rawlsing_next.pre553_empirical_objects import (  # noqa: E402
    ExactRef, canonicalize, semantic_hash)

E03 = sys.modules[NAME]
EXT_CONTRACT = "N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER_EXT@1.1.0"


def _world():
    rows = E03.synthetic_world_rows()
    tag = "e04-base-r1"
    source = fx._build_source(
        tag, rows, question_namespace="E04_NATIVE_BINARY",
        risk_sets={"R_ALL": {q: {r["id"] for r in rows} for q in ("A", "B", "C", "Y")}},
        risk_namespace=tag)
    source["risk_refs"]["R"] = source["risk_refs"]["R_ALL"]
    qauth = fx._query_authority(tag + "-query")
    return dict(
        tag=tag, source=source, qauth=qauth,
        registry=fx._registry(source, qauth),
        pairing=c1.make_pairing_authority(tag),
        model_rule=c1.make_model_rule(source["universe"].ref, tag),
        rows_hash=semantic_hash(rows),
        permission_root="TEST_ONLY_E04_SOURCE_ROOT",
        publication="2026-03-01")


def _step(world, target, conditions):
    source = world["source"]
    predicate = E03._joint_predicate(world, conditions)
    query = E03._producer_query(world, predicate, target)
    bindings = [
        c1.make_conditioner_binding(
            binding_id=q.lower(),
            subject_fact_ref=ExactRef(**c1.subject_fact_ref(source, q, v)),
            empirical_coordinate_ref=source["qrefs"][q],
            comparability_authority_ref=world["pairing"],
            source_universe_ref=source["universe"].ref,
            release_ref=source["release_ref"])
        for q, v in conditions]
    consumer = c1.make_multi_conditioner_consumer_query(
        query_id="J42-" + semantic_hash([target, [list(c) for c in conditions]])[:12],
        subject_ref=ExactRef("J42_SYNTHETIC_SUBJECT", "urn:test:j42:subject",
                             semantic_hash("j42-subject")),
        target_ref=source["qrefs"][target],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=bindings,
        projection_kind="J42_JOINED_EMPIRICAL_POSSIBILITY",
        projection_payload={"ordered_conditions": [list(c) for c in conditions]})
    witness = E03._witness(world, "j42", consumer, query, predicate, conditions)
    result = provide_empirical_possibility_slice_ext(
        repository=source["repo"], empirical_query=query, predicate=predicate,
        authority_registry=world["registry"],
        release_refs=(source["release_ref"],), consumer_query=consumer,
        model_rule=world["model_rule"], condition_binding_witness=witness)
    composition = result.composition_result
    cells = [{"cell": str(row["cell"]),
              "raw_numerator_support": int(row["raw_numerator_support"])}
             for row in composition.complete_cell_geometry]
    return dict(
        target=target,
        conditioners=[[q, v] for q, v in conditions],
        route=result.producer_route,
        provider_state=result.provider_state,
        fact_state=composition.producer_fact_state,
        denominator=int(composition.raw_denominator_support),
        cells=cells,
        evidence_ref=(None if result.generated_evidence_or_null is None
                      else result.generated_evidence_or_null.evidence_ref.as_dict()),
        composed_hash=composition.composed_result_identity_hash,
        consumer_state=(None if result.consumer_result_or_null is None
                        else result.consumer_result_or_null.result_state),
        joint_component_count=int(result.extension_receipt.joint_component_count),
        joint_order_semantics=result.extension_receipt.joint_order_semantics)


def _bank_custody():
    root = E41 / "artifacts"
    out = {}
    for name in ("computed_slice_evidence.json", "f1f4_coverage_ledger.json",
                 "slice_consumer_receipt.json"):
        data = (root / name).read_bytes()
        payload = json.loads(data)
        row = dict(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
        if name == "computed_slice_evidence.json":
            row["slice_count"] = payload["slice_count"]
        if name == "f1f4_coverage_ledger.json":
            row.update(executed=payload["executed_operation_count"],
                       expected=payload["expected_operation_count"],
                       no_drop_ok=payload["no_drop_ok"],
                       original_source_occupied_count=payload["original_source_occupied_count"],
                       held_original_scope=payload.get("held_original_scope"))
        out[name] = row
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    world = _world()
    source = world["source"]
    steps = {}
    for depth, conditions in ((1, (("A", 1),)), (2, (("A", 1), ("B", 1))),
                              (3, (("A", 1), ("B", 1), ("C", 1)))):
        steps[f"Y/{depth}"] = _step(world, "Y", conditions)
    steps["A/1"] = _step(world, "A", (("Y", 1),))
    payload = dict(
        schema="J42_E41_FRESH_RUN@1",
        source_commit="6e123bafe749d6997c764ae117fb5e68e0139ed7",
        provider_contract=EXT_CONTRACT,
        provider_module=Path(sys.modules["e41_provider_extension"].__file__).name,
        world_identity=dict(
            rows_hash=world["rows_hash"],
            source_universe_ref=source["universe"].ref.as_dict(),
            release_ref=source["release_ref"].as_dict(),
            permission_root=world["permission_root"],
            model_rule_hash=world["model_rule"].rule_hash,
            risk_R=canonicalize(source["risk_refs"]["R"])),
        steps=steps,
        returned_bank_custody=_bank_custody(),
        no_original_source_read=True)
    Path(args.out).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"steps": {k: {"denominator": v["denominator"],
                                    "cells": {c["cell"]: c["raw_numerator_support"]
                                              for c in v["cells"]},
                                    "route": v["route"]}
                               for k, v in steps.items()}}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
