"""Governed producer court for OBL059 R13 canonical-input boundary."""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents if (parent / "rawlsing_next").is_dir())
R13_AUTHORITY = HERE / "positive_applicability_authority_r13.py"
R12_COURT = HERE.parent / "OBL059_POSITIVE_APPLICABILITY_R12" / "governed_bounded_court_r12.py"

spec = importlib.util.spec_from_file_location("_obl059_r13_authority", R13_AUTHORITY)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load R13 authority: {R13_AUTHORITY}")
r13 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r13)

court_spec = importlib.util.spec_from_file_location("_obl059_r12_court_for_r13", R12_COURT)
if court_spec is None or court_spec.loader is None:
    raise RuntimeError(f"cannot load R12 producer context: {R12_COURT}")
r12_court = importlib.util.module_from_spec(court_spec)
court_spec.loader.exec_module(r12_court)

EFFECT_KEYS = tuple(r12_court.EFFECT_KEYS)
NODES = (
    "opportunity",
    "evidence",
    "subject_classification",
    "actor_activation",
    "developmental_phase",
)


def fixture():
    return r12_court.fixture()


def get_node(packet, node):
    if node in ("opportunity", "evidence"):
        return packet[node]
    return packet["evidence"][node]


def mutate_node(packet, node):
    if node == "opportunity":
        packet["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:r13:wrong-world"
    elif node == "evidence":
        packet["evidence"]["actor_activation"] = None
    elif node == "subject_classification":
        packet["evidence"][node]["predicate"] = "WRONG_PREDICATE"
    elif node == "actor_activation":
        packet["evidence"][node]["semantic_owner"] = "WRONG_AUTHORITY"
    else:
        packet["evidence"][node]["phase"] = "V3DP_OTHER"


class LayeredSource(Mapping):
    def __init__(self, *layers):
        self.layers = [dict(layer) for layer in layers]
        self.keys_calls = 0
        self.getitem_calls = 0

    def keys(self):
        self.keys_calls += 1
        seen = []
        for layer in self.layers:
            for key in layer:
                if key not in seen:
                    seen.append(key)
        return seen

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.keys())

    def __getitem__(self, key):
        self.getitem_calls += 1
        for layer in self.layers:
            if key in layer:
                return layer[key]
        raise KeyError(key)


class CacheWarmingSource(LayeredSource):
    def __init__(self, *layers):
        super().__init__(*layers)
        self.cache = None

    def keys(self):
        if self.cache is None:
            self.cache = tuple(super().keys())
        return list(self.cache)


class DirectTrapMapping(Mapping):
    def __init__(self):
        self.calls = 0

    def _called(self):
        self.calls += 1
        raise RuntimeError("direct mapping must not be traversed")

    def keys(self):
        return self._called()

    def __iter__(self):
        return self._called()

    def __len__(self):
        return self._called()

    def __getitem__(self, key):
        return self._called()


class RepairNestedOnGetEvidence(Mapping):
    """R12 review family: nested value changes during parent path resolution."""
    def __init__(self, data):
        self.data = copy.deepcopy(data)
        self.getitem_calls = 0

    def keys(self):
        return list(self.data.keys())

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        self.getitem_calls += 1
        if key == "actor_activation":
            self.data[key]["semantic_owner"] = r13.ADP007_OWNER
        return self.data[key]


