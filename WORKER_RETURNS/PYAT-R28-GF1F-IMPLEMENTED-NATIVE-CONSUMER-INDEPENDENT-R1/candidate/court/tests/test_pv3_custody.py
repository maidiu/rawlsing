"""Additional request/control-boundary falsifiers; arithmetic remains PV2I's."""

import copy, json, subprocess, sys, os
from dataclasses import replace, FrozenInstanceError
from pathlib import Path
import pytest
import pv2_sourcefree_fixture as F
from fixture_owner import FixtureOwnerControl, pinned
from pv3_candidate import RequestAPI, validate_consumer_roles_against_declared
from rawlsing_next.pre553_empirical_objects import semantic_hash

R = Path(__file__).resolve().parents[1]


@pytest.fixture
def case(tmp_path):
    owner = FixtureOwnerControl()  # installation precedes all caller work/production
    api = RequestAPI(owner.client(), owner._attest)
    fx = F.pv2_sourcefree_fixture(tmp_path / "ledger")
    kw = dict(
        expected=fx["expected"],
        selected_scopes=fx["plans"],
        register=fx["register"],
        scope_metadata=tuple(fx["meta"]),
    )
    report = api.run_sourcefree_with_register(**kw)
    return owner, api, fx, kw, report


def test_source_selective_withdrawal_preserves_exact_other_namespace(case):
    owner, api, fx, kw, r = case
    history = copy.deepcopy(r)
    before = api.read_current_consumer_material(
        fx["register"], r, namespace="PV2-ADULT-B"
    )
    owner.withdraw("PV2-ADULT-A", "INDEPENDENT_SOURCE_A_WITHDRAWAL")
    a = api.read_current_consumer_material(fx["register"], r, namespace="PV2-ADULT-A")
    b = api.read_current_consumer_material(fx["register"], r, namespace="PV2-ADULT-B")
    assert not a["servable"] and a["links"] == [] and b == before and r == history
    allread = api.read_current_consumer_material(fx["register"], r)
    assert not allread["servable"] and len(allread["links"]) == 3
    assert all(
        l["original_identity"]["original"]["respondent_namespace"] == "PV2-ADULT-B"
        for l in allread["links"]
    )
    with pytest.raises(ValueError):
        api.run_sourcefree_with_register(**kw)
    (R / "observations/selective_revocation.json").write_text(
        json.dumps(
            {
                "A": a,
                "B_before": before,
                "B_after": b,
                "history_bit_stable": r == history,
            },
            indent=2,
        )
        + "\n"
    )


def test_old_request_snapshot_does_not_undo_owner_withdrawal(case):
    owner, api, fx, kw, r = case
    old = copy.deepcopy(fx["register"])
    owner.withdraw("PV2-ADULT-A")
    for _ in range(2):
        assert not api.read_current_consumer_material(old, r, namespace="PV2-ADULT-A")[
            "servable"
        ]
    assert owner.resolutions[-2:] == [("PV2-ADULT-A", 2)] * 2


@pytest.mark.parametrize("change", ["clock", "asof", "edition"])
def test_each_read_resolves_owner_edition_clock_asof(case, change):
    owner, api, fx, kw, r = case
    ns = "PV2-ADULT-A"
    old = owner._state[ns]
    owner.advance(ns, edition="NEW_SOURCE_EDITION" if change == "edition" else None)
    options = {change: getattr(old, change)}
    result = api.read_current_consumer_material(
        fx["register"], r, namespace=ns, **options
    )
    assert not result["servable"] and result["links"] == []
    assert api.read_current_consumer_material(
        fx["register"], r, namespace="PV2-ADULT-B"
    )["servable"]


@pytest.mark.parametrize(
    "field,value",
    [
        ("scope", "self-issued unrestricted"),
        ("revoked", True),
        ("ceiling", ("PRODUCTION",)),
        ("issuer", "FORGED_FIXTURE_OWNER"),
    ],
)
def test_request_grant_never_controls_owner_state(case, field, value):
    owner, api, fx, kw, r = case
    reg = replace(
        fx["register"],
        fixture_use_grant=replace(fx["register"].fixture_use_grant, **{field: value}),
    )
    before = copy.deepcopy(owner._state)
    with pytest.raises(ValueError):
        api.read_current_consumer_material(reg, r)
    with pytest.raises(ValueError):
        api.run_sourcefree_with_register(**dict(kw, register=reg))
    assert owner._state == before
    assert api.read_current_consumer_material(fx["register"], r)["servable"]


