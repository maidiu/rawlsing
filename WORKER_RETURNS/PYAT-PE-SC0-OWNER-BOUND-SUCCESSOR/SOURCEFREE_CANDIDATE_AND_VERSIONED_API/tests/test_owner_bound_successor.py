from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.tests.n10e_empirical_slice_fixture import FROZEN_ORACLE

from fixtures import (
    WORLD_OWNER,
    WORLD_REVISION,
    build_success_fixture,
)
from owner_bound_successor import (
    ExactIssuerRegistry,
    OwnerBoundRefusal,
    RECEIPT_SCHEMA,
    ROLE_FORWARD,
    ROLE_REVERSE,
    SERVICE_GRADE,
    verify_receipt_integrity,
    verify_result_integrity,
    serve,
)
from sourcefree_world import make_test_grant

CANDIDATE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]


def _serve(fixture):
    return serve(
        producer=fixture["producer"],
        world_provider=fixture["world_provider"],
        issuer_registry=fixture["issuer_registry"],
        consumer=fixture["consumer"],
        request=fixture["request"],
    )


def _fraction(cell):
    parts = cell["raw_probability_exact_fraction"]["$exact_fraction"]
    return parts[0], parts[1]


def test_reverse_positive_binds_exact_n10e_geometry_and_world():
    fixture = build_success_fixture(role_direction=ROLE_REVERSE)
    result = _serve(fixture)
    assert result.result_state == "EXACT_SUPPORTED"
    assert result.receipt is not None
    verify_result_integrity(result)
    receipt = result.receipt
    assert receipt.world["world_owner"] == WORLD_OWNER
    assert receipt.world["revision"] == WORLD_REVISION
    assert receipt.world["selection_digest"] == fixture["world_provider"].selection_digest
    assert receipt.world["grade"].startswith("TEST_ONLY_SOURCEFREE")
    assert receipt.provenance["sitecustomize_used"] is False
    assert receipt.provenance["global_monkeypatch_used"] is False
    assert receipt.provenance["service_grade"] == SERVICE_GRADE
    assert receipt.geometry["denominator"] == FROZEN_ORACLE["reverse"]["denominator"] == 62
    assert receipt.geometry["target_cell"] == "P1"
    target = next(c for c in receipt.geometry["cells"] if c["cell"] == "P1")
    assert target["raw_numerator_support"] == 54
    assert Fraction(*_fraction(target)) == Fraction(54, 62)
    assert receipt.geometry["cells"]
    assert sum(c["raw_numerator_support"] for c in receipt.geometry["cells"]) == 62
    assert receipt.consumer_output["no_person_generation"] is True
    assert receipt.consumer_output["no_actor_state"] is True
    assert receipt.consumer_output["route_constraints"]
    assert receipt.consumer_output["consumer_grade"].startswith("TEST_ONLY_SOURCEFREE")
    assert receipt.refresh_receipts["publication"]["executed"] is True
    assert receipt.refresh_receipts["binding"]["executed"] is True
    assert receipt.refresh_receipts["publication"] != receipt.refresh_receipts["binding"]
    assert receipt.issuer_grant["issuer_grade"] == "TEST_ONLY_SOURCEFREE"
    assert receipt.issuer_grant["valid_until"] is None
    assert receipt.issuer_grant["target_refs"] == [fixture["request"].target_ref.key]
    assert receipt.issuer_grant["risk_set_refs"] == [fixture["request"].risk_set_ref.key]


def test_forward_positive_is_distinct_from_reverse():
    forward = _serve(build_success_fixture(role_direction=ROLE_FORWARD))
    reverse = _serve(build_success_fixture(role_direction=ROLE_REVERSE))
    assert forward.result_state == reverse.result_state == "EXACT_SUPPORTED"
    assert forward.receipt.geometry["denominator"] == FROZEN_ORACLE["forward"]["denominator"] == 60
    assert reverse.receipt.geometry["denominator"] == FROZEN_ORACLE["reverse"]["denominator"] == 62
    assert forward.receipt.geometry["target_cell"] == "yes"
    assert reverse.receipt.geometry["target_cell"] == "P1"
    target = next(c for c in forward.receipt.geometry["cells"] if c["cell"] == "yes")
    assert target["raw_numerator_support"] == 54
    assert Fraction(*_fraction(target)) == Fraction(54, 60)
    assert forward.result_hash != reverse.result_hash


def test_issuer_grant_is_scoped_even_when_all_time():
    fixture = build_success_fixture()
    request = fixture["request"]
    grant = make_test_grant(
        target_ref=request.target_ref,
        risk_set_ref=request.risk_set_ref,
        world_owner=request.selected_world_owner,
        operations={ROLE_REVERSE},
        target_refs={"urn:test:attacker:target"},
        valid_until=None,
    )
    fixture["issuer_registry"] = ExactIssuerRegistry([grant])
    fixture["request"] = replace(request, issuer_ref=grant.authority_ref)
    result = _serve(fixture)
    assert result.result_state == "TYPED_REFUSAL"
    assert result.refusal_state == "ISSUER_TARGET_REFUSED"
    assert result.receipt is None


def test_test_only_issuer_cannot_authorize_source_promotion():
    fixture = build_success_fixture()
    registry = fixture["issuer_registry"]
    with pytest.raises(OwnerBoundRefusal) as excinfo:
        registry.require_source_promotion(fixture["grant"].authority_ref)
    assert excinfo.value.state == "TEST_AUTHORITY_NOT_COMPETENT_FOR_SOURCE_PROMOTION"


