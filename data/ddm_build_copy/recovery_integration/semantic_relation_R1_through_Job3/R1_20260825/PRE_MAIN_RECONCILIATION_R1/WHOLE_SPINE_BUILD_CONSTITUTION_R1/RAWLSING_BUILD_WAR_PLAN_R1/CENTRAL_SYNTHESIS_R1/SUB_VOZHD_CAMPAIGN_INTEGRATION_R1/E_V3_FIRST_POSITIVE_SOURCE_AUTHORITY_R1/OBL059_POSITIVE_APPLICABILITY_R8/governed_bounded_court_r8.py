"""Governed bounded court for OBL059 R8 nested Mapping snapshot repair."""

from __future__ import annotations

import importlib.util
import json
import unittest
from collections.abc import Mapping
from pathlib import Path

HERE = Path(__file__).resolve().parent
R8_AUTHORITY = HERE / "positive_applicability_authority_r8.py"

r8_spec = importlib.util.spec_from_file_location("_obl059_r8_authority", R8_AUTHORITY)
if r8_spec is None or r8_spec.loader is None:
    raise RuntimeError(f"cannot load R8 authority: {R8_AUTHORITY}")
r8 = importlib.util.module_from_spec(r8_spec)
r8_spec.loader.exec_module(r8)

R7_WRAPPER_REL = Path("rawlsing_next/tests/test_subv_e_obl059_positive_applicability_r7_court.py")
ROOT = next(parent for parent in HERE.parents if (parent / R7_WRAPPER_REL).is_file())
r7_wrapper_path = ROOT / R7_WRAPPER_REL
r7_wrapper_spec = importlib.util.spec_from_file_location("_obl059_r7_corrected_wrapper_for_r8", r7_wrapper_path)
if r7_wrapper_spec is None or r7_wrapper_spec.loader is None:
    raise RuntimeError(f"cannot load corrected R7 wrapper: {r7_wrapper_path}")
r7_wrapper = importlib.util.module_from_spec(r7_wrapper_spec)
r7_wrapper_spec.loader.exec_module(r7_wrapper)

# Reuse the exact R7 module objects already bound by the corrected wrapper so
# inherited preservation tests and R8's delegate chain address the same state.
_original_r7 = r7_wrapper.module.r7
r8._r7 = _original_r7
r8._r6 = _original_r7._r6
r7_wrapper.module.r7 = r8

# Route inherited public evaluation points through R8.
r7_wrapper.module.r6_court.r6.evaluate_direct_positive_applicability = r8.evaluate_direct_positive_applicability
r7_wrapper.module.r6_court.r5_court.r5.evaluate_direct_positive_applicability = r8.evaluate_direct_positive_applicability
r7_wrapper.module.r6_court.r5_court.r4_court.r4.evaluate_direct_positive_applicability = r8.evaluate_direct_positive_applicability
r7_wrapper.module.r6_court.r5_court.r4_court.r3_court.r3.evaluate_direct_positive_applicability = r8.evaluate_direct_positive_applicability
r7_wrapper.module.r6_court.r5_court.r4_court.r3_court.r2_court.r2.evaluate_direct_positive_applicability = r8.evaluate_direct_positive_applicability
r7_wrapper.module.r6_court.r5_court.r4_court.r3_court.r2_court.r1_court.evaluate_direct_positive_applicability = r8.evaluate_direct_positive_applicability

EFFECT_KEYS = tuple(r7_wrapper.module.EFFECT_KEYS)


def fixture():
    return r7_wrapper.module.fixture()


class StableNestedMapping(Mapping):
    def __init__(self, data):
        self._data = dict(data)
    def __getitem__(self, key):
        return self._data[key]
    def __iter__(self):
        return iter(self._data)
    def __len__(self):
        return len(self._data)
    def keys(self):
        return list(self._data.keys())


class ReviewFailureNestedMapping(Mapping):
    def __getitem__(self, key):
        raise RuntimeError("nested-field-access-failure")
    def __iter__(self):
        return iter(("placeholder",))
    def __len__(self):
        return 1
    def get(self, key, default=None):
        raise RuntimeError("nested-get-failure")


class ThrowKeysNested(StableNestedMapping):
    def keys(self):
        raise RuntimeError("nested-keys-failure")


class ThrowIterNested(Mapping):
    def __init__(self, data):
        self._data = dict(data)
    def __getitem__(self, key):
        return self._data[key]
    def __iter__(self):
        raise RuntimeError("nested-iter-failure")
    def __len__(self):
        return len(self._data)


class ThrowGetitemNested(StableNestedMapping):
    def __getitem__(self, key):
        raise RuntimeError("nested-getitem-failure")


