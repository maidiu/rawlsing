# HQ218 — H-D/F8 AUTHENTICATION FINAL HOSTILE REREVIEW — R1

**Disposition: `ACCEPT_HD_F8_AUTHENTICATION_REPAIR__READY_FOR_HQ_ADOPTION`**

**Terminal: `HQ218_HD_F8_AUTHENTICATION_FINAL_REREVIEW_RETURNED__HQ_DECISION_REQUIRED`**

Review commission:

`agent/reviewer-pyat-hq218-hd-f8-authentication-final-rereview-r1 @ e6185d4fd6ce9a1708cb54242ba247fe494ec329`

Exact candidate:

`agent/rabochii-pyat-hq217-hd-f8-binding-authentication-repair-r1 @ cff8449e1752f816ad82d1b18626e2290913f8b9`

Code-bearing repair:

`d588f709a8b923082d5d458ed6a671e2ae57fb76`

Prior hostile disposition:

`HD_F8_REPAIR_AUTHORITY_OVERREACH @ 6df6c86816a949d02bd91d33b6686ba0de728050`

HQD-216 was read from the exact control object required by the commission:

`e0e7ce0e596e4e5ea7ec96c265ec949b9fe801a2:PYAT_CONTROL_ROOM/26_HQD216_PRODUCTIVE_ADEQUACY_AND_PREV3_EMPIRICAL_GATE_LAW.md`

## Verdict

The HQ215 forged-binding authority bypass is closed at the authority-consuming paths.

The repair is safe for HQ adoption at the commissioned H-D/F8 source-scope binding grain.

The decisive change is not a self-hash or shape check. Every path that can independently assert source eligibility, expose the authoritative admitted set, or delegate into adopted F8 now requires the exact binding request, authoritative applicability receipt, and exact F8 rule, and authenticates by re-deriving the binding from those inputs before using its authority-bearing fields.

A directly constructed, `dataclasses.replace`-modified, copied-id, or self-consistently rehashed binding cannot manufacture eligibility because the presented binding is only the thing being checked; the authority-bearing object subsequently used is the re-derived binding.

## 1. Independent public-surface census

I did not rely on the worker's census.

At candidate `cff8449e...` I independently resolve:

- `__all__`: 28 names;
- exported classes: 3;
- exported module functions: 4;
- public names visible on `ServiceApplicabilityF8SourceScopeBinding`: 14;
- of those 14 public class names, 13 are methods and one is the public dataclass default field `binding_statement`.

The three authority-consuming operations are:

1. `ServiceApplicabilityF8SourceScopeBinding.assert_query_source_admitted`
   - independently returns `admitted: true`;
   - now requires `request`, `receipt`, and `rule`;
   - authenticates first and reads admission/provenance from the re-derived binding.

2. `ServiceApplicabilityF8SourceScopeBinding.expose_unranked_admitted_source_set`
   - independently exposes the admitted set;
   - now requires `request`, `receipt`, and `rule`;
   - authenticates first and returns the re-derived set.

3. `evaluate_bound_positioned_subject_possibility`
   - can reach adopted F8;
   - now requires `request`, `receipt`, `query`, `rule`, and `evidence`;
   - authenticates before admission assertion or F8 delegation.

No fourth positive authority-consuming path was found.

`bind_service_applicability_to_f8_scope` is the lawful constructor from authority.
`verify_service_f8_scope_binding_replay` is the exact re-derivation verifier.
`assert_complete_coverage_from_binding` is a guard only and cannot emit eligibility.
`material`, `as_dict`, and `replay_identity` serialize or identify the value but do not independently assert admission or call F8.

The remaining power-shaped methods refuse.

Nonblocking census precision: the return prose's “14 public methods” is not literally exact. The class has 13 public methods plus the public `binding_statement` data attribute. Likewise the operative refusal set contains eight loud-refusal methods, not nine. The court itself pins the 14 public names mechanically, so this wording error does not create a blind spot.

## 2. Direct-construction / replace forgery

The prior bypass is no longer viable.

The authentication helper:

`_authenticate_binding_against_authority(binding, *, request, receipt, rule)`

requires:
- exact `ServiceApplicabilityF8ScopeBindingRequest`;
- exact adopted `CandidateClassApplicabilityReceipt`;
- exact recognized `PositionedSubjectPossibilityModelRule`.

It calls `verify_service_f8_scope_binding_replay`, which calls the lawful constructor again:

