"""Independent I2 adversarial court for PYAT R35 T35 (reviewer-authored).

Written by the independent R38 reviewer from the pinned T35 frozen expectations,
runtime sources and the sealed repo only. Recomputes expected values from the
publisher records, the hand-derived 58-respondent cell counts and its own
git-blob preimage math; does not import the worker's test suite.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

T35_ROOT = Path(os.environ.get(
    "PYAT_R38_T35_ROOT",
    "/Users/matthewsmith/Desktop/Rawlsing/R38-N9TI-T35-pin-8bfb145f7",
)).resolve()
N9J_ROOT = Path(os.environ.get(
    "PYAT_R38_N9J_ROOT",
    "/Users/matthewsmith/Desktop/Rawlsing/R38-N9TI-N9J-pin-7628840c4",
)).resolve()
RETURN = T35_ROOT / "WORKER_RETURNS/PYAT-R35-T35-TEMPORAL-WORLD-POSITIVE-R1"
RUNTIME = RETURN / "runtime"
PINNED_PRODUCT = RETURN / "03_WORLD_TWO_EPOCH_CONSUMER_DELTA.json"
PINNED_SHA256 = "c4697da7e08a6920d2208e46274a0bab122ecdd334249f6268875625ea2f857b"
PINNED_BYTES = 1099273

sys.path.insert(0, str(RUNTIME))
import bootstrap  # noqa: E402

bootstrap.install()

import two_epoch_world as W  # noqa: E402
import e05_n9_selected_world_adapter as E  # noqa: E402
from product.service import GenericSelectedWorldService  # noqa: E402
from rawlsing_next.pre553_empirical_objects import semantic_hash  # noqa: E402
from rawlsing_next.pre553_hq297_n9c_two_field_reader import (  # noqa: E402
    GSS, NCA, TestOnlyRegistry)

CELL_COUNTS = {
    (1, 1, 1): (6, 2), (1, 1, 0): (4, 4), (1, 0, 1): (5, 3), (1, 0, 0): (3, 5),
    (0, 1, 1): (4, 2), (0, 1, 0): (2, 4), (0, 0, 1): (3, 3), (0, 0, 0): (2, 6),
}


def _expected_steps():
    out = []
    for cond in ((("A", 1),), (("A", 1), ("B", 1)), (("A", 1), ("B", 1), ("C", 1))):
        n = sum(n1 + n0 for cell, (n1, n0) in CELL_COUNTS.items()
                if all(cell["ABC".index(q)] == v for q, v in cond))
        y = sum(n1 for cell, (n1, n0) in CELL_COUNTS.items()
                if all(cell["ABC".index(q)] == v for q, v in cond))
        out.append((n, {"0": n - y, "1": y}))
    return out


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def _mk(support_loss=False):
    service = GenericSelectedWorldService(support_loss=support_loss)
    catalog = service.catalog
    for key, value in (("training_fee", 6), ("exit_cost", 8)):
        catalog._publish(key, value, W.RULE_REVISION["effective_from"],
                         W.RULE_REVISION["effective_to"],
                         W.RULE_REVISION["publication"],
                         revision=W.RULE_REVISION["revision"])
    catalog.catalog_hash = semantic_hash(
        dict(records=catalog.records, empirical=catalog.empirical_identity()))
    return E.N9SelectedWorldAdapter(
        service=service, registry=TestOnlyRegistry(bootstrap.fixture_rows()))


def _steps(receipt):
    return [dict(denominator=s["denominator"],
                 cells={c["cell"]: c["raw_numerator_support"] for c in s["cells"]})
            for s in receipt["empirical_steps"]]


def _routes(receipt):
    return {k: v["state"] for k, v in
            receipt["consumers"][0]["consumer_material"]["structural_routes"].items()}


def _scenarios(receipt):
    return [r["feasibility"] for r in
            receipt["consumers"][1]["consumer_material"]["scenarios"]]


def _walk_strings(value, out):
    if isinstance(value, dict):
        for k, item in value.items():
            out.append(str(k))
            _walk_strings(item, out)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _walk_strings(item, out)
    elif isinstance(value, str):
        out.append(value)


def test_t01_rule_revision_identity_recomputed_from_publisher_records():
    adapter = W.make_adapter()
    catalog = adapter.service.catalog
    by_key_rev = {}
    for record in catalog.records:
        value = catalog.handles[record["ref"]["content_hash"]].payload["value"]
        by_key_rev[(record["key"], record["revision"])] = dict(
            value=value, start=record["start"], end=record["end"],
            publication=record["publication"])
    fee1 = by_key_rev[("training_fee", 1)]
    fee2 = by_key_rev[("training_fee", 2)]
    exit2 = by_key_rev[("exit_cost", 2)]
    assert fee1["value"] == 2 and fee1["start"] == "2026-01-01" and \
        fee1["publication"] == "2026-03-01"
    assert fee2["value"] == 6 and exit2["value"] == 8
    assert fee2["start"] == exit2["start"] == "2027-01-01"
    assert fee2["publication"] == exit2["publication"] == "2027-06-01"
    assert ("training_access", 2) not in by_key_rev
    assert ("civil_open", 2) not in by_key_rev and ("civil_sanction", 2) not in by_key_rev

    e1 = W.serve(W.make_adapter(), W.E1)["receipt"]
    e2 = W.serve(W.make_adapter(), W.E2)["receipt"]
    for receipt, (fee, exit_cost, revision, publication) in (
            (e1, (2, 2, 1, "2026-03-01")), (e2, (6, 8, 2, "2027-06-01"))):
        s = receipt["structural_values"]
        assert (s["training_fee"]["value"], s["exit_cost"]["value"]) == (fee, exit_cost)
        assert (s["training_access"]["value"], s["civil_open"]["value"],
                s["civil_sanction"]["value"]) == (True, True, False)
        assert s["training_fee"]["revision"] == s["exit_cost"]["revision"] == revision
        assert s["training_fee"]["publication"] == publication
        assert s["training_fee"]["effective_from"] == (
            "2026-01-01" if revision == 1 else "2027-01-01")
    assert e1["selection"] == dict(mode="AS_OF", valid_at="2026-06-01",
                                   published_asof="2026-04-15",
                                   purpose="TEST_ONLY_CONTEXT")
    assert e2["selection"]["mode"] == "TEST_CURRENT"
    assert e1["acceptance_state"] == e2["acceptance_state"] == "ACCEPTED_ATOMIC_SELECTED_SNAPSHOT"


def test_t02_empirical_steps_recomputed_from_hand_derived_cell_counts():
    expected = _expected_steps()
    assert expected == [(32, {"0": 14, "1": 18}), (16, {"0": 6, "1": 10}),
                        (8, {"0": 2, "1": 6})]
    e1 = W.serve(W.make_adapter(), W.E1)["receipt"]
    e2 = W.serve(W.make_adapter(), W.E2)["receipt"]
    assert _steps(e1) == _steps(e2) == [dict(denominator=n, cells=c)
                                        for n, c in expected]
    for receipt in (e1, e2):
        for step in receipt["empirical_steps"]:
            one = next(c for c in step["cells"] if c["cell"] == "1")
            assert Fraction(*one["raw_probability_exact_fraction"]["$exact_fraction"]) == \
                Fraction(one["raw_numerator_support"], step["denominator"])
            assert all(c["raw_numerator_support"] > 0 for c in step["cells"])
        balances = [r["source_balance_count"] for r in
                    receipt["consumers"][0]["consumer_material"]["source_balance_reads"]]
        assert balances == [4, 4, 4]
        assert receipt["empirical_state"] == "PRODUCTIVE_TEST_ONLY"


def test_t03_material_affordability_threshold_ladder_is_recomputed():
    adapter = W.make_adapter()
    result = W.serve(adapter, W.E2)
    snapshot = result["snapshot"]
    expectations = {
        5: ("BLOCKED_BY_MODELED_RULE", "RESOURCE_CONSTRAINED"),
        6: ("ELIGIBLE", "RESOURCE_CONSTRAINED"),
        7: ("ELIGIBLE", "RESOURCE_CONSTRAINED"),
        8: ("ELIGIBLE", "WITHIN_MODELED_BUDGET"),
    }
    for budget, (training, exit_state) in expectations.items():
        material = W.consume(adapter.service, snapshot, budget_tokens=budget)["material"]
        routes = material["structural_routes"]
        assert routes["training"]["state"] == training, budget
        assert routes["exit_constraint"]["state"] == exit_state, budget
        assert routes["civil"]["state"] == "ELIGIBLE"
    proposal = W.evaluate(adapter.service, snapshot, W.PROPOSALS)["material"]
    assert [s["feasibility"] for s in proposal["scenarios"]] == \
        ["FEASIBLE_MODELED_PREMISE", "FEASIBLE_MODELED_PREMISE"]
    assert result["receipt"]["structural_values"]["training_access"]["value"] is True
    e1 = W.serve(W.make_adapter(), W.E1)["receipt"]
    assert _routes(e1)["training"] == "ELIGIBLE"
    assert _routes(e1)["exit_constraint"] == "WITHIN_MODELED_BUDGET"


def test_t04_clock_cross_product_recomputed_at_both_boundaries():
    cases = [
        ("2027-09-01", "2027-05-31", 2, 2, "ELIGIBLE"),
        ("2027-09-01", "2027-06-01", 6, 8, "BLOCKED_BY_MODELED_RULE"),
        ("2026-06-01", "2027-09-01", 2, 2, "ELIGIBLE"),
        ("2027-01-01", "2027-06-01", 6, 8, "BLOCKED_BY_MODELED_RULE"),
        ("2026-12-31", "2027-09-01", 2, 2, "ELIGIBLE"),
    ]
    adapter = W.make_adapter()
    for valid_at, published_asof, fee, exit_cost, route in cases:
        clock = W.clock("AS_OF", valid_at, published_asof)
        receipt = W.serve(adapter, clock)["receipt"]
        values = receipt["structural_values"]
        assert (values["training_fee"]["value"], values["exit_cost"]["value"]) == \
            (fee, exit_cost), (valid_at, published_asof)
        assert _routes(receipt)["training"] == route
        assert receipt["native_field_readset"]["as_of"] == published_asof
        assert receipt["selection"]["valid_at"] == valid_at
    control = W.serve(W.make_adapter(), W.E2_AS_OF)["receipt"]
    served = W.serve(W.make_adapter(), W.E2)["receipt"]
    control_values = {k: v.get("value") for k, v in control["structural_values"].items()}
    served_values = {k: v.get("value") for k, v in served["structural_values"].items()}
    assert control_values == served_values
    assert _routes(control) == _routes(served) == {
        "training": "BLOCKED_BY_MODELED_RULE", "civil": "ELIGIBLE",
        "exit_constraint": "RESOURCE_CONSTRAINED"}
    assert control["selection"]["mode"] == "AS_OF"


def test_t05_epoch_recepts_match_pinned_product_and_history_is_stable():
    pin = json.loads(PINNED_PRODUCT.read_text())
    e1 = W.serve(W.make_adapter(), W.E1)
    e2 = W.serve(W.make_adapter(), W.E2)
    for label, result in (("E1_EARLY_2026", e1), ("E2_LATE_2027", e2)):
        json_receipt = json.loads(json.dumps(result["receipt"], sort_keys=True))
        assert json_receipt == pin["epoch_receipts"][label]
        assert result["receipt"]["receipt_hash"] == pin["epochs"][label]["receipt_hash"]
        assert result["receipt"]["snapshot_hash"] == pin["epochs"][label]["snapshot_hash"]
    one_adapter = W.make_adapter()
    first = W.serve(one_adapter, W.E1)["receipt"]
    W.serve(one_adapter, W.E2)
    resserved = W.serve(one_adapter, W.E1)["receipt"]
    assert resserved["receipt_hash"] == first["receipt_hash"]
    historical = one_adapter.historical_receipt(first["receipt_hash"])
    assert historical["archival_only"] is True
    assert historical["fresh_use_authorized"] is False
    assert historical["receipt"]["structural_values"] == first["structural_values"]


def test_t06_revocation_matrix_is_typed_and_selective():
    civil = W.make_adapter()
    before = W.serve(civil, W.E1)
    old_hash = before["receipt"]["receipt_hash"]
    invalidation = civil.invalidate("civil_sanction")
    after = W.serve(civil, W.E1)["receipt"]
    assert after["state"] == "TYPED_PARTIAL_SELECTED_WORLD"
    assert _routes(after)["civil"] == "UNAVAILABLE_AUTHORITY_OR_CLOCK"
    assert _routes(after)["training"] == "ELIGIBLE"
    assert _routes(after)["exit_constraint"] == "WITHIN_MODELED_BUDGET"
    assert old_hash in invalidation["invalidated_for_fresh_use"]

    fee = W.make_adapter()
    civil_only = ("civil_open", "civil_sanction")
    civil_only_hash = W.serve(fee, W.E1, keys=civil_only,
                              consumers=False)["receipt"]["receipt_hash"]
    fee_invalidation = fee.invalidate("training_fee")
    assert civil_only_hash in fee_invalidation["unaffected"]
    civil_only_after = W.serve(fee, W.E1, keys=civil_only, consumers=False)["receipt"]
    assert civil_only_after["state"] == "SELECTED_WORLD_VALUES_SERVED"
    full_after = W.serve(fee, W.E1)["receipt"]
    assert _routes(full_after)["training"] == "UNAVAILABLE_AUTHORITY_OR_CLOCK"
    assert _routes(full_after)["civil"] == "ELIGIBLE"

    native = W.make_adapter()
    native.invalidate(GSS)
    native_receipt = W.serve(native, W.E1)["receipt"]
    nf = native_receipt["native_field_readset"]
    assert native_receipt["state"] == "TYPED_PARTIAL_SELECTED_WORLD"
    assert nf["state"] == "PARTIAL_TEST_ONLY_NOT_POSITIVE"
    assert [r["role"] for r in nf["values_read"]] == [NCA]
    assert any(r["role"] == GSS for r in nf["refusals"])
    assert _routes(native_receipt) == {
        "training": "ELIGIBLE", "civil": "ELIGIBLE",
        "exit_constraint": "WITHIN_MODELED_BUDGET"}


def test_t07_mismatch_matrix_refuses_untyped_reuse():
    base = W.make_adapter()
    q1 = W.make_request(W.E1)
    s1 = base.build_snapshot(q1)
    acc1 = base.accept(q1, s1)
    consumers1 = [W.consume(base.service, s1)["material"],
                  W.evaluate(base.service, s1, W.PROPOSALS)["material"]]
    q2 = W.make_request(W.E2)
    s2 = base.build_snapshot(q2)
    acc2 = base.accept(q2, s2)
    consumers2 = [W.consume(base.service, s2)["material"],
                  W.evaluate(base.service, s2, W.PROPOSALS)["material"]]
    foreign = W.make_adapter(empirical_changed=True)
    tampered_material = json.loads(json.dumps(s1.material))
    tampered_material["source_permission_root"] = "CALLER_ROOT"
    from product.world import SelectedSnapshot
    tampered = SelectedSnapshot(tampered_material, semantic_hash(tampered_material))
    for label, call, code in (
            ("foreign_accept", lambda: foreign.accept(q1, s1),
             "UNREGISTERED_SELECTED_SNAPSHOT"),
            ("foreign_serve", lambda: foreign.serve(q1, acc1, s1, consumers=consumers1),
             "ACCEPTANCE_BINDING_MISMATCH"),
            ("cross_epoch_acceptance", lambda: base.serve(q2, acc1, s2, consumers=consumers2),
             "ACCEPTED_SNAPSHOT_SUBSTITUTION"),
            ("rehashed_tampered", lambda: base.accept(q1, tampered),
             "UNREGISTERED_SELECTED_SNAPSHOT")):
        with pytest.raises(ValueError) as err:
            call()
        if code is not None:
            assert code in str(err.value), label


def test_t08_authority_flags_and_forbidden_tokens_absent_from_receipts():
    freeze = bootstrap.freeze()
    tokens = freeze["world_receipt_must_not_contain_tokens"]
    assert "N8E" in tokens and "GHA_R5" in tokens
    e1 = W.serve(W.make_adapter(), W.E1)["receipt"]
    e2 = W.serve(W.make_adapter(), W.E2)["receipt"]
    for receipt in (e1, e2):
        strings = []
        _walk_strings(receipt, strings)
        blob = "|".join(strings)
        for token in tokens:
            assert token not in blob
        for flag, value in freeze["world_receipt_required_flags"].items():
            if flag in receipt:
                assert receipt[flag] == value, flag
        non = receipt["consumers"][0]["consumer_material"]
        assert non["actor_executions"] == 0 and non["model_calls"] == 0
        assert receipt["operative_N9"] is False and receipt["operative_OC05"] is False
        assert receipt["issued_N5N6"] is False and receipt["issued_EE13"] is False
    assert e1["claim_ceiling"] == "SOURCE_LOCAL_EMPIRICAL_POSSIBILITY_NOT_CAUSAL_OR_PERSONAL"


def _pin_file(path):
    if path.endswith("e05r_selected_world_adapter.py"):
        return RUNTIME / "selected" / "e05_n9_selected_world_adapter.py"
    if path.endswith("pre553_hq297_n9c_two_field_reader.py"):
        return RUNTIME / "selected" / "native_extra" / "pre553_hq297_n9c_two_field_reader.py"
    if path.endswith("pre553_n9_n10w_progressive_candidate.py"):
        return RUNTIME / "selected" / "native_extra" / "pre553_n9_n10w_progressive_candidate.py"
    if path.endswith("02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json"):
        return RUNTIME / "selected" / "fixtures" / "02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json"
    if path.endswith("test_product.py"):
        return RUNTIME / "author_courts" / "test_product_r10.py"
    if "-R10-E04-" in path and "/product/" in path:
        return RUNTIME / "selected" / "product" / Path(path).name
    if path.startswith(("rawlsing_next/", "data/")):
        return T35_ROOT / path
    raise AssertionError("UNMAPPED_PIN:" + path)


def test_t09_every_pinned_closure_file_matches_its_own_recorded_preimage():
    for pin in bootstrap.freeze()["pinned_closure"]:
        file = _pin_file(pin["path"])
        data = file.read_bytes()
        assert _git_blob(data) == pin["git_blob"], pin["path"]
        assert hashlib.sha256(data).hexdigest() == pin["sha256"], pin["path"]
        tree = subprocess.run(
            ["git", "-C", str(T35_ROOT), "ls-tree", pin["commit"], pin["path"]],
            capture_output=True, text=True)
        assert tree.returncode == 0, pin["path"]
        assert pin["git_blob"] in tree.stdout, pin["path"]
    t35_adapter = (RUNTIME / "selected/e05_n9_selected_world_adapter.py").read_bytes()
    n9j_adapter = (N9J_ROOT / "WORKER_RETURNS/PYAT-R37-N9J-SELECTED-WORLD-PROGRESSIVE-"
                   "CONSUMER-R1/native/e05_n9_selected_world_adapter.py").read_bytes()
    assert _git_blob(t35_adapter) == "690790e81854cde363643edc64946ddc63c58dbf"
    assert _git_blob(n9j_adapter) == "642381bc033aaeef878624bdce71f9f94708043d"
    assert _git_blob(t35_adapter) != _git_blob(n9j_adapter)


def test_t10_cold_redrive_is_byte_identical_to_the_pinned_product(tmp_path):
    pinned = PINNED_PRODUCT.read_bytes()
    assert hashlib.sha256(pinned).hexdigest() == PINNED_SHA256
    assert len(pinned) == PINNED_BYTES
    out = tmp_path / "t35_adversarial_product.json"
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run(
        [sys.executable, "two_epoch_world.py", str(out)],
        cwd=str(RUNTIME), env=env, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr[-2000:]
    fresh = out.read_bytes()
    assert fresh == pinned
    assert hashlib.sha256(fresh).hexdigest() == PINNED_SHA256
    cold_a = (RETURN / "02_PINNED_NATIVE_TEMPORAL_IMPORTS_AND_JUNIT/cold_a.json").read_bytes()
    cold_b = (RETURN / "02_PINNED_NATIVE_TEMPORAL_IMPORTS_AND_JUNIT/cold_b.json").read_bytes()
    assert cold_a == cold_b == pinned
    product = json.loads(fresh)
    assert product["failed_assertions"] == []
    assert all(product["assertions"].values())
    assert product["terminal"].startswith("TWO_EPOCH_TEST_ONLY_NATIVE_WORLD_CONSUMER_POSITIVE")
    assert product["sealed_startup"] == "5064d76b3c58a8225693055a8ec6bb07e216d9b1"
    assert product["contract"] == "N9_SELECTED_WORLD_REQUEST@2"
    n8e = product["n8e_input"]
    assert n8e["state"] == "ABSENT_HOLD" and n8e["numeric_delta"] is None
    assert n8e["measured_no_change"] is None and n8e["world_input"] is False
    assert n8e["consumer_input"] is False
    v553 = product["v553_candidate"]
    assert v553["empty_readiness_error_count"] == 45
    assert v553["candidate_verdict"] == \
        "V553_STRUCTURAL_TEMPORAL_HARMONIZATION_CANDIDATE__NOT_N8E_SURVEY_COMPARATOR"
    adapter_rows = [r for r in product["import_preimages"]
                    if r["path"].endswith("e05_n9_selected_world_adapter.py")]
    assert adapter_rows and adapter_rows[0]["git_blob"] == \
        "690790e81854cde363643edc64946ddc63c58dbf"
    assert adapter_rows[0]["source_commit"] == "84485d32c0088995f8dc664dc0517b2d27f2563d"


def test_t11_runtime_is_wall_clock_and_network_free():
    for name in ("bootstrap.py", "two_epoch_world.py", "runner_cold.py",
                 "n8e_sourcefree_comparator.py", "v553_candidate_eval.py"):
        source = (RUNTIME / name).read_text()
        for token in ("datetime.now", "utcnow", "time.time(", "time.sleep",
                      "os.getpid", "socket", "urllib", "requests.",
                      "http://", "https://"):
            assert token not in source, (name, token)


def test_t12_r13_adapter_types_zero_support_step_without_n9j_keyerror():
    """The T35 adapter (R13 E05R) must survive the no-evidence step path.

    The N9J-delivered R11 adapter crashes with KeyError('binding_order') there
    (see the N9J adversarial court); this court verifies the newer R13 seam
    actually fixes it and emits a typed partial receipt instead.
    """
    adapter = _mk(support_loss=True)
    q = W.make_request(W.E1)
    s = adapter.build_snapshot(q)
    acc = adapter.accept(q, s)
    consumers = [W.consume(adapter.service, s)["material"],
                 W.evaluate(adapter.service, s, W.PROPOSALS)["material"]]
    receipt = adapter.serve(q, acc, s, consumers=consumers)
    assert receipt["state"] == "TYPED_PARTIAL_SELECTED_WORLD"
    assert receipt["empirical_state"] == "PARTIAL_TYPED_EMPIRICAL_SUPPORT"
    last = receipt["empirical_steps"][-1]
    assert last["denominator"] == 0
    assert last["cells"] == []
    assert any(i.startswith("EMPIRICAL_NOT_PRODUCTIVE") for i in receipt["inconsistencies"])
    assert _routes(receipt)["training"] == "ELIGIBLE"


def test_t13_r13_adapter_refuses_tampered_consumer_envelopes():
    adapter = W.make_adapter()
    result = W.serve(adapter, W.E2)
    q, s, acc = result["request"], result["snapshot"], result["acceptance"]
    materials = [W.consume(adapter.service, s)["material"],
                 W.evaluate(adapter.service, s, W.PROPOSALS)["material"]]
    assert adapter.serve(q, acc, s, consumers=materials)["state"] == \
        "SELECTED_WORLD_VALUES_SERVED"
    tampered = json.loads(json.dumps(materials))
    tampered[0]["structural_routes"]["training"]["state"] = "ELIGIBLE"
    with pytest.raises(ValueError) as err:
        adapter.serve(q, acc, s, consumers=tampered)
    assert "CONSUMER_MATERIAL_NOT_EXACT_ORIGINAL_OUTPUT" in str(err.value)
    trimmed = [materials[0]]
    with pytest.raises(ValueError) as err2:
        adapter.serve(q, acc, s, consumers=trimmed)
    assert "TWO_ORIGINAL_CONSUMERS_REQUIRED" in str(err2.value)
