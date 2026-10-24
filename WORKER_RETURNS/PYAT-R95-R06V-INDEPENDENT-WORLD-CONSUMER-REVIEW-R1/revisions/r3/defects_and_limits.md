# R95-R06V R3 exact defects and limits — REVISE

Verdict: **REVISE**. Three exact R3 boundary failures remain despite the
author 14/14 suite and the five prior probe passes. Repairs 2 (actual temporal
payload dependence) and 3 (cross-unit linkage refusal) pass independent
successor controls. Repair 1 (actual P41/E04 execution) is incomplete and
repair 4 (competent FF admission) is bypassable.

## Defect 1 (blocking): forged P41 runtime mints actual execution

`_execute_p41_world` trusts `R05ActualExecution.p41_runtime` as a caller string,
prepends it to `sys.path`, imports `bootstrap`, `p41_service.P41Service` and
`product.world.SelectedWorldCatalog` with no packet/commit/content verification,
and then imports/uses whatever service is found. Optional `claimed_receipts` are
only compared to the output of that same forged service.

Successor `S1` built a fake runtime whose `P41Service.progressive` returned the
genuine canned T0/T1 receipts; the wrapper returned `R05_WORLD_SELECTED_VIEW`
with `ACTUAL_R05_TO_P41_VIEW`. No actual pinned P41/N9/N10W/E04 code ran. A
self-consistent canned runtime therefore becomes authenticated output, exactly
the forbidden forged-runtime path.

**Missing function:** exact runtime identity/content pin or internal
construction of the accepted actual owner from a host-retained invariant;
reject caller-supplied/forged runtime modules. Do not weaken to class-name/hash
checks on the receipt itself.

## Defect 2 (blocking): subject-selected coordinator original emitted

`R05ActualExecution.coordinator_original_ref` is copied into
`_world_block["r05_binding"]` and then into the accepted view without any
independent original check. `S3` replaced it with
`ExactRef("FORGED_COORDINATOR_ORIGINAL", ..., "a"*64)` and still received an
accepted view; the returned `coordinator_original_ref` was the forged value.

The learned/step checks are also self-referential: `_execute_p41_world` compares
`actual.learned_consumer` to `request.learned_consumer`, both caller-supplied,
and the step hash to that same learned result. No independently retained R05/R03
coordinator original or actual-execution attestation is resolved.

**Missing function:** bind/verify the exact coordinator original and learned/
step originals against the accepted R05/R03 host-retained original; refuse a
subject-selected or mismatched original. Do not emit the execution-provided ref
as authentication.

## Defect 3 (blocking): forged real-type FF admission accepted by joined wrapper

`select_joined_world_view` validates only
`isinstance(StructuralEmpiricalAdmission)`, `typed_state ==
ADMITTED_FOR_EXACT_STRUCTURAL_USE`, and
`target_use == STRUCTURAL_MEDIATION_INPUT`. It does not check source universe,
structural field identity, admission authority, issuance context, target-use
permission, focal proposition, authority closure, or interpretation evidence.
`S6` built an arbitrary real-type admission with arbitrary authority/content and
the joined wrapper returned `SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER` for a
CONTEXT field.

The R05 and simple wrappers do check source/field, but compare
`request.source_universe_ref`/`field.field_ref` (`ExactRef`) to
`admission.source_universe_refs`/`structural_semantic_identity_refs`, which
canonicalize to `MappingProxy` dicts. A genuine canonical admission therefore
also fails (`FF_STRUCTURAL_ADMISSION_SOURCE_MISMATCH` in `S2`); the rejection is
a representation mismatch, not actual issuance/authority validation. The joined
wrapper is the hidden easier bypass.

**Missing function:** canonical ref comparison plus actual competent FF
admission issuance/authority closure verification (source, field, authority,
target-use permission, interpretation/admission evidence) consistently in all
public wrappers; otherwise typed UNAVAILABLE/refusal. Preserve the declared
direct STRUCTURAL synthetic positive; do not issue F5/F6/F7 science.

## Retained corrections and positives

- Author R3 suite: 14/14 passed under the reviewer harness.
- Prior R06V probes: 5/5 passed.
- `S4`: equal actual consumer payload with distinct clocks/hashes returns
  `R05_TEMPORAL_PAIR_NOT_CONSUMED`; actual route/N10W change positive, cold
  current/as-of, revocation and restore remain.
- `S5`: genuine actual R05->P41 positive, hostile callback refusal, and exact
  view-hash restore pass.
- Cross-unit label-only pooling returns `CROSS_UNIT_LINKED_QUERY_UNAVAILABLE`
  in all three public wrappers; no invented linked-query method.
- Two fields affect the same actual route/assertion; actual N10E/N10W/E04
  positive, cold replay and J42/N10E positives remain.
- Only the two authorized R06 code paths differ from startup; accepted
  R03/R04/R05/R08/native/FF/temporal/service/evaluator bodies unchanged. No
  candidate repair or new R09 service.

## Limits / NOT_REACHED

Sourcefree TEST_ONLY local trusted host only; no source respondent access. No
cryptographic/R09 isolation. The reviewer does not treat the author's
"host-retained" convention as authentication because public requests accept
forged runtime and original inputs and mint output. Original F7 measured waves,
original 35/1890/F6/F8, source/science, F5/F6/F7 issuance, CI/prod, N11/N12,
Sorok and J52/W52 remain held/NOT_REACHED. Temporal evidence is synthetic
modeled-rule software evidence, not original F7 issuance. No self-adoption,
production merge or R05 wake.
