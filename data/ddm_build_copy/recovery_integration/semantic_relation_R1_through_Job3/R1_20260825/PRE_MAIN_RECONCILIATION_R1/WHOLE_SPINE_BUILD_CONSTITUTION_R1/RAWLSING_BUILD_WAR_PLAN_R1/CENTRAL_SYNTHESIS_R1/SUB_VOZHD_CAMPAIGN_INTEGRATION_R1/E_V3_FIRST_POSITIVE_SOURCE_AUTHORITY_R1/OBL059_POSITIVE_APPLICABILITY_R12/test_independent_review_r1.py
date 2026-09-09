"""Fresh distinct independent review court for frozen OBL059 R12."""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
import time
import unittest
from collections import ChainMap
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import MappingProxyType

HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents if (parent / "rawlsing_next").is_dir())
R12_AUTHORITY = HERE / "positive_applicability_authority_r12.py"
PRODUCER_COURT = HERE / "governed_bounded_court_r12.py"

r12_spec = importlib.util.spec_from_file_location("_obl059_r12_independent_target", R12_AUTHORITY)
if r12_spec is None or r12_spec.loader is None:
    raise RuntimeError(f"cannot load frozen R12 target: {R12_AUTHORITY}")
r12 = importlib.util.module_from_spec(r12_spec)
r12_spec.loader.exec_module(r12)

producer_spec = importlib.util.spec_from_file_location("_obl059_r12_producer_context_for_review", PRODUCER_COURT)
if producer_spec is None or producer_spec.loader is None:
    raise RuntimeError(f"cannot load R12 producer context: {PRODUCER_COURT}")
producer = importlib.util.module_from_spec(producer_spec)
producer_spec.loader.exec_module(producer)

EFFECT_KEYS = tuple(producer.EFFECT_KEYS)
NODES = (
    "opportunity",
    "evidence",
    "subject_classification",
    "actor_activation",
    "developmental_phase",
)


def fixture():
    return producer.fixture()


def get_node(packet, node):
    if node in ("opportunity", "evidence"):
        return packet[node]
    return packet["evidence"][node]


def install_node(packet, node, value):
    if node in ("opportunity", "evidence"):
        packet[node] = value
    else:
        packet["evidence"][node] = value


class LayeredView(Mapping):
    """Generic composed Mapping with first-layer precedence."""
    def __init__(self, *layers, reverse=False):
        self.layers = tuple(dict(layer) for layer in layers)
        self.reverse = bool(reverse)

    def _keys(self):
        seen = set()
        out = []
        for layer in self.layers:
            for key in layer:
                if key not in seen:
                    seen.add(key)
                    out.append(key)
        if self.reverse:
            out.reverse()
        return out

    def keys(self):
        return list(self._keys())

    def __iter__(self):
        return iter(self._keys())

    def __len__(self):
        return len(self._keys())

    def __getitem__(self, key):
        for layer in self.layers:
            if key in layer:
                return layer[key]
        raise KeyError(key)


class CacheWarmMapping(LayeredView):
    """First observation builds a private key cache only."""
    def __init__(self, *layers):
        super().__init__(*layers)
        self._cache = None

    def _keys(self):
        if self._cache is None:
            self._cache = tuple(super()._keys())
        return list(self._cache)


class MemoValueMapping(LayeredView):
    """Value memoization changes private state only."""
    def __init__(self, *layers):
        super().__init__(*layers)
        self._memo = {}

    def __getitem__(self, key):
        if key not in self._memo:
            self._memo[key] = super().__getitem__(key)
        return self._memo[key]


class LazyIndexMapping(Mapping):
    """Lazily creates a private lookup index from stable items."""
    def __init__(self, data):
        self._items = tuple(data.items())
        self._index = None

    def _ensure(self):
        if self._index is None:
            self._index = dict(self._items)
        return self._index

    def keys(self):
        return list(self._ensure().keys())

    def __iter__(self):
        return iter(self._ensure())

    def __len__(self):
        return len(self._ensure())

    def __getitem__(self, key):
        return self._ensure()[key]


class AccessCounterMapping(LayeredView):
    """Observation increments private counters but never changes contents."""
    def __init__(self, *layers):
        super().__init__(*layers)
        self.keys_calls = 0
        self.getitem_calls = 0

    def keys(self):
        self.keys_calls += 1
        return super().keys()

    def __getitem__(self, key):
        self.getitem_calls += 1
        return super().__getitem__(key)


