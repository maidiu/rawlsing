"""R2 native-oracle, changed/restore and guard checks for the locality experiment."""
from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time
from typing import Any

REVIEW = Path(__file__).resolve().parents[1]
REPO = REVIEW.parents[1]
AUTHOR = REPO / "WORKER_RETURNS" / "PYAT1006_PHYSICAL_ECONOMICS_R1"
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(AUTHOR))

import pyarrow.parquet as pq

from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError, VerifiedDirectEstate, write_direct_estate,
)
import rawlsing_next._pre553_query_eval as query_eval

from fixture_1006 import ShapeSpec, build_context
from query_1006 import build_query_bundle, execute_bundle_oracle
from r2_locality_probe import REAL_SORTED, fact_material, locality_sorted


def write_estate(tmp: Path, shape: ShapeSpec):
    root = tmp / shape.name
    root.mkdir(parents=True, mode=0o700)
    ctx = build_context(shape)
    bundle = build_query_bundle(ctx)
    receipt = write_direct_estate(
        ctx.direct_sections(), ctx.universe.ref, root, chunk_rows=16,
    )
    return root, ctx, bundle, receipt


def open_estate(root: Path, receipt: Any, bundle: Any, authorizer=lambda _r: True):
    return SavedC11Admission.open(
        root=root, exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        release_ref=receipt.reconstructed_v1_release_ref,
        runtime_catalog=bundle.catalog,
        current_authorizer=authorizer,
    )


def run(admission: SavedC11Admission, bundle: Any, name: str):
    query, predicate = bundle.by_name(name)
    return admission.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)


def sig(result: Any) -> list[dict[str, Any]]:
    return [fact_material(fact) for fact in result.facts]


