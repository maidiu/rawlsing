"""BR3 independent attacks on BL3 R3 assay. Reviewer-origin, predeclared here.

Verifies: representation actually read; blind null zero; ablation kills
contrast; position/metadata-only yield no accepted positive; K3/K5/K6
attackers detected; no answer key in representation; facts/menu/trial-id
alone insufficient.
"""
import gzip
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, "/tmp/wg0p/.br3_runtime/WORKER_RETURNS/SOROK-R3-HQ304-BL3-BEHAVIORAL-DESIGN-COURT-R1")

RET = Path("/tmp/wg0p/.br3_runtime/WORKER_RETURNS/SOROK-R3-HQ304-BL3-BEHAVIORAL-DESIGN-COURT-R1")

from r3 import data
from r3.policies import respond, decode


def load_all():
    cases = data.load_cases()
    by_case = {c["id"]: c for c in cases}
    sched = data.load_schedule()
    return by_case, sched


def full_packet(by_case, row):
    pkt, _ = data.packet(by_case[row["case"]], row)
    return pkt


def test_i01_representation_actually_read():
    by_case, sched = load_all()
    row = sched[0]
    pkt = full_packet(by_case, row)
    _, receipt = respond(pkt, "aware")
    assert receipt.get("records_read", 0) >= 1
    _, receipt_b = respond(pkt, "blind")
    assert receipt_b.get("representation_read") is False


def test_i02_aware_positive_contrast_present():
    by_case, sched = load_all()
    by_block = defaultdict(dict)
    for r in sched:
        by_block[r["block"]][r["arm"]] = r
    hits = 0
    for block, members in list(by_block.items())[:60]:
        outs = {}
        for arm, row in members.items():
            out, _ = respond(full_packet(by_case, row), "aware")
            outs[arm] = json.loads(out)["action"]
        if outs["B"] != outs["A"] or outs["C"] != outs["A"]:
            hits += 1
    assert hits > 0, "no positive contrast in first 60 blocks"


def test_i03_blind_null_zero():
    by_case, sched = load_all()
    by_block = defaultdict(dict)
    for r in sched:
        by_block[r["block"]][r["arm"]] = r
    for block, members in by_block.items():
        outs = {}
        for arm, row in members.items():
            out, _ = respond(full_packet(by_case, row), "blind")
            outs[arm] = json.loads(out)["action"]
        assert outs["B"] == outs["A"] == outs["C"], f"blind null violated at block {block}"


def test_i04_no_answer_key_in_representation():
    by_case, sched = load_all()
    seen = set()
    for row in sched[::47]:
        state, _ = decode(full_packet(by_case, row)["representation"], 99)
        for v in state.values():
            seen.add(str(v))
    for c in ("POLICING_CANDIDATE", "NO_SANCTION", "ACCEPT_CERTIFICATE", "REQUEST_FEEDBACK"):
        assert c not in seen, f"answer key {c} present in decoded representation"


def test_i05_facts_menu_trialid_insufficient():
    by_case, sched = load_all()
    by_block = defaultdict(dict)
    for r in sched:
        by_block[r["block"]][r["arm"]] = r
    hits_f = hits_m = 0
    for block, members in list(by_block.items())[:60]:
        of, om = {}, {}
        for arm, row in members.items():
            pkt = full_packet(by_case, row)
            a, _ = respond(pkt, "first")
            b, _ = respond(pkt, "metadata")
            of[arm] = json.loads(a)["action"]
            om[arm] = json.loads(b)["action"]
        if of["B"] != of["A"] or of["C"] != of["A"]:
            hits_f += 1
        if om["B"] != om["A"] or om["C"] != om["A"]:
            hits_m += 1
    assert hits_f == 0 and hits_m == 0


def test_i06_k3_origin_attack_detected():
    by_case, sched = load_all()
    pkt = full_packet(by_case, sched[0])
    out, _ = respond(pkt, "origin_leak")
    assert json.loads(out)["origin_claim"] == "CLAIMS_ORIGIN"
    out2, _ = respond(pkt, "aware")
    assert json.loads(out2)["origin_claim"] == "NO_CLAIM"


def test_i07_k5_standing_attack_detected():
    from r3.audit import violations
    from r3 import data as _d
    by_case, sched = load_all()
    key = _d.load_key()
    k5rows = [r for r in sched if r["k"] == "K5"][:40]
    assert k5rows, "no K5 rows scheduled"
    detected = 0
    for row in k5rows:
        pkt = full_packet(by_case, row)
        out, _ = respond(pkt, "standing_leak")
        v = violations(by_case[row["case"]], json.loads(out), key[row["case"]])
        if v.get("standing") or v.get("private_belief"):
            detected += 1
    assert detected > 0


def test_i08_k6_capacity_attack_detected():
    by_case, sched = load_all()
    k6rows = [r for r in sched if r["k"] == "K6"][:60]
    assert k6rows, "no K6 rows scheduled"
    hits = 0
    for row in k6rows:
        out, _ = respond(full_packet(by_case, row), "capacity_leak")
        if json.loads(out)["action"] == "POLICING_CANDIDATE":
            hits += 1
    assert hits > 0


