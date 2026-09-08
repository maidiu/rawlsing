"""Governed producer court for OBL059 R11 composed Mapping preservation."""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from collections import ChainMap
from collections.abc import Mapping
from pathlib import Path
from types import MappingProxyType

HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents if (parent / "rawlsing_next").is_dir())
R11_AUTHORITY = HERE / "positive_applicability_authority_r11.py"
R10_WRAPPER = ROOT / "rawlsing_next/tests/test_subv_e_obl059_positive_applicability_r10_court.py"

r11_spec = importlib.util.spec_from_file_location("_obl059_r11_authority", R11_AUTHORITY)
if r11_spec is None or r11_spec.loader is None:
    raise RuntimeError(f"cannot load R11 authority: {R11_AUTHORITY}")
r11 = importlib.util.module_from_spec(r11_spec)
r11_spec.loader.exec_module(r11)

wrapper_spec = importlib.util.spec_from_file_location("_obl059_r10_wrapper_for_r11", R10_WRAPPER)
if wrapper_spec is None or wrapper_spec.loader is None:
    raise RuntimeError(f"cannot load R10 wrapper: {R10_WRAPPER}")
r10_wrapper = importlib.util.module_from_spec(wrapper_spec)
wrapper_spec.loader.exec_module(r10_wrapper)

# Route R10-specific inherited public evaluation points through frozen R11.
r10_wrapper.module.r10.evaluate_direct_positive_applicability = r11.evaluate_direct_positive_applicability

EFFECT_KEYS = tuple(r10_wrapper.module.EFFECT_KEYS)
NODES = (
    "opportunity",
    "evidence",
    "subject_classification",
    "actor_activation",
    "developmental_phase",
)


def fixture():
    return r10_wrapper.module.fixture()


def get_node(packet, node):
    if node in ("opportunity", "evidence"):
        return packet[node]
    return packet["evidence"][node]


def install_node(packet, node, value):
    if node in ("opportunity", "evidence"):
        packet[node] = value
    else:
        packet["evidence"][node] = value


class LayeredMapping(Mapping):
    """Generic stable composed Mapping with first-layer precedence."""
    def __init__(self, *layers):
        self.layers = [dict(layer) for layer in layers]

    def __getitem__(self, key):
        for layer in self.layers:
            if key in layer:
                return layer[key]
        raise KeyError(key)

    def __iter__(self):
        seen = set()
        for layer in self.layers:
            for key in layer:
                if key not in seen:
                    seen.add(key)
                    yield key

    def __len__(self):
        return len(set().union(*(set(layer) for layer in self.layers)))


class ThrowingLayered(LayeredMapping):
    def keys(self):
        raise RuntimeError("r11-producer-keys-failure")


class MutatingLayered(LayeredMapping):
    def __init__(self, *layers, field, value):
        super().__init__(*layers)
        self.field = field
        self.value = value
        self.fired = False

    def keys(self):
        if not self.fired:
            self.fired = True
            self.layers[0][self.field] = self.value
        return super().keys()


class CallbackLayered(LayeredMapping):
    def __init__(self, *layers, callback):
        super().__init__(*layers)
        self.callback = callback
        self.fired = False

    def keys(self):
        if not self.fired:
            self.fired = True
            self.callback()
        return super().keys()


