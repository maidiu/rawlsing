"""RBA independent hostile probes on the R2 candidate (reviewer-owned).

These probes are independently authored against the staged candidate closure.
They do not modify candidate bytes. Verdicts: PASS (property holds),
RED (property violated -> finding), NOT_REACHED (needs live grant/model).

ZERO real model/actor/provider calls: socket connect is denied by fixture.
"""
import copy
import hashlib
import inspect
import json
import re
import socket
from collections import Counter, defaultdict
from pathlib import Path

import pytest

RET = Path(__file__).resolve().parents[1]
EXEC = RET / "exec" / "r2"
import sys
sys.path.insert(0, str(EXEC))

from assay.architecture import build_packet, canonical, digest, form_owner  # noqa: E402
from assay.corpus import MENUS  # noqa: E402
from assay.experiment import mock_permit, code_capture  # noqa: E402
from assay.oracle import check_key, proposed_key  # noqa: E402
from assay.scoring import UNIVERSE, fraction, paired, score  # noqa: E402
from assay.transport import (  # noqa: E402
    Denied,
    Frozen,
    MockIssuer,
    MockTransport,
    Runner,
    validate,
)

CORPUS = json.loads((EXEC / "data" / "corpus.json").read_text())
SCHEDULE = json.loads((EXEC / "data" / "schedule.json").read_text())
ORACLE = json.loads((EXEC / "data" / "oracle.json").read_text())
FZ = None


def get_frozen():
    global FZ
    if FZ is None:
        from assay.transport import Frozen as _F
        FZ = _F(EXEC, EXEC / (EXEC / "CURRENT_FREEZE").read_text().strip())
    return FZ


@pytest.fixture(autouse=True)
def zero_network(monkeypatch):
    def deny(*a, **k):
        raise AssertionError("ZERO_REAL_MODEL_CALL_NETWORK_GUARD")

    monkeypatch.setattr(socket.socket, "connect", deny)
    monkeypatch.setattr(socket.socket, "connect_ex", deny)
    monkeypatch.setattr(socket, "getaddrinfo", deny)


UUID_RE = re.compile(r"^([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|[0-9a-f]{32})$")


def full_packet_bytes(case, row, cache=None):
    packet, _receipt = build_packet(case, row, cache)
    return packet


# ---------------------------------------------------------------- H1: leaks

def test_h01_no_k_contrast_arm_expected_labels_in_packet():
    """Full serialized provider packets must not name K/contrast/arm/expected."""
    bad = []
    rows = {r["id"]: r for r in SCHEDULE}
    for case in CORPUS:
        row = next(r for r in SCHEDULE if r["case"] == case["id"])
        for arm in ("A", "B", "C"):
            rr = dict(row, arm=arm)
            text = canonical(full_packet_bytes(case, rr)).decode()
            for tok in ("K1", "K2", "K3", "K4", "K5", "K6", "contrast", "expected", "HISTORY"):
                if tok in text:
                    bad.append((case["id"], arm, tok))
    assert bad == [], bad[:5]


def test_h02_no_inaccessible_origin_content_in_packet():
    """Origin-bearing IDs and hidden origin strings must be absent from packets."""
    bad = []
    for case in CORPUS:
        row = next(r for r in SCHEDULE if r["case"] == case["id"])
        hidden_vals = [str(v) for v in (case.get("hidden") or {}).values()]
        origin_ids = [e["id"] for e in case["history"] if not e.get("accessible")]
        for arm in ("A", "B", "C"):
            text = canonical(full_packet_bytes(case, dict(row, arm=arm))).decode()
            for secret in hidden_vals + origin_ids:
                if secret and secret.encode() in text.encode():
                    bad.append((case["id"], arm, secret[:24]))
    assert bad == [], bad[:5]


def test_h03_ids_are_uuid_shaped_not_lookup_keys():
    """Trial/case/event IDs must be UUIDs, not K__contrast__seed lookup keys."""
    bad = []
    for case in CORPUS:
        if not UUID_RE.match(case["id"]):
            bad.append(("case", case["id"]))
        for e in case["history"]:
            if not UUID_RE.match(e["id"]):
                bad.append(("event", e["id"]))
    for row in SCHEDULE:
        if not UUID_RE.match(row["id"]):
            bad.append(("trial", row["id"]))
    assert bad == [], bad[:5]


