"""Governed producer court for OBL059 R10 coherent-entry-view repair."""
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
R10_AUTHORITY = HERE / "positive_applicability_authority_r10.py"
R9_WRAPPER = ROOT / "rawlsing_next/tests/test_subv_e_obl059_positive_applicability_r9_court.py"

r10_spec = importlib.util.spec_from_file_location("_obl059_r10_authority", R10_AUTHORITY)
if r10_spec is None or r10_spec.loader is None:
    raise RuntimeError(f"cannot load R10 authority: {R10_AUTHORITY}")
r10 = importlib.util.module_from_spec(r10_spec)
r10_spec.loader.exec_module(r10)

wrapper_spec = importlib.util.spec_from_file_location("_obl059_r9_corrected_wrapper_for_r10", R9_WRAPPER)
if wrapper_spec is None or wrapper_spec.loader is None:
    raise RuntimeError(f"cannot load corrected R9 wrapper: {R9_WRAPPER}")
r9_wrapper = importlib.util.module_from_spec(wrapper_spec)
r9_wrapper_spec_loader = wrapper_spec.loader
r9_wrapper_spec_loader.exec_module(r9_wrapper)

EFFECT_KEYS = tuple(r9_wrapper.module.EFFECT_KEYS)


def fixture():
    return r9_wrapper.module.fixture()


class MutableCarrier(Mapping):
    def __init__(self, data):
        self._data = dict(data)
        self.keys_calls = 0
        self.getitem_calls = 0

    def keys(self):
        self.keys_calls += 1
        return list(self._data.keys())

    def __getitem__(self, key):
        self.getitem_calls += 1
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def replace(self, key, value):
        self._data[key] = value


class SideEffectCarrier(MutableCarrier):
    def __init__(self, data, callback):
        super().__init__(data)
        self._callback = callback
        self._fired = False

    def keys(self):
        self.keys_calls += 1
        if not self._fired:
            self._fired = True
            self._callback()
        return list(self._data.keys())


class FailKeysCarrier(MutableCarrier):
    def keys(self):
        raise RuntimeError("r10-producer-keys-failure")


class FailGetitemCarrier(MutableCarrier):
    def __getitem__(self, key):
        raise RuntimeError("r10-producer-getitem-failure")


class OuterCarrier(MutableCarrier):
    pass


NODE_REASONS = {
    "opportunity": "OPPORTUNITY_BINDING_MISSING_OR_MALFORMED",
    "evidence": "ACTOR_ACTIVATION_EVIDENCE_MISSING",
    "subject_classification": "SUBJECT_CLASSIFICATION_PREDICATE_MISMATCH",
    "actor_activation": "ACTOR_ACTIVATION_WRONG_AUTHORITY",
    "developmental_phase": "DEVELOPMENTAL_PHASE_NOT_ACTIVE",
}

VALID_FIELDS = {
    "opportunity": ("world_id", None),
    "evidence": ("actor_activation", None),
    "subject_classification": ("predicate", None),
    "actor_activation": ("semantic_owner", None),
    "developmental_phase": ("phase", None),
}


def make_all_custom():
    p = fixture()
    opp = MutableCarrier(copy.deepcopy(p["opportunity"]))
    classification = MutableCarrier(copy.deepcopy(p["evidence"]["subject_classification"]))
    actor = MutableCarrier(copy.deepcopy(p["evidence"]["actor_activation"]))
    phase = MutableCarrier(copy.deepcopy(p["evidence"]["developmental_phase"]))
    evidence = MutableCarrier({
        "subject_classification": classification,
        "actor_activation": actor,
        "developmental_phase": phase,
    })
    p["opportunity"] = opp
    p["evidence"] = evidence
    return p, {
        "opportunity": opp,
        "evidence": evidence,
        "subject_classification": classification,
        "actor_activation": actor,
        "developmental_phase": phase,
    }


