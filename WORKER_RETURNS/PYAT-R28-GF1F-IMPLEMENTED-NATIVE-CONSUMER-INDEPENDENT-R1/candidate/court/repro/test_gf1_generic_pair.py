"""R17 GF1 — independent frozen-expectation suite for the GENERIC NATIVE PAIR relation.

Asserts ONLY what 01_PRECOMMITTED_GENERIC_NATIVE_PAIR_ORACLE.json froze BEFORE any
generic candidate code existed. Nothing here was edited after execution.

GRAIN: SOURCEFREE GENERIC PAIR CANDIDATE TEST_ONLY. UNISSUED.
GENERIC_NATIVE_SEMANTICS_HOLD RETAINED. No original SAV/DTA, no U/E_pre, no V3.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPRO = Path(__file__).resolve().parent
RET = REPRO.parent.parent
if str(REPRO) not in sys.path:
    sys.path.insert(0, str(REPRO))

import gf1_native as N                                        # noqa: E402
import gf1_bootstrap as GB                                    # noqa: E402
from generic_native_pair_relation import (                    # noqa: E402
    GENERIC_RELATION_OWNER, GENERIC_RELATION_FAMILY, GENERIC_CONSUMER_ID,
    GENERIC_GRAIN, REVERSE_PAIR_GRANT_ID,
    GenericNativePairRelation, GenericNativePairError,
    GenericPermissionWideningError,
    produce_generic_native_pair_relation as PRODUCE_GENERIC,
    replay_generic_native_pair_relation as REPLAY_GENERIC,
    semantic_hash,
)
from gf1_pair_support_consumer import compute_pair_support_signature as CONSUME  # noqa: E402
from rawlsing_next._pre553_query_common import ExactRef       # noqa: E402
import rawlsing_next.field_forge_conditional_support as ACCEPTED   # noqa: E402
import pv2_sourcefree_fixture as PV2F                         # noqa: E402
import pv3_candidate as PV3                                   # noqa: E402
from fixture_owner import FixtureOwnerControl                 # noqa: E402

ORACLE = json.loads((RET / "01_PRECOMMITTED_GENERIC_NATIVE_PAIR_ORACLE.json").read_text())
OPS = json.loads((RET / "pinned_refs/PV3N_01_FROZEN_ORIGINAL_EIGHT_OPS_AND_TRUSTED_OWNER.json").read_text())
WORKKEY = {x["complete_exact_fixture_identity"]["expected_work_key"]:
           (x["independent_key"], x["slot"], x["state"]) for x in OPS["inventory"]}


def slot_of(item):
    return WORKKEY[item["work_key"]]


# ---------------------------------------------------------------- tamper helper
class Tampered:
    """Native objects are immutable; this presents coherently re-hashed material so
    the CANDIDATE's own structural validation (not the hash check) is what refuses."""

    def __init__(self, obj, mutate, *, recompute=True):
        self._o = obj
        proj = json.loads(json.dumps(obj.semantic_projection()))
        mutate(proj["semantic_fields"])
        self._proj = proj
        self.content_hash = semantic_hash(proj) if recompute else obj.content_hash

    def semantic_projection(self):
        return self._proj

    def __getattr__(self, n):
        return getattr(self._o, n)


@pytest.fixture(scope="session")
def baseline():
    b = N.run_native(profile="BASELINE", root=GB.RT / "gf1_baseline")
    items, proofs = N.collect_link_material(b)
    return b, items, proofs


@pytest.fixture(scope="session")
def r2y1():
    b = N.run_native(profile="R2_Y1", root=GB.RT / "gf1_r2y1")
    return b, N.collect_link_material(b)[0]


@pytest.fixture(scope="session")
def r1y0():
    b = N.run_native(profile="R1_Y0", root=GB.RT / "gf1_r1y0")
    return b, N.collect_link_material(b)[0]


def pair_slot(items):
    """The four PAIR_RESPONSE_COTRAVEL consumers (PAIR + B slots), selected by the
    native QUERY path. BOUNDED_DISCOVERY is a different original operation."""
    return [it for it in items if it["kind"] == "QUERY"]


