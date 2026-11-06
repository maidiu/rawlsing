import json
from rawlsing_next.tests.test_pre553_empirical_query import _build_source, _query_authority, _registry
from rawlsing_next.tests import c1_at08_at13_fixture as fx
from rawlsing_next.tests.test_l01_reviewed_progressive_world import _progressive_prefix
from rawlsing_next.tests.l01_evidence_world_fixture import admit_readers
from rawlsing_next.pre553_universal_world_binding import progressive_source_rows_identity, ProgressiveWorldRequest, progressive_world_view
from rawlsing_next.pre553_universal_evidence_binding import _value_bearing_leaves, _leaf_semantic_ref, _actual_condition_identities
from rawlsing_next.pre553_empirical_objects import canonicalize
from rawlsing_next.pre553_evidence_world_consumer import configure_evidence_world_context

tag='ord00'
rows=[{"id":f"R{i}","responses":{"X":str(i%2),"Y":"1","O":"AB"}} for i in range(8)]
source=_build_source(tag,rows,question_namespace=tag,
    risk_sets={"R":{q:{row["id"] for row in rows} for q in ("X","Y","O")}})
qauth=_query_authority(tag+"-query"); registry=_registry(source,qauth)
model=fx.make_model_rule(source["universe"].ref,tag); pairing=fx.make_pairing_authority(tag)
conds=(("X","1"),("O","AB"))
prefixes=tuple(_progressive_prefix(source,qauth,registry,model,"Y",conds[:d],f"{tag}-{d}",pairing) for d in (1,2))
conditions=tuple((source["qrefs"][q],v) for q,v in conds)
world={"source":source,"release_ref":source["release_ref"],"risk_refs":{"R":source["risk_refs"]["R"]},
       "rows_hash":progressive_source_rows_identity(source["repo"],source["release_ref"]),"publication":"2026-03-01"}
readers,resolver,bindings=admit_readers(prefixes,world)
out={"tag":tag,"requested_order":[list(c) for c in conds],"prefixes":[]}
for i,(b,reader) in enumerate(zip(bindings,readers)):
    leaves=_value_bearing_leaves(b.predicate)
    leaf_order=[canonicalize(_leaf_semantic_ref(l)).get("object_id") for l in leaves]
    bind_order=[c.empirical_coordinate_ref.object_id for c in b.consumer_query.conditioner_bindings]
    actual=_actual_condition_identities(b)
    actual_order=[a["leaf_semantic_ref"].get("object_id") for a in actual]
    old_zip_wrong=any(canonicalize(_leaf_semantic_ref(l))!=canonicalize(c.empirical_coordinate_ref.as_dict())
                      for l,c in zip(leaves,b.consumer_query.conditioner_bindings))
    out["prefixes"].append({"prefix_index":i,"conditioner_count":len(bind_order),
        "canonical_leaf_order":leaf_order,"requested_binding_order":bind_order,
        "orders_differ":leaf_order!=bind_order,"actual_association_order":actual_order,
        "association_matches_requested":actual_order==bind_order,
        "old_positional_would_mismatch":old_zip_wrong,
        "request_mismatch_reason":b.mismatch_reason(reader.request),
        "resolved_state":reader.result.result_state,"resolved_denominator":reader.result.denominator})
handle=configure_evidence_world_context(target_ref=source["qrefs"]["Y"],conditions=conditions,
    prefixes=prefixes,world_empirical=world,evidence_readers=readers)
view=progressive_world_view(ProgressiveWorldRequest(handle,"T0"))
out["view_state"]=view.state; out["view_reason"]=view.reason_code
out["n10w"]=None if view.n10w is None else {
  "state":view.n10w.get("world_conditioned_state"),
  "prefix_count":len(view.n10w.get("world_conditioned_prefixes") or []),
  "prefix_cells":[{c["cell"]:c["raw_numerator_support"] for c in p["native_material"]["source_balance_reads"][0]["all_alternatives"]}
                  for p in view.n10w.get("world_conditioned_prefixes") or []]}
print(json.dumps(out,indent=2,sort_keys=True))
