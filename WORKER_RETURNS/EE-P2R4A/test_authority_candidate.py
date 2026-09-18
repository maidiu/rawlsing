import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def load(n): return json.loads((ROOT/n).read_text(encoding="utf-8"))
def canon(v): return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def check(o,k): assert hashlib.sha256(canon(o["identity_material"])).hexdigest()==o[k]
def test_content_addresses_and_links():
 r=load("02_RESPONDENT_BINDING_COMPATIBILITY_AUTHORITY.json"); g=load("03_PARENT_CHILD_GRAMMAR_COMPOSITION_AUTHORITY.json"); d=load("04_DERIVED_PREDICATE_AUTHORITY_CONTRACT.json"); s=load("05_PUBLIC_PREDICATE_SUCCESSOR_AUTHORITY_CANDIDATE.json")
 check(r,"authority_content_hash"); check(g,"authority_content_hash"); check(d,"contract_content_hash"); check(s,"authority_candidate_content_hash")
 assert g["identity_material"]["respondent_binding_compatibility_ref"]==r["candidate_ref"]
 assert d["identity_material"]["composition_authority_ref"]==g["candidate_authority_ref"]
 assert s["identity_material"]["derived_predicate_contract_ref"]==d["candidate_ref"]
def test_exact_identity_preservation():
 m=load("01_F02_PREDICATE_DIALECT_SEMANTICS_MATRIX.json"); s=load("05_PUBLIC_PREDICATE_SUCCESSOR_AUTHORITY_CANDIDATE.json")
 expected=["c9a0c8106d457bba7e3f3f5abb7ee7fb98482bd86af629d860e4a904ad58456a","78dbd1a899fe43ac2e2ca6985ea0eccb086989fa2c4315fa518524e7ba94a6df","c4d2dd827326b6ff29f3c02382c36fa33c47c6227bfbf8c8053c11e1089923ca","69dc59f79014a7c17190ca658e193a004e167c322c7f713f4540882fb980feb8","f63d6121776500912342ab377178a15fcf6fabf7071864f4f413d95babb43849","a6494153b4defeb13e1658b73eead7c5df6e25847708c770dad5f42142492c7d"]
 assert m["exact_scope"]["selector_predicate_hashes"]==expected
 assert s["identity_material"]["exact_frozen_inputs"]["f02"]["selector_hashes"]==expected
 x=s["identity_material"]["exact_frozen_inputs"]["d02"]; assert (x["candidates"],x["roles"],x["K"],x["J"])==(50,77,3,2)
 assert s["identity_material"]["preservation_contract"]["b12_predicate_exactrefs"]=="PRESERVE_ALL"
def test_refinement_not_global_equivalence():
 r=load("02_RESPONDENT_BINDING_COMPATIBILITY_AUTHORITY.json")["identity_material"]; g=load("03_PARENT_CHILD_GRAMMAR_COMPOSITION_AUTHORITY.json")["identity_material"]
 assert r["semantics"]["global_equivalence"] is False
 assert r["semantics"]["relation"]=="CHILD_BINDING_REFINES_PARENT_BINDING_WITHIN_EXACT_BOUND_SCOPE"
 assert g["permitted_mixed_composition"]["ast_operation"]=="AND"
 assert g["permitted_mixed_composition"]["other_boolean_operations"]=="NOT_GRANTED_FOR_MIXED_GRAMMAR"
 assert g["fail_closed"] is True
def test_derived_authority_explicit():
 d=load("04_DERIVED_PREDICATE_AUTHORITY_CONTRACT.json")["identity_material"]
 assert d["first_input_inheritance_for_mixed_composition"]=="FORBIDDEN"
 assert d["deterministic_construction"]["grammar_authority_ref"]==d["composition_authority_ref"]
 assert d["output_identity_law"].startswith("DERIVED_PREDICATE_IS_NEW_CONTENT_ADDRESSED_OBJECT")
def test_direct_interpretation_preserves_ast():
 m=load("01_F02_PREDICATE_DIALECT_SEMANTICS_MATRIX.json"); law=m["interpretation_law"]
 assert law["direct_without_predicate_rewrite"] is True and law["predicate_exact_ref_preserved"] is True
 assert law["operator_semantics"]=="TRUE_IFF_SAME_ROW_GOVERNED_EVENT_HAS_EXACT_NATIVE_VALUE"
 assert law["missing_is_false"] is True and "CROSS_RELEASE_INTERPRETATION" in m["fail_closed_negative_cases"]
def test_generic_contract_has_no_source_selector_special_case():
 s=load("05_PUBLIC_PREDICATE_SUCCESSOR_AUTHORITY_CANDIDATE.json"); generic=json.dumps(s["identity_material"]["generic_runtime_requirements"],sort_keys=True).lower()
 for forbidden in ("lits","q310","q311","f02","d02","c9a0c8106d457bba7e3f3f5abb7ee7fb98482bd86af629d860e4a904ad58456a"): assert forbidden not in generic
 assert s["identity_material"]["generic_runtime_requirements"]["default_on_missing_authority"]=="FAIL_CLOSED"
 assert s["identity_material"]["preservation_contract"]["existing_pre553_same_grammar_same_binding_behavior"]=="UNCHANGED"