class ConvenienceMethodsRaiseNested(StableNestedMapping):
    def get(self, key, default=None):
        raise RuntimeError("nested-get-must-not-run")
    def items(self):
        raise RuntimeError("nested-items-must-not-run")
    def values(self):
        raise RuntimeError("nested-values-must-not-run")
    def __contains__(self, key):
        raise RuntimeError("nested-contains-must-not-run")
    def __repr__(self):
        raise RuntimeError("nested-repr-must-not-run")
    def __str__(self):
        raise RuntimeError("nested-str-must-not-run")
    def __hash__(self):
        raise RuntimeError("nested-hash-must-not-run")
    def __eq__(self, other):
        raise RuntimeError("nested-equality-must-not-run")
    def __lt__(self, other):
        raise RuntimeError("nested-order-must-not-run")


class OneShotNestedMapping(Mapping):
    def __init__(self, data):
        self._data = dict(data)
        self._keys = list(self._data.keys())
        self._reads = 0
        self._sealed = False
    def _guard(self):
        if self._sealed:
            raise RuntimeError("nested-read-after-snapshot")
    def keys(self):
        self._guard()
        return list(self._keys)
    def __getitem__(self, key):
        self._guard()
        value = self._data[key]
        self._reads += 1
        if self._reads == len(self._keys):
            self._sealed = True
        return value
    def __iter__(self):
        self._guard()
        return iter(self._keys)
    def __len__(self):
        return len(self._keys)
    def get(self, key, default=None):
        self._guard()
        return self._data.get(key, default)
    def items(self):
        self._guard()
        return self._data.items()
    def values(self):
        self._guard()
        return self._data.values()


class NestedMappingLookalike:
    def keys(self):
        raise RuntimeError("nested-lookalike-keys-must-not-run")
    def __iter__(self):
        raise RuntimeError("nested-lookalike-iter-must-not-run")
    def __getitem__(self, key):
        raise RuntimeError("nested-lookalike-getitem-must-not-run")
    def __len__(self):
        raise RuntimeError("nested-lookalike-len-must-not-run")
    def get(self, key, default=None):
        raise RuntimeError("nested-lookalike-get-must-not-run")


