# Bounded omission challenge

**Search ID:** `ZAK1057:QSM:SEARCH:01`.
**Cuts:** candidate `0d90c2470b0b476dcb74ce157b706b10f8392f4f`; protected `6a5c12f04323d74001f9632063ec907f4fc4468e`.
**Method:** one targeted `git grep` for existing binding/ref transport, plus `semantic_input_refs=` producers.

**Pattern:** `binding_root|binding_receipt|SelectedQsmRouteResult|projection_binding_receipt|semantic_input_refs=`

**Result:**
- `binding_root` appears only in the candidate reader (`L311`) and its static test (`L179`); no non-test consumer.
- `projection_binding_receipt` and `repository_executor_binding_receipt` are generic projection/repository mappings produced by Route B (`pre553_carrier_execution.py` L194-L221; `pre553_route_b_production.py` L529/L605/L623). They are not selected-QSM bindings and are not populated with QSM identity.
- No protected `semantic_input_refs=` producer passes a selected-QSM binding. The issued workload builds Batch units with `(r.predicate_ref, workload.decision_ref)` (`pre553_issued_workload.py` L324-L327).
- The non-test issued-workload caller `pre553_native_workload_binding.py` (`L433`) was not named in the return; it supplies no QSM binding.

**Conclusion:** the omission challenge does not overturn the return. It strengthens the distinction: the gap is a missing canonical selected-QSM exact ref/carrier, not a missing generic Batch slot. Dynamic/external callers and differently named artifacts are not excluded; no global absence is claimed.