class AlternatingOrderStableMapping(LayeredView):
    """Key order alternates while normalized key/value semantics stay equal."""
    def __init__(self, *layers):
        super().__init__(*layers)
        self._flip = False

    def keys(self):
        self._flip = not self._flip
        keys = super()._keys()
        return list(reversed(keys)) if self._flip else keys

    def __iter__(self):
        return iter(self.keys())


class TombstoneView(LayeredView):
    """Stable composed view with explicitly hidden keys."""
    def __init__(self, primary, fallback, tombstones=()):
        super().__init__(primary, fallback, reverse=True)
        self.tombstones = frozenset(tombstones)

    def _keys(self):
        return [key for key in super()._keys() if key not in self.tombstones]

    def __getitem__(self, key):
        if key in self.tombstones:
            raise KeyError(key)
        return super().__getitem__(key)


class ChangingValueMapping(LayeredView):
    """One contract-relevant value alternates between observations."""
    def __init__(self, data, field, alternate):
        super().__init__(data)
        self.field = field
        self.alternate = alternate
        self.original = data[field]
        self.flip = False

    def __getitem__(self, key):
        value = super().__getitem__(key)
        if key == self.field:
            self.flip = not self.flip
            return self.alternate if self.flip else self.original
        return value


class ChangingKeysMapping(LayeredView):
    """The observable key set alternates between observations."""
    def __init__(self, data, omitted_key):
        super().__init__(data)
        self.omitted_key = omitted_key
        self.flip = False

    def keys(self):
        self.flip = not self.flip
        keys = super()._keys()
        if self.flip:
            return [key for key in keys if key != self.omitted_key]
        return keys

    def __iter__(self):
        return iter(self.keys())


class CrossChangeMapping(LayeredView):
    """Observation tries to change a separately consumed parent object."""
    def __init__(self, target, field, value, *layers):
        super().__init__(*layers)
        self.target = target
        self.field = field
        self.value = value
        self.done = False

    def keys(self):
        if not self.done:
            self.done = True
            self.target[self.field] = self.value
        return super().keys()


class RepairNestedOnGetEvidence(Mapping):
    """Custom evidence parent changes nested actor only while resolving that path."""
    def __init__(self, evidence, correct_owner):
        self._data = copy.deepcopy(evidence)
        self.correct_owner = correct_owner

    def keys(self):
        return list(self._data.keys())

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        if key == "actor_activation":
            self._data["actor_activation"]["semantic_owner"] = self.correct_owner
        return self._data[key]


class RepairNestedOnGetOuter(Mapping):
    """Custom outer parent changes nested actor while resolving evidence."""
    def __init__(self, packet, correct_owner):
        self._data = copy.deepcopy(packet)
        self.correct_owner = correct_owner

    def keys(self):
        return list(self._data.keys())

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        if key == "evidence":
            self._data["evidence"]["actor_activation"]["semantic_owner"] = self.correct_owner
        return self._data[key]


class ThrowKeysMapping(LayeredView):
    def keys(self):
        raise RuntimeError("r12-independent-keys-failure")


class ThrowGetitemMapping(LayeredView):
    def __getitem__(self, key):
        raise RuntimeError("r12-independent-getitem-failure")


class SlowKeysMapping(LayeredView):
    def keys(self):
        time.sleep(2.25)
        return super().keys()


