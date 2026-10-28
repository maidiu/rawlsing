#!/usr/bin/env python3
"""Read-only Sorok command validator. Executes without a provider, network or original source."""

import json
import pathlib
import re
import sys
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
errors = []

def check(test, description):
    if not test:
        errors.append(description)

def unique_ids(rows, expected, label):
    check(isinstance(rows, list), label + " must be an array")
    if not isinstance(rows, list):
        return set()
    ids = [r.get("id") for r in rows if isinstance(r, dict)]
    check(len(ids) == len(rows), label + " must contain objects with IDs")
    check(sorted(ids) == sorted(expected), label + " IDs are missing, duplicated or extra")
    return set(ids)

def sha40(s):
    return isinstance(s, str) and re.fullmatch(r"[0-9a-f]{40}", s) is not None

def evidence_fields(obj, fields, label):
    check(isinstance(obj, dict), label + " must be an evidence object")
    if not isinstance(obj, dict):
        return
    for f in fields:
        check(bool(obj.get(f)), label + " missing " + f)
    check(sha40(obj.get("source_sha")), label + " source_sha must be exact")

try:
    d = json.loads((HERE / "02_CAPABILITY_REGISTER.json").read_text(encoding="utf-8"))
except (OSError, ValueError) as exc:
    print("COMMAND_INVALID: unreadable JSON:", exc)
    sys.exit(1)

ms, ns = d.get("milestone_rows", []), d.get("neo_requirements", [])
ds, es = d.get("decision_register", []), d.get("critical_consumer_edges", [])
expected_ms = [f"C{i}" for i in range(13)] + [f"A{i}" for i in range(6)]
expected_ns = [f"N{i:02}" for i in range(1, 13)]
expected_ds = [f"O{i:02}" for i in range(1, 17)]
ms_ids = unique_ids(ms, expected_ms, "milestone")
ns_ids = unique_ids(ns, expected_ns, "Neo requirements")
ds_ids = unique_ids(ds, expected_ds, "scientific decisions")
edge_ids = [e.get("id") for e in es if isinstance(e, dict)]
check(isinstance(es, list) and len(edge_ids) == len(es), "consumer edges must be an array of objects")
check(len(edge_ids) > 0 and len(set(edge_ids)) == len(edge_ids), "consumer IDs must be nonempty and unique")

count = Counter()
for m in ms:
    if not isinstance(m, dict):
        continue
    label = str(m.get("id"))
    grade = m.get("engineering_maturity_0_6")
    check(type(grade) is int and 0 <= grade <= 6, "bad maturity: " + label)
    if type(grade) is int and 0 <= grade <= 6:
        count[str(grade)] += 1
    check(set(m.get("neo_requirements", [])) <= ns_ids, "unknown Neo requirement: " + label)
    check(set(m.get("original_science_dockets", [])) <= ds_ids, "unknown decision: " + label)
    check(bool(m.get("next_indispensable_operation")), "milestone without next action: " + label)
    check(bool(m.get("first_required_consumer")), "milestone without first consumer: " + label)
    if m.get("native_product_accepted"):
        check(type(grade) is int and grade >= 5, "native acceptance with grade below 5: " + label)
    if type(grade) is int and grade >= 3:
        check(m.get("actual_full_product_consumer") not in (None, "", "NOT_PROVEN"),
              "grade >=3 without actual integrated consumer: " + label)
        check(m.get("consumer_integration_claim") not in (None, "", "FULL_MILESTONE_CHAIN_NOT_ESTABLISHED"),
              "grade >=3 still says no chain: " + label)
        evidence_fields(m.get("integrated_consumer_evidence"),
                        ("source_sha", "producer", "consumer", "test_command", "test_result", "evidence_scope"),
                        "milestone " + label + " integration")
    if type(grade) is int and grade >= 4:
        evidence_fields(m.get("causal_severance_evidence"),
                        ("source_sha", "negative_control", "positive_control", "held_control", "result"),
                        "milestone " + label + " causality")
    if type(grade) is int and grade >= 5:
        check(bool(m.get("native_product_accepted")), "operative grade without acceptance: " + label)
        evidence_fields(m.get("operative_acceptance_evidence"),
                        ("source_sha", "original_owner", "grant_scope", "independent_qualification", "first_native_consumer"),
                        "milestone " + label + " operative")
    if type(grade) is int and grade >= 6:
        evidence_fields(m.get("continuing_product_evidence"),
                        ("source_sha", "person_id_scope", "actual_continuation", "owner_acceptance"),
                        "milestone " + label + " continuing product")