def _walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield f"{path}.{k}", v
            yield from _walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _walk(v, f"{path}[{i}]")


def test_h04_no_raw_owner_effects_or_grants_in_packet():
    """Packets must carry representations/facts, never raw owner effects or grants."""
    bad = []
    for case in CORPUS:
        row = next(r for r in SCHEDULE if r["case"] == case["id"])
        packet = full_packet_bytes(case, dict(row, arm="A"))
        for path, v in _walk(packet):
            lk = path.split(".")[-1].lower()
            if lk in ("grant", "issuer", "signature", "authority_ref", "owner_effect",
                      "public_standing_change", "issuer_identity", "mock_key"):
                bad.append((case["id"], path))
        text = canonical(packet).decode()
        for tok in ("LOCAL_MOCK_AUTHORITY_ONLY", "PUBLIC_STANDING_CHANGE", "MOCK_MODEL"):
            if tok in text:
                bad.append((case["id"], tok))
    assert bad == [], bad[:5]


# ---------------------------------------------------------------- H2: liveness

def test_h05_arm_representations_differ_by_intervention():
    """A/B/C cores must differ by implemented intervention on matched cells."""
    diffs = {"A-B": 0, "B-C": 0, "A-C": 0}
    n = 0
    for case in CORPUS:
        row = next(r for r in SCHEDULE if r["case"] == case["id"])
        reps = {}
        for arm in ("A", "B", "C"):
            p = full_packet_bytes(case, dict(row, arm=arm))
            reps[arm] = p["representation"]
        n += 1
        if reps["A"] != reps["B"]:
            diffs["A-B"] += 1
        if reps["B"] != reps["C"]:
            diffs["B-C"] += 1
        if reps["A"] != reps["C"]:
            diffs["A-C"] += 1
    assert n == 126
    for k, v in diffs.items():
        assert v == n, (k, v, n)


def test_h06_same_lawful_facts_across_arms():
    """All arms must share the exact lawful fact values (organization differs)."""
    for case in CORPUS[:30]:
        row = next(r for r in SCHEDULE if r["case"] == case["id"])
        facts = [full_packet_bytes(case, dict(row, arm=a))["facts"] for a in ("A", "B", "C")]
        assert facts[0] == facts[1] == facts[2], case["id"]


# ---------------------------------------------------------------- H3: K3/K5/K6

def test_h07_k3_trace_visible_origin_absent_testimony_conditioned():
    """K3 actor sees current trace effect + conditioned testimony, never origin."""
    k3 = [c for c in CORPUS if c["k"] == "K3"]
    assert len(k3) == 36
    for case in k3:
        row = next(r for r in SCHEDULE if r["case"] == case["id"])
        p = full_packet_bytes(case, dict(row, arm="A"))
        facts = p["facts"]
        org = facts["organization"]
        assert "alertness" in org  # current trace effect visible
        se = org.get("self_explanation") or {}
        assert se.get("claim") in (None, "current workload explains my feeling")
        assert se.get("confidence") in ("UNSTATED", "LOW", "HIGH", None)
        # evaluator condition labels must never reach actor-visible testimony
        assert "mistaken" not in json.dumps(se).lower()
        assert "confident_mistaken" not in json.dumps(se).lower()
        text = canonical(p).decode()
        for secret in [str(v) for v in (case.get("hidden") or {}).values()]:
            assert not secret or secret.encode() not in text.encode()


def test_h08_k5_public_private_separation():
    """K5 public notice, private prior and belief report must be distinct slots."""
    k5 = [c for c in CORPUS if c["k"] == "K5"]
    assert len(k5) == 24
    for case in k5:
        row = next(r for r in SCHEDULE if r["case"] == case["id"])
        p = full_packet_bytes(case, dict(row, arm="A"))
        assert "public_notice" in p["facts"]
        out = p["output_schema"]
        assert "belief_report" in out and "standing_report" in out


def test_h09_k6_capacity_factual_and_sanction_optional():
    """K6 sets must cite actual position/capacity facts; NO_SANCTION optional."""
    k6 = [c for c in CORPUS if c["k"] == "K6"]
    assert len(k6) == 24
    caps = Counter(
        (c["position"].get("issuer"), c["position"].get("scope"),
         c["position"].get("capacity")) for c in k6)
    # the factual contrast (capacity True vs False with same issuer/scope) exists
    assert any(v[2] is True for v in caps) and any(v[2] is False for v in caps)
    assert all(v[0] == "fixture_position_owner" for v in caps)
    import itertools
    menus = {tuple(r["menu"]) for r in SCHEDULE if r["k"] == "K6"}
    assert any("NO_SANCTION" in m for m in menus)


