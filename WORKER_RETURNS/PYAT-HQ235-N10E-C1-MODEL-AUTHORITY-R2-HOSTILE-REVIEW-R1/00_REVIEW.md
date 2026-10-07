# PYAT HQ235 — N10E / C1 OWNER-NATIVE MODEL-AUTHORITY R2 HOSTILE REVIEW — R1

**DISPOSITION:** `C1_OWNER_NATIVE_MODEL_AUTHORITY_R2_PARTIAL__NAMED_DEFECT`

**CANDIDATE:** `agent/rabochii-pyat-hq232-n10e-c1-model-authority-correction-r2 @ d042fd69f8536bb5e2a58ce59806419d3c3bd3a4`  
**REVIEW BRANCH START:** `8d4a138f0972d2407ce70483a6b36d55427b06bd`  
**MODE:** hostile documentary semantic-authority review only; no implementation; no adoption.

## Dispositive finding

R2 substantially repairs HQ231. The complete hash chain independently reproduces 10/10; the authority/rule/crosswalk graph remains acyclic; the historical `C1-AT07-MODEL@1.0.0 | 2876572d...` fixture remains fixture-only and nongenealogical; and the negative actor/V3, real-source, source-semantics, comparability, source-composition, threshold, structural-admission, prediction and normative ceilings are preserved.

R2 is nevertheless **not ready for explicit HQ adoption** because two identity/enforcement defects remain.

## A — stable semantic basis attack

The R2 basis correctly freezes the HQ231 omissions and most of the admitted Z08/A05 surface:

- proxy lane only after exact lane remains unresolved;
- exact `SUPPORTED` returns immediately;
- exact `VALID_EMPTY` and `NONCOMPARABLE` are terminal;
- every step proxy authority must be positively listed;
- only upstream `SUPPORTED` proxy evidence may satisfy a proxy;
- strict subset against both original and immediately preceding conditioner sets;
- no sibling substitution or re-widening;
- exact query-grain obligations;
- same-source/same-release fail-closed proxy boundary;
- finite authority-supplied ladder and first-supported selection;
- specificity-loss receipt semantics;
- replay determinant inclusion/exclusion, including unused-evidence exclusion;
- epistemic/jurisdiction ceiling.

### Named defect: `HQ235-DEFECT-STABLE-TYPED-RESULT-MAPPING-001`

The canonical stable-basis preimage does **not** freeze the complete typed result-state mapping admitted by Z08/A05.

The admitted Z08 contract distinguishes these public V1 result states:

- `EXACT_SUPPORTED`;
- `EXACT_UNRESOLVED_PROXY_AVAILABLE`;
- `UNRESOLVED`;
- `VALID_EMPTY`;
- `NONCOMPARABLE`;
- `FAIL_CLOSED`.

The admitted implementation likewise maps exact support, terminal exact states, unauthorized proxy source/release, selected proxy, and exhausted walkback to those exact result-state/disposition combinations.

R2's `01_STABLE_RULE_BASIS.json` contains `supported_exact_state = EXACT_SUPPORTED`, exact-disposition handling, and fail-closed/proxy prose, but contains no `result_state` law at all and does not name `EXACT_UNRESOLVED_PROXY_AVAILABLE` or `FAIL_CLOSED`. Therefore a later implementation could change the public result-state mapping — for example rename or collapse proxy-available or fail-closed outcomes — while leaving the R2 stable basis hash unchanged.

That violates the commission's requirement that the **exact typed-disposition mapping** be identity-bearing and recreates the same class of semantic-drift-under-stable-hash failure that HQ231 identified.

Required bounded correction: add an exact stable mapping from evaluated condition to public `result_state`, `exact_disposition`, proxy eligibility/noneligibility and fail-closed state. Then recompute every downstream identity.

## B — scope-enforcement attack

R2 correctly selects a bounded kind-specific validator and freezes positive state, exact kind/operation/family/source universe, exact release membership, exact fixture membership, exact permitted-use membership, `real_source_effect=false`, `AT07_FIXTURE_ONLY`, exact matching, fail-closed omission, and a load-bearing pre-construction/pre-provider sequence.

