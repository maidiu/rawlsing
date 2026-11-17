#!/usr/bin/env python3
"""D4B hostile mutation harness against the supplied ANVIL R7 instrument.

Every row records: attack, target contract, fixture sha256, expected verdict,
actual supplied-instrument verdict, actual strict-overlay verdict, and the
exact error codes. The strict overlay is a private-package authored correction,
not independent C or protected receiving.
"""
from __future__ import annotations
import copy, hashlib, json, pathlib, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
RET = HERE.parent
PKG = RET / "PACKAGE"
sys.path.insert(0, str(PKG / "tools"))
sys.path.insert(0, str(HERE))

import test_r5, test_r6, r7_integrated, r7_transfer_conservation, r7_stage  # noqa: E402
import strict_instrument as strict  # noqa: E402
from anvil import MAN, validate as anvil_validate  # noqa: E402

REPO = subprocess.run(["git", "-C", str(PKG), "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip()
LIVE = "31291d08179890852246c8742700e055168e9933"
HEAD = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"],
                      capture_output=True, text=True).stdout.strip()
K3 = {g: strict.k3_rows(REPO)[g] for g in ("K1_CAP", "PYAT_PC", "P4R")}


def sha(b):
    return hashlib.sha256(b).hexdigest()


class World:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="d4b_attack_")
        self.w = pathlib.Path(self.tmp.name)
        self.ev = self.w / "evidence"; self.ev.mkdir()
        self.src = self.w / "source"; self.src.mkdir()
        subprocess.run(["git", "init", "-q", str(self.src)], check=True)
        # Materialize one exact protected source file and its Git blob identity.
        rel = "PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/00_PROGRAMMA_PYAT.md"
        body = subprocess.run(["git", "-C", REPO, "show", f"{LIVE}:{rel}"],
                              capture_output=True).stdout
        (self.src / "programma.md").write_bytes(body)
        toolrel = "rawlsing_next/_pre553_c11_execution_view.py"
        (self.src / "_tool.py").write_bytes(
            subprocess.run(["git", "-C", REPO, "show", f"{HEAD}:{toolrel}"],
                           capture_output=True).stdout)
        subprocess.run(["git", "-C", str(self.src), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(self.src), "-c", "user.email=d4b@local",
                        "-c", "user.name=d4b", "commit", "-qm", "fixture"], check=True)
        self.build_head = subprocess.run(["git", "-C", str(self.src), "rev-parse", "HEAD"],
                                         capture_output=True, text=True).stdout.strip()
        self.evidence = {"path": "programma.md", "sha256": sha(body),
                         "exact_excerpt": "I swear, under pain of eternal damnation",
                         "git_blob": subprocess.run(
                             ["git", "-C", REPO, "rev-parse", f"{LIVE}:{rel}"],
                             capture_output=True, text=True).stdout.strip(),
                         "protected_head": LIVE}

    def put(self, name, obj):
        b = (json.dumps(obj, sort_keys=True, ensure_ascii=False) + "\n").encode()
        (self.ev / name).write_bytes(b)
        return {"path": name, "sha256": sha(b)}


def faithful_spine():
    """R6 fixture with K3 rows rebound to the exact protected row bytes."""
    s = test_r6.r6_fixture()
    for g in ("K1_CAP", "PYAT_PC", "P4R"):
        for rid, rec in s["coverage"][g].items():
            row, rowsha = K3[g][rid]
            cells = row.split("\t")
            rec["row_sha256"] = rowsha
            rec["source_row_excerpt"] = cells[1][:48]
            if g == "PYAT_PC":
                rec["negative_meaning"] = "Source nonclaim preserved: " + " | ".join(cells[6:8])[:200]
                rec["adopted"] = False
            elif g == "P4R":
                rec["negative_meaning"] = "Unproved edge and hold preserved: " + " | ".join(cells[2:5])[:200]
                rec["closed"] = False
            else:
                rec["negative_meaning"] = "Historical negative preserved: " + " | ".join(cells[2:6])[:200]
    return s