def main(argv: list[str] | None = None) -> int:
    outdir = (REVIEW / "data" / "guard-probe") if len(sys.argv) == 1 else Path(sys.argv[1])
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    tmp = outdir
    result: dict[str, Any] = {
        "schema": "PYAT1006_R2_GUARD_PROBE@1",
        "status": "RUNNING",
    }
    original = ShapeSpec(
        "r2-guard-original", 48, include_weights=True,
        tag="PYAT1006-R2-GUARD-ORIGINAL",
    )
    changed = replace(
        original, name="r2-guard-changed", mutate_respondent=3,
        mutate_question="C",
    )
    root_a, ctx_a, bundle_a, receipt_a = write_estate(tmp, original)
    root_b, ctx_b, bundle_b, receipt_b = write_estate(tmp, changed)
    repo_a, release_a = ctx_a.native_oracle()
    repo_b, release_b = ctx_b.native_oracle()
    oracle_a = execute_bundle_oracle(
        repo_a, release_a, bundle_a,
        qa=bundle_a.catalog.authorities[-2], dauth=bundle_a.catalog.authorities[-1],
    )
    oracle_b = execute_bundle_oracle(
        repo_b, release_b, bundle_b,
        qa=bundle_b.catalog.authorities[-2], dauth=bundle_b.catalog.authorities[-1],
    )
    admission_a = open_estate(root_a, receipt_a, bundle_a)
    admission_b = open_estate(root_b, receipt_b, bundle_b)
    names = ("selected", "f2_reverse", "f4_three", "weighted", "repeated")
    baseline = {name: sig(run(admission_a, bundle_a, name)) for name in names}
    query_eval.sorted = locality_sorted
    try:
        candidate = {name: sig(run(admission_a, bundle_a, name)) for name in names}
        candidate_b = {name: sig(run(admission_b, bundle_b, name)) for name in names}
        restored = {name: sig(run(admission_a, bundle_a, name)) for name in names}
    finally:
        query_eval.sorted = REAL_SORTED
    for name in names:
        baseline[name] = baseline[name]
        assert candidate[name] == baseline[name], name
        assert baseline[name] == [fact_material(f) for f in oracle_a[name].facts], name
        assert candidate_b[name] == [fact_material(f) for f in oracle_b[name].facts], name
        assert restored[name] == baseline[name], name
    assert candidate_b["selected"] != baseline["selected"]
    assert candidate_b["f2_reverse"] != baseline["f2_reverse"]
    assert candidate_b["f4_three"] != baseline["f4_three"]
    original_repo_init = C11Repository.__init__
    original_read_table = pq.read_table

    def forbidden(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("candidate used a forbidden full-graph/whole-table fallback")

    try:
        C11Repository.__init__ = forbidden
        pq.read_table = forbidden
        query_eval.sorted = locality_sorted
        nofallback_result = run(admission_a, bundle_a, "selected")
    finally:
        C11Repository.__init__ = original_repo_init
        pq.read_table = original_read_table
        query_eval.sorted = REAL_SORTED
    assert [fact_material(f) for f in nofallback_result.facts] == baseline["selected"]
    result["no_fallback"] = {
        "full_c11_repository_init_blocked": True,
        "whole_table_read_blocked": True,
        "candidate_selected_still_exact": True,
    }
    result["oracle_parity"] = {
        "queries": list(names),
        "candidate_equal_baseline": True,
        "baseline_equal_native_oracle": True,
        "changed_equal_changed_oracle": True,
        "restored_equal_baseline": True,
        "changed_selected_differs": True,
    }
    hostile = ShapeSpec(
        "r2-guard-hostile", 24, include_weights=False,
        tag="PYAT1006-R2-GUARD-HOSTILE",
    )
    root_h, ctx_h, bundle_h, receipt_h = write_estate(tmp, hostile)
    guards: dict[str, Any] = {}
    try:
        open_estate(root_h, receipt_h, bundle_h, authorizer=lambda _r: False)
    except Exception as exc:  # noqa: BLE001
        guards["denied_current"] = {"refused": True, "error": f"{type(exc).__name__}: {exc}"}
    else:
        guards["denied_current"] = {"refused": False}
    wrong = replace(receipt_h.i02, source="SOURCE_ARTIFACT|forged:0")
    try:
        SavedC11Admission.open(
            root=root_h, exact_path=receipt_h.path,
            independently_held_manifest_sha256=receipt_h.manifest_sha256,
            independently_held_i02=wrong,
            release_ref=receipt_h.reconstructed_v1_release_ref,
            runtime_catalog=bundle_h.catalog,
            current_authorizer=lambda _r: True,
        )
    except Exception as exc:  # noqa: BLE001
        guards["wrong_source_root"] = {"refused": True, "error": f"{type(exc).__name__}: {exc}"}
    else:
        guards["wrong_source_root"] = {"refused": False}
    (Path(receipt_h.path) / "event_locator.parquet").unlink()
    try:
        VerifiedDirectEstate(
            root_h, exact_path=receipt_h.path,
            independently_held_manifest_sha256=receipt_h.manifest_sha256,
            independently_held_i02=receipt_h.i02,
            current_authorizer=lambda _r: True,
        )
    except DirectEstateError as exc:
        guards["omitted_locator"] = {"refused": True, "error": str(exc)}
    else:
        guards["omitted_locator"] = {"refused": False}
    hostile2 = ShapeSpec(
        "r2-guard-omission", 24, include_weights=False,
        tag="PYAT1006-R2-GUARD-OMISSION",
    )
    root_o, ctx_o, bundle_o, receipt_o = write_estate(tmp, hostile2)
    (Path(receipt_o.path) / "RoutingEligibilityFact.parquet").unlink()
    try:
        VerifiedDirectEstate(
            root_o, exact_path=receipt_o.path,
            independently_held_manifest_sha256=receipt_o.manifest_sha256,
            independently_held_i02=receipt_o.i02,
            current_authorizer=lambda _r: True,
        )
    except DirectEstateError as exc:
        guards["omitted_family_member"] = {"refused": True, "error": str(exc)}
    else:
        guards["omitted_family_member"] = {"refused": False}
    result["guards"] = guards
    result["all_guards_refused"] = all(row.get("refused") for row in guards.values())
    result["status"] = "MEASURED" if result["all_guards_refused"] else "FAILED_GUARD"
    (outdir / "guard_probe.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({
        "status": result["status"],
        "oracle_parity": result["oracle_parity"],
        "guards": guards,
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "MEASURED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