def make_invalid(target, carriers, packet):
    if target == "opportunity":
        carriers[target].replace("world_id", "urn:rawlsing:noncurrent-synthetic:wrong-world")
        return ("world_id", packet["world_id"]), "OPPORTUNITY_SCOPE_MISMATCH:world_id"
    if target == "evidence":
        valid = carriers["actor_activation"]
        carriers[target].replace("actor_activation", None)
        return ("actor_activation", valid), "ACTOR_ACTIVATION_EVIDENCE_MISSING"
    if target == "subject_classification":
        carriers[target].replace("predicate", "WRONG_PREDICATE")
        return ("predicate", r10.SUBJECT_CLASSIFICATION_PREDICATE), "SUBJECT_CLASSIFICATION_PREDICATE_MISMATCH"
    if target == "actor_activation":
        carriers[target].replace("semantic_owner", "WRONG_AUTHORITY")
        return ("semantic_owner", r10.ADP007_OWNER), "ACTOR_ACTIVATION_WRONG_AUTHORITY"
    carriers[target].replace("phase", "V3DP_OTHER")
    return ("phase", "V3DP_DEVELOPMENT_ACTIVE"), "DEVELOPMENTAL_PHASE_NOT_ACTIVE"


def install_side_effect(packet, carriers, node, callback):
    old = carriers[node]
    replacement = SideEffectCarrier(dict(old._data), callback)
    carriers[node] = replacement
    if node == "opportunity":
        packet["opportunity"] = replacement
    elif node == "evidence":
        packet["evidence"] = replacement
    else:
        carriers["evidence"]._data[node] = replacement
    return replacement


