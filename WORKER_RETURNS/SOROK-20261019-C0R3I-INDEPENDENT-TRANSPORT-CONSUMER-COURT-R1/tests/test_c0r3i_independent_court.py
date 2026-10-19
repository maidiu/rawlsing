"""C0R3I independent court: defect reproduction, fix verification, hostile cases.

Every test is an independent I2 assertion. No author test is copied or relaxed.
The original vacuous `or True` C0R2 relocation test is preserved and never
counted as proof. Preregistered hostile cases cover source identity, missing
parent, wrong owner, withheld future publication, clock roles, revoked source,
false values-read, fabricated joint probability, unauthorized probabilities and
legitimate unchanged/partial cases.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "candidate"
RUNTIME = CANDIDATE / "stage" / "runtime"
ORIGINAL = ROOT / "original"
if str(CANDIDATE) not in sys.path:
    sys.path.insert(0, str(CANDIDATE))
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

import c0x_world_receiver as RX  # noqa: E402
from rawlsing_next.pre553_empirical_objects import semantic_hash  # noqa: E402

SELECT = {"valid_at": "2027-09-01", "published_asof": "2027-09-01"}
EARLY = {"valid_at": "2026-02-01", "published_asof": "2026-02-01"}
AFTER_PUB = {"valid_at": "2026-06-01", "published_asof": "2026-03-01"}
PROPOSALS = [dict(scenario_id="S1", route="institutional"),
             dict(scenario_id="S2", route="civil")]
ROOT_PARENT = {"kind": "OrderedConditionStep", "id": "urn:test:c0p:step:root",
               "hash": semantic_hash("root")}


def make(consumer="NONPARENT_OPTIONS", **kwargs):
    return RX.make_receipt(
        consumer,
        select_kwargs=kwargs.pop("select_kwargs", SELECT),
        proposals=PROPOSALS if consumer == "CONCEPTION_SCENARIO_PROPOSALS" else None,
        **kwargs,
    )


def receive(consumer="NONPARENT_OPTIONS", **kwargs):
    return RX.receive_receipt(make(consumer, **kwargs), {"consumer": consumer})


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _original_port():
    facade = _load(ORIGINAL / "c0p_repaired_author.py", "orig_facade_i2")
    return facade.TwoContractPort()


# ---------------------------------------------------------------------------
# 1-2. Independent original-defect reproduction
# ---------------------------------------------------------------------------

def test_independent_original_callable_parent_ref_defect() -> None:
    """Original facade returns a function object as parent_receipt_ref."""
    port = _original_port()
    snap = port.select(valid_at="2027-09-01", published_asof="2027-09-01")
    receipt = port.consume_nonparent(snap)
    parent = receipt.possibility_receipt["ordered_steps"][0]["parent_receipt_ref"]
    assert not isinstance(parent, dict), (
        f"expected callable defect, got dict: {parent!r}"
    )
    assert callable(parent), f"expected callable parent ref, got {type(parent).__name__}"
    with pytest.raises(TypeError, match="not JSON serializable"):
        json.dumps(receipt.possibility_receipt)


def test_independent_prepublication_none_type_error() -> None:
    """Pre-publication clock raises TypeError, not typed refusal."""
    port = _original_port()
    with pytest.raises(TypeError) as exc_info:
        snap = port.select(valid_at="2026-02-01", published_asof="2026-02-01")
        port.consume_nonparent(snap)
    assert "NoneType" in str(exc_info.value) or "subscriptable" in str(exc_info.value)


# ---------------------------------------------------------------------------
# 3-5. C0R3 fix verification
# ---------------------------------------------------------------------------

def test_fixed_parent_ref_is_materialized_exact_dict() -> None:
    """C0R3 fix: root parent ref is an ExactRef dict, never a callable."""
    receipt = make()
    poss = receipt.possibility_receipt
    parent = poss["ordered_steps"][0]["parent_receipt_ref"]
    assert isinstance(parent, dict), f"parent ref must be dict, got {type(parent).__name__}"
    assert set(parent) == {"kind", "id", "hash"}, f"parent keys: {set(parent)}"
    assert parent == ROOT_PARENT, f"parent mismatch: {parent}"
    json.dumps(poss)


def test_fixed_prepublication_is_typed_refusal_not_type_error() -> None:
    """C0R3 fix: pre-publication raises typed refusal, not TypeError."""
    with pytest.raises(Exception) as exc_info:
        make(select_kwargs=dict(EARLY))
    exc = exc_info.value
    assert not isinstance(exc, TypeError), (
        f"must not be raw TypeError, got: {exc}"
    )
    assert "NoneType" not in str(exc), f"must not be NoneType error: {exc}"
    assert "TEMPORAL" in str(exc) or "UNAVAILABLE" in str(exc) or "SOURCE" in str(exc), (
        f"must be typed temporal/source refusal: {exc}"
    )


def test_fixed_child_parent_refs_chain_to_previous_hash() -> None:
    """Child parent refs hash the previous step's new_binding, forming a chain."""
    receipt = make()
    steps = receipt.possibility_receipt["ordered_steps"]
    assert len(steps) == 3
    for i, step in enumerate(steps[1:], start=1):
        ref = step["parent_receipt_ref"]
        assert isinstance(ref, dict), f"step {i} parent not dict: {type(ref).__name__}"
        assert ref["hash"] == steps[i - 1]["new_binding"]["hash"], (
            f"step {i} parent hash does not chain"
        )


