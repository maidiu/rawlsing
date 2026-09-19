from __future__ import annotations
import importlib.util, json
from pathlib import Path
import pytest

from rawlsing_next.pre553_physical_decoder import PhysicalVariable
from rawlsing_next.pre553_carrier_execution import bind_governed_c11_projection, RuntimeObjectCatalog

ROOT=Path(__file__).resolve().parents[2]
MAT=ROOT/"WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py"
PKG=ROOT/"WORKER_RETURNS/EE-P2R6S/04_COMPLETE_WVS7_FROZEN_P2_PROJECTION_AUTHORITY.json"

spec=importlib.util.spec_from_file_location("r6s_mat",MAT); assert spec and spec.loader
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def vars3():
    special=tuple({"kind":"discrete","value":v} for v in (-5,-4,-2,-1))
    return (
      PhysicalVariable(301,"Q291G5","double",None,{},special,{},{}),
      PhysicalVariable(302,"Q291P5","double",None,{},special,{},{}),
      PhysicalVariable(7,"B_COUNTRY","double","ISO 3166-1 numeric country code",{},(),{},{}),
    )

def test_country_authority_and_complete_projection_bind():
    assert m.COORDINATE_AUTH_REF.authority_content_hash=="9e7f98a7ad723743771d6bea39077553d2a3920ac4c077e90720bb9e44da029d"
    fields=m.build_projection_fields(physical_variables=vars3(),row_country_values=(231,704,840),enforce_frozen_dimensions=False)
    p=bind_governed_c11_projection(fields)
    assert len(p.coordinate_slots)==1 and p.coordinate_slots[0].slot.name=="B_COUNTRY"
    assert len(p.weight_slots)==0 and len(p.response_slots)==2 and len(p.routing)==6
    rr={b.respondent_ref.object_id:b.row_ordinal for b in p.row_bindings}
    states={}
    for fact in p.routing:
        states.setdefault(rr[fact.scoped_respondent_ref["object_id"]],set()).add(fact.routing_state)
    assert states=={1:{"ELIGIBLE_APPLICABLE"},2:{"ELIGIBLE_APPLICABLE"},3:{"NOT_ELIGIBLE"}}

def test_country_codes_are_source_owner_exact_and_viet_nam_is_704():
    assert m.REQUIRED_COUNTRY_CODES==frozenset({104,231,364,404,417,434,504,558,608,704,716,762,862})
    assert m.SOURCE_OWNER_COUNTRY_CODE_TO_LABEL[704]=="Viet Nam"
    assert m.SOURCE_OWNER_COUNTRY_CODE_TO_LABEL[231]=="Ethiopia"

def test_no_fuzzy_or_duplicate_source_identity():
    alias=tuple(PhysicalVariable(v.ordinal,"COUNTRY" if v.name=="B_COUNTRY" else v.name,v.storage_type,v.variable_label,v.value_labels,v.missing_declarations,v.display_metadata,v.topology_metadata) for v in vars3())
    with pytest.raises(ValueError,match="B_COUNTRY"):
        m.build_projection_fields(physical_variables=alias,row_country_values=(231,),enforce_frozen_dimensions=False)
    dup=vars3()+(PhysicalVariable(700,"B_COUNTRY","double",None,{},(),{},{}),)
    with pytest.raises(ValueError,match="must resolve uniquely"):
        m.build_projection_fields(physical_variables=dup,row_country_values=(231,),enforce_frozen_dimensions=False)

def test_runtime_package_is_exact_p2f2_lock2_catalog():
    pkg=json.loads(PKG.read_text())
    assert pkg["lock2"]==m.LOCK2
    assert pkg["counts"]=={"authorities":6,"predicates":11,"queries":3,"discovery_authorities":1,"candidates":46}
    cat=RuntimeObjectCatalog.from_documents(
      authority_documents=pkg["authority_documents"],
      predicate_documents=pkg["predicate_documents"],
      query_documents=pkg["query_documents"],
      discovery_authority_documents=pkg["discovery_authority_documents"],
    )
    assert len(cat.predicates)==11 and len(cat.queries)==3 and len(cat.discovery_authorities)==1


def test_backend_contract_and_current_runtime_support_are_source_inert():
    import importlib
    backend=importlib.import_module("rawlsing_next.ee_p2x_darwin_stage_backend")
    assert backend.BACKEND_CONTRACT=="RAWLSING_EE_P2X_DARWIN_STAGE_BACKEND@1.0.0"
    support_path=ROOT/"WORKER_RETURNS/EE-P2R6S/SUPPORT/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py"
    s=importlib.util.spec_from_file_location("r6s_lits_support_test",support_path); assert s and s.loader
    sm=importlib.util.module_from_spec(s); s.loader.exec_module(sm)
    package=sm.materialize_runtime_package()
    assert package["runtime_catalog_identity"]=="5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02"
    assert package["active_binding"]=="a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308"
    assert package["runtime_release"]=="192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f"
    assert package["candidate_count"]==50 and package["query_role_executions"]==77

def test_backend_exhaustively_handles_ready_reducer_stages_and_preserves_c_laws():
    import importlib
    backend=importlib.import_module("rawlsing_next.ee_p2x_darwin_stage_backend")
    reducer=json.loads((ROOT/"WORKER_RETURNS/EE-P2X-CONTINUATION-REDUCER-R1/01_CONTINUATION_STATE_MACHINE.json").read_text())
    ready=set()
    for cell in reducer["cells"].values():
        for sid,record in cell["stages"].items():
            if record[0]=="READY__RUN_LOCALLY":
                ready.add(sid)
    for sid,record in reducer["final_stage"]["stages"].items() if isinstance(reducer["final_stage"].get("stages"),dict) else []:
        if record[0]=="READY__RUN_LOCALLY": ready.add(sid)
    ready.add("S17_FINAL_COMPLETENESS_AND_VERIFICATION")
    assert ready==set(backend.HANDLERS)
    source=Path(backend.__file__).read_text()
    assert "C_NONQUALIFYING__S02_C11_REACHABILITY__FROZEN_CACC1_STREAM_OMITS_Q310_Q311_REQUIRED_BY_F02_COMPOSITE_PROJECTION" in source
    assert 'if s.source=="WVS7" and s.candidate=="C"' in source
    assert "--fresh-replay" in source and "subprocess.run" in source
    assert "performance cannot precede parity PASS" in source
    assert "PURE_B_NO_CACHE" in source
    assert "driver-bound final verifier" in source
    assert "ranking_or_selection" in source
    assert "historic_product_substitution" in source and '"product_identity":product' in source
    assert "LITS_PRODUCT" not in source[source.index("def _s05"):source.index("def _s06")]
