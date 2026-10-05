# HQ215 — H-D/F8 SOURCE-SCOPE BINDING FINAL HOSTILE REREVIEW — R1

**Disposition: `HD_F8_REPAIR_AUTHORITY_OVERREACH`**

**Terminal: `HQ215_HD_F8_FINAL_REREVIEW_RETURNED__HQ_DECISION_REQUIRED`**

Review commission:

`agent/reviewer-pyat-hq215-hd-f8-final-rereview-r1 @ 72b840fc0257958a1376b98f3f2c6ce894c6189d`

Exact repair candidate:

`agent/rabochii-pyat-hq213-hd-f8-binding-repair-r1 @ 09e4dc0d9e8dba21eadab0b5dd55821af7f4811c`

Code-bearing repair commit:

`17737c09194bffd7f8f2f7d135f79d5f8ebfa7fc`

Exact repair base:

`8d352f7d80983cbf49e7e57511f8cf6d5b80966d`

Prior hostile review:

`33062ccfcca5c121bd699a98af11460440cd15ba`

## Executive verdict

The five HQ211/HQ213 bounded repairs are substantially real on the **lawful constructor-produced path**. In particular:

- the original A-bound/B-query defect is closed;
- a requested source must be the bound requested source, positively admitted, and inside the F8 rule source scope;
- the requested-source refinement is included in request material and binding material and therefore changes replay identity;
- the old false “exactly two returning functions” claim has been withdrawn;
- off-release positive decisions fail closed;
- COMPLETE/INCOMPLETE anti-laundering remains intact;
- all three adopted owners are byte-identical;
- the binder still passes query/rule/evidence unchanged to the adopted F8 evaluator;
- silent write-terrain skips were removed;
- the new currentness import consumes only `STATES` and creates no Python dependency cycle.

However the repaired candidate still permits an **authority-bypassing construction path that can manufacture source eligibility without the applicability owner**.

That is adoption-blocking and is properly classified as authority overreach.

## Blocking finding F6 — forged binding bypasses applicability authority

`ServiceApplicabilityF8SourceScopeBinding` is:

- publicly exported in `__all__`;
- a normal `@dataclass(frozen=True)`;
- directly constructible;
- without a `__post_init__` integrity/authority check.

The module contains exactly one `__post_init__`, and it belongs to
`ServiceApplicabilityF8ScopeBindingRequest`, not the binding result.

The public delegating evaluator:

`evaluate_bound_positioned_subject_possibility(...)`

accepts any object that is an instance of the binding class. It then:

1. verifies the caller's F8 rule structurally;
2. compares that rule's hash to `binding.f8_rule_hash`;
3. **optionally** compares a supplied receipt's replay identity and receipt id to the corresponding strings already stored on the binding;
4. calls `binding.assert_query_source_admitted(query)`;
5. delegates to adopted F8.

It does **not**:

- recompute the binding from the applicability receipt;
- require the original binding request;
- require `verify_service_f8_scope_binding_replay`;
- verify `binding_ref` against authorized construction material;
- verify `binding_request_ref`;
- recompute `admitted_source_universe_refs` from the supplied receipt;
- recompute `admission_provenance` from the supplied receipt;
- compare `f8_model_rule_refs` against the caller's rule.

The result is a direct authorization bypass.

### Static counterexample

Suppose source B has a structurally valid F8 rule/evidence but is **not** positively admitted by service applicability.

A caller can construct a `ServiceApplicabilityF8SourceScopeBinding` whose fields say:

- `admitted_source_universe_refs=(B,)`;
- `admission_provenance` contains a hand-authored row for B;
- `release_identity_ref` equals the query release;
- `f8_rule_hash` equals the real F8 rule hash for B;
- `binding_mode=SINGLE_SOURCE_VALIDATION`;
- `requested_source_universe_ref=B`.

The caller can also copy the `applicability_receipt_id` and
`applicability_receipt_replay_identity` from a real receipt that did **not** admit B.

Even when that real receipt is passed to the evaluator, the receipt checks succeed,
because they only compare those two copied identity fields. The evaluator never checks
that B appears in the receipt's actual admissible set.

`assert_query_source_admitted` then trusts the forged binding's own
`admitted_source_universe_refs` and `admission_provenance`, and F8 is reached.