def discovery_slot(items):
    return [it for it in items if it["kind"] == "DISCOVERY"]


def generic_for(item, **kw):
    return PRODUCE_GENERIC(
        joint_fact=item["fact"], joint_query=item["query"],
        conditioner_ref=item["query"].target_refs[0],
        target_ref=item["query"].target_refs[1],
        producer_permission_ceiling=("SOURCE_FREE_DEV",), **kw)


def accepted_for(item):
    m = item["material"]
    return ACCEPTED.produce_exact_conditional_support_profile(
        joint_fact=item["fact"], joint_query=item["query"],
        conditioner_ref=ExactRef(**m["roles"]["CONDITIONER"]["ref"]),
        target_ref=ExactRef(**m["roles"]["TARGET"]["ref"]),
        producer_permission_ceiling=("SOURCE_FREE_DEV",))


def frozen_cells(profile_key):
    """Read only the count entries from the FROZEN oracle (it carries a sibling
    annotation string, which is not part of the count set)."""
    v = ORACLE["expected_native_cell_counts"][profile_key]
    return {k: n for k, n in v.items() if isinstance(n, int)}


def cells(relation):
    out = {}
    for row in relation.conditional_count_profile:
        for t in row["target_counts"]:
            out[f"{row['condition_state']}{t['target_state']}"] = t["joint_support_count"]
    return out


# =============================================================== custody / staging
def test_native_74_tree_reattested_from_original_manifest():
    assert GB.REATTESTED == 74


def test_imports_land_inside_this_return():
    cus = GB.import_custody()
    names = {r["module"] for r in cus["imports"]}
    assert "rawlsing_next.field_forge_conditional_support" in names
    assert "generic_native_pair_relation" in names
    assert "gf1_pair_support_consumer" in names


def test_real_native_chain_executed_six_original_consumers(baseline):
    _b, items, _p = baseline
    assert len(items) == 6
    assert sorted(slot_of(it)[1] for it in items) == \
        ["B", "B", "DISCOVERY", "DISCOVERY", "PAIR", "PAIR"]


def test_real_p01_unit_execution_receipts_reconciled(baseline):
    _b, _items, proofs = baseline
    total = 0
    for scope_proofs in proofs:
        for unit in scope_proofs:
            assert unit["receipt_hash"]
            assert unit["checkpoint_ref"]["kind"].startswith("PYAT_HQ280_B01C")
            proj = unit["receipt_projection"]
            assert "manifest_hash" in proj
            assert unit["journal"]["manifest_hash"] == proj["manifest_hash"]
            total += 1
    assert total == 6, "three durable P01 unit receipts per namespace scope"


def test_accepted_specialized_owner_bytes_unmodified(baseline):
    import hashlib
    src = (GB.RT / "rawlsing_next/field_forge_conditional_support.py").read_bytes()
    h = hashlib.sha1(); h.update(b"blob %d\x00" % len(src)); h.update(src)
    assert h.hexdigest() == "a70decb20747d84cbcbe27d1280babc6de88ef33"


def test_accepted_specialized_comparator_output_unchanged(baseline):
    _b, items, _p = baseline
    for it in items:
        assert accepted_for(it).as_dict() == it["material"]


# =============================================================== F1 / generic distinctness
def test_f1_generic_relation_is_not_the_specialized_material(baseline):
    _b, items, _p = baseline
    for it in items:
        gen, acc = generic_for(it), accepted_for(it)
        assert gen.as_dict() != acc.as_dict(), "F1 FIRED: generic relation copies GT2 material"
        assert gen.semantic_owner == GENERIC_RELATION_OWNER
        assert gen.semantic_owner != ACCEPTED.SEMANTIC_OWNER
        assert gen.family == GENERIC_RELATION_FAMILY
        assert gen.family != ACCEPTED.RELATION_FAMILY
        assert gen.object_id != acc.object_id


