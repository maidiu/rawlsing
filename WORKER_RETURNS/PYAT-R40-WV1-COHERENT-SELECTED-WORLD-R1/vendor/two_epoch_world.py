"""R35 T35 two-epoch TEST_ONLY institutional-rule world over real E04/M4/M5.

The institutional rules are synthesized TEST_ONLY values published through the
original E04 catalog's own ``_publish`` path.  The E04 consumers, M4 V557/V558
publication/repository law, M5 RSC currentness and the N9C two-field reader are
executed unchanged.  Nothing here installs N9/OC05, reads original source,
issues EE12, models a structural route or acts as a Sorok actor.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from contextlib import contextmanager
from pathlib import Path

import bootstrap

bootstrap.install()

import e05_n9_selected_world_adapter as E
from product.nonparent import consume
from product.scenario import evaluate
from product.service import GenericSelectedWorldService
from product.world import SelectedSnapshot
from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_hq297_n9c_two_field_reader import GSS, TestOnlyRegistry

RETURN = bootstrap.RETURN
SEALED = bootstrap.SEALED
CONTRACT = E.CONTRACT
PROPOSALS = [
    {"scenario_id": "INSTITUTIONAL_ROUTE", "route": "institutional"},
    {"scenario_id": "CIVIL_ROUTE", "route": "civil"},
]
E1 = E.SelectedWorldClock("AS_OF", "2026-06-01", "2026-04-15")
E2 = E.SelectedWorldClock("TEST_CURRENT", "2027-09-01", "2027-09-01",
                          test_now="2027-09-01")
E2_AS_OF = E.SelectedWorldClock("AS_OF", "2027-09-01", "2027-09-01")
RULE_REVISION = dict(effective_from="2027-01-01", effective_to="2028-01-01",
                     publication="2027-06-01", revision=2)


def clock(mode: str, valid_at: str, published_asof: str, test_now=None):
    return E.SelectedWorldClock(mode, valid_at, published_asof, test_now=test_now)


def make_adapter(*, variant: str = "two_epoch", empirical_changed: bool = False):
    """Build one TEST_ONLY world.  ``variant`` selects the institutional rules.

    two_epoch : base rule + fee/exit revision 2
    base      : base rule only (for same-clock material-control)
    formal    : base rule + training_access revision 2 false only
    """
    if variant not in ("two_epoch", "base", "formal"):
        raise ValueError("UNKNOWN_WORLD_VARIANT:" + str(variant))
    service = GenericSelectedWorldService(empirical_changed=empirical_changed)
    catalog = service.catalog
    if variant == "two_epoch":
        catalog._publish("training_fee", 6, RULE_REVISION["effective_from"],
                         RULE_REVISION["effective_to"],
                         RULE_REVISION["publication"],
                         revision=RULE_REVISION["revision"])
        catalog._publish("exit_cost", 8, RULE_REVISION["effective_from"],
                         RULE_REVISION["effective_to"],
                         RULE_REVISION["publication"],
                         revision=RULE_REVISION["revision"])
    elif variant == "formal":
        catalog._publish("training_access", False,
                         RULE_REVISION["effective_from"],
                         RULE_REVISION["effective_to"],
                         RULE_REVISION["publication"],
                         revision=RULE_REVISION["revision"])
    catalog.catalog_hash = semantic_hash(
        dict(records=catalog.records, empirical=catalog.empirical_identity()))
    adapter = E.N9SelectedWorldAdapter(
        service=service, registry=TestOnlyRegistry(bootstrap.fixture_rows()))
    return adapter


def make_request(clock_value, keys=None):
    return E.N9SelectedWorldRequest(
        contract=CONTRACT, purpose="TEST_ONLY_CONTEXT",
        structural_keys=tuple(keys or E.STRUCTURAL_KEYS),
        empirical_target="Y",
        empirical_conditions=(("A", 1), ("B", 1), ("C", 1)),
        native_field_roles=E.NATIVE_FIELD_ROLES, clock=clock_value)


def serve(adapter, clock_value, *, keys=None, consumers=True):
    keys = tuple(keys or E.STRUCTURAL_KEYS)
    full = set(keys) == set(E.STRUCTURAL_KEYS)
    if consumers and not full:
        raise ValueError("CONSUMERS_REQUIRE_FULL_STRUCTURAL_READSET")
    request = make_request(clock_value, keys)
    snapshot = adapter.build_snapshot(request)
    acceptance = adapter.accept(request, snapshot)
    materials = []
    if consumers:
        materials = [consume(adapter.service, snapshot)["material"],
                     evaluate(adapter.service, snapshot, PROPOSALS)["material"]]
    receipt = adapter.serve(request, acceptance, snapshot, consumers=materials)
    return dict(request=request, snapshot=snapshot, acceptance=acceptance,
                materials=materials, receipt=receipt)


def _step_view(step):
    return dict(
        target=step["target"],
        denominator=step["denominator"],
        cells={cell["cell"]: cell["raw_numerator_support"]
               for cell in step["cells"]},
        conditioners=[list(c) for c in step["conditioners"]],
        state=step["state"],
        evidence_ref=step.get("evidence_ref"),
        source_universe_ref=step.get("source_universe_ref"),
        release_ref=step.get("release_ref"),
        risk_set_ref=step.get("risk_set_ref"),
    )


def receipt_view(label, result, clock_value):
    receipt = result["receipt"]
    structural = {}
    for key, value in receipt["structural_values"].items():
        structural[key] = {name: value.get(name) for name in (
            "value", "unit", "revision", "publication", "effective_from",
            "state", "requested_ref", "field_ref", "rsc_ref",
            "validation_ref", "currentness_ref", "epistemic_class",
            "currentness_grade") if name in value}
    routes = {key: dict(state=value["state"],
                        dependencies=value["dependencies"],
                        value_refs=value["value_refs"])
              for key, value in
              receipt["consumers"][0]["consumer_material"]["structural_routes"].items()}
    scenarios = [dict(scenario_id=row["scenario_id"], route=row["route"],
                      feasibility=row["feasibility"],
                      selection_weight=row.get("selection_weight"),
                      weight_reason=row.get("weight_reason"))
                 for row in receipt["consumers"][1]["consumer_material"]["scenarios"]]
    native = receipt["native_field_readset"]
    return dict(
        label=label,
        clock=clock_value.binding(),
        selection=receipt["selection"],
        receipt_state=receipt["state"],
        acceptance_state=receipt["acceptance_state"],
        receipt_hash=receipt["receipt_hash"],
        snapshot_hash=receipt["snapshot_hash"],
        acceptance_hash=receipt["acceptance_hash"],
        structural_values=structural,
        structural_value_refs=receipt["structural_value_refs"],
        nonparent_routes=routes,
        scenario_feasibility=scenarios,
        empirical_steps=[_step_view(step) for step in receipt["empirical_steps"]],
        empirical_state=receipt["empirical_state"],
        empirical_native_time=receipt.get("empirical_native_time"),
        native_field_readset=dict(
            roles=native["roles"], state=native["state"], as_of=native["as_of"],
            values_read=[dict(role=row["role"], native_unit=row["native_unit"],
                              native_geography=row["native_geography"],
                              native_measure=row["native_measure"],
                              fixture_ref=row["fixture_ref"],
                              values=row["values"])
                         for row in native["values_read"]],
            refusals=native["refusals"]),
        units=receipt["native_units"],
        source_families=receipt["source_families"],
        inconsistencies=receipt["inconsistencies"],
        snapshot_flags=dict(
            operative_CURRENT=result["snapshot"].material.get("operative_CURRENT"),
            operative_N9=result["snapshot"].material.get("operative_N9")),
        flags=dict(operative_N9=receipt["operative_N9"],
                   operative_OC05=receipt["operative_OC05"],
                   pooling=receipt["pooling"],
                   person_exposure=receipt["person_exposure"],
                   model_use=receipt["model_use"],
                   issued_EE13=receipt["issued_EE13"],
                   issued_N5N6=receipt["issued_N5N6"],
                   actor_executions=receipt["consumers"][0]["consumer_material"].get("actor_executions"),
                   model_calls=receipt["consumers"][0]["consumer_material"].get("model_calls")),
    )


def _steps(receipt):
    return [dict(denominator=step["denominator"],
                 cells={cell["cell"]: cell["raw_numerator_support"]
                        for cell in step["cells"]})
            for step in receipt["empirical_steps"]]


def _routes(receipt):
    return {key: value["state"] for key, value in
            receipt["consumers"][0]["consumer_material"]["structural_routes"].items()}


def _scenarios(receipt):
    return [row["feasibility"] for row in
            receipt["consumers"][1]["consumer_material"]["scenarios"]]


def consumer_delta(e1, e2):
    a = e1["receipt"]
    b = e2["receipt"]
    structural = {}
    for key in E.STRUCTURAL_KEYS:
        av = a["structural_values"][key]
        bv = b["structural_values"][key]
        structural[key] = dict(
            epoch_1=av.get("value"), epoch_2=bv.get("value"),
            changed=av.get("value") != bv.get("value"),
            formal_eligibility=(key == "training_access"),
            material_constraint=(key in ("training_fee", "exit_cost")),
        )
    routes_1, routes_2 = _routes(a), _routes(b)
    scenarios_1, scenarios_2 = _scenarios(a), _scenarios(b)
    changed_routes = [k for k in routes_1 if routes_1[k] != routes_2[k]]
    return dict(
        structural=structural,
        practical_routes=dict(epoch_1=routes_1, epoch_2=routes_2,
                              changed=changed_routes),
        scenarios=dict(epoch_1=scenarios_1, epoch_2=scenarios_2,
                       changed=[i for i, (x, y) in enumerate(zip(scenarios_1, scenarios_2))
                                if x != y]),
        empirical=dict(
            epoch_1_steps=_steps(a), epoch_2_steps=_steps(b),
            identical=_steps(a) == _steps(b),
            epoch_1_source_balance=[row["source_balance_count"] for row in
                                    a["consumers"][0]["consumer_material"]["source_balance_reads"]],
            epoch_2_source_balance=[row["source_balance_count"] for row in
                                    b["consumers"][0]["consumer_material"]["source_balance_reads"]],
        ),
        formal_eligibility_preserved=(
            structural["training_access"]["epoch_1"] is True and
            structural["training_access"]["epoch_2"] is True),
        material_affordability_changed=(
            structural["training_fee"]["changed"] and
            structural["exit_cost"]["changed"]),
        legitimate_null_effects=[
            "civil route unchanged: " + routes_1["civil"] + " -> " + routes_2["civil"],
            "institutional proposal feasibility unchanged: " +
            scenarios_1[0] + " -> " + scenarios_2[0],
            "empirical possibility steps unchanged under the rule-only change",
        ],
    )


@contextmanager
def profile_calls():
    counts = Counter()

    def trace(frame, _event, _arg):
        module = frame.f_globals.get("__name__", "")
        if module.startswith(("rawlsing_next.m4", "rawlsing_next.m5",
                              "rawlsing_next.pre553_empirical",
                              "rawlsing_next.pre553_analytical",
                              "rawlsing_next.source_backed",
                              "product.", "e05_n9_selected_world_adapter")):
            counts[(module, frame.f_code.co_name)] += 1

    sys.setprofile(trace)
    try:
        yield counts
    finally:
        sys.setprofile(None)


def _refusal(fn):
    try:
        fn()
    except Exception as exc:  # exact native refusal is the evidence
        return dict(refused=True, type=type(exc).__name__, message=str(exc))
    return dict(refused=False)


def clock_cross_product():
    adapter = make_adapter()
    out = []
    for valid_at, published_asof, interpretation in (
            ("2027-09-01", "2027-05-31", "effective but unpublished revision"),
            ("2027-09-01", "2027-06-01", "publication boundary"),
            ("2026-06-01", "2027-09-01", "retrospective as-of query"),
            ("2027-01-01", "2027-06-01", "effective boundary"),
            ("2026-12-31", "2027-09-01", "day before effective boundary")):
        result = serve(adapter, clock("AS_OF", valid_at, published_asof))
        receipt = result["receipt"]
        out.append(dict(
            valid_at=valid_at, published_asof=published_asof,
            interpretation=interpretation,
            training_access=receipt["structural_values"]["training_access"].get("value"),
            training_fee=receipt["structural_values"]["training_fee"].get("value"),
            exit_cost=receipt["structural_values"]["exit_cost"].get("value"),
            training_route=_routes(receipt)["training"],
            receipt_hash=receipt["receipt_hash"],
        ))
    return out


def formal_isolation():
    base = make_adapter(variant="base")
    formal = make_adapter(variant="formal")
    base_result = serve(base, E2)
    formal_result = serve(formal, E2)
    base_r, formal_r = base_result["receipt"], formal_result["receipt"]
    return dict(
        clock=E2.binding(),
        material_control=dict(
            adapter_variant="base",
            training_access=base_r["structural_values"]["training_access"].get("value"),
            training_fee=base_r["structural_values"]["training_fee"].get("value"),
            exit_cost=base_r["structural_values"]["exit_cost"].get("value"),
            training_route=_routes(base_r)["training"],
            scenarios=_scenarios(base_r),
            receipt_hash=base_r["receipt_hash"]),
        formal_rule=dict(
            adapter_variant="formal",
            training_access=formal_r["structural_values"]["training_access"].get("value"),
            training_fee=formal_r["structural_values"]["training_fee"].get("value"),
            exit_cost=formal_r["structural_values"]["exit_cost"].get("value"),
            training_route=_routes(formal_r)["training"],
            scenarios=_scenarios(formal_r),
            receipt_hash=formal_r["receipt_hash"]),
        empirical_steps_identical=_steps(base_r) == _steps(formal_r),
        material_constraints_held_fixed=(
            base_r["structural_values"]["training_fee"].get("value") ==
            formal_r["structural_values"]["training_fee"].get("value") == 2 and
            base_r["structural_values"]["exit_cost"].get("value") ==
            formal_r["structural_values"]["exit_cost"].get("value") == 2),
    )


def source_rule_matrix():
    base = make_adapter()
    changed = make_adapter(empirical_changed=True)
    views = {}
    for name, adapter in (("base_E1", base), ("base_E2", base),
                          ("changed_E1", changed), ("changed_E2", changed)):
        clock_value = E1 if name.endswith("E1") else E2
        views[name] = serve(adapter, clock_value)
    base_e1, base_e2 = views["base_E1"]["receipt"], views["base_E2"]["receipt"]
    changed_e1 = views["changed_E1"]["receipt"]
    changed_e2 = views["changed_E2"]["receipt"]
    return dict(
        base_E1=receipt_view("base_E1", views["base_E1"], E1),
        base_E2=receipt_view("base_E2", views["base_E2"], E2),
        changed_E1=receipt_view("changed_E1", views["changed_E1"], E1),
        changed_E2=receipt_view("changed_E2", views["changed_E2"], E2),
        rule_only_change=dict(
            empirical_identical=_steps(base_e1) == _steps(base_e2),
            structural_routes_changed=_routes(base_e1) != _routes(base_e2)),
        source_only_change=dict(
            empirical_changed=_steps(base_e1) != _steps(changed_e1),
            structural_routes_identical=_routes(base_e1) == _routes(changed_e1)),
        source_and_rule=dict(
            empirical_changed=_steps(base_e1) != _steps(changed_e2),
            structural_routes_changed=_routes(base_e1) != _routes(changed_e2)),
        base_balance=[row["source_balance_count"] for row in
                      base_e1["consumers"][0]["consumer_material"]["source_balance_reads"]],
        changed_balance=[row["source_balance_count"] for row in
                         changed_e1["consumers"][0]["consumer_material"]["source_balance_reads"]],
    )


def revocation_cases():
    civil = make_adapter()
    before = serve(civil, E1)
    old_hash = before["receipt"]["receipt_hash"]
    invalidation = civil.invalidate("civil_sanction")
    after = serve(civil, E1)
    historical = civil.historical_receipt(old_hash)
    after_r = after["receipt"]

    fee = make_adapter()
    civil_only_keys = ("civil_open", "civil_sanction")
    civil_only_before = serve(fee, E1, keys=civil_only_keys, consumers=False)
    civil_only_hash = civil_only_before["receipt"]["receipt_hash"]
    fee_invalidation = fee.invalidate("training_fee")
    civil_only_after = serve(fee, E1, keys=civil_only_keys, consumers=False)
    full_after = serve(fee, E1)
    full_after_r = full_after["receipt"]

    native = make_adapter()
    native.invalidate(GSS)
    native_after = serve(native, E1)
    native_r = native_after["receipt"]

    return dict(
        civil_sanction=dict(
            invalidation=invalidation,
            before_receipt_hash=old_hash,
            after_state=after_r["state"],
            after_civil_route=_routes(after_r)["civil"],
            after_training_route=_routes(after_r)["training"],
            after_exit_constraint=_routes(after_r)["exit_constraint"],
            after_civil_value=after_r["structural_values"]["civil_sanction"],
            historical=dict(archival_only=historical["archival_only"],
                            fresh_use_authorized=historical["fresh_use_authorized"]),
            old_receipt_invalidated=old_hash in invalidation["invalidated_for_fresh_use"],
        ),
        training_fee=dict(
            invalidation=fee_invalidation,
            civil_only_before_hash=civil_only_hash,
            civil_only_before_in_unaffected=(
                civil_only_hash in fee_invalidation["unaffected"]),
            civil_only_after_state=civil_only_after["receipt"]["state"],
            full_after_state=full_after_r["state"],
            full_after_training_route=_routes(full_after_r)["training"],
            full_after_civil_route=_routes(full_after_r)["civil"],
        ),
        native_field=dict(
            revoked_role=GSS,
            after_state=native_r["state"],
            native_state=native_r["native_field_readset"]["state"],
            remaining_roles=[row["role"] for row in
                             native_r["native_field_readset"]["values_read"]],
            refusals=native_r["native_field_readset"]["refusals"],
        ),
    )


def mismatch_cases():
    base = make_adapter()
    q = make_request(E1)
    s = base.build_snapshot(q)
    acc = base.accept(q, s)
    consumers = [consume(base.service, s)["material"],
                 evaluate(base.service, s, PROPOSALS)["material"]]
    q2 = make_request(E2)
    s2 = base.build_snapshot(q2)
    acc2 = base.accept(q2, s2)
    consumers2 = [consume(base.service, s2)["material"],
                  evaluate(base.service, s2, PROPOSALS)["material"]]

    foreign = make_adapter(empirical_changed=True)
    tampered_material = json.loads(json.dumps(s.material))
    tampered_material["source_permission_root"] = "CALLER_ROOT"
    tampered = SelectedSnapshot(tampered_material, semantic_hash(tampered_material))

    return dict(
        foreign_source_world_snapshot=dict(
            expectation="UNREGISTERED_SELECTED_SNAPSHOT",
            refusal=_refusal(lambda: foreign.accept(q, s))),
        foreign_acceptance_into_other_world=dict(
            expectation="ACCEPTANCE_BINDING_MISMATCH",
            refusal=_refusal(lambda: foreign.serve(
                q, acc, s, consumers=consumers))),
        cross_epoch_acceptance_snapshot=dict(
            expectation="ACCEPTED_SNAPSHOT_SUBSTITUTION",
            refusal=_refusal(lambda: base.serve(
                q2, acc, s2, consumers=consumers2))),
        rehashed_tampered_snapshot=dict(
            expectation="UNREGISTERED_SELECTED_SNAPSHOT",
            refusal=_refusal(lambda: base.accept(q, tampered))),
    )


def _walk_strings(value, out):
    if isinstance(value, dict):
        for key, item in value.items():
            out.append(str(key))
            _walk_strings(item, out)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _walk_strings(item, out)
    elif isinstance(value, str):
        out.append(value)


def forbidden_tokens(views):
    tokens = bootstrap.freeze()["world_receipt_must_not_contain_tokens"]
    found = []
    for label, view in views.items():
        strings = []
        _walk_strings(view, strings)
        blob = "|".join(strings)
        for token in tokens:
            if token in blob:
                found.append(dict(epoch=label, token=token))
    return found


def import_manifest():
    rows = []
    for name, module in sorted(sys.modules.items()):
        file = getattr(module, "__file__", None)
        if not file:
            continue
        path = Path(file).resolve()
        if path.suffix != ".py":
            continue
        if not (path.is_relative_to(bootstrap.REPO) or
                path.is_relative_to(bootstrap.RETURN)):
            continue
        data = path.read_bytes()
        staged = bootstrap.staged_source_path(path) if path.is_relative_to(
            bootstrap.RETURN) else None
        if staged:
            commit, source_path = staged
            rel = path.relative_to(bootstrap.RETURN).as_posix()
            kind = "STAGED_PINNED_NATIVE"
        elif path.is_relative_to(bootstrap.RUNTIME):
            commit, source_path = None, path.relative_to(bootstrap.RETURN).as_posix()
            rel = source_path
            kind = "WORKER_TRANSPORT"
        else:
            commit, source_path = SEALED, path.relative_to(bootstrap.REPO).as_posix()
            rel = source_path
            kind = "SEALED_NATIVE"
        pin = bootstrap.frozen_pin(source_path)
        rows.append(dict(
            module=name, path=rel, kind=kind, source_commit=commit,
            source_path=source_path,
            git_blob=bootstrap.git_blob_sha1(data),
            sha256=bootstrap.sha256(data), bytes=len(data),
            frozen_pin_present=pin is not None,
            frozen_pin_match=(None if pin is None else
                              (pin["git_blob"] == bootstrap.git_blob_sha1(data) and
                               pin["sha256"] == bootstrap.sha256(data))),
        ))
    return rows


def _staged_path_for_pin(pin):
    path = pin["path"]
    if path.endswith("e05r_selected_world_adapter.py"):
        return bootstrap.RETURN / "runtime" / "selected" / "e05_n9_selected_world_adapter.py"
    if path.endswith("pre553_hq297_n9c_two_field_reader.py"):
        return (bootstrap.RETURN / "runtime" / "selected" / "native_extra" /
                "pre553_hq297_n9c_two_field_reader.py")
    if path.endswith("pre553_n9_n10w_progressive_candidate.py"):
        return (bootstrap.RETURN / "runtime" / "selected" / "native_extra" /
                "pre553_n9_n10w_progressive_candidate.py")
    if path.endswith("02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json"):
        return (bootstrap.RETURN / "runtime" / "selected" / "fixtures" /
                "02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json")
    if path.endswith("test_product.py"):
        return bootstrap.RETURN / "runtime" / "author_courts" / "test_product_r10.py"
    if "-R10-E04-" in path and "/product/" in path:
        return (bootstrap.RETURN / "runtime" / "selected" / "product" /
                Path(path).name)
    if path.startswith("rawlsing_next/") or path.startswith("data/"):
        return bootstrap.REPO / path
    raise ValueError("UNMAPPED_PIN:" + path)


def pinned_closure_verification():
    rows = []
    for pin in bootstrap.freeze()["pinned_closure"]:
        path = _staged_path_for_pin(pin)
        data = path.read_bytes()
        blob = bootstrap.git_blob_sha1(data)
        digest = bootstrap.sha256(data)
        rows.append(dict(
            source_commit=pin["commit"], source_path=pin["path"],
            staged_path=path.relative_to(bootstrap.RETURN).as_posix()
            if path.is_relative_to(bootstrap.RETURN) else path.relative_to(bootstrap.REPO).as_posix(),
            expected_git_blob=pin["git_blob"], actual_git_blob=blob,
            expected_sha256=pin["sha256"], actual_sha256=digest,
            match=blob == pin["git_blob"] and digest == pin["sha256"]))
    return rows


def n8e_absent_hold():
    return dict(
        state="ABSENT_HOLD",
        claim_id="N8E_GHA_R5Q43_R9Q31_DSAT_R1",
        reason=("N03 requires exact original merged-release custody, national "
                "design/weight/variance authority, an independent science decision "
                "and a positive exact EE12/C7 relation before any wave fact; none "
                "is issued in this return"),
        actual_result_state="HELD_UPSTREAM_EVIDENCE_AND_ISSUANCE",
        numeric_delta=None,
        measured_no_change=None,
        world_input=False,
        m4_root_input=False,
        consumer_input=False,
        n9_installation_state="NOT_INSTALLED_HOLD",
        separate_owner_record="04_GHANA_EE12_EXACT_PENDING_OWNER_RECORD.md",
    )


def build_product():
    import v553_candidate_eval

    with profile_calls() as counts:
        e1_adapter = make_adapter()
        e2_adapter = make_adapter()
        e1 = serve(e1_adapter, E1)
        e2 = serve(e2_adapter, E2)
        e2_asof = serve(make_adapter(), E2_AS_OF)
        source_rule = source_rule_matrix()
        formal = formal_isolation()
        clocks = clock_cross_product()
        revocations = revocation_cases()
        mismatches = mismatch_cases()

    e1_view = receipt_view("E1_EARLY_2026", e1, E1)
    e2_view = receipt_view("E2_LATE_2027", e2, E2)
    control_view = receipt_view("E2_AS_OF_CONTROL", e2_asof, E2_AS_OF)
    control_values = {key: value.get("value") for key, value in
                      control_view["structural_values"].items()}
    e2_values = {key: value.get("value") for key, value in
                 e2_view["structural_values"].items()}
    control_routes = {key: value["state"] for key, value in
                      control_view["nonparent_routes"].items()}
    e2_routes = {key: value["state"] for key, value in
                 e2_view["nonparent_routes"].items()}
    control_scenarios = [row["feasibility"] for row in control_view["scenario_feasibility"]]
    e2_scenarios = [row["feasibility"] for row in e2_view["scenario_feasibility"]]
    epoch_clock_mode_control = dict(
        control_clock=E2_AS_OF.binding(),
        structural_values=control_values,
        nonparent_routes=control_routes,
        scenarios=control_scenarios,
        identical_institutional_rule=(control_values == e2_values and
                                      control_routes == e2_routes and
                                      control_scenarios == e2_scenarios),
        note=("The late epoch's rule is also selectable under an explicit AS_OF "
              "clock; the TEST_CURRENT clock is a synthetic test clock and the "
              "snapshot's operative_CURRENT flag remains false."),
    )
    delta = consumer_delta(e1, e2)
    views = dict(E1=e1_view, E2=e2_view)
    forbidden = forbidden_tokens(views)
    raw_counts = [dict(module=module, function=function, count=count)
                  for (module, function), count in sorted(counts.items())
                  if not function.startswith("<") and not function.startswith("__")]
    native_summary = [
        dict(module=module, function=function, count=count)
        for (module, function), count in sorted(counts.items())
        if function in ("resolve_v558", "build_v557_publication_bundle",
                        "build_v558_repository_bundle",
                        "make_structural_currentness_receipt",
                        "materialize_resolved_structural_context",
                        "validate_resolved_structural_context",
                        "select", "structural", "possibilities", "progressive",
                        "consume", "evaluate")]
    call_counts = raw_counts
    total_profiled_calls = sum(counts.values())
    has_m4 = any(row["module"] == "rawlsing_next.m4_v557_v558_publication_repository" and
                 row["function"] == "resolve_v558" for row in call_counts)
    has_m5 = any(row["module"] == "rawlsing_next.m5_runtime_rsc_peer_prior" and
                 row["function"] == "materialize_resolved_structural_context"
                 for row in call_counts)

    assertions = dict(
        both_epochs_served=(e1_view["receipt_state"] == "SELECTED_WORLD_VALUES_SERVED" and
                            e2_view["receipt_state"] == "SELECTED_WORLD_VALUES_SERVED"),
        formal_eligibility_preserved=delta["formal_eligibility_preserved"],
        material_affordability_and_exit_changed=delta["material_affordability_changed"],
        practical_opportunity_changed=(
            delta["practical_routes"]["epoch_1"]["training"] == "ELIGIBLE" and
            delta["practical_routes"]["epoch_2"]["training"] == "BLOCKED_BY_MODELED_RULE" and
            delta["practical_routes"]["epoch_2"]["exit_constraint"] == "RESOURCE_CONSTRAINED"),
        empirical_steps_identical=delta["empirical"]["identical"],
        civil_and_proposal_nulls_retained=(
            delta["practical_routes"]["epoch_1"]["civil"] ==
            delta["practical_routes"]["epoch_2"]["civil"] == "ELIGIBLE" and
            delta["scenarios"]["changed"] == []),
        source_only_change_leaves_routes_identical=(
            source_rule["source_only_change"]["structural_routes_identical"]),
        rule_only_change_leaves_empirical_identical=(
            source_rule["rule_only_change"]["empirical_identical"]),
        formal_change_isolated=(
            formal["formal_rule"]["training_access"] is False and
            formal["formal_rule"]["training_fee"] == 2 and
            formal["formal_rule"]["training_route"] == "BLOCKED_BY_MODELED_RULE" and
            formal["formal_rule"]["scenarios"][0] == "INFEASIBLE_MODELED_PREMISE" and
            formal["material_constraints_held_fixed"] and
            formal["empirical_steps_identical"]),
        clock_matrix_matches_frozen=[row["training_fee"] for row in clocks] == [2, 6, 2, 6, 2],
        asof_clock_control_matches_test_current=(
            epoch_clock_mode_control["identical_institutional_rule"] and
            e2_view["snapshot_flags"]["operative_CURRENT"] is False),
        revocation_typed=(
            revocations["civil_sanction"]["after_state"] == "TYPED_PARTIAL_SELECTED_WORLD" and
            revocations["civil_sanction"]["after_civil_route"] == "UNAVAILABLE_AUTHORITY_OR_CLOCK" and
            revocations["civil_sanction"]["historical"]["archival_only"] is True and
            revocations["civil_sanction"]["historical"]["fresh_use_authorized"] is False),
        revocation_selective=(
            revocations["training_fee"]["civil_only_before_in_unaffected"] and
            revocations["training_fee"]["civil_only_after_state"] == "SELECTED_WORLD_VALUES_SERVED" and
            revocations["training_fee"]["full_after_training_route"] == "UNAVAILABLE_AUTHORITY_OR_CLOCK"),
        native_field_revocation_typed=(
            revocations["native_field"]["native_state"] == "PARTIAL_TEST_ONLY_NOT_POSITIVE" and
            revocations["native_field"]["remaining_roles"] == ["NCA_NATIONAL_MOBILE_DATA"]),
        all_mismatches_refused=all(row["refusal"]["refused"] for row in mismatches.values()),
        no_n8e_or_ghana_temporal_context_in_world=not forbidden,
        n8e_envelope_hold=True,
        actor_flags_false=(
            e1_view["flags"]["actor_executions"] == 0 and
            e1_view["flags"]["model_calls"] == 0 and
            e1_view["flags"]["operative_N9"] is False and
            e1_view["flags"]["operative_OC05"] is False and
            e1_view["flags"]["pooling"] is False and
            e1_view["flags"]["person_exposure"] is False and
            e1_view["flags"]["model_use"] is False),
        native_m4_m5_calls_observed=has_m4 and has_m5,
    )
    failed = [name for name, ok in assertions.items() if not ok]
    terminal = ("TWO_EPOCH_TEST_ONLY_NATIVE_WORLD_CONSUMER_POSITIVE__N8E_ABSENT_HOLD"
                if not failed else "TWO_EPOCH_TEST_ONLY_NATIVE_WORLD_PARTIAL_OR_RED")
    product = dict(
        schema="PYAT_R35_T35_TWO_EPOCH_NATIVE_WORLD_CONSUMER_DELTA@1",
        terminal=terminal,
        failed_assertions=failed,
        sealed_startup=SEALED,
        branch="agent/rabochii-pyat-r35-t35-historical-temporal-world-consumer-r1",
        contract="N9_SELECTED_WORLD_REQUEST@2",
        product_type="TEST_ONLY_SELECTED_INSTITUTIONAL_RULE",
        authority=dict(
            operative_N9=False, operative_OC05=False, installed_OC05=False,
            n8e_product=False, n9_installed_historical_context=False,
            n10w_structural_route_model=False, n8s_structural_authority=False,
            original_source_read=False, ee12_issued=False,
            field_forge_issued=False, sorok_actor=False,
            actor_executions=0, model_calls=0),
        epochs=dict(E1_EARLY_2026=e1_view, E2_LATE_2027=e2_view),
        epoch_receipts=dict(E1_EARLY_2026=e1["receipt"],
                            E2_LATE_2027=e2["receipt"]),
        epoch_clock_mode_control=epoch_clock_mode_control,
        consumer_delta=delta,
        timeline_interventions=clocks,
        formal_eligibility_isolation=formal,
        source_versus_rule_matrix=source_rule,
        revocation=revocations,
        mismatch=mismatches,
        n8e_input=n8e_absent_hold(),
        v553_candidate=v553_candidate_eval.evaluate(),
        native_call_counts=call_counts,
        native_call_summary=native_summary,
        total_profiled_calls=total_profiled_calls,
        assertions=assertions,
        pinned_closure_verification=pinned_closure_verification(),
        import_preimages=import_manifest(),
        replay=dict(
            required_child_processes=2,
            product_contains_no_wall_clock_or_pid=True,
            evidence_path="02_PINNED_NATIVE_TEMPORAL_IMPORTS_AND_JUNIT/cold_replay.json",
        ),
    )
    return json.loads(json.dumps(product, sort_keys=True))


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        raise SystemExit("USAGE: two_epoch_world.py <output.json>")
    out = Path(argv[0])
    product = build_product()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(product, sort_keys=True, indent=2) + "\n")
    print(json.dumps(dict(terminal=product["terminal"],
                          failed=product["failed_assertions"],
                          epochs=[product["epochs"][key]["receipt_state"]
                                  for key in ("E1_EARLY_2026", "E2_LATE_2027")]),
                     sort_keys=True))
    return 0 if not product["failed_assertions"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