class CourtR12Independent(unittest.TestCase):
    def assert_no_effect(self, result):
        for key in EFFECT_KEYS:
            self.assertFalse(result[key], key)

    def assert_positive(self, packet):
        result = r12.evaluate_direct_positive_applicability(packet)
        self.assertEqual(result["decision"], r12.POSITIVE_DECISION, result)
        self.assert_no_effect(result)
        json.dumps(result, sort_keys=True)
        return result

    def assert_negative(self, packet, reason=None):
        try:
            result = r12.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(f"R12 review negative case raised {type(exc).__name__}: {exc}")
        self.assertEqual(result["decision"], r12.NEGATIVE_DECISION, result)
        if reason is not None:
            self.assertEqual(result["reason"], reason, result)
        self.assert_no_effect(result)
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64)
        return result

    def _layers(self, data):
        items = list(data.items())
        cut = max(1, len(items) // 2)
        return dict(items[:cut]), dict(items[cut:])

    def test_001_r11_cache_warming_reproducer_all_five_nodes(self):
        baseline = self.assert_positive(fixture())
        for node in NODES:
            with self.subTest(node=node):
                packet = fixture()
                data = copy.deepcopy(get_node(packet, node))
                high, low = self._layers(data)
                carrier = CacheWarmMapping(high, low)
                install_node(packet, node, carrier)
                self.assertEqual(r12.evaluate_direct_positive_applicability(packet), baseline)
                self.assertIsNone(carrier._cache)

    def test_002_unrelated_private_only_changes_preserve_semantics(self):
        baseline = self.assert_positive(fixture())
        factories = (
            lambda data: MemoValueMapping({}, data),
            lambda data: LazyIndexMapping(data),
            lambda data: AccessCounterMapping({}, data),
        )
        for index, factory in enumerate(factories):
            for node in NODES:
                with self.subTest(factory=index, node=node):
                    packet = fixture()
                    carrier = factory(copy.deepcopy(get_node(packet, node)))
                    install_node(packet, node, carrier)
                    self.assertEqual(r12.evaluate_direct_positive_applicability(packet), baseline)
                    if isinstance(carrier, AccessCounterMapping):
                        self.assertEqual((carrier.keys_calls, carrier.getitem_calls), (0, 0))

    def test_003_order_variation_is_normalized_not_semantic(self):
        baseline = self.assert_positive(fixture())
        for node in NODES:
            with self.subTest(node=node):
                packet = fixture()
                data = copy.deepcopy(get_node(packet, node))
                carrier = AlternatingOrderStableMapping({}, data)
                install_node(packet, node, carrier)
                self.assertEqual(r12.evaluate_direct_positive_applicability(packet), baseline)
                self.assertFalse(carrier._flip)

    def test_004_general_composition_precedence_proxy_and_tombstone(self):
        baseline = self.assert_positive(fixture())
        makers = (
            lambda data: ChainMap({}, data),
            lambda data: LayeredView({}, data, reverse=True),
            lambda data: LayeredView({}, MappingProxyType(data)),
        )
        for maker_index, maker in enumerate(makers):
            for node in NODES:
                with self.subTest(maker=maker_index, node=node):
                    packet = fixture()
                    install_node(packet, node, maker(copy.deepcopy(get_node(packet, node))))
                    self.assertEqual(r12.evaluate_direct_positive_applicability(packet), baseline)

        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        lower = dict(actor)
        lower["semantic_owner"] = "LOWER_WRONG_AUTHORITY"
        packet["evidence"]["actor_activation"] = LayeredView(
            {"semantic_owner": r12.ADP007_OWNER}, lower
        )
        self.assert_positive(packet)

        exact = fixture()
        exact_actor = copy.deepcopy(exact["evidence"]["actor_activation"])
        del exact_actor["semantic_owner"]
        exact["evidence"]["actor_activation"] = exact_actor
        expected = r12.evaluate_direct_positive_applicability(exact)
        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        packet["evidence"]["actor_activation"] = TombstoneView(actor, {}, ("semantic_owner",))
        self.assertEqual(r12.evaluate_direct_positive_applicability(packet), expected)

    def test_005_outer_nested_and_exact_custom_composition(self):
        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        packet["evidence"]["actor_activation"] = CacheWarmMapping({}, actor)
        packet["evidence"] = LayeredView({}, packet["evidence"])
        outer = CacheWarmMapping({}, packet)
        self.assert_positive(outer)
        self.assertIsNone(outer._cache)

    def test_006_aliases_and_shared_backing_are_deterministic(self):
        packet = fixture()
        shared_data = copy.deepcopy(packet["evidence"]["actor_activation"])
        shared_data.update({
            "phase": packet["evidence"]["developmental_phase"]["phase"],
            "fresh_for_time_id": packet["evidence"]["developmental_phase"]["fresh_for_time_id"],
            "stale": False,
        })
        shared = CacheWarmMapping({}, shared_data)
        packet["evidence"]["actor_activation"] = shared
        packet["evidence"]["developmental_phase"] = shared
        first = r12.evaluate_direct_positive_applicability(packet)
        second = r12.evaluate_direct_positive_applicability(packet)
        self.assertEqual(first, second)
        self.assert_no_effect(first)
        self.assertIsNone(shared._cache)

    def test_007_actual_observable_value_or_key_disagreement_fails_closed(self):
        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        packet["evidence"]["actor_activation"] = ChangingValueMapping(
            actor, "semantic_owner", "CHANGED_AUTHORITY"
        )
        a = self.assert_negative(packet)
        b = self.assert_negative(packet)
        self.assertEqual(a, b)

        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        packet["evidence"]["actor_activation"] = ChangingKeysMapping(actor, "semantic_owner")
        a = self.assert_negative(packet)
        b = self.assert_negative(packet)
        self.assertEqual(a, b)

    def test_008_cross_carrier_changes_both_directions_stay_child_local(self):
        packet = fixture()
        actor = packet["evidence"]["actor_activation"]
        actor["semantic_owner"] = "WRONG_AUTHORITY"
        packet["opportunity"] = CrossChangeMapping(
            actor, "semantic_owner", r12.ADP007_OWNER, {}, copy.deepcopy(packet["opportunity"])
        )
        self.assert_negative(packet, "ACTOR_ACTIVATION_WRONG_AUTHORITY")
        self.assertEqual(actor["semantic_owner"], "WRONG_AUTHORITY")

        packet = fixture()
        opportunity = packet["opportunity"]
        opportunity["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-world"
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        packet["evidence"]["actor_activation"] = CrossChangeMapping(
            opportunity, "world_id", packet["world_id"], {}, actor
        )
        self.assert_negative(packet, "OPPORTUNITY_SCOPE_MISMATCH:world_id")
        self.assertEqual(opportunity["world_id"], "urn:rawlsing:noncurrent-synthetic:wrong-world")

    def test_009_parent_path_resolution_cannot_rewrite_initial_negative_entry_view(self):
        # Evidence is the custom parent actually traversed to resolve actor_activation.
        packet = fixture()
        evidence = copy.deepcopy(packet["evidence"])
        evidence["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"
        carrier = RepairNestedOnGetEvidence(evidence, r12.ADP007_OWNER)
        packet["evidence"] = carrier
        result = self.assert_negative(packet, "ACTOR_ACTIVATION_WRONG_AUTHORITY")
        self.assertEqual(carrier._data["actor_activation"]["semantic_owner"], "WRONG_AUTHORITY")
        self.assert_no_effect(result)

        # Outer custom parent is traversed on every nested evidence path.
        packet = fixture()
        packet["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"
        outer = RepairNestedOnGetOuter(packet, r12.ADP007_OWNER)
        result = self.assert_negative(outer, "ACTOR_ACTIVATION_WRONG_AUTHORITY")
        self.assertEqual(
            outer._data["evidence"]["actor_activation"]["semantic_owner"],
            "WRONG_AUTHORITY",
        )
        self.assert_no_effect(result)

    def test_010_cycles_depth_breadth_timeout_and_protocol_failures_are_negative(self):
        cases = []

        packet = fixture()
        cyc = LayeredView({}, copy.deepcopy(packet["opportunity"]))
        cyc.layers[0]["cycle"] = cyc
        packet["opportunity"] = cyc
        cases.append(packet)

        packet = fixture()
        deep = {}
        cursor = deep
        for _ in range(140):
            child = {}
            cursor["x"] = child
            cursor = child
        data = copy.deepcopy(packet["opportunity"])
        data["deep"] = deep
        packet["opportunity"] = LayeredView({}, data)
        cases.append(packet)

        packet = fixture()
        wide = copy.deepcopy(packet["opportunity"])
        for index in range(16400):
            wide[f"extra_{index}"] = index
        packet["opportunity"] = LayeredView({}, wide)
        cases.append(packet)

        packet = fixture()
        packet["opportunity"] = SlowKeysMapping({}, copy.deepcopy(packet["opportunity"]))
        cases.append(packet)

        packet = fixture()
        packet["evidence"]["actor_activation"] = ThrowKeysMapping({}, copy.deepcopy(packet["evidence"]["actor_activation"]))
        cases.append(packet)

        packet = fixture()
        packet["evidence"]["actor_activation"] = ThrowGetitemMapping({}, copy.deepcopy(packet["evidence"]["actor_activation"]))
        cases.append(packet)

        for index, packet in enumerate(cases):
            with self.subTest(case=index):
                self.assert_negative(packet)

    def test_011_exact_dict_controls_remain_inherited_equivalent(self):
        cases = [fixture()]
        p = fixture(); p["execution_scope"] = "PROJECT_CURRENT"; cases.append(p)
        p = fixture(); p["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong"; cases.append(p)
        p = fixture(); p["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"; cases.append(p)
        p = fixture(); p["evidence"]["developmental_phase"]["stale"] = True; cases.append(p)
        for index, packet in enumerate(cases):
            with self.subTest(index=index):
                self.assertEqual(
                    r12.evaluate_direct_positive_applicability(copy.deepcopy(packet)),
                    r12._r11.evaluate_direct_positive_applicability(copy.deepcopy(packet)),
                )

    def test_012_initial_negative_custom_cases_remain_negative(self):
        variants = []
        p = fixture(); p["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"; variants.append((p, "actor_activation"))
        p = fixture(); p["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong"; variants.append((p, "opportunity"))
        p = fixture(); p["evidence"]["developmental_phase"]["stale"] = True; variants.append((p, "developmental_phase"))
        p = fixture(); p["evidence"]["subject_classification"]["predicate"] = "WRONG_PREDICATE"; variants.append((p, "subject_classification"))
        for index, (packet, node) in enumerate(variants):
            with self.subTest(index=index, node=node):
                data = copy.deepcopy(get_node(packet, node))
                install_node(packet, node, CacheWarmMapping({}, data))
                self.assert_negative(packet)

    def test_013_oversized_integer_runtime_setting_totality_and_neighbors(self):
        original = sys.get_int_max_str_digits()
        try:
            threshold = int(sys.int_info.str_digits_check_threshold)
            values = (10 ** 5000, -(10 ** 5000), 10 ** (threshold - 1), 10 ** threshold)
            for value_index, value in enumerate(values):
                baseline = None
                for setting in (0, threshold):
                    sys.set_int_max_str_digits(setting)
                    packet = fixture()
                    actor = copy.deepcopy(packet["evidence"]["actor_activation"])
                    actor["actor_id"] = value
                    packet["evidence"]["actor_activation"] = CacheWarmMapping({}, actor)
                    result = self.assert_negative(packet, "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id")
                    if baseline is None:
                        baseline = result
                    else:
                        self.assertEqual(result, baseline, (value_index, setting))
        finally:
            sys.set_int_max_str_digits(original)

    def test_014_proof_determinism_equality_and_distinction(self):
        packet = fixture()
        packet["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY_A"
        a1 = self.assert_negative(copy.deepcopy(packet))
        a2 = self.assert_negative(copy.deepcopy(packet))
        self.assertEqual(a1, a2)
        packet["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY_B"
        b = self.assert_negative(packet)
        self.assertNotEqual(a1["proof_sha256"], b["proof_sha256"])

    def test_015_repeated_and_concurrent_custom_evaluation_is_deterministic(self):
        baseline = self.assert_positive(fixture())
        packet = fixture()
        carrier = AccessCounterMapping({}, copy.deepcopy(packet["opportunity"]))
        packet["opportunity"] = carrier
        for _ in range(3):
            self.assertEqual(r12.evaluate_direct_positive_applicability(packet), baseline)
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(lambda _: r12.evaluate_direct_positive_applicability(packet), range(8)))
        self.assertTrue(all(result == baseline for result in results))
        self.assertEqual((carrier.keys_calls, carrier.getitem_calls), (0, 0))

    def test_016_malformed_inputs_are_deterministic_negatives(self):
        for value in (None, [], object(), "not-a-packet"):
            with self.subTest(type=type(value).__name__):
                first = r12.evaluate_direct_positive_applicability(value)
                second = r12.evaluate_direct_positive_applicability(value)
                self.assertEqual(first, second)
                self.assertEqual(first["decision"], r12.NEGATIVE_DECISION)
                self.assert_no_effect(first)

    def test_017_noncurrent_positive_and_project_current_rejection(self):
        positive = self.assert_positive(fixture())
        self.assertEqual(positive["execution_scope"], r12.SYNTHETIC_SCOPE)
        packet = fixture()
        packet["execution_scope"] = "PROJECT_CURRENT"
        packet["opportunity"] = CacheWarmMapping({}, copy.deepcopy(packet["opportunity"]))
        self.assert_negative(packet)

    def test_018_unrelated_errors_after_successful_semantic_preparation_remain_visible(self):
        original = r12._r11._r10._r9._evaluate_prepared
        packet = fixture()
        packet["opportunity"] = CacheWarmMapping({}, copy.deepcopy(packet["opportunity"]))
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("r12-independent-post-preparation-error")
                r12._r11._r10._r9._evaluate_prepared = deliberate
                with self.assertRaisesRegex(exc_type, "r12-independent-post-preparation-error"):
                    r12.evaluate_direct_positive_applicability(packet)
        finally:
            r12._r11._r10._r9._evaluate_prepared = original

    def test_019_revision_identity_and_no_current_effects(self):
        self.assertEqual(
            r12.R12_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_SEMANTIC_VIEW_REDESIGN_R12",
        )
        result = self.assert_positive(fixture())
        for key in EFFECT_KEYS:
            self.assertFalse(result[key])


if __name__ == "__main__":
    unittest.main()
