#!/usr/bin/env python3
"""Build the A41 receipt bank from REAL banked producer evidence.

Every artifact listed here is read back through ``git`` at its exact commit and
re-hashed; the builder refuses to emit a receipt whose preimage does not verify.
No fixture PASS metadata is invented. Occupancy kinds are honest and
non-substitutable: a sourcefree local positive never claims original occupancy.

Usage (from the A41 return root):
    python3 scripts/build_receipt_bank.py [--repo REPO_ROOT]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RETURN_ROOT = HERE.parent
sys.path.insert(0, str(RETURN_ROOT))

from a41.gitpreimage import GitPreimage, PreimageError  # noqa: E402
from a41 import receipt_bank  # noqa: E402

ALL_WAVES = [f"SRC{i:02d}" for i in range(1, 36)]

# (receipt_id, kind, commit, occupancy_kind, claim_id, claim_grain, evidence_state,
#  proof_grade, wave_ids, axis_ids, register_ids, ledger_ids, global_relations,
#  grain_note, method_source, limitations, downstream_consumer_refs, artifacts)
DECLARATIONS = [
    {
        "receipt_id": "O35B-ORIGINAL35-ACCOUNTING",
        "receipt_kind": "ORIGINAL35_ESTATE_ACCOUNTING",
        "commit": "c714af26a5a749706c6da06df40ac0ef026c6296",
        "return_ref": "WORKER_RETURNS/PYAT-R40-O35B-ORIGINAL35-AUTHORITY-OPERATION-BINDING-R1",
        "claim_id": "O35B_ALL35_NO_DROP_IDENTITY_AND_HELD_ACCOUNTING",
        "claim_grain": "whole-estate identity census and held-unit accounting",
        "occupancy_kind": "DOCUMENTARY_IDENTITY_RECONCILIATION",
        "evidence_state": "EXECUTED_GREEN",
        "proof_grade": "METADATA_ACCOUNTING_EDGE_PROVED__NOT_ORIGINAL_EXECUTION",
        "producer_inputs": ["original P2 master", "original O35E matrix", "P10 frozen census"],
        "releases": [],
        "downstream_consumer_read_refs": [],
        "native_test_ref": "evidence/o35b_junit.xml (27 new + 93 unchanged native)",
        "replay_ref": "independently frozen expected ledger sha256 2f3f40fcdb49bc7f558d0958b23983897910ecf3503a24efea43f394e33b6ffd",
        "method_source": "direct P2 vs O35E identity reconciliation + declared held accounting",
        "unknown_bounds": {
            "issued_eligible_operation_count": None,
            "reason": "null with cause: original35 source/operation use not issued",
            "permitted_current_original35_source_rights": 0,
        },
        "coverage": {
            "wave_ids": ALL_WAVES,
            "axis_ids": ["S01", "S02"],
            "register_151_ids": ["G001"],
            "ledger_101_ids": ["G01"],
            "global_relations": [],
            "occupancy_grain_note": (
                "identity/accounting reconciliation for all 35 waves at source identity and "
                "release axes only; NOT original measured occupancy"),
        },
        "limitations": [
            "18,276 P2 vs 18,259 active O35E, 18,250 common, 26 P2-only (6 carrier/admin + 20 substantive), 9 O35E-only",
            "127,813 candidate profile units HELD, not issued E_pre; eligible count null not zero",
            "the 20 substantive P2-only identities are NOT automatically eligible operations",
        ],
        "artifacts": [
            "WORKER_RETURNS/PYAT-R40-O35B-ORIGINAL35-AUTHORITY-OPERATION-BINDING-R1/00_RETURN.md",
            "WORKER_RETURNS/PYAT-R40-O35B-ORIGINAL35-AUTHORITY-OPERATION-BINDING-R1/evidence/owner_binding_audit.json",
            "WORKER_RETURNS/PYAT-R40-O35B-ORIGINAL35-AUTHORITY-OPERATION-BINDING-R1/evidence/P10_frozen_census.csv",
        ],
    },
    {
        "receipt_id": "O35B-C11-REPLAY-BLOCKER",
        "receipt_kind": "DEVELOPMENT_BLOCKER",
        "commit": "c714af26a5a749706c6da06df40ac0ef026c6296",
        "return_ref": "WORKER_RETURNS/PYAT-R40-O35B-ORIGINAL35-AUTHORITY-OPERATION-BINDING-R1",
        "claim_id": "O35B_EXACT_C11_REPLAY_PREREQUISITE_UNMET",
        "claim_grain": "exact original C11 validated release preimage",
        "occupancy_kind": "DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER",
        "evidence_state": "EXECUTED_GREEN__TYPED_BLOCKER",
        "proof_grade": "NARROW_OWNER_STOP_PROVED__NOT_COMPLETION",
        "producer_inputs": ["retained empirical closure (234 public objects)"],
        "releases": ["LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669"],
        "downstream_consumer_read_refs": [],
        "native_test_ref": "evidence/c11_block_boundary_recheck.junit.xml",
        "replay_ref": "semantic hash 192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f",
        "method_source": "native retention audit of the 15-section candidate validator preimages",
        "unknown_bounds": {
            "missing_sections": "carrier/internal record/event/routing/manifest preimages of the 15 native C11 SourceReleaseCandidate sections",
            "count_of_missing": None,
            "reason": "null with cause: exact section inventory owned by the custodian delivery",
        },
        "coverage": {
            "wave_ids": ALL_WAVES,
            "axis_ids": ["S19"],
            "register_151_ids": [],
            "ledger_101_ids": [],
            "global_relations": [],
            "occupancy_grain_note": (
                "narrow owner stop on the validated logical release axis; gates original "
                "I03/Batch replay for all 35 waves; NOT a global hold on E41/W41/P41/A41"),
        },
        "limitations": [
            "original I03/Batch replay and its execution-plan omission witness remain NOT_RUN",
            "no current original reconstruction source/host/purpose warrant observed",
            "do not dispatch a fourth repeat search/grammar archaeology",
        ],
        "artifacts": [
            "WORKER_RETURNS/PYAT-R40-O35B-ORIGINAL35-AUTHORITY-OPERATION-BINDING-R1/evidence/c11_retention_preimage_gap.json",
            "WORKER_RETURNS/PYAT-R40-O35B-ORIGINAL35-AUTHORITY-OPERATION-BINDING-R1/evidence/C11_REPLAY_CUSTODIAN_DELIVERY_REQUEST.json",
        ],
    },
    {
        "receipt_id": "O35B-P1-M1-NATIVE-BINDING",
        "receipt_kind": "PRODUCER_NATIVE_POSITIVE",
        "commit": "c714af26a5a749706c6da06df40ac0ef026c6296",
        "return_ref": "WORKER_RETURNS/PYAT-R40-O35B-ORIGINAL35-AUTHORITY-OPERATION-BINDING-R1",
        "claim_id": "O35B_THREE_NATIVE_FACTS_P1_TO_M1_ACTUAL_POSITIVE",
        "claim_grain": "retained native Fact objects bound through exact M1 authority resolution",
        "occupancy_kind": "SOURCEFREE_LOCAL_POSITIVE",
        "evidence_state": "EXECUTED_GREEN__CLAIM_EDGE_RED",
        "proof_grade": "CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED",
        "producer_inputs": ["3 permitted P1 Fact preimages", "one historical projection snapshot"],
        "releases": ["exact source release LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669"],
        "downstream_consumer_read_refs": ["M1 learned empirical adjudication"],
        "native_test_ref": "evidence/p1_corrected_projection_positive.junit.xml",
        "replay_ref": "evidence/p1_corrected_claim_receipt.json",
        "method_source": "exact retained Fact preimages + exact authority resolution + M1 binding repair",
        "unknown_bounds": {
            "original_exact_c11_replay": "HELD",
            "full35_competent_scientific_bindings": None,
            "reason": "null with cause: competent issuer decisions outstanding",
        },
        "coverage": {
            "wave_ids": ["SRC27"],
            "axis_ids": ["S16", "S24"],
            "register_151_ids": [],
            "ledger_101_ids": [],
            "global_relations": [],
            "occupancy_grain_note": (
                "sourcefree/retained positive on LiTS-family native Fact objects; "
                "original exact C11 replay HELD; NOT original measured occupancy"),
        },
        "limitations": [
            "joint-Fact severance produced the intended named assertion RED; byte-exact restoration GREEN",
            "does not prove an omission from an actual original I03/Batch execution plan",
            "the original-to-learned-consumer claim remains NOT_PROVED",
        ],
        "artifacts": [
            "WORKER_RETURNS/PYAT-R40-O35B-ORIGINAL35-AUTHORITY-OPERATION-BINDING-R1/evidence/p1_corrected_claim_receipt.json",
            "WORKER_RETURNS/PYAT-R40-O35B-ORIGINAL35-AUTHORITY-OPERATION-BINDING-R1/evidence/continuation_p1_M1_result.json",
        ],
    },
    {
        "receipt_id": "AS2B-LITS-HISTORICAL-POSITIVE",
        "receipt_kind": "HISTORICAL_SOURCE_POSITIVE",
        "commit": "c714af26a5a749706c6da06df40ac0ef026c6296",
        "return_ref": "WORKER_RETURNS/PYAT-R40-O35B-ORIGINAL35-AUTHORITY-OPERATION-BINDING-R1",
        "claim_id": "AS2B_LITS_HISTORICAL_SCOPED_POSITIVE",
        "claim_grain": "historical AS2B LiTS operation execution at historic scope",
        "occupancy_kind": "HISTORICAL_SCOPE_POSITIVE",
        "evidence_state": "HISTORICAL_EVIDENCE_PRESERVED__NOT_NEW_EXECUTION",
        "proof_grade": "HISTORICAL_GRADE_NOT_EQUIVALENT_TO_CURRENT_ORIGINAL_OCCUPANCY",
        "producer_inputs": ["historical AS2B execution log"],
        "releases": [],
        "downstream_consumer_read_refs": [],
        "native_test_ref": "evidence/AS2B_HISTORICAL_NOT_NEW_EXECUTION.csv",
        "replay_ref": "historical fact 516c1a8b1bfa2f84a39f0423220ecb37f8880e8916e961e61909f5cc933d7cd8 (5,155/5,155 support)",
        "method_source": "historical operation log, explicitly marked NOT new execution",
        "unknown_bounds": {
            "operations_executed": 8,
            "supported": 1,
            "unresolved": 6,
            "unavailable": 1,
            "unavailable_cause": "weight authority absent",
            "methods_typed_not_applicable": 4,
        },
        "coverage": {
            "wave_ids": ["SRC27"],
            "axis_ids": ["S15", "S20"],
            "register_151_ids": [],
            "ledger_101_ids": [],
            "global_relations": [],
            "occupancy_grain_note": (
                "historical scope only; one SUPPORTED operation with 5,155/5,155 support; "
                "no receipt relabelled as a new source execution"),
        },
        "limitations": [
            "historical grade is not equivalent to current original occupancy",
            "six UNRESOLVED and one UNAVAILABLE operation preserved as null/unresolved with cause",
        ],
        "artifacts": [
            "WORKER_RETURNS/PYAT-R40-O35B-ORIGINAL35-AUTHORITY-OPERATION-BINDING-R1/evidence/AS2B_HISTORICAL_NOT_NEW_EXECUTION.csv",
        ],
    },
    {
        "receipt_id": "E04L-SOURCEFREE-READTHROUGH",
        "receipt_kind": "CONSUMER_INTEGRATION_POSITIVE",
        "commit": "daf0d085e930696708c755e687879b155653c215",
        "return_ref": "WORKER_RETURNS/PYAT-R39-E04L-RELEASE-READTHROUGH-CONSUMER-R1",
        "claim_id": "E04L_SELECTED_RELEASE_READTHROUGH_TO_ORIGINAL_CONSUMER",
        "claim_grain": "unchanged original E04 NONPARENT_OPTIONS consumer reads selected learned release",
        "occupancy_kind": "SOURCEFREE_LOCAL_POSITIVE",
        "evidence_state": "EXECUTED_GREEN__I2_ACCEPTED_TEST_ONLY",
        "proof_grade": "ASSERTION_EFFICACY_PROVED__TEST_ONLY",
        "producer_inputs": ["synthetic E04 world rows", "M1/M2/B5/I4 owner objects"],
        "releases": ["B5 current-selected exact M2 release"],
        "downstream_consumer_read_refs": ["product.nonparent.consume"],
        "native_test_ref": "evidence/final_court.xml (22 new + 7 original native)",
        "replay_ref": "two cold interpreters, byte-identical native capture",
        "method_source": "TEST_ONLY service adapter resolving live B5/M2/I4 + producer-owned fact objects",
        "unknown_bounds": {
            "route_probability": None,
            "reason": "null with cause: NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL",
        },
        "coverage": {
            "wave_ids": [],
            "axis_ids": ["S24", "S29"],
            "register_151_ids": [],
            "ledger_101_ids": [],
            "global_relations": [],
            "occupancy_grain_note": (
                "SOURCEFREE TEST_ONLY method/owner local positive on a synthetic world; "
                "occupies NO original35 per-wave cell; SOURCEFREE_LOCAL_PASS != ORIGINAL_ESTATE_OCCUPANCY"),
        },
        "limitations": [
            "synthetic fixture source and fixture lifecycle; no real source/clock, no all-35",
            "the selected release is an authorization/binding gate over producer-owned fact objects, not an inlined payload",
            "not a real-source or all35 grant",
        ],
        "artifacts": [
            "WORKER_RETURNS/PYAT-R39-E04L-RELEASE-READTHROUGH-CONSUMER-R1/readthrough.py",
            "WORKER_RETURNS/PYAT-R39-E04L-RELEASE-READTHROUGH-CONSUMER-R1/test_readthrough_consumer.py",
            "WORKER_RETURNS/PYAT-R39-E04L-RELEASE-READTHROUGH-CONSUMER-R1/evidence/proof_witness.json",
        ],
    },
    {
        "receipt_id": "F6P-SOURCEFREE-PARTIAL-BOUND",
        "receipt_kind": "CONSUMER_INTEGRATION_POSITIVE",
        "commit": "912467aaacb715fd6e80ebc8c2bdd7285c26120b",
        "return_ref": "WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1",
        "claim_id": "F6P_F6M_PARTIAL_BOUND_EVIDENCE_CONSUMER",
        "claim_grain": "bounded read-only F6 evidence consumer over the actual repaired F6M product",
        "occupancy_kind": "SOURCEFREE_LOCAL_POSITIVE",
        "evidence_state": "EXECUTED_GREEN__I2_ACCEPTED_TEST_ONLY",
        "proof_grade": "ASSERTION_EFFICACY_PROVED__TEST_ONLY",
        "producer_inputs": ["F6M blob 2df811d76db258d98d89ffb43c830cb221ff9a7d", "frozen W1/W2/W3/W7 world inputs"],
        "releases": ["F6M candidate bundle with content_hash replay identity"],
        "downstream_consumer_read_refs": ["consume_f6m_evidence"],
        "native_test_ref": "evidence/native_court.xml (32 native tests)",
        "replay_ref": "cold replay two hash seeds 32/32; restored post-gate cold court green",
        "method_source": "independent exact-rational recomputation of W1/W2/W3/W7 from frozen counts",
        "unknown_bounds": {
            "uncovered_target_mass_W2": "1/4",
            "uncovered_target_mass_W7": "1/2",
            "uncovered_target_mass_W3": "1/5",
            "route_probability": None,
            "reason": "null with cause: unknown mass preserved, never renamed to a point",
        },
        "coverage": {
            "wave_ids": [],
            "axis_ids": ["S26", "S28"],
            "register_151_ids": [],
            "ledger_101_ids": [],
            "global_relations": ["cross_family_F6"],
            "occupancy_grain_note": (
                "SOURCEFREE TEST_ONLY contribution to the global F6 relation at sourcefree grain; "
                "occupies NO original35 per-wave cell; no net F6M->original E04 join is claimed"),
        },
        "limitations": [
            "sourcefree TEST_ONLY; no transport/model-use permission",
            "C cross-channel native primitive NOT_RUN in the published tree",
            "A0 blob 182cc797 is historical negative control only, never comparison A",
        ],
        "artifacts": [
            "WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1/f6p_partial_bound_evidence_consumer.py",
            "WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1/tests/test_f6p_consumer.py",
            "WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1/evidence/proof_witness_receipt.json",
        ],
    },
    {
        "receipt_id": "I2-R39I-INDEPENDENT-COURT",
        "receipt_kind": "INDEPENDENT_REVIEW",
        "commit": "05c21c54c538d523965d0b312525224d4d2c2a0d",
        "return_ref": "WORKER_RETURNS/PYAT-R40-R39I-INDEPENDENT-REAL-CONSUMER-CLAIM-COURT-R1",
        "claim_id": "I2_R39I_ACCEPT_E04L_AND_F6P_SOURCEFREE_TEST_ONLY",
        "claim_grain": "independent arm's-length I2 claim-edge court over E04L and F6P",
        "occupancy_kind": "SOURCEFREE_LOCAL_POSITIVE",
        "evidence_state": "EXECUTED_GREEN__INDEPENDENT_ACCEPT",
        "proof_grade": "CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED",
        "producer_inputs": ["E04L return", "F6P return"],
        "releases": [],
        "downstream_consumer_read_refs": [],
        "native_test_ref": "evidence/logs/court_a_reviewer_fault_witness.json; court_b_reviewer_fault_witness.json",
        "replay_ref": "cold replay 29/29 (E04L) and 32/32 (F6P) under two hash seeds",
        "method_source": "reviewer-recomputed oracles from frozen source counts, independent of candidate output",
        "unknown_bounds": {"incremental_cash_cost": None, "reason": "null with cause: UNKNOWN"},
        "coverage": {
            "wave_ids": [],
            "axis_ids": [],
            "register_151_ids": [],
            "ledger_101_ids": ["A12"],
            "global_relations": [],
            "occupancy_grain_note": (
                "independent review grade only; accepts the two sourcefree TEST_ONLY claims at "
                "their exact grain and issues no source/world/model right"),
        },
        "limitations": [
            "accepts at source-free TEST_ONLY grain only",
            "F6P does not join to original E04 NONPARENT_OPTIONS; that residual is open",
            "four reviewer fault witnesses proved assertion-level RED and restoration",
        ],
        "artifacts": [
            "WORKER_RETURNS/PYAT-R40-R39I-INDEPENDENT-REAL-CONSUMER-CLAIM-COURT-R1/00_INDEPENDENT_REVIEW_VERDICTS.md",
            "WORKER_RETURNS/PYAT-R40-R39I-INDEPENDENT-REAL-CONSUMER-CLAIM-COURT-R1/evidence/logs/court_a_reviewer_fault_witness.json",
            "WORKER_RETURNS/PYAT-R40-R39I-INDEPENDENT-REAL-CONSUMER-CLAIM-COURT-R1/evidence/logs/court_b_reviewer_fault_witness.json",
        ],
    },
    {
        "receipt_id": "WV1-SOURCEFREE-WORLD-CONSUMPTION",
        "receipt_kind": "CONSUMER_INTEGRATION_POSITIVE",
        "commit": "23989684dd980efe49de9f2b21e15373ba58a709",
        "return_ref": "WORKER_RETURNS/PYAT-R40-WV1-COHERENT-SELECTED-WORLD-R1",
        "claim_id": "WV1_SELECTED_WORLD_DRIVES_ORIGINAL_E04_CONSUMER",
        "claim_grain": "original E04 NONPARENT_OPTIONS consumes a selected B5/M2/I4 two-epoch world",
        "occupancy_kind": "SOURCEFREE_LOCAL_POSITIVE",
        "evidence_state": "EXECUTED_GREEN__235_NATIVE_PASS",
        "proof_grade": "ASSERTION_EFFICACY_PROVED__THREE_LOAD_BEARING_MUTATION_REDS",
        "producer_inputs": ["T35 rule revisions", "M4/M5 selected-world owner", "R13 correction"],
        "releases": ["selected B5/M2/I4 learned release"],
        "downstream_consumer_read_refs": ["product.nonparent.consume", "proposal purpose"],
        "native_test_ref": "evidence/cold_replay.json (235 native PASS)",
        "replay_ref": "evidence/cold_replay.json",
        "method_source": "coherent selected-world composition over inherited T35/M4/M5/R13 owners",
        "unknown_bounds": {
            "N9_SELECTED_WORLD_serving": "HOLD",
            "F6M_cross_source": None,
            "reason": "null with cause: F6M cross-source not admitted",
        },
        "coverage": {
            "wave_ids": [],
            "axis_ids": ["S29"],
            "register_151_ids": [],
            "ledger_101_ids": [],
            "global_relations": ["possibility_F8"],
            "occupancy_grain_note": (
                "sourcefree bounded nonparent positive and proposal purpose; "
                "R13 full N9_SELECTED_WORLD serving remains HOLD; occupies NO original35 per-wave cell"),
        },
        "limitations": [
            "sourcefree bounded; not a route model and no route probability",
            "F6M cross-source contribution not admitted into this world",
        ],
        "artifacts": [
            "WORKER_RETURNS/PYAT-R40-WV1-COHERENT-SELECTED-WORLD-R1/00_RETURN.md",
            "WORKER_RETURNS/PYAT-R40-WV1-COHERENT-SELECTED-WORLD-R1/evidence/cold_replay.json",
        ],
    },
    {
        "receipt_id": "EE1-SOURCEFREE-TEMPORAL-NULL",
        "receipt_kind": "TEMPORAL_METHOD_POSITIVE_WITH_NULL",
        "commit": "affe600d05073fd9ffbdb071af5762e48c76112e",
        "return_ref": "WORKER_RETURNS/PYAT-R40-EE1-HISTORICAL-SOURCE-QUALIFIED-TEMPORAL-METHOD-CONSUMER-R1",
        "claim_id": "EE1_INHERITED_V553_TEMPORAL_METHOD_WITH_GHANA_TREND_NULL",
        "claim_grain": "sourcefree historical-source-qualified temporal method and comparability discipline",
        "occupancy_kind": "EMPIRICAL_NULL_WITH_CAUSE",
        "evidence_state": "EXECUTED_GREEN__FOUR_ASSERTED_CONTROLS_RED",
        "proof_grade": "ASSERTION_EFFICACY_PROVED__NULL_PRODUCT",
        "producer_inputs": ["inherited V553 harmonisation/temporal method", "T35 rule revisions"],
        "releases": [],
        "downstream_consumer_read_refs": ["EE1 historical consumer"],
        "native_test_ref": "evidence/ee1-suite.xml (33 tests)",
        "replay_ref": "evidence/proof-gate-changed.json",
        "method_source": "inherited V553 temporal method with source/population comparability and time discipline",
        "unknown_bounds": {
            "measured_EE12_source": None,
            "ghana_trend": "NULL_WITH_CAUSE__HOLD",
            "reason": "null with cause: no measured EE12 source; trend not fabricated",
        },
        "coverage": {
            "wave_ids": [],
            "axis_ids": ["S27"],
            "register_151_ids": [],
            "ledger_101_ids": [],
            "global_relations": ["temporal_F7"],
            "occupancy_grain_note": (
                "sourcefree temporal method positive with an honest measured null (Ghana trend) "
                "and recorded cause; occupies NO original35 per-wave cell; no fabricated change"),
        },
        "limitations": [
            "no measured EE12 source; Ghana trend is a null with cause, not a change estimate",
            "comparability and time discipline sourcefree, not original measured",
        ],
        "artifacts": [
            "WORKER_RETURNS/PYAT-R40-EE1-HISTORICAL-SOURCE-QUALIFIED-TEMPORAL-METHOD-CONSUMER-R1/03_EE1_FUNCTIONAL_RESULTS_AND_GRADES.md",
            "WORKER_RETURNS/PYAT-R40-EE1-HISTORICAL-SOURCE-QUALIFIED-TEMPORAL-METHOD-CONSUMER-R1/evidence/proof-gate-changed.json",
        ],
    },
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=RETURN_ROOT.parents[1])
    ap.add_argument("--out", type=Path,
                    default=RETURN_ROOT / "evidence" / "receipt_bank_frozen.json")
    args = ap.parse_args()

    gp = GitPreimage(args.repo)
    receipts = []
    for decl in DECLARATIONS:
        artifacts = []
        for path in decl["artifacts"]:
            rec = gp.verify(decl["commit"], path)
            artifacts.append(rec)
        receipts.append({
            "schema": receipt_bank.RECEIPT_SCHEMA,
            "receipt_id": decl["receipt_id"],
            "receipt_kind": decl["receipt_kind"],
            "origin_commit": decl["commit"],
            "return_ref": decl["return_ref"],
            "claim_id": decl["claim_id"],
            "claim_grain": decl["claim_grain"],
            "occupancy_kind": decl["occupancy_kind"],
            "evidence_state": decl["evidence_state"],
            "proof_grade": decl["proof_grade"],
            "producer_inputs": decl["producer_inputs"],
            "releases": decl["releases"],
            "downstream_consumer_read_refs": decl["downstream_consumer_read_refs"],
            "native_test_ref": decl["native_test_ref"],
            "replay_ref": decl["replay_ref"],
            "method_source": decl["method_source"],
            "unknown_bounds": decl["unknown_bounds"],
            "coverage": decl["coverage"],
            "limitations": decl["limitations"],
            "currentness": {
                "archive_or_current": ("ARCHIVE"
                                       if decl["occupancy_kind"] == "HISTORICAL_SCOPE_POSITIVE"
                                       else "CURRENT"),
                "as_of": "2026-10-18T23:30:00-0400",
                "note": ("historical scope receipt retained as archive"
                         if decl["occupancy_kind"] == "HISTORICAL_SCOPE_POSITIVE"
                         else "current accepted bank receipt"),
            },
            "independent_u_e_pre_authority": decl.get("independent_u_e_pre_authority"),
            "artifacts": artifacts,
        })

    bank = {
        "schema": receipt_bank.BANK_SCHEMA,
        "receipts": receipts,
        "pending_slots": receipt_bank.PENDING_RETURN_SLOTS,
        "note": (
            "genuinely banked producer evidence at exact Git preimages; occupancy kinds are "
            "non-substitutable; no fixture PASS metadata; E41/W41/P41 slots reserved pending"),
    }
    bank["bank_digest"] = hashlib.sha256(
        json.dumps(bank, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    # Self-ingest to prove the bank is admissible before freezing.
    scope_path = RETURN_ROOT / "evidence" / "expected_scope_frozen.json"
    scope = json.loads(scope_path.read_text(encoding="utf-8"))
    result = receipt_bank.ingest_bank(bank, gp, expected_scope=scope)

    args.out.write_text(json.dumps(bank, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "out": str(args.out),
        "receipts": len(receipts),
        "ingested_verified": result["ingested_count"],
        "bank_digest": bank["bank_digest"],
        "occupancy_kind_counts": {
            k: sum(1 for r in receipts if r["occupancy_kind"] == k)
            for k in receipt_bank.OCCUPANCY_KINDS},
        "pending_slots": [s["slot_id"] for s in bank["pending_slots"]],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
