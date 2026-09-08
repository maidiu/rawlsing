"""Independent R11 review court for OBL059 positive applicability."""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from collections import ChainMap
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents if (parent / "rawlsing_next").is_dir())
R11_AUTHORITY = HERE / "positive_applicability_authority_r11.py"
PRODUCER_COURT = HERE / "governed_bounded_court_r11.py"

r11_spec = importlib.util.spec_from_file_location("_obl059_r11_independent_target", R11_AUTHORITY)
if r11_spec is None or r11_spec.loader is None:
    raise RuntimeError(f"cannot load R11 target: {R11_AUTHORITY}")
r11 = importlib.util.module_from_spec(r11_spec)
r11_spec.loader.exec_module(r11)

producer_spec = importlib.util.spec_from_file_location("_obl059_r11_producer_context", PRODUCER_COURT)
if producer_spec is None or producer_spec.loader is None:
    raise RuntimeError(f"cannot load R11 producer context: {PRODUCER_COURT}")
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


class TupleLayeredMapping(Mapping):
    """Stable composed Mapping whose view is not stored in one dict."""
    def __init__(self, *layers, reverse_order=False):
        self.layers = tuple(dict(layer) for layer in layers)
        self.reverse_order = bool(reverse_order)

    def __getitem__(self, key):
        for layer in self.layers:
            if key in layer:
                return layer[key]
        raise KeyError(key)

    def __iter__(self):
        seen = set()
        keys = []
        for layer in self.layers:
            for key in layer:
                if key not in seen:
                    seen.add(key)
                    keys.append(key)
        if self.reverse_order:
            keys.reverse()
        return iter(keys)

    def __len__(self):
        return sum(1 for _ in self.__iter__())


class CachingLayeredMapping(Mapping):
    """Observable view is stable; first traversal only warms a private key cache."""
    def __init__(self, *layers):
        self.layers = tuple(dict(layer) for layer in layers)
        self._key_cache = None

    def _keys(self):
        if self._key_cache is None:
            seen = set()
            keys = []
            for layer in self.layers:
                for key in layer:
                    if key not in seen:
                        seen.add(key)
                        keys.append(key)
            self._key_cache = tuple(keys)
        return self._key_cache

    def __getitem__(self, key):
        for layer in self.layers:
            if key in layer:
                return layer[key]
        raise KeyError(key)

    def __iter__(self):
        return iter(self._keys())

    def __len__(self):
        return len(self._keys())


class TombstoneOverlay(Mapping):
    """Stable layered Mapping with explicit hidden keys."""
    def __init__(self, primary, fallback, tombstones=()):
        self.layers = (dict(primary), dict(fallback))
        self.tombstones = set(tombstones)

    def __getitem__(self, key):
        if key in self.tombstones:
            raise KeyError(key)
        for layer in self.layers:
            if key in layer:
                return layer[key]
        raise KeyError(key)

    def __iter__(self):
        seen = set()
        keys = []
        for layer in self.layers:
            for key in layer:
                if key not in seen and key not in self.tombstones:
                    seen.add(key)
                    keys.append(key)
        keys.reverse()  # unusual but lawful stable ordering
        return iter(keys)

    def __len__(self):
        return sum(1 for _ in self.__iter__())


class CrossChangingMapping(TupleLayeredMapping):
    def __init__(self, target, field, value, *layers):
        super().__init__(*layers)
        self.target = target
        self.field = field
        self.value = value
        self.done = False

    def __iter__(self):
        if not self.done:
            self.done = True
            self.target[self.field] = self.value
        return super().__iter__()


class ChangingObservableMapping(TupleLayeredMapping):
    def __init__(self, *layers):
        super().__init__(*layers)
        self.flip = False

    def __getitem__(self, key):
        value = super().__getitem__(key)
        if key == "semantic_owner":
            self.flip = not self.flip
            return value if self.flip else "CHANGED_AUTHORITY"
        return value


class RaiseKeysMapping(TupleLayeredMapping):
    def keys(self):
        raise RuntimeError("r11-independent-keys-failure")


