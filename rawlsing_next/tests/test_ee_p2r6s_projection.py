from __future__ import annotations
import importlib.util, json
from pathlib import Path
import pytest

from rawlsing_next.pre553_physical_decoder import PhysicalVariable
from rawlsing_next.pre553_carrier_execution import bind_governed_c11_projection, RuntimeObjectCatalog

ROOT=Path(__file__).resolve().parents[2]
MAT=ROOT/"WORKER_RETURNS/EE-P2R6S/08_WVS7_FROZEN_P2_PROJECTION_MATERIALIZER.py"
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

def test_identity_probe():
    raise AssertionError("R6S_IDENTITIES="+json.dumps(m.authority_identity_receipt(),sort_keys=True))
