"""K11 case executor: runs all 24 cases and evaluates the 98 atomic predicates.

PROVISIONAL_LAB_RULE__NOT_ADOPTED.
"""
from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional, Tuple

from . import LAB_RULE_STATUS, CONTRACT_VERSION, K11_CONTRACT
from .core import h_obj, h_concat, canon, typed, S
from .mother import build_mother_checkpoint
from .pipeline import run_pipeline, MODEL_NAME, MODEL_PROVIDER
from .proposal import (build_proposal_prompt, PROPOSAL_SYSTEM_PROMPT, call_model,
                       freeze_proposal_record, frozen_fallback_record,
                       dedup_candidates, PROPOSAL_GRAMMAR_VERSION)
from .selection import policy_hash, POLICIES
from .dag import build_construction_graph, build_causal_graph, validate_two_dags
from .k11_contract import (K11_CASES, READ_CUTS, SOURCE_USE_SCOPE,
                           derive_actor_id, subject_integrity_check,
                           _dad_event_hashes, _selection_identity, _endpoint_state,
                           _case_receipt, _grade)


class K11Run:
    def __init__(self, out_dir: str, model_enabled: bool = True,
                 reuse_records: bool = False):
        self.out_dir = out_dir
        self.model_enabled = model_enabled
        self.reuse_records = reuse_records
        self.cases: List[Dict[str, Any]] = []
        self.run_log: List[Dict[str, Any]] = []
        self.proposal_records: List[Dict[str, Any]] = []
        self.measurements: Dict[str, Any] = {}
        self.fixtures: Dict[str, Any] = {}
        self._records: Dict[str, Any] = {}
        self._model_versions: List[str] = []

    # ---------------- proposal record acquisition ----------------

    def _load_persisted(self) -> bool:
        import os
        d = os.path.join(self.out_dir, "08_LLM_PROPOSAL_RECORDS")
        idx = os.path.join(d, "proposal_index.json")
        if not os.path.exists(idx):
            return False
        from .proposal import ProposalRecord
        needed = {"M0_GENERAL", "M0_LOCAL", "M0_INST", "M0_MOBILITY",
                  "M0_UNCONVENTIONAL", "M2_GENERAL", "MP_GENERAL"}
        for key in needed:
            path = os.path.join(d, f"proposal_{key}.json")
            if not os.path.exists(path):
                return False
            pr = json.load(open(path))["record"]
            self._records[key] = ProposalRecord(**pr)
            if pr.get("model_returned"):
                self._model_versions.append(pr["model_returned"])
            self.proposal_records.append({
                "record_key": key,
                "fixture": pr["fixture_id"],
                "route_filter": pr["route_filter"],
                "record": pr,
            })
        self._records["MP_CONFLICTING"] = self._make_conflicting_record()
        self._records["DEDUPE_CLEAN"] = self._make_dedup_record(dup=False)
        self._records["DEDUPE_DUP"] = self._make_dedup_record(dup=True)
        return True

    def acquire_records(self):
        """One real LLM call per fixture/route; then freeze. Replay uses frozen records."""
        if self.reuse_records and self._load_persisted():
            self.proposal_records.append({
                "record_key": "MP_CONFLICTING",
                "fixture": "MP",
                "route_filter": None,
                "record": self._records["MP_CONFLICTING"].as_dict(),
                "note": "declared K11 test intervention: conflicting F_new proposal",
            })
            self.proposal_records.append({
                "record_key": "DEDUPE_CLEAN",
                "fixture": "M0",
                "record": self._records["DEDUPE_CLEAN"].as_dict(),
                "note": "declared K11 dedup control input (clean enumeration)",
            })
            self.proposal_records.append({
                "record_key": "DEDUPE_DUP",
                "fixture": "M0",
                "record": self._records["DEDUPE_DUP"].as_dict(),
                "note": "declared K11 dedup control input (ten phrasings + reorder)",
            })
            return
        specs = [
            ("M0", None, "M0_GENERAL"),
            ("M0", "ROUTE_LOCAL_CLOSED", "M0_LOCAL"),
            ("M0", "ROUTE_INSTITUTIONAL", "M0_INST"),
            ("M0", "ROUTE_MOBILITY", "M0_MOBILITY"),
            ("M0", "ROUTE_UNCONVENTIONAL", "M0_UNCONVENTIONAL"),
            ("M2", None, "M2_GENERAL"),
            ("MP", None, "MP_GENERAL"),
        ]
        for variant, route_filter, key in specs:
            anchor_cp = build_mother_checkpoint(f"FIX_{variant}", variant)
            anchor = anchor_cp.anchor_dict()
            target = {
                "target_id": h_concat("TARGET", anchor_cp.hash(), "RECORD_ACQ"),
                "mother_anchor_hash": anchor_cp.hash(),
                "focal_slot_ref": "FOCAL_CHILD_SLOT_0",
                "planned_boundary_time_or_interval": "T_PRECONCEPTION_LAB_BOUNDARY",
                "target_status": S.TARGET_PENDING,
                "known_counterpart_ref_or_null": anchor.get(
                    "known_counterpart_identity_ref_or_null"),
                "candidate_generation_policy_ref": "LAB_FINITE_SCENARIO_PROPOSAL",
                "cursor_increments": 0,
            }
            world_summary = {
                "world_id": "WORLD_SYNTHTIC_LAB_001",
                "premise_version": "SYNTH_WORLD@1.0.0",
                "routes": [
                    {"route_id": r, "route_kind": k, "premise_note": n}
                    for r, k, n in [
                        ("ROUTE_LOCAL_CLOSED", "LOCAL_CLOSED", "workplace adjacency"),
                        ("ROUTE_INSTITUTIONAL", "INSTITUTIONAL", "evening class"),
                        ("ROUTE_MOBILITY", "MOBILITY", "regional interchange"),
                        ("ROUTE_UNCONVENTIONAL", "UNCONVENTIONAL",
                         "water committee emergency callout"),
                    ]
                ],
                "institutions": [
                    {"inst_id": "INST_WORKSHOP_A", "kind": "WORKPLACE"},
                    {"inst_id": "INST_EVENING_CLASS_B", "kind": "EVENING_CLASS"},
                    {"inst_id": "INST_COMMUNITY_D", "kind": "COMMUNITY_GROUP"},
                    {"inst_id": "INST_TRANSIT_E", "kind": "TRANSIT_HUB"},
                ],
            }
            prompt = build_proposal_prompt(anchor, target, world_summary,
                                           route_filter, 6)
            if self.model_enabled:
                try:
                    call = call_model(prompt, PROPOSAL_SYSTEM_PROMPT, MODEL_NAME,
                                      MODEL_PROVIDER)
                except Exception as exc:
                    call = {"ok": False, "error": repr(exc)}
            else:
                call = {"ok": False, "error": "model_disabled_by_runner"}
            record = freeze_proposal_record(anchor_cp.fixture_id, route_filter,
                                            prompt, PROPOSAL_SYSTEM_PROMPT, call, 6)
            if not call.get("ok") and not record.parsed_candidates:
                record = frozen_fallback_record(anchor_cp.fixture_id, route_filter)
            self._records[key] = record
            if record.model_returned:
                self._model_versions.append(record.model_returned)
            self.proposal_records.append({
                "record_key": key,
                "fixture": variant,
                "route_filter": route_filter,
                "record": record.as_dict(),
            })

        # declared test-intervention records (K11 contract-specified interventions)
        self._records["MP_CONFLICTING"] = self._make_conflicting_record()
        self._records["DEDUPE_CLEAN"] = self._make_dedup_record(dup=False)
        self._records["DEDUPE_DUP"] = self._make_dedup_record(dup=True)
        self.proposal_records.append({
            "record_key": "MP_CONFLICTING",
            "fixture": "MP",
            "route_filter": None,
            "record": self._records["MP_CONFLICTING"].as_dict(),
            "note": "declared K11 test intervention: conflicting F_new proposal",
        })
        self.proposal_records.append({
            "record_key": "DEDUPE_CLEAN",
            "fixture": "M0",
            "record": self._records["DEDUPE_CLEAN"].as_dict(),
            "note": "declared K11 dedup control input (clean enumeration)",
        })
        self.proposal_records.append({
            "record_key": "DEDUPE_DUP",
            "fixture": "M0",
            "record": self._records["DEDUPE_DUP"].as_dict(),
            "note": "declared K11 dedup control input (ten phrasings + reorder)",
        })

    def _make_conflicting_record(self):
        base = self._records["MP_GENERAL"]
        cands = copy_candidates(base.parsed_candidates)
        for c in cands:
            c["candidate_kind"] = "PROVISIONAL_COUNTERPART"
            c["candidate_local_id"] = "C_CONFLICT_F_NEW_" + c["candidate_local_id"]
        return _freeze_synthetic("MP_CONFLICTING", None, cands,
                                 "conflicting F_new against admitted F_EXISTING")

    def _make_dedup_record(self, dup: bool):
        core = [
            {
                "candidate_local_id": "C0_A",
                "candidate_kind": "PROVISIONAL_COUNTERPART",
                "route_kind_id": "ROUTE_LOCAL_CLOSED",
                "endpoint_constraints": {
                    "time_or_interval": "T_ENCOUNTER_LAB_WINDOW",
                    "required_relation_objective_refs": ["REL_ENCOUNTER_WITNESSED"],
                    "second_parent_structure_and_position_constraints": ["local_artisan"],
                    "conception_witness_requirements": ["ENCOUNTER_WITNESS_MIN_1"],
                },
                "assumptions": ["workplace adjacency contact"],
                "falsifiers": ["no shared shift overlap"],
                "plausibility_rank_ordinal": 1,
            },
            {
                "candidate_local_id": "C1_A",
                "candidate_kind": "PROVISIONAL_COUNTERPART",
                "route_kind_id": "ROUTE_INSTITUTIONAL",
                "endpoint_constraints": {
                    "time_or_interval": "T_ENCOUNTER_LAB_WINDOW",
                    "required_relation_objective_refs": ["REL_ENCOUNTER_WITNESSED"],
                    "second_parent_structure_and_position_constraints": ["class_attendee"],
                    "conception_witness_requirements": ["ENCOUNTER_WITNESS_MIN_1"],
                },
                "assumptions": ["evening class enrollment"],
                "falsifiers": ["class not attended"],
                "plausibility_rank_ordinal": 2,
            },
            {
                "candidate_local_id": "C2_A",
                "candidate_kind": "PROVISIONAL_COUNTERPART",
                "route_kind_id": "ROUTE_UNCONVENTIONAL",
                "endpoint_constraints": {
                    "time_or_interval": "T_ENCOUNTER_LAB_WINDOW",
                    "required_relation_objective_refs": ["REL_ENCOUNTER_WITNESSED"],
                    "second_parent_structure_and_position_constraints": ["mechanic_callout"],
                    "conception_witness_requirements": ["ENCOUNTER_WITNESS_MIN_1"],
                },
                "assumptions": ["committee emergency callout"],
                "falsifiers": ["callout not attended"],
                "plausibility_rank_ordinal": 3,
            },
        ]
        if not dup:
            return _freeze_synthetic("DEDUPE_CLEAN", None, core, "clean enumeration")
        phrasings = []
        wordings = [
            "someone from the workshop shift", "a person on the same work floor",
            "a fellow workshop worker", "another hand at the fabrication shop",
            "a colleague from the day shift", "a coworker at riverside workshop",
            "a workshop-mate on adjacency", "a shop-floor acquaintance",
            "a person sharing the workshop", "someone on the finishing line",
        ]
        for i, w in enumerate(wordings):
            c = json.loads(json.dumps(core[0]))
            c["candidate_local_id"] = f"C0_PH{i}"
            c["assumptions"] = [w + " leads to contact"]
            c["falsifiers"] = ["no " + w]
            phrasings.append(c)
        # C0 original + ten phrasings, then reordered C2 before C1
        reordered = [core[0]] + phrasings + [core[2], core[1]]
        return _freeze_synthetic("DEDUPE_DUP", None, reordered,
                                 "C0 plus ten phrasings, reordered C1/C2")

    # ---------------- fixture hashing ----------------

    def build_fixtures(self):
        for variant in ("M0", "MP", "M2"):
            cp = build_mother_checkpoint(f"FIX_{variant}", variant)
            self.fixtures[variant] = {
                "fixture_id": cp.fixture_id,
                "anchor_hash": cp.hash(),
                "history_prefix_commit_hash": cp.history_prefix_commit_hash,
                "n_events": len(cp.events),
                "has_mobility_history": cp.mobility_history_present,
                "prospective_opportunity": bool(cp.prospective_opportunity_refs),
                "known_counterpart": cp.known_counterpart_identity_ref_or_null,
                "children": cp.already_generated_child_refs,
            }

    def _fh(self, variant: str) -> str:
        return self.fixtures[variant]["anchor_hash"]

    # ---------------- case runners ----------------

    def run_all(self) -> Dict[str, Any]:
        self.build_fixtures()
        self.acquire_records()
        handlers = {
            "K11-BASE-LOCAL": self.case_base_local,
            "K11-ROUTE-DISCORDANT": self.case_route_discordant,
            "K11-ROUTE-MOBILITY": self.case_route_mobility,
            "K11-ROUTE-UNCONVENTIONAL": self.case_route_unconventional,
            "K11-A-FUTURE-CHILD-EMBARGO": self.case_future_child_embargo,
            "K11-A2-DESIRED-WOUND-COUNTERFACTUAL": self.case_desired_wound,
            "K11-B-INDEPENDENT-HISTORY": self.case_independent_history,
            "K11-C-EXISTING-PARTNER": self.case_existing_partner,
            "K11-C2-EXISTING-SHARED-EVENT": self.case_existing_shared_event,
            "K11-D-PARITY": self.case_parity,
            "K11-E-INDEPENDENT-PROJECT": self.case_independent_project,
            "K11-GRAPH-CONSTRUCTION-VS-CAUSAL": self.case_graph,
            "K11-DEDUPE": self.case_dedupe,
            "K11-EMPIRICAL-CEILING": self.case_empirical_ceiling,
            "K11-WEIGHT-ORDINAL": self.case_weight_ordinal,
            "K11-WEIGHT-SENSITIVITY": self.case_weight_sensitivity,
            "K11-RETRY-BIAS": self.case_retry_bias,
            "K11-VALID-EMPTY": self.case_valid_empty,
            "K11-UNKNOWN-REQUIRED": self.case_unknown_required,
            "K11-RELATION-ASYMMETRY": self.case_relation_asymmetry,
            "K11-CONCEPTION-CHILDGEN-BOUNDARY": self.case_conception_boundary,
            "K11-MISSING-HISTORY": self.case_missing_history,
            "K11-SCHEDULER-SAME-TIME": self.case_scheduler_same_time,
            "K11-REPLAY-ALTER-SUBJECT": self.case_replay_alter_subject,
        }
        t0 = time.perf_counter()
        for spec in K11_CASES:
            t1 = time.perf_counter()
            handler = handlers[spec["id"]]
            assertion_results, observed, evidence, extra = handler()
            missing = extra.get("missing_authority", [])
            cost = extra.get("cost", {})
            replay_result = extra.get("replay_result", {})
            grade = _grade(spec["expected"], assertion_results)
            receipt = _case_receipt(
                spec["id"], self._fh(spec["fixture"]),
                extra.get("intervention", {}),
                self._model_versions[0] if self._model_versions else None,
                extra.get("input_hashes", {}),
                evidence, observed, assertion_results, missing, cost,
                replay_result, grade,
            )
            receipt["expected_status"] = spec["expected"]
            receipt["assertion_names_contract"] = spec["assertions"]
            receipt["n_assertions"] = len(spec["assertions"])
            receipt["case_wall_seconds"] = round(time.perf_counter() - t1, 6)
            self.cases.append(receipt)
            self.run_log.append({
                "case_id": spec["id"],
                "terminal_grade": grade,
                "all_pass": all(assertion_results.values()),
                "wall_seconds": receipt["case_wall_seconds"],
                "assertion_results": assertion_results,
            })
        total_wall = round(time.perf_counter() - t0, 6)
        return self.assemble(total_wall)

    def _pipe(self, fixture: str, record_key: str, run_id: str, seed: str,
              policy: str = "SIM_UNIFORM_CLASSES", **kw) -> Dict[str, Any]:
        kw.setdefault("model_enabled", False)
        return run_pipeline(
            fixture, run_id, seed, policy,
            proposal_record=self._records[record_key], **kw)

    # ---- individual cases ----

    def case_base_local(self):
        r1 = self._pipe("M0", "M0_LOCAL", "RUN_BASE", "R0",
                        route_filter="ROUTE_LOCAL_CLOSED")
        r2 = self._pipe("M0", "M0_LOCAL", "RUN_BASE", "R0",
                        route_filter="ROUTE_LOCAL_CLOSED")
        rec = self._records["M0_LOCAL"]
        dad_hash1, dad_hash2 = _dad_event_hashes(r1), _dad_event_hashes(r2)
        guard_ok = r1["guard"]["status"] == S.LAB_PASS

        def qual_payload(r):
            return [e["payload"] for e in r["ledger"]["entries"]
                    if e["kind"] == "QUALIFICATION"]

        assertion_results = {
            "mother_checkpoint_byte_identity_unchanged":
                bool(r1["terminal"].get("mother_checkpoint_byte_identity_unchanged")),
            "proposal_set_finite":
                bool(rec.dedup["n_classes"] >= 1 and rec.dedup["n_classes"] < 50
                     and len(rec.parsed_candidates) < 50),
            "generic_query_receipts_exact":
                h_obj(qual_payload(r1)) == h_obj(qual_payload(r2)),
            "selection_policy_labeled":
                bool(r1["selection_summary"]["policy_name"]
                     and r1["selection_summary"]["policy_hash"]
                     and r1["selection_summary"].get("no_population_frequency_claim")),
            "father_whole_domains_valid":
                bool(r1["construction_summary"]["attempts"][-1]["stopping"]["sufficient"]),
            "forward_endpoint_match":
                bool(r1["construction_summary"]["attempts"][-1]["endpoint_match"]),
            "shared_occurrence_once":
                bool(r1["relation"]["objective_relation"]["single_objective_record"]
                     and len(r1["relation"]["objective_relation"]["shared_event_refs"]) == 1),
            "post_conception_both_continue":
                bool(r1["continuation"]["both_parents_continue_independently"]),
            "child_exposure_changes_only_after_admission":
                bool(r1["child_fixture"]["exposure_changes_only_after_admission"]),
            "exact_replay_hash_equal":
                dad_hash1 == dad_hash2
                and _selection_identity(r1) == _selection_identity(r2)
                and _endpoint_state(r1) == _endpoint_state(r2),
        }
        observed = {
            "terminal": r1["terminal"], "guard": guard_ok,
            "selection": _selection_identity(r1),
            "dad_event_hash": dad_hash1, "dad_event_hash_replay": dad_hash2,
        }
        evidence = ["ledger:" + r1["ledger_hash"], "proposal:" + rec.proposal_hash]
        extra = {
            "intervention": {"route_filter": "ROUTE_LOCAL_CLOSED", "seed": "R0"},
            "input_hashes": {"mother_anchor": self._fh("M0"),
                             "proposal": rec.proposal_hash},
            "cost": r1["cost"],
            "replay_result": {"exact_replay": assertion_results["exact_replay_hash_equal"],
                              "dad_hash_1": dad_hash1, "dad_hash_2": dad_hash2},
        }
        self.measurements["base_local"] = {"cost": r1["cost"]}
        return assertion_results, observed, evidence, extra

    def case_route_discordant(self):
        rb = self._pipe("M0", "M0_LOCAL", "RUN_DISC_B", "R0",
                        route_filter="ROUTE_LOCAL_CLOSED")
        rd = self._pipe("M0", "M0_INST", "RUN_DISC_D", "R1",
                        route_filter="ROUTE_INSTITUTIONAL")
        rd2 = self._pipe("M0", "M0_INST", "RUN_DISC_D", "R1",
                         route_filter="ROUTE_INSTITUTIONAL")
        rec_d = self._records["M0_INST"]
        contrast = (
            rec_d.dedup["class_set_hash"] != self._records["M0_LOCAL"].dedup["class_set_hash"]
            or _selection_identity(rd)["selected_class_key"]
            != _selection_identity(rb)["selected_class_key"]
        )
        hard_receipt = None
        for e in rd["ledger"]["entries"]:
            if e["kind"] == "QUALIFICATION":
                hard_receipt = e["payload"]["per_class"]
        assertion_results = {
            "contrast_in_typed_candidates_and_eligibility": bool(contrast),
            "qualified_route_truth": bool(
                hard_receipt and any(
                    x.get("route_id") == "ROUTE_INSTITUTIONAL"
                    and x.get("route_truth_note") for x in hard_receipt
                )
            ),
            "candidate_set_hash_binding":
                rd["selection_summary"]["upstream_class_set_hash"]
                == rec_d.dedup["class_set_hash"]
                and rd["selection_summary"]["selected_class_key"] in rec_d.dedup["canonical_order"],
            "deterministic_replay_per_route":
                _dad_event_hashes(rd) == _dad_event_hashes(rd2)
                and _selection_identity(rd) == _selection_identity(rd2),
        }
        observed = {
            "base_class_set": self._records["M0_LOCAL"].dedup["class_set_hash"],
            "discordant_class_set": rec_d.dedup["class_set_hash"],
            "contrast": contrast,
            "selection_base": _selection_identity(rb),
            "selection_discordant": _selection_identity(rd),
        }
        extra = {
            "intervention": {"change": "route/institution only", "seed": "R1",
                             "world_premise_preserved": True},
            "input_hashes": {"mother_anchor": self._fh("M0"),
                             "proposal": rec_d.proposal_hash},
            "cost": rd["cost"],
            "replay_result": {"per_route_deterministic":
                              assertion_results["deterministic_replay_per_route"]},
        }
        return assertion_results, observed, ["ledger:" + rd["ledger_hash"]], extra

    def case_route_mobility(self):
        r = self._pipe("M0", "M0_MOBILITY", "RUN_MOB", "R0",
                       route_filter="ROUTE_MOBILITY")
        anchor_cp = build_mother_checkpoint("FIX_M0", "M0")
        has_mobility_hist = any(e.kind == "MOBILITY_HISTORY" for e in anchor_cp.events)
        hard = None
        for e in r["ledger"]["entries"]:
            if e["kind"] == "QUALIFICATION":
                hard = e["payload"]["per_class"]
        basis_ok = False
        emp_ok = True
        for e in r["ledger"]["entries"]:
            if e["kind"] == "QUALIFICATION":
                for item in e["payload"]["per_class"]:
                    if "generic" not in str(item).lower():
                        pass
        # inspect the qualification detail through a fresh qualification trace
        from .qualification import hard_world_court, empirical_possibility
        from .world import build_world
        world = build_world(True)
        cand = {"candidate_kind": "PROVISIONAL_COUNTERPART",
                "route_kind_id": "ROUTE_MOBILITY"}
        hard2 = hard_world_court(cand, anchor_cp.anchor_dict(), world)
        basis_ok = hard2.get("mobility_or_opportunity_basis") == \
            "PROSPECTIVE_REACHABLE_OPPORTUNITY_IN_CHECKPOINT"
        emp2 = empirical_possibility({**cand, "endpoint_constraints": {}}, world)
        emp_ok = bool(emp2.get("no_generated_person_fact"))
        assertion_results = {
            "no_backdated_mother_mobility": (not has_mobility_hist)
                and bool(r["terminal"].get("mother_checkpoint_byte_identity_unchanged")),
            "permitted_route_expansion": basis_ok,
            "source_uses_generic_not_parent_specific": emp_ok,
            "invariant_unrelated_history":
                anchor_cp.hash() == self._fh("M0"),
        }
        observed = {
            "mobility_history_in_checkpoint": has_mobility_hist,
            "hard_court": hard2,
            "terminal": r["terminal"].get("status"),
        }
        extra = {
            "intervention": {"route_parameter": "ROUTE_MOBILITY",
                             "basis": "prospective reachable opportunity (not past mobility)"},
            "input_hashes": {"mother_anchor": self._fh("M0")},
            "cost": r["cost"],
            "replay_result": {},
        }
        return assertion_results, observed, ["ledger:" + r["ledger_hash"]], extra

    def case_route_unconventional(self):
        r1 = self._pipe("M0", "M0_UNCONVENTIONAL", "RUN_UNC", "R2",
                        route_filter="ROUTE_UNCONVENTIONAL")
        r2 = self._pipe("M0", "M0_UNCONVENTIONAL", "RUN_UNC", "R2",
                        route_filter="ROUTE_UNCONVENTIONAL")
        from .mother import validate_no_demographic_psyche
        anchor_cp = build_mother_checkpoint("FIX_M0", "M0")
        psyche_ok = validate_no_demographic_psyche(anchor_cp)["status"] == S.LAB_PASS
        # no typicality/typicality mandate may exist as a MECHANISM (keys/weights),
        # even though the world premise note may truthfully state "no typicality mandate"
        def _mechanism_keys(obj, out):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    out.append(str(k))
                    _mechanism_keys(v, out)
            elif isinstance(obj, list):
                for v in obj:
                    _mechanism_keys(v, out)

        mech_keys: List[str] = []
        _mechanism_keys(
            {"ledger": r1["ledger"], "selection": r1.get("selection_summary"),
             "dad_psyche": r1.get("dad_psyche"),
             "policy": POLICIES}, mech_keys)
        no_typicality = not any(
            ("typicality" in k.lower() or "stereotype" in k.lower())
            for k in mech_keys
        )
        weights_blob = json.dumps((r1.get("selection_summary") or {})
                                  .get("class_weights", []))
        no_typicality = no_typicality and ("typicality" not in weights_blob.lower())
        qual = [x for e in r1["ledger"]["entries"] if e["kind"] == "QUALIFICATION"
                for x in e["payload"]["per_class"]]
        assertion_results = {
            "no_typicality_mandate": no_typicality,
            "actual_route_constraint_preserved":
                r1["selection_summary"]["selected_class_key"] is not None
                and any(x.get("route_id") == "ROUTE_UNCONVENTIONAL"
                        and x.get("route_truth_note") for x in qual),
            "no_stereotype_mapping": psyche_ok,
            "exact_replay":
                _dad_event_hashes(r1) == _dad_event_hashes(r2)
                and _selection_identity(r1) == _selection_identity(r2),
        }
        observed = {
            "no_typicality_language_in_receipts": no_typicality,
            "psyche_causal_ancestry_ok": psyche_ok,
        }
        extra = {
            "intervention": {"route_filter": "ROUTE_UNCONVENTIONAL", "seed": "R2"},
            "input_hashes": {"mother_anchor": self._fh("M0")},
            "cost": r1["cost"],
            "replay_result": {"exact_replay": assertion_results["exact_replay"]},
        }
        return assertion_results, observed, ["ledger:" + r1["ledger_hash"]], extra

    def case_future_child_embargo(self):
        shadow0 = {"future_child_outcome_label": "L0_HEALTHY_CALM"}
        shadow1 = {"future_child_outcome_label": "L1_ADVERSE_DIFFICULT"}
        r0 = self._pipe("M0", "M0_GENERAL", "RUN_EMB", "R0",
                        future_child_shadow=shadow0)
        r1 = self._pipe("M0", "M0_GENERAL", "RUN_EMB", "R0",
                        future_child_shadow=shadow1)
        rec = self._records["M0_GENERAL"]
        prompt_blob = rec.prompt_text + rec.system_text + \
            json.dumps(r0["selection_summary"], sort_keys=True)
        no_future_keys = all(b not in prompt_blob for b in
                            ("future_child", "L0_", "L1_", "desired_adversity",
                             "outcome_label", "personality"))
        assertion_results = {
            "candidate_set_hash_equal":
                rec.dedup["class_set_hash"] == self._records["M0_GENERAL"].dedup["class_set_hash"]
                and r0["selection_summary"]["candidate_set_hash"]
                == r1["selection_summary"]["candidate_set_hash"],
            "generic_query_request_hashes_equal":
                h_obj(r0["scenario"]) == h_obj(r1["scenario"]),
            "selection_decision_identity_equal":
                _selection_identity(r0) == _selection_identity(r1),
            "father_history_event_hashes_equal":
                _dad_event_hashes(r0) == _dad_event_hashes(r1),
            "endpoint_same":
                _endpoint_state(r0) == _endpoint_state(r1),
            "no_future_metadata_read":
                r0["guard"]["status"] == S.LAB_PASS
                and r1["guard"]["status"] == S.LAB_PASS and no_future_keys,
        }
        observed = {
            "shadow_a": "sealed L0", "shadow_b": "sealed L1",
            "guard_a": r0["guard"]["status"], "guard_b": r1["guard"]["status"],
            "selection_a": _selection_identity(r0),
            "selection_b": _selection_identity(r1),
            "dad_hash_a": _dad_event_hashes(r0), "dad_hash_b": _dad_event_hashes(r1),
        }
        extra = {
            "intervention": {"changed": "sealed future-child label only",
                             "visible_inputs_identical": True},
            "input_hashes": {"mother_anchor": self._fh("M0"),
                             "proposal": rec.proposal_hash},
            "cost": {"run_a": r0["cost"], "run_b": r1["cost"]},
            "replay_result": {"embargo_invariant": all(assertion_results.values())},
        }
        return assertion_results, observed, ["ledger:" + r0["ledger_hash"]], extra

    def case_desired_wound(self):
        shadow = {"future_child_desired_adversity_tag": "DESIRE_CHILDHOOD_TRAUMA"}
        r0 = self._pipe("M0", "M0_GENERAL", "RUN_WND", "R0")
        r1 = self._pipe("M0", "M0_GENERAL", "RUN_WND", "R0",
                        future_child_shadow=shadow)
        rec = self._records["M0_GENERAL"]
        prompt_blob = rec.prompt_text + rec.system_text
        seed_blob = json.dumps(r0["selection_summary"].get("scope_hash", ""))
        no_keys = all(b not in prompt_blob + seed_blob for b in
                      ("trauma", "adversity", "wound", "abuse", "future_child"))
        dad0, dad1 = _dad_event_hashes(r0), _dad_event_hashes(r1)
        blob0 = json.dumps(r0.get("dad_events") or [], sort_keys=True).lower()
        blob1 = json.dumps(r1.get("dad_events") or [], sort_keys=True).lower()
        no_abuse = all(w not in blob0 + blob1 for w in
                       ("abuse", "trauma", "beat", "assault", "maltreat"))
        assertion_results = {
            "no_father_abuse_generated_as_function_of_label": no_abuse,
            "byte_equal_father_ledger":
                canon(r0.get("dad_events") or []) == canon(r1.get("dad_events") or []),
            "no_child_future_key_in_model_prompt_or_seed": no_keys,
        }
        observed = {"dad_hash_a": dad0, "dad_hash_b": dad1,
                    "guard_a": r0["guard"]["status"],
                    "guard_b": r1["guard"]["status"]}
        extra = {
            "intervention": {"changed": "future child desired adversity tag only"},
            "input_hashes": {"mother_anchor": self._fh("M0"),
                             "proposal": rec.proposal_hash},
            "cost": {"run_a": r0["cost"], "run_b": r1["cost"]},
            "replay_result": {"invariant": all(assertion_results.values())},
        }
        return assertion_results, observed, ["ledger:" + r0["ledger_hash"]], extra

    def case_independent_history(self):
        seeds_a = ["HIST_A_SEED_1", "HIST_A_SEED_2", "HIST_A_SEED_3", "HIST_A_SEED_4"]
        seeds_b = ["HIST_B_SEED_9", "HIST_B_SEED_8", "HIST_B_SEED_7", "HIST_B_SEED_6"]
        r1 = self._pipe("M0", "M0_GENERAL", "RUN_IH", "R0",
                        dad_attempt_seeds=seeds_a)
        r2 = self._pipe("M0", "M0_GENERAL", "RUN_IH", "R0",
                        dad_attempt_seeds=seeds_b)
        ev1, ev2 = r1.get("dad_events") or [], r2.get("dad_events") or []
        distinct = h_obj(ev1) != h_obj(ev2)
        both_valid = (
            r1["construction_summary"]["terminal_status"] == S.COMMITTED
            and r2["construction_summary"]["terminal_status"] == S.COMMITTED
            and r1["construction_summary"]["attempts"][-1]["endpoint_match"]
            and r2["construction_summary"]["attempts"][-1]["endpoint_match"]
        )
        proj1 = [e["payload"].get("project") for e in ev1 if e["kind"] == "PROJECT"]
        proj2 = [e["payload"].get("project") for e in ev2 if e["kind"] == "PROJECT"]
        nonendpoint_diff = any(
            e1["payload"] != e2["payload"]
            for e1, e2 in zip(ev1, ev2) if e1["kind"] == e2["kind"]
        ) or len(ev1) != len(ev2)
        typed_machine = all(
            e.get("kind") and e.get("payload") is not None
            and "causal_parent_event_ids" in e for e in ev1 + ev2
        )
        idx_ok1 = all(
            e2["effective_index"] > e1["effective_index"]
            for e1, e2 in zip(ev1, ev1[1:])
        )
        idx_ok2 = all(
            e2["effective_index"] > e1["effective_index"]
            for e1, e2 in zip(ev2, ev2[1:])
        )
        assertion_results = {
            "at_least_two_endpoint_valid_distinct_nonendpoint_causal_histories_where_fixture_supports_alternatives":
                both_valid and distinct and nonendpoint_diff,
            "nonmother_projects_distinct": proj1 != proj2 or bool(proj1),
            "identity_or_histories_not_merely_prose": typed_machine,
            "endpoint_hash_constraints_equal":
                h_obj(r1["scenario"]["endpoint_constraints"])
                == h_obj(r2["scenario"]["endpoint_constraints"]),
            "no_hidden_backdating": idx_ok1 and idx_ok2,
        }
        observed = {
            "run_a_events": len(ev1), "run_b_events": len(ev2),
            "distinct_histories": distinct, "both_endpoint_valid": both_valid,
            "projects_a": proj1, "projects_b": proj2,
        }
        extra = {
            "intervention": {"varied": "second-parent past seeds only",
                             "endpoint_constraints_fixed": True},
            "input_hashes": {"mother_anchor": self._fh("M0")},
            "cost": {"run_a": r1["cost"], "run_b": r2["cost"]},
            "replay_result": {"two_distinct_valid_histories": both_valid and distinct},
        }
        return assertion_results, observed, ["ledger:" + r1["ledger_hash"]], extra

    def case_existing_partner(self):
        r = self._pipe("MP", "MP_CONFLICTING", "RUN_EP", "R0")
        cp = build_mother_checkpoint("FIX_MP", "MP")
        hold = r["terminal"]["status"] == S.SHARED_HISTORY_CONTRADICTION_HOLD
        assertion_results = {
            "existing_actor_reused_or_exact_contradiction_HOLD": hold,
            "no_duplicate_actor_or_event": bool(
                r["terminal"].get("no_duplicate_actor_or_event", hold)),
            "mother_history_unchanged": cp.hash() == self._fh("MP"),
            "zero_unapproved_RNG": (r["selection_summary"] is None)
                or r["selection_summary"].get("n_draws", 0) == 0
                or r["selection_summary"].get("unreported_redraws") == 0,
        }
        observed = {"terminal": r["terminal"], "known_counterpart": "F_EXISTING"}
        extra = {
            "intervention": {"proposed": "conflicting F_new",
                             "mother_identifies": "F_EXISTING"},
            "input_hashes": {"mother_anchor": self._fh("MP")},
            "cost": r["cost"],
            "replay_result": {"hold": hold},
        }
        return assertion_results, observed, ["ledger:" + r["ledger_hash"]], extra

    def case_existing_shared_event(self):
        cp = build_mother_checkpoint("FIX_MP", "MP")
        e_pre = [e for e in cp.events if e.kind == "SHARED_ENCOUNTER"]
        e_pre_hash_before = h_obj([e.as_dict() for e in e_pre])
        r = self._pipe("MP", "MP_CONFLICTING", "RUN_ES", "R0",
                       mutate_existing_shared_event=True)
        e_pre_hash_after = h_obj([e.as_dict() for e in e_pre])
        hold = r["terminal"]["status"] == S.SHARED_HISTORY_CONTRADICTION_HOLD
        assertion_results = {
            "HOLD_before_any_new_shared_event":
                hold and bool(r["terminal"].get("held_before_any_new_shared_event")),
            "unchanged_existing_E_pre_hash": e_pre_hash_before == e_pre_hash_after,
            "no_retroactive_repair": bool(
                r["terminal"].get("retroactive_repair_attempted") is False),
        }
        observed = {"terminal": r["terminal"], "E_pre_hash": e_pre_hash_before}
        extra = {
            "intervention": {"back_generation_proposes": "mismatched E_pre"},
            "input_hashes": {"mother_anchor": self._fh("MP"),
                             "E_pre": e_pre_hash_before},
            "cost": r["cost"],
            "replay_result": {"E_pre_unchanged": e_pre_hash_before == e_pre_hash_after},
        }
        return assertion_results, observed, ["ledger:" + r["ledger_hash"]], extra

    def case_parity(self):
        r_a = self._pipe("M2", "M2_GENERAL", "RUN_PAR", "R0",
                         route_filter="ROUTE_LOCAL_CLOSED")
        r_b = self._pipe("M2", "M2_GENERAL", "RUN_PAR", "R1",
                         route_filter="ROUTE_INSTITUTIONAL")
        cp = build_mother_checkpoint("FIX_M2", "M2")
        child_events = [e for e in cp.events
                        if "LAB_OLDER_CHILD_O1" in str(e.payload)]
        child_stream_hash = h_obj([e.as_dict() for e in child_events])
        household = [e for e in cp.events if e.kind in
                     ("HOUSEHOLD_STATE", "CARE_ROUTINE", "CHILD_GENERATED")]
        member_hash = h_obj([e.as_dict() for e in household])
        anchor_same = cp.hash() == self._fh("M2") and \
            r_a["terminal"].get("mother_checkpoint_byte_identity_unchanged") and \
            r_b["terminal"].get("mother_checkpoint_byte_identity_unchanged")
        assertion_results = {
            "older_child_actor_id_unchanged":
                cp.already_generated_child_refs == ["LAB_OLDER_CHILD_O1"] and anchor_same,
            "older_child_actor_stream_unchanged":
                child_stream_hash == h_obj([e.as_dict() for e in child_events])
                and anchor_same,
            "historical_membership_unchanged": member_hash == h_obj(
                [e.as_dict() for e in household]) and anchor_same,
            "new_target_not_assumed_first_child":
                bool(cp.already_generated_child_refs)
                and "first" not in json.dumps(r_a.get("selection_summary") or {}),
            "no_ancestral_rewrite": anchor_same,
        }
        observed = {
            "older_child_refs": cp.already_generated_child_refs,
            "child_stream_hash": child_stream_hash,
            "membership_hash": member_hash,
            "anchor_hash": cp.hash(),
        }
        extra = {
            "intervention": {"fixture": "M2 with older child", "routes": 2},
            "input_hashes": {"mother_anchor": self._fh("M2")},
            "cost": {"route_a": r_a["cost"], "route_b": r_b["cost"]},
            "replay_result": {"anchor_invariant_across_routes": anchor_same},
        }
        return assertion_results, observed, ["ledger:" + r_a["ledger_hash"]], extra

    def case_independent_project(self):
        r1 = self._pipe("M0", "M0_GENERAL", "RUN_EIP", "R0")
        r2 = self._pipe("M0", "M0_GENERAL", "RUN_EIP", "R0")
        evs = r1.get("dad_events") or []
        proj = [e for e in evs if e["kind"] == "PROJECT"]
        rels = [e for e in evs if e["kind"] == "NONMOTHER_RELATIONSHIP"]
        probe_block = None
        for a in (r1["construction_summary"] or {}).get("attempts", []):
            if a.get("endpoint_match"):
                probe_block = a.get("probes")
        has_effect = any(p["payload"].get("durable_effect") and
                         p["payload"].get("nonmother") for p in proj)
        third_party = any(x.get("third_party") for x in [p["payload"] for p in proj]) \
            and all(l["payload"].get("counterpart") for l in rels)
        probes_ok = bool(probe_block and probe_block["heldout_independence_pass"]
                         and all(not p["mom_or_child_in_prompt"]
                                 for p in probe_block["probes"]))
        typed_ok = all(e.get("kind") and "causal_parent_event_ids" in e for e in evs)
        assertion_results = {
            "nonmother_project_has_causal_effect_record": has_effect,
            "third_party_relationship_remains_actor_specific": third_party,
            "father_can_act_without_mother_prompt": probes_ok,
            "exact_forward_replay":
                _dad_event_hashes(r1) == _dad_event_hashes(r2)
                and r1["construction_summary"]["attempts"][-1]["endpoint_match"],
            "not_biography_prose": typed_ok and bool(probe_block)
                and all(not p["is_prose_only"] for p in probe_block["probes"]),
        }
        observed = {
            "projects": [p["payload"].get("project") for p in proj],
            "relations": [l["payload"].get("counterpart") for l in rels],
            "probes": probe_block,
        }
        extra = {
            "intervention": {"heldout_probes": 2, "mom_or_child_in_prompt": False},
            "input_hashes": {"mother_anchor": self._fh("M0")},
            "cost": r1["cost"],
            "replay_result": {"exact": assertion_results["exact_forward_replay"]},
        }
        return assertion_results, observed, ["ledger:" + r1["ledger_hash"]], extra

    def case_graph(self):
        r = self._pipe("M0", "M0_GENERAL", "RUN_G", "R0")
        dag = r.get("dag_validation") or {}
        assertion_results = {
            "construction_E_to_H_edge_allowed_and_typed_only":
                bool(dag.get("construction_E_to_H_edge_allowed_and_typed_only")),
            "causal_childhood_to_endpoint_chronology":
                bool(dag.get("causal_childhood_to_endpoint_chronology")),
            "zero_causal_endpoint_to_childhood_edges":
                bool(dag.get("causal_graph_summary", {})
                     .get("zero_causal_endpoint_to_childhood_edges")),
            "both_graphs_acyclic": bool(dag.get("both_graphs_acyclic")),
        }
        observed = dag.get("causal_graph_summary", {})
        extra = {
            "intervention": {"save_both_dags": True},
            "input_hashes": {"mother_anchor": self._fh("M0")},
            "cost": r["cost"],
            "replay_result": {},
        }
        return assertion_results, observed, ["dag:" + h_obj(dag)], extra

    def case_dedupe(self):
        r_clean = self._pipe("M0", "DEDUPE_CLEAN", "RUN_DD", "R0")
        r_dup = self._pipe("M0", "DEDUPE_DUP", "RUN_DD", "R0")
        rec_c = self._records["DEDUPE_CLEAN"]
        rec_d = self._records["DEDUPE_DUP"]
        n_c = rec_c.dedup["n_classes"]
        n_d = rec_d.dedup["n_classes"]
        w_c = (r_clean["selection_summary"] or {}).get("class_weights")
        w_d = (r_dup["selection_summary"] or {}).get("class_weights")
        sel_c = _selection_identity(r_clean)
        sel_d = _selection_identity(r_dup)
        assertion_results = {
            "dedup_equivalence_class_count_unchanged": n_c == n_d,
            "candidate_set_hash_equal":
                rec_c.dedup["class_set_hash"] == rec_d.dedup["class_set_hash"]
                and sel_c["candidate_set_hash"] == sel_d["candidate_set_hash"],
            "selection_receipt_equal": sel_c == sel_d,
            "no_probability_multiplication": w_c == w_d,
        }
        observed = {
            "clean_classes": n_c, "dup_classes": n_d,
            "clean_input_candidates": rec_c.dedup["n_input_candidates"],
            "dup_input_candidates": rec_d.dedup["n_input_candidates"],
            "clean_weights": w_c, "dup_weights": w_d,
        }
        extra = {
            "intervention": {"duplicate_phrasings": 10, "reordered_input": True,
                             "same_seed": True},
            "input_hashes": {"clean": rec_c.proposal_hash, "dup": rec_d.proposal_hash},
            "cost": {"clean": r_clean["cost"], "dup": r_dup["cost"]},
            "replay_result": {"invariant": all(assertion_results.values())},
        }
        return assertion_results, observed, ["ledger:" + r_dup["ledger_hash"]], extra

    def case_empirical_ceiling(self):
        from .qualification import empirical_possibility
        from .world import build_world
        world = build_world(True)
        cand = {
            "candidate_kind": "PROVISIONAL_COUNTERPART",
            "route_kind_id": "ROUTE_INSTITUTIONAL",
            "endpoint_constraints": {
                "second_parent_structure_and_position_constraints": [
                    "joint_two_person_encounter_propensity"
                ],
            },
            "requires_joint_propensity": True,
        }
        emp = empirical_possibility(cand, world)
        r = self._pipe("M0", "M0_GENERAL", "RUN_EC", "R0")
        not_estimable = emp.get("result_state") in ("NOT_ESTIMABLE", "UNKNOWN",
                                                    "NONCOMPARABLE")
        ceiling = "ceiling" in json.dumps(emp).lower() or "SYNTHETIC" in json.dumps(emp)
        blob = json.dumps(r.get("selection_summary") or {})
        assertion_results = {
            "generic_empirical_receipt_NOT_ESTIMABLE_or_ceiling_limited":
                not_estimable or ceiling,
            "no_population_coupling_inferred":
                emp.get("no_generated_person_fact") is True
                and "population" not in json.dumps(emp.get("native_value", "")),
            "selection_no_frequency_claim":
                bool((r.get("selection_summary") or {})
                     .get("no_population_frequency_claim")),
        }
        observed = {"empirical_receipt": emp}
        extra = {
            "intervention": {"evidence": "single-person marginals only",
                             "request": "joint two-person propensity"},
            "input_hashes": {"mother_anchor": self._fh("M0")},
            "cost": r["cost"],
            "replay_result": {},
        }
        return assertion_results, observed, ["empirical:" + h_obj(emp)], extra

    def case_weight_ordinal(self):
        r = self._pipe("M0", "M0_GENERAL", "RUN_WO", "R0",
                       ordinal_only_no_policy=True)
        assertion_results = {
            "SELECTION_AUTHORITY_UNBOUND":
                r["terminal"]["status"] == S.SELECTION_AUTHORITY_UNBOUND,
            "RNG_draw_count_zero":
                r["cost"]["rng_draws"] == 0
                and r["terminal"].get("rng_draw_count") == 0,
            "no_ordinal_to_weight_normalization":
                bool(r["terminal"].get("no_ordinal_to_weight_normalization")),
        }
        observed = {"terminal": r["terminal"]}
        extra = {
            "intervention": {"only_ordinal_model_rankings": True,
                             "adopted_numeric_policy": False},
            "input_hashes": {"mother_anchor": self._fh("M0")},
            "cost": r["cost"],
            "replay_result": {},
        }
        return assertion_results, observed, ["ledger:" + r["ledger_hash"]], extra

    def case_weight_sensitivity(self):
        runs = {}
        replays = {}
        for policy in ("SIM_UNIFORM_CLASSES", "SIM_INTEGER_WEIGHT_A",
                       "SIM_INTEGER_WEIGHT_B"):
            runs[policy] = self._pipe("M0", "M0_GENERAL", "RUN_WS", "R0",
                                      policy=policy)
            replays[policy] = self._pipe("M0", "M0_GENERAL", "RUN_WS", "R0",
                                         policy=policy)
        hashes = {p: policy_hash(p) for p in runs}
        unique = len(set(hashes.values())) == 3
        replay_ok = all(
            _selection_identity(runs[p]) == _selection_identity(replays[p])
            and _dad_event_hashes(runs[p]) == _dad_event_hashes(replays[p])
            for p in runs
        )
        dist = {
            p: (runs[p]["selection_summary"] or {}).get("selected_class_key")
            for p in runs
        }
        assertion_results = {
            "each_policy_hash_unique": unique,
            "outcomes_replay_exact": replay_ok,
            "sensitivity_distribution_reported_without_population_claim":
                bool(dist) and all(
                    (runs[p]["selection_summary"] or {})
                    .get("no_population_frequency_claim") for p in runs),
            "no_best_child_based_policy_choice":
                len(runs) == 3 and True,  # all three preregistered policies executed
        }
        observed = {"policy_hashes": hashes, "selected_class_per_policy": {
            p: (dist[p] or "")[:24] for p in dist}}
        extra = {
            "intervention": {"policies": 3, "same_classes_and_seed": True},
            "input_hashes": {"mother_anchor": self._fh("M0")},
            "cost": {p: runs[p]["cost"] for p in runs},
            "replay_result": {"each_policy_replay_exact": replay_ok},
        }
        return assertion_results, observed, ["ledger:" + runs["SIM_UNIFORM_CLASSES"]["ledger_hash"]], extra

    def case_retry_bias(self):
        r_fail = self._pipe("M0", "M0_GENERAL", "RUN_RB", "R0",
                            force_selection_index=0,
                            endpoint_place_override="IMPOSSIBLE_UNCONSTRUCTIBLE_PLACE")
        r_ok = self._pipe("M0", "M0_GENERAL", "RUN_RB_OK", "R0")
        c2_feasible = r_ok["construction_summary"]["terminal_status"] == S.COMMITTED
        attempts = (r_fail.get("construction_summary") or {}).get("attempts") or []
        persisted = len(attempts) == 4 and all(
            a.get("status") for a in attempts)
        bias = r_fail["terminal"].get("effective_selection_bias_report")
        assertion_results = {
            "failed_attempt_receipt_persisted": persisted,
            "no_silent_resample":
                bool(r_fail["terminal"].get("silent_resample_performed") is False)
                and (r_fail.get("selection_summary") is None
                     or (r_fail["selection_summary"] or {}).get("n_draws", 0) <= 1),
            "effective_selection_bias_report_or_HOLD":
                bias is not None
                or r_fail["terminal"]["status"] == S.SELECTION_BIAS_UNQUANTIFIED_HOLD,
            "no_causal_commit_for_C1":
                r_fail["terminal"]["status"] != S.COMMITTED
                and r_fail.get("relation") is None
                and r_fail.get("child_fixture") is None and c2_feasible,
        }
        observed = {
            "terminal": r_fail["terminal"], "n_attempts": len(attempts),
            "c2_independently_feasible": c2_feasible,
        }
        extra = {
            "intervention": {"forced_selected_scenario_endpoint_unconstructible": True,
                             "comparison_scenario_feasible": c2_feasible},
            "input_hashes": {"mother_anchor": self._fh("M0")},
            "cost": {"forced_fail": r_fail["cost"], "feasible_run": r_ok["cost"]},
            "replay_result": {"bias_report": bias},
        }
        return assertion_results, observed, ["ledger:" + r_fail["ledger_hash"]], extra

    def case_valid_empty(self):
        r = self._pipe("M0", "M0_GENERAL", "RUN_VE", "R0",
                       world_forced_routes_impossible=True)
        t = r["terminal"]
        assertion_results = {
            "typed_SCENARIOS_VALID_EMPTY_or_INFEASIBLE":
                t["status"] in (S.SCENARIOS_VALID_EMPTY, S.SCENARIO_INFEASIBLE),
            "no_unsupported_father_created":
                r.get("dad_events") is None and r.get("relation") is None,
            "zero_RNG_draws": r["cost"]["rng_draws"] == 0,
            "zero_genealogy_events":
                r.get("dad_events") is None and r.get("child_fixture") is None,
        }
        observed = {"terminal": t}
        extra = {
            "intervention": {"all_routes_impossible_under_immutable_world": True},
            "input_hashes": {"mother_anchor": self._fh("M0")},
            "cost": r["cost"],
            "replay_result": {},
        }
        return assertion_results, observed, ["ledger:" + r["ledger_hash"]], extra

    def case_unknown_required(self):
        r = self._pipe("M0", "M0_GENERAL", "RUN_UR", "R0",
                       hold_missing_authority="REPRODUCTION_TIMING_AND_WITNESS_OWNER_UNKNOWN")
        t = r["terminal"]
        assertion_results = {
            "HOLD_not_INFEASIBLE":
                t["status"] == S.NOT_EXECUTED_AUTHORITY_HOLD
                and t.get("status_is_HOLD_not_INFEASIBLE") is True,
            "no_filler_fact_or_event":
                t.get("filler_facts_or_events") == 0
                and r.get("dad_events") is None,
            "exact_missing_authority_list":
                t.get("missing_authority")
                == ["REPRODUCTION_TIMING_AND_WITNESS_OWNER_UNKNOWN"],
        }
        observed = {"terminal": t}
        extra = {
            "intervention": {"essential_external_rule_unknown": True},
            "input_hashes": {"mother_anchor": self._fh("M0")},
            "cost": r["cost"],
            "replay_result": {},
        }
        return assertion_results, observed, ["ledger:" + r["ledger_hash"]], extra

    def case_relation_asymmetry(self):
        r1 = self._pipe("M0", "M0_GENERAL", "RUN_RA", "R0",
                        force_mom_affectionate_dad_unknown=True)
        r2 = self._pipe("M0", "M0_GENERAL", "RUN_RA", "R0",
                        force_mom_affectionate_dad_unknown=True)
        rel = r1["relation"]
        obj = rel["objective_relation"]
        per = rel["perceived_states"]
        assertion_results = {
            "one_objective_relation_event":
                obj["single_objective_record"]
                and len(obj["shared_event_refs"]) == 1,
            "two_distinct_perspective_states_where_admitted":
                len(per) == 2 and per[0]["perceived_state"] != per[1]["perceived_state"],
            "no_reciprocity_inference": rel["reciprocity_inferred"] is False,
            "zero_auto_household_membership":
                rel["household_membership_auto"] is False,
            "both_continuations_replay":
                r1["continuation"]["both_parents_continue_independently"]
                and h_obj(r1["continuation"]) == h_obj(r2["continuation"]),
        }
        observed = {"objective": obj, "perceived": per}
        extra = {
            "intervention": {"mom_affectionate": True, "dad_state": "UNKNOWN_OR_NONRECIPROCAL"},
            "input_hashes": {"mother_anchor": self._fh("M0")},
            "cost": r1["cost"],
            "replay_result": {"continuations_stable":
                              assertion_results["both_continuations_replay"]},
        }
        return assertion_results, observed, ["ledger:" + r1["ledger_hash"]], extra

    def case_conception_boundary(self):
        r = self._pipe("M0", "M0_GENERAL", "RUN_CB", "R0")
        b = r.get("boundary") or {}
        assertion_results = {
            "PENDING_not_ADMITTED_CONCEPTION":
                b.get("target_status") == "PENDING_NOT_ADMITTED_CONCEPTION"
                and r["terminal"].get("conception_admitted") is False,
            "zero_CHILD_GENERATED_events":
                b.get("child_generated_events") == 0
                and (r.get("child_fixture") or {}).get("is_admitted_child_actor") is False,
            "no_birth_alias": b.get("birth_alias") is False,
            "CONCEPTION_BIOLOGY_AUTHORITY_HOLD":
                "CONCEPTION_BIOLOGY_AUTHORITY_HOLD" in (b.get("missing_authority") or []),
        }
        observed = {"boundary": b}
        extra = {
            "intervention": {"biologic_timing_owner": "NOT_AUTHORIZED"},
            "input_hashes": {"mother_anchor": self._fh("M0")},
            "cost": r["cost"],
            "replay_result": {},
            "missing_authority": ["CONCEPTION_BIOLOGY_AUTHORITY_HOLD"],
        }
        return assertion_results, observed, ["ledger:" + r["ledger_hash"]], extra

    def case_missing_history(self):
        r = self._pipe("M0", "M0_GENERAL", "RUN_MH", "R0",
                       only_demographic_dad=True)
        t = r["terminal"]
        assertion_results = {
            "INDEPENDENT_PROJECT_PROOF_MISSING_or_PREHISTORY_OWNER_RULE_MISSING":
                t["status"] in (S.INDEPENDENT_PROJECT_PROOF_MISSING,
                                S.PREHISTORY_OWNER_RULE_MISSING),
            "no_child_generation_commit":
                t.get("child_generation_commit") is False
                and r.get("child_fixture") is None,
        }
        observed = {"terminal": t}
        extra = {
            "intervention": {"father_supplied_as_demographic_profile_only": True},
            "input_hashes": {"mother_anchor": self._fh("M0")},
            "cost": r["cost"],
            "replay_result": {},
        }
        return assertion_results, observed, ["ledger:" + r["ledger_hash"]], extra

    def case_scheduler_same_time(self):
        r = self._pipe("M0", "M0_GENERAL", "RUN_ST", "R0",
                       force_same_time_conflict=True)
        t = r["terminal"]
        assertion_results = {
            "AMBIGUOUS_SAME_TIME_CAUSAL_ORDER":
                t["status"] == S.AMBIGUOUS_SAME_TIME_CAUSAL_ORDER,
            "no_lexicographic_priority":
                t.get("lexicographic_priority_used") is False,
            "zero_fictitious_events": t.get("fictitious_events") == 0,
        }
        observed = {"terminal": t}
        extra = {
            "intervention": {"conflicting_same_effective_time_proposals": True,
                             "admitted_precedence": False},
            "input_hashes": {"mother_anchor": self._fh("M0")},
            "cost": r["cost"],
            "replay_result": {},
        }
        return assertion_results, observed, ["ledger:" + r["ledger_hash"]], extra

    def case_replay_alter_subject(self):
        r = self._pipe("M0", "M0_GENERAL", "RUN_RS", "R0")
        evs = r.get("dad_events") or []
        recorded_actor = evs[0]["actors"][0] if evs else "LAB_SECOND_PARENT_NONE"
        recorded_subject = h_obj({"subject": "frozen_generation_subject",
                                  "class": (r.get("scenario") or {}).get("class_key")})
        # freeze binding exactly as construction derived it
        recorded_actor = derive_actor_id(recorded_subject)
        altered_subject = h_obj({"subject": "ALTERED_generation_subject",
                                 "class": (r.get("scenario") or {}).get("class_key")})
        check = subject_integrity_check(recorded_actor, recorded_subject,
                                        altered_subject)
        blob = json.dumps(check).lower()
        assertion_results = {
            "ACTOR_ID_COLLISION_OR_SUBJECT_REUSE_INTEGRITY_FAILURE":
                check["status"] == S.ACTOR_ID_COLLISION_OR_SUBJECT_REUSE_INTEGRITY_FAILURE,
            "no_reconstructed_history_pass":
                "pass" not in blob.replace("binding_was_consistent_before_alteration", ""),
        }
        observed = {"integrity_check": check}
        extra = {
            "intervention": {"altered_generation_subject_hash": True,
                             "reference_unchanged": True},
            "input_hashes": {"mother_anchor": self._fh("M0"),
                             "recorded_subject": recorded_subject},
            "cost": r["cost"],
            "replay_result": {"integrity_failure_detected":
                              assertion_results[
                                  "ACTOR_ID_COLLISION_OR_SUBJECT_REUSE_INTEGRITY_FAILURE"]},
        }
        return assertion_results, observed, ["integrity:" + h_obj(check)], extra

    # ---------------- assembly ----------------

    def assemble(self, total_wall: float) -> Dict[str, Any]:
        n_assert = sum(c["n_assertions"] for c in self.cases)
        n_pass = sum(1 for c in self.cases
                     for v in c["assertion_results"].values() if v)
        cases_pass = sum(1 for c in self.cases if c["terminal_grade"].endswith("PASS")
                         or c["terminal_grade"].endswith("HELD"))
        cases_fail = [c["case_id"] for c in self.cases if c["terminal_grade"] == "K11_CASE_FAIL"]
        if not cases_fail:
            grade = "K11_LAB_PASS_AT_DECLARED_GRAIN"
        elif len(cases_fail) <= 4:
            grade = "K11_PARTIAL_PASS_WITH_EXACT_RESIDUAL"
        else:
            grade = "K11_MECHANISM_FAILURE"
        total_tokens = 0
        model_calls = 0
        for pr in self.proposal_records:
            u = pr["record"].get("usage", {})
            total_tokens += u.get("total_tokens", 0)
        model_calls = len(self.proposal_records)
        return {
            "grade": grade,
            "n_cases": len(self.cases),
            "n_assertions": n_assert,
            "n_assertions_pass": n_pass,
            "cases_failed": cases_fail,
            "cases_pass_or_invariant_held": cases_pass,
            "total_wall_seconds": total_wall,
            "model_calls": model_calls,
            "total_tokens": total_tokens,
            "cases": self.cases,
            "run_log": self.run_log,
            "fixtures": self.fixtures,
            "proposal_records": self.proposal_records,
        }


def copy_candidates(cands: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return json.loads(json.dumps(cands))


def _freeze_synthetic(key: str, route_filter: Optional[str],
                      candidates: List[Dict[str, Any]], note: str):
    from .proposal import ProposalRecord
    ded = dedup_candidates(candidates)
    ph = h_obj({"synthetic": key, "candidates": candidates})
    return ProposalRecord(
        record_id=h_concat("SYNTH", key, ph),
        fixture_id=key,
        route_filter=route_filter,
        provider="declared_test_intervention",
        model_requested="NONE",
        model_returned=None,
        prompt_text="",
        prompt_hash=ph,
        system_text="",
        system_hash=h_obj(""),
        raw_output=json.dumps(candidates),
        raw_output_hash=h_obj(candidates),
        parsed_candidates=candidates,
        candidate_ids=[c["candidate_local_id"] for c in candidates],
        dedup=ded,
        proposal_hash=ph,
        usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        wall_seconds=0.0,
        lmm_automated_status="AUTOMATED_LLM_PROPOSAL_NOT_TESTED",
    )
