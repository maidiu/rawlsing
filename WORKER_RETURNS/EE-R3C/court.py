from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

B03_COMMIT = "3d1cdd242fe10f544bdcbb5bb91cf042c56ef787"
EE_R2D_COMMIT = "ec1d5dc11a13290853632d7ab967b6094f2b9955"
EXPECTED_TARGET_STREAM_SHA256 = "dc1cfbfd49abbb313e0d36ff3229fcd07abfc627f67f9e2fbb936fcfca129502"
B03_REL = Path("data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/RESIDUAL_ZERO_LOSS_EXECUTION_WAVE_R2/B03_ROUTING_GSS_WVS_EVS")

TARGET_IDS = [
    "question_impl.phase0.0b98e85ad59489ef0d20",
    "question_impl.phase0.0dfba63129bbfe4c9d68",
    "question_impl.phase0.123de9d4868bf66d84a1",
    "question_impl.phase0.1569f26ce284ee346a1c",
    "question_impl.phase0.16f57b613e4329998eb3",
    "question_impl.phase0.19fea645f0733f9def7f",
    "question_impl.phase0.1a07d9cb975a0d5ffe5c",
    "question_impl.phase0.1bdd9e7b6024d62e0c91",
    "question_impl.phase0.1fc99fb5900345f99ca1",
    "question_impl.phase0.34c2787bfafaeeab3d50",
    "question_impl.phase0.388a01fb094a3f81ac6b",
    "question_impl.phase0.3cc925ddb6c18bd16025",
    "question_impl.phase0.42929081bc9fc60d93e9",
    "question_impl.phase0.45ace696dbd830b04729",
    "question_impl.phase0.51b35a036068417c8fe0",
    "question_impl.phase0.5293a667d39627fbca8b",
    "question_impl.phase0.54b211649ee6fccd651a",
    "question_impl.phase0.5bbf9f25f27cf385fade",
    "question_impl.phase0.6854543f9e0c00197661",
    "question_impl.phase0.6bd976214617dc817176",
    "question_impl.phase0.726dbf48581c3d4d600c",
    "question_impl.phase0.7555028a2eafddb1c875",
    "question_impl.phase0.75881b2f3c8a69ce35f1",
    "question_impl.phase0.7b9f2c4c0a351e5e91db",
    "question_impl.phase0.85cc129d00e20a392652",
    "question_impl.phase0.8ad4a48146d247ecd389",
    "question_impl.phase0.8c065399c60e281fd7bd",
    "question_impl.phase0.8da159b3ddb964ba6920",
    "question_impl.phase0.91849a2d395fb6d52287",
    "question_impl.phase0.b78ee930bd27f2493b94",
    "question_impl.phase0.bb7f69b7f5938c5d2e65",
    "question_impl.phase0.bbbde435f9f054f959b6",
    "question_impl.phase0.bd1338131ce6dca3d091",
    "question_impl.phase0.be54e9d12c75b9ed00a8",
    "question_impl.phase0.c0cf7b45b65b869e67c8",
    "question_impl.phase0.c0ed2eee1551ce834721",
    "question_impl.phase0.c140c59eb116d2004a07",
    "question_impl.phase0.c4069d5a276ee56be677",
    "question_impl.phase0.cb14f127baccd4db32e7",
    "question_impl.phase0.cc80dd91292510bfb789",
    "question_impl.phase0.cf972cf2474a8233da88",
    "question_impl.phase0.d0ae65f150648b24b479",
    "question_impl.phase0.d292d43a900c311b3b1c",
    "question_impl.phase0.d385df9245e874ea361c",
    "question_impl.phase0.d3b2172408cac937fcea",
    "question_impl.phase0.d48f4a1e573dd15d4b8a",
    "question_impl.phase0.d91b4359c4e1e64389d8",
    "question_impl.phase0.db76b576cd89e3223278",
    "question_impl.phase0.dc8a1f84391d374d3994",
    "question_impl.phase0.e0f4edddd84cf0bef13a",
    "question_impl.phase0.eaadb4c99a2528500c3d",
    "question_impl.phase0.ed62f99c401abffa0b5b",
    "question_impl.phase0.f7a82a1a1bee1bac144c",
    "question_impl.phase0.f7fcccad99227a9259a3",
    "question_impl.phase0.fe4af24c3dc059e8c1b9",
]

