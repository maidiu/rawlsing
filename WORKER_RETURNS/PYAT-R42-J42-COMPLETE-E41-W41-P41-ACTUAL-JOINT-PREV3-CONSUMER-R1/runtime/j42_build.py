"""Build the J42 actual joined product and the four required artifacts.

Each producer is executed fresh in its own isolated process; the joined
consumer runs in this process against their exact run identities.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
REPO = PACKET.parents[1]
sys.path.insert(0, str(HERE))

import j42_join as J  # noqa: E402


def _sha256(path):
    data = Path(path).read_bytes()
    return hashlib.sha256(data).hexdigest()


def run_driver(script, out_path):
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run(
        [sys.executable, str(HERE / script), "--out", str(out_path)],
        env=env, cwd=str(REPO), capture_output=True, text=True, timeout=1800)
    if proc.returncode != 0:
        raise SystemExit(f"{script} failed:\n{proc.stdout[-2000:]}\n{proc.stderr[-2000:]}")
    return json.loads(Path(out_path).read_text())


def typed_holds(e41, w41):
    bank = json.loads((PACKET / "vendor/e41/artifacts/computed_slice_evidence.json")
                      .read_text())
    slices = [dict(composed_result_identity_hash=row["composed_result_identity_hash"],
                   consumer_result_state=row["consumer_result_state"],
                   coverage_state=row["coverage_state"])
              for row in bank["slices"]]
    return dict(
        schema="J42_TYPED_HELD_MATRIX@1",
        e41_returned_bank=dict(
            slice_count=len(slices),
            dereference_state="DEREFERENCED_BY_HASH_AS_RETURNED_EVIDENCE",
            join_state="SAME_SOURCE_JOIN_UNISSUED",
            reason=("returned slices are heterogeneous sourcefree fixtures "
                    "(AT07/AT08/AT09/AT10/AT11 families), not slices of the "
                    "shared E04 58-row source consumed by W41/P41; they are "
                    "never pasted into the same-source empirical channel"),
            slices=slices),
        retained_gt2_j04=dict(
            retained_context_state=w41["retained_context"].get("state"),
            retained_context_grade=w41["retained_context"].get("grade"),
            position_state=w41["position_context"].get("state"),
            position_values_read=w41["position_context"].get("values_read"),
            join_state="NO_AUTHORIZED_JOIN",
            reason="retained GT2/J04 context is a separate retained read unit"),
        f6_evidence=dict(
            cases={key: dict(state=value["state"],
                             world_use=value["world_use"],
                             display_class=value["display_class"])
                   for key, value in w41["multifield"].items()},
            join_state="SEPARATE_READONLY_EVIDENCE_ONLY",
            reason="F6M/F6P not admitted as N9 transport"),
        purposes={key: value["state"] for key, value in w41["purposes"].items()},
        original35=e41["returned_bank_custody"]["f1f4_coverage_ledger.json"]
        ["held_original_scope"],
        actor="NOT TOUCHED", n11="HAND-BACK ONLY", n12="NOT TOUCHED")


def scientific_projection(manifest, receipts, matrix, handback, build_summary):
    payload = dict(manifest=manifest, receipts=receipts, matrix=matrix,
                   handback=handback, build_summary=build_summary)
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"),
                   allow_nan=False).encode()).hexdigest()


def build(outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    e41 = run_driver("e41_driver.py", outdir / "e41_fresh_run.json")
    w41 = run_driver("w41_driver.py", outdir / "w41_fresh_run.json")
    product = J.build_join(e41, w41)
    reverse = J.reverse_join(e41, w41)
    holds = typed_holds(e41, w41)

    coverage_ok = all(view["match"] for view in product["views"])
    expected_keys = {J.view_key(f, m, b)
                     for f in J.JOIN_FAMILIES for m in J.JOIN_MODES
                     for b in J.JOIN_BUDGETS}
    actual_keys = {view["key"] for view in product["views"]}
    no_drop = (expected_keys == actual_keys
               and len(product["views"]) == 84
               and len(product["joined_receipts"]) == 84
               and len(product["p41_receipts"]) == 84
               and all(len(receipt["n10e_steps"]) == 3
                       for receipt in product["p41_receipts"]))

    manifest = dict(
        schema="PYAT_R42_J42_JOINT_DEPENDENCY_MANIFEST@1",
        sealed_startup="cebb6c4197e101a28f07ab7f088221250d225056",
        upstreams=dict(
            E41=dict(commit=e41["source_commit"], provider=e41["provider_contract"],
                     rows_hash=e41["world_identity"]["rows_hash"],
                     packet_manifest_sha256=_sha256(PACKET / "vendor/e41/SHA256SUMS"),
                     bank=dict((k, v) for k, v in
                               e41["returned_bank_custody"].items())),
            W41=dict(commit=w41["source_commit"], contract=w41["contract"],
                     owner_archive_manifest_sha256=_sha256(
                         PACKET / "vendor/w41/owner_archive_manifest.json"),
                     custody=w41["returned_artifact_custody"]),
            P41=dict(commit="f27d1101048638bba395143a48efb7ef00bfcda4",
                     service="P41_GENERIC_POSSIBILITY_SERVICE@1",
                     staged_sha256=_sha256(PACKET / "vendor/p41/runtime/p41_service.py"),
                     runtime_provenance_sha256=_sha256(
                         PACKET / "vendor/p41/runtime/PROVENANCE.json"))),
        compatible_universe=dict(
            w41_views=len(w41["worlds"]),
            joined_views=len(product["views"]),
            joined_p41_receipts=len(product["p41_receipts"]),
            progressive_step_receipts=sum(len(r["n10e_steps"])
                                          for r in product["p41_receipts"]),
            e41_expected_ops=e41["returned_bank_custody"]
            ["f1f4_coverage_ledger.json"]["expected"],
            e41_executed_ops=e41["returned_bank_custody"]
            ["f1f4_coverage_ledger.json"]["executed"],
            e41_bank_slices=e41["returned_bank_custody"]
            ["computed_slice_evidence.json"]["slice_count"]),
        coverage=dict(route_oracle_match=coverage_ok, no_drop=no_drop,
                      expected_keys=sorted(expected_keys),
                      actual_keys=sorted(actual_keys)),
        held=holds,
        scientific_grade=dict(
            measured_original="NOT_RUN__NO_WARRANT",
            sourcefree_same_source_join="EXECUTED_GREEN",
            cross_source="TYPED_HELD",
            actor="NOT_TOUCHED", n11="HAND_BACK_ONLY", n12="NOT_TOUCHED"))

    receipts = dict(
        schema="PYAT_R42_J42_N9_N10E_N10W_JOINED_CONSUMER_RECEIPTS@1",
        contract=J.J42_CONTRACT,
        joined_service_steps="W41 structural -> E41 computed slices -> unchanged E04 NONPARENT_OPTIONS; P41 progressive over the same joined inputs",
        views={view["key"]: dict(
            expected_routes=view["expected"], actual_routes=view["actual"],
            match=view["match"],
            w41_snapshot_hash=view["w41_snapshot_hash"],
            w41_view_hash=view["w41_view_hash"],
            joined_consumer_receipt_hash=view["joined_receipt_hash"],
            p41_joined_receipt_hash=view["p41_receipt_hash"])
            for view in product["views"]},
        joined_consumer_receipts={
            entry["key"]: entry["joined_receipt"]
            for entry in product["joined_receipts"]},
        p41_joined_receipts={
            product["views"][index]["key"]: receipt
            for index, receipt in enumerate(product["p41_receipts"])},
        reverse_role=dict(
            target=reverse["query"]["target"],
            role_class=reverse["query"]["role_class"],
            denominators=[step["denominator"] for step in reverse["n10e_steps"]],
            cells=[{cell["cell"]: cell["raw_numerator_support"]
                    for cell in step["cells"]} for step in reverse["n10e_steps"]],
            receipt_hash=reverse["content_hash"]))

    matrix = dict(
        schema="PYAT_R42_J42_SOURCEFREE_VS_RETAINED_GRADE_MATRIX@1",
        F1=dict(local="sourcefree deterministic E41 bank", integrated="joined readset identity", original35="UNISSUED_HELD"),
        F2=dict(local="E41 AT07/AT08 computed slices", integrated="E41 32/16/8 chain into unchanged consumer", original35="UNISSUED_HELD"),
        F3=dict(local="E41 branch/discovery/recursive ops", integrated="E41 bank dereferenced, SAME_SOURCE_JOIN_UNISSUED", original35="UNISSUED_HELD"),
        F4=dict(local="E41 joint/cloud ops", integrated="E41 bank dereferenced, no cross-source fusion", original35="UNISSUED_HELD"),
        F5=dict(local="W41 retained FF context (GT2/J04)", integrated="read-only retained context; NO_AUTHORIZED_JOIN", original35="HELD"),
        F6=dict(local="F6M/F6P separate evidence", integrated="separate readonly evidence only; no N9 transport", original35="HELD"),
        F7=dict(local="EE1 temporal methods via W41", integrated="sourcefree probe-only; no measured pair", original35="HELD"),
        F8=dict(local="P41 generic service + W41 worlds", integrated="EXECUTED_GREEN same-source join", original35="hand-back to A42"),
        typed_holds=holds)

    handback = dict(
        schema="PYAT_R42_J42_N11_ACTUAL_JOIN_HANDBACK@1",
        claim_id="J42_E41xW41xP41_ACTUAL_JOINED_PREV3_CONSUMER_V1",
        actual_target_consumer="product.nonparent.consume NONPARENT_OPTIONS (unchanged byte-identical) + P41 GENERIC_POSITIONED_SUBJECT",
        claimed_dependency="fresh E41 computed slices + fresh W41 ObjectiveWorld reads -> joined E04 service -> unchanged consumer; P41 progressive assembly",
        frozen_oracle="01_FROZEN_JOIN_PLAN.json",
        receipt_contract=J.J42_CONTRACT,
        receipt_hashes=dict(
            joined_consumer=[view["joined_receipt_hash"] for view in product["views"]],
            p41_joined=[view["p41_receipt_hash"] for view in product["views"]],
            reverse=reverse["content_hash"],
            e41_rows_hash=e41["world_identity"]["rows_hash"],
            w41_views=sorted(view["w41_view_hash"] for view in product["views"])),
        expected_vs_consumed=dict(expected_views=84, consumed_views=len(product["views"]),
                                  route_oracle_match=coverage_ok, no_drop=no_drop),
        proof_witnesses="evidence/witness-*.json (five severance edges)",
        exact_remaining_decisions=[
            "original-source read/operation warrant (N03/C11 custody)",
            "consumer purpose admission for CONCEPTION_SCENARIO_PROPOSALS / N9_SELECTED_WORLD",
            "F6 transport/partial-world model grant (no admission granted here)",
            "dyad/household sampling-unit linkage authority",
            "independent joint scientific acceptance (not self-issued)"],
        original35_state="UNISSUED_HELD",
        actor="NOT TOUCHED", n11_adoption="NONE (hand-back only)", n12="NOT TOUCHED")

    build_summary = dict(
        schema="PYAT_R42_J42_BUILD_SUMMARY@1",
        families=list(J.JOIN_FAMILIES), modes=list(J.JOIN_MODES),
        budgets=list(J.JOIN_BUDGETS),
        w41_views=len(w41["worlds"]), joined_views=len(product["views"]),
        progressive_receipts=len(product["p41_receipts"]),
        route_oracle_match=coverage_ok, no_drop=no_drop,
        e41_world_rows_hash=e41["world_identity"]["rows_hash"],
        e41_reverse_denominator=reverse["n10e_steps"][0]["denominator"])

    files = {}
    for name, payload in (
            ("actual_e41_w41_p41_joint_dependency_manifest.json", manifest),
            ("n9_n10e_n10w_real_joined_consumer_receipts.json", receipts),
            ("sourcefree_vs_retained_scientific_grade_matrix.json", matrix),
            ("n11_actual_join_handback.json", handback),
            ("evidence/j42_build_summary.json", build_summary)):
        target = PACKET / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        files[name] = _sha256(target)
    projection = scientific_projection(manifest, receipts, matrix, handback,
                                       build_summary)
    (PACKET / "evidence/j42_scientific_projection.sha256").write_text(projection + "\n")
    return dict(files=files, projection=projection, coverage_ok=coverage_ok,
                no_drop=no_drop)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()
    import tempfile
    outdir = Path(args.outdir) if args.outdir else Path(
        tempfile.mkdtemp(prefix="j42-drivers-"))
    result = build(outdir)
    print(json.dumps(result, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