class CourtR10(r9_wrapper.TestOBL059R9BoundedRepair):
    def assert_no_effect(self, result):
        for key in EFFECT_KEYS:
            self.assertFalse(result[key], key)

    def assert_negative_r10(self, packet, reason=None):
        try:
            result = r10.evaluate_direct_positive_applicability(packet)
        except Exception as exc:
            self.fail(f"R10 negative case raised {type(exc).__name__}: {exc}")
        self.assertEqual(result["decision"], r10.NEGATIVE_DECISION, result)
        if reason is not None:
            self.assertEqual(result["reason"], reason, result)
        json.dumps(result, sort_keys=True)
        self.assertEqual(len(result["proof_sha256"]), 64)
        self.assert_no_effect(result)
        return result

    def test_119_exact_r9_f1_evidence_cannot_change_entry_opportunity(self):
        packet = fixture()
        wrong = copy.deepcopy(packet["opportunity"])
        wrong["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong-world"
        opportunity = MutableCarrier(wrong)
        packet["opportunity"] = opportunity
        evidence_data = copy.deepcopy(packet["evidence"])
        packet["evidence"] = SideEffectCarrier(
            evidence_data,
            lambda: opportunity.replace("world_id", packet["world_id"]),
        )
        self.assert_negative_r10(packet, "OPPORTUNITY_SCOPE_MISMATCH:world_id")

    def test_120_exact_r9_f2_opportunity_cannot_change_entry_actor(self):
        packet = fixture()
        actor_data = copy.deepcopy(packet["evidence"]["actor_activation"])
        actor_data["semantic_owner"] = "WRONG_AUTHORITY"
        actor = MutableCarrier(actor_data)
        packet["evidence"]["actor_activation"] = actor
        packet["opportunity"] = SideEffectCarrier(
            copy.deepcopy(packet["opportunity"]),
            lambda: actor.replace("semantic_owner", r10.ADP007_OWNER),
        )
        self.assert_negative_r10(packet, "ACTOR_ACTIVATION_WRONG_AUTHORITY")

    def test_121_exact_r9_f3_component_cannot_change_later_actor(self):
        packet = fixture()
        actor_data = copy.deepcopy(packet["evidence"]["actor_activation"])
        actor_data["semantic_owner"] = "WRONG_AUTHORITY"
        actor = MutableCarrier(actor_data)
        packet["evidence"]["actor_activation"] = actor
        packet["evidence"]["subject_classification"] = SideEffectCarrier(
            copy.deepcopy(packet["evidence"]["subject_classification"]),
            lambda: actor.replace("semantic_owner", r10.ADP007_OWNER),
        )
        self.assert_negative_r10(packet, "ACTOR_ACTIVATION_WRONG_AUTHORITY")

    def test_122_all_ordered_cross_carrier_negative_to_positive_mutations_use_entry_view(self):
        nodes = tuple(NODE_REASONS)
        for target in nodes:
            for mutator in nodes:
                if target == mutator:
                    continue
                with self.subTest(target=target, mutator=mutator):
                    packet, carriers = make_all_custom()
                    repair, expected = make_invalid(target, carriers, packet)
                    field, valid_value = repair
                    target_carrier = carriers[target]
                    install_side_effect(
                        packet,
                        carriers,
                        mutator,
                        lambda target_carrier=target_carrier, field=field, valid_value=valid_value: target_carrier.replace(field, valid_value),
                    )
                    self.assert_negative_r10(packet, expected)

    def test_123_positive_entry_view_is_not_changed_by_later_child_side_effect(self):
        nodes = ("opportunity", "subject_classification", "actor_activation", "developmental_phase")
        for target in nodes:
            for mutator in nodes:
                if target == mutator:
                    continue
                with self.subTest(target=target, mutator=mutator):
                    packet, carriers = make_all_custom()
                    target_carrier = carriers[target]
                    if target == "opportunity":
                        field, bad = "world_id", "urn:rawlsing:noncurrent-synthetic:wrong-world"
                    elif target == "subject_classification":
                        field, bad = "predicate", "WRONG_PREDICATE"
                    elif target == "actor_activation":
                        field, bad = "semantic_owner", "WRONG_AUTHORITY"
                    else:
                        field, bad = "phase", "V3DP_OTHER"
                    install_side_effect(
                        packet,
                        carriers,
                        mutator,
                        lambda target_carrier=target_carrier, field=field, bad=bad: target_carrier.replace(field, bad),
                    )
                    result = r10.evaluate_direct_positive_applicability(packet)
                    self.assertEqual(result["decision"], r10.POSITIVE_DECISION, result)
                    self.assert_no_effect(result)

    def test_124_negative_reason_is_derived_from_entry_view_not_child_timing(self):
        packet = fixture()
        actor_data = copy.deepcopy(packet["evidence"]["actor_activation"])
        actor_data["semantic_owner"] = "WRONG_AUTHORITY"
        actor = MutableCarrier(actor_data)
        packet["evidence"]["actor_activation"] = actor
        packet["opportunity"] = SideEffectCarrier(
            copy.deepcopy(packet["opportunity"]),
            lambda: (actor.replace("semantic_owner", r10.ADP007_OWNER), actor.replace("state", "INACTIVE")),
        )
        self.assert_negative_r10(packet, "ACTOR_ACTIVATION_WRONG_AUTHORITY")

    def test_125_outer_side_effect_cannot_change_nested_entry_view(self):
        packet = fixture()
        actor_data = copy.deepcopy(packet["evidence"]["actor_activation"])
        actor_data["semantic_owner"] = "WRONG_AUTHORITY"
        actor = MutableCarrier(actor_data)
        packet["evidence"]["actor_activation"] = actor
        outer = SideEffectCarrier(
            packet,
            lambda: actor.replace("semantic_owner", r10.ADP007_OWNER),
        )
        self.assert_negative_r10(outer, "ACTOR_ACTIVATION_WRONG_AUTHORITY")

    def test_126_shared_carrier_alias_is_validated_once_and_entry_semantics_preserved(self):
        packet = fixture()
        shared = MutableCarrier(copy.deepcopy(packet["evidence"]["actor_activation"]))
        packet["evidence"]["actor_activation"] = shared
        packet["evidence"]["developmental_phase"] = shared
        self.assert_negative_r10(packet)
        # Validation occurs in a child copy; parent-visible counters are intentionally unchanged.
        self.assertEqual(shared.keys_calls, 0)

    def test_127_stable_custom_mappings_all_consumed_nodes_equal_exact_dict(self):
        exact = fixture()
        packet = fixture()
        packet["opportunity"] = MutableCarrier(copy.deepcopy(packet["opportunity"]))
        classification = MutableCarrier(copy.deepcopy(packet["evidence"]["subject_classification"]))
        actor = MutableCarrier(copy.deepcopy(packet["evidence"]["actor_activation"]))
        phase = MutableCarrier(copy.deepcopy(packet["evidence"]["developmental_phase"]))
        packet["evidence"] = MutableCarrier({
            "subject_classification": classification,
            "actor_activation": actor,
            "developmental_phase": phase,
        })
        self.assertEqual(
            r10.evaluate_direct_positive_applicability(packet),
            r10.evaluate_direct_positive_applicability(exact),
        )

    def test_128_invoked_snapshot_failures_are_field_specific(self):
        cases = (
            ("opportunity", "OPPORTUNITY_BINDING_MISSING_OR_MALFORMED"),
            ("evidence", "EVIDENCE_MISSING_OR_MALFORMED"),
            ("subject_classification", "STRUCTURAL_CLASSIFICATION_EVIDENCE_MISSING"),
            ("actor_activation", "ACTOR_ACTIVATION_EVIDENCE_MISSING"),
            ("developmental_phase", "DEVELOPMENTAL_PHASE_EVIDENCE_MISSING"),
        )
        for node, reason in cases:
            for maker in (FailKeysCarrier, FailGetitemCarrier):
                with self.subTest(node=node, maker=maker.__name__):
                    packet = fixture()
                    if node == "opportunity":
                        packet[node] = maker(copy.deepcopy(packet[node]))
                    elif node == "evidence":
                        packet[node] = maker(copy.deepcopy(packet[node]))
                    else:
                        packet["evidence"][node] = maker(copy.deepcopy(packet["evidence"][node]))
                    self.assert_negative_r10(packet, reason)

    def test_129_nested_oversized_integer_repair_is_preserved(self):
        original_limit = sys.get_int_max_str_digits()
        try:
            baseline = None
            for setting in (0, int(sys.int_info.str_digits_check_threshold)):
                sys.set_int_max_str_digits(setting)
                packet = fixture()
                actor = copy.deepcopy(packet["evidence"]["actor_activation"])
                actor["actor_id"] = 10 ** 5000
                packet["evidence"]["actor_activation"] = MutableCarrier(actor)
                result = self.assert_negative_r10(packet, "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id")
                if baseline is None:
                    baseline = result
                else:
                    self.assertEqual(result, baseline)
        finally:
            sys.set_int_max_str_digits(original_limit)

    def test_130_exact_dict_positive_negative_and_scope_controls_equal_r9(self):
        cases = [fixture()]
        p = fixture(); p["execution_scope"] = "PROJECT_CURRENT"; cases.append(p)
        p = fixture(); p["opportunity"]["world_id"] = "urn:rawlsing:noncurrent-synthetic:wrong"; cases.append(p)
        p = fixture(); p["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"; cases.append(p)
        p = fixture(); p["evidence"]["developmental_phase"]["stale"] = True; cases.append(p)
        for index, packet in enumerate(cases):
            with self.subTest(index=index):
                self.assertEqual(
                    r10.evaluate_direct_positive_applicability(copy.deepcopy(packet)),
                    r10._r9.evaluate_direct_positive_applicability(copy.deepcopy(packet)),
                )

    def test_131_unrelated_error_after_successful_preparation_remains_visible(self):
        original = r10._r9._evaluate_prepared
        packet = fixture()
        packet["opportunity"] = MutableCarrier(copy.deepcopy(packet["opportunity"]))
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("r10-post-preparation-programmer-error")
                r10._r9._evaluate_prepared = deliberate
                with self.assertRaisesRegex(exc_type, "r10-post-preparation-programmer-error"):
                    r10.evaluate_direct_positive_applicability(packet)
        finally:
            r10._r9._evaluate_prepared = original

    def test_132_repeated_and_concurrent_exact_dict_evaluations_are_deterministic(self):
        expected = r10.evaluate_direct_positive_applicability(fixture())
        self.assertEqual(expected, r10.evaluate_direct_positive_applicability(fixture()))
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(lambda _: r10.evaluate_direct_positive_applicability(fixture()), range(12)))
        for result in results:
            self.assertEqual(result, expected)

    def test_133_r10_revision_identity_and_no_current_effect(self):
        self.assertEqual(
            r10.R10_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R10",
        )
        result = r10.evaluate_direct_positive_applicability(fixture())
        self.assertEqual(result["decision"], r10.POSITIVE_DECISION)
        self.assert_no_effect(result)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CourtR10)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({
        "court": "OBL059_R10_GOVERNED_BOUNDED_COURT",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "successful": result.wasSuccessful(),
        "execution_scope": r10.SYNTHETIC_SCOPE,
        "project_current_state_created": False,
        "self_review_performed": False,
        "independent_review_performed": False,
    }, sort_keys=True))
    raise SystemExit(0 if result.wasSuccessful() else 1)
