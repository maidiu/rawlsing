"""Governed producer court for OBL059 R12 observable semantic-view redesign."""
from __future__ import annotations

import copy
import importlib.util
from collections import ChainMap
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents if (parent / "rawlsing_next").is_dir())
R12_AUTHORITY = HERE / "positive_applicability_authority_r12.py"
R11_COURT = HERE.parent / "OBL059_POSITIVE_APPLICABILITY_R11" / "governed_bounded_court_r11.py"

r12_spec = importlib.util.spec_from_file_location("_obl059_r12_authority", R12_AUTHORITY)
if r12_spec is None or r12_spec.loader is None:
    raise RuntimeError(f"cannot load R12 authority: {R12_AUTHORITY}")
r12 = importlib.util.module_from_spec(r12_spec)
r12_spec.loader.exec_module(r12)

r11_court_spec = importlib.util.spec_from_file_location("_obl059_r11_court_for_r12", R11_COURT)
if r11_court_spec is None or r11_court_spec.loader is None:
    raise RuntimeError(f"cannot load R11 court: {R11_COURT}")
r11_court = importlib.util.module_from_spec(r11_court_spec)
r11_court_spec.loader.exec_module(r11_court)

# Route inherited public evaluation points through frozen R12.
r11_court.r11.evaluate_direct_positive_applicability = r12.evaluate_direct_positive_applicability
r11_court.r10_wrapper.module.r10.evaluate_direct_positive_applicability = r12.evaluate_direct_positive_applicability

EFFECT_KEYS = tuple(r11_court.EFFECT_KEYS)
NODES = tuple(r11_court.NODES)


def fixture():
    return r11_court.fixture()


def get_node(packet, node):
    return r11_court.get_node(packet, node)


def install_node(packet, node, value):
    r11_court.install_node(packet, node, value)


class CachingLayeredMapping(Mapping):
    """Stable layered Mapping whose first traversal only warms a private cache."""
    def __init__(self, *layers):
        self.layers = [dict(layer) for layer in layers]
        self._key_cache = None

    def _keys(self):
        if self._key_cache is None:
            seen = set()
            ordered = []
            for layer in self.layers:
                for key in layer:
                    if key not in seen:
                        seen.add(key)
                        ordered.append(key)
            self._key_cache = tuple(ordered)
        return self._key_cache

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


class LazyIndexMapping(Mapping):
    """Stable Mapping that lazily builds a private lookup index."""
    def __init__(self, items):
        self._items = list(items)
        self._index = None

    def _ensure(self):
        if self._index is None:
            self._index = {key: value for key, value in self._items}
        return self._index

    def keys(self):
        return list(self._ensure().keys())

    def __iter__(self):
        return iter(self._ensure())

    def __len__(self):
        return len(self._ensure())

    def __getitem__(self, key):
        return self._ensure()[key]


class MemoizedOrderMapping(Mapping):
    """Stable semantics with a lazily memoized, reversed key order."""
    def __init__(self, data):
        self._data = dict(data)
        self._memo = None

    def _order(self):
        if self._memo is None:
            self._memo = tuple(reversed(tuple(self._data.keys())))
        return self._memo

    def keys(self):
        return list(self._order())

    def __iter__(self):
        return iter(self._order())

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        return self._data[key]


class AlternatingOrderMapping(Mapping):
    """Iteration order changes, while observable key/value semantics stay equal."""
    def __init__(self, data):
        self._data = dict(data)
        self._flip = False

    def keys(self):
        self._flip = not self._flip
        keys = list(self._data.keys())
        return list(reversed(keys)) if self._flip else keys

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        return self._data[key]


class ObservableChangingMapping(Mapping):
    """Each materialization changes one observable field; must not be admitted."""
    def __init__(self, data, field, alternate):
        self._data = dict(data)
        self._field = field
        self._alternate = alternate
        self._original = self._data[field]
        self._flip = False

    def keys(self):
        self._flip = not self._flip
        self._data[self._field] = self._alternate if self._flip else self._original
        return list(self._data.keys())

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        return self._data[key]


class ThrowingKeysMapping(CachingLayeredMapping):
    def keys(self):
        raise RuntimeError("r12-producer-keys-failure")


class ThrowingGetitemMapping(CachingLayeredMapping):
    def __getitem__(self, key):
        raise RuntimeError("r12-producer-getitem-failure")


class CallbackCachingMapping(CachingLayeredMapping):
    def __init__(self, *layers, callback):
        super().__init__(*layers)
        self._callback = callback
        self._fired = False

    def keys(self):
        if not self._fired:
            self._fired = True
            self._callback()
        return super().keys()


