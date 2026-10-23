"""R8 targeted successor: exact cache-hit configuration refusal codes.

Limited to the R7-AF-01 correction plus the retained native/cold positives in
the copied R7 successor probes.
"""
from __future__ import annotations

from collections import Counter
import copy
import json
from pathlib import Path

import pytest

from rawlsing_next.pre553_universal_evidence_binding import (
    EvidenceAssociationError,
    EvidenceResolver,
)
from rawlsing_next.tests.n10e_empirical_slice_fixture import at07_rows, build_provider_case
from rawlsing_next.tests.test_universal_evidence_binding import (
    _R4_VERIFIER,
    _binding,
    _reader,
    _request,
    _resolver,
)

OUTCOMES = Path(__file__).resolve().parents[1] / "outcomes"
OBSERVATIONS: list[dict] = []


def _record(name: str, observed: dict) -> None:
    OBSERVATIONS.append({"probe": name, **observed})


@pytest.fixture(scope="module", autouse=True)
def _dump():
    yield
    OUTCOMES.mkdir(parents=True, exist_ok=True)
    (OUTCOMES / "r8_targeted_observations.json").write_text(
        json.dumps(
            {
                "schema": "R61_R08V_R8_TARGETED_OBSERVATIONS@1",
                "probes": OBSERVATIONS,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _canonical(request_id):
    case = build_provider_case("forward")
    request = _request(case, request_id=request_id)
    return case, request


def test_legacy_binding_pin_cache_hit_exact_code():
    case, request = _canonical("r8-legacy-code")
    resolver = _resolver(trusted_binding_hashes=("a" * 64,))
    resolver.bind(_binding(request, case))
    first = resolver.resolve(request)
    second = resolver.resolve(request)
    assert first.result_state == "SUPPORTED"
    assert first.denominator == 60
    assert second.result_state == "UNKNOWN"
    assert second.typed_refusal == "LEGACY_BINDING_PINS_REQUIRE_MIGRATION"
    _record(
        "legacy_binding_pin_replay",
        {"first": first.result_state, "second": second.result_state,
         "second_refusal": second.typed_refusal},
    )


def test_descriptor_pin_cache_hit_exact_code_and_correct_pin_positive():
    case, request = _canonical("r8-descriptor-pin-code")
    live = _resolver(trusted_descriptor_hashes=("a" * 64,))
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    assert resolver.resolve(request).denominator == 60
    baseline = resolver.export_cache()
    descriptor_hash = baseline["entries"][0]["cache_owner_descriptor"]["descriptor_hash"]

    live.bind(_binding(request, case))
    assert live.resolve(request).denominator == 60
    pinned_hit = live.resolve(request)
    assert pinned_hit.result_state == "UNKNOWN"
    assert pinned_hit.typed_refusal == "CACHE_OWNER_DESCRIPTOR_NOT_PINNED"

    correct = EvidenceResolver(
        admission_verifier=_R4_VERIFIER, trusted_descriptor_hashes=(descriptor_hash,)
    )
    correct.import_authenticated_cache(copy.deepcopy(baseline))
    assert _reader(request, correct.resolve(request)).read()["denominator"] == 60
    _record(
        "descriptor_pin_replay",
        {"hit_state": pinned_hit.result_state, "hit_refusal": pinned_hit.typed_refusal,
         "correct_pin_denominator": 60},
    )


def test_genuine_stale_state_remains_generic_and_no_support():
    case, request = _canonical("r8-stale-code")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    produced = resolver.resolve(request)
    assert produced.result_state == "SUPPORTED"
    produced.consumer_values_read["denominator"] = 999
    stale = resolver.resolve(request)
    assert stale.result_state == "UNKNOWN"
    assert stale.typed_refusal == "STALE_OR_UNAUTHENTICATED_CACHE"
    with pytest.raises(EvidenceAssociationError):
        _reader(request, produced).read()
    _record(
        "genuine_stale_replay",
        {"state": stale.result_state, "refusal": stale.typed_refusal,
         "support_served": False},
    )


def test_missing_verifier_cache_hit_preserves_code():
    case, request = _canonical("r8-no-verifier-code")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    assert resolver.resolve(request).denominator == 60
    resolver._admission_verifier = None
    hit = resolver.resolve(request)
    assert hit.result_state == "UNKNOWN"
    assert hit.typed_refusal == "NO_CONFIGURED_TRUST_ROOT"
    _record(
        "missing_verifier_cache_hit",
        {"state": hit.result_state, "refusal": hit.typed_refusal},
    )


def test_import_export_limits_remain_explicit():
    case, request = _canonical("r8-import-export-limits")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    baseline = resolver.export_cache()
    legacy = _resolver(trusted_binding_hashes=("a" * 64,))
    try:
        legacy.import_authenticated_cache(copy.deepcopy(baseline))
    except Exception as exc:
        import_error = str(exc)
    else:
        import_error = None
    try:
        legacy.export_cache()
    except Exception as exc:
        export_error = str(exc)
    else:
        export_error = None
    assert "LEGACY_BINDING_PINS_REQUIRE_MIGRATION" in (import_error or "")
    assert "LEGACY_BINDING_PINS_REQUIRE_MIGRATION" in (export_error or "")
    _record(
        "import_export_limits",
        {"import_error": import_error, "export_error": export_error},
    )