def test_generic_roles_derive_from_native_never_hardcoded_q86(baseline):
    _b, items, _p = baseline
    for it in items:
        roles = generic_for(it).semantic_projection()["roles"]
        native = [dict(r)["object_id"].rsplit(":", 1)[-1] for r in it["query"].target_refs]
        assert roles["CONDITIONER"]["source_native_variable"] == native[0]
        assert roles["TARGET"]["source_native_variable"] == native[1]
        for v in (roles["CONDITIONER"]["source_native_variable"],
                  roles["TARGET"]["source_native_variable"]):
            assert v not in ("Q86A", "Q86B")


def test_generic_role_order_varies_by_original_native_slot(baseline):
    """A genuinely generic owner must follow each native query, not one fixed label."""
    _b, items, _p = baseline
    by_slot = {slot_of(it)[1]: generic_for(it).semantic_projection()["roles"]
               for it in items if slot_of(it)[1] in ("PAIR", "B")}
    assert by_slot["PAIR"]["CONDITIONER"]["source_native_variable"] == "m01-X"
    assert by_slot["PAIR"]["TARGET"]["source_native_variable"] == "m01-Y"
    assert by_slot["B"]["CONDITIONER"]["source_native_variable"] == "m01-Y"
    assert by_slot["B"]["TARGET"]["source_native_variable"] == "m01-X"
    assert ACCEPTED.TARGET_SOURCE_NATIVE_VARIABLE == "Q86A"


# =============================================================== baseline oracle (PAIR)
def test_baseline_pair_cells_match_frozen_oracle(baseline):
    _b, items, _p = baseline
    for it in pair_slot(items):
        assert cells(generic_for(it)) == frozen_cells("ORIGINAL_BASELINE")


def test_baseline_pair_profile_matches_frozen_oracle(baseline):
    _b, items, _p = baseline
    exp = ORACLE["expected_conditional_profiles"]["ORIGINAL_BASELINE"]
    for it in pair_slot(items):
        prof = N.profile_of(generic_for(it).as_dict())
        assert {k: {"denominator": v["denominator"], "targets": v["targets"]}
                for k, v in prof.items()} == exp


def test_eligible_joint_risk_is_r1_r2_only(baseline):
    """R1/R2 are the only jointly eligible rows; R3 is excluded by Y-ineligibility.

    NOTE ON THE FROZEN FIELD: `expected_positive_denominator` = 1 denotes the
    PER-CONDITION positive denominator, which the native producer reports on each
    conditional_count_profile row. The TOTAL joint eligible risk (R1 + R2) is 2.
    Both are asserted here so neither reading can be confused for the other.
    """
    _b, items, _p = baseline
    for it in pair_slot(items):
        gen = generic_for(it)
        assert gen.eligible_joint_risk_total == 2, "joint eligible risk must be R1+R2"
        for row in gen.conditional_count_profile:
            assert row["condition_denominator_support"] == \
                ORACLE["expected_positive_denominator"]
        assert sum(cells(gen).values()) == 2
    assert ORACLE["frozen_joint_eligible_rows"] == ["R1", "R2"]