class CourtR11(r10_wrapper.TestOBL059R10BoundedRepair):
    def assert_no_effect_r11(self, result):
        for key in EFFECT_KEYS:
            self.assertFalse(result[key], key)

    def assert_negative_r11(self, packet, reason=None):
        try:
            result = r11.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(f"R11 negative case raised {type(exc).__name__}: {exc}")
        self.assertEqual(result["decision"], r11.NEGATIVE_DECISION, result)
        if reason is not None:
            self.assertEqual(result["reason"], reason, result)
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64)
        self.assert_no_effect_r11(result)
        return result

    def test_134_chainmap_exact_dict_equivalence_at_all_consumed_nodes(self):
        baseline = r11.evaluate_direct_positive_applicability(fixture())
        self.assertEqual(baseline["decision"], r11.POSITIVE_DECISION)
        for node in NODES:
            with self.subTest(node=node):
                packet = fixture()
                data = copy.deepcopy(get_node(packet, node))
                install_node(packet, node, ChainMap(data, {}))
                result = r11.evaluate_direct_positive_applicability(packet)
                self.assertEqual(result, baseline)
                self.assert_no_effect_r11(result)

    def test_135_multilayer_composition_distribution_precedence_and_shadowing(self):
        # Keys distributed across multiple layers preserve observable Mapping meaning.
        for node in ("opportunity", "actor_activation", "developmental_phase"):
            with self.subTest(node=node, mode="distributed"):
                packet = fixture()
                data = copy.deepcopy(get_node(packet, node))
                items = list(data.items())
                high = dict(items[::2])
                low = dict(items[1::2])
                composed = ChainMap(high, {}, low)
                exact_packet = fixture()
                install_node(exact_packet, node, dict(composed))
                install_node(packet, node, composed)
                self.assertEqual(
                    r11.evaluate_direct_positive_applicability(packet),
                    r11.evaluate_direct_positive_applicability(exact_packet),
                )

        # First layer shadows lower layers exactly as Mapping semantics specify.
        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        low = dict(actor); low["semantic_owner"] = "WRONG_AUTHORITY"
        high = {"semantic_owner": r11.ADP007_OWNER}
        composed = ChainMap(high, low)
        packet["evidence"]["actor_activation"] = composed
        self.assertEqual(
            r11.evaluate_direct_positive_applicability(packet)["decision"],
            r11.POSITIVE_DECISION,
        )

        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        high = {"semantic_owner": "WRONG_AUTHORITY"}
        composed = ChainMap(high, actor)
        packet["evidence"]["actor_activation"] = composed
        exact = fixture(); exact["evidence"]["actor_activation"] = dict(composed)
        self.assertEqual(
            r11.evaluate_direct_positive_applicability(packet),
            r11.evaluate_direct_positive_applicability(exact),
        )

    def test_136_generic_layered_mapping_not_type_special_cased(self):
        baseline = r11.evaluate_direct_positive_applicability(fixture())
        for node in NODES:
            with self.subTest(node=node):
                packet = fixture()
                data = copy.deepcopy(get_node(packet, node))
                items = list(data.items())
                composed = LayeredMapping(dict(items[::2]), {}, dict(items[1::2]))
                install_node(packet, node, composed)
                self.assertEqual(r11.evaluate_direct_positive_applicability(packet), baseline)

    def test_137_read_only_proxy_mapping_preserves_exact_dict_meaning(self):
        baseline = r11.evaluate_direct_positive_applicability(fixture())
        for node in NODES:
            with self.subTest(node=node):
                packet = fixture()
                data = copy.deepcopy(get_node(packet, node))
                install_node(packet, node, MappingProxyType(data))
                self.assertEqual(r11.evaluate_direct_positive_applicability(packet), baseline)

    def test_138_throwing_or_self_changing_composed_carrier_fails_closed(self):
        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        packet["evidence"]["actor_activation"] = ThrowingLayered(actor, {})
        first = self.assert_negative_r11(packet)
        second = self.assert_negative_r11(packet)
        self.assertEqual(first, second)

        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        packet["evidence"]["actor_activation"] = MutatingLayered(
            actor, {}, field="semantic_owner", value="WRONG_AUTHORITY"
        )
        self.assert_negative_r11(packet)

    def test_139_cross_node_change_from_composed_validation_cannot_rewrite_entry_view(self):
        packet = fixture()
        actor_data = copy.deepcopy(packet["evidence"]["actor_activation"])
        actor_data["semantic_owner"] = "WRONG_AUTHORITY"
        actor = r10_wrapper.module.MutableCarrier(actor_data)
        packet["evidence"]["actor_activation"] = actor
        packet["opportunity"] = CallbackLayered(
            copy.deepcopy(packet["opportunity"]),
            {},
            callback=lambda: actor.replace("semantic_owner", r11.ADP007_OWNER),
        )
        self.assert_negative_r11(packet)
        self.assertEqual(actor._data["semantic_owner"], "WRONG_AUTHORITY")

    def test_140_parent_slot_change_from_composed_validation_is_child_local_and_negative(self):
        packet = fixture()
        original_actor = packet["evidence"]["actor_activation"]
        composed = CallbackLayered(
            copy.deepcopy(packet["opportunity"]),
            {},
            callback=lambda: packet["evidence"].__setitem__("actor_activation", None),
        )
        packet["opportunity"] = composed
        result = self.assert_negative_r11(packet)
        self.assertIs(packet["evidence"]["actor_activation"], original_actor)
        self.assert_no_effect_r11(result)

    def test_141_outer_composed_plus_nested_composed_positive(self):
        packet = fixture()
        actor = copy.deepcopy(packet["evidence"]["actor_activation"])
        packet["evidence"]["actor_activation"] = ChainMap({"semantic_owner": actor["semantic_owner"]}, actor)
        outer = LayeredMapping(packet, {})
        result = r11.evaluate_direct_positive_applicability(outer)
        self.assertEqual(result["decision"], r11.POSITIVE_DECISION, result)
        self.assert_no_effect_r11(result)

    def test_142_shared_composed_alias_and_cycles_are_deterministic(self):
        shared_data = {
            "actor_id": fixture()["actor_id"],
            "world_id": fixture()["world_id"],
            "time_id": fixture()["time_id"],
            "semantic_owner": r11.ADP007_OWNER,
            "state": "ACTIVE",
            "phase": "V3DP_DEVELOPMENT_ACTIVE",
            "fresh_for_time_id": fixture()["time_id"],
            "stale": False,
        }
        shared = LayeredMapping(shared_data, {})
        packet = fixture()
        packet["evidence"]["actor_activation"] = shared
        packet["evidence"]["developmental_phase"] = shared
        first = self.assert_negative_r11(packet)
        second = self.assert_negative_r11(packet)
        self.assertEqual(first, second)

        packet = fixture()
        data = copy.deepcopy(packet["opportunity"])
        cyc = LayeredMapping(data, {})
        cyc.layers[0]["cycle"] = cyc
        packet["opportunity"] = cyc
        a = self.assert_negative_r11(packet)
        b = self.assert_negative_r11(packet)
        self.assertEqual(a, b)

    def test_143_composed_nested_oversized_integer_preserves_runtime_setting_totality(self):
        original_limit = sys.get_int_max_str_digits()
        try:
            baseline = None
            for setting in (0, int(sys.int_info.str_digits_check_threshold)):
                sys.set_int_max_str_digits(setting)
                packet = fixture()
                actor = copy.deepcopy(packet["evidence"]["actor_activation"])
                actor["actor_id"] = 10 ** 5000
                packet["evidence"]["actor_activation"] = ChainMap(actor, {})
                result = self.assert_negative_r11(packet, "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id")
                if baseline is None:
                    baseline = result
                else:
                    self.assertEqual(result, baseline)
        finally:
            sys.set_int_max_str_digits(original_limit)

    def test_144_exact_dict_controls_remain_exactly_r10(self):
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

    def test_145_unrelated_errors_after_composed_view_established_remain_visible(self):
        original = r11._r10._r9._evaluate_prepared
        packet = fixture()
        packet["opportunity"] = ChainMap(copy.deepcopy(packet["opportunity"]), {})
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("r11-post-view-programmer-error")
                r11._r10._r9._evaluate_prepared = deliberate
                with self.assertRaisesRegex(exc_type, "r11-post-view-programmer-error"):
                    r11.evaluate_direct_positive_applicability(packet)
        finally:
            r11._r10._r9._evaluate_prepared = original

    def test_146_repeated_composed_positive_is_deterministic(self):
        packet = fixture()
        packet["opportunity"] = ChainMap(copy.deepcopy(packet["opportunity"]), {})
        first = r11.evaluate_direct_positive_applicability(packet)
        self.assertEqual(first["decision"], r11.POSITIVE_DECISION)
        for _ in range(5):
            self.assertEqual(r11.evaluate_direct_positive_applicability(packet), first)

    def test_147_revision_identity_is_exact(self):
        self.assertEqual(
            r11.R11_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R11",
        )
