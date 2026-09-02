# WSC002 — GT0 CENTRAL INTEGRATION BOUNDED HOSTILE AUDIT RETURN R1

## Terminal

`FAIL__MATERIAL_CANDIDATE_DEFECT__GT0_NOT_READY_FOR_CANONICALIZATION`

Audited candidate:

`0301e7ac123132d948561af2612a17bd7eb217ac`

Audit branch starting head / instruction evidence:

`8028353c289875bb5d9993457362759932235535`

No PRE-MAIN or `main` movement was performed. FIELD FORGE R2 was not reopened. No positive actor authority was invented. No physical architecture was selected.

## Bounded execution result

The exact integrated GT0 baseline was reconstructed from the candidate source and executed against its integrated API surface. The expected happy-path sequence is reproducible and deterministic:

`GT0_F0_BIND: PASS`
`-> GT0_PREFF: PASS`
`-> GT0_FIELD_FORGE_INGRESS: PASS`
`-> GT0_FIELD_FORGE_TO_PREV3: UNDEFINED_FOR_OBJECT`
`-> GT0_PREV3_TO_V3: BLOCKED_COMPARATOR_ANCESTRY`
`-> GT0_V3_TO_V2: BLOCKED_NAMED_AUTHORITY_REQUIRED`

The reconstructed focused harness passed its protocol/D/integrated happy-path checks, including deterministic replay, owner conservation, permission non-widening, PRE-V3 abstention, and local zero-effect/nonrender booleans.

The connector surface does not expose a synchronous checkout/pytest executor for this private repository. Therefore the exact full inherited pytest subset was not runnable as a repository checkout here. I inspected the exact inherited contract implementations/tests implicated by the handoff and compared the candidate against PRE-MAIN. The candidate adds GT0 glue rather than modifying those current modules. This limitation does not affect the material candidate defects below: both are directly established from the integrated candidate code and its protocol contract.

## Checks

1. **Exact F0 / current-J ceiling — PASS.** The bound row is exactly `cssu.r1.afrobarometer.r1.005b474d6eb4253cb166`, `MATRIX_GRID`, `Current-versus-past freedoms and equality`, members `pfesol|pfrsay|pfrass|pfrvot|pfreql|pfpsaf`, row SHA-256 `ef21f9f95c26e7ddd833401618e70cddcebdb7250ba7605de97a3387665843c6`. Governing J01A evidence disposes it as `CURRENT_J_CANDIDATE` and explicitly does not adjudicate executable J. Candidate permission remains `REFERENCE_ONLY__NO_RESPONDENT_VALUES__NO_EXECUTABLE_J`.
2. **FIELD FORGE semantic promotion/reownership — baseline PASS.** The happy path copies producer identity/authority/scope/replay and mints no FIELD/CAPITAL/HEGEMONY/HOMOLOGY/PRESSURE/MECHANISM meaning.
3. **PRE-V3 admission firewall — PASS.** F0 never enters current I04/P06 or M1 as `EmpiricalFact`, `StructuralEmpiricalAdmission`, or direct basis. Baseline is `UNDEFINED_FOR_OBJECT`; named structural request is `BLOCKED_EXPLICIT_AUTHORITY`; no V554/V555 object is fabricated and `ZERO_V556_OBJECTS` is explicit.
4. **Owner / permission / deterministic replay — happy-path PASS.** One semantic owner survives the thread, permission remains a subset of the source ceiling, and the whole-thread hash is deterministic.
5. **Typed-negative conservation — FAIL.** Concrete candidate defect below.
6. **PRE-V3→V3 accepted-firewall integration — FAIL.** Concrete candidate bypass below.
7. **V3→V2 actor-safe/render integration — FAIL.** Concrete candidate bypass below.
8. **Candidate-caused inherited-module mutation — none found.** The relevant accepted PRE553/V3/M6/render modules are not modified by the GT0 candidate; the defect is instead that E/F do not actually traverse the accepted seams they claim to validate.

## Material defect 1 — PRE-FF → FIELD FORGE typed-negative handoff is internally inconsistent

File:

`rawlsing_next/wsc_gt0_field_forge_ingress.py`

The function constructs its output envelope with:

`status=source.status`