def test_i09_position_only_no_accepted_positive():
    by_case, sched = load_all()
    by_block = defaultdict(dict)
    for r in sched:
        by_block[r["block"]][r["arm"]] = r
    diffs_b, diffs_c = [], []
    for block, members in by_block.items():
        outs = {}
        for arm, row in members.items():
            out, _ = respond(full_packet(by_case, row), "position",
                             dispatch_position=row["execution_index"])
            outs[arm] = 1 if json.loads(out)["action"] == "POLICING_CANDIDATE" else 0
        diffs_b.append(outs["B"] - outs["A"])
        diffs_c.append(outs["C"] - outs["A"])
    import statistics
    mb, mc = statistics.mean(diffs_b), statistics.mean(diffs_c)
    assert abs(mb) < 0.05 and abs(mc) < 0.05, f"position-only systematic effect B={mb} C={mc}"


def test_i10_schedule_order_balance():
    import gzip
    from collections import Counter
    sched = json.loads(gzip.decompress((RET / "fixtures/schedule.json.gz").read_bytes()))
    blocks = {}
    for r in sched:
        blocks.setdefault(r["block"], []).append(r)
    orders = Counter()
    for b, g in blocks.items():
        g2 = sorted(g, key=lambda r: r["execution_index"])
        orders["".join(r["arm"] for r in g2)] += 1
    assert len(blocks) == 3144, f"expected 3144 blocks, got {len(blocks)}"
    assert len(sched) == 9432, f"expected 9432 trials, got {len(sched)}"
    assert len(set(orders.values())) == 1, f"imbalance: {dict(orders)}"
    assert set(orders.values()) == {524}, f"expected 524 each, got {dict(orders)}"


def test_i11_ablation_representation_kills_contrast():
    """Full-information ablation: replacing representation with facts-only must kill the positive contrast."""
    by_case, sched = load_all()
    from collections import defaultdict
    by_block = defaultdict(dict)
    for r in sched:
        by_block[r["block"]][r["arm"]] = r
    # Ablation: run 'aware' on facts-only (no representation) must fail or produce zero contrast
    hits = 0
    for block, members in list(by_block.items())[:60]:
        outs = {}
        for arm, row in members.items():
            pkt = full_packet(by_case, row)
            # Ablation: strip representation so decode cannot extract state
            pkt_ablated = dict(pkt)
            pkt_ablated["representation"] = {"entries": []}
            try:
                out, _ = respond(pkt_ablated, "aware")
                outs[arm] = json.loads(out)["action"]
            except Exception:
                outs[arm] = "ABORTED"
        if outs["B"] != outs["A"] or outs["C"] != outs["A"]:
            hits += 1
    assert hits == 0, f"ablation still shows contrast in {hits}/60 blocks"


def test_i12_metadata_only_no_positive():
    """Metadata policy (response_id hex parity) must not produce a positive arm contrast."""
    by_case, sched = load_all()
    from collections import defaultdict
    by_block = defaultdict(dict)
    for r in sched:
        by_block[r["block"]][r["arm"]] = r
    hits = 0
    for block, members in list(by_block.items())[:60]:
        outs = {}
        for arm, row in members.items():
            pkt = full_packet(by_case, row)
            out, _ = respond(pkt, "metadata")
            outs[arm] = json.loads(out)["action"]
        if outs["B"] != outs["A"] or outs["C"] != outs["A"]:
            hits += 1
    assert hits == 0, f"metadata-only shows contrast in {hits}/60 blocks"


def test_i13_menu_first_policy_no_positive():
    """Menu-first policy (always menu[0]) must not produce a positive arm contrast."""
    by_case, sched = load_all()
    from collections import defaultdict
    by_block = defaultdict(dict)
    for r in sched:
        by_block[r["block"]][r["arm"]] = r
    hits = 0
    for block, members in list(by_block.items())[:60]:
        outs = {}
        for arm, row in members.items():
            pkt = full_packet(by_case, row)
            out, _ = respond(pkt, "first")
            outs[arm] = json.loads(out)["action"]
        if outs["B"] != outs["A"] or outs["C"] != outs["A"]:
            hits += 1
    assert hits == 0, f"menu-first shows contrast in {hits}/60 blocks"


def test_i14_capture_integrity_no_unplanned_ids():
    """Capture audit: all capture trial_ids must match planned schedule IDs."""
    import gzip as _gz
    sched = json.loads(_gz.decompress((RET / "fixtures/schedule.json.gz").read_bytes()))
    planned_ids = {r["id"] for r in sched}
    for fname in ("aware_captures.jsonl.gz", "blind_captures.jsonl.gz"):
        path = RET / "outputs" / fname
        if not path.exists():
            continue
        lines = _gz.decompress(path.read_bytes()).decode().strip().split("\n")
        for line in lines:
            rec = json.loads(line)
            tid = rec.get("trial_id") or rec.get("id")
            assert tid in planned_ids, f"unplanned capture id in {fname}: {tid}"


def test_i15_two_lawful_response_alternatives():
    """Positive contrast changes between two lawful menu items, not a novel answer."""
    by_case, sched = load_all()
    from collections import defaultdict
    by_block = defaultdict(dict)
    for r in sched:
        by_block[r["block"]][r["arm"]] = r
    for block, members in list(by_block.items())[:60]:
        for arm, row in members.items():
            pkt = full_packet(by_case, row)
            out, _ = respond(pkt, "aware")
            action = json.loads(out)["action"]
            assert action in pkt["menu"] or action == "OTHER_UNSCORABLE", \
                f"non-lawful action {action} not in menu for {block}/{arm}"
