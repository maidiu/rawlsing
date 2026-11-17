#!/usr/bin/env python3
"""Run hostile mutations against the original and repaired ANVIL gate copies.

Every attack is a local authored fixture. No native source, owner, science or H1
is authenticated. Results distinguish the old package from the private repair.
"""
import copy, hashlib, json, os, pathlib, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
EV = ROOT / "EVIDENCE"
SNAP = EV / "source_snapshot"
ORIG = ROOT / "PACKAGE" / "ANVIL_R7_ORIGINAL"
REP = ROOT / "PACKAGE" / "ANVIL_R7_REPAIRED"
GIT = pathlib.Path("/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/D4A")
PY = sys.executable


def sha(b): return hashlib.sha256(b).hexdigest()


def jsha(o): return hashlib.sha256(json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def write(p, o):
    p.write_text(json.dumps(o, indent=2, sort_keys=True) + "\n"); return {"path": p.name, "sha256": sha(p.read_bytes())}


def run(pkg, stage, packet, ev, source, git_root=True):
    cmd = [PY, str(pkg / "tools" / "r7_integrated.py"), stage, str(packet),
           "--evidence-root", str(ev), "--source-root", str(source)]
    if git_root:
        cmd += ["--git-root", str(GIT)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    try:
        out = json.loads(r.stdout)
    except Exception:
        out = {"status": "UNPARSED", "errors": [r.stdout[-500:], r.stderr[-500:]]}
    return out, r.returncode


def base_evidence(tmp):
    ev = pathlib.Path(tmp)
    ev.mkdir(parents=True, exist_ok=True)
    for name in ("source_authenticated_inventory.json", "release_register.json", "frame.json", "decision.json", "C.json"):
        shutil.copy2(EV / name, ev / name)
    shutil.copy2(SNAP / "package" / "02_BOUNDARY_CONTRACTS.json", ev / "02_BOUNDARY_CONTRACTS.json")
    return ev


def repaired_clean(ev):
    f = json.loads((EV / "frame.json").read_text()); d = json.loads((EV / "decision.json").read_text()); c = json.loads((EV / "C.json").read_text())
    f["boundary_contract"] = {"path": "02_BOUNDARY_CONTRACTS.json", "sha256": sha((ev / "02_BOUNDARY_CONTRACTS.json").read_bytes())}
    write(ev / "frame.json", f)
    d["common_frame"] = {"path": "frame.json", "sha256": sha((ev / "frame.json").read_bytes())}
    d["frame_sha256"] = jsha(f)
    write(ev / "decision.json", d)
    c["integrated_decision"] = {"path": "decision.json", "sha256": sha((ev / "decision.json").read_bytes())}
    c["integrated_decision_sha256"] = jsha(d)
    write(ev / "C.json", c)
    return f, d, c


def synthetic_spine():
    """Fabricated but schema-valid R5/R6 SPINE; no accepted artifact exists."""
    from importlib.util import spec_from_file_location, module_from_spec
    spec = spec_from_file_location("anvil_orig", ORIG / "R5_BASELINE" / "tools" / "anvil.py")
    m = module_from_spec(spec); spec.loader.exec_module(m)
    cov = {}
    for group, ids in m.REQUIRED.items():
        cov[group] = {}
        for rid in ids:
            rec = {"source_anchor": "SYNTHETIC/" + rid, "source_semantics": "Synthetic placeholder semantics for " + rid,
                   "consumer_or_hold": "No real consumer; synthetic test only", "negative_meaning": "Synthetic negative placeholder",
                   "architecture_effect": "Synthetic effect placeholder", "why": "Synthetic fixture reason placeholder",
                   "evidence_ids": ["SYNTH-" + rid], "decision_ids": ["D1"], "necessity": "MUST_PRESERVE_NOW",
                   "status": "PRESERVE_WITHOUT_BUILD"}
            if group == "PYAT_PC": rec.update(adopted=False, necessity="HISTORICAL_NOT_ADOPTED")
            if group == "P4R": rec.update(closed=False, necessity="HISTORICAL_PROOF_HELD")
            cov[group][rid] = rec
    return {"schema": "ANVIL_SPINE_R6", "coverage": cov, "outcome": "CONDITIONAL_CANDIDATE",
            "verdict_reason": "Synthetic source-consistent fixture used only to test laundering"}


def orig_base(ev):
    """Build old-gate frame/history/spine and decision/C pointing at them."""
    spine = synthetic_spine()
    sp = write(ev / "spine.json", spine)
    hist = {"schema": "ANVIL_R7_INHERITED_CONSERVATION", "source_authentication_origin": "AUTHORED_SYNTHETIC_FIXTURE",
            "source_authentication": "NOT_AUTHENTICATED_BY_LOCAL_CHECK", "source_spine_sha256": sp["sha256"],
            "transfer_method": "VERBATIM_R5_R6_SEMANTIC_COVERAGE_NO_RECLASSIFICATION", "coverage": spine["coverage"]}
    hp = write(ev / "history.json", hist)
    # reuse clean frame requirements but replace inventory/release/boundary with old fields
    f = json.loads((EV / "frame.json").read_text())
    f.pop("historical_inventory", None)
    f["release_register"] = {"path": "release_register.json", "sha256": sha((ev / "release_register.json").read_bytes())}
    f["boundary_contract"] = {"path": "02_BOUNDARY_CONTRACTS.json", "sha256": sha((ev / "02_BOUNDARY_CONTRACTS.json").read_bytes())}
    f["historical_conservation"] = hp; f["historical_source_spine"] = sp
    f["source_currentness"] = "Synthetic local fixture only; no live currentness is authenticated at all."
    write(ev / "frame.json", f)
    d = json.loads((EV / "decision.json").read_text())
    d["common_frame"] = {"path": "frame.json", "sha256": sha((ev / "frame.json").read_bytes())}
    d["frame_sha256"] = jsha(f)
    d["historical_identity_dispositions"] = []
    write(ev / "decision.json", d)
    c = json.loads((EV / "C.json").read_text())
    c["integrated_decision"] = {"path": "decision.json", "sha256": sha((ev / "decision.json").read_bytes())}
    c["integrated_decision_sha256"] = jsha(d)
    write(ev / "C.json", c)
    return f, d, c


def add_attack(rows, aid, target, expected, old_pass, new_pass, note, fixture_sha, old_err="", new_err=""):
    rows.append({"attack_id": aid, "target_contract": target, "fixture_input_sha256": fixture_sha,
                 "expected_verdict": expected,
                 "original_actual": "PASS" if old_pass else "RED",
                 "repaired_actual": "PASS" if new_pass else "RED",
                 "original_error": old_err[:300], "repaired_error": new_err[:300],
                 "verdict": ("REPAIRED_DETECTS" if old_pass and not new_pass else ("BOTH_DETECT" if not old_pass and not new_pass else ("RESIDUAL" if old_pass and new_pass else "REGRESSION"))),
                 "scope_note": note, "code_head": "D4A private repaired copy", "git_base": "cea2d4d3009e9087d2267e9d1f53bec28b730dc7"})


def main():
    rows = []
    with tempfile.TemporaryDirectory(prefix="anvil_d4_attacks_") as td:
        # A1 synthetic spine laundering
        ev = base_evidence(pathlib.Path(td) / "a1")
        f, d, c = orig_base(ev)
        o, _ = run(ORIG, "FRAME", ev / "frame.json", ev, SNAP)
        # repaired rejects the same synthetic frame because it lacks the inventory path
        r, _ = run(REP, "FRAME", ev / "frame.json", ev, SNAP)
        add_attack(rows, "A1", "history: accepted R5/R6 SPINE", "RED", o["status"] != "RED", r["status"] != "RED",
                   "A schema-valid synthetic SPINE with 118 fabricated semantic strings. Old gate accepted it; repaired gate requires a source-authenticated inventory or an accepted artifact anchor.",
                   sha((ev / "frame.json").read_bytes()), str(o.get("errors", [])[:1]), str(r.get("errors", [])[:1]))

        # A2 K3 raw row byte change
        ev = base_evidence(pathlib.Path(td) / "a2"); f, d, c = repaired_clean(ev)
        inv = json.loads((ev / "source_authenticated_inventory.json").read_text())
        inv["groups"]["K1_CAP"]["K1-CAP-01"]["row_sha256"] = "0" * 64
        write(ev / "source_authenticated_inventory.json", inv)
        f["historical_inventory"] = {"path": "source_authenticated_inventory.json", "sha256": sha((ev / "source_authenticated_inventory.json").read_bytes())}
        write(ev / "frame.json", f)
        o, _ = run(ORIG, "FRAME", ev / "frame.json", ev, SNAP)
        r, _ = run(REP, "FRAME", ev / "frame.json", ev, SNAP)
        add_attack(rows, "A2", "K3 exact TSV row bytes", "RED", o["status"] != "RED", r["status"] != "RED",
                   "K1-CAP-01 row hash changed without changing the snapshot. Old gate never read the K3 row; repaired gate rejects the row hash.",
                   sha((ev / "frame.json").read_bytes()), str(o.get("errors", [])[:1]), str(r.get("errors", [])[:1]))

        # A3 NOT_ADOPTED semantics changed while adopted=false
        ev = base_evidence(pathlib.Path(td) / "a3"); f, d, c = repaired_clean(ev)
        inv = json.loads((ev / "source_authenticated_inventory.json").read_text())
        inv["groups"]["PYAT_PC"]["PYAT-PC-R9-01"]["source_semantics"] = "ADOPTED as a current mandatory requirement"
        write(ev / "source_authenticated_inventory.json", inv)
        f["historical_inventory"] = {"path": "source_authenticated_inventory.json", "sha256": sha((ev / "source_authenticated_inventory.json").read_bytes())}
        write(ev / "frame.json", f)
        o, _ = run(ORIG, "FRAME", ev / "frame.json", ev, SNAP)
        r, _ = run(REP, "FRAME", ev / "frame.json", ev, SNAP)
        add_attack(rows, "A3", "K3 NOT_ADOPTED status", "RED", o["status"] != "RED", r["status"] != "RED",
                   "The 26 R15 proposal text is rewritten as ADOPTED while the boolean guard remains false. Old gate only checked the boolean; repaired gate checks the exact source row substring.",
                   sha((ev / "frame.json").read_bytes()), str(o.get("errors", [])[:1]), str(r.get("errors", [])[:1]))

        # A4 fabricated local evidence with matching hash, no frozen anchor
        ev = base_evidence(pathlib.Path(td) / "a4"); f, d, c = repaired_clean(ev)
        fake_snap = pathlib.Path(td) / "a4_snap"; shutil.copytree(SNAP, fake_snap)
        (fake_snap / "fake_source.md").write_text("This is a fabricated local source with a perfectly matching hash and quote.\n")
        bad = {"path": "fake_source.md", "sha256": sha((fake_snap / "fake_source.md").read_bytes()),
               "exact_excerpt": "fabricated local source with a perfectly matching hash", "source_class": "AUTHORED_FIXTURE"}
        f["requirements"][0]["evidence"] = bad
        write(ev / "frame.json", f)
        o, _ = run(ORIG, "FRAME", ev / "frame.json", ev, fake_snap)
        r, _ = run(REP, "FRAME", ev / "frame.json", ev, fake_snap)
        add_attack(rows, "A4", "source pin authenticity / unanchored producer", "RED", o["status"] != "RED", r["status"] != "RED",
                   "A local file with matching SHA and quote is offered as evidence. Old gate treats content-addressed local bytes as source; repaired gate requires a frozen Git/ZIP anchor.",
                   sha((ev / "frame.json").read_bytes()), str(o.get("errors", [])[:1]), str(r.get("errors", [])[:1]))

        # A5 omission of one negative from one 118 record
        ev = base_evidence(pathlib.Path(td) / "a5"); f, d, c = repaired_clean(ev)
        inv = json.loads((ev / "source_authenticated_inventory.json").read_text())
        inv["groups"]["K1_CAP"]["K1-CAP-02"].pop("negative_meaning")
        write(ev / "source_authenticated_inventory.json", inv)
        f["historical_inventory"] = {"path": "source_authenticated_inventory.json", "sha256": sha((ev / "source_authenticated_inventory.json").read_bytes())}
        write(ev / "frame.json", f)
        o, _ = run(ORIG, "FRAME", ev / "frame.json", ev, SNAP)
        r, _ = run(REP, "FRAME", ev / "frame.json", ev, SNAP)
        add_attack(rows, "A5", "118 negative evidence conservation", "RED", o["status"] != "RED", r["status"] != "RED",
                   "One K3 record's negative_meaning is omitted. Both gates reject a missing required record field; repaired also requires the remaining value to occur in the exact source row.",
                   sha((ev / "frame.json").read_bytes()), str(o.get("errors", [])[:1]), str(r.get("errors", [])[:1]))

        # A6 omission of a free requirement row (not one of the nine domains)
        ev = base_evidence(pathlib.Path(td) / "a6"); f, d, c = repaired_clean(ev)
        extra = copy.deepcopy(f["requirements"][0]); extra.update(id="R10", domain="F1_F4_ANALYTICS",
            substantive_requirement="A free requirement that can be silently deleted without losing a whole domain.",
            why_needed="Local fixture for requirement-set omission testing only.", loss_if_missing="The gate has no exact source-fixed requirement roster and can omit a free requirement.",
            first_consumer="local::fixture_requirement_for_omission_test", architectural_consequence="No architectural consequence beyond the local omission test.", proof_or_owner_hold="Local authored test only; no owner or science claim.")
        f["requirements"].append(extra); write(ev / "frame.json", f)
        # decision must cover R10 to pass; add disposition
        d["common_frame"] = {"path": "frame.json", "sha256": sha((ev / "frame.json").read_bytes())}
        d["frame_sha256"] = jsha(f); d["requirement_dispositions"].append(copy.deepcopy(d["requirement_dispositions"][0])); d["requirement_dispositions"][-1]["requirement_id"] = "R10"
        write(ev / "decision.json", d)
        o, _ = run(ORIG, "FRAME", ev / "frame.json", ev, SNAP); r, _ = run(REP, "FRAME", ev / "frame.json", ev, SNAP)
        add_attack(rows, "A6", "requirement set completeness", "RED", o["status"] != "RED", r["status"] != "RED",
                   "A non-domain requirement is deleted; the gate still passes because requirement rows are not fixed by the source inventory. RESIDUAL: no exact per-risk roster is enforced.",
                   sha((ev / "frame.json").read_bytes()), str(o.get("errors", [])[:1]), str(r.get("errors", [])[:1]))

        # A7 false 118 -> design coverage
        ev = base_evidence(pathlib.Path(td) / "a7"); f, d, c = repaired_clean(ev)
        d["historical_identity_dispositions"].pop()
        write(ev / "decision.json", d)
        o, _ = run(ORIG, "DECISION", ev / "decision.json", ev, SNAP); r, _ = run(REP, "DECISION", ev / "decision.json", ev, SNAP)
        add_attack(rows, "A7", "118 -> design/hold semantic conservation", "RED", o["status"] != "RED", r["status"] != "RED",
                   "One identity disposition is removed while the decision still says ready. Old gate never required 118 dispositions; repaired gate requires all 118 exact IDs.",
                   sha((ev / "decision.json").read_bytes()), str(o.get("errors", [])[:1]), str(r.get("errors", [])[:1]))

        # A8 false T boundary
        ev = base_evidence(pathlib.Path(td) / "a8"); f, d, c = repaired_clean(ev)
        f["boundary_contracts"][3]["producer"] = "survey respondents directly write objective material power"
        write(ev / "frame.json", f)
        o, _ = run(ORIG, "FRAME", ev / "frame.json", ev, SNAP); r, _ = run(REP, "FRAME", ev / "frame.json", ev, SNAP)
        add_attack(rows, "A8", "T1-T7 typed boundary contracts", "RED", o["status"] != "RED", r["status"] != "RED",
                   "T4's producer is rewritten to collapse survey evidence into material power. Old gate had no T contract check; repaired gate compares all seven exact fields.",
                   sha((ev / "frame.json").read_bytes()), str(o.get("errors", [])[:1]), str(r.get("errors", [])[:1]))

        # A9 stale/revoked release
        ev = base_evidence(pathlib.Path(td) / "a9"); f, d, c = repaired_clean(ev)
        rel = json.loads((ev / "release_register.json").read_text())
        rel["revoked"] = [{"name": "SUPPLIED_ZIP", "sha256": "526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332", "reason": "simulated revocation"}]
        write(ev / "release_register.json", rel)
        f["release_register"] = {"path": "release_register.json", "sha256": sha((ev / "release_register.json").read_bytes())}
        write(ev / "frame.json", f)
        o, _ = run(ORIG, "FRAME", ev / "frame.json", ev, SNAP); r, _ = run(REP, "FRAME", ev / "frame.json", ev, SNAP)
        add_attack(rows, "A9", "stale/revoked release", "RED", o["status"] != "RED", r["status"] != "RED",
                   "The supplied ZIP pin is marked revoked, but a requirement still cites it. Old gate has no release register; repaired gate rejects any revoked SHA in evidence.",
                   sha((ev / "frame.json").read_bytes()), str(o.get("errors", [])[:1]), str(r.get("errors", [])[:1]))

        # A10 fabricated source -> actor knowledge
        ev = base_evidence(pathlib.Path(td) / "a10"); f, d, c = repaired_clean(ev)
        d["actor_world_boundary"]["survey_implies_actor_knowledge"] = True
        write(ev / "decision.json", d)
        o, _ = run(ORIG, "DECISION", ev / "decision.json", ev, SNAP); r, _ = run(REP, "DECISION", ev / "decision.json", ev, SNAP)
        add_attack(rows, "A10", "actor/world firewall", "RED", o["status"] != "RED", r["status"] != "RED",
                   "The decision asserts that a survey response directly gives actor knowledge. Old gate cannot see the field; repaired gate rejects the explicit boundary breach.",
                   sha((ev / "decision.json").read_bytes()), str(o.get("errors", [])[:1]), str(r.get("errors", [])[:1]))

        # A11 builder card with filename-only consumer and fabricated receipt
        ev = base_evidence(pathlib.Path(td) / "a11"); f, d, c = repaired_clean(ev)
        fake_src = pathlib.Path(td) / "a11_src"; (fake_src / "rawlsing_next").mkdir(parents=True)
        fake_py = fake_src / "rawlsing_next" / "pre553_empirical_query.py"
        fake_py.write_text("def execute_empirical_query(*args, **kwargs):\n    return None\n")
        fh = sha(fake_py.read_bytes())
        c["builder_cards"][0] = {"id": "current", "domain": "CURRENT_FIRST_CONSUMER", "grade": "EXECUTED_FIRST_READER_PROOF",
            "producer_symbol": "rawlsing_next/pre553_empirical_query.py::execute_empirical_query",
            "consumer_symbol": "rawlsing_next/pre553_empirical_query.py::execute_empirical_query",
            "source_head": "cea2d4d3009e9087d2267e9d1f53bec28b730dc7",
            "producer_sha256": fh, "consumer_sha256": fh,
            "test_command": "python3 -m unittest rawlsing_next.tests.test_pre553_empirical_query",
            "first_consumer": "rawlsing_next/pre553_empirical_query.py",
            "executed_test_receipt": None}
        receipt = {"schema": "ANVIL_R7_EXECUTION_TEST_RECEIPT", "command": c["builder_cards"][0]["test_command"],
                   "exit_code": 0, "execution_kind": "REAL_FIRST_READER", "first_consumer_effect": "looks changed",
                   "negative_refusal": "looks refused", "restore_replay": "looks restored",
                   "runner_code_head": "cea2d4d3009e9087d2267e9d1f53bec28b730dc7",
                   "source_or_fixture_sha256": "b" * 64}
        rp = write(ev / "receipt.json", receipt)
        c["builder_cards"][0]["executed_test_receipt"] = rp
        write(ev / "C.json", c)
        o, _ = run(ORIG, "C_INTEGRATED", ev / "C.json", ev, fake_src); r, _ = run(REP, "C_INTEGRATED", ev / "C.json", ev, fake_src)
        add_attack(rows, "A11", "builder card / first consumer", "RED", o["status"] != "RED", r["status"] != "RED",
                   "A fabricated receipt with no raw log and a filename-only first consumer is supplied. Old gate checks only presence; repaired gate requires executable path::symbol, argv, raw log and stdout hash.",
                   sha((ev / "C.json").read_bytes()), str(o.get("errors", [])[:1]), str(r.get("errors", [])[:1]))

        # A12 fabricated H1
        ev = base_evidence(pathlib.Path(td) / "a12"); f, d, c = repaired_clean(ev)
        d["protected_h1_claimed"] = True; c["protected_h1_claimed"] = True
        write(ev / "decision.json", d); write(ev / "C.json", c)
        o, _ = run(ORIG, "DECISION", ev / "decision.json", ev, SNAP); r, _ = run(REP, "DECISION", ev / "decision.json", ev, SNAP)
        add_attack(rows, "A12", "protected H1 authority", "RED", o["status"] != "RED", r["status"] != "RED",
                   "The author claims protected H1 in the decision. Old gate has no H1 field; repaired gate rejects the false authority claim.",
                   sha((ev / "decision.json").read_bytes()), str(o.get("errors", [])[:1]), str(r.get("errors", [])[:1]))

        # A13 118 printed with generic semantics
        ev = base_evidence(pathlib.Path(td) / "a13"); f, d, c = repaired_clean(ev)
        inv = json.loads((ev / "source_authenticated_inventory.json").read_text())
        for group, recs in inv["groups"].items():
            for rid, rec in recs.items():
                rec["negative_meaning"] = "This identity is preserved and there is no meaningful loss in this record at all."
        write(ev / "source_authenticated_inventory.json", inv)
        f["historical_inventory"] = {"path": "source_authenticated_inventory.json", "sha256": sha((ev / "source_authenticated_inventory.json").read_bytes())}
        write(ev / "frame.json", f)
        o, _ = run(ORIG, "FRAME", ev / "frame.json", ev, SNAP); r, _ = run(REP, "FRAME", ev / "frame.json", ev, SNAP)
        add_attack(rows, "A13", "118 identity printed vs meaningful conservation", "RED", o["status"] != "RED", r["status"] != "RED",
                   "All 118 negative meanings are replaced with one generic no-loss sentence. Old gate never sees the inventory; repaired gate requires K3 negatives to occur in the exact protected row.",
                   sha((ev / "frame.json").read_bytes()), str(o.get("errors", [])[:1]), str(r.get("errors", [])[:1]))

        # Clean restoration on the private repaired copy
        ev = base_evidence(pathlib.Path(td) / "clean"); f, d, c = repaired_clean(ev)
        fr, _ = run(REP, "FRAME", ev / "frame.json", ev, SNAP)
        dr, _ = run(REP, "DECISION", ev / "decision.json", ev, SNAP)
        cr, _ = run(REP, "C_INTEGRATED", ev / "C.json", ev, SNAP)
        rows.append({"attack_id": "RESTORE", "target_contract": "clean source-authenticated fixture", "fixture_input_sha256": sha((ev / "decision.json").read_bytes()),
                     "expected_verdict": "PASS_LOCAL_PENDING_C", "original_actual": "N/A", "repaired_actual": "PASS" if all(x["status"] != "RED" for x in (fr, dr, cr)) else "RED",
                     "original_error": "", "repaired_error": "; ".join(str(x.get("errors", [])[:1]) for x in (fr, dr, cr)),
                     "verdict": "CLEAN_RESTORATION", "scope_note": "No native/owner/science/H1 acceptance; only local structural and source-byte checks.",
                     "code_head": "D4A private repaired copy", "git_base": "cea2d4d3009e9087d2267e9d1f53bec28b730dc7"})
    # write TSV
    cols = ["attack_id", "target_contract", "fixture_input_sha256", "expected_verdict", "original_actual", "repaired_actual",
            "original_error", "repaired_error", "verdict", "scope_note", "code_head", "git_base"]
    out = ROOT / "HOSTILE_ATTACK_MATRIX.tsv"
    with out.open("w") as fh:
        fh.write("\t".join(cols) + "\n")
        for row in rows:
            fh.write("\t".join(str(row.get(c, "")).replace("\t", " ").replace("\n", " ") for c in cols) + "\n")
    print(json.dumps({"rows": len(rows), "matrix": str(out), "sha256": sha(out.read_bytes())}, indent=2))
    for row in rows:
        print(row["attack_id"], row["original_actual"], "->", row["repaired_actual"], row["verdict"])


if __name__ == "__main__":
    main()