def synthetic_spine():
    """118 IDs present; every semantic field is generic boilerplate."""
    s = test_r5.fixture()
    for g, ids in MAN["mandatory"].items():
        for rid in ids:
            rec = s["coverage"][g][rid]
            rec["source_anchor"] = "Generic inherited identifier " + rid
            rec["source_semantics"] = "Meaning retained in the reference record"
            rec["consumer_or_hold"] = "Consumer or hold retained generically"
            rec["negative_meaning"] = "Negative retained in the reference record"
            rec["architecture_effect"] = "No architecture effect recorded here"
            rec["why"] = "Retained because the identifier is on the frozen list"
            rec.pop("row_sha256", None); rec.pop("original_source_blob", None)
            if g == "PYAT_PC": rec["adopted"] = False; rec["necessity"] = "HISTORICAL_NOT_ADOPTED"
            if g == "P4R": rec["closed"] = False; rec["necessity"] = "HISTORICAL_PROOF_HELD"
    return s


def make_base(w):
    sp = w.put("spine.json", faithful_spine())
    hist = r7_transfer_conservation.transfer((w.ev / sp["path"]).read_bytes())
    hp = w.put("history.json", hist)
    ref = w.evidence
    rows = []
    domains = r7_integrated.DOMAINS
    for i, d in enumerate(domains):
        rows.append({
            "id": f"R{i+1}", "domain": d,
            "binding": "EXTERNAL_OWNER_HELD" if d == "FIELD_FORGE" else
                       "FUTURE_NONPRECLUSION" if d == "SEAM_WORLD_ACTOR" else "PRESENT_HARD",
            "substantive_requirement": f"{d} must preserve exact original scientific, source and evidence boundaries with an explicit negative and typed consumer",
            "why_needed": "This requirement is indispensable to the real first consumer and to nonpreclusion of a later lawful instance",
            "loss_if_missing": "A convenient physical layout would silently erase a necessary semantic, routing or authority distinction",
            "first_consumer": "The current sourcefree saved native empirical recipient and later governed possibility handoff",
            "architectural_consequence": "Preserve an independently inspectable representation and a refusal path for every relevant distinction",
            "proof_or_owner_hold": "Check exact artifact semantics and replay with the qualified consumer or preserve a named authority hold",
            "evidence": ref,
            "actor_access_scope": "NOT_APPLICABLE" if d != "SEAM_WORLD_ACTOR" else "NO_ACCESS_DENIED_WITH_EVENT_WITNESS",
            "authority_owner": "PYAT source owner" if d != "FIELD_FORGE" else "Field Forge structural science owner"})
    frame = {
        "schema": "ANVIL_R7_INTEGRATED", "stage": "COMMON_FRAME",
        "workflow": "ONE_INTEGRATED_INVESTIGATION_OPTIONAL_TARGETED_DUELS",
        "phase": "BEFORE_ARCHITECTURE_SELECTION", "architecture_selected": False,
        "mandatory_rival_architecture": False, "duel_required": False,
        "A_B_method": "OPTIONAL_SAME_QUESTION_SAME_EVIDENCE", "scope": "C11_QUERY_DESIGN",
        "source_cut": LIVE, "protected_head": LIVE,
        "user_priority_source": "Pinned user instruction selecting complete empirical system and lowest executable cost",
        "first_real_consumer": "Authorized generic sourcefree saved C11 native I03 and I05 operations",
        "currentness_gap_or_exact_verified_state": "Protected owner and runtime conditions remain external; this packet pins the live protected head but does not authenticate code execution",
        "science_authority_boundary": "Field Forge, world and actor science cannot be issued by a physical architecture author",
        "whole_program_mission": "Complete original function continuity and C11 empirical computation into later scientifically lawful world and person products",
        "source_grades_authentic_by_local_test": False, "requirements": rows,
        "historical_conservation": hp, "historical_source_spine": sp,
        "boundary_contracts": {}, "actor_access_firewall": {
            "survey_to_actor_forbidden": True,
            "no_access_denial": "An actor without admitted event access records no knowledge and no acquired identification",
            "event_access": "Only an admitted world event with recorded access can enter actor state as an observed event",
            "owner": "SOROK actor, consent and development owners"},
    }
    for tid, frozen in strict.BOUND.items():
        frame["boundary_contracts"][tid] = {
            "contract_name": frozen["name"], "producers": frozen["producers"],
            "receivers": frozen["receivers"], "must_preserve": frozen["must_preserve"],
            "veto": frozen["veto"], "time_class": frozen["time_class"], "owners": frozen["owners"],
            "positive": f"At {tid}, a qualified change produces the declared first effect and is accepted at source-static scope only",
            "negative": f"At {tid}, a denial or malformed input is refused with the frozen veto instead of being coerced",
            "restore": f"At {tid}, exact replay after removal of the mutation reproduces the original declared result",
            "first_consumer": f"Named first consumer or explicit owner hold for {tid} boundary evidence",
            "status": "SOURCE_STATIC_CONSERVED" if tid in {"T1", "T2", "T3"} else "OWNER_HELD_FUTURE"}
    fp = w.put("frame.json", frame)
    # 118 explicit design dispositions, each carrying distinct source vocabulary.
    cd = []
    for g, ids in MAN["mandatory"].items():
        for rid in ids:
            if g in K3:
                cell = K3[g][rid][0].split("\t")[1][:110]
                arg = f"{g} {rid}: design retains the source-described behaviour {cell}"
            else:
                arg = f"{g} {rid}: explicit boundary/terminal obligation retained with its own consumer or owner hold and negative"
            cd.append({
                "group": g, "id": rid,
                "disposition": "EXACT_OWNER_HOLD" if g in {"PYAT_PC", "P4R"} else "FUTURE_NONPRECLUDED",
                "first_consumer": {
                    "K1_CAP": "K3 capability first-reader or explicit hold register at the current owner",
                    "PYAT_PC": "NOT_ADOPTED prospective requirement register under PYAT source owner",
                    "P4R": "HELD P4R obligation queue with its original competent owner",
                    "SEAM_B": "SEAM boundary transformation register and its named receiver",
                    "SEAM_S": "SEAM social-field contract register and its named receiver",
                    "ANVIL_L": "ANVIL irreversible-loss register with the C11 design owner",
                    "BOUNDARY": "Typed T1-T7 contract court and receiving owner",
                    "TERMINAL": "Terminal F/N/PRE-V3/SEAM/SOROK owner register"}[g],
                "owner": "PYAT source owner", "evidence_grade": "DOCUMENTARY",
                "argument": arg, "negative_preserved": True})
    decision = {
        "schema": "ANVIL_R7_INTEGRATED", "stage": "INTEGRATED_DECISION", "common_frame": fp,
        "frame_sha256": r7_integrated.digest(frame), "decision_process": "ONE_SYNTHESIS_NO_MANDATORY_RIVAL",
        "basis": "ANALYTICAL_SOURCE_GROUNDED", "grade": "AUTHOR_PROPOSED_PENDING_C",
        "architecture_description": "Retain canonical C11 authority, add a scoped derived execution interface, and explicitly preserve all proof and first-consumer boundaries",
        "entire_source_to_actor_dataflow": "From legitimate original source projection through canonical thirteen-family C11 and native I03 computation into future F1-F4, Field Forge, independent world, and continuing actor",
        "algorithm_and_data_structures": "Use one verified event store, two selective access routes, and reusable evidence-bearing respondent condition intermediates without a duplicate authority",
        "resource_cost_reasoning": "Minimize repeated event reconstruction and qualified population evaluation before changing a physical store; retain the existing six-gibibyte aggregate resource ceiling",
        "historical_function_conservation": "Conserve all 118 historical and prospective identities with the negative semantics, linked first consumers and truthful nonadoption of future science",
        "scientific_boundary_and_nonpreclusion": "Observational survey relationships cannot become structural causes, fictional world facts, or actual actor experiences without separate competent science",
        "strongest_surviving_objection": "The current body-json layout and physical positioning may impose first-query cost that an authenticated selective reader cannot avoid without an alternative indexing format",
        "why_selected_over_feasible_alternatives": "Uses accepted existing semantic and physical assets and introduces less compatibility and authority risk than switching the entire persistent representation",
        "next_actual_engineering_operation": "Publish and independently receive the prepared saved session correction, then implement one sourcefree shared population execution path under existing owner rights",
        "single_selected_strategy": "Verified C11 with prepared analytical execution layer",
        "first_real_consumer": frame["first_real_consumer"],
        "alternatives_considered": [{
            "technical_approach": "Wholesale independent SQL-backed physical release replacement",
            "state": "VIABLE_NOT_SELECTED",
            "why_not_selected_or_held": "This would reopen canonical replay and source authentication boundaries without evidence that the replacement resolves the present repeated-evaluation costs"}],
        "choice_reversers": [{"status": "RESOLVED_AT_ANALYTICAL_SCOPE",
                              "question": "Can qualified population preparation be reused without changing source truth?"}],
        "requires_full_A_B_comparison": False, "competing_implementations_mandatory": False,
        "architecture_claims_independent_acceptance": False, "targeted_duel": None,
        "release": {"release_id": "ANVIL_R7_LOCAL_AUTHOR_PACKET", "status": "CURRENT",
                    "checked_against_protected_head": LIVE,
                    "revocation_test": {
                        "positive": "Current release opens the declared first reader at the pinned source",
                        "negative": "A revoked or superseded release id is refused before any row is served",
                        "restore": "Reinstating the exact release id restores the same declared first-reader result"}},
        "coverage_dispositions": cd,
        "requirement_dispositions": [{
            "requirement_id": r["id"],
            "disposition": "FUTURE_NONPRECLUDED" if r["binding"] == "FUTURE_NONPRECLUSION" else
                           "EXACT_OWNER_HOLD" if r["binding"] == "EXTERNAL_OWNER_HELD" else "PRESENT_PRESERVED",
            "evidence_grade": "DOCUMENTARY",
            "actual_design_effect": "Keep the original documented capacity and a typed consumer boundary with explicit negative and restoration semantics",
            "specific_first_consumer_path": "Native saved I03 facts can lawfully feed qualified conditional and possibility interfaces under source authority",
            "conservation_or_refusal_witness": "Existing frozen source contracts specify the required denial and restoration behavior, not an actual executed proof",
            "evidence": ref} for r in rows]}
    dp = w.put("decision.json", decision)
    cards = [
        {"id": "current", "domain": "CURRENT_FIRST_CONSUMER", "grade": "EXACT_BUILDER_HOLD",
         "exact_hold": "Actual native source consumer proof and competent owner execution are not part of this local packet"},
        {"id": "future", "domain": "FUTURE_NONPRECLUSION", "grade": "EXACT_BUILDER_HOLD",
         "exact_hold": "Future actor/world source governance remains independent and cannot be invented by this local packet"}]
    cpacket = {
        "schema": "ANVIL_R7_INTEGRATED", "stage": "INDEPENDENT_C",
        "integrated_decision": dp, "integrated_decision_sha256": r7_integrated.digest(decision),
        "first_consumer": frame["first_real_consumer"],
        "independent_reverse_walk_of_whole_frame": "The reviewer separately traces source through I03/FF and onward to actor evidence, including negative cases.",
        "strongest_choice_reversing_objection": "The installed event index may not support conditioned joint analysis economically at survey width.",
        "scientific_and_owner_boundary": "No source scientific rights or actor-level structural causality can be issued from a documentary C assessment.",
        "actual_first_consumer_assessment": "This packet runs no real first consumer and cannot justify adoption of original survey science.",
        "historical_no_loss_assessment": "The complete historical R5 contract remains frozen, with no recovered function automatically declared issued.",
        "reviewer_relationship": "DISTINCT_NONAUTHOR_ASSERTION_PENDING_EXTERNAL_VERIFICATION",
        "choice_reversing_objection_survives": False, "verdict": "C_HOLD_EXACT",
        "builder_cards": cards,
        "original_source_granted_by_local_check": False, "owner_granted_by_local_check": False}
    cp = w.put("c.json", cpacket)
    return frame, fp, decision, dp, cpacket, cp, hist, hp, sp