class CourtR12(r11_court.CourtR11):
    def assert_no_effect_r12(self, result):
        for key in EFFECT_KEYS:
            self.assertFalse(result[key], key)

    def assert_negative_r12(self, packet, reason=None):
        try:
            result = r12.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(f"R12 negative case raised {type(exc).__name__}: {exc}")
        self.assertEqual(result["decision"], r12.NEGATIVE_DECISION, result)
        if reason is not None:
            self.assertEqual(result["reason"], reason, result)
        self.assertEqual(len(result["proof_sha256"]), 64)
        self.assert_no_effect_r12(result)
        return result

    def _split_layers(self, data):
        items = list(data.items())
        cut = max(1, len(items) // 2)
        return dict(items[:cut]), dict(items[cut:])

    def test_148_r11_cache_warming_reproduction_preserved_at_all_five_nodes(self):
        baseline = r12.evaluate_direct_positive_applicability(fixture())
        self.assertEqual(baseline["decision"], r12.POSITIVE_DECISION)
        for node in NODES:
            with self.subTest(node=node):
                packet = fixture()
                data = copy.deepcopy(get_node(packet, node))
                high, low = self._split_layers(data)
                carrier = CachingLayeredMapping(high, low)
                self.assertEqual(dict(carrier), data)
                carrier._key_cache = None
                install_node(packet, node, carrier)
                result = r12.evaluate_direct_positive_applicability(packet)
                self.assertEqual(result, baseline)
                self.assert_no_effect_r12(result)
                self.assertIsNone(carrier._key_cache)

    def test_149_multiple_lazy_implementations_preserve_exact_dict_semantics(self):
        baseline = r12.evaluate_direct_positive_applicability(fixture())
        factories = (
            lambda data: LazyIndexMapping(list(data.items())),
            lambda data: MemoizedOrderMapping(data),
            lambda data: AlternatingOrderMapping(data),
        )
        for factory_index, factory in enumerate(factories):
            for node in NODES:
                with self.subTest(factory=factory_index, node=node):
                    packet = fixture()
                    data = copy.deepcopy(get_node(packet, node))
                    carrier = factory(data)
                    install_node(packet, node, carrier)
                    self.assertEqual(r12.evaluate_direct_positive_applicability(packet), baseline)

    def test_150_general_layered_composition_precedence_shadowing_and_order(self):
        baseline = r12.evaluate_direct_positive_applicability(fixture())
        for node in NODES:
            with self.subTest(node=node):
                packet = fixture()
                data = copy.deepcopy(get_node(packet, node))
                high, low = self._split_layers(data)
                composed = CachingLayeredMapping(high, {}, low)
                install_node(packet, node, composed)
                self.assertEqual(r12.evaluate_direct_positive_applicability(packet), baseline)

        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        low = dict(actor); low["semantic_owner"] = "WRONG_AUTHORITY"
        packet["evidence"]["actor_activation"] = CachingLayeredMapping(
            {"semantic_owner": r12.ADP007_OWNER}, low
        )
        self.assertEqual(
            r12.evaluate_direct_positive_applicability(packet)["decision"],
            r12.POSITIVE_DECISION,
        )

    def test_151_cache_warming_outer_plus_nested_composition_preserves_positive(self):
        packet = fixture()
        actor_data = copy.deepcopy(packet["evidence"]["actor_activation"])
        ah, al = self._split_layers(actor_data)
        packet["evidence"]["actor_activation"] = LazyIndexMapping(list({**al, **ah}.items()))
        outer = CachingLayeredMapping(packet, {})
        result = r12.evaluate_direct_positive_applicability(outer)
        self.assertEqual(result["decision"], r12.POSITIVE_DECISION, result)
        self.assert_no_effect_r12(result)
        self.assertIsNone(outer._key_cache)

    def test_152_shared_aliases_preserve_semantics_without_parent_state_change(self):
        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        actor.update({
            "phase": packet["evidence"]["developmental_phase"]["phase"],
            "fresh_for_time_id": packet["evidence"]["developmental_phase"]["fresh_for_time_id"],
            "stale": False,
        })
        shared = CachingLayeredMapping(actor, {})
        packet["evidence"]["actor_activation"] = shared
        packet["evidence"]["developmental_phase"] = shared
        first = r12.evaluate_direct_positive_applicability(packet)
        second = r12.evaluate_direct_positive_applicability(packet)
        self.assertEqual(first, second)
        self.assertIsNone(shared._key_cache)
        self.assert_no_effect_r12(first)

    def test_153_cross_node_changes_in_both_directions_are_child_local(self):
        # opportunity observation attempts to change an initially invalid actor.
        packet = fixture()
        actor_data = copy.deepcopy(packet["evidence"]["actor_activation"])
        actor_data["semantic_owner"] = "WRONG_AUTHORITY"
        actor = r11_court.r10_wrapper.module.MutableCarrier(actor_data)
        packet["evidence"]["actor_activation"] = actor
        packet["opportunity"] = CallbackCachingMapping(
            copy.deepcopy(packet["opportunity"]), {},
            callback=lambda: actor.replace("semantic_owner", r12.ADP007_OWNER),
        )
        self.assert_negative_r12(packet, "ACTOR_ACTIVATION_WRONG_AUTHORITY")
        self.assertEqual(actor._data["semantic_owner"], "WRONG_AUTHORITY")

        # actor observation attempts to repair an initially invalid opportunity.
        packet = fixture()
        opportunity_data = copy.deepcopy(packet["opportunity"])
        opportunity_data["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-world"
        opportunity = r11_court.r10_wrapper.module.MutableCarrier(opportunity_data)
        packet["opportunity"] = opportunity
        actor_data = copy.deepcopy(packet["evidence"]["actor_activation"])
        packet["evidence"]["actor_activation"] = CallbackCachingMapping(
            actor_data, {},
            callback=lambda: opportunity.replace("world_id", packet["world_id"]),
        )
        self.assert_negative_r12(packet, "OPPORTUNITY_SCOPE_MISMATCH:world_id")
        self.assertEqual(opportunity._data["world_id"], "urn:rawlsing:noncurrent-synthetic:wrong-world")

    def test_154_parent_and_component_replacement_attempts_do_not_rewrite_entry_view(self):
        packet = fixture()
        original_actor = packet["evidence"]["actor_activation"]
        packet["opportunity"] = CallbackCachingMapping(
            copy.deepcopy(packet["opportunity"]), {},
            callback=lambda: packet["evidence"].__setitem__("actor_activation", None),
        )
        result = r12.evaluate_direct_positive_applicability(packet)
        self.assertEqual(result["decision"], r12.POSITIVE_DECISION, result)
        self.assertIs(packet["evidence"]["actor_activation"], original_actor)
        self.assert_no_effect_r12(result)

    def test_155_observable_disagreement_fails_closed_deterministically(self):
        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        packet["evidence"]["actor_activation"] = ObservableChangingMapping(
            actor, "semantic_owner", "WRONG_AUTHORITY"
        )
        first = self.assert_negative_r12(packet)
        second = self.assert_negative_r12(packet)
        self.assertEqual(first, second)

    def test_156_invoked_mapping_operation_failures_are_deterministic_negatives(self):
        for carrier_type in (ThrowingKeysMapping, ThrowingGetitemMapping):
            for node in NODES:
                with self.subTest(carrier=carrier_type.__name__, node=node):
                    packet = fixture()
                    data = copy.deepcopy(get_node(packet, node))
                    install_node(packet, node, carrier_type(data, {}))
                    first = self.assert_negative_r12(packet)
                    second = self.assert_negative_r12(packet)
                    self.assertEqual(first, second)

    def test_157_cycles_and_bounded_view_failure_are_deterministic(self):
        packet = fixture()
        data = copy.deepcopy(packet["opportunity"])
        cyc = CachingLayeredMapping(data, {})
        cyc.layers[0]["cycle"] = cyc
        packet["opportunity"] = cyc
        first = self.assert_negative_r12(packet)
        second = self.assert_negative_r12(packet)
        self.assertEqual(first, second)

    def test_158_chainmap_and_non_chainmap_controls_remain_equal(self):
        baseline = r12.evaluate_direct_positive_applicability(fixture())
        for node in NODES:
            packet = fixture()
            data = copy.deepcopy(get_node(packet, node))
            install_node(packet, node, ChainMap(data, {}))
            self.assertEqual(r12.evaluate_direct_positive_applicability(packet), baseline)

            packet = fixture()
            data = copy.deepcopy(get_node(packet, node))
            high, low = self._split_layers(data)
            install_node(packet, node, r11_court.LayeredMapping(high, low))
            self.assertEqual(r12.evaluate_direct_positive_applicability(packet), baseline)

    def test_159_oversized_integer_runtime_setting_repair_remains_closed(self):
        # Inherited R11 test covers 10**5000 under both supported settings.
        self.test_143_composed_nested_oversized_integer_preserves_runtime_setting_totality()

    def test_160_repeated_and_concurrent_cache_mapping_evaluation_is_stable(self):
        baseline = r12.evaluate_direct_positive_applicability(fixture())
        packet = fixture()
        data = copy.deepcopy(packet["opportunity"])
        high, low = self._split_layers(data)
        carrier = CachingLayeredMapping(high, low)
        packet["opportunity"] = carrier

        for _ in range(3):
            self.assertEqual(r12.evaluate_direct_positive_applicability(packet), baseline)
        self.assertIsNone(carrier._key_cache)

        def one(_):
            return r12.evaluate_direct_positive_applicability(packet)

        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(one, range(8)))
        self.assertTrue(all(result == baseline for result in results))
        self.assertIsNone(carrier._key_cache)

    def test_161_unrelated_errors_after_observable_preparation_remain_visible(self):
        original = r12._r11._r10._r9._evaluate_prepared
        packet = fixture()
        packet["opportunity"] = CachingLayeredMapping(copy.deepcopy(packet["opportunity"]), {})
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("r12-post-view-programmer-error")
                r12._r11._r10._r9._evaluate_prepared = deliberate
                with self.assertRaisesRegex(exc_type, "r12-post-view-programmer-error"):
                    r12.evaluate_direct_positive_applicability(packet)
        finally:
            r12._r11._r10._r9._evaluate_prepared = original

    def test_162_revision_identity_is_exact_and_no_effects_remain(self):
        self.assertEqual(
            r12.R12_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_SEMANTIC_VIEW_REDESIGN_R12",
        )
        result = r12.evaluate_direct_positive_applicability(fixture())
        self.assertEqual(result["decision"], r12.POSITIVE_DECISION)
        self.assert_no_effect_r12(result)