for n in ns:
    if not isinstance(n, dict):
        continue
    label = str(n.get("id"))
    check(set(n.get("decision_ids", [])) <= ds_ids, "bad decision in Neo: " + label)
    check(bool(n.get("scientific_review")), "Neo missing review grade: " + label)
    check(bool(n.get("specific_original_causal_rule")), "Neo missing causal-rule status: " + label)
for dec in ds:
    if not isinstance(dec, dict):
        continue
    label = str(dec.get("id"))
    check(set(dec.get("unlocks_milestones", [])) <= ms_ids, "bad unlock milestone: " + label)
    check(set(dec.get("unlocks_neo_requirements", [])) <= ns_ids, "bad unlock Neo: " + label)
    check(any(label in e.get("science_decision_ids", []) for e in es),
          "science decision without consumer edge: " + label)
    if dec.get("settled_by_scoped_original_owner"):
        evidence_fields(dec.get("evidence_of_issuer_action"),
                        ("source_sha", "owner", "rule_or_withholding", "scope", "readset", "first_consumer"),
                        "settled scientific decision " + label)
        check(dec.get("decision_status") != "ISSUER_ACTION_NOT_VERIFIED_AT_OBSERVED_CUT",
              "settled issuer action still labelled unverified: " + label)
    else:
        check(not dec.get("evidence_of_issuer_action"),
              "issuer evidence present but scientific question not marked settled: " + label)
for e in es:
    if not isinstance(e, dict):
        continue
    label = str(e.get("id"))
    check(set(e.get("science_decision_ids", [])) <= ds_ids, "bad science edge: " + label)
    check(set(e.get("unlocks_milestones", [])) <= ms_ids, "bad milestone edge: " + label)
    for field in ("first_actual_required_consumer", "next_authorized_operation",
                  "acceptance_test_or_issuer_condition", "competent_owner_domain",
                  "priority", "implementation_status", "blocking_authority",
                  "pinned_evidence_locator"):
        check(bool(e.get(field)), "edge " + label + " missing " + field)
    if e.get("native_accepted"):
        evidence_fields(e.get("native_acceptance_evidence"),
                        ("source_sha", "original_owner", "first_native_consumer", "qualification"),
                        "edge " + label + " native")

front = d.get("execution_frontier", {})
check(isinstance(front, dict), "missing machine execution frontier")
lanes = front.get("lanes", []) if isinstance(front, dict) else []
check(isinstance(lanes, list) and len(lanes) > 0, "missing prioritized lanes")
if isinstance(lanes, list):
    ranked = [x.get("priority_rank") for x in lanes if isinstance(x, dict)]
    lids = [x.get("id") for x in lanes if isinstance(x, dict)]
    check(len(lids) == len(lanes) and len(set(lids)) == len(lids), "duplicate/malformed lane")
    check(sorted(ranked) == list(range(1, len(lanes) + 1)), "lane ranks must be contiguous and distinct")
    for lane in lanes:
        if not isinstance(lane, dict):
            continue
        label = str(lane.get("id"))
        check(bool(lane.get("next_authorized_action")), "lane missing next action: " + label)
        check(bool(lane.get("first_real_consumer")), "lane missing consumer: " + label)
        check(bool(lane.get("stop_only")), "lane missing hold boundary: " + label)
        check(bool(lane.get("edge_ids")) and set(lane.get("edge_ids", [])) <= set(edge_ids),
              "lane references bad edges: " + label)
        check(set(lane.get("decision_ids", [])) <= ds_ids,
              "lane references bad science: " + label)
        check(set(lane.get("can_parallelize_with", [])) <= set(lids) - {label},
              "lane references invalid parallelism: " + label)

stat = d.get("measured_completion", {})
expected_dist = {str(i): count.get(str(i), 0) for i in range(7)}
check(stat.get("milestones_total") == len(expected_ms), "milestone denominator incorrect")
check(stat.get("engineering_maturity_distribution") == expected_dist, "milestone maturity distribution stale")
check(stat.get("native_milestones_accepted") == sum(bool(x.get("native_product_accepted")) for x in ms),
      "native milestone count stale")