def test_forged_fixture_owner_cannot_be_installed_in_request(case):
    owner, api, fx, kw, r = case
    with pytest.raises(TypeError):
        api.run_sourcefree_with_register(
            **kw, fixture_owner=FixtureOwnerControl("R2_Y1")
        )
    with pytest.raises(FrozenInstanceError):
        api._owner = FixtureOwnerControl("R2_Y1").client()
    with pytest.raises(FrozenInstanceError):
        api._owner.installation.expected_root = "f" * 64
    with pytest.raises(FrozenInstanceError):
        api._owner.installation = FixtureOwnerControl("R2_Y1").installation


def test_coherent_renamed_report_ref_cannot_mint_custody(case):
    owner, api, fx, kw, r = case
    fake = copy.deepcopy(r)
    l = fake["links"][0]
    m = l["consumer_material"]
    m["conditional_count_profile"][0]["condition_denominator_support"] = 999
    h = semantic_hash(
        {k: v for k, v in m.items() if k not in ("object_id", "content_hash")}
    )
    m["content_hash"] = h
    m["object_id"] = "urn:rawlsing:field-forge:conditional-support:sha256:" + h
    l["consumer_ref"]["content_hash"] = h
    l["consumer_ref"]["object_id"] = m["object_id"]
    from fixture_owner import canonical
    import hashlib

    material = canonical(
        {
            k: fake[k]
            for k in (
                "links",
                "nonrunnable",
                "original_expected_digest",
                "pv3_receipt_proofs",
                "pv2_register",
            )
        }
    )
    fake["pv3_custody"]["material_sha256"] = hashlib.sha256(
        material.encode()
    ).hexdigest()
    with pytest.raises(ValueError, match="OFFLINE_FACT_RESTORATION_HOLD"):
        api.read_current_consumer_material(fx["register"], fake)


@pytest.mark.parametrize(
    "field", ["producer_query_ref", "risk_set_ref", "producer_fact_ref"]
)
def test_missing_query_risk_and_fact_material_fail_closed(case, field):
    owner, api, fx, kw, r = case
    links = copy.deepcopy(r["links"])
    links[0]["consumer_material"].pop(field)
    with pytest.raises(ValueError):
        validate_consumer_roles_against_declared(links, fx["register"])


def test_deep_read_mutation_does_not_corrupt_service_or_historical_report(case):
    owner, api, fx, kw, r = case
    history = copy.deepcopy(r)
    result = api.read_current_consumer_material(fx["register"], r)
    result["links"][0]["consumer_material"]["conditional_count_profile"][0][
        "condition_denominator_support"
    ] = 999
    result["current_decisions"]["PV2-ADULT-A"]["issuer"] = "MUTANT"
    assert r == history
    reread = api.read_current_consumer_material(fx["register"], r)
    assert (
        reread["links"] == history["links"]
        and reread["current_decisions"]["PV2-ADULT-A"]["issuer"] != "MUTANT"
    )


@pytest.mark.parametrize(
    "field",
    [
        "result_refs",
        "manifest_hash",
        "unit_key",
        "attempt_index",
        "journal_seq",
        "receipt_state",
    ],
)
def test_separate_journal_fields_must_match_actual_owner_receipt(case, field):
    owner, api, fx, kw, r = case
    session = fx["plans"][0].p01_kwargs["session"]
    p = session.side_effect_journal_path
    lines = p.read_text().splitlines()
    row = json.loads(lines[0])
    before = [len(c) for c in fx["calls"]]
    if field == "result_refs":
        row[field][0]["content_hash"] = "f" * 64
    elif isinstance(row[field], int):
        row[field] += 1
    else:
        row[field] = "FORGED"
    lines[0] = json.dumps(row)
    p.write_text("\n".join(lines) + "\n")
    with pytest.raises(ValueError):
        api.run_sourcefree_with_register(**kw)
    assert [len(c) for c in fx["calls"]] == before


def test_changed_checkpoint_identity_is_refused_before_any_new_unit(case):
    owner, api, fx, kw, r = case
    p = fx["plans"][0].p01_kwargs["session"].store.path
    d = json.loads(p.read_text())
    d["identity"]["manifest_hash"] = "f" * 64
    p.write_text(json.dumps(d))
    before = [len(c) for c in fx["calls"]]
    with pytest.raises(ValueError):
        api.run_sourcefree_with_register(**kw)
    assert [len(c) for c in fx["calls"]] == before


