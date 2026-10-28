#!/usr/bin/env python3
"""Local read-only validator for Sorok's single derived command register.

No network, no original source access, no dynamic provider calls and no automatic
progress upgrades. Run from any cwd: python3 <path-to>/validate_command.py
"""
import json
import pathlib
import sys
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
errors = []
try:
    d = json.loads((HERE / "02_CAPABILITY_REGISTER.json").read_text(encoding="utf-8"))
except (OSError, ValueError) as exc:
    print("COMMAND_INVALID: unreadable JSON:", exc)
    sys.exit(1)

ms = d.get("milestone_rows", [])
ns = d.get("neo_requirements", [])
ds = d.get("decision_register", [])
es = d.get("critical_consumer_edges", [])
expected_ms = [f"C{i}" for i in range(13)] + [f"A{i}" for i in range(6)]
expected_ns = [f"N{i:02}" for i in range(1, 13)]
expected_ds = [f"O{i:02}" for i in range(1, 17)]

def ensure(cond, msg):
    if not cond:
        errors.append(msg)

def ids(rows):
    return [x.get("id") for x in rows if isinstance(x, dict)]

ensure(sorted(ids(ms)) == sorted(expected_ms), "milestone IDs must be exactly C0-C12/A0-A5")
ensure(sorted(ids(ns)) == sorted(expected_ns), "Neo IDs must be exactly N01-N12")
ensure(sorted(ids(ds)) == sorted(expected_ds), "decision IDs must be exactly O01-O16")
ensure(len(ids(es)) == len(set(ids(es))) and len(ids(es)) > 0, "consumer edges must be uniquely identified")
real_ds = set(expected_ds)
real_ms = set(expected_ms)
real_ns = set(expected_ns)
counts = Counter()
for m in ms:
    grade = m.get("engineering_maturity_0_6")
    ensure(type(grade) is int and 0 <= grade <= 6, "invalid maturity for " + str(m.get("id")))
    if type(grade) is int:
        counts[str(grade)] += 1
    ensure(set(m.get("original_science_dockets", [])) <= real_ds, "bad decision in milestone " + str(m.get("id")))
    if grade is not None and grade >= 5:
        ensure(bool(m.get("native_product_accepted")), "operative grade without native acceptance " + str(m.get("id")))
for n in ns:
    ensure(set(n.get("decision_ids", [])) <= real_ds, "bad Neo decision " + str(n.get("id")))
for dec in ds:
    ensure(set(dec.get("unlocks_milestones", [])) <= real_ms, "bad milestone link in " + str(dec.get("id")))
    ensure(set(dec.get("unlocks_neo_requirements", [])) <= real_ns, "bad Neo link in " + str(dec.get("id")))
    ensure(any(dec.get("id") in e.get("science_decision_ids", []) for e in es), "unlinked science decision " + str(dec.get("id")))
    if dec.get("settled_by_scoped_original_owner"):
        ensure(bool(dec.get("evidence_of_issuer_action")), "issued decision without exact evidence " + str(dec.get("id")))
for e in es:
    ensure(set(e.get("science_decision_ids", [])) <= real_ds, "invalid science ID in edge " + str(e.get("id")))
    ensure(set(e.get("unlocks_milestones", [])) <= real_ms, "invalid milestone in edge " + str(e.get("id")))
    ensure(bool(e.get("next_authorized_operation")), "missing actionable next operation in edge " + str(e.get("id")))
    ensure(bool(e.get("acceptance_test_or_issuer_condition")), "missing exit condition in edge " + str(e.get("id")))
    ensure(bool(e.get("competent_owner_domain")), "missing owner in edge " + str(e.get("id")))
    ensure(bool(e.get("priority")), "missing priority in edge " + str(e.get("id")))

stat = d.get("measured_completion", {})
ensure(stat.get("milestones_total") == 19, "wrong terminal denominator")
ensure(stat.get("engineering_maturity_distribution") == {str(i): counts.get(str(i), 0) for i in range(7)}, "maturity counts do not match rows")
ensure(stat.get("native_milestones_accepted") == sum(bool(x.get("native_product_accepted")) for x in ms), "native count does not match rows")
ensure(stat.get("global_weighted_percentage") is None, "unjustified weighted completion percent")
for name in ["00_COMMAND.md", "01_SCIENTIFIC_DECISION_FRONTIER.md",
             "03_COMPLETION_SEQUENCE.md", "04_FLIGHT_AND_CURRENTNESS.md",
             "05_EXISTING_AUTHORITIES_AND_EVIDENCE.md",
             "06_HQ_COORDINATION_AND_UPDATE_PROTOCOL.md"]:
    ensure((HERE / name).is_file(), "missing command view " + name)
ensure((ROOT / "00_READ_ME_FIRST.md").is_file(), "Sorok front door missing")

if errors:
    print("COMMAND_INVALID:", len(errors), "issue(s)")
    for item in errors:
        print(" -", item)
    sys.exit(1)
print("COMMAND_VALID: 19 milestones, 12 Neo requirements, 16 science decisions, "
      f"{len(es)} consumer edges; maturity {dict(counts)}; "
      "no native/weighted inference")