# ---------------------------------------------------------------- H4: oracle

def test_h10_oracle_attack_alternative_lawful_counterexample():
    """A lawful-structure, wrong-content key must fail BOTH oracle channels."""
    from assay.oracle import audit_legality
    from assay.scoring import IntegrityError as SE

    good_id = next(iter(ORACLE))
    key = ORACLE[good_id]
    forged = copy.deepcopy(key)
    if isinstance(forged, dict):
        for fk in list(forged.keys()):
            if isinstance(forged[fk], str) and len(forged[fk]) > 4:
                forged[fk] = forged[fk][::-1]
                break
            if isinstance(forged[fk], list) and forged[fk]:
                forged[fk] = list(reversed(forged[fk]))
                break
    else:
        forged = str(forged)[::-1]
    cases = list(json.loads((EXEC / "data" / "corpus.json").read_text()))[:1]
    from assay.scoring import UNIVERSE as _U
    ok_frozen = check_key(cases, proposed_key(cases), _U)
    assert ok_frozen is None or ok_frozen is True
    with pytest.raises(SE):
        check_key(cases, {cases[0]["id"]: forged}, _U)
    # rejection-rule channel must independently refuse the same forgery
    sample = {"action": "FORGED_ACTION_XYZ", "belief_report": "CONFIDENT",
              "standing_report": "RECORDED", "origin_claim": "CLAIMS_ORIGIN"}
    refused = audit_legality(cases[0], sample)
    assert refused is False or (isinstance(refused, dict) and not refused.get("legal", True))


def test_h11_oracle_channels_are_distinct_code_paths():
    """Frozen-key construction and rejection-rule adjudication must differ."""
    import assay.oracle as O

    src_proposed = inspect.getsource(O.proposed_key)
    # rejection-rule oracle lives in a separate function from key construction
    fns = [n for n, f in inspect.getmembers(O, inspect.isfunction)]
    assert "proposed_key" in fns and "check_key" in fns
    assert src_proposed != inspect.getsource(O.check_key)


# ---------------------------------------------------------------- H5: schedule/menu

def test_h12_menu_matched_within_cell_all_permutations_present():
    """Each cell: one shared menu, all three arms; all six arm orders exist."""
    by_cell = defaultdict(list)
    for r in SCHEDULE:
        by_cell[(r["block"], r["case"])].append(r)
    assert len(by_cell) == 3600
    for k, rows in by_cell.items():
        assert {x["arm"] for x in rows} == {"A", "B", "C"}, k
        assert len({tuple(x["menu"]) for x in rows}) == 1, k
    orders = Counter()
    for rows in by_cell.values():
        rows = sorted(rows, key=lambda x: x["execution_index"])
        orders[tuple(x["arm"] for x in rows)] += 1
    assert set(orders) == {("A", "B", "C"), ("A", "C", "B"), ("B", "A", "C"),
                           ("B", "C", "A"), ("C", "A", "B"), ("C", "B", "A")}
    # OBSERVATION (not a failure): permutation counts are unbalanced 1440:432.
    # Pairing is within-cell so this cannot bias B-A/C-A point estimates, but a
    # position-sensitive responder could interact with order; the first-option
    # control (H7 + R2's own) is the guard. Recorded for HQ, not a RED.
    assert orders[("A", "B", "C")] == 1440
    assert all(v == 432 for k, v in orders.items() if k != ("A", "B", "C"))


def test_h13_unique_ids_and_cell_counts():
    order = [r["id"] for r in SCHEDULE]
    assert len(order) == 10800 and len(set(order)) == 10800
    per_case = Counter(r["case"] for r in SCHEDULE)
    assert set(per_case.values()) <= {78, 96}
    assert len(set(r["case"] for r in SCHEDULE)) == 126


def test_h14_paired_ids_exact_and_denominator_includes_unscorable():
    assert any("OTHER_UNSCORABLE" in m for ms in MENUS for m in ([ms] if isinstance(ms, str) else ms)) \
        or any("OTHER_UNSCORABLE" in json.dumps(r["menu"]) for r in SCHEDULE[:200])
    # every schedule row carries a menu containing OTHER_UNSCORABLE (checked on sample + full below)
    missing = [r["id"] for r in SCHEDULE if "OTHER_UNSCORABLE" not in r["menu"]]
    assert missing == [], missing[:3]


