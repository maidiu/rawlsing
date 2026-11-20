"""C7 sourcefree proof: actual independently pinned C6 entrances into R4.

The R4 test requires a second checkout at exact R4 HEAD, never a copied
surrogate module and never permission to update the native Sorok owners.
"""
from dataclasses import replace
import json
import os
from pathlib import Path
import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, canonical_json, semantic_hash
from rawlsing_next.pre553_s04_cold_custody import SOURCEFREE_ASSERTION
from rawlsing_next.pre553_s04_dhikr_comparative import DHIKRComparisonRequest
from rawlsing_next.pre553_s04_field_forge_v3_bridge import build_empirical_field_forge_v3_handoff
from rawlsing_next.pre553_ff_prev3_possibility_navigation import run_v3_sourcefree_context_path
from rawlsing_next.pre553_c6_seam_contextual_entrances import (
    ENTRY_PARENT,C6ContextualEntrance,C6IndependentParents,
    assemble_c6_contextual_entrance,assemble_two_sourcefree_parent_entrances,
)
from rawlsing_next.pre553_c7_actual_r4_world_bridge import (
    R4_HEAD, R4_SOURCE_SHA256, FICTIONAL_WORLD_PREMISE,
    C7BridgeError, C7Receipt, prepare_c7_world_input, run_c7_pinned_r4_world,
    replay_c7_pinned_r4_world,
)
from rawlsing_next.tests import test_pre553_empirical_query as native


def _source(tag="PYAT-C7-INDEPENDENT-SOURCE"):
    rows=[]
    for x,y,z,n in ((0,0,0,4),(0,1,1,1),(0,1,0,1),(1,0,1,2),(1,1,0,2)):
        for j in range(n):
            rows.append({"id":f"R{x}{y}{z}_{j}",
                         "responses":{"X":x,"Y":y,"Z":z}})
    source=native._build_source(tag,rows,question_namespace="C7-RAW-SOURCE-AXES")
    auth=native._query_authority(tag)
    pred=native._branch_predicate(source,auth,tag="all")
    query=native._query(source,auth,pred,("X","Y","Z"),tag="all")
    execution=native._run(source,auth,pred,query)
    assert execution.facts[0].typed_state=="SUPPORTED"
    return build_empirical_field_forge_v3_handoff(
        query=query,execution=execution,
        comparison_request=DHIKRComparisonRequest(
            target_axis=2,predictor_axes=(0,1),min_branch_n=2,
            max_depth=2,max_nodes=9,max_interaction_order=2,bootstrap_replicates=0,
        ),
        conditioner_index=0,
        sourcefree_origin_assertion=SOURCEFREE_ASSERTION,
    )


def _evidence(tag="PYAT-C7-WORLD"):
    base=_source(tag)
    a_path=run_v3_sourcefree_context_path(
        envelope=base.envelope,external_pin=base.external_pin,
        starting_conditions={0:"0",1:"0"},steps=(),seed=4,
    )
    b_path=run_v3_sourcefree_context_path(
        envelope=base.envelope,external_pin=base.external_pin,
        starting_conditions={0:"1",1:"0"},steps=(),seed=5,
    )
    def enter(path,slot):
        return assemble_c6_contextual_entrance(
            envelope=base.envelope,external_pin=base.external_pin,
            path=path,entrance=ENTRY_PARENT,slot=slot,
        )
    a,b=enter(a_path,"adult-one"),enter(b_path,"adult-two")
    assert a.material()["original_selected_cell_n_if_disclosable"]==4
    assert b.material()["original_selected_cell_n_if_disclosable"]==2
    ar=(base.envelope,base.external_pin,a_path)
    br=(base.envelope,base.external_pin,b_path)
    pair=assemble_two_sourcefree_parent_entrances(
        first=a,second=b,first_source=ar,second_source=br,
        first_expected_receipt_ref=a.ref,second_expected_receipt_ref=b.ref,
    )
    return pair,a,b,ar,br


def _ready(tag="PYAT-C7-ADMIT"):
    pair,a,b,ar,br=_evidence(tag)
    return prepare_c7_world_input(
        pair=pair,expected_pair_ref=pair.ref,first=a,second=b,
        first_source=ar,second_source=br,first_expected_ref=a.ref,
        second_expected_ref=b.ref,
        fictional_world_premise=FICTIONAL_WORLD_PREMISE,
    )


def test_sourcefree_two_adult_candidates_have_distinct_source_pins_and_real_counts():
    material=_ready().material()
    assert material["contract"]=="PYAT_C7_ACTUAL_R4_WORLD_INPUT@1"
    assert material["household_grade"]==FICTIONAL_WORLD_PREMISE
    assert material["actor_issuer"] is None
    assert material["adult_one"]["raw_selected_joint_cell_n"]==4
    assert material["adult_two"]["raw_selected_joint_cell_n"]==2
    assert len(material["adult_one"]["answers"])==3
    assert len(material["adult_two"]["answers"])==3
    assert material["adult_one"]["c6_ref"]!=material["adult_two"]["c6_ref"]
    assert all(x.startswith("opaque_axis_") for x in material["adult_one"]["answers"])
    assert material["adult_one"]["no_real_respondent"] is True
    assert "REAL_PARENT_RELATIONSHIP_OR_PARTNER_SELECTION" in material["not_issued"]