The same class of attack is possible with `dataclasses.replace` on a legitimate
frozen binding: frozen prevents field assignment, not creation of a modified replacement
instance. With no result-object integrity hook, the replacement is accepted as the same
public binding type.

This violates the seam's load-bearing law that F8 source eligibility must be derived
from adopted service-source applicability authority.

## Why replay does not save the evaluator

The repair correctly added requested-source material to replay identity.

That solves the original A/B defect for bindings produced by
`bind_service_applicability_to_f8_scope`.

But `verify_service_f8_scope_binding_replay` is a **separate optional public function**.
The evaluator never invokes it.

A forged binding can therefore have a replay identity computed from forged material or
simply carry arbitrary `binding_ref`/`binding_request_ref` fields; neither is
validated on the evaluation path.

This makes the module's evaluator docstring claim that omitting `receipt` “does not
weaken the binding” too strong. More importantly, even supplying a receipt does not
close the forged-binding path.

## Court blind spot

The repaired court does not attack direct construction of the public binding result.

Both binder courts contain **zero** direct calls to:

`ServiceApplicabilityF8SourceScopeBinding(...)`

The Repair 2 “exact public callable surface” court also structurally excludes the two
exported data classes from its module-callable inventory, and its binding-method helper
iterates only the already-pinned two positive method names rather than discovering the
actual public method surface.

So the court cannot detect the exact constructor bypass found here.

The production docstring itself says “declared public callables are EIGHT,” while the
repair court's operative power-accounting assertion says “six public callables.” That
remaining count mismatch is documentary, but it is downstream of the more important
fact: the public binding class constructor is not authority-neutral.

## Mandatory attacks — results

### 1. Original A-bound/B-query defect

**CLOSED on constructor-produced bindings.**

`assert_query_source_admitted` now checks, in single-source mode, that the query source
equals `requested_source_universe_ref` and refuses with:

`F8_QUERY_SOURCE_NOT_THE_REQUESTED_SOURCE`

before admission/release succeeds for a different admitted source.

The repair court contains the exact A-bound/B-query witness.

### 2. Requested source constraints

**CLOSED on lawful construction path.**

At bind time the requested source must:
- be positively admitted;
- be inside `rule.source_universe_refs`.

At evaluation it must equal the query source in single-source mode.

### 3. Requested-source replay/content identity

**CLOSED on lawful construction path.**

The requested source is present in:
- request material;
- binding material;
- binding replay identity.

Re-deriving a binding for B cannot replay-verify as a binding for A.

This does not authenticate an arbitrarily hand-built binding unless the verifier is
actually invoked.

### 4. Public API / power accounting

**PARTIAL / BLOCKING.**

The old “exactly two returning functions” claim is gone, and the module now distinguishes
two source-touching powers, constructor assembly, delegating evaluator, replay verifier,
and coverage guard.

But the exported result dataclass constructor is omitted from the operative authority
analysis even though it can mint the object the evaluator trusts. This is a real positive
authority path, not merely a counting nit.

### 5. F8 non-transformation

**PASS for the adopted F8 operation itself.**

The evaluator passes:

`query=query, rule=rule, evidence=evidence`

directly to `evaluate_positioned_subject_possibility`.

The binder does not read `exact_geometry`, `retained_conditioner_ids`, probability,
distribution, density, likelihood, posterior or related geometry/estimation fields.

The three adopted owners remain byte-identical:

- `pre553_service_source_applicability.py`
  `3e40caca29e8c96ee1f412f919cfc7dba63f96c4`
- `source_backed_positioned_subject_possibility.py`
  `62e5eced47b64512f47b004e3e13a6ef3fe21de7`
- `objective_consumer_bounded_evidence.py`
  `f30fca20e7b56e00348e82765d95f974b4b6a195`

The problem is not F8 transformation; it is unauthorized access to the unchanged F8
evaluator through a forged eligibility binding.

### 6. COMPLETE / INCOMPLETE

**PASS on constructor-produced bindings; bypassable through forged result objects.**

The module requires COMPLETE coverage for exhaustive binding and again before set
exposure. Single-source validation remains available under INCOMPLETE.

But a direct binding constructor can simply set
`candidate_class_coverage="COMPLETE"`, so the coverage guard is not authoritative
unless the binding is first proven to derive from the adopted receipt.

### 7. Release/currentness

**Repair 3 CLOSED.**

Off-release positive applicability decisions now refuse with
`BINDING_OFF_RELEASE_POSITIVE_DECISION`.