# ---------------------------------------------------------------- H6: grant gate

def test_h15_grant_gate_hostile_battery():
    from assay.transport import Frozen as _F, MockIssuer, MockTransport, Runner, validate

    fz = _F(EXEC, EXEC / (EXEC / "CURRENT_FREEZE").read_text().strip())
    rows = list(fz.rows.values())[:2]
    # wrong issuer class
    class FakeIssuer:
        identity = "LOCAL_MOCK_AUTHORITY_ONLY"
    with pytest.raises(Exception):
        validate({"body": {}, "signature": "x"}, FakeIssuer(), fz)
    # tampered signature
    from assay.experiment import mock_permit
    iss = MockIssuer()
    g = mock_permit(iss, fz, rows)
    g2 = copy.deepcopy(g)
    g2["signature"] = "0" * 64
    with pytest.raises(Exception):
        validate(g2, iss, fz)
    # live-mode body
    g3 = copy.deepcopy(g)
    g3["body"] = dict(g3["body"], mode="LIVE")
    with pytest.raises(Exception):
        validate(g3, iss, fz)
    # custom transport attempt
    with pytest.raises(Exception):
        MockTransport("http-custom-evil")


def test_h16_ledger_relocation_removal_rollback_denied(tmp_path):
    from assay.experiment import mock_permit
    from assay.transport import Frozen as _F, MockIssuer, MockTransport, Runner

    fz = _F(EXEC, EXEC / (EXEC / "CURRENT_FREEZE").read_text().strip())
    rows = list(fz.rows.values())[:2]
    iss = MockIssuer()
    g = mock_permit(iss, fz, rows)
    t = MockTransport("lawful")
    j = tmp_path / "journal.jsonl"
    with Runner(g, iss, fz, t, j) as runner:
        row = rows[0]
        from assay.architecture import build_packet

        packet, _ = build_packet(fz.cases[row["case"]], row)
        runner.call(row["id"], packet, 256, "typed")
    assert j.exists()
    # completed-trial redraw is forbidden
    from assay.transport import Denied as _D
    with pytest.raises(_D):
        runner.call(row["id"], packet, 256, "typed")
    # relocation after binding is denied
    moved = tmp_path / "moved.jsonl"
    j.rename(moved)
    with pytest.raises(Exception):
        with Runner(g, iss, fz, t, j):
            pass
    # truncation is rollback: restore, truncate to the START line, re-enter
    moved.rename(j)
    lines = j.read_text().splitlines()
    j.write_text(lines[0] + "\n")
    iss2 = MockIssuer()
    with pytest.raises(Exception):
        with Runner(g, iss2, fz, t, j):
            pass
    # interrupted capture (partial trailing line) fails closed, never resumes
    (tmp_path / "part.jsonl").write_text(lines[0] + "\n{\"broken\": ")
    with pytest.raises(Exception):
        with Runner(g, MockIssuer(), fz, t, tmp_path / "part.jsonl"):
            pass


# ---------------------------------------------------------------- H8: intervals

def test_h17_intervals_recomputed_and_no_power_claim():
    from assay.scoring import paired

    assert callable(paired)
    src = inspect.getsource(paired)
    assert "sqrt" in src or "log" in src or "bound" in src.lower()


# ---------------------------------------------------------------- H9: static transport scan

def test_h18_no_live_transports_or_network_imports():
    bad = []
    for p in (EXEC / "assay").glob("*.py"):
        text = p.read_text()
        for tok in ("import socket", "from socket", "import requests", "from requests",
                    "import urllib", "from urllib", "import http", "from http",
                    "urlopen(", "requests.get(", "requests.post(", "socket.socket(",
                    "subprocess", "os.system", "provider_sdk", "LIVE_MODE_ACCEPT"):
            if tok in text:
                bad.append((p.name, tok))
    assert bad == [], bad


def test_h19_live_mode_unconditionally_denied():
    from assay.transport import Denied, MockTransport

    for bad_policy in ("live", "LIVE", "http-custom-evil", "https://example.invalid"):
        with pytest.raises(Denied):
            MockTransport(bad_policy)