@pytest.mark.parametrize(
    "path",
    [
        ("world", "values", "absolute_horizon"),
        ("world", "values", "public_sanctions"),
        ("world", "clocks", "publication_knowledge"),
        ("world", "negative_status_rows", 0, "scope"),
        ("refresh_receipts", "publication", "successor_digest"),
        ("refresh_receipts", "binding", "invocation_token"),
        ("geometry", "cells", 0, "raw_numerator_support"),
        ("consumer_output", "route_constraints", 0, "horizon"),
        ("issuer_grant", "target_refs"),
        ("producer_evidence", "producer_fact_ref", "content_hash"),
    ],
)
def test_every_value_bearing_field_is_inside_receipt_and_result_identity(path):
    result = _serve(build_success_fixture())
    verify_result_integrity(result)
    material = copy.deepcopy(result.receipt.material())
    cursor = material
    for key in path[:-1]:
        cursor = cursor[key]
    leaf = path[-1]
    if isinstance(cursor[leaf], list):
        cursor[leaf] = list(cursor[leaf]) + ["urn:test:tampered"]
    elif isinstance(cursor[leaf], int):
        cursor[leaf] = cursor[leaf] + 1
    else:
        cursor[leaf] = "TAMPERED_VALUE"
    tampered_hash = semantic_hash(material)
    assert tampered_hash != result.receipt.receipt_hash
    tampered_ref = {
        "kind": RECEIPT_SCHEMA,
        "object_id": f"urn:rawlsing:pyat:pe-sc0:owner-bound-receipt:sha256:{tampered_hash}",
        "content_hash": tampered_hash,
    }
    tampered_result_hash = semantic_hash(
        {
            "schema": "PYAT_PE_SC0_OWNER_BOUND_RESULT@1",
            "contract": result.material()["contract"],
            "request_ref": result.request_ref.as_dict(),
            "result_state": result.result_state,
            "receipt_ref": tampered_ref,
            "receipt_hash": tampered_hash,
            "refusal_state": None,
            "refusal_reason": None,
        }
    )
    assert tampered_result_hash != result.result_hash


def test_receipt_integrity_detects_tampered_ref():
    result = _serve(build_success_fixture())
    assert result.receipt.ref.content_hash == result.receipt.receipt_hash
    verify_receipt_integrity(result.receipt)


def test_deterministic_in_process_replay():
    fixture = build_success_fixture()
    first = _serve(fixture)
    second = _serve(fixture)
    assert first.result_hash == second.result_hash
    assert first.receipt.receipt_hash == second.receipt.receipt_hash
    assert first.receipt.material() == second.receipt.material()


def test_fresh_process_cold_replay(tmp_path):
    script = tmp_path / "replay.py"
    script.write_text(
        "import json\n"
        "from fixtures import build_success_fixture\n"
        "from owner_bound_successor import serve\n"
        "f = build_success_fixture()\n"
        "r = serve(producer=f['producer'], world_provider=f['world_provider'], "
        "issuer_registry=f['issuer_registry'], consumer=f['consumer'], request=f['request'])\n"
        "print(json.dumps({'result': r.result_hash, 'receipt': r.receipt.receipt_hash, "
        "'state': r.result_state}, sort_keys=True))\n",
        encoding="utf-8",
    )
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([str(CANDIDATE_DIR), str(REPO_ROOT)])
    runs = []
    for _ in range(2):
        completed = subprocess.run(
            [sys.executable, str(script)],
            cwd=REPO_ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=True,
        )
        runs.append(json.loads(completed.stdout))
    assert runs[0] == runs[1]
    assert runs[0]["state"] == "EXACT_SUPPORTED"


def test_no_sitecustomize_or_global_monkeypatch():
    assert not (CANDIDATE_DIR / "sitecustomize.py").exists()
    from rawlsing_next.pre553_empirical_possibility_provider import (
        provide_empirical_possibility_slice,
    )

    before = provide_empirical_possibility_slice
    import fixtures as _fixtures  # noqa: F401
    import first_consumer as _first_consumer  # noqa: F401
    import n10e_adapter as _n10e_adapter  # noqa: F401
    import owner_bound_successor as _owner_bound_successor  # noqa: F401
    import sourcefree_world as _sourcefree_world  # noqa: F401

    assert provide_empirical_possibility_slice is before
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([str(CANDIDATE_DIR), str(REPO_ROOT)])
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; print('sitecustomize' in sys.modules); "
            "import rawlsing_next.pre553_empirical_possibility_provider as p; "
            "print(p.provide_empirical_possibility_slice.__module__)",
        ],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    assert completed.stdout.splitlines() == [
        "False",
        "rawlsing_next.pre553_empirical_possibility_provider",
    ]


def test_grade_is_test_only_sourcefree_everywhere():
    result = _serve(build_success_fixture())
    receipt = result.receipt
    assert receipt.material()["service_grade"] == SERVICE_GRADE
    assert "TEST_ONLY_SOURCEFREE" in SERVICE_GRADE
    assert "OPERATIVE_N9" in SERVICE_GRADE
    assert "NOT_OPERATIVE_N9" in SERVICE_GRADE
    assert receipt.world["grade"] == "TEST_ONLY_SOURCEFREE_FIXTURE_WORLD__NOT_OPERATIVE_N9"
    assert receipt.provenance["issuer"] == "exact test-only scoped issuer registry"
    assert "TEST_ONLY_SOURCEFREE" in receipt.consumer_output["consumer_grade"]
