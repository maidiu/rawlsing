"""GF1E — independent differential + cold-process tests for the named consumer.

These are the AUTHOR'S OWN new tests for this lane (not the frozen 44, not the
GF1I reviewer suite).  They exercise the four separation classes with genuinely
computed relations, the F2 non-copy falsifier, a real native-chain relation and
a fresh OS process reconstruction.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from generic_native_pair_relation import (
    GENERIC_CONSUMER_ID,
    GENERIC_RELATION_OWNER,
    GenericNativePairRelation,
    semantic_hash,
)
from gf1_pair_support_consumer import compute_pair_support_signature as CONSUME
from gf1e_relations import four_relations, PATTERNS

RET = Path(__file__).resolve().parents[1]
COLD_CHILD = RET / "repro" / "cold_consumer_child.py"

CONSUMER_FIELDS = (
    "separation_class", "separation_signature", "support_vectors",
    "zero_cell_semantics", "joint_support_total",
    "condition_states_with_positive_denominator", "result_hash",
)
BANNED = ("dyad", "peer_trait", "personality", "romantic", "attraction")


# ---------------------------------------------------------------- four patterns
@pytest.mark.parametrize("name", sorted(PATTERNS))
def test_four_differential_patterns_classify(name):
    rel = four_relations()[name]
    out = CONSUME(rel)
    assert out["decision_state"] == "PAIR_SUPPORT_SIGNATURE_COMPUTED"
    assert out["separation_class"] == name
    assert out["downstream_value_produced"] is True
    assert out["consumer_id"] == GENERIC_CONSUMER_ID


def test_computed_fields_are_not_copied_and_are_derived():
    for name, rel in four_relations().items():
        material = rel.as_dict()
        for field in CONSUMER_FIELDS:
            assert field not in material, f"{name}: {field} must not be copied"
        out = CONSUME(rel)
        cells, eligible = PATTERNS[name]
        # support vectors genuinely recompute the 2x2 counts
        for c in sorted(cells):
            for t in sorted(cells[c]):
                assert out["support_vectors"][c][t] == cells[c][t]
        # joint total is the sum of the profile
        assert out["joint_support_total"] == sum(
            v for row in cells.values() for v in row.values())
        assert out["joint_support_total"] == eligible
        # positive-denominator condition states are recomputed, not asserted
        assert out["condition_states_with_positive_denominator"] == sorted(
            c for c in sorted(cells) if sum(cells[c].values()) > 0)
        # zero-cell semantics preserves the observed-zero vs zero-support typing
        for c in sorted(cells):
            for t in sorted(cells[c]):
                expect = ("OBSERVED_POSITIVE" if cells[c][t] > 0
                          else "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET")
                assert out["zero_cell_semantics"][c][t] == expect
        # deterministic result hash
        assert out["result_hash"] == CONSUME(rel)["result_hash"]
        assert len(out["result_hash"]) == 64


def test_identity_semantics_and_no_personhood_claim():
    rel = four_relations()["EXACT_PAIR_SEPARATION"]
    out = CONSUME(rel)
    assert out["read_relation_object_id"] == rel.object_id
    assert out["read_relation_content_hash"] == rel.content_hash
    assert out["read_relation_owner"] == GENERIC_RELATION_OWNER
    assert out["generic_native_semantics_hold"] == "RETAINED"
    assert out["is_population_evidence_not_actor_fact"] is True
    assert out["makes_no_causal_or_psychological_claim"] is True
    assert out["production_owner_commit"] is False
    assert out["measure_kind"] == "RAW"
    assert out["permission_ceilings"]["producer"] == ["SOURCE_FREE_DEV"]
    flat = json.dumps(out).lower()
    for banned in BANNED:
        assert banned not in flat.replace("!= relationship_or_dyad", "")


def test_invalid_and_empty_inputs():
    assert CONSUME({"nope": 1})["decision_state"] == "CONSUMER_INPUT_NOT_GENERIC_PAIR_RELATION"
    rel = four_relations()["EXACT_PAIR_SEPARATION"]
    f = dict(rel.__dict__)
    f.pop("content_hash"); f.pop("object_id")
    f["conditional_count_profile"] = ()
    from generic_native_pair_relation import _projection
    d = semantic_hash(_projection(f))
    empty = GenericNativePairRelation(
        **f, content_hash=d, object_id=f"urn:rawlsing:gf1:generic-pair-relation:sha256:{d}")
    out = CONSUME(empty)
    assert out["decision_state"] == "RESPONSE_INPUTS_VALID_EMPTY"
    assert out["downstream_value_produced"] is False


# ---------------------------------------------------------------- real native
def test_real_native_baseline_relation_classifies_exact_separation():
    import gf1_bootstrap as GB  # noqa: F401  (reattests the 74-object closure)
    import gf1_native as N
    from generic_native_pair_relation import (
        produce_generic_native_pair_relation as PRODUCE_GENERIC)

    bundle = N.run_native(profile="BASELINE", root=GB.RT / "gf1_run")
    items, _ = N.collect_link_material(bundle)
    item = [it for it in items if it["kind"] == "QUERY"][0]
    relation = PRODUCE_GENERIC(
        joint_fact=item["fact"], joint_query=item["query"],
        conditioner_ref=item["query"].target_refs[0],
        target_ref=item["query"].target_refs[1],
        producer_permission_ceiling=("SOURCE_FREE_DEV",))
    out = CONSUME(relation)
    assert out["separation_class"] == "EXACT_PAIR_SEPARATION"
    assert out["support_vectors"] == {"0": {"0": 1, "1": 0}, "1": {"0": 0, "1": 1}}
    assert out["joint_support_total"] == 2
    assert out["condition_states_with_positive_denominator"] == ["0", "1"]
    assert relation.eligible_joint_risk_total == 2


# ---------------------------------------------------------------- cold process
def test_cold_process_consumer_reconstruction_bit_identical():
    outs = []
    for i in range(2):
        dest = RET / "observations" / f"gf1e_cold_consumer_{i}.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, str(COLD_CHILD), str(dest)],
                       check=True, capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        outs.append(json.loads(dest.read_text()))
    assert len({o["pid"] for o in outs}) == 2
    assert json.dumps(outs[0]["results"], sort_keys=True) == \
        json.dumps(outs[1]["results"], sort_keys=True)
    got = {k: v["separation_class"] for k, v in outs[0]["results"].items()}
    assert got == {k: k for k in PATTERNS}
    # the cold process result matches the in-process result
    for name in PATTERNS:
        assert outs[0]["results"][name] == CONSUME(four_relations()[name])