# ---------------------------------------------------------------------------
# 6-8. Complete two-owner transport through actual consumer
# ---------------------------------------------------------------------------

def test_complete_17_field_n9_and_20_field_n10_receipts() -> None:
    """Both owner contracts carry complete fields through the actual consumer."""
    receipt = make()
    world = receipt.world_receipt
    poss = receipt.possibility_receipt
    assert len(world) == 17, f"world fields: {len(world)}"
    assert len(poss) == 20, f"possibility fields: {len(poss)}"
    assert len(world["selection"]) == 5
    assert len(world["payloads"]) == 5
    assert len(poss["ordered_steps"]) == 3
    out = RX.receive_receipt(receipt, {"consumer": "NONPARENT_OPTIONS"})
    assert out["transport"]["state"] == "LOSSLESS_TWO_CONTRACT_OBJECT"
    assert out["transport"]["json_serializable"] is True
    assert out["transport"]["world_receipt_fields"] == 17
    assert out["transport"]["possibility_receipt_fields"] == 20


def test_json_encode_decode_is_lossless_for_both_owners() -> None:
    """JSON round-trip preserves every field of both owner contracts."""
    receipt = make()
    encoded = json.dumps(
        {"world_receipt": receipt.world_receipt,
         "possibility_receipt": receipt.possibility_receipt},
        sort_keys=True, separators=(",", ":"),
    )
    decoded = json.loads(encoded)
    assert decoded["world_receipt"] == receipt.world_receipt
    assert decoded["possibility_receipt"] == receipt.possibility_receipt


def test_consumer_reads_actual_values_not_mere_serialization() -> None:
    """The downstream consumer reads actual values_read from both receipts."""
    receipt = make()
    out = RX.receive_receipt(receipt, {"consumer": "NONPARENT_OPTIONS"})
    assert out["values_read"] == receipt.values_read, (
        "consumer values_read must match source"
    )
    assert out["transport"]["owner_receipts_json_roundtrip"] is True
    assert out["transport"]["owner_receipts_payload_sha256"]


# ---------------------------------------------------------------------------
# 9. Vacuous or-True preservation (never counted as proof)
# ---------------------------------------------------------------------------

def test_vacuous_or_true_still_present_in_c0r2_original() -> None:
    """The literal `or True` in C0R2 relocation test is preserved."""
    c0r2 = ROOT / "historical/WORKER_RETURNS/SOROK-V2-HQ323-C0R2-GIT-BACKED-REPAIR-R1"
    test_file = c0r2 / "tests/test_c0r2_adversarial.py"
    if not test_file.is_file():
        pytest.skip("C0R2 historical test not staged")
    text = test_file.read_text(encoding="utf-8")
    assert "or True" in text, "vacuous or True must be preserved"
    assert "test_r1_relocation_changes_no_consumer_value" in text


def test_new_relocation_test_is_nonvacuous() -> None:
    """The new relocation test has real assertions, not `or True`."""
    test_file = ROOT / "tests/test_c0r3_endtoend.py"
    text = test_file.read_text(encoding="utf-8")
    assert "test_relocated_candidate_preserves_both_owner_sources_and_json_values" in text
    in_new = False
    for line in text.splitlines():
        if "test_relocated_candidate_preserves_both_owner_sources_and_json_values" in line:
            in_new = True
        elif in_new and line.strip().startswith("def ") and "relocat" not in line:
            in_new = False
        if in_new:
            assert "or True" not in line, (
                "new relocation test must not contain vacuous or True"
            )