`bind_service_applicability_to_f8_scope(request=request, receipt=receipt, rule=rule, ...)`

and compares both replay identity and complete material.

Therefore a forged:
- admitted source tuple;
- provenance row;
- coverage;
- requested source;
- rule hash;
- receipt id/replay string;
- binding ref;
- binding request ref;

cannot become authoritative merely by being internally self-consistent.

A self-hash proves only consistency of attacker material. It does not make that material match the binding re-derived from the adopted receipt.

The new court's direct-construction and `dataclasses.replace` fixtures are structurally genuine attacks: they fabricate the exact authority-bearing fields HQ215 showed were trusted before the repair. The self-consistent-rehash witness additionally recomputes the binding hash using the module's own `semantic_hash`.

Static comparison with the pre-authentication code independently confirms why these witnesses fail on the old implementation: the old eligibility methods trusted `self.admitted_source_universe_refs`, and the old evaluator did not require authentication from the exact request/receipt/rule.

I therefore sustain the worker's negative-control conclusion as mechanically credible, while classifying its 18/25 shadow-tree execution as candidate-produced runtime evidence rather than a reviewer rerun.

## 3. Authentication quality

The helper's security property is correct:

`presented binding != authority`

`re-derived binding from request + adopted receipt + exact rule = authority-bearing binding`

The evaluator and both eligibility powers use the returned re-derived binding.

The helper additionally repeats a full material-equality check after the verifier. That second gate is redundant today but is valid defence against future weakening of the verifier.

A self-consistent attacker hash cannot satisfy the path unless the attacker's material is exactly what the authoritative receipt/request/rule themselves lawfully derive. In that case it is no longer a forged eligibility claim; it is the same authorized binding material.

## 4. Closing powers 1 and 2 was necessary, not semantic widening

HQ215's defect was not merely “forged bindings reach F8.” It was that the public binding could manufacture **source eligibility**.

Leaving either:
- `assert_query_source_admitted`, or
- `expose_unranked_admitted_source_set`

unauthenticated would preserve the same authority overreach even if the F8 evaluator were closed.

Requiring authentication on these two existing powers does not add a new power. It narrows their preconditions so they can no longer speak from caller-controlled binding fields.

That is the correct scope.

## 5. Breaking API compatibility

This is a real breaking contract change and is correctly disclosed.

I independently scanned all **136 candidate-visible production Python files** under `rawlsing_next/` at the exact candidate tree for:
- `evaluate_bound_positioned_subject_possibility`;
- `assert_query_source_admitted`;
- `expose_unranked_admitted_source_set`;
- `assert_complete_coverage_from_binding`;
- `ServiceApplicabilityF8SourceScopeBinding`;
- import/reference to `pre553_service_f8_source_scope_binding`.

No production consumer exists outside the binder module itself.

Therefore no current candidate-visible production caller is stranded by the new required `request` / `receipt` / `rule` parameters.

The lawful in-repo callers are the binder courts. Their call sites were updated.

The visible break for hypothetical external/future callers is intentional fail-closed behavior: an unauthenticated call no longer returns eligibility or reaches F8.

## 6. Currentness recovery

The helper recovers `currentness_result` from the presented binding solely so the deterministic binding can be re-derived at the same material grain.

This does **not** authenticate an independent external currentness authority. The module explicitly defines the value as caller-supplied carried material and continues to refuse `currentness_authority()`.

Re-derivation re-applies the existing currentness contract:
- no claim + supplied result refuses;
- claim + missing result refuses;
- adopted noncurrency states refuse;
- legacy negative states refuse;
- arbitrary caller-defined positive vocabulary refuses;
- only the already-adopted vocabulary member `CURRENT` may be carried.

Thus a forged currentness string cannot expand the vocabulary or become a new currentness decision power.

Important precision: the authoritative applicability receipt itself does not certify currentness. The safety claim is narrower: currentness remains explicitly non-authoritative carried material, and authentication cannot turn an arbitrary binding string into source-eligibility authority or currentness authority.

That is consistent with the existing seam law and does not block this repair.

## 7. Removed `BINDING_RULE_REPLAY_MISMATCH`

Removing the old evaluator-local comparison is safe.

If a lawful binding was produced from rule A and evaluation presents rule B, authentication re-binds from rule B. The resulting material/replay identity differs from the expected binding and refuses as:

`BINDING_REPLAY_MISMATCH`.