class CourtR8(r7_wrapper.TestOBL059R7BoundedRepair):
    def assert_no_effect(self, result):
        for key in EFFECT_KEYS:
            self.assertFalse(result[key], key)

    def assert_negative_total(self, packet, key=None):
        try:
            result = r8.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(f"R8 negative path raised {type(exc).__name__}: {exc}")
        self.assertEqual(result["decision"], r8.NEGATIVE_DECISION, result)
        if key is not None:
            self.assertEqual(result["reason"], f"MALFORMED_BINDING:{key}", result)
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64)
        self.assert_no_effect(result)
        return result

    def test_91_reproduced_nested_opportunity_mapping_failure_closes(self):
        packet = fixture(); packet["opportunity"] = ReviewFailureNestedMapping()
        result = self.assert_negative_total(packet)
        self.assertEqual(result["reason"], "OPPORTUNITY_BINDING_MISSING_OR_MALFORMED")

    def test_92_reproduced_nested_evidence_mapping_failure_closes(self):
        packet = fixture(); packet["evidence"] = ReviewFailureNestedMapping()
        result = self.assert_negative_total(packet)
        self.assertEqual(result["reason"], "EVIDENCE_MISSING_OR_MALFORMED")

    def test_93_reproduced_nested_actor_evidence_mapping_failure_closes(self):
        packet = fixture(); packet["evidence"]["actor_activation"] = ReviewFailureNestedMapping()
        result = self.assert_negative_total(packet)
        self.assertEqual(result["reason"], "ACTOR_ACTIVATION_EVIDENCE_MISSING")

    def test_94_stable_nested_opportunity_preserves_exact_dict_meaning(self):
        exact = fixture(); mapped = fixture()
        mapped["opportunity"] = StableNestedMapping(mapped["opportunity"])
        self.assertEqual(r8.evaluate_direct_positive_applicability(mapped), r8.evaluate_direct_positive_applicability(exact))

    def test_95_stable_top_level_evidence_preserves_exact_dict_meaning(self):
        exact = fixture(); mapped = fixture()
        mapped["evidence"] = StableNestedMapping(mapped["evidence"])
        self.assertEqual(r8.evaluate_direct_positive_applicability(mapped), r8.evaluate_direct_positive_applicability(exact))

    def test_96_stable_evidence_components_preserve_exact_dict_meaning(self):
        for component in r8._EVIDENCE_COMPONENT_KEYS:
            exact = fixture(); mapped = fixture()
            mapped["evidence"][component] = StableNestedMapping(mapped["evidence"][component])
            with self.subTest(component=component):
                self.assertEqual(r8.evaluate_direct_positive_applicability(mapped), r8.evaluate_direct_positive_applicability(exact))

    def test_97_successful_nested_snapshot_is_single_use(self):
        packets = []
        p = fixture(); p["opportunity"] = OneShotNestedMapping(p["opportunity"]); packets.append(p)
        p = fixture(); p["evidence"] = OneShotNestedMapping(p["evidence"]); packets.append(p)
        for component in r8._EVIDENCE_COMPONENT_KEYS:
            p = fixture(); p["evidence"][component] = OneShotNestedMapping(p["evidence"][component]); packets.append(p)
        for index, packet in enumerate(packets):
            with self.subTest(index=index):
                result = r8.evaluate_direct_positive_applicability(packet)
                self.assertEqual(result["decision"], r8.POSITIVE_DECISION, result)
                self.assert_no_effect(result)

    def test_98_throwing_nested_snapshot_protocols_never_escape(self):
        makers = (ThrowKeysNested, ThrowIterNested, ThrowGetitemNested)
        for maker in makers:
            p = fixture(); p["opportunity"] = maker(p["opportunity"])
            self.assertEqual(self.assert_negative_total(p)["reason"], "OPPORTUNITY_BINDING_MISSING_OR_MALFORMED")
            p = fixture(); p["evidence"] = maker(p["evidence"])
            self.assertEqual(self.assert_negative_total(p)["reason"], "EVIDENCE_MISSING_OR_MALFORMED")
            p = fixture(); p["evidence"]["actor_activation"] = maker(p["evidence"]["actor_activation"])
            self.assertEqual(self.assert_negative_total(p)["reason"], "ACTOR_ACTIVATION_EVIDENCE_MISSING")

    def test_99_unused_nested_convenience_protocols_are_not_reconsulted(self):
        packets = []
        p = fixture(); p["opportunity"] = ConvenienceMethodsRaiseNested(p["opportunity"]); packets.append(p)
        p = fixture(); p["evidence"] = ConvenienceMethodsRaiseNested(p["evidence"]); packets.append(p)
        for component in r8._EVIDENCE_COMPONENT_KEYS:
            p = fixture(); p["evidence"][component] = ConvenienceMethodsRaiseNested(p["evidence"][component]); packets.append(p)
        for index, packet in enumerate(packets):
            with self.subTest(index=index):
                result = r8.evaluate_direct_positive_applicability(packet)
                self.assertEqual(result["decision"], r8.POSITIVE_DECISION, result)
                self.assert_no_effect(result)

    def test_100_outer_and_nested_mapping_snapshots_compose(self):
        packet = fixture()
        packet["opportunity"] = StableNestedMapping(packet["opportunity"])
        packet["evidence"]["actor_activation"] = StableNestedMapping(packet["evidence"]["actor_activation"])
        result = r8.evaluate_direct_positive_applicability(r7_wrapper.module.CarrierMapping(packet))
        self.assertEqual(result, r8.evaluate_direct_positive_applicability(fixture()))

    def test_101_nested_snapshot_failure_is_deterministic(self):
        def make_packet():
            p = fixture(); p["evidence"]["actor_activation"] = ReviewFailureNestedMapping(); return p
        a = self.assert_negative_total(make_packet()); b = self.assert_negative_total(make_packet())
        self.assertEqual(a, b); self.assertEqual(a["proof_sha256"], b["proof_sha256"])

    def test_102_nested_mapping_lookalike_does_not_gain_mapping_status(self):
        packet = fixture(); packet["opportunity"] = NestedMappingLookalike()
        result = self.assert_negative_total(packet)
        self.assertEqual(result["reason"], "OPPORTUNITY_BINDING_MISSING_OR_MALFORMED")

    def test_103_exact_dict_ordinary_controls_remain_exactly_r7(self):
        packets = [fixture()]
        p = fixture(); p["execution_scope"] = "PROJECT_CURRENT"; packets.append(p)
        p = fixture(); p["actor_id"] = 7; packets.append(p)
        p = fixture(); del p["world_id"]; packets.append(p)
        for index, packet in enumerate(packets):
            with self.subTest(index=index):
                self.assertEqual(r8.evaluate_direct_positive_applicability(packet), r8._r7.evaluate_direct_positive_applicability(packet))

    def test_104_unrelated_error_after_successful_nested_snapshot_remains_visible(self):
        original = r8._r7.evaluate_direct_positive_applicability
        packet = fixture(); packet["opportunity"] = StableNestedMapping(packet["opportunity"])
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("r8-post-snapshot-programmer-error")
                r8._r7.evaluate_direct_positive_applicability = deliberate
                with self.assertRaisesRegex(exc_type, "r8-post-snapshot-programmer-error"):
                    r8.evaluate_direct_positive_applicability(packet)
        finally:
            r8._r7.evaluate_direct_positive_applicability = original

    def test_105_r8_revision_identity_is_exact(self):
        self.assertEqual(r8.R8_CANDIDATE_REVISION, "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R8")


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CourtR8)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({"court": "OBL059_R8_GOVERNED_BOUNDED_COURT", "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "successful": result.wasSuccessful(), "execution_scope": r8.SYNTHETIC_SCOPE, "project_current_state_created": False, "independent_review_performed": False}, sort_keys=True))
    raise SystemExit(0 if result.wasSuccessful() else 1)