check(stat.get("integrated_full_milestones_verified") == sum(x.get("engineering_maturity_0_6", 0) >= 3 for x in ms),
      "integrated milestone count stale")
check(stat.get("neo_scoped_requirement_reviews") ==
      sum(x.get("scientific_review") == "REVIEWED_SCOPED_REQUIREMENT" for x in ns), "Neo reviewed count stale")
check(stat.get("neo_issued_concrete_rules_verified") ==
      sum(x.get("specific_original_causal_rule") == "ISSUED_SCOPED" for x in ns), "Neo issued count stale")
check(stat.get("original_science_decisions_verified_settled") ==
      sum(x.get("settled_by_scoped_original_owner") is True for x in ds),
      "original scientific decision count stale")
check(stat.get("critical_edges_total") == len(es), "consumer-edge count stale")
check(stat.get("actual_native_critical_edges_accepted") ==
      sum(x.get("native_accepted") is True for x in es), "native edge count stale")
check(stat.get("critical_edges_accepted_at_component_sourcefree_only") ==
      sum(x.get("implementation_status") in (
          "SOURCEFREE_REPAIRED_FORK_CURRENT_C9_READER_PROVEN_AT_SELECTED_TEST_SCOPE__NOT_NATIVE",
          "REPAIRED_SOURCEFREE_COMPONENT") for x in es),
      "sourcefree component edge count stale")
check(stat.get("global_weighted_percentage") is None, "unsupported weighted percentage")
check(d.get("publication_branch") ==
      d.get("command_operating_contract", {}).get("canonical_branch"), "published branch pointer inconsistent")
check(sha40(d.get("generated_from_foundation_sha")), "source observation SHA invalid")
check(sha40(front.get("evidence_cut_sha")), "priority frontier evidence SHA invalid")
transitions = d.get("progress_transition_ledger", {})
check(isinstance(transitions, dict), "missing command grade transition ledger")
if isinstance(transitions, dict):
    events = transitions.get("recorded_events", [])
    check(isinstance(events, list), "change events must be list")
    if isinstance(events, list):
        check(transitions.get("current_revision") == len(events), "change revision/count mismatch")
        for i, ev in enumerate(events):
            if not isinstance(ev, dict):
                check(False, "invalid change event at " + str(i))
                continue
            evidence_fields(ev, ("source_sha", "affected_capability", "prior_grade", "new_grade",
                                 "producer", "first_consumer", "test_scope", "why_changed"),
                            "change event " + str(i))
            check(ev.get("affected_capability") in ms_ids, "change event bad milestone ID " + str(i))
            check(type(ev.get("prior_grade")) is int and type(ev.get("new_grade")) is int and
                  0 <= ev.get("prior_grade") <= 6 and 0 <= ev.get("new_grade") <= 6,
                  "change event bad maturity " + str(i))
            if i == len(events)-1 and ev.get("affected_capability") in ms_ids:
                row = next(m for m in ms if m.get("id") == ev["affected_capability"])
                check(row.get("engineering_maturity_0_6") == ev.get("new_grade"),
                      "latest changed milestone grade contradicts current register")

for name in ("00_COMMAND.md", "01_SCIENTIFIC_DECISION_FRONTIER.md",
             "03_COMPLETION_SEQUENCE.md", "04_FLIGHT_AND_CURRENTNESS.md",
             "05_EXISTING_AUTHORITIES_AND_EVIDENCE.md",
             "06_HQ_COORDINATION_AND_UPDATE_PROTOCOL.md"):
    check((HERE / name).is_file(), "missing command view: " + name)
check((ROOT / "00_READ_ME_FIRST.md").is_file(), "Sorok front door missing")
if errors:
    print("COMMAND_INVALID: " + str(len(errors)) + " issue(s)")
    for msg in errors:
        print(" - " + msg)
    sys.exit(1)
print("COMMAND_VALID: 19 C/A milestones, 12 Neo requirements, 16 science decisions, " +
      str(len(es)) + " consumer edges; " + str(len(lanes)) +
      " ranked operational lanes; maturity " + str(dict(count)) +
      "; no inferred native or global percent")
