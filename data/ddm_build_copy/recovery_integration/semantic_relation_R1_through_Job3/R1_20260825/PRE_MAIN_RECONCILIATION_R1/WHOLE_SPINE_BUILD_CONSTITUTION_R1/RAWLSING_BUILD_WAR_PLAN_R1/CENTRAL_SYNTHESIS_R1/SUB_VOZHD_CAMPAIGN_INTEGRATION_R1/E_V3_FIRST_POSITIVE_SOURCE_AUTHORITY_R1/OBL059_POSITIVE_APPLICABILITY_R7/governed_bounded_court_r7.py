"""Governed bounded court for OBL059 R7 outer Mapping snapshot repair."""

from __future__ import annotations

import importlib.util
import json
import unittest
from collections.abc import Mapping
from pathlib import Path

HERE = Path(__file__).resolve().parent
R6_DIR = HERE.parent / "OBL059_POSITIVE_APPLICABILITY_R6"
R7_AUTHORITY = HERE / "positive_applicability_authority_r7.py"

r7_spec = importlib.util.spec_from_file_location("_obl059_r7_authority", R7_AUTHORITY)
if r7_spec is None or r7_spec.loader is None:
    raise RuntimeError(f"cannot load R7 authority: {R7_AUTHORITY}")
r7 = importlib.util.module_from_spec(r7_spec)
r7_spec.loader.exec_module(r7)

r6_court_path = R6_DIR / "governed_bounded_court_r6.py"
r6_spec = importlib.util.spec_from_file_location("_obl059_r6_court_for_r7", r6_court_path)
if r6_spec is None or r6_spec.loader is None:
    raise RuntimeError(f"cannot load R6 court: {r6_court_path}")
r6_court = importlib.util.module_from_spec(r6_spec)
r6_spec.loader.exec_module(r6_court)

# Route inherited public evaluation points through frozen R7.
r6_court.r6.evaluate_direct_positive_applicability = r7.evaluate_direct_positive_applicability
r6_court.r5_court.r5.evaluate_direct_positive_applicability = r7.evaluate_direct_positive_applicability
r6_court.r5_court.r4_court.r4.evaluate_direct_positive_applicability = r7.evaluate_direct_positive_applicability
r6_court.r5_court.r4_court.r3_court.r3.evaluate_direct_positive_applicability = r7.evaluate_direct_positive_applicability
r6_court.r5_court.r4_court.r3_court.r2_court.r2.evaluate_direct_positive_applicability = r7.evaluate_direct_positive_applicability
r6_court.r5_court.r4_court.r3_court.r2_court.r1_court.evaluate_direct_positive_applicability = r7.evaluate_direct_positive_applicability

EFFECT_KEYS = tuple(r6_court.EFFECT_KEYS)


def fixture():
    return r6_court.fixture()


class CarrierMapping(Mapping):
    """Configurable Mapping used to verify the single snapshot boundary."""

    def __init__(self, data, fail=None):
        self._data = data
        self._fail = fail

    def _maybe(self, name):
        if self._fail == name:
            raise RuntimeError(f"carrier-{name}-failure")

    def __getitem__(self, key):
        self._maybe("getitem")
        return self._data[key]

    def __iter__(self):
        self._maybe("iter")
        return iter(self._data)

    def __len__(self):
        self._maybe("len")
        return len(self._data)

    def keys(self):
        self._maybe("keys")
        return self._data.keys()

    def items(self):
        self._maybe("items")
        return self._data.items()

    def values(self):
        self._maybe("values")
        return self._data.values()

    def get(self, key, default=None):
        self._maybe("get")
        return self._data.get(key, default)

    def __contains__(self, key):
        self._maybe("contains")
        return key in self._data

    def __repr__(self):
        self._maybe("repr")
        return "CarrierMapping(<bounded>)"

    def __str__(self):
        self._maybe("str")
        return "CarrierMapping"


class MappingLookalike:
    def __iter__(self):
        raise RuntimeError("lookalike-iter-must-not-run")

    def __len__(self):
        raise RuntimeError("lookalike-len-must-not-run")

    def __getitem__(self, key):
        raise RuntimeError("lookalike-getitem-must-not-run")

    def keys(self):
        raise RuntimeError("lookalike-keys-must-not-run")

    def __repr__(self):
        raise RuntimeError("lookalike-repr-must-not-run")


class NestedThrowingMapping(Mapping):
    def __getitem__(self, key):
        raise RuntimeError("nested-getitem-must-not-run")

    def __iter__(self):
        raise RuntimeError("nested-iter-must-not-run")

    def __len__(self):
        raise RuntimeError("nested-len-must-not-run")

    def items(self):
        raise RuntimeError("nested-items-must-not-run")

    def keys(self):
        raise RuntimeError("nested-keys-must-not-run")

    def __repr__(self):
        raise RuntimeError("nested-repr-must-not-run")