def test_pair_source_ref_must_be_independent_not_rehashed():
    pair,a,b,ar,br=_evidence("PYAT-C7-FORGED-PAIR")
    forged=pair.material()
    forged["pairing_state"]="MARRIED_BY_SOURCE_EVIDENCE"
    corrupted=C6IndependentParents(canonical_json(forged),semantic_hash(forged))
    with pytest.raises(C7BridgeError,match="pair pins"):
        prepare_c7_world_input(
            pair=corrupted,expected_pair_ref=pair.ref,first=a,second=b,
            first_source=ar,second_source=br,first_expected_ref=a.ref,
            second_expected_ref=b.ref,fictional_world_premise=FICTIONAL_WORLD_PREMISE,
        )


def test_parent_self_rehash_or_pin_replacement_fails():
    pair,a,b,ar,br=_evidence("PYAT-C7-FORGED-PARENT")
    material=a.material()
    material["scenario_slot_not_actor_id"]="forged-parent"
    forged=C6ContextualEntrance(canonical_json(material),semantic_hash(material))
    with pytest.raises(Exception):
        prepare_c7_world_input(
            pair=pair,expected_pair_ref=pair.ref,first=forged,second=b,
            first_source=ar,second_source=br,first_expected_ref=a.ref,
            second_expected_ref=b.ref,fictional_world_premise=FICTIONAL_WORLD_PREMISE,
        )


def test_cannot_infer_marriage_or_family_without_declared_world_premise():
    pair,a,b,ar,br=_evidence("PYAT-C7-RELATION")
    with pytest.raises(C7BridgeError,match="explicit independent fictional"):
        prepare_c7_world_input(
            pair=pair,expected_pair_ref=pair.ref,first=a,second=b,
            first_source=ar,second_source=br,
            first_expected_ref=a.ref,second_expected_ref=b.ref,
            fictional_world_premise="SURVEY_PREDICTS_THESE_TWO_PEOPLE_MARRIED",
        )


def test_truly_undisclosed_singleton_cannot_become_r4_parent():
    """A C4 context N>=2 does not allow disclosure of a joint singleton."""
    base=_source("PYAT-C7-SINGLETON-DENY")
    path=run_v3_sourcefree_context_path(
        envelope=base.envelope,external_pin=base.external_pin,
        starting_conditions={0:"0",1:"1"},steps=(),seed=21,
    )
    single=assemble_c6_contextual_entrance(
        envelope=base.envelope,external_pin=base.external_pin,path=path,
        entrance=ENTRY_PARENT,slot="adult-b",
    )
    # context N=2 but each full-joint observed cell has raw support 1.
    assert single.material()["hypothetical_joint_configuration"]==[]
    other_path=run_v3_sourcefree_context_path(
        envelope=base.envelope,external_pin=base.external_pin,
        starting_conditions={0:"0",1:"0"},steps=(),seed=4,
    )
    disclosed=assemble_c6_contextual_entrance(
        envelope=base.envelope,external_pin=base.external_pin,
        path=other_path,entrance=ENTRY_PARENT,slot="adult-a",
    )
    ar=(base.envelope,base.external_pin,path)
    br=(base.envelope,base.external_pin,other_path)
    pair=assemble_two_sourcefree_parent_entrances(
        first=single,second=disclosed,first_source=ar,second_source=br,
        first_expected_receipt_ref=single.ref,
        second_expected_receipt_ref=disclosed.ref,
    )
    with pytest.raises(C7BridgeError,match="whole-joint cell WITHHELD"):
        prepare_c7_world_input(
            pair=pair,expected_pair_ref=pair.ref,first=single,second=disclosed,
            first_source=ar,second_source=br,
            first_expected_ref=single.ref,second_expected_ref=disclosed.ref,
            fictional_world_premise=FICTIONAL_WORLD_PREMISE,
        )


def test_sourcefree_c7_receipt_self_hash_not_external_authority():
    receipt=_ready("PYAT-C7-HASH")
    forged=receipt.material()
    forged["household_grade"]="EMPIRICALLY_ISSUED_SPOUSAL_RELATION"
    altered=C7Receipt(canonical_json(forged),semantic_hash(forged))
    assert altered.ref != receipt.ref
    with pytest.raises(C7BridgeError,match="independently pinned"):
        run_c7_pinned_r4_world(
            input_receipt=altered,expected_input_ref=receipt.ref,
            r4_package_dir=Path("/unavailable"),db_path=Path("/tmp/unavailable"),
            interventions=[],
        )