The adopted applicability owner independently stamps every decision with the request
release.

**Repair 4 currentness vocabulary pin is exact at vocabulary grain.**

The imported contract has exactly:

`CURRENT, STALE, REFRESH_REQUIRED, INVALID`

The binder accepts only `CURRENT` as a positive carried result and refuses the three
adopted non-currency states plus the legacy negative tokens.

This does not itself create a currentness decision: the binder still requires a
caller-supplied claim/result and `currentness_authority()` refuses.

### 8. Adopted owner integrity

**PASS.**

All three required owner blob identities match exactly.

### 9. Selection/ranking/etc.

**No ranking/selection/weighting transformation found on the lawful path.**

The seven refusal-shaped methods remain loud. No geometry/distribution transformation,
pooling, permission grant, equivalence creation, backfill, conditioning or actor/person
inference is added.

The blocking overreach is narrower and more fundamental: a caller can fabricate
**eligibility scope itself**.

### 10. Court authenticity / 190 surface

This review is Browser/GitHub read-only and has no lawful local execution environment,
so I did not pretend to independently execute pytest.

Candidate-produced evidence reports 190/190 with zero skips across three hash seeds.

Static verification confirms:
- the repaired binder court contains zero real `pytest.skip(...)` calls;
- the pre-repair binder court contained five;
- the key Repair 1/3/4/5 witnesses correspond to real code deltas against
  `8d352f7d...`;
- the A/B witness would fail against the pre-repair code because the pre-repair binding
  result had no requested-source field and `assert_query_source_admitted` checked only
  admitted-set membership;
- the off-release false branch exists in the pre-repair code and is absent in the repair;
- the pre-repair currentness path accepted arbitrary nonnegative strings and the repaired
  path does not.

However the courts have **no witness for result-object forgery or dataclass replacement**,
so the reported 190/190 surface does not cover the blocking bypass.

### 11. New currentness import

`pre553_service_f8_source_scope_binding.py` imports only:

`STATES as ADOPTED_CURRENTNESS_STATES`

from:

`objective_non_event_currentness_contract.py`

That contract imports exact-ref primitives through `m4_v557_v558_publication_repository`,
which imports M1/M2/M3. Static import inspection finds no path from M1/M2/M3/M4 back into
this binder or the currentness contract, so no Python import cycle is created.

The binder consumes no currentness receipt type, authority ref or selection record from
that module. At current code grain this is a vocabulary-only dependency, not a new
currentness authority dependency.

Nonblocking precision note: if the imported state vocabulary ever ceased to include
`CURRENT`, the defensive import-time branch references `ServiceF8ScopeBindingError`
before that class is defined, so the failure would be a `NameError` rather than the
intended typed refusal. It still fails closed, but the diagnostic path is malformed.

### 12. Environment classification

The repair packet truthfully labels its execution environment
**reconstructed-equivalent**, not governed certification.

This Browser/GitHub rereview does not upgrade that classification.

## Required repair before adoption

The evaluator must not trust an arbitrary public binding result as proof of applicability
authority.

A lawful repair must make the **evaluation path itself** authenticate the binding against
the authoritative receipt/request, for example by requiring the exact request and receipt
and internally re-deriving/verifying the binding before delegation.

Merely adding a `__post_init__` that checks field shapes or self-hashes is insufficient:
a caller can self-consistently hash fabricated eligibility material. The missing proof is
that the admitted set/provenance came from the adopted applicability receipt.

Add hostile witnesses for:
1. direct construction of a binding that falsely admits B;
2. `dataclasses.replace` of a lawful binding to admit B;
3. the same attacks with a real receipt supplied to the evaluator;
4. altered `binding_ref`, `binding_request_ref`, admitted set, provenance and coverage;
5. evaluator refusal unless the binding is re-derived/verified from the exact authority
   inputs.

## Final

The repair closes the five commissioned defects at their intended path, but the final
rereview uncovers a deeper source-authority bypass. The seam is therefore **not safe for
HQ adoption**.

`HD_F8_REPAIR_AUTHORITY_OVERREACH`

No implementation was modified. No repair, merge, rebase, source access, locator
discovery, warrant issuance, live C4, C7, actor/person work or self-adoption occurred.

Terminal:

`HQ215_HD_F8_FINAL_REREVIEW_RETURNED__HQ_DECISION_REQUIRED`
