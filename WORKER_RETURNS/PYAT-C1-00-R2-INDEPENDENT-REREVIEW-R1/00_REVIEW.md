# PYAT C1-00 R2 — independent contract / oracle rereview — R1

Disposition: `CHANGES_REQUIRED`

Terminal: `C1_00_R2_INDEPENDENT_REREVIEW_COMPLETE__HQ_ADJUDICATION_REQUIRED`

Reviewed return:
`a94649020346383e9d9cd18cc2b5a448e0a09ad7`

Reviewer commission:
`9e47d9d9db5c45c7073ce5608bcc8bcf461f43ca`

R2 commission:
`00b7091190505c0b41feaf0c45a29a791bab0cb5`

Prior independent review:
`8baa2e1e3a6f4f96311fbd660b65933fb4aff6c4`

Implementation baseline:
`b3b2fa13049513078c301a1f6574b661fcf390c5`

This rereview is documentary/source-free only. It does not implement or execute C1-01, edit production code/tests, access raw survey sources, or create semantic/comparability/model/pooling/survey authority.

## 1. Scope / terrain check

The exact R2 commission-to-return compare `00b7091...a946490` is 15 commits ahead, 0 behind, with 13 changed files. Every changed file is inside one of the two R2-authorized return terrains:

- `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/**`
- `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/**`

No production code or production test changed in the reviewed worker return.

Raw survey source reads by this reviewer: **0**.

## 2. Defect A — value-bearing condition relation: PASS

R2 replaces the prior co-custody witness with explicit source-free value-bearing fixture material:

- subject preimages for `POSITION=P1`, `POSITION=P2`, and `ANSWER=yes`;
- exact predicate-leaf preimages for `POSITION==P1`, `POSITION==P2`, and `ANSWER==yes`;
- exact frozen pairing-ground-truth objects;
- a witness schema requiring the full consumer binding, subject preimage material, producer leaf material, exact source/release/time and fixture-only pairing authority.

Independent canonical-JSON/SHA-256 recomputation matches every subject preimage, predicate leaf, pairing object and the witness-schema digest.

Hostile recomputation also closes the prior counterexample:

- subject preimage: `POSITION=P1`;
- producer leaf: `POSITION==P2`;
- semantic ref: equal;
- exact value: unequal;
- frozen P1↔P2 pairing ground truth: absent.

Under the frozen deterministic checks this must reject as `CONDITION_VALUE_RELATION_MISMATCH` before slice construction / consumer invocation. P1 and P2 subject preimages also have distinct exact hashes despite the shared conditioner ID.

No real-source subject↔survey relation is inferred.

## 3. Defect B — complete synthetic authority freeze: FAIL

The good part is real: all eight R2 authority digests independently reproduce from the declared canonical material, and targeted mutations of scope, operation, model algorithm, and pairing set all produce different hashes.

But the frozen PRE553 query authority is not actually fit for the current public I03 owner contract.

R2 freezes `C1-AT07-QUERY` with:

- kind `PREDICATE_GRAMMAR`;
- operation `C1_AT07_QUERY`;
- governed families `EmpiricalPredicate@1.0.0`, `EmpiricalQuerySpec@1.0.0`, `EmpiricalFact@1.0.0`;
- `scope_envelope = {fixture_id, source_family, source_seed, use}`.

Current I03 `rawlsing_next/pre553_empirical_query.py` blob
`03facecf70890bfd13b80418620d274cbcd69d02`
calls `require_positive_authority(... source_universe_ref=universe_ref.as_dict())` for each query authority and each exact universe.

Current authority owner `rawlsing_next/pre553_empirical_authority.py` blob
`ca65a7fd4d52f0c44447434559b1d09412e7aa39`
checks source scope only at `scope_envelope["source_universe_refs"]`; absent scope returns false and the authority fails closed.

Therefore the exact frozen `C1-AT07-QUERY` authority cannot authorize the declared narrow C1-01 I03 path in the ordinary current public route. R2 has frozen a reproducible authority hash, but not a current-owner-usable authority scope.

This is an ordinary documentary correction, not an architectural residual: freeze the exact synthetic universe ref(s) first and include them under owner-native `source_universe_refs`, or explicitly freeze a lawful owner-recognized unrestricted source scope if that is actually intended. Recompute every affected authority ref/hash and downstream oracle ref.

## 4. Defect C — UNKNOWN / UNVISITED / UNRESOLVED separation: FAIL AS FROZEN FIXTURE

The state vocabulary is now correctly separated in prose:

- `UNKNOWN_CURRENTNESS`
- `EXPLICIT_UNKNOWN_UNVISITED`
- `UNRESOLVED`
- `UNAVAILABLE`
- `NO_CURRENT`
- `CONFLICTING_CURRENT_SELECTION`

and current B5 does contain `UNKNOWN_CURRENTNESS`.

However R2 freezes the specific UNKNOWN fixture owner as:

`LearnedProductLifecycleStore.resolve_selection_exact`

with setup: a lawful selection key for which no current selection/no-current receipt exists.

The current actual owner is `LearnedProductLifecycleExecutor` in
`rawlsing_next/pre553_learned_product_lifecycle.py` blob
`a11c9eb73abab9be118ef4f0b6e325e676059f27`.

For an unselected key, `resolve_selection_exact(selection_key_ref, selection_receipt_ref)` first compares the supplied receipt with `_selection_index.get(...)`, which is `None`; because the public method requires an `ExactRef`, the mismatch raises:

`currentness requires the exact current selection/no-current receipt`

before the function can reach its terminal `UNKNOWN_CURRENTNESS` branch.

The owner-native reachable witness for an unselected key is instead `current_selection_receipt_ref(selection_key_ref)`, which explicitly raises `LearnedProductLifecycleError("UNKNOWN_CURRENTNESS")` when no selection/no-current receipt exists.

So the semantic distinction is repaired, but the frozen fixture names the wrong current owner path and does not yet constitute an executable/documentarily exact UNKNOWN oracle.

Minimal correction: freeze the exact reachable B5 method/setup/expected exception for `UNKNOWN_CURRENTNESS`, keeping it distinct from adaptive unvisited and empirical unresolved.

## 5. Defect D — exact possibility slice projection: FAIL ON EVIDENCE IDENTITY PREIMAGE

Most of the R2 projection repair is correct and independently reproducible:

- `C1_POSSIBILITY_SLICE_PROJECTION@1` schema hash independently recomputes to
  `c00e038dd2c1177bfc7842f12febef7b3e30b92bc421df244e2a8e3c4a20b17a`;
- geometry binds producer fact/query/predicate/witness;
- target component/topology/domain material is retained;
- risk-set and denominator member refs are retained;
- RAW / governed-weighted measure material is separated;
- cell numerators and exact fractions are fixed;
- `raw_support` is unambiguously `EmpiricalFact.raw_denominator_support`;
- AT07 forward/reverse geometry is correct.

The remaining exactness defect is the frozen `evidence_ref` law:

> `sha256 identity over the complete PossibilitySliceEvidence payload plus contract id...`

The current `PossibilitySliceEvidence` object has `evidence_ref` as one of its fields and has no owner-native `material()`/derived-ref method. Taken literally, hashing the **complete payload** includes the value being derived and is circular. If implementations silently omit `evidence_ref`, they are relying on an unstated convention rather than the frozen oracle.

This matters because R2 also makes `constructed PossibilitySliceEvidence.evidence_ref` a composition determinant.

Minimal correction: freeze one explicit noncircular identity preimage, e.g. contract id plus all evidence fields **except** `evidence_ref`, in exact canonical shape/order law, and freeze/recompute at least the two AT07 expected evidence refs. Then denominator-member or geometry changes can be independently shown to reidentify rather than only asserted.

## 6. Defect E — determinant / replay / invalidation closure: PASS AT DOCUMENTARY GRAIN

R2 now explicitly includes as mandatory direct determinants:

- condition-value witness ref/hash;
- subject-condition preimage refs;
- producer predicate-leaf refs/projections;
- pairing ground-truth refs;
- pairing/comparability authority refs;
- risk/denominator member refs;
- target topology/domain material;
- exact constructed slice evidence ref;
- projection schema hash.

The composed-result identity rule includes the relation determinants; the full-fresh-process replay input list explicitly requires the witness/preimage/leaf/pairing material; replay omitting those inputs cannot claim `FULL_COMPOSITION_FRESH_PROCESS_RECOMPUTE`.

The relation-only mutation oracle is therefore closed at documentary grain: with other determinants fixed, replacing the exact relation/witness determinant changes canonical composed material and must reidentify. For lifecycle-governed families, R2 correctly leaves selective invalidation to existing B5 edges and does not impose B5 universally on direct empirical composition.

This PASS does not cure the separate defect-D ambiguity in how the slice `evidence_ref` itself is derived.

## 7. Preserved prior holdings

R2 does not weaken the previously accepted holdings:

- exact source universe + release nonaliasing;
- exact target topology/domain/component custody;
- exact risk/eligibility/denominator/member identity;
- RAW versus governed-weighted measure/design/estimand distinction;
- recursive immediate-parent ancestry and positive-handoff/full-coverage separation;
- replay-grade separation;
- direct versus learned/adjudicated anti-bypass law;
- narrow future C1-01 write terrain;
- AT07 arithmetic.

Independent arithmetic remains:

- total: `54 + 6 + 8 + 32 = 100`;
- forward P1 denominator: `54 + 6 = 60`; `P(yes|P1)=54/60=9/10`;
- forward complement: `6/60=1/10`;
- reverse yes denominator: `54 + 8 = 62`; `P(P1|yes)=54/62=27/31`;
- reverse P2: `8/62=4/31`.

No candidate output was used.

## 8. Additional documentary inconsistency

`worker_return.json` lists `family_binding_manifest.json` in `changed_blobs`, while the exact R2 commission-to-return compare shows that file was not modified. The R2 `00_RETURN.md` correctly says it was not modified. This does not independently determine the disposition, but the worker return should be made internally exact when the packet is corrected.

## 9. Final disposition

The five mandatory R2 correction classes are not all closed.

- A: PASS
- B: FAIL
- C: FAIL AS FROZEN FIXTURE
- D: FAIL ON IDENTITY PREIMAGE
- E: PASS

The failures are bounded documentary contract defects with concrete current-owner corrections. They do not establish an unrepresentable essential grain, changed required semantics, or missing authority that warrants `TYPED_RESIDUAL` / Astra escalation.

Therefore:

`CHANGES_REQUIRED`

C1-01 must remain blocked.

`C1_00_R2_INDEPENDENT_REREVIEW_COMPLETE__HQ_ADJUDICATION_REQUIRED`