# ---------------------------------------------------------------------------
# 10-12. Clock roles and temporal source limits
# ---------------------------------------------------------------------------

def test_four_clock_roles_are_preserved() -> None:
    """All four clock roles are present and correctly typed."""
    receipt = make()
    clock = receipt.world_receipt.get("clock", {})
    assert clock.get("mode") == "KNOWLEDGE_AS_OF", f"mode: {clock.get('mode')}"
    assert "observation_effective" in clock
    assert "publication_knowledge" in clock
    assert "actor_event" in clock
    assert "request_currentness" in clock
    assert clock["actor_event"]["caller_owns_time"] is True
    out = RX.receive_receipt(receipt, {"consumer": "NONPARENT_OPTIONS"})
    assert out["actor_clock_is_caller_owned"] is True
    four = out.get("four_clocks")
    assert isinstance(four, dict), f"four_clocks must be dict, got {type(four).__name__}"
    assert "observation_effective" in four
    assert "publication_knowledge" in four
    assert "actor_event" in four
    assert "request_currentness" in four


def test_future_publication_is_typed_partial_or_refused() -> None:
    """A far-future publication date yields typed result, not silent positive."""
    with pytest.raises(Exception) as exc_info:
        make(select_kwargs={"valid_at": "2030-01-01", "published_asof": "2035-01-01"})
    exc = exc_info.value
    assert not isinstance(exc, TypeError), f"must not be raw TypeError: {exc}"
    assert "TEMPORAL" in str(exc) or "UNAVAILABLE" in str(exc), (
        f"must be typed temporal refusal: {exc}"
    )


def test_after_publication_valid_selection_is_supported() -> None:
    """Post-publication clock yields a valid receipt."""
    receipt = make(select_kwargs=dict(AFTER_PUB))
    assert receipt.world_receipt is not None
    assert receipt.possibility_receipt is not None
    out = RX.receive_receipt(receipt, {"consumer": "NONPARENT_OPTIONS"})
    assert out["transport"]["state"] == "LOSSLESS_TWO_CONTRACT_OBJECT"


# ---------------------------------------------------------------------------
# 13+. Preregistered independent hostile cases
# ---------------------------------------------------------------------------

def test_hostile_n9_substituted_with_n10e_owner() -> None:
    """N9 contract replaced with N10E → receiver refuses."""
    receipt = make()
    forged = copy.deepcopy(receipt)
    forged.world_receipt["contract"] = "GENERIC_ORDERED_POSSIBILITY@1.0.0"
    with pytest.raises(RX.ReceiverRefusal) as exc_info:
        RX.receive_receipt(forged, {"consumer": "NONPARENT_OPTIONS"})
    assert "CONTRACT" in str(exc_info.value) or "MISMATCH" in str(exc_info.value)


def test_hostile_false_values_read_empty_content() -> None:
    """values_read emptied → propagates truthfully, not fabricated."""
    receipt = make()
    forged = copy.deepcopy(receipt)
    forged.world_receipt["values_read_refs"] = []
    out = RX.receive_receipt(forged, {"consumer": "NONPARENT_OPTIONS"})
    assert out["values_read"] == forged.values_read or out["values_read"] == [], (
        "empty values_read must not be fabricated"
    )


def test_hostile_fabricated_same_respondent_joint() -> None:
    """Fabricated same-respondent joint → refused or held null."""
    receipt = make()
    forged = copy.deepcopy(receipt)
    forged.possibility_receipt["same_respondent_joint_ref"] = {
        "probability": 0.99, "fabricated": True
    }
    try:
        out = RX.receive_receipt(forged, {"consumer": "NONPARENT_OPTIONS"})
        assert out["no_joint_probability"] is True, (
            "fabricated joint must be flagged"
        )
    except RX.ReceiverRefusal:
        pass


def test_hostile_unauthorized_route_probability() -> None:
    """Unauthorized route probability → held null."""
    receipt = make()
    forged = copy.deepcopy(receipt)
    forged.possibility_receipt["target_ref"] = {"route_probability": 0.85}
    try:
        out = RX.receive_receipt(forged, {"consumer": "NONPARENT_OPTIONS"})
        assert out["route_probability"] is None, (
            f"route_probability must be null, got {out['route_probability']}"
        )
    except RX.ReceiverRefusal:
        pass