but constructs the enclosing `GT0StageReceipt` with:

`status=GT0StageStatus.PASS`.

`GT0StageReceipt` correctly requires receipt status to equal output-envelope status. Therefore any lawful non-PASS typed upstream state — for example `DENIED`, `UNRESOLVED`, `NONCOMPARABLE`, or `INTEGRITY_FAILURE` — reaches FIELD FORGE with the negative envelope intact and then crashes construction because the wrapper attempts to relabel the receipt `PASS`.

This is a concrete protocol/type mismatch and violates the WSC002 law that typed blocked/denied/unresolved/noncomparable/integrity states remain conserved across handoffs. The happy-path integrated test cannot see it because the bound F0 baseline enters C as PASS.

### Smallest exact repair 1

In `run_gt0_field_forge_ingress(...)`, change only the receipt status assignment from:

`status=GT0StageStatus.PASS`

to:

`status=source.status`

and add one focused hostile regression that supplies a valid non-PASS `GT0SourcePreFFResult` and asserts that the exact typed status survives C without promotion or constructor failure.

No semantic redesign is required.

## Material defect 2 — E/F shadow the expected blocked outcomes instead of binding the accepted V3 and V2 seams

Files:

- `rawlsing_next/wsc_gt0_v3_runtime.py`
- `rawlsing_next/wsc_gt0_v2_mediation.py`

The WSC001 constitution and WSC002 E/F handoffs require the GT0 thread to prove the actual PRE-V3→V3 firewall and actor-safe/render blocking using the accepted current machinery where lawful.

The integrated E module imports only the GT0 protocol. It does not bind `source_backed_positioned_subject_possibility.py` or the accepted `v3_psepf_zero_positive_guard.py`. Instead it creates a GT0-local checkpoint, sets `after = before`, and independently labels the result `BLOCKED_COMPARATOR_ANCESTRY`.

The accepted V3 guard is stricter and separately governed: its production positive-transition registry is exactly empty, guarded learned-world truth has zero actor effect, and callers cannot manufacture a positive authority override. GT0 currently does not traverse or bind that guard; it merely reproduces the expected outcome locally.

Likewise the integrated F module imports only the GT0 protocol plus the GT0-local E result. It does not bind `m6_actor_safe_expression.py` or `render_bounded_expression.py`. Instead it independently returns `actor_claim_created=False`, `rendered_text=None`, and `BLOCKED_NAMED_AUTHORITY_REQUIRED`.

The accepted M6/render machinery already owns the relevant negative boundaries: upstream structural/empirical material is not behavioral authority, situated expression requires named authority, and current positive render-plan authority is blocked. GT0 currently does not prove those actual seams; it shadows them.

This is material because the audit target is an executable **whole-spine** Golden Thread, not merely a set of adapters that emit the same status strings. A future divergence in the accepted V3/M6/render contracts could leave GT0 green while the real seam fails.

### Smallest exact repair 2

Do not add positive authority or fabricate an actor/PSEPF/render plan. Narrowly bind the existing negative surfaces:

1. In E, derive/validate the GT0 zero-positive disposition against the accepted current V3 guard contract/zero-positive authority state rather than minting the conclusion solely inside the GT0 wrapper. Preserve the baseline fact that no exact positioned-subject possibility/comparator exists; do not manufacture one to call the guard.
2. In F, bind the current M6/render negative-only authority surfaces so the terminal blocker is demonstrated by current actor-safe/render law, not only by GT0-local booleans. No actor-safe claim entry, admitted semantic plan, renderer/model call, or causal return may be created.
3. Add focused integration assertions that E/F are bound to those current contracts and that the same blocked terminal is reached with zero V3 mutation and zero render/model invocation.

This is a binding repair, not a spine redesign.

## Disposition

The integrated baseline demonstrates useful conservation behavior, but the candidate cannot be canonicalized from this audit state because a typed negative state can break the C handoff and because the E/F whole-spine proof bypasses the current authoritative seams it is supposed to validate.

`NEXT_ACTION__APPLY_ONLY_THE_TWO_BOUNDED_REPAIR_SETS__RERUN_THIS_EXACT_AUDIT__DO_NOT_ADVANCE_PRE_MAIN_OR_MAIN`
