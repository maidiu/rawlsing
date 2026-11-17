#!/usr/bin/env python3
"""Build clean source-authenticated frame/decision/C fixtures for the D4A attack court."""
import hashlib, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SNAP = ROOT / "EVIDENCE" / "source_snapshot"
EV = ROOT / "EVIDENCE"
PKG = ROOT / "PACKAGE" / "ANVIL_R7_REPAIRED"
ZIP = "526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332"


def sha(b): return hashlib.sha256(b).hexdigest()


def ref(local, excerpt, commit=None, blob=None, git_path=None, klass="SUPPLIED_ZIP"):
    b = (SNAP / local).read_bytes()
    d = {"path": local, "sha256": sha(b), "exact_excerpt": excerpt, "source_class": klass}
    if commit:
        d.update(git_commit=commit, git_blob=blob, git_path=git_path)
    else:
        d["zip_sha256"] = ZIP
    return d


def main():
    inv_path = EV / "source_authenticated_inventory.json"
    inv = json.loads(inv_path.read_text())
    rel = {"schema": "ANVIL_R7_SOURCE_RELEASE_REGISTER",
           "status": "AUTHORED_LOCAL_REGISTER_NOT_OWNER_CURRENTNESS",
           "current": [
               {"name": "K3_PROTECTED_7FC", "sha256": sha((SNAP / "K3/K3_CONSERVATION_VS_IMPLEMENTATION_29.tsv").read_bytes())},
               {"name": "SEAM25", "sha256": sha((SNAP / "docs/SEAM25.md").read_bytes())},
               {"name": "SEAM26", "sha256": sha((SNAP / "docs/SEAM26.md").read_bytes())},
               {"name": "ANVIL15", "sha256": sha((SNAP / "docs/ANVIL15.md").read_bytes())},
               {"name": "SUPPLIED_ZIP", "sha256": ZIP},
           ],
           "revoked": [],
           "note": "No source/owner currentness is granted. This register only prevents silent use of a locally marked revoked pin."}
    (EV / "release_register.json").write_text(json.dumps(rel, indent=2, sort_keys=True) + "\n")

    k1 = inv["groups"]["K1_CAP"]["K1-CAP-01"]["source_anchor"]
    s01 = inv["groups"]["SEAM_S"]["S-01"]["source_anchor"]
    s03 = inv["groups"]["SEAM_S"]["S-03"]["source_anchor"]
    b04 = inv["groups"]["SEAM_B"]["B-04"]["source_anchor"]
    reqs = [
        {"id": "R1", "domain": "SOURCE_SEMANTICS", "binding": "PRESENT_HARD",
         "substantive_requirement": "Preserve exact native question, option, routing, occurrence and source identity semantics through source projection and C11.",
         "why_needed": "Without native semantics a later reader cannot distinguish asked, eligible, missing, released and recoded values.",
         "loss_if_missing": "The instrument would launder a convenience code as an original observation and destroy lawful negative evidence.",
         "first_consumer": "rawlsing_next/pre553_empirical_query.py::DirectEstateI03Session",
         "architectural_consequence": "C11 must retain exact source anchors and typed missing/routing states rather than a single normalized display value.",
         "proof_or_owner_hold": "Check exact K3 and SEAM source rows; no native source right is issued by this fixture.",
         "evidence": ref("docs/29.md", "source bytes/excerpt, real first consumer", klass="SUPPLIED_ZIP")},
        {"id": "R2", "domain": "C11_PERSISTENCE", "binding": "PRESENT_HARD",
         "substantive_requirement": "Retain one sealed canonical C11 authority with source-qualified body, typed projection and cold reopen rather than a rival respondent fact store.",
         "why_needed": "A second authority would make source provenance and revocation ambiguous across consumers.",
         "loss_if_missing": "Cold revocation, restore and consumer equivalence cannot be demonstrated or falsified.",
         "first_consumer": "rawlsing_next/pre553_c11_repository.py::VerifiedDirectEstate",
         "architectural_consequence": "The chosen physical layer must prove cold authenticated readback and exact negative/restore behavior.",
         "proof_or_owner_hold": "This is a design obligation; no native run or owner receiving is claimed.",
         "evidence": ref("docs/29.md", "catastrophic cold access?", klass="SUPPLIED_ZIP")},
        {"id": "R3", "domain": "CURRENT_I03_I05", "binding": "PRESENT_HARD",
         "substantive_requirement": "Serve respondent-coherent I03/I05 and F1-F4 reads for 1, 10 and 100 distinct operations without full-body replay per operation.",
         "why_needed": "The present empirical consumer cannot be replaced by identity strings or a static 118-row ledger.",
         "loss_if_missing": "Same-person joints, reverse denominators and minority patterns become unqueryable.",
         "first_consumer": "rawlsing_next/pre553_empirical_query.py::execute_empirical_query",
         "architectural_consequence": "Prepared selective access must preserve exact respondent identity and conditioned risk sets.",
         "proof_or_owner_hold": "Native/sourcefree execution and process-tree economics remain held; no result is asserted here.",
         "evidence": ref("docs/SEAM26.md", "1/10/100 distinct authorized wide queries", klass="SEAM_DOCUMENTARY", commit="796452b8cb788fa5a02f37a7ce86eafce8312dfe", blob="a05c21dd0b7b1d404fc500c0ef36c81aee67c96e", git_path="SEAM/26_CONDITIONED_SOCIAL_FIELD_IDENTIFICATION_AND_GENERATIVE_PERSON_REVERSE_CONTRACT_R1.md")},
        {"id": "R4", "domain": "HISTORICAL_DDM_FUNCTIONS", "binding": "PRESENT_HARD",
         "substantive_requirement": "Conserve V549/V550/V550J/F26 historical function, genuine same-person k>=3 joint, branch/route negatives and non-gating FAIL semantics.",
         "why_needed": "The original DDM was not failed work to be replaced; old carriers may change while function and negative survive.",
         "loss_if_missing": "The repair would silently reduce empirical analysis to pairwise marginals or resurrect known bugs.",
         "first_consumer": "Historical DDM conservation consumer, owner-held until a competent historical reader is named.",
         "architectural_consequence": "Old PostgreSQL layout need not survive; exact source semantics and negative evidence must.",
         "proof_or_owner_hold": "R5 is PREPARED / LOCALLY STRUCTURALLY TESTED / NOT DISPATCHED; no production claim.",
         "evidence": ref("docs/20_RECOVERY.md", "PREPARED / LOCALLY STRUCTURALLY TESTED / NOT DISPATCHED", klass="SUPPLIED_ZIP")},
        {"id": "R5", "domain": "F1_F4_ANALYTICS", "binding": "PRESENT_HARD",
         "substantive_requirement": "Support true same-person three-way and higher joint patterns with exact denominators, minority tails and typed missingness.",
         "why_needed": "Matching marginals can conceal different true three-way respondent patterns.",
         "loss_if_missing": "FF and later consumers would mistake a synthetic pairwise product for an observed configuration.",
         "first_consumer": "F1-F4 qualified consumer under the existing empirical owner.",
         "architectural_consequence": "The physical route must not collapse event identity or synthesize cross-survey links.",
         "proof_or_owner_hold": "No F4 native first reader is claimed by this authored fixture.",
         "evidence": ref("docs/SEAM26.md", "Exact respondent-coherent ordered k≥3 F4", klass="SEAM_DOCUMENTARY")},
        {"id": "R6", "domain": "FIELD_FORGE", "binding": "FUTURE_NONPRECLUSION",
         "substantive_requirement": "Permit differentiated social-field possibility across positions without inventing household, sect or ancestry observations.",
         "why_needed": "SEAM requires the complete conditional joint distribution of several positions, not a mode-only stereotype.",
         "loss_if_missing": "A later actor/world owner would receive fabricated encounter or identity claims.",
         "first_consumer": "Field Forge #1009 qualified descriptive recipient (owner-held).",
         "architectural_consequence": "C11 must preserve source-qualified position evidence and nonpooling; FF science stays separately owned.",
         "proof_or_owner_hold": "FF02 causal/material authority and encounter owner remain held.",
         "evidence": ref("docs/SEAM26.md", "Position-conditioned distributions", klass="SEAM_DOCUMENTARY")},
        {"id": "R7", "domain": "SEAM_WORLD_ACTOR", "binding": "EXTERNAL_OWNER_HELD",
         "substantive_requirement": "Keep observed survey answers, independently sourced material power, fictional world facts and actor knowledge as separate typed authorities.",
         "why_needed": "A survey response cannot become a private motive, institutional power or an actor's acquired knowledge.",
         "loss_if_missing": "The instrument could fabricate source-to-actor knowledge and erase the actor/world firewall.",
         "first_consumer": "SOROK #1011 / N11-N12 owner-held world and actor ingress.",
         "architectural_consequence": "The selected C11 design must preserve the boundary even while the downstream science is held.",
         "proof_or_owner_hold": "SOROK actor/consent/development owner; no actor grant is issued.",
         "authority_owner": "SOROK #1011 actor/consent/development owner",
         "evidence": ref("docs/SEAM25.md", "Who commits an **actual fictional household/person/world**", klass="SEAM_DOCUMENTARY")},
        {"id": "R8", "domain": "AUTHORITY_AND_RECOVERY", "binding": "PRESENT_HARD",
         "substantive_requirement": "Fail closed on stale or revoked release state and preserve exact positive, denied and restored consumer behavior.",
         "why_needed": "A producer and verifier agreeing on a hash does not prove the source is current or owner-authorized.",
         "loss_if_missing": "A revoked release could be replayed as current empirical evidence.",
         "first_consumer": "Cold authenticated C11 reader at the existing source/physical owner boundary.",
         "architectural_consequence": "Release pins and revocation witnesses must be explicit and checked before acceptance.",
         "proof_or_owner_hold": "No protected H1 or owner receiving is claimed.",
         "evidence": ref("docs/29.md", "No local H1 accreditation; protected CAS", klass="SUPPLIED_ZIP")},
        {"id": "R9", "domain": "RESOURCE_ECONOMICS", "binding": "PRESENT_HARD",
         "substantive_requirement": "Respect the existing six-GiB process-tree ceiling and account for cold, repeated, scratch and retained costs separately.",
         "why_needed": "A small sourcefree fixture at 3.245 events per respondent cannot establish a dense 600-1,300-slot workload.",
         "loss_if_missing": "A design could pass a toy test while failing the actual physical consumer.",
         "first_consumer": "Existing physical runner and cold-builder consumer under separately verified host rights.",
         "architectural_consequence": "Only matched, actually executed measurements may support a physical claim.",
         "proof_or_owner_hold": "No native 100k or 6-GiB proof is asserted by this return.",
         "evidence": ref("docs/29.md", "cold/repeated, heavy query, exact negative/replay and 6 GiB", klass="SUPPLIED_ZIP")},
    ]

    bc_doc = json.loads((SNAP / "package/02_BOUNDARY_CONTRACTS.json").read_text())
    boundary_claims = []
    for b in bc_doc["boundaries"]:
        boundary_claims.append({
            "id": b["id"], "producer": b["producers"], "receiver": b["receivers"],
            "must_preserve": b["must_preserve"], "expected_first_effect": b["first_effect"],
            "veto": b["veto"], "time_class": b["time_class"], "owner": b["owners"],
        })

    frame = {
        "schema": "ANVIL_R7_INTEGRATED", "stage": "COMMON_FRAME",
        "workflow": "ONE_INTEGRATED_INVESTIGATION_OPTIONAL_TARGETED_DUELS",
        "phase": "BEFORE_ARCHITECTURE_SELECTION",
        "architecture_selected": False, "mandatory_rival_architecture": False, "duel_required": False,
        "A_B_method": "OPTIONAL_SAME_QUESTION_SAME_EVIDENCE", "scope": "C11_QUERY_DESIGN",
        "source_cut": "31291d08179890852246c8742700e055168e9933",
        "protected_head": "31291d08179890852246c8742700e055168e9933",
        "user_priority_source": "Pinned D4A controller instruction: repair the ANVIL decision instrument, not the physical architecture; retain exact source/negative/consumer accounting.",
        "first_real_consumer": "rawlsing_next/pre553_empirical_query.py::DirectEstateI03Session (current code), with future SOROK #1011 separately owner-held.",
        "currentness_gap_or_exact_verified_state": "Protected source bytes are verified locally at the stated Git/ZIP pins; live GitHub state, owner leases and native source rights are not authenticated.",
        "science_authority_boundary": "No survey answer becomes private motive, institutional power, fictional fact or actor knowledge without a separate competent owner.",
        "whole_program_mission": "Conserve the mixed 118 identity universe, eliminate the false accepted-SPINE dependency, and expose T1-T7 and actual first consumers honestly.",
        "source_currentness": "K3 7fc, SEAM25 596f, SEAM26 7964, ANVIL15 3cc0 and supplied ZIP 526d are exact local snapshot pins; live currentness remains a hold.",
        "source_grades_authentic_by_local_test": False,
        "requirements": reqs,
        "historical_inventory": {"path": "source_authenticated_inventory.json", "sha256": sha(inv_path.read_bytes())},
        "release_register": {"path": "release_register.json", "sha256": sha((EV / "release_register.json").read_bytes())},
        "boundary_contract": {"path": "source_snapshot/package/02_BOUNDARY_CONTRACTS.json", "sha256": sha((SNAP / "package/02_BOUNDARY_CONTRACTS.json").read_bytes())},
        "boundary_contracts": boundary_claims,
    }
    (EV / "frame.json").write_text(json.dumps(frame, indent=2, sort_keys=True) + "\n")

    # 118 identity dispositions
    hd = []
    for group, recs in inv["groups"].items():
        for rid, rec in recs.items():
            a = rec["source_anchor"]
            ev = {"path": a["path"], "sha256": a["sha256"], "exact_excerpt": a["exact_excerpt"], "source_class": a["source_class"]}
            if a.get("git_commit"):
                ev.update(git_commit=a["git_commit"], git_blob=a["git_blob"], git_path=a["git_path"])
            else:
                ev["zip_sha256"] = a["zip_sha256"]
            if group == "PYAT_PC":
                st = "NOT_ADOPTED"
            elif group == "P4R":
                st = "PROOF_HELD"
            elif group == "K1_CAP":
                st = "CONSERVED"
            elif group == "TERMINAL":
                st = "IDENTITY_ONLY"
            else:
                st = "FUTURE_NONPRECLUDED"
            hd.append({"id": rid, "disposition": st, "negative_preserved": True,
                       "consumer": rec["consumer_or_hold"][:300], "evidence": ev})

    decision = {
        "schema": "ANVIL_R7_INTEGRATED", "stage": "INTEGRATED_DECISION",
        "common_frame": {"path": "frame.json", "sha256": sha((EV / "frame.json").read_bytes())},
        "frame_sha256": None,
        "decision_process": "ONE_SYNTHESIS_NO_MANDATORY_RIVAL",
        "basis": "ANALYTICAL_SOURCE_GROUNDED", "grade": "AUTHOR_PROPOSED_PENDING_C",
        "architecture_description": "Retain one canonical C11 authority and add only a source-authenticated identity inventory plus release/boundary guards; no physical architecture is selected.",
        "entire_source_to_actor_dataflow": "Original source rows -> sealed C11 -> I03/I05/F1-F4 -> qualified FF possibility; actor/world remains a separate owner-held boundary and is never written by survey data.",
        "algorithm_and_data_structures": "Exact K3 TSV rows, SEAM/ANVIL documentary rows, T1-T7 contracts and terminal identities keyed by content hash; no synthetic R5/R6 SPINE is manufactured.",
        "resource_cost_reasoning": "The inventory is a small source index; the actual C11/I03 physical costs remain unmeasured and cannot be inferred from this authored fixture.",
        "historical_function_conservation": "All 118 identities are present; 69 K3 rows have exact row bytes; 26 proposals remain NOT_ADOPTED; 14 proofs remain HELD; terminal IDs are identity-only.",
        "scientific_boundary_and_nonpreclusion": "SEAM/T5-T7 and SOROK actor science remain owner-held; the decision claims no survey-to-actor knowledge or material power.",
        "strongest_surviving_objection": "A source-authenticated identity inventory still cannot prove that a future C11 implementation preserves the required query semantics at dense workload scale.",
        "why_selected_over_feasible_alternatives": "The accepted-SPINE dependency is factually unavailable and invites synthetic laundering; a bounded source inventory plus explicit owner holds is the strongest honest alternative.",
        "next_actual_engineering_operation": "Have a qualified source owner authenticate the K3/SEAM snapshot and then test the current C11 consumer on a matched dense workload; do not claim readiness from this local fixture.",
        "single_selected_strategy": "Source-authenticated 118 identity inventory with explicit owner holds",
        "first_real_consumer": frame["first_real_consumer"],
        "alternatives_considered": [
            {"technical_approach": "Wait for or reconstruct an accepted R5/R6 SPINE.json", "state": "RULED_OUT_BY_REASON",
             "why_not_selected_or_held": "No such accepted artifact exists in the supplied package or exact Git cuts; using a synthetic spine would launder fabricated semantics as historical conservation."},
            {"technical_approach": "Drop the 118 accounting and design only the physical C11 path", "state": "RULED_OUT_BY_REASON",
             "why_not_selected_or_held": "That directly loses the inherited identity/negative/consumer obligations and cannot answer the pair question."}
        ],
        "choice_reversers": [{"status": "RESOLVED_AT_ANALYTICAL_SCOPE", "question": "Can the 118 mixed identities be sourced without an accepted SPINE?"}],
        "requires_full_A_B_comparison": False, "competing_implementations_mandatory": False,
        "architecture_claims_independent_acceptance": False, "targeted_duel": None,
        "historical_identity_dispositions": hd,
        "actor_world_boundary": {"survey_implies_actor_knowledge": False, "fictional_mutates_source": False,
                                  "source_implies_material_power": False,
                                  "owner_held_instead": "SOROK #1011 / N11-N12 owner-held; no actor or material-power grant issued."},
        "protected_h1_claimed": False, "source_authentication_claimed": False,
        "requirement_dispositions": [],
    }
    for r in reqs:
        state = "FUTURE_NONPRECLUDED" if r["binding"] == "FUTURE_NONPRECLUSION" else ("EXACT_OWNER_HOLD" if r["binding"] == "EXTERNAL_OWNER_HELD" else "PRESENT_PRESERVED")
        grade = "DOCUMENTARY"
        decision["requirement_dispositions"].append({
            "requirement_id": r["id"], "disposition": state, "evidence_grade": grade,
            "actual_design_effect": "Retain the exact source/negative/consumer obligation and mark the physical or owner proof still missing.",
            "specific_first_consumer_path": r["first_consumer"],
            "conservation_or_refusal_witness": "The exact source pin is named; no native execution or owner acceptance is claimed by this authored fixture.",
            "evidence": r["evidence"],
        })
    # frame digest
    decision["frame_sha256"] = hashlib.sha256(json.dumps(frame, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()).hexdigest()
    (EV / "decision.json").write_text(json.dumps(decision, indent=2, sort_keys=True) + "\n")

    c = {
        "schema": "ANVIL_R7_INTEGRATED", "stage": "INDEPENDENT_C",
        "integrated_decision": {"path": "decision.json", "sha256": sha((EV / "decision.json").read_bytes())},
        "integrated_decision_sha256": hashlib.sha256(json.dumps(decision, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()).hexdigest(),
        "first_consumer": frame["first_real_consumer"],
        "independent_reverse_walk_of_whole_frame": "The reviewer traces each of the 118 identities from its exact row or documentary anchor to a named consumer or an explicit owner hold, and finds no synthetic SPINE substitution.",
        "strongest_choice_reversing_objection": "A source-located identity inventory does not by itself prove the physical C11 query semantics or dense workload economics.",
        "scientific_and_owner_boundary": "No survey answer is promoted to actor knowledge, material power or fictional world fact; SOROK and structural science remain owner-held.",
        "actual_first_consumer_assessment": "The current first consumer is named as a code symbol; no actual native first-reader execution is available in this bounded return.",
        "historical_no_loss_assessment": "K3 69 rows are exact; 26 proposals remain NOT_ADOPTED; 14 proofs remain HELD; 16 terminal identities remain identity-only and are not claimed implemented.",
        "reviewer_relationship": "DISTINCT_NONAUTHOR_ASSERTION_PENDING_EXTERNAL_VERIFICATION",
        "choice_reversing_objection_survives": True, "verdict": "C_HOLD_EXACT",
        "builder_cards": [
            {"id": "current", "domain": "CURRENT_FIRST_CONSUMER", "grade": "EXACT_BUILDER_HOLD",
             "first_consumer": "rawlsing_next/pre553_empirical_query.py::DirectEstateI03Session",
             "exact_hold": "Current native/sourcefree C11 first-reader execution is absent from this bounded return; no command receipt is claimed."},
            {"id": "future", "domain": "FUTURE_NONPRECLUSION", "grade": "EXACT_BUILDER_HOLD",
             "first_consumer": "WORKER_RETURNS/ANVIL_R7_FLEET/D4A/COLD_BUILDER_REHEARSAL.md::SOROK_1011_OWNER_HELD",
             "exact_hold": "SOROK #1011 actor/world receiving is owner-held and not present; no actor/science grant is claimed."}
        ],
        "original_source_granted_by_local_check": False, "owner_granted_by_local_check": False,
        "protected_h1_claimed": False,
    }
    (EV / "C.json").write_text(json.dumps(c, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"frame": sha((EV / "frame.json").read_bytes()), "decision": sha((EV / "decision.json").read_bytes()), "C": sha((EV / "C.json").read_bytes()), "inventory": sha(inv_path.read_bytes())}, indent=2))


if __name__ == "__main__":
    main()
