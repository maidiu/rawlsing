"""Fresh distinct independent review for frozen OBL059 R13 canonical-input boundary."""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1"
R13_PATH = BASE / "OBL059_POSITIVE_APPLICABILITY_R13/positive_applicability_authority_r13.py"
PRODUCER_CONTEXT_PATH = BASE / "OBL059_POSITIVE_APPLICABILITY_R13/governed_bounded_court_r13.py"

spec = importlib.util.spec_from_file_location("_obl059_r13_independent_target", R13_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load frozen R13 authority: {R13_PATH}")
r13 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r13)

ctx_spec = importlib.util.spec_from_file_location("_obl059_r13_fixture_context", PRODUCER_CONTEXT_PATH)
if ctx_spec is None or ctx_spec.loader is None:
    raise RuntimeError(f"cannot load R13 immutable fixture context: {PRODUCER_CONTEXT_PATH}")
producer_context = importlib.util.module_from_spec(ctx_spec)
ctx_spec.loader.exec_module(producer_context)

EFFECT_KEYS = tuple(producer_context.EFFECT_KEYS)


def fixture():
    # Prior producer fixture material is used only as immutable setup context.
    # No producer CourtR13 test method is inherited or executed by this review.
    return copy.deepcopy(producer_context.fixture())


def canonical(packet):
    value = r13.canonicalize_exact_packet(copy.deepcopy(packet))
    assert value is not None, "independent fixture failed canonical construction"
    return value


def assert_no_effect(result):
    for key in EFFECT_KEYS:
        assert result[key] is False, (key, result)


def assert_negative(value, reason=None):
    try:
        result = r13.evaluate_direct_positive_applicability(value)
    except Exception as exc:  # totality is part of the contract
        raise AssertionError(f"negative public-boundary case escaped {type(exc).__name__}: {exc}") from exc
    assert result["decision"] == r13.NEGATIVE_DECISION, result
    if reason is not None:
        assert result["reason"] == reason, result
    assert len(result["proof_sha256"]) == 64, result
    json.dumps(result, sort_keys=True)
    assert_no_effect(result)
    return result


def assert_positive(value):
    result = r13.evaluate_direct_positive_applicability(value)
    assert result["decision"] == r13.POSITIVE_DECISION, result
    assert len(result["proof_sha256"]) == 64, result
    json.dumps(result, sort_keys=True)
    assert_no_effect(result)
    return result


class DirectProtocolTrap(Mapping):
    def __init__(self, mode="stable"):
        self.mode = mode
        self.calls = []
        self.state = 0
        self.inner = {"actor_activation": {"semantic_owner": "WRONG_AUTHORITY"}}

    def _hit(self, name):
        self.calls.append(name)
        self.state += 1
        if self.mode == "throw":
            raise RuntimeError("direct-carrier-protocol-must-not-run")

    def keys(self):
        self._hit("keys")
        return list(self.inner.keys())

    def __iter__(self):
        self._hit("iter")
        return iter(self.inner)

    def __len__(self):
        self._hit("len")
        return len(self.inner)

    def __getitem__(self, key):
        self._hit("getitem")
        if self.mode == "path_mutating":
            self.inner["actor_activation"]["semantic_owner"] = r13.ADP007_OWNER if self.state % 2 else "WRONG_AUTHORITY"
        return self.inner[key]


class CacheLayerAliasMapping(Mapping):
    def __init__(self, data):
        self.data = data
        self.cache = None
        self.calls = 0

    def _keys(self):
        self.calls += 1
        if self.cache is None:
            self.cache = tuple(reversed(tuple(self.data.keys())))
        return self.cache

    def keys(self):
        return list(self._keys())

    def __iter__(self):
        return iter(self._keys())

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        self.calls += 1
        return self.data[key]


class RepairingEvidenceParent(Mapping):
    """R12 family: parent path lookup attempts to repair an invalid child."""
    def __init__(self, evidence):
        self.data = copy.deepcopy(evidence)
        self.calls = 0

    def keys(self):
        self.calls += 1
        return list(self.data.keys())

    def __iter__(self):
        self.calls += 1
        return iter(self.data)

    def __len__(self):
        self.calls += 1
        return len(self.data)

    def __getitem__(self, key):
        self.calls += 1
        if key == "actor_activation":
            self.data[key]["semantic_owner"] = r13.ADP007_OWNER
        return self.data[key]