def test_generic_label_red_is_contained_by_explicit_hold(case):
    owner, api, fx, kw, r = case
    assert all(
        l["consumer_material"]["roles"]["CONDITIONER"]["source_native_variable"]
        == "Q86B"
        and l["consumer_material"]["roles"]["TARGET"]["source_native_variable"]
        == "Q86A"
        for l in r["links"]
    )
    result = api.read_current_consumer_material(
        fx["register"], r, semantics="GENERIC_NATIVE"
    )
    assert result == {
        "servable": False,
        "claim": "GENERIC_NATIVE_SEMANTICS_HOLD",
        "historical_links": 6,
    }
    assert api.read_current_consumer_material(
        fx["register"], r, semantics="SPECIALIZED_TEST_ONLY"
    )["servable"]
    (R / "observations/generic_semantics_hold.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )


def test_true_fresh_process_does_not_claim_offline_fact_restoration(case, tmp_path):
    owner, api, fx, kw, r = case
    p = tmp_path / "history.json"
    p.write_text(json.dumps(r))
    cmd = [sys.executable, str(R / "repro/offline_read.py"), str(p)]
    out = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
    assert out.returncode == 0, out.stderr
    observed = json.loads(out.stdout)
    assert (
        observed["pid"] != os.getpid()
        and observed["claim"] == "OFFLINE_FACT_RESTORATION_HOLD"
        and observed["source_calls"] == 0
    )
    (R / "observations/offline_fact_restoration_hold.json").write_text(
        json.dumps({"argv": cmd, "exit": out.returncode, **observed}, indent=2) + "\n"
    )


def test_owner_withdrawal_persists_in_true_fresh_process(case, tmp_path):
    _, _, fx, kw, r = case
    policy = tmp_path / "independent_owner/current.json"
    owner = FixtureOwnerControl(policy_path=policy, provision=True)
    api = RequestAPI(owner.client(), owner._attest)
    history = api.run_sourcefree_with_register(**kw)
    b_before = api.read_current_consumer_material(
        fx["register"], history, namespace="PV2-ADULT-B"
    )
    owner.withdraw("PV2-ADULT-A", "PERSISTED_SOURCE_A_WITHDRAWAL")
    history_path = tmp_path / "history.json"
    history_path.write_text(json.dumps(history))
    saved = policy.read_bytes()
    cmd = [
        sys.executable,
        str(R / "repro/current_owner_child.py"),
        str(policy),
        str(history_path),
    ]
    p = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
    assert p.returncode == 0, p.stderr
    observed = json.loads(p.stdout)
    assert observed["pid"] != os.getpid()
    assert observed["decisions"]["PV2-ADULT-A"]["withdrawn"] is True
    assert observed["decisions"]["PV2-ADULT-B"]["withdrawn"] is False
    assert not observed["old_request_read"]["servable"]
    assert observed["old_request_read"]["claim"] == "OFFLINE_FACT_RESTORATION_HOLD"
    assert policy.read_bytes() == saved
    assert (
        api.read_current_consumer_material(
            fx["register"], history, namespace="PV2-ADULT-B"
        )
        == b_before
    )
    (R / "observations/persisted_selective_revocation.json").write_text(
        json.dumps(
            {
                "argv": cmd,
                "exit": p.returncode,
                "actual": observed,
                "policy_unchanged_in_child": True,
                "B_current_material_bit_stable_in_live_service": True,
            },
            indent=2,
        )
        + "\n"
    )


def test_missing_owner_store_fails_closed_and_is_not_reprovisioned(case, tmp_path):
    policy = tmp_path / "independent_owner/current.json"
    owner = FixtureOwnerControl(policy_path=policy, provision=True)
    owner.withdraw("PV2-ADULT-A")
    policy.unlink()
    with pytest.raises(ValueError, match="CURRENT_OWNER_SERVICE_UNAVAILABLE"):
        owner.client().resolve("PV2-ADULT-A")
    with pytest.raises(ValueError, match="CURRENT_OWNER_SERVICE_UNAVAILABLE"):
        FixtureOwnerControl(policy_path=policy)
    assert not policy.exists()


def test_two_service_clients_resolve_the_same_current_owner_decision(case, tmp_path):
    policy = tmp_path / "independent_owner/current.json"
    first = FixtureOwnerControl(policy_path=policy, provision=True)
    second = FixtureOwnerControl(policy_path=policy)
    old = second.client().resolve("PV2-ADULT-A")
    first.withdraw("PV2-ADULT-A", "OWNER_SERVICE_EVENT")
    current = second.client().resolve("PV2-ADULT-A")
    assert (
        old.withdrawn is False
        and current.withdrawn is True
        and current.clock == old.clock + 1
    )
    assert second.client().resolve("PV2-ADULT-B").clock == 1


def test_current_read_binds_receipt_and_journal_proof_content(case):
    owner, api, fx, kw, r = case
    fake = copy.deepcopy(r)
    fake["pv3_receipt_proofs"][0][0]["journal"]["result_refs"][0]["content_hash"] = (
        "f" * 64
    )
    with pytest.raises(ValueError, match="CONSUMER_CUSTODY_CONTENT_MISMATCH"):
        api.read_current_consumer_material(fx["register"], fake)