class CourtR13(unittest.TestCase):
    def assert_no_effect(self, result):
        for key in EFFECT_KEYS:
            self.assertFalse(result[key], key)

    def canonical(self, packet):
        value = r13.canonicalize_exact_packet(packet)
        self.assertIsNotNone(value)
        return value

    def assert_positive(self, canonical_packet):
        result = r13.evaluate_direct_positive_applicability(canonical_packet)
        self.assertEqual(result["decision"], r13.POSITIVE_DECISION, result)
        self.assert_no_effect(result)
        json.dumps(result, sort_keys=True)
        return result

    def assert_negative(self, canonical_packet, reason=None):
        try:
            result = r13.evaluate_direct_positive_applicability(canonical_packet)
        except Exception as exc:
            self.fail(f"R13 negative case raised {type(exc).__name__}: {exc}")
        self.assertEqual(result["decision"], r13.NEGATIVE_DECISION, result)
        if reason is not None:
            self.assertEqual(result["reason"], reason, result)
        self.assert_no_effect(result)
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64)
        return result

    def test_001_exact_canonical_positive_matches_exact_dict_core(self):
        packet = fixture()
        canonical = self.canonical(copy.deepcopy(packet))
        result = self.assert_positive(canonical)
        expected = r13._evaluate_prepared(copy.deepcopy(packet))
        self.assertEqual(result, expected)

    def test_002_exact_canonical_negative_controls_preserve_meaning(self):
        cases = []
        p = fixture(); p["execution_scope"] = "PROJECT_CURRENT"; cases.append(p)
        p = fixture(); p["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:r13:wrong"; cases.append(p)
        p = fixture(); p["evidence"]["subject_classification"]["predicate"] = "WRONG_PREDICATE"; cases.append(p)
        p = fixture(); p["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"; cases.append(p)
        p = fixture(); p["evidence"]["developmental_phase"]["stale"] = True; cases.append(p)
        for index, packet in enumerate(cases):
            with self.subTest(index=index):
                expected = r13._evaluate_prepared(copy.deepcopy(packet))
                result = self.assert_negative(self.canonical(packet))
                self.assertEqual(result, expected)

    def test_003_canonical_snapshot_is_independent_at_all_five_consumed_nodes(self):
        baseline = self.assert_positive(self.canonical(fixture()))
        for node in NODES:
            with self.subTest(node=node):
                source = fixture()
                canonical = self.canonical(source)
                mutate_node(source, node)
                self.assertEqual(r13.evaluate_direct_positive_applicability(canonical), baseline)

    def test_004_raw_exact_dict_is_not_direct_authority_input(self):
        self.assert_negative(fixture())

    def test_005_direct_custom_mapping_is_rejected_without_protocol_calls(self):
        trap = DirectTrapMapping()
        self.assert_negative(trap)
        self.assertEqual(trap.calls, 0)

    def test_006_direct_stable_cache_layered_and_aliasing_carriers_are_not_authority_inputs(self):
        raw = fixture()
        stable = LayeredSource(raw, {})
        cached = CacheWarmingSource(raw, {})
        for carrier in (stable, cached):
            with self.subTest(kind=type(carrier).__name__):
                before = (carrier.keys_calls, carrier.getitem_calls)
                self.assert_negative(carrier)
                self.assertEqual((carrier.keys_calls, carrier.getitem_calls), before)
        shared = LayeredSource(raw["evidence"]["actor_activation"], {})
        raw["evidence"]["actor_activation"] = shared
        raw["evidence"]["developmental_phase"] = shared
        self.assert_negative(raw)
        self.assertEqual(shared.keys_calls, 0)
        self.assertEqual(shared.getitem_calls, 0)

    def test_007_explicit_upstream_adapter_converts_lawful_layered_source(self):
        source = fixture()
        source["opportunity"] = CacheWarmingSource(source["opportunity"], {})
        source["evidence"]["actor_activation"] = LayeredSource({}, source["evidence"]["actor_activation"])
        outer = LayeredSource({}, source)
        canonical = r13.adapt_source_mapping_to_canonical(outer)
        self.assertIsNotNone(canonical)
        self.assert_positive(canonical)
        self.assertGreater(outer.keys_calls, 0)

    def test_008_adapter_output_wrong_scope_remains_negative(self):
        source = fixture()
        source["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:r13:adapter-wrong"
        canonical = r13.adapt_source_mapping_to_canonical(LayeredSource(source, {}))
        self.assertIsNotNone(canonical)
        self.assert_negative(canonical, "OPPORTUNITY_SCOPE_MISMATCH:world_id")

    def test_009_r12_nested_path_rewrite_cannot_affect_prebuilt_canonical_packet(self):
        source = fixture()
        source["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"
        canonical = self.canonical(copy.deepcopy(source))
        source["evidence"] = RepairNestedOnGetEvidence(source["evidence"])
        result = self.assert_negative(canonical, "ACTOR_ACTIVATION_WRONG_AUTHORITY")
        self.assertEqual(source["evidence"].getitem_calls, 0)
        self.assertEqual(result["decision"], r13.NEGATIVE_DECISION)

    def test_010_raw_packet_containing_r12_reproducer_is_rejected_without_nested_resolution(self):
        packet = fixture()
        packet["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"
        carrier = RepairNestedOnGetEvidence(packet["evidence"])
        packet["evidence"] = carrier
        self.assert_negative(packet)
        self.assertEqual(carrier.getitem_calls, 0)

    def test_011_malformed_and_noncanonical_forms_fail_deterministically(self):
        malformed = (
            None,
            (),
            ("WRONG_SCHEMA", ()),
            (r13.CANONICAL_SCHEMA, {}),
            (r13.CANONICAL_SCHEMA, ("D", (("opportunity", ("N",)),))),
            (r13.CANONICAL_SCHEMA, ("X",)),
        )
        baseline = None
        for index, value in enumerate(malformed):
            with self.subTest(index=index):
                result = self.assert_negative(value)
                if baseline is None:
                    baseline = result
                self.assertEqual(result, baseline)

    def test_012_adapter_cycle_or_unsupported_value_does_not_create_canonical_packet(self):
        cyc = fixture()
        cyc["cycle"] = cyc
        self.assertIsNone(r13.adapt_source_mapping_to_canonical(cyc))
        unsupported = fixture(); unsupported["unsupported"] = object()
        self.assertIsNone(r13.adapt_source_mapping_to_canonical(unsupported))

    def test_013_nested_oversized_integer_runtime_setting_remains_total(self):
        original = sys.get_int_max_str_digits()
        try:
            settings = (0, int(sys.int_info.str_digits_check_threshold))
            for setting in settings:
                sys.set_int_max_str_digits(setting)
                for value in (10 ** 5000, -(10 ** 5000), 10 ** 639, -(10 ** 639)):
                    with self.subTest(setting=setting, sign=value < 0, bits=value.bit_length()):
                        packet = fixture()
                        packet["evidence"]["actor_activation"]["actor_id"] = value
                        result = self.assert_negative(
                            self.canonical(packet),
                            "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id",
                        )
                        self.assertEqual(len(result["proof_sha256"]), 64)
        finally:
            sys.set_int_max_str_digits(original)

    def test_014_top_level_oversized_integer_remains_total_and_json_safe(self):
        original = sys.get_int_max_str_digits()
        try:
            for setting in (0, int(sys.int_info.str_digits_check_threshold)):
                sys.set_int_max_str_digits(setting)
                packet = fixture(); packet["actor_id"] = 10 ** 5000
                result = self.assert_negative(self.canonical(packet))
                json.dumps(result, sort_keys=True)
        finally:
            sys.set_int_max_str_digits(original)

    def test_015_proof_determinism_equality_and_distinction(self):
        p = fixture(); p["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_A"
        a1 = self.assert_negative(self.canonical(copy.deepcopy(p)))
        a2 = self.assert_negative(self.canonical(copy.deepcopy(p)))
        self.assertEqual(a1, a2)
        p["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_B"
        b = self.assert_negative(self.canonical(p))
        self.assertNotEqual(a1["proof_sha256"], b["proof_sha256"])

    def test_016_repeated_and_concurrent_canonical_evaluation_is_deterministic(self):
        canonical = self.canonical(fixture())
        baseline = r13.evaluate_direct_positive_applicability(canonical)
        for _ in range(5):
            self.assertEqual(r13.evaluate_direct_positive_applicability(canonical), baseline)
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(lambda _: r13.evaluate_direct_positive_applicability(canonical), range(16)))
        self.assertTrue(all(result == baseline for result in results))

    def test_017_canonical_tuple_contains_no_mapping_objects(self):
        canonical = self.canonical(fixture())
        def walk(value):
            self.assertIs(type(value), tuple)
            for item in tuple.__iter__(value):
                if type(item) is tuple:
                    walk(item)
                else:
                    self.assertNotIsInstance(item, Mapping)
        walk(canonical)

    def test_018_unrelated_programmer_errors_after_canonical_preparation_remain_visible(self):
        original = r13._evaluate_prepared
        canonical = self.canonical(fixture())
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("r13-post-canonical-programmer-error")
                r13._evaluate_prepared = deliberate
                with self.assertRaisesRegex(exc_type, "r13-post-canonical-programmer-error"):
                    r13.evaluate_direct_positive_applicability(canonical)
        finally:
            r13._evaluate_prepared = original

    def test_019_current_and_project_current_shapes_remain_rejected(self):
        for field, value in (
            ("execution_scope", "PROJECT_CURRENT"),
            ("execution_scope", "CURRENT"),
        ):
            packet = fixture(); packet[field] = value
            self.assert_negative(self.canonical(packet))

    def test_020_revision_identity_and_no_current_effects(self):
        self.assertEqual(
            r13.R13_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_CANONICAL_INPUT_BOUNDARY_R13",
        )
        result = self.assert_positive(self.canonical(fixture()))
        self.assertEqual(r13.CANONICAL_SCHEMA, "OBL059_CANONICAL_POSITIVE_APPLICABILITY_PACKET@R13")
        self.assert_no_effect(result)


if __name__ == "__main__":
    unittest.main()