The old later-stage `BINDING_RULE_REPLAY_MISMATCH` branch is therefore unreachable after successful authentication.

The remaining assertion:

`bound_rule.rule_hash == authenticated.f8_rule_hash`

is an internal invariant proving that authentication returned a binding derived from the presented rule.

This is strictly at least as strong semantically: the rule mismatch is rejected earlier, during authority authentication. The compatibility impact is refusal-reason vocabulary only.

Because the candidate-visible production census found no external production consumer of this binder at all, there is no current production consumer matching on the removed reason code.

## 8. Existing-court edits

I inspected the code-bearing patch rather than trusting the stated “20 hoisted request variables.”

The main court contains 23 added `req...` assignment lines under a raw patch-line count; the repair court adds two request-return helper paths. The worker's “20” is therefore not an exact mechanical count under that simple definition.

The substantive pattern is nevertheless safe:
- previously inlined binding requests are hoisted and passed back into authenticated calls;
- positive assertions remain positive;
- negative assertions remain negative;
- the receipt-mutation witness was **tightened** so the admitted set stays unchanged and only replay identity changes;
- the rule-mismatch witness changes only its expected refusal from the removed later-stage code to `BINDING_REPLAY_MISMATCH`.

I found no assertion weakened into accepting success, no broad “any exception” substitution on a formerly exact positive result, and no positive path made unreachable merely to satisfy the repair.

## 9. Court authenticity and HQD-216 productive adequacy

The new hostile court is fail-capable by static inspection.

It includes:
- direct constructor forgery;
- `dataclasses.replace` forgery with fabricated provenance;
- copied receipt id/replay identity;
- self-consistently rehashed forgery;
- wrong request;
- wrong receipt;
- individual field mutations;
- mandatory-parameter signature checks;
- exact exported-surface census;
- positive single-source mode;
- positive exhaustive mode;
- positive F8 delegation with preserved geometry/authority/replay determinants;
- original A-bound/B-query refusal;
- COMPLETE/INCOMPLETE preservation;
- off-release fail-closed preservation;
- adopted-owner byte guards.

The court does not pass by refusing everything:
- competent applicability + lawful rule reaches `EXACT_SUPPORTED`;
- single-source mode reaches `EXACT_SUPPORTED`;
- exhaustive mode reaches `EXACT_SUPPORTED` and exposes the complete admitted set;
- F8 geometry, rule hash, model authority, walkback authority, and replay determinants are asserted.

That satisfies HQD-216 at local stage grain.

The candidate reports 215/215, zero skipped, across three hash seeds. This Browser/GitHub reviewer has no lawful local runtime under the commissioned modality, so those execution results remain candidate-produced reconstructed-equivalent evidence, not independent reviewer execution. The static court and code attacks above are independent.

## 10. Preservation

The three adopted owners are independently byte-verified at candidate:

- `pre553_service_source_applicability.py`
  `3e40caca29e8c96ee1f412f919cfc7dba63f96c4`
- `source_backed_positioned_subject_possibility.py`
  `62e5eced47b64512f47b004e3e13a6ef3fe21de7`
- `objective_consumer_bounded_evidence.py`
  `f30fca20e7b56e00348e82765d95f974b4b6a195`

No selection, ranking, priority, preference, weighting, pooling, respondent linkage, permission grant, source equivalence creation, backfill, F8 conditioner mutation, F8 geometry/distribution transformation, or actor/person inference was added.

The actor firewall remains intact.

## Nonblocking precision notes

1. “14 public methods” should read **13 public methods + one public data attribute**.
2. “nine loud refusals” should read **eight loud-refusal methods**.
3. “20 hoisted request variables” is not an exact raw patch-assignment count; the patch contains more request-assignment additions depending on counting convention.
4. The defensive import-time currentness vocabulary check still references `ServiceF8ScopeBindingError` before that class is defined. If the adopted vocabulary ever removed `CURRENT`, import would fail with `NameError` instead of the intended typed refusal. It remains fail-closed and is unrelated to the authentication repair.

None is adoption-blocking.

## Final

`ACCEPT_HD_F8_AUTHENTICATION_REPAIR__READY_FOR_HQ_ADOPTION`

No implementation was modified. No repair, merge, rebase, source access, locator discovery, warrant issuance, live C4, C7, actor/person work or self-adoption occurred.

Terminal:

`HQ218_HD_F8_AUTHENTICATION_FINAL_REREVIEW_RETURNED__HQ_DECISION_REQUIRED`