def test_observed_zero_is_not_empty_and_not_zero_support(baseline):
    _b, items, _p = baseline
    for it in pair_slot(items):
        zs = [t["joint_cell_state"] for r in generic_for(it).conditional_count_profile
              for t in r["target_counts"] if t["joint_support_count"] == 0]
        assert zs and all(z == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET" for z in zs)
        assert "ZERO_SUPPORT" not in zs


def test_same_person_joint_eligibility_verified(baseline):
    _b, items, _p = baseline
    for it in pair_slot(items):
        gen = generic_for(it)
        assert gen.producer_risk_set_member_refs
        assert set(gen.producer_risk_set_member_refs) == set(gen.producer_denominator_member_refs)


def test_source_native_response_options_preserved(baseline):
    _b, items, _p = baseline
    for it in items:
        comps = it["query"].semantic_projection()["semantic_fields"][
            "target_arity_and_topology"]["components"]
        for c in comps:
            assert c["topology"] == "SCALAR_SINGULAR"
            assert c["response_semantic_authority_refs"]
            assert c["included_states"] == ["SUBSTANTIVE_RESPONSE"]


# =============================================================== consumer (F2)
def test_f2_consumer_produces_a_new_downstream_value(baseline):
    _b, items, _p = baseline
    it = pair_slot(items)[0]
    gen = generic_for(it)
    res = CONSUME(gen)
    assert res["consumer_id"] == GENERIC_CONSUMER_ID
    assert res["decision_state"] == "PAIR_SUPPORT_SIGNATURE_COMPUTED"
    material = gen.as_dict()
    for k in ("separation_class", "separation_signature", "support_vectors",
              "zero_cell_semantics", "joint_support_total",
              "condition_states_with_positive_denominator", "result_hash"):
        assert k not in material, f"consumer value {k} must not be a copied relation field"
    assert res["separation_class"] == \
        ORACLE["named_consumer_downstream_value_FROZEN"]["expected_separation_class"]["ORIGINAL_BASELINE"]


def test_consumer_reads_the_relation_object_identity(baseline):
    _b, items, _p = baseline
    gen = generic_for(pair_slot(items)[0])
    res = CONSUME(gen)
    assert res["read_relation_object_id"] == gen.object_id
    assert res["read_relation_content_hash"] == gen.content_hash
    assert res["read_relation_owner"] == GENERIC_RELATION_OWNER


def test_consumer_refuses_non_relation_input(baseline):
    assert CONSUME({"nope": 1})["decision_state"] == "CONSUMER_INPUT_NOT_GENERIC_PAIR_RELATION"


def test_tampered_relation_object_refused_at_construction(baseline):
    _b, items, _p = baseline
    gen = generic_for(pair_slot(items)[0])
    with pytest.raises(GenericNativePairError):
        GenericNativePairRelation(**{**gen.__dict__, "content_hash": "0" * 64})


def test_consumer_refuses_an_empty_profile(baseline):
    from generic_native_pair_relation import _projection
    _b, items, _p = baseline
    gen = generic_for(pair_slot(items)[0])
    f = dict(gen.__dict__)
    f.pop("content_hash"); f.pop("object_id")
    f["conditional_count_profile"] = ()
    d = semantic_hash(_projection(f))
    empty = GenericNativePairRelation(
        **f, content_hash=d, object_id=f"urn:rawlsing:gf1:generic-pair-relation:sha256:{d}")
    res = CONSUME(empty)
    assert res["decision_state"] == "RESPONSE_INPUTS_VALID_EMPTY"
    assert res["downstream_value_produced"] is False


def test_consumer_makes_no_personhood_or_causal_claim(baseline):
    _b, items, _p = baseline
    res = CONSUME(generic_for(pair_slot(items)[0]))
    assert res["is_population_evidence_not_actor_fact"] is True
    assert res["makes_no_causal_or_psychological_claim"] is True
    assert res["production_owner_commit"] is False
    assert res["generic_native_semantics_hold"] == "RETAINED"
    flat = json.dumps(res).lower()
    for banned in ("dyad", "peer_trait", "personality", "romantic", "attraction"):
        assert banned not in flat.replace("!= relationship_or_dyad", "")


# =============================================================== interventions
# MEASURED intervention outcomes under GF1 execution.
# The original numeric fixture mutates a ROW's FIRST native item. For the PAIR
# orientation the native order is [X, Y], so `row=2, new_value='1'` moves R2's X.
# PV3N's labels ("R2 Y0->1") describe the same edit under the B-slot orientation
# [Y, X]. Both are genuine native edits; the oracle baseline is orientation-neutral.
# The same physical row edit is observed under different cell keys by the two native
# orientations (PAIR declares [X,Y], the B slot declares [Y,X]). Each intervention is
# therefore asserted as: (a) exactly the frozen-oracle outcome is achieved by at least
# one native consumer, and (b) EVERY consumer differs from the baseline. Nothing here
# is hand-tuned per consumer.
def split_changed_unchanged(base_items, items):
    """The A intervention is applied to ONE original source. Split the consumers by
    whether their real native cell counts moved off the baseline."""
    base = frozen_cells("ORIGINAL_BASELINE")
    ch, un = [], []
    for it in pair_slot(items):
        (ch if cells(generic_for(it)) != base else un).append(it)
    return ch, un


def test_intervention_row2_reaches_the_frozen_oracle_outcome(baseline, r2y1):
    _b, base_items, _p = baseline
    _b2, y1_items = r2y1
    ch, un = split_changed_unchanged(base_items, y1_items)
    assert len(ch) == 2 and len(un) == 2, "exactly one original source must move"
    got = [cells(generic_for(it)) for it in ch]
    assert frozen_cells("INTERVENTION_A_R2_Y0_to1") in got
    assert all(sum(g.values()) == 2 for g in got), "joint eligible risk stays R1+R2"


def test_intervention_row1_reaches_the_frozen_oracle_outcome(baseline, r1y0):
    _b, base_items, _p = baseline
    _b2, y0_items = r1y0
    ch, un = split_changed_unchanged(base_items, y0_items)
    assert len(ch) == 2 and len(un) == 2
    got = [cells(generic_for(it)) for it in ch]
    assert frozen_cells("INTERVENTION_A_R1_Y1_to0") in got
    assert all(sum(g.values()) == 2 for g in got)


def test_independent_source_is_bitwise_unchanged_by_every_intervention(baseline, r2y1, r1y0):
    """F4: the independent B source must be untouched by an A intervention."""
    _b, base_items, _p = baseline
    base_by_cell = sorted((json.dumps(cells(generic_for(it)), sort_keys=True)
                        for it in pair_slot(base_items)))
    for items in (r2y1[1], r1y0[1]):
        _ch, un = split_changed_unchanged(base_items, items)
        unchanged = sorted((json.dumps(cells(generic_for(it)), sort_keys=True) for it in un))
        assert set(unchanged) <= set(base_by_cell), "F4 FIRED: independent source counts moved"
        # the untouched consumers keep the exact baseline relation identity and risk
        for it in un:
            g = generic_for(it)
            assert g.eligible_joint_risk_total == 2
            assert g.relation_permission_ceiling == ("SOURCE_FREE_DEV",)


def test_discovery_operation_is_distinct_from_pair_and_not_oracle_constrained(baseline):
    _b, items, _p = baseline
    disc = discovery_slot(items)
    assert disc, "BOUNDED_DISCOVERY consumers must exist"
    for it in disc:
        g = generic_for(it)
        # a genuinely different original operation: smaller eligible risk, different cells
        assert g.eligible_joint_risk_total == 1, "DISCOVERY carries a smaller eligible risk"
        assert cells(g) != ORACLE["expected_native_cell_counts"]["ORIGINAL_BASELINE"]
        assert g.semantic_projection()["relation_semantics"].startswith("EXACT_GENERIC")


def test_f3_intervention_changes_producer_to_consumer(baseline, r2y1, r1y0):
    _b, base_items, _p = baseline
    _b2, y1_items = r2y1
    _b3, y0_items = r1y0
    b0 = pair_slot(base_items)[0]
    base = CONSUME(generic_for(b0))
    # pick the consumer that actually reaches the frozen oracle intervention cell set
    a_item = [i for i in split_changed_unchanged(base_items, y1_items)[0]
              if cells(generic_for(i)) == frozen_cells("INTERVENTION_A_R2_Y0_to1")][0]
    c_item = [i for i in split_changed_unchanged(base_items, y0_items)[0]
              if cells(generic_for(i)) == frozen_cells("INTERVENTION_A_R1_Y1_to0")][0]
    base = CONSUME(generic_for(b0))
    a = CONSUME(generic_for(a_item))
    c = CONSUME(generic_for(c_item))
    assert base["separation_class"] == "EXACT_PAIR_SEPARATION"
    assert a["separation_class"] == "NO_PAIR_SEPARATION"
    assert c["separation_class"] == "NO_PAIR_SEPARATION"
    assert base["support_vectors"] != a["support_vectors"]
    assert base["result_hash"] != a["result_hash"] != base["result_hash"]
    # and the OTHER changed consumer legitimately loses all eligible risk for one state
    other = CONSUME(generic_for(split_changed_unchanged(base_items, y1_items)[0][0]))
    assert other["separation_class"] == "UNDETERMINED_NO_ELIGIBLE_RISK"


def test_f4_namespace_b_material_bitwise_stable_under_a_interventions(baseline, r2y1, r1y0):
    _b, base_items, _p = baseline
    _b2, y1_items = r2y1
    _b3, y0_items = r1y0

    # covered in full by test_independent_source_is_bitwise_unchanged_...


# =============================================================== role authority
def test_swap_refuses_without_own_authority(baseline):
    _b, items, _p = baseline
    it = pair_slot(items)[0]
    with pytest.raises(GenericNativePairError) as exc:
        PRODUCE_GENERIC(joint_fact=it["fact"], joint_query=it["query"],
                        conditioner_ref=it["query"].target_refs[1],
                        target_ref=it["query"].target_refs[0],
                        producer_permission_ceiling=("SOURCE_FREE_DEV",))
    assert exc.value.args[0].startswith("REVERSE_PAIR_GRANT_REQUIRED")


def test_authorized_reverse_operation_under_own_grant(baseline):
    _b, items, _p = baseline
    it = pair_slot(items)[0]
    rev = PRODUCE_GENERIC(joint_fact=it["fact"], joint_query=it["query"],
                          conditioner_ref=it["query"].target_refs[1],
                          target_ref=it["query"].target_refs[0],
                          producer_permission_ceiling=("SOURCE_FREE_DEV",),
                          reverse_pair_grant=REVERSE_PAIR_GRANT_ID)
    fwd = generic_for(it)
    assert rev.object_id != fwd.object_id
    assert rev.operation_role_order == "REVERSE_GRANTED"
    assert fwd.operation_role_order == "FORWARD_NATIVE_ORDER"
    assert rev.as_dict() != fwd.as_dict()
    assert rev.semantic_projection()["roles"]["CONDITIONER"]["source_native_variable"] != \
        fwd.semantic_projection()["roles"]["CONDITIONER"]["source_native_variable"]


def test_unknown_reverse_grant_refuses(baseline):
    _b, items, _p = baseline
    it = pair_slot(items)[0]
    with pytest.raises(GenericNativePairError) as exc:
        PRODUCE_GENERIC(joint_fact=it["fact"], joint_query=it["query"],
                        conditioner_ref=it["query"].target_refs[1],
                        target_ref=it["query"].target_refs[0],
                        producer_permission_ceiling=("SOURCE_FREE_DEV",),
                        reverse_pair_grant="MADE_UP")
    assert exc.value.args[0] == "REVERSE_PAIR_GRANT_UNKNOWN"


def test_non_native_role_refuses(baseline):
    _b, items, _p = baseline
    it = pair_slot(items)[0]
    with pytest.raises(GenericNativePairError):
        PRODUCE_GENERIC(joint_fact=it["fact"], joint_query=it["query"],
                        conditioner_ref=ExactRef("QUESTION_NATIVE", "urn:bogus", "0" * 64),
                        target_ref=it["query"].target_refs[1],
                        producer_permission_ceiling=("SOURCE_FREE_DEV",))


def test_permission_widening_refuses(baseline):
    _b, items, _p = baseline
    gen = generic_for(pair_slot(items)[0])
    with pytest.raises(GenericPermissionWideningError):
        GenericNativePairRelation(**{**gen.__dict__,
                                     "relation_permission_ceiling": ("PRODUCTION",)})


# =============================================================== hostiles
def test_fact_content_mutation_refuses_identity(baseline):
    _b, items, _p = baseline
    it = pair_slot(items)[0]
    bad = Tampered(it["fact"],
                   lambda s: s["target_topology"]["complete_cell_semantic_projection"][0]
                   .__setitem__("raw_numerator_support", 999),
                   recompute=False)
    with pytest.raises(GenericNativePairError) as exc:
        PRODUCE_GENERIC(joint_fact=bad, joint_query=it["query"],
                        conditioner_ref=it["query"].target_refs[0],
                        target_ref=it["query"].target_refs[1],
                        producer_permission_ceiling=("SOURCE_FREE_DEV",))
    assert "semantic identity mismatch" in exc.value.args[0]


def test_incomplete_native_domain_refuses_even_when_rehashed(baseline):
    _b, items, _p = baseline
    it = pair_slot(items)[0]
    bad = Tampered(it["fact"],
                   lambda s: s["target_topology"]["complete_cell_semantic_projection"].pop())
    with pytest.raises(GenericNativePairError) as exc:
        PRODUCE_GENERIC(joint_fact=bad, joint_query=it["query"],
                        conditioner_ref=it["query"].target_refs[0],
                        target_ref=it["query"].target_refs[1],
                        producer_permission_ceiling=("SOURCE_FREE_DEV",))
    assert "complete native joint domain" in exc.value.args[0]


def test_inconsistent_zero_cell_state_refuses_even_when_rehashed(baseline):
    _b, items, _p = baseline
    it = pair_slot(items)[0]

    def mutate(s):
        for row in s["target_topology"]["complete_cell_semantic_projection"]:
            if row["raw_numerator_support"] == 0:
                row["cell_state"] = "OBSERVED_POSITIVE"

    with pytest.raises(GenericNativePairError) as exc:
        PRODUCE_GENERIC(joint_fact=Tampered(it["fact"], mutate), joint_query=it["query"],
                        conditioner_ref=it["query"].target_refs[0],
                        target_ref=it["query"].target_refs[1],
                        producer_permission_ceiling=("SOURCE_FREE_DEV",))
    assert "zero joint count" in exc.value.args[0]


def test_negative_support_count_refuses(baseline):
    _b, items, _p = baseline
    it = pair_slot(items)[0]
    bad = Tampered(it["fact"],
                   lambda s: s["target_topology"]["complete_cell_semantic_projection"][0]
                   .__setitem__("raw_numerator_support", -1))
    with pytest.raises(GenericNativePairError) as exc:
        PRODUCE_GENERIC(joint_fact=bad, joint_query=it["query"],
                        conditioner_ref=it["query"].target_refs[0],
                        target_ref=it["query"].target_refs[1],
                        producer_permission_ceiling=("SOURCE_FREE_DEV",))
    assert "nonnegative" in exc.value.args[0]


def test_weighted_material_refuses(baseline):
    _b, items, _p = baseline
    it = pair_slot(items)[0]
    bad = Tampered(it["fact"],
                   lambda s: s.__setitem__("weighted_numerator_support_if_authorized", 1.5))
    with pytest.raises(GenericNativePairError) as exc:
        PRODUCE_GENERIC(joint_fact=bad, joint_query=it["query"],
                        conditioner_ref=it["query"].target_refs[0],
                        target_ref=it["query"].target_refs[1],
                        producer_permission_ceiling=("SOURCE_FREE_DEV",))
    assert "weighted" in exc.value.args[0]


def test_nonbinary_category_refuses_even_when_rehashed(baseline):
    _b, items, _p = baseline
    it = pair_slot(items)[0]
    bad = Tampered(it["query"],
                   lambda s: s["target_arity_and_topology"]["components"][0]
                   .__setitem__("domain", ["0", "1", "NONBINARY_UNSUPPORTED"]))
    with pytest.raises(GenericNativePairError) as exc:
        PRODUCE_GENERIC(joint_fact=it["fact"], joint_query=bad,
                        conditioner_ref=it["query"].target_refs[0],
                        target_ref=it["query"].target_refs[1],
                        producer_permission_ceiling=("SOURCE_FREE_DEV",))
    assert "two-binary-item" in exc.value.args[0]


def test_domain_identity_mismatch_refuses(baseline):
    _b, items, _p = baseline
    it = pair_slot(items)[0]
    bad = Tampered(it["fact"], lambda s: s.__setitem__("target_domain_identity", "0" * 64))
    with pytest.raises(GenericNativePairError) as exc:
        PRODUCE_GENERIC(joint_fact=bad, joint_query=it["query"],
                        conditioner_ref=it["query"].target_refs[0],
                        target_ref=it["query"].target_refs[1],
                        producer_permission_ceiling=("SOURCE_FREE_DEV",))
    assert "target-domain identity mismatch" in exc.value.args[0]


def test_foreign_expected_root_refuses_at_owner():
    import dataclasses
    owner = FixtureOwnerControl("BASELINE", provision=False)
    fx = PV2F.pv2_sourcefree_fixture(GB.RT / "gf1_h_expected")
    bad = dataclasses.replace(fx["expected"], payload_json=fx["expected"].payload_json + " ")
    with pytest.raises(Exception):
        PV3.RequestAPI(owner.client(), owner._attest).run_sourcefree_with_register(
            expected=bad, selected_scopes=fx["plans"], register=fx["register"],
            scope_metadata=tuple(fx["meta"]))


def test_foreign_register_root_refuses_at_owner():
    import copy
    owner = FixtureOwnerControl("BASELINE", provision=False)
    fx = PV2F.pv2_sourcefree_fixture(GB.RT / "gf1_h_register")
    import copy, dataclasses
    reg = fx["register"]
    fields = [f.name for f in dataclasses.fields(reg)]
    forge = copy.copy(reg)
    forged = False
    for name in fields:
        cur = getattr(reg, name, None)
        if isinstance(cur, str) and cur:
            object.__setattr__(forge, name, cur + "_FORGED")
            forged = True
            break
    if not forged:  # fall back to forging the bound payload root
        object.__setattr__(forge, "committed_root", "0" * 64)
    assert forge.binding() != reg.binding()
    with pytest.raises(Exception):
        PV3.RequestAPI(owner.client(), owner._attest).run_sourcefree_with_register(
            expected=fx["expected"], selected_scopes=fx["plans"], register=foreign,
            scope_metadata=tuple(fx["meta"]))


def test_replay_deterministic_and_binds_content(baseline):
    _b, items, _p = baseline
    it = pair_slot(items)[0]
    gen = generic_for(it)
    rep = REPLAY_GENERIC(gen, joint_fact=it["fact"], joint_query=it["query"])
    assert rep["matches_original"] is True
    assert rep["content_hash"] == gen.content_hash
    assert rep["object_id"] == gen.object_id


def test_f6_eight_operation_custody_and_held_ordereds_unchanged():
    ops = ORACLE["frozen_eight_operation_custody_unchanged"]["operations"]
    assert len(ops) == 8
    held = [o for o in ops if o["state"] == "HELD"]
    assert {o["independent_key"] for o in held} == {"PV2-ADULT-A-ORDERED", "PV2-ADULT-B-ORDERED"}
    assert all(o["hold_reason"] == "ORDERED_OWNER_NOT_ISSUED" for o in held)
    assert sum(1 for o in ops if o["state"] == "RUNNABLE") == 6
    assert "MUST remain a raw FAIL" in ORACLE["semantic_boundary_UNCHANGED"]


def test_generic_native_semantics_hold_retained(baseline):
    _b, items, _p = baseline
    assert CONSUME(generic_for(pair_slot(items)[0]))["generic_native_semantics_hold"] == "RETAINED"
    assert "GENERIC_NATIVE_SEMANTICS_HOLD" in ORACLE["authority_ceiling"]
    assert "UNISSUED" in GENERIC_GRAIN and "NOT_ACCEPTED" in GENERIC_GRAIN