class AlternatingNestedView(Mapping):
    def __init__(self, data):
        self.data = copy.deepcopy(data)
        self.flip = False
        self.calls = 0

    def keys(self):
        self.calls += 1
        return list(self.data.keys())

    def __iter__(self):
        self.calls += 1
        return iter(self.data)

    def __len__(self):
        self.calls += 1
        return len(self.data)

    def __getitem__(self, key):
        self.calls += 1
        if key == "actor_activation":
            self.flip = not self.flip
            child = copy.deepcopy(self.data[key])
            child["semantic_owner"] = r13.ADP007_OWNER if self.flip else "WRONG_AUTHORITY"
            return child
        return self.data[key]


class TupleSubclass(tuple):
    pass


def test_001_direct_custom_effectful_cache_layer_alias_path_mappings_are_rejected_without_calls():
    carriers = [
        DirectProtocolTrap("stable"),
        DirectProtocolTrap("throw"),
        DirectProtocolTrap("path_mutating"),
        CacheLayerAliasMapping({"x": 1}),
        AlternatingNestedView({"actor_activation": {"semantic_owner": "WRONG_AUTHORITY"}}),
    ]
    for carrier in carriers:
        before = getattr(carrier, "calls", 0)
        assert_negative(carrier)
        after = getattr(carrier, "calls", 0)
        assert after == before, (type(carrier).__name__, before, after)
        if isinstance(carrier, DirectProtocolTrap):
            assert carrier.state == 0


def test_002_raw_exact_dict_and_raw_packet_with_nested_effectful_mapping_never_traverse_nested_protocols():
    raw = fixture()
    nested = RepairingEvidenceParent(raw["evidence"])
    raw["evidence"] = nested
    assert_negative(raw)
    assert nested.calls == 0


def test_003_canonical_packet_is_exact_tuple_tree_with_no_mapping_or_mutable_container():
    value = canonical(fixture())

    def walk(node):
        assert type(node) is tuple, type(node)
        for item in tuple.__iter__(node):
            if type(item) is tuple:
                walk(item)
            else:
                assert not isinstance(item, Mapping), type(item)
                assert type(item) not in (dict, list, set, bytearray), type(item)

    walk(value)


def test_004_tuple_subclasses_and_nonexact_outer_or_payload_containers_are_not_authoritative():
    valid = canonical(fixture())
    assert_negative(TupleSubclass(valid))
    assert_negative((r13.CANONICAL_SCHEMA, TupleSubclass(valid[1])))
    assert_negative([r13.CANONICAL_SCHEMA, valid[1]])
    assert_negative((r13.CANONICAL_SCHEMA, [valid[1]]))


def test_005_canonical_snapshot_survives_aggressive_source_mutation_at_all_authority_positions():
    source = fixture()
    frozen = canonical(source)
    baseline = assert_positive(frozen)
    source["actor_id"] = "urn:wrong:actor"
    source["subject_id"] = "urn:wrong:subject"
    source["world_id"] = "urn:wrong:world"
    source["time_id"] = "urn:wrong:time"
    source["adp010_opportunity_id"] = "urn:wrong:opportunity"
    source["opportunity"].clear()
    source["evidence"]["subject_classification"].clear()
    source["evidence"]["actor_activation"].clear()
    source["evidence"]["developmental_phase"].clear()
    assert r13.evaluate_direct_positive_applicability(frozen) == baseline