### Named defect: `HQ235-DEFECT-SCOPE-CONTEXT-BINDING-001`

The contract validates `fixture_id` and `permitted_use` as **caller-supplied strings**, but does not freeze the authority-bearing provenance of those values or bind each load-bearing use site to one exact permitted-use token.

The candidate authority permits two distinct strings:

- `SOURCE_FREE_C1_01_COMPATIBILITY`;
- `SOURCE_FREE_N10E_LIFECYCLE`.

The validator contract says only that the supplied string must be an exact member of `permitted_uses`. It never states which token is mandatory for stable-rule/C1 compatibility construction versus N10E provider/lifecycle use. A conforming implementer must therefore invent that mapping, or could pass either in-scope token at either call site and still satisfy the frozen validator.

The fixture/effective-time boundary has the same enforcement-shape problem. `fixture_id` is accepted as a caller value, while `effective_time_or_interval_must_equal = AT07_FIXTURE_ONLY` checks only the snapshot's static field. The current N10E provider request binds source/release/query/model-rule determinants but carries no fixture id, permitted-use identity, or fixture-effective-context witness. R2 does not freeze how those runtime facts are derived rather than self-asserted.

Thus the packet converts scope fields into membership tests, but does not yet prove that the active owner path cannot satisfy them by supplying convenient allowed literals. That leaves a necessary enforcement rule to later implementer discretion, which the HQ235 commission explicitly forbids for a green result.

Required bounded correction: freeze trusted context derivation and call-site-to-use-token mapping. The later validator must compare authority scope against invocation/owner context that is itself exact and non-self-declared. This can remain kind-specific; no generic authority-family redesign is required.

## C — identity recomputation

Independent PRE553 canonicalization/sha256 reproduction passed **10/10**:

- stable basis `409b3968455be046c58d996de47d04261fd27925d2636cfb7b2dfbdc022d0c79`;
- scope contract `a0223ead6cadd09f40d29cced20e4655deee8dc4e2ebdd2c8062ee317a5a7211`;
- interpretation `3ed241a8d97bd7c14da86ce09775757da6d48e06ae92ad4151ddcec4f4d2c857`;
- replay `9a250d5a00f519b0f00126fcbc85f344e095f0932574f1d44994f380c48640e4`;
- owner authority `e8215547c90ddf2b88dc5338e08de290f5c97e7db7741e9394c8dd6328631d85`;
- stable rule `a7bcf8a4ab84859cfcac1f2505e2eefccd58d9ea193936a8ff1b85bc0e29064a`;
- crosswalk `43c58d12ff090dadd6fe9116b5d9fd32d623d3e2515dfee498ea85dc01c447f4`;
- evidence `18e2d671707dcc7656e38f1ae4015f8a3a5efaa1a2fc25a5d5c96c5c09da4932`;
- evidence receipt `e042d3d321c0cb894eeca63c0570aae4608ce87fe6368cbafe0db7ca1fcc2abb`;
- maintenance candidate `6fa5efe5dd0209d003bb10d9d4c260b6556a88e927f49034977cb15ce068f69b`.

Dependency ordering is coherent and acyclic. Rejected HQ230 hashes occur only in explicitly labeled historical-rejected/tombstone material in the crosswalk, evidence object and recomputation manifest; they are not active authority refs, parents, supersession refs, or rule dependencies.

## D — negative ceiling

PASS. R2 creates no actor/V3, real-source-effect, source-semantic, comparability, source-composition, support-threshold, structural-admission, prediction or normative authority. Walkback authority remains separate. Historical fixture authority remains fixture-only and nongenealogical.

## E — implementation readiness

FAIL pending the two bounded repairs above. The candidate is close, but a Space Bunny implementer would still have to invent (1) the exact public result-state mapping absent from the stable basis and (2) trusted fixture/use context derivation plus the exact use-token assignment at each load-bearing call site.

No production code is authorized here. No authority is adopted here. After correction, identities must be recomputed and hostile-reviewed again before explicit HQ adoption and any implementation/re-freeze/lifecycle work.

**TERMINAL:** `C1_OWNER_NATIVE_MODEL_AUTHORITY_R2_PARTIAL__NAMED_DEFECT`
