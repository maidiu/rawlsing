# FFIF007 — MINIMAL SUFFICIENT SET CONTRACT

## 1. Universe and coverage

Let finite frozen `U = {A1...An}` and claim bundle `R(C) = {r1...rm}`.

Each AOS produces a componentwise matrix over R(C):

`PASS_WITHIN_CITC | HARD_ZERO_FAIL | BOUNDED_LOSS_FAIL | UNDEFINED | INSUFFICIENT_SUPPORT | INVALID | UNRESOLVED`.

A set's coverage is not majority vote. For each `ri`, at least one valid member must supply an answer within CITC, and cross-object composition must obey the frozen bundle contract.

## 2. Sufficient set

`S subseteq U` is `SUFFICIENT_SET_FOR_C` iff:

1. the union of lawful member interfaces covers every `ri` within CITC/support;
2. no required answer depends on an object outside S at query time;
3. any cross-member join, transform, or reconciliation was preregistered and separately authorized;
4. inconsistent same-slot answers are resolved only by the frozen CVCR/uncertainty law, not selection of the preferred result;
5. every member is independently valid for its assigned slot;
6. the set as a set passes applicable hostile/nuisance/holdout tests.

## 3. Minimality

S is inclusion-minimal iff S is sufficient and every proper subset is insufficient. Cardinality alone is not enough; two equal-size sets can differ in commitments.

After enumerating all inclusion-minimal sets, apply set-level commitment dominance:

`S1 SET_DOMINATES_C S2` only if S1 supplies the same complete interface with no stronger union of claim-relevant commitments and at least one strict reduction, without illicit fusion.

Report the complete nondominated frontier.

## 4. Multiple minimal sets

If `{configuration, ordinal-neighborhood}` and `{direct-existence, topology}` both lawfully satisfy the same bundle and neither dominates, emit:

`MULTIPLE_NONDOMINATED_MINIMAL_SUFFICIENT_SETS_WITHIN_U`.

This means the bounded engineering problem has more than one empirically lawful minimal architecture. It does not mean the objects agree, the sets are semantically interchangeable, or one may be selected by theory prestige. Engineering criteria may select an implementation only after the full frontier is preserved.

## 5. No sufficient set

`NO_SUFFICIENT_SET_WITHIN_U` means the current lawful design universe cannot preserve the complete bundle. It can motivate claim splitting, new authority, or new object design. It does not falsify the empirical proposition and does not permit lowering CITC.

## 6. Search law

Because U is finite, exact subset enumeration is conceptually defined. An implementation may use deterministic pruning by ex-ante dominance and coverage impossibility, but must prove pruning cannot remove a minimal set. Heuristic first-found search is insufficient for a uniqueness claim.

## 7. Receipt fields

- `comparison_claim_hash`
- `U_hash`
- `AOS_hashes[]`
- `invariant_coverage_matrix_ref`
- `composition_rules_ref`
- `all_inclusion_minimal_sets[]`
- `set_commitment_vectors[]`
- `set_dominance_relations[]`
- `nondominated_frontier[]`
- `hostile_nuisance_holdout_refs[]`
- `engineering_selection` separately typed, if any
- `unresolved_states[]`
- `supersession`

## 8. Forbidden shortcuts

- assuming the FFX002 A/B/C set is sufficient;
- counting more variants as stronger evidence;
- calling a set minimal because each member adds some utility;
- hiding a fusion transform inside set union;
- reporting only the first minimal set found;
- averaging hard-zero invariant failures across members.