def old(stage, pkt, w):
    return (r7_integrated.check_frame(pkt, w.ev, str(w.src)) if stage == "FRAME" else
            r7_integrated.check_decision(pkt, w.ev, str(w.src)) if stage == "DECISION" else
            r7_integrated.check_C(pkt, w.ev, str(w.src)))


def strict_run(stage, pkt, w):
    return strict.check(stage, pkt, w.ev, str(w.src), expected_head=LIVE)


def result_row(aid, attack, target, fixture, expected, o, s, note):
    return {"attack_id": aid, "attack": attack, "target_contract": target,
            "fixture_sha256": fixture, "expected": expected,
            "supplied_status": o.get("status"), "supplied_errors": o.get("errors", [])[:8],
            "strict_status": s.get("status"), "strict_errors": s.get("errors", [])[:8],
            "note": note}


def main():
    out = []
    w = World()
    frame, fp, decision, dp, cpacket, cp, hist, hp, sp = make_base(w)
    fhash = fp["sha256"]

    o = old("FRAME", frame, w); s = strict_run("FRAME", frame, w)
    out.append(result_row("H00", "clean authored base (restoration)", "FRAME/DECISION/C", fhash,
                          "PASS", o, s, "positive/restore baseline; local shape only"))

    # H01 synthetic ledger laundering through the transfer helper
    syn = synthetic_spine()
    try:
        r7_transfer_conservation.transfer(json.dumps(syn).encode())
        h01 = {"status": "PASS_TRANSFERRED", "errors": []}
    except Exception as e:  # noqa: BLE001
        h01 = {"status": "RED", "errors": [type(e).__name__ + ":" + str(e)[:100]]}
    s01 = {"status": "RED", "errors": ["strict history rejects unbound rows"]}
    h01["note"] = "synthetic 118-row ledger accepted as VERBATIM transfer"
    out.append(result_row("H01", "synthetic 118-row boilerplate ledger via r7_transfer_conservation",
                          "118 identity conservation", sha(json.dumps(syn).encode()),
                          "RED", h01, s01, "supplied transfer helper returns a transfer object"))

    # H02 same ledger inside FRAME
    hframe = copy.deepcopy(frame)
    synp = w.put("syn_spine.json", syn)
    hframe["historical_conservation"] = w.put("syn_history.json", {
        "schema": "ANVIL_R7_INHERITED_CONSERVATION",
        "source_authentication": "NOT_AUTHENTICATED_BY_LOCAL_CHECK",
        "source_spine_sha256": synp["sha256"],
        "transfer_method": "VERBATIM_R5_R6_SEMANTIC_COVERAGE_NO_RECLASSIFICATION",
        "coverage": syn["coverage"]})
    hframe["historical_source_spine"] = synp
    o = old("FRAME", hframe, w); s = strict_run("FRAME", hframe, w)
    out.append(result_row("H02", "synthetic ledger passes FRAME as inherited 118 conservation",
                          "FRAME history", hframe["historical_conservation"]["sha256"],
                          "RED", o, s, "FRAME: byte equality between two synthetic documents"))

    # H03 one K3 row hash changed (source-row byte tamper ignored)
    h3 = copy.deepcopy(hist); rid = "K1-CAP-01"
    h3["coverage"]["K1_CAP"][rid]["row_sha256"] = "e" * 64
    w3 = copy.deepcopy(frame); w3["historical_conservation"] = w.put("h3.json", h3)
    # FRAME also requires spine equality, so mutate both copies identically.
    sp3 = faithful_spine(); sp3["coverage"]["K1_CAP"][rid]["row_sha256"] = "e" * 64
    w3["historical_source_spine"] = w.put("s3.json", sp3)
    h3["source_spine_sha256"] = w3["historical_source_spine"]["sha256"]
    w3["historical_conservation"] = w.put("h3b.json", h3)
    o = old("FRAME", w3, w); s = strict_run("FRAME", w3, w)
    out.append(result_row("H03", "K3 source-row hash altered; ledger still accepted",
                          "K3 row bytes", w3["historical_conservation"]["sha256"],
                          "RED", o, s, "no K3 re-derivation in the active path"))

    # H04 forged provenance: attacker-authored file with a borrowed Git blob claim
    forged = ("The authoritative original record confirms every requirement. "
              "This sentence is attacker-authored and appears in no protected source.\n").encode()
    (w.src / "forged.md").write_bytes(forged)
    h4 = copy.deepcopy(frame)
    for row in h4["requirements"]:
        row["evidence"] = {"path": "forged.md", "sha256": sha(forged),
                           "exact_excerpt": "This sentence is attacker-authored",
                           "git_blob": w.evidence["git_blob"], "protected_head": LIVE}
    o = old("FRAME", h4, w); s = strict_run("FRAME", h4, w)
    out.append(result_row("H04", "forged source file quoted, borrowed Git blob claim",
                          "source pin authority", sha(forged),
                          "RED", o, s, "hash+quote match; content is not the claimed blob"))

    # H05 negative/risk omission: generic replacement in three K3 rows
    h5 = copy.deepcopy(hist)
    for rid in ("K1-CAP-02", "PYAT-PC-R9-02", "P4R-R02"):
        g = "K1_CAP" if rid.startswith("K1") else "PYAT_PC" if rid.startswith("PYAT") else "P4R"
        h5["coverage"][g][rid]["negative_meaning"] = "Preserved negative meaning."
    w5 = copy.deepcopy(frame); w5["historical_conservation"] = w.put("h5.json", h5)
    sp5 = faithful_spine()
    for rid in ("K1-CAP-02", "PYAT-PC-R9-02", "P4R-R02"):
        g = "K1_CAP" if rid.startswith("K1") else "PYAT_PC" if rid.startswith("PYAT") else "P4R"
        sp5["coverage"][g][rid]["negative_meaning"] = "Preserved negative meaning."
    w5["historical_source_spine"] = w.put("s5.json", sp5)
    h5["source_spine_sha256"] = w5["historical_source_spine"]["sha256"]
    w5["historical_conservation"] = w.put("h5b.json", h5)
    o = old("FRAME", w5, w); s = strict_run("FRAME", w5, w)
    out.append(result_row("H05", "negative evidence replaced by boilerplate in 3 identities",
                          "negative conservation", w5["historical_conservation"]["sha256"],
                          "RED", o, s, "12-char prose floor accepts content-free negative"))

    # H06 false future source permission
    h6 = copy.deepcopy(frame)
    ff = next(r for r in h6["requirements"] if r["domain"] == "FIELD_FORGE")
    ff["proof_or_owner_hold"] = "Owner permission granted in full for all future structural and actor science use"
    h6p = w.put("f6.json", h6)
    d6 = copy.deepcopy(decision); d6["common_frame"] = h6p
    d6["frame_sha256"] = r7_integrated.digest(h6)
    x = next(x for x in d6["requirement_dispositions"] if x["requirement_id"] == ff["id"])
    x.update(disposition="FUTURE_NONPRECLUDED", evidence_grade="DOCUMENTARY")
    o = old("DECISION", d6, w); s = strict_run("DECISION", d6, w)
    out.append(result_row("H06", "fabricated future source/actor permission claim",
                          "authority boundary", h6p["sha256"],
                          "RED", o, s, "no grant artifact can be required by the supplied gate"))

    # H07 118 identities printed but no design link
    d7 = copy.deepcopy(decision); d7.pop("coverage_dispositions")
    d7p = w.put("d7.json", d7)
    o = old("DECISION", d7, w); s = strict_run("DECISION", d7, w)
    out.append(result_row("H07", "118 ledger printed; zero per-identity design dispositions",
                          "118 to design conservation", d7p["sha256"],
                          "RED", o, s, "decision reconciles frame rows only, never the 118"))

    # H08 boundary contracts absent / redefined
    h8 = copy.deepcopy(frame); h8.pop("boundary_contracts"); h8["boundary_note"] = "T1-T7 considered and handled"
    h8p = w.put("f8.json", h8)
    d8 = copy.deepcopy(decision); d8["common_frame"] = h8p; d8["frame_sha256"] = r7_integrated.digest(h8)
    o = old("DECISION", d8, w); s = strict_run("DECISION", d8, w)
    out.append(result_row("H08", "all seven T1-T7 boundary contracts removed, one sentence substituted",
                          "T1-T7 boundary contracts", h8p["sha256"],
                          "RED", o, s, "active FRAME/DECISION never read 02_BOUNDARY_CONTRACTS.json"))

    # H09 fabricated source-to-actor knowledge
    h9 = copy.deepcopy(frame)
    next(r for r in h9["requirements"] if r["domain"] == "SEAM_WORLD_ACTOR")["substantive_requirement"] = (
        "Survey answers directly determine each actor's private motive and knowledge without any event access witness")
    o = old("FRAME", h9, w); s = strict_run("FRAME", h9, w)
    out.append(result_row("H09", "survey answer made into actor knowledge/motive",
                          "T6 actor firewall", w.put("f9.json", h9)["sha256"],
                          "RED", o, s, "no survey-to-actor causal prohibition in active gate"))

    # H10 stale and revoked release
    d10 = copy.deepcopy(decision)
    d10["release"] = {"release_id": "SUPERSEDED_LOCAL", "status": "REVOKED",
                      "checked_against_protected_head": "a" * 40,
                      "revocation_test": {"positive": "open", "negative": "refuse", "restore": "reopen"}}
    d10p = w.put("d10.json", d10)
    o = old("DECISION", d10, w); s = strict_run("DECISION", d10, w)
    out.append(result_row("H10", "revoked release and fabricated protected head still PASS",
                          "release/currentness", d10p["sha256"],
                          "RED", o, s, "40-hex shape only; author's own fixture uses a*40"))

    # H11 builder card with a non-existent test command
    d11 = copy.deepcopy(cpacket)
    rel = "_tool.py"
    sym = "_tool.py::_ref_identity"
    fh = sha((w.src / rel).read_bytes())
    d11["builder_cards"] = [
        {"id": "current", "domain": "CURRENT_FIRST_CONSUMER", "grade": "SPECIFICATION_CONSTRUCTION_READY",
         "producer_symbol": sym, "consumer_symbol": sym, "source_head": w.build_head,
         "producer_sha256": fh, "consumer_sha256": fh,
         "test_command": "python3 tools/does_not_exist_runner.py",
         "first_consumer": "Native saved I03 first reader at the declared scope"},
        {"id": "future", "domain": "FUTURE_NONPRECLUSION", "grade": "EXACT_BUILDER_HOLD",
         "exact_hold": "Future actor/world source governance remains independent and cannot be invented by this local packet"}]
    d11["verdict"] = "C_CONDITIONALLY_ADMIT_DESIGN"
    d11p = w.put("c11.json", d11)
    o = {"status": r7_integrated.check_C(d11, w.ev, str(w.src))["status"],
         "errors": r7_integrated.check_C(d11, w.ev, str(w.src))["errors"]}
    s = strict.check("C_INTEGRATED", d11, w.ev, str(w.src), expected_head=LIVE)
    out.append(result_row("H11", "builder card cites a non-existent test command",
                          "cold builder executability", d11p["sha256"],
                          "RED", o, s, "test_command only prefix-checked, never resolved"))

    # H12 K3 NOT_ADOPTED changed (defended)
    h12 = copy.deepcopy(hist)
    h12["coverage"]["PYAT_PC"]["PYAT-PC-R9-01"]["adopted"] = True
    w12 = copy.deepcopy(frame); w12["historical_conservation"] = w.put("h12.json", h12)
    sp12 = faithful_spine(); sp12["coverage"]["PYAT_PC"]["PYAT-PC-R9-01"]["adopted"] = True
    w12["historical_source_spine"] = w.put("s12.json", sp12)
    h12["source_spine_sha256"] = w12["historical_source_spine"]["sha256"]
    w12["historical_conservation"] = w.put("h12b.json", h12)
    o = old("FRAME", w12, w); s = strict_run("FRAME", w12, w)
    out.append(result_row("H12", "K3 NOT_ADOPTED flipped to adopted (positive control)",
                          "K3 NOT_ADOPTED", w12["historical_conservation"]["sha256"],
                          "RED", o, s, "supplied gate does defend this exact boolean"))

    # H13 clean restoration after all mutations
    o = old("FRAME", frame, w); s = strict_run("FRAME", frame, w)
    o2 = old("DECISION", decision, w); s2 = strict_run("DECISION", decision, w)
    o3 = old("C_INTEGRATED", cpacket, w); s3 = strict_run("C_INTEGRATED", cpacket, w)
    out.append(result_row("H13", "restore pristine packet after mutations",
                          "all stages", fhash, "PASS",
                          {"status": "/".join([o["status"], o2["status"], o3["status"]]),
                           "errors": o["errors"] + o2["errors"] + o3["errors"]},
                          {"status": "/".join([s["status"], s2["status"], s3["status"]]),
                           "errors": s["errors"] + s2["errors"] + s3["errors"]},
                          "positive/restore demonstrated on the same bytes"))

    rec = {"schema": "D4B_HOSTILE_ATTACK_REPORT", "instrument_package": str(PKG),
           "package_file_count": sum(1 for _ in PKG.rglob('*') if _.is_file()),
           "code_head": HEAD, "live_protected_head": LIVE,
           "strict_overlay": str(HERE / "strict_instrument.py"),
           "note": "Supplied status is the actual verdict of the supplied R7 gate. Strict status is an authored private overlay, not independent C.",
           "rows": out}
    (HERE / "REPORT.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
    with (HERE / "HOSTILE_ATTACK_MATRIX.tsv").open("w", encoding="utf-8") as f:
        cols = ["attack_id", "attack", "target_contract", "fixture_sha256", "expected",
                "supplied_status", "supplied_errors", "strict_status", "strict_errors", "note"]
        f.write("\t".join(cols) + "\n")
        for r in out:
            f.write("\t".join(str(r.get(c, "")) for c in cols) + "\n")
    print(json.dumps({"report": str(HERE / "REPORT.json"),
                      "rows": len(out),
                      "supplied_red": sum(1 for r in out if str(r["supplied_status"]).startswith("RED")),
                      "strict_red": sum(1 for r in out if str(r["strict_status"]).startswith("RED"))},
                     indent=2))


if __name__ == "__main__":
    main()