STATUS_MEANING = {
    "G": "UNCONDITIONAL_SOURCE_PROVEN",
    "R": "RESPONDENT_ANSWER_CONDITIONAL",
    "E": "DEMOGRAPHIC_OR_ELIGIBILITY_CONDITIONAL",
    "M": "MULTI_CONDITION",
    "B": "MODULE_OR_BALLOT_CONDITIONAL",
    "S": "SPLIT_SAMPLE_CONDITIONAL",
    "C": "COUNTRY_CONDITIONAL",
}

SOURCE_OWNER = {
    "W01": {
        "authority_code": "B03-W01",
        "source_path": "RETURN/O06_IMPLEMENTATION_ROUTING.jsonl",
        "source_return_sha256": "6809a1b4f39304ae779786e3b339420404ad4c57d27e8d26c7da1e9cd1c59533",
        "library_file_id_reference_only": "file_00000000ae5c822fb3b4c39ca262132e",
    },
    "W02": {
        "authority_code": "B03-W02",
        "source_path": "RETURN_U1/O06_IMPLEMENTATION_ROUTING.jsonl",
        "source_return_sha256": "0acde5f2a1d76b32f2dbf37fd8efadebe7e67485d3143fa01cd5ef213ef742ad",
        "library_file_id_reference_only": "file_000000007a2881f981c49a6914a8804d",
    },
}


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def sorted_stream_sha(ids: list[str]) -> str:
    return sha_bytes(("\n".join(sorted(ids)) + "\n").encode("utf-8"))


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def adjudicate(b03_root: Path) -> tuple[dict, dict, dict]:
    if len(TARGET_IDS) != 55 or len(set(TARGET_IDS)) != 55:
        raise AssertionError("target list must be exactly 55 unique qids")
    if sorted_stream_sha(TARGET_IDS) != EXPECTED_TARGET_STREAM_SHA256:
        raise AssertionError("target stream does not match EE-R2D frozen GSS batch")

    base = b03_root / B03_REL
    proof = json.loads((base / "CURRENT_REBIND_PROOF.json").read_text(encoding="utf-8"))
    if proof["bounded_current_family_slice"]["families"]["GSS"] != 6021:
        raise AssertionError("unexpected B03 GSS current-family slice")
    if proof["bounded_current_family_slice"]["exact_source_substrate_matches"] != 9464:
        raise AssertionError("unexpected B03 exact-source-substrate match count")

    ledger = load_csv(base / "EXACT_REF_LEDGER.csv")
    ledger_by_role = {row["role"]: row for row in ledger}
    for worker, owner in SOURCE_OWNER.items():
        row = ledger_by_role.get(worker)
        if not row:
            raise AssertionError(f"missing exact ref ledger row {worker}")
        if row["sha256_or_commit"] != owner["source_return_sha256"]:
            raise AssertionError(f"source return hash drift for {worker}")
        if row["identity_or_path"] != owner["library_file_id_reference_only"]:
            raise AssertionError(f"source return identity drift for {worker}")

    native: dict[str, dict[str, str]] = {}
    native_source_files: dict[str, str] = {}
    for path in sorted(base.glob("NATIVE_CURRENT_REBIND_*.csv")):
        native_source_files[path.name] = file_sha(path)
        for row in load_csv(path):
            qid = row["qid"]
            if qid not in TARGET_IDS or row["worker"] not in SOURCE_OWNER:
                continue
            if qid in native:
                raise AssertionError(f"duplicate native target qid: {qid}")
            if row["s"] not in STATUS_MEANING:
                raise AssertionError(f"unknown B03 status code {row['s']} for {qid}")
            native[qid] = {**row, "rebind_shard": path.name}

    derivative_path = base / "DERIVATIVE_ONLY_CURRENT_REBIND.csv"
    derivative_hits: dict[str, dict[str, str]] = {}
    for row in load_csv(derivative_path):
        qid = row["qid"]
        if qid in TARGET_IDS and row["worker"] in SOURCE_OWNER:
            derivative_hits[qid] = row
    overlap = set(native) & set(derivative_hits)
    if overlap:
        raise AssertionError(f"native/derivative target overlap: {sorted(overlap)}")

    rulings: list[dict] = []
    positives: list[dict] = []
    for qid in sorted(TARGET_IDS):
        if qid in native:
            row = native[qid]
            owner = SOURCE_OWNER[row["worker"]]
            ruling = {
                "question_implementation_id": qid,
                "routing_disposition": "APPLICABLE_OR_CURRENT_ROUTING_REF_BOUND",
                "authority_code": owner["authority_code"],
                "b03_worker": row["worker"],
                "native_status_code": row["s"],
                "native_status_meaning": STATUS_MEANING[row["s"]],
                "basis": "EXACT_QID_BOUND_B03_NATIVE_CURRENT_REBIND__AFFIRMATIVE_NATIVE_SOURCE_FINDING",
                "authority_refs": {
                    "b03_commit": B03_COMMIT,
                    "rebind_shard": str(B03_REL / row["rebind_shard"]),
                    "source_owner_path": owner["source_path"],
                    "source_return_sha256": owner["source_return_sha256"],
                    "source_return_library_file_id_reference_only": owner["library_file_id_reference_only"],
                },
            }
            rulings.append(ruling)
            positives.append({
                "question_implementation_id": qid,
                "routing_disposition": ruling["routing_disposition"],
                "routing_authority_code": owner["authority_code"],
                "routing_binding_ref": {
                    "b03_commit": B03_COMMIT,
                    "source_return_sha256": owner["source_return_sha256"],
                    "native_status_code": row["s"],
                    "qid": qid,
                },
            })
        elif qid in derivative_hits:
            row = derivative_hits[qid]
            ruling = {
                "question_implementation_id": qid,
                "routing_disposition": "UNRESOLVED_ROUTING_APPLICABILITY_AUTHORITY",
                "authority_code": f"B03-{row['worker']}",
                "basis": "DERIVATIVE_ONLY_CURRENT_REBIND_QUARANTINED__NOT_NATIVE_AUTHORITY",
                "derivative_status_code": row.get("o06"),
                "authority_refs": {
                    "b03_commit": B03_COMMIT,
                    "derivative_quarantine": str(B03_REL / derivative_path.name),
                },
            }
            rulings.append(ruling)
        else:
            rulings.append({
                "question_implementation_id": qid,
                "routing_disposition": "UNRESOLVED_ROUTING_APPLICABILITY_AUTHORITY",
                "authority_code": None,
                "basis": "NO_QID_BOUND_AFFIRMATIVE_NATIVE_SOURCE_FINDING_ON_AUTHORIZED_REPO_SURFACE__ABSENCE_NOT_NEGATIVE_EVIDENCE",
                "authority_refs": {
                    "b03_commit": B03_COMMIT,
                    "native_rebind_surface": str(B03_REL / "NATIVE_CURRENT_REBIND_*.csv"),
                },
            })

    if len(rulings) != 55 or len({r["question_implementation_id"] for r in rulings}) != 55:
        raise AssertionError("court output must account for exactly 55 unique qids")
    if {r["question_implementation_id"] for r in rulings} != set(TARGET_IDS):
        raise AssertionError("court output target set mismatch")

    counts = {
        "input_rows": 55,
        "applicable_or_current_routing_ref_bound": len(positives),
        "unresolved_routing_applicability_authority": 55 - len(positives),
        "derivative_only_quarantined_within_unresolved": len(derivative_hits),
    }

    per_id = {
        "schema": "RAWLSING_EE_R3C_GSS_ROUTING_AUTHORITY_RULINGS@1.0.0",
        "worker": "EE-R3C",
        "grain": "ADJUDICATE_ONLY_THE_55_GSS_IDS_IN_EE_R2D_BATCH_EE_R2D_B01_GSS_B03_SOURCE_SUBSTRATE",
        "input_authority": {
            "ee_r2d_commit": EE_R2D_COMMIT,
            "unit_id": "EE-R2D-B01-GSS-B03-SOURCE-SUBSTRATE",
            "sorted_id_stream_sha256": EXPECTED_TARGET_STREAM_SHA256,
            "rows": 55,
        },
        "source_authority": {
            "b03_commit": B03_COMMIT,
            "owners": SOURCE_OWNER,
            "current_rebind_proof_sha256": file_sha(base / "CURRENT_REBIND_PROOF.json"),
            "exact_ref_ledger_sha256": file_sha(base / "EXACT_REF_LEDGER.csv"),
            "native_rebind_shards": native_source_files,
            "derivative_quarantine_sha256": file_sha(derivative_path),
            "library_access_used": False,
        },
        "law": [
            "EXACT_QID_MATCH_ONLY",
            "AFFIRMATIVE_NATIVE_SOURCE_FINDING_MAY_BIND_ROUTING_REF",
            "DERIVATIVE_ONLY_NE_NATIVE_AUTHORITY",
            "ABSENCE_FROM_AFFIRMATIVE_LEDGER_NE_NEGATIVE_ROUTING_EVIDENCE",
            "UNRESOLVED_NE_NONAPPLICABLE",
            "NO_INFERENCE_FROM_LABEL_NUMBERING_ADJACENCY_MISSINGNESS_STATISTICS_OR_RESEMBLANCE",
        ],
        "counts": counts,
        "rulings": rulings,
    }

    objectizer = {
        "schema": "RAWLSING_EE_R3C_OBJECTIZER_READY_ROUTING_SUBSET@1.0.0",
        "worker": "EE-R3C",
        "source_rulings_schema": per_id["schema"],
        "rows": len(positives),
        "objects": positives,
        "law": "ONLY_EXACT_QID_BOUND_POSITIVE_KNOWN_RULINGS_INCLUDED__UNRESOLVED_EXCLUDED",
    }

    first_rulings_sha = sha_bytes(canonical_bytes(per_id))
    first_objectizer_sha = sha_bytes(canonical_bytes(objectizer))
    replay = {
        "schema": "RAWLSING_EE_R3C_REPLAY_RECEIPT@1.0.0",
        "worker": "EE-R3C",
        "result": "PASS",
        "target_rows": 55,
        "target_unique_ids": 55,
        "target_sorted_id_stream_sha256": sorted_stream_sha(TARGET_IDS),
        "expected_target_sorted_id_stream_sha256": EXPECTED_TARGET_STREAM_SHA256,
        "counts": counts,
        "rulings_canonical_sha256": first_rulings_sha,
        "objectizer_ready_canonical_sha256": first_objectizer_sha,
        "authority_checks": {
            "b03_gss_current_family_rows": proof["bounded_current_family_slice"]["families"]["GSS"],
            "b03_exact_source_substrate_matches": proof["bounded_current_family_slice"]["exact_source_substrate_matches"],
            "w01_source_return_sha256_exact": True,
            "w02_source_return_sha256_exact": True,
            "library_used": False,
            "no_non_gss_owner_used": all(r.get("b03_worker") in (None, "W01", "W02") for r in rulings),
            "zero_rows_outside_frozen_55": True,
        },
        "replay_law": "DETERMINISTIC_STD_LIB_INTERSECTION_OVER_PINNED_B03_COMMIT_AND_FROZEN_55_ID_STREAM",
    }
    return per_id, objectizer, replay


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--b03-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    first = adjudicate(args.b03_root)
    second = adjudicate(args.b03_root)
    for a, b in zip(first, second):
        if canonical_bytes(a) != canonical_bytes(b):
            raise AssertionError("second replay differs from first")

    per_id, objectizer, replay = first
    replay["second_replay_identical"] = True
    replay["terminal"] = (
        "PASS__EE_R3C_EXACT_55_ACCOUNTED__POSITIVE_NATIVE_BINDINGS_"
        f"{per_id['counts']['applicable_or_current_routing_ref_bound']}__UNRESOLVED_"
        f"{per_id['counts']['unresolved_routing_applicability_authority']}__ZERO_INFERENCE"
    )

    args.out.mkdir(parents=True, exist_ok=True)
    outputs = {
        "01_PER_ID_RULINGS.json": per_id,
        "02_OBJECTIZER_READY_SUBSET.json": objectizer,
        "03_REPLAY_RECEIPT.json": replay,
    }
    for name, value in outputs.items():
        (args.out / name).write_bytes(canonical_bytes(value))

    manifest = {
        "schema": "RAWLSING_EE_R3C_GENERATED_MANIFEST@1.0.0",
        "files": {
            name: {"bytes": (args.out / name).stat().st_size, "sha256": file_sha(args.out / name)}
            for name in sorted(outputs)
        },
        "terminal": replay["terminal"],
    }
    (args.out / "04_GENERATED_MANIFEST.json").write_bytes(canonical_bytes(manifest))
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
