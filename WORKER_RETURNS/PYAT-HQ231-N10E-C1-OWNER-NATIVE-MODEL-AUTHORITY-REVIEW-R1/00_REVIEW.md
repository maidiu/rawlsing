# PYAT HQ231 — C1 / N10E OWNER-NATIVE MODEL-AUTHORITY HOSTILE REVIEW — R1

**DISPOSITION:** `C1_OWNER_NATIVE_MODEL_AUTHORITY_PARTIAL__NAMED_DEFECT`

**CANDIDATE:** `agent/rabochii-pyat-hq230-n10e-c1-model-authority-hq-adjudication-r1 @ bd980fb30fc9f2cc6b4fa99b5f75baca5c0a22ec`

**REVIEW MODE:** read-only; no repair; no authority adoption.

## Dispositive finding

HQ230 got the difficult architecture shape substantially right:

- the historical `C1-AT07-MODEL@1.0.0 | 287657...` fixture ref remains fixture-only and unchanged;
- the new owner-native authority is distinct and does not manufacture false PRE553 genealogy;
- no existing current authority kind genuinely owns this semantic jurisdiction;
- the proposed bounded kind `POSITIONED_SUBJECT_EMPIRICAL_POSSIBILITY_MODEL_RULE` is narrower than SOURCE_SEMANTICS, PREDICATE_GRAMMAR, UNCERTAINTY_METHOD, TARGET_USE_PERMISSION, or REPLAY_PROTOCOL;
- the proposed governed family `PositionedSubjectModelRule@1.0.0` is a materially better owner surface than the deferred result-field family or ReplayReceipt;
- all candidate hashes independently reproduce from the committed canonical material;
- Option B is structurally acyclic: stable rule basis -> authority hash -> stable rule object/ref, with no final rule ref feeding back into authority identity;
- the proposed lifecycle graph shape authority -> stable rule -> products matches current generic determinant-graph law;
- the re-freeze/non-rewrite distinction is sound;
- the inability to instantiate the candidate under the current enum/family set is honestly pre-implementation, not evidence of malformed canonical material;
- no architecture warrant is required for the bounded kind/family extension itself.

The candidate is nevertheless **not ready for HQ adoption** because two identity-bearing closure defects remain.

## DEFECT 1 — stable rule basis is not semantically complete

HQ230 says the stable rule basis is the owner-owned determinant whose mutation must capture every stable model-rule semantic change. The frozen basis hash is:

`de15a0fbf77eb71f5b405d9d42cba4eeb8844e3803868295ada41b18afd5372b`

and the resulting stable rule ref is:

`59e82a51b26cca26aff84e42878c1c8f1c0c52e4ad4e26a5b23244999454add2`.

But adopted Z08/A05 semantics contain stable invariants that are not actually represented in that basis.

At minimum the frozen basis omits these binding rules:

1. **proxy lane gate:** Lane P may run only when Lane E is unresolved; exact supported, VALID_EMPTY, and NONCOMPARABLE do not enter walkback;
2. **positive proxy authority membership:** every walkback step's exact `proxy_authority_ref` must also be positively listed in that invocation's `positive_proxy_authority_refs`; an arbitrary step AuthorityRef is insufficient;
3. **proxy evidence qualification:** a proxy slice satisfies a step only in upstream `SUPPORTED` state; other typed states are recorded but cannot satisfy proxy support;
4. **exact ladder relation:** every retained-conditioner set must be a strict subset of both the original requested set and the immediately preceding set. `walkback_steps_strictly_decrease_specificity=true` is weaker/less exact than the adopted subset law.

These are not incidental implementation choices. They are admitted Z08 model semantics and are enforced by the current admitted implementation. If any of them were weakened while HQ230's frozen basis stayed unchanged, the owner-native authority ref and stable rule ref could remain unchanged while model behavior changed. That defeats the purpose of introducing the stable rule determinant.

The repair must therefore re-freeze the **complete stable semantic basis**, not merely keep these rules in implementation tests or per-invocation material.

## DEFECT 2 — frozen authority scope is not fully bound to a validation contract

The candidate authority material correctly freezes:

- exact AT07 fixture id;
- exact source-universe ref;
- exact release ref;
- exact permitted uses;
- `real_source_effect=false`.

But HQ230's replay protocol requires only:

`require_positive_exact_kind_operation_family_and_AT07_source_universe_scope`

and its wake contract likewise names source-universe scope but does not require exact release/use/fixture scope validation.

Current `require_positive_authority()` can enforce exact:

- kind;
- operation;
- public family;
- `source_universe_refs`;
- `target_use_refs`;
- `predicate_or_risk_set_refs`.

It has no parameter for `release_refs`, `fixture_ids`, HQ230's string `permitted_uses`, or `real_source_effect`. The HQ230 implementation-impact map does not explicitly require a new kind-specific scope validator or an extension of this validation contract.

Therefore the candidate currently freezes release/use restrictions into authority identity without freezing how the active owner path must prove those restrictions before use. A future implementation following the packet literally could validate kind/operation/family/source-universe and still fail to enforce the exact release/use ceiling.

The correction must explicitly freeze the validation law for every restrictive scope key. It may be a bounded kind-specific validator or a bounded extension of the existing exact scope API; no broad architecture reopen is implied.

## Hash review

Independent recomputation from committed HQ230 material passed **9/9**:

- interpretation fingerprint: `bcf2f374f8e56f765f01367fc6092983949ffb79759738802f6f47baada4b708`;
- replay protocol: `4ea14ebe4f724e05a0d2560ae7f19b3f4d48522a1bd9750b0544ed976248a08e`;
- authority content: `db0060afb25dfcf7f77b35864c2dd2499e974057aca73a252a208fb93ed2fc65`;
- evidence object: `36b26e090aac64fc736c2ac6362b83011382815af8d09d4939d131eb08a0ea10`;
- evidence receipt: `1315ddecf70cfd7897e63bcc9c00c31d8eb172d1aedf143d544121e33946c0c0`;
- maintenance candidate record: `dd8bdcb2181282d264793293c592a7b401c268a774faf7b15a08d89f3287c10e`;
- stable rule basis: `de15a0fbf77eb71f5b405d9d42cba4eeb8844e3803868295ada41b18afd5372b`;
- stable rule object: `59e82a51b26cca26aff84e42878c1c8f1c0c52e4ad4e26a5b23244999454add2`;
- fixture crosswalk: `4eb8aaaaef078cc7c3da32c5232aa62b45692ec0ffb7867a0376e9a7c47071f0`.

The problem is semantic completeness, not hash arithmetic.

## Required bounded correction

A corrected HQ candidate should:

1. expand/rewrite the stable rule basis so every adopted Z08 stable invariant whose mutation changes behavior is identity-bearing;
2. freeze exact scope-enforcement law for release/use/fixture/real-source ceilings;
3. recompute all identities transitively affected by those changes:
   - stable rule basis hash;
   - replay protocol ref if its scope-validation steps change;
   - interpretation fingerprint;
   - owner-native authority content hash;
   - stable rule object ref;
   - fixture crosswalk ref;
   - evidence/evidence-receipt refs;
   - maintenance candidate record ref;
4. preserve all HQ230 passes: distinct owner identity, non-genealogical fixture crosswalk, separate walkback authority, no real-source effect, Option B acyclic graph, historical C1 non-rewrite, and sealed-successor recomposition.

**No production repair is authorized in this review.**

**TERMINAL:** `C1_OWNER_NATIVE_MODEL_AUTHORITY_PARTIAL__NAMED_DEFECT`