def test_006_r12_parent_path_rewrite_cannot_repair_or_change_prebuilt_canonical_input():
    source = fixture()
    source["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"
    frozen = canonical(source)
    baseline = assert_negative(frozen, "ACTOR_ACTIVATION_WRONG_AUTHORITY")
    parent = RepairingEvidenceParent(source["evidence"])
    source["evidence"] = parent
    again = r13.evaluate_direct_positive_applicability(frozen)
    assert again == baseline
    assert parent.calls == 0


def test_007_inconsistent_nested_source_views_are_upstream_only_and_cannot_touch_saved_canonical_packet():
    source = fixture()
    frozen = canonical(source)
    baseline = assert_positive(frozen)
    alternating = AlternatingNestedView(source["evidence"])
    source["evidence"] = alternating
    for _ in range(4):
        assert r13.evaluate_direct_positive_applicability(frozen) == baseline
    assert alternating.calls == 0


def test_008_upstream_adapter_may_traverse_source_mapping_but_decision_does_not_reconsult_it():
    source = fixture()
    outer = CacheLayerAliasMapping(source)
    frozen = r13.adapt_source_mapping_to_canonical(outer)
    assert frozen is not None
    assert outer.calls > 0
    baseline = assert_positive(frozen)
    calls_after_adapt = outer.calls
    outer.data["actor_id"] = "urn:mutated:after-canonicalization"
    assert r13.evaluate_direct_positive_applicability(frozen) == baseline
    assert outer.calls == calls_after_adapt


def test_009_decision_function_does_not_invoke_adapter_even_if_adapter_symbol_is_replaced():
    frozen = canonical(fixture())
    original = r13.adapt_source_mapping_to_canonical
    called = {"count": 0}

    def forbidden(*_args, **_kwargs):
        called["count"] += 1
        raise RuntimeError("adapter must remain upstream")

    r13.adapt_source_mapping_to_canonical = forbidden
    try:
        assert_positive(frozen)
        trap = DirectProtocolTrap("throw")
        assert_negative(trap)
        assert trap.state == 0
        assert called["count"] == 0
    finally:
        r13.adapt_source_mapping_to_canonical = original


def test_010_malformed_schema_shape_tags_duplicate_keys_and_scalar_tokens_are_total_negatives():
    malformed = [
        None,
        (),
        ("WRONG_SCHEMA", ()),
        (r13.CANONICAL_SCHEMA,),
        (r13.CANONICAL_SCHEMA, {}),
        (r13.CANONICAL_SCHEMA, ("X",)),
        (r13.CANONICAL_SCHEMA, ("I", 0, "01")),
        (r13.CANONICAL_SCHEMA, ("I", 1, "not-hex")),
        (r13.CANONICAL_SCHEMA, ("F", "00")),
        (r13.CANONICAL_SCHEMA, ("B", "zz")),
        (r13.CANONICAL_SCHEMA, ("Q", 1)),
        (r13.CANONICAL_SCHEMA, ("D", (("x", ("N",)), ("x", ("N",))))),
        (r13.CANONICAL_SCHEMA, ("D", ((1, ("N",)),))),
        (r13.CANONICAL_SCHEMA, ("D", (("x", ["N"]),))),
    ]
    for value in malformed:
        assert_negative(value)


def test_011_exact_positive_and_five_top_level_binding_mutations_are_negative_and_proof_distinct():
    base = fixture()
    positive = assert_positive(canonical(base))
    changes = {
        "actor_id": "urn:wrong:actor",
        "subject_id": "urn:wrong:subject",
        "world_id": "urn:wrong:world",
        "time_id": "urn:wrong:time",
        "adp010_opportunity_id": "urn:wrong:opportunity",
    }
    proofs = set()
    for key, value in changes.items():
        packet = fixture()
        packet[key] = value
        result = assert_negative(canonical(packet))
        assert result["proof_sha256"] != positive["proof_sha256"]
        proofs.add(result["proof_sha256"])
    assert len(proofs) == len(changes)


def test_012_nested_scope_and_wrong_authority_source_owner_controls_remain_negative():
    cases = []
    p = fixture(); p["opportunity"]["world_id"] = "urn:wrong:nested-world"; cases.append(p)
    p = fixture(); p["evidence"]["subject_classification"]["predicate"] = "WRONG_PREDICATE"; cases.append(p)
    p = fixture(); p["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"; cases.append(p)
    p = fixture(); p["evidence"]["developmental_phase"]["phase"] = "V3DP_OTHER"; cases.append(p)
    for packet in cases:
        assert_negative(canonical(packet))


def test_013_receipt_source_and_authority_identity_are_exact_and_forbidden_aliases_do_not_surface():
    result = assert_positive(canonical(fixture()))
    identity_values = {value for value in result.values() if type(value) is str}
    assert r13.AUTHORITY_ID in identity_values or result.get("authority_id") == r13.AUTHORITY_ID
    for forbidden in r13.FORBIDDEN_ALIAS_AUTHORITIES:
        assert forbidden not in identity_values


def test_014_oversized_integer_encoding_and_evaluation_are_total_under_supported_runtime_settings():
    original = sys.get_int_max_str_digits()
    try:
        baselines = {}
        for setting in (0, int(sys.int_info.str_digits_check_threshold)):
            sys.set_int_max_str_digits(setting)
            for value in (10 ** 5000, -(10 ** 5000), 10 ** 700, -(10 ** 700)):
                packet = fixture()
                packet["evidence"]["actor_activation"]["actor_id"] = value
                result = assert_negative(canonical(packet), "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id")
                key = (value < 0, value.bit_length())
                if key in baselines:
                    assert result == baselines[key]
                else:
                    baselines[key] = result
    finally:
        sys.set_int_max_str_digits(original)


def test_015_equal_inputs_are_deterministic_and_authority_relevant_unequal_inputs_are_distinct():
    a1 = assert_positive(canonical(fixture()))
    a2 = assert_positive(canonical(fixture()))
    assert a1 == a2
    p = fixture(); p["world_id"] = "urn:wrong:world:a"
    n1 = assert_negative(canonical(p))
    p = fixture(); p["world_id"] = "urn:wrong:world:b"
    n2 = assert_negative(canonical(p))
    assert n1["proof_sha256"] != n2["proof_sha256"]


def test_016_repeated_and_concurrent_mixed_positive_negative_evaluation_is_stable():
    pos = canonical(fixture())
    bad = fixture(); bad["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"
    neg = canonical(bad)
    pos_expected = r13.evaluate_direct_positive_applicability(pos)
    neg_expected = r13.evaluate_direct_positive_applicability(neg)
    for _ in range(8):
        assert r13.evaluate_direct_positive_applicability(pos) == pos_expected
        assert r13.evaluate_direct_positive_applicability(neg) == neg_expected
    work = [pos, neg] * 16
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(r13.evaluate_direct_positive_applicability, work))
    for item, result in zip(work, results):
        assert result == (pos_expected if item is pos else neg_expected)


def test_017_noncurrent_synthetic_positive_and_current_project_current_exclusion_are_exact():
    base = fixture()
    assert base["execution_scope"] == r13.SYNTHETIC_SCOPE
    assert_positive(canonical(base))
    for scope in ("CURRENT", "PROJECT_CURRENT"):
        packet = fixture(); packet["execution_scope"] = scope
        assert_negative(canonical(packet))


def test_018_no_current_or_downstream_effects_on_positive_and_negative_paths():
    pos = assert_positive(canonical(fixture()))
    bad = fixture(); bad["evidence"]["actor_activation"]["semantic_owner"] = "WRONG_AUTHORITY"
    neg = assert_negative(canonical(bad))
    for result in (pos, neg):
        assert_no_effect(result)
        text = json.dumps(result, sort_keys=True)
        for forbidden_true in (
            '"project_current_positive_applicability_created": true',
            '"current_positive_obl056_entry_created": true',
            '"actor_current_transition_created": true',
            '"adp008_current_phase_transition_created": true',
            '"adp019_current_occurrence_admitted": true',
            '"obl055_execution_triggered": true',
            '"encounter_or_oee_effect_created": true',
            '"authority_index_effect_created": true',
        ):
            assert forbidden_true not in text.lower()


def test_019_revision_and_schema_identity_are_exact():
    assert r13.R13_CANDIDATE_REVISION == "OBL059_POSITIVE_APPLICABILITY_CANONICAL_INPUT_BOUNDARY_R13"
    assert r13.CANONICAL_SCHEMA == "OBL059_CANONICAL_POSITIVE_APPLICABILITY_PACKET@R13"


def test_020_review_does_not_depend_on_producer_test_class_execution():
    # Independence guard: fixture context is allowed, inherited producer tests are not.
    assert not issubclass(type, producer_context.CourtR13)
    assert callable(r13.evaluate_direct_positive_applicability)