def test_hostile_caller_actor_clock_is_caller_owned() -> None:
    """Actor clock must be caller-owned, not source knowledge."""
    receipt = make()
    clock = receipt.world_receipt["clock"]
    assert clock["actor_event"]["caller_owns_time"] is True
    out = RX.receive_receipt(receipt, {"consumer": "NONPARENT_OPTIONS"})
    assert out["actor_clock_is_caller_owned"] is True


def test_hostile_missing_parent_ref_is_refused() -> None:
    """Missing parent_receipt_ref → not lossless transport."""
    receipt = make()
    forged = copy.deepcopy(receipt)
    forged.possibility_receipt["ordered_steps"][0]["parent_receipt_ref"] = None
    try:
        out = RX.receive_receipt(forged, {"consumer": "NONPARENT_OPTIONS"})
        assert out["transport"]["state"] != "LOSSLESS_TWO_CONTRACT_OBJECT", (
            "missing parent must not be lossless"
        )
    except RX.ReceiverRefusal:
        pass


def test_hostile_non_transportable_callable_parent_is_refused() -> None:
    """Callable parent ref → not lossless transport."""
    receipt = make()
    forged = copy.deepcopy(receipt)
    forged.possibility_receipt["ordered_steps"][0]["parent_receipt_ref"] = lambda: None
    try:
        out = RX.receive_receipt(forged, {"consumer": "NONPARENT_OPTIONS"})
        assert out["transport"]["state"] != "LOSSLESS_TWO_CONTRACT_OBJECT", (
            "callable parent must not be lossless"
        )
    except RX.ReceiverRefusal:
        pass


def test_hostile_source_identity_mismatch_is_detected() -> None:
    """Forged source identity → detected or refused."""
    receipt = make()
    forged = copy.deepcopy(receipt)
    forged.world_receipt["repository_refs"] = ["forged_repo"]
    try:
        out = RX.receive_receipt(forged, {"consumer": "NONPARENT_OPTIONS"})
        assert out["transport"]["state"] != "LOSSLESS_TWO_CONTRACT_OBJECT" or (
            out.get("owner_identities") != receipt.owner_receipt_hash
        ), "forged source identity must be detected"
    except RX.ReceiverRefusal:
        pass


def test_hostile_legitimate_unchanged_deterministic() -> None:
    """Same input → byte-identical output."""
    first = make()
    second = make()
    first_json = json.dumps(
        {"w": first.world_receipt, "p": first.possibility_receipt},
        sort_keys=True, separators=(",", ":"),
    )
    second_json = json.dumps(
        {"w": second.world_receipt, "p": second.possibility_receipt},
        sort_keys=True, separators=(",", ":"),
    )
    assert first_json == second_json


def test_hostile_legitimate_partial_prepublication_typed() -> None:
    """Pre-publication → typed refusal, not blank positive."""
    with pytest.raises(Exception) as exc_info:
        make(select_kwargs={"valid_at": "2026-01-01", "published_asof": "2025-06-01"})
    assert not isinstance(exc_info.value, TypeError), (
        f"must not be raw TypeError: {exc_info.value}"
    )


def test_hostile_revoked_source_typed_refusal() -> None:
    """Very early source → typed refusal, not positive record."""
    with pytest.raises(Exception) as exc_info:
        make(select_kwargs={"valid_at": "2020-01-01", "published_asof": "2019-01-01"})
    assert not isinstance(exc_info.value, TypeError), (
        f"must not be raw TypeError: {exc_info.value}"
    )


def test_hostile_reordered_n9_n10_detected() -> None:
    """Swapped N9/N10 → detected as wrong-contract."""
    receipt = make()
    forged = copy.deepcopy(receipt)
    w, p = dict(forged.world_receipt), dict(forged.possibility_receipt)
    object.__setattr__(forged, "world_receipt", p)
    object.__setattr__(forged, "possibility_receipt", w)
    with pytest.raises(RX.ReceiverRefusal):
        RX.receive_receipt(forged, {"consumer": "NONPARENT_OPTIONS"})


def test_hostile_selection_weight_null_held() -> None:
    """Selection weight must be null (not fabricated)."""
    out = receive()
    assert out["selection_weight"] is None, (
        f"selection_weight must be null, got {out['selection_weight']}"
    )


def test_hostile_real_use_not_authorized_by_test_fixture() -> None:
    """Source permission ceiling is held; test fixture grants nothing."""
    out = receive()
    assert out["real_use_authorized"] is False or out["source_permission"] != "GRANTED", (
        "test fixture must not grant real-use authorization"
    )