class CourtR7(r6_court.CourtR6):
    REQUIRED = tuple(r7._REQUIRED_BINDINGS)

    def assert_no_effect(self, result):
        for key in EFFECT_KEYS:
            self.assertFalse(result[key], key)

    def assert_negative_total(self, packet):
        try:
            result = r7.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(f"R7 carrier path raised {type(exc).__name__}: {exc}")
        self.assertEqual(result["decision"], r7.NEGATIVE_DECISION, result)
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64)
        self.assert_no_effect(result)
        return result

    def test_81_well_behaved_custom_mapping_preserves_authorized_positive_semantics(self):
        packet = fixture()
        result = r7.evaluate_direct_positive_applicability(CarrierMapping(packet))
        self.assertEqual(result["decision"], r7.POSITIVE_DECISION, result)
        self.assert_no_effect(result)
        self.assertEqual(result, r7._r6.evaluate_direct_positive_applicability(packet))

    def test_82_throwing_outer_mapping_protocols_never_escape(self):
        methods = ("keys", "iter", "getitem", "len", "items", "values", "get", "contains")
        for method in methods:
            with self.subTest(method=method):
                data = fixture()
                data["actor_id"] = 10 ** 5000
                result = self.assert_negative_total(CarrierMapping(data, fail=method))
                self.assertIn(
                    result["reason"],
                    ("PACKET_MALFORMED", "MALFORMED_BINDING:actor_id"),
                )

    def test_83_reproduced_throwing_keys_case_closes_without_hidden_backing_inspection(self):
        data = fixture()
        data["actor_id"] = 10 ** 5000
        result = self.assert_negative_total(CarrierMapping(data, fail="keys"))
        self.assertEqual(result["reason"], "PACKET_MALFORMED")
        self.assertEqual(result["bindings"]["actor_id"], None)

    def test_84_mapping_lookalike_is_not_promoted_to_authorized_mapping_carrier(self):
        result = self.assert_negative_total(MappingLookalike())
        self.assertEqual(result["reason"], "PACKET_MALFORMED")

    def test_85_positive_looking_custom_mapping_needs_real_complete_content(self):
        data = fixture()
        del data["evidence"]
        data.update({
            "classification": "public clinic",
            "routing": "eligible",
            "occurrence": True,
            "causal_use_permission": True,
            "contact_witness_independence": True,
            "narrative_plausibility": "obvious",
        })
        result = self.assert_negative_total(CarrierMapping(data))
        self.assertNotEqual(result["decision"], r7.POSITIVE_DECISION)

    def test_86_exact_dict_nested_custom_mapping_remains_isolated(self):
        for key in self.REQUIRED:
            with self.subTest(key=key):
                packet = fixture()
                packet[key] = NestedThrowingMapping()
                result = self.assert_negative_total(packet)
                self.assertEqual(result["reason"], f"MALFORMED_BINDING:{key}")

    def test_87_custom_mapping_snapshot_is_single_use_and_deterministic_for_same_content(self):
        data = fixture()
        data["world_id"] = 10 ** 5000
        first = self.assert_negative_total(CarrierMapping(dict(data)))
        second = self.assert_negative_total(CarrierMapping(dict(data)))
        self.assertEqual(first, second)
        self.assertEqual(first["proof_sha256"], second["proof_sha256"])

    def test_88_exact_dict_path_is_byte_for_byte_r6_for_ordinary_controls(self):
        packets = [fixture()]
        p = fixture(); p["execution_scope"] = "PROJECT_CURRENT"; packets.append(p)
        p = fixture(); p["actor_id"] = 7; packets.append(p)
        p = fixture(); del p["world_id"]; packets.append(p)
        for index, packet in enumerate(packets):
            with self.subTest(index=index):
                self.assertEqual(
                    r7.evaluate_direct_positive_applicability(packet),
                    r7._r6.evaluate_direct_positive_applicability(packet),
                )

    def test_89_unrelated_delegate_errors_remain_visible_after_successful_snapshot(self):
        original = r7._r6.evaluate_direct_positive_applicability
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("r7-deliberate-programmer-error")
                r7._r6.evaluate_direct_positive_applicability = deliberate
                with self.subTest(exc_type=exc_type.__name__):
                    with self.assertRaisesRegex(exc_type, "r7-deliberate-programmer-error"):
                        r7.evaluate_direct_positive_applicability(fixture())
                    with self.assertRaisesRegex(exc_type, "r7-deliberate-programmer-error"):
                        r7.evaluate_direct_positive_applicability(CarrierMapping(fixture()))
        finally:
            r7._r6.evaluate_direct_positive_applicability = original

    def test_90_r7_revision_identity_is_exact(self):
        self.assertEqual(
            r7.R7_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R7",
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CourtR7)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({
        "court": "OBL059_R7_GOVERNED_BOUNDED_COURT",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "successful": result.wasSuccessful(),
        "execution_scope": r7.SYNTHETIC_SCOPE,
        "project_current_state_created": False,
        "independent_review_performed": False,
    }, sort_keys=True))
    raise SystemExit(0 if result.wasSuccessful() else 1)
