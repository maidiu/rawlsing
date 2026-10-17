"""Build the F6N Phase-A case oracle from the frozen F6L worlds."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

RET = Path(__file__).resolve().parents[2]
F6L = RET / "01_INHERITED_F6L"
sys.path.insert(0, str(F6L / "02_PHASE_A/03_SCRIPTS"))
sys.path.insert(0, str(RET / "02_PHASE_A/03_SCRIPTS"))

import f6l_expectations as E  # noqa: E402
import f6n_worlds as N  # noqa: E402
import f6l_worlds as W  # noqa: E402

OUT = RET / "02_PHASE_A/01_FROZEN_CONSUMER_CASES.json"


def main():
    rare = N.rare_renormalization(150)
    positive = N.positive_world()
    cases = {
        "schema": "PYAT_R29_F6N_FROZEN_CONSUMER_CASES@1",
        "role": "independent F6L scientific-review continuation; NOT F6M/F6C author or HQ",
        "sealed_startup": "44700b0445673fad11c4f9779345d2920aeddd56",
        "inherited_f6l_tip": "6060adfac10f80020ed8e52cf2736467112d57c1",
        "inherited_f6l_oracle_sha256": hashlib.sha256(
            (F6L / "02_PHASE_A/01_WORLDS_AND_EXACT_EXPECTATIONS.json").read_bytes()
        ).hexdigest(),
        "native_under_test": {
            "producer_blob": "fc5e37fa5b2f0eb689593b42d95479d1327cb94c",
            "source_commit": "1428c2e92bce1a49efd87378cb23df936d646dc5",
            "method": "PRE553_TARGET_JOINT_STANDARDIZATION@1",
        },
        "ordering_attestation": {
            "f6m_candidate_read_before_this_freeze": False,
            "f6m_report_read_before_this_freeze": False,
            "f6l_phase_a_preserved": True,
            "f6j_freeze_preserved": True,
        },
        "cases": [
            {
                "id": "N1_RARE_CATEGORY_RENORMALIZATION",
                "world_id": rare["world_id"],
                "question": "A rare-category source is excluded by aggregate support. Does the producer avoid a false complete S2-only population estimate?",
                "expected_safe": "candidate.distribution is None, or uncovered_target_mass > 0, or a typed partial/no-complete decision; R1 exclusion remains visible; no complete renormalized population point",
                "expected_actual_pre_repair": {
                    "decision": "SYNTHETIC_CANDIDATE",
                    "candidate_distribution_present": True,
                    "uncovered_target_mass": "0",
                    "excluded_source": "R1",
                    "s2_only_distribution": ["1/8", "1/8", "1/8", "1/8", "1/4", "1/4"],
                },
                "expected_actual_is_unsafe": True,
            },
            {
                "id": "N2_SCOPE_RISK_SUBSTITUTION",
                "world_id": "F6N_SCOPE_MISMATCH",
                "question": "A source population scope substituted away from the target must produce a typed source-indexed refusal, not a complete target joint.",
                "expected_safe": "decision SOURCE_INDEXED_BACKOFF; candidate None; refusal TARGET_SCOPE_MISMATCH; no supported target joint",
                "expected_actual_pre_repair": {
                    "decision": "SOURCE_INDEXED_BACKOFF",
                    "candidate_none": True,
                    "refusal": "TARGET_SCOPE_MISMATCH",
                },
                "expected_actual_is_unsafe": False,
            },
            {
                "id": "N3_MAPPING_HASH_SUBSTITUTION",
                "world_id": "F6N_MAPPING_HASH_SUBSTITUTION",
                "question": "Changing source mapping material while leaving the policy mapping hash stale must refuse the source.",
                "expected_safe": "decision SOURCE_INDEXED_BACKOFF; candidate None; MAPPING_REVIEW_PREIMAGE_MISMATCH; no supported target joint",
                "expected_actual_pre_repair": {
                    "decision": "SOURCE_INDEXED_BACKOFF",
                    "candidate_none": True,
                    "refusal": "MAPPING_REVIEW_PREIMAGE_MISMATCH",
                },
                "expected_actual_is_unsafe": False,
            },
            {
                "id": "N4_PRODUCT_REF_SUBSTITUTION",
                "world_id": "F6N_PRODUCT_REF_SUBSTITUTION",
                "question": "A same-cardinality product_ref swap between two sources must bind each measured parent identity to the current source, not a stale identity.",
                "expected_safe": "measured_parent_ref follows the substituted product_ref; baseline input_hash equals semantic_hash(current source); content hash changes versus pristine",
                "expected_actual_pre_repair": {
                    "measured_parent_refs": ["F6L_PRODUCT_S2", "F6L_PRODUCT_S1"],
                    "input_hashes_match_current_sources": True,
                    "content_hash_changes": True,
                },
                "expected_actual_is_unsafe": False,
            },
            {
                "id": "N5_DUPLICATE_SOURCE_IDENTITY",
                "world_id": "F6N_DUPLICATE_SOURCE_IDENTITY",
                "question": "Two sources with the same product/survey/sample identity must be refused as a duplicate sample.",
                "expected_safe": "decision SOURCE_INDEXED_BACKOFF; candidate None; overlap reason DUPLICATE_SAMPLE; no supported target joint",
                "expected_actual_pre_repair": {
                    "decision": "SOURCE_INDEXED_BACKOFF",
                    "candidate_none": True,
                    "overlap_reason": "DUPLICATE_SAMPLE",
                },
                "expected_actual_is_unsafe": False,
            },
            {
                "id": "N6_PRODUCER_HASH_SUBSTITUTION_GUARD",
                "world_id": "PRODUCER_IDENTITY_GUARD",
                "question": "A one-byte producer mutation must be detectable by an independent blob/hash guard before import.",
                "expected_safe": "guard accepts the exact pinned producer and rejects a mutated copy; no mutated producer is executed",
                "expected_actual_pre_repair": {
                    "guard_accepts_pinned": True,
                    "guard_rejects_mutated": True,
                },
                "expected_actual_is_unsafe": False,
            },
            {
                "id": "N7_MACHINE_INDEPENDENT_STAGING",
                "world_id": "F6N_POSITIVE_COMPLETE_SOURCEFREE",
                "question": "The same pinned source and worlds copied to two independent relative roots must produce the same content hash.",
                "expected_safe": "two subprocess roots import their own producer and produce byte-identical content_hash; no machine-absolute symlink",
                "expected_actual_pre_repair": {
                    "content_hashes_equal": True,
                    "symlink_free_stage": True,
                },
                "expected_actual_is_unsafe": False,
            },
            {
                "id": "N8_POSITIVE_COMPLETE_SOURCEFREE",
                "world_id": "F6N_POSITIVE_COMPLETE_SOURCEFREE",
                "question": "A valid complete sourcefree target world must remain an exact complete positive with a usable consumer.",
                "expected_safe": "distribution present; sum 1; exact joint 1/3,1/6,1/6,1/3; conditional P(YES|LOW)=1/3; decision complete",
                "expected_actual_pre_repair": {
                    "distribution_present": True,
                    "joint": ["1/3", "1/6", "1/6", "1/3"],
                    "conditional_yes_given_low": "1/3",
                    "decision": "SYNTHETIC_CANDIDATE",
                },
                "expected_actual_is_unsafe": False,
            },
        ],
        "decision_law": {
            "complete_token_only_when": "candidate.distribution is not None and uncovered_target_mass == 0",
            "incomplete_tokens": ["PARTIAL", "NO_COMPLETE", "INCOMPLETE", "BACKOFF", "UNIDENTIFIED"],
            "test_only_never_real_use": True,
            "no_new_original_source_right": True,
        },
    }
    text = json.dumps(cases, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print("wrote", OUT, "sha256", hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()