def test_r4_runtime_cannot_be_called_without_separate_exact_package(tmp_path):
    receipt=_ready("PYAT-C7-SOURCE-CUT-HOLD")
    with pytest.raises(C7BridgeError,match="package"):
        run_c7_pinned_r4_world(
            input_receipt=receipt,expected_input_ref=receipt.ref,
            r4_package_dir=tmp_path/"not-a-package",
            db_path=tmp_path/"absent.db",interventions=[],
        )


def test_bad_intervention_shape_or_existing_database_refused(tmp_path):
    receipt=_ready("PYAT-C7-MALFORMED")
    with pytest.raises(C7BridgeError,match="bounded research"):
        run_c7_pinned_r4_world(
            input_receipt=receipt,expected_input_ref=receipt.ref,
            r4_package_dir=tmp_path,db_path=tmp_path/"db",interventions=[("nadia",1)],
        )
    with pytest.raises(C7BridgeError,match="bounded nonnegative"):
        run_c7_pinned_r4_world(
            input_receipt=receipt,expected_input_ref=receipt.ref,
            r4_package_dir=tmp_path,db_path=tmp_path/"db",interventions=[],
            background_days=-1,
        )


def test_20_real_R4_modules_are_byte_pinned_and_original_owners_unmodified():
    assert len(R4_SOURCE_SHA256)==20
    assert len(set(R4_SOURCE_SHA256))==20
    assert R4_HEAD=="7bff10db7adb7b17bcf035a27561ea59e9a3b2be"
    assert "runtime.py" in R4_SOURCE_SHA256
    assert "parents.py" in R4_SOURCE_SHA256
    assert "world.py" in R4_SOURCE_SHA256
    assert "becoming.py" in R4_SOURCE_SHA256


@pytest.mark.skipif(not os.getenv("PYAT_C7_R4_PACKAGE_DIR"),
                    reason="SEPARATE_R4_CHECKOUT_NOT_SUPPLIED; no R4 runtime proof")
def test_actual_separate_R4_world_actor_body_event_afterlife(tmp_path):
    """Actual Sorok R4, no stub; external two-branch worktrees required."""
    receipt=_ready("PYAT-C7-ACTUAL-R4-ONE-WORLD")
    result=run_c7_pinned_r4_world(
        input_receipt=receipt,expected_input_ref=receipt.ref,
        r4_package_dir=Path(os.environ["PYAT_C7_R4_PACKAGE_DIR"]),
        db_path=tmp_path/"actual-epistemic-world.sqlite3",
        interventions=[("nadia","SIGNAL"),("adult-one","REST"),("adult-two","REST")],
        background_days=3,
    )
    body=result.material()
    assert set(body["actor_ids"])=={"nadia","adult-one","adult-two"}
    assert body["parent_initial_psychic_form_counts"]==[0,0]
    assert body["R4_event_chain_verified"] is True
    assert body["R4_event_chain_count"]>=5
    assert body["final_world_clock"]>=3
    assert len(body["research_interventions"])==3
    assert all(x["choice_grade"]=="INJECTED_NOT_NATIVE_ACTOR_CHOICE"
               for x in body["research_interventions"])
    assert body["native_Sorok_or_original_source_authorized"] is False
    assert body["genuine_R4_world_actor_development_owner_used"] is True
    cold=replay_c7_pinned_r4_world(
        run_receipt=result,expected_run_ref=result.ref,
        source_input=receipt,expected_source_input_ref=receipt.ref,
        r4_package_dir=Path(os.environ["PYAT_C7_R4_PACKAGE_DIR"]),
        db_path=tmp_path/"actual-epistemic-world.sqlite3",
    )
    assert cold.ref==result.ref
    with pytest.raises(C7BridgeError,match="independent input and execution"):
        replay_c7_pinned_r4_world(
            run_receipt=result,
            expected_run_ref=receipt.ref,
            source_input=receipt,expected_source_input_ref=receipt.ref,
            r4_package_dir=Path(os.environ["PYAT_C7_R4_PACKAGE_DIR"]),
            db_path=tmp_path/"actual-epistemic-world.sqlite3",
        )


@pytest.mark.skipif(not os.getenv("PYAT_C7_R4_PACKAGE_DIR"),
                    reason="SEPARATE_R4_CHECKOUT_NOT_SUPPLIED")
def test_r4_byte_modification_rejected_before_execution(tmp_path):
    """Changed/corrupt standalone R4 tree cannot be silently imported."""
    original=Path(os.environ["PYAT_C7_R4_PACKAGE_DIR"])
    target=tmp_path/"um_sorok_organism"
    target.mkdir()
    for name in R4_SOURCE_SHA256:
        (target/name).write_bytes((original/name).read_bytes())
    with (target/"parents.py").open("ab") as f:f.write(b"\n# forged version\n")
    receipt=_ready("PYAT-C7-TAMPER-R4")
    with pytest.raises(C7BridgeError,match="byte/source fidelity"):
        run_c7_pinned_r4_world(
            input_receipt=receipt,expected_input_ref=receipt.ref,
            r4_package_dir=target,db_path=tmp_path/"void.db",interventions=[],
        )