class CourtR11Independent(unittest.TestCase):
    def assert_no_effect(self, result):
        for key in EFFECT_KEYS:
            self.assertFalse(result[key], key)

    def assert_positive(self, packet):
        result = r11.evaluate_direct_positive_applicability(packet)
        self.assertEqual(result["decision"], r11.POSITIVE_DECISION, result)
        self.assert_no_effect(result)
        json.dumps(result, sort_keys=True)
        return result

    def assert_negative(self, packet, reason=None):
        try:
            result = r11.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(f"negative review case raised {type(exc).__name__}: {exc}")
        self.assertEqual(result["decision"], r11.NEGATIVE_DECISION, result)
        if reason is not None:
            self.assertEqual(result["reason"], reason, result)
        self.assert_no_effect(result)
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64)
        return result

    def test_001_chainmap_positive_all_five_nodes(self):
        exact = fixture()
        baseline = r11.evaluate_direct_positive_applicability(copy.deepcopy(exact))
        for node in NODES:
            with self.subTest(node=node):
                packet = fixture()
                data = copy.deepcopy(get_node(packet, node))
                keys = list(data)
                cut = max(1, len(keys) // 2)
                first = {key: data[key] for key in keys[:cut]}
                second = {key: data[key] for key in keys[cut:]}
                composed = ChainMap(first, {}, second)
                install_node(packet, node, composed)
                self.assertEqual(r11.evaluate_direct_positive_applicability(packet), baseline)

    def test_002_chainmap_shadowing_precedence_matches_exact_dict(self):
        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        lower = dict(actor)
        lower["semantic_owner"] = "LOWER_WRONG_AUTHORITY"
        upper = {"semantic_owner": actor["semantic_owner"]}
        packet["evidence"]["actor_activation"] = ChainMap(upper, lower)
        self.assert_positive(packet)

    def test_003_two_non_chainmap_composed_implementations_preserve_positive(self):
        baseline = r11.evaluate_direct_positive_applicability(fixture())
        for maker in (
            lambda data: TupleLayeredMapping({}, data, reverse_order=True),
            lambda data: TombstoneOverlay({}, data, tombstones=("unused-review-key",)),
        ):
            for node in NODES:
                with self.subTest(maker=maker.__name__ if hasattr(maker, "__name__") else "maker", node=node):
                    packet = fixture()
                    install_node(packet, node, maker(copy.deepcopy(get_node(packet, node))))
                    self.assertEqual(r11.evaluate_direct_positive_applicability(packet), baseline)

    def test_004_stable_cache_warming_composed_mapping_must_preserve_positive(self):
        """Private cache warming is not an observable Mapping-content change."""
        baseline = r11.evaluate_direct_positive_applicability(fixture())
        for node in NODES:
            with self.subTest(node=node):
                packet = fixture()
                data = copy.deepcopy(get_node(packet, node))
                keys = list(data)
                cut = max(1, len(keys) // 2)
                carrier = CachingLayeredMapping(
                    {key: data[key] for key in keys[:cut]},
                    {key: data[key] for key in keys[cut:]},
                )
                # Establish that observable semantics really are exact-dict-equivalent.
                self.assertEqual(dict(carrier), data)
                carrier._key_cache = None
                install_node(packet, node, carrier)
                self.assertEqual(r11.evaluate_direct_positive_applicability(packet), baseline)

    def test_005_tombstone_observable_negative_matches_exact_control(self):
        exact = fixture()
        exact_actor = copy.deepcopy(exact["evidence"]["actor_activation"])
        del exact_actor["semantic_owner"]
        exact["evidence"]["actor_activation"] = exact_actor
        expected = r11.evaluate_direct_positive_applicability(exact)

        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        packet["evidence"]["actor_activation"] = TombstoneOverlay(actor, {}, tombstones=("semantic_owner",))
        self.assertEqual(r11.evaluate_direct_positive_applicability(packet), expected)

    def test_006_outer_and_nested_composed_positive(self):
        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        packet["evidence"]["actor_activation"] = TupleLayeredMapping({}, actor)
        evidence = copy.deepcopy(packet["evidence"])
        evidence["actor_activation"] = packet["evidence"]["actor_activation"]
        packet["evidence"] = ChainMap({}, evidence)
        outer = TupleLayeredMapping({}, packet)
        self.assert_positive(outer)

    def test_007_shared_alias_is_deterministic_and_never_escapes(self):
        packet = fixture()
        shared = TupleLayeredMapping({}, copy.deepcopy(packet["evidence"]["actor_activation"]))
        packet["evidence"]["actor_activation"] = shared
        packet["evidence"]["developmental_phase"] = shared
        first = self.assert_negative(packet)
        second = self.assert_negative(packet)
        self.assertEqual(first, second)

    def test_008_cross_node_change_during_materialization_cannot_make_positive(self):
        packet = fixture()
        actor = packet["evidence"]["actor_activation"]
        actor["semantic_owner"] = "WRONG_AUTHORITY"
        opp = copy.deepcopy(packet["opportunity"])
        packet["opportunity"] = CrossChangingMapping(
            actor,
            "semantic_owner",
            r11.ADP007_OWNER,
            {},
            opp,
        )
        self.assert_negative(packet)
        self.assertEqual(actor["semantic_owner"], "WRONG_AUTHORITY")

    def test_009_observable_change_between_materializations_fails_closed(self):
        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        packet["evidence"]["actor_activation"] = ChangingObservableMapping({}, actor)
        self.assert_negative(packet)

    def test_010_invoked_mapping_exception_is_field_specific_negative(self):
        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        packet["evidence"]["actor_activation"] = RaiseKeysMapping({}, actor)
        self.assert_negative(packet, "ACTOR_ACTIVATION_EVIDENCE_MISSING")

    def test_011_initial_negative_chainmap_shadow_cannot_become_positive(self):
        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        upper = {"semantic_owner": "WRONG_AUTHORITY"}
        packet["evidence"]["actor_activation"] = ChainMap(upper, actor)
        self.assert_negative(packet, "ACTOR_ACTIVATION_WRONG_AUTHORITY")

    def test_012_oversized_integer_runtime_setting_totality_is_preserved(self):
        original = sys.get_int_max_str_digits()
        try:
            baseline = None
            settings = (0, int(sys.int_info.str_digits_check_threshold))
            for setting in settings:
                sys.set_int_max_str_digits(setting)
                for value in (10 ** 5000, -(10 ** 5000)):
                    packet = fixture()
                    actor = copy.deepcopy(packet["evidence"]["actor_activation"])
                    actor["actor_id"] = value
                    packet["evidence"]["actor_activation"] = TupleLayeredMapping({}, actor)
                    result = self.assert_negative(packet, "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id")
                    if baseline is None and value > 0:
                        baseline = result
                    if value > 0:
                        self.assertEqual(result, baseline)
        finally:
            sys.set_int_max_str_digits(original)

    def test_013_proof_determinism_and_distinction(self):
        packet = fixture()
        packet["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY_A"
        a1 = self.assert_negative(copy.deepcopy(packet))
        a2 = self.assert_negative(copy.deepcopy(packet))
        self.assertEqual(a1, a2)
        packet["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY_B"
        b = self.assert_negative(packet)
        self.assertNotEqual(a1["proof_sha256"], b["proof_sha256"])

    def test_014_exact_dict_controls_and_current_rejection_match_r10(self):
        cases = [fixture()]
        p = fixture(); p["execution_scope"] = "PROJECT_CURRENT"; cases.append(p)
        p = fixture(); p["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong"; cases.append(p)
        p = fixture(); p["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"; cases.append(p)
        p = fixture(); p["evidence"]["developmental_phase"]["stale"] = True; cases.append(p)
        for index, packet in enumerate(cases):
            with self.subTest(index=index):
                self.assertEqual(
                    r11.evaluate_direct_positive_applicability(copy.deepcopy(packet)),
                    r11._r10.evaluate_direct_positive_applicability(copy.deepcopy(packet)),
                )

    def test_015_repeated_and_concurrent_exact_dict_evaluation_is_deterministic(self):
        packet = fixture()
        baseline = r11.evaluate_direct_positive_applicability(copy.deepcopy(packet))
        for _ in range(5):
            self.assertEqual(r11.evaluate_direct_positive_applicability(copy.deepcopy(packet)), baseline)
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(lambda _: r11.evaluate_direct_positive_applicability(copy.deepcopy(packet)), range(12)))
        self.assertTrue(all(result == baseline for result in results))

    def test_016_unrelated_error_after_successful_preparation_remains_visible(self):
        original = r11._r10._r9._evaluate_prepared
        packet = fixture()
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("r11-independent-post-preparation-error")
                r11._r10._r9._evaluate_prepared = deliberate
                with self.assertRaisesRegex(exc_type, "r11-independent-post-preparation-error"):
                    r11.evaluate_direct_positive_applicability(copy.deepcopy(packet))
        finally:
            r11._r10._r9._evaluate_prepared = original

    def test_017_revision_identity_and_no_current_effects(self):
        self.assertEqual(r11.R11_CANDIDATE_REVISION, "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R11")
        result = self.assert_positive(fixture())
        for key in EFFECT_KEYS:
            self.assertFalse(result[key])


if __name__ == "__main__":
    unittest.main()
