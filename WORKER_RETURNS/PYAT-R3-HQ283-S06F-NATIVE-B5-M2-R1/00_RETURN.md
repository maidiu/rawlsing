# PYAT HQ283 — S06F Native B5/M2 Security Repair — Worker Return

**STATUS:** `BOUNDED_NATIVE_PATCH_PUSHED__SOURCE_FREE_STATIC_REVIEW_ONLY__NO_RUNTIME_EXECUTION__EXTERNAL_ISSUER_HOLD__INDEPENDENT_REVIEW_REQUIRED`

**Role:** S06F commissioned worker, not HQ. No self-adoption or merge.

## Exact start and evidence

- Repository: `maidiu/rawlsing`.
- Exact sealed startup / confirmed initial remote branch HEAD: `85d9e0c815f1aeb78969fc179ad25092c628db04`.
- Assigned branch: `agent/rabochii-pyat-r3-hq283-s06f-native-b5-m2-r1`.
- Commission read at sealed SHA: `WORKER_COMMISSIONS/PYAT-R3-HQ283-S06F-NATIVE-B5-M2-R1/00_COMMISSION.md` (blob `0f1c3420fac49215b99180936327199a5b6c8813`).
- Accepted native source at startup:
  - B5 `rawlsing_next/pre553_learned_product_lifecycle.py` blob `a11c9eb73abab9be118ef4f0b6e325e676059f27`;
  - M2 `rawlsing_next/pre553_learned_product_release.py` blob `f76c390665f06ef126968ccf1a6b2d816f43ae92`.
- Frozen independent S06R requirements: `7e96914ed6c9a186d5de8a778e8396e46a741eb2`, 24 unchanged expected outcomes; S06R review `25722ffab845c54bd5330384ca800b9e4cfcfded`; independent S06T execution `e2cdad12228b4dc7533c8fb55a1750fb0d306e3f`; N04 `b5a6b6409c765d2aecb8c2f9c9ef9bd8fc6473c2` and N04R `fde95ee9275f9fe14b6868db363035757cffab48`; P02R `b3523bed5d751b24f0bf1fd111af4161727fe9b5`.
- S06R/S06T found detached S06 state machine and independent oracle failures; **no reuse or adaptation** of `s06_trusted_release_replay.py`.

## Exact changed paths (worker-owned branch only)

1. `rawlsing_next/pre553_learned_product_lifecycle.py` — native B5 mutation preflights, typed event-derived checkpoint consistency, immediate parent/ordinal chain enforcement, runtime schema/duplicate pair rejection, recertification validity and NO_CURRENT family/scope checks, N04-corrected explicit M2 release/producer-subject cross-check.
2. `rawlsing_next/pre553_learned_product_release.py` — native M2 in-method mutation preflights and direct registration validation against exact subjects, required closures, replay grade, representation and publication binding.
3. `rawlsing_next/tests/test_pre553_s06f_native_owner_security.py` — 16 source-free test functions, one parametrized 3-way case, including local replay/schema/state tampering, typed unknown event refusal, dependency graph transitivity and sibling preservation, direct M2 registration, in-method guard inventory, saved method-callable in protected-mode negative cases, N04 release-vs-subject correction, explicit custody HOLD.

Return artifacts reside only in `WORKER_RETURNS/PYAT-R3-HQ283-S06F-NATIVE-B5-M2-R1/`.

## What was actually changed and what it proves

### B5 native entrypoints

A `_native_mutation_preflight` check is now placed **inside the accepted `LearnedProductLifecycleExecutor` owner implementation**, rather than in a process-local external wrapper, for all 17 public mutating methods:

`stage_release`, `stage_protocol`, `register_product`, `publish_product`, `record_recertification`, `selection_key`, `select_current`, `declare_no_current`, `supersede_current`, `withdraw_product`, `declare_invalidation`, `record_rebuild_eligibility`, `link_rebuild`, `record_cache_materialized`, `record_cache_dropped`, `attest_gc_eligibility`, `record_payload_gc`.

This includes all **nine** B5 methods previously unwrapped by C02J/N04. The two previously partial cases have additional native checks: `record_recertification` refuses withdrawn/invalidated releases; `declare_no_current` refuses an explicit or inferred subject with a different family/scope. Native methods do not accept `trusted=True` as issuance or promote arbitrary text tokens into authority.

**Qualification:** the existing local B5 lifecycle transitions remain operative in the explicitly `LOCAL_UNAUTHENTICATED` environment. These checks do not themselves authenticate event authority/permission, provide cryptographic principal isolation or issue PROTECTED_CURRENT. A same-process Python caller can manipulate instance internals; actual security requires trusted host controls. This is native in-method coverage, **not a complete protected issuer solution**.

### Native checkpoint and replay

`from_checkpoint` now compares its typed event chain to independently derived **within-checkpoint** registered set, publication, validity, replay, rebuild, materialization, payload-materialization, selection/NO_CURRENT receipt links and selection history, as well as invalidation/rebuild/GC receipt-event links. It validates an immediate predecessor for each append-only event (not merely any prior known event), exact family/scope on selection, native runtime schema, and duplicate pair keys.

Recomputed local hashes cannot excuse a **checkpoint whose stored projections disagree with its own event sequence**. The determinant graph still derives from exact registered subjects; existing `LearnedProductDeterminantGraph.affected` computes full directed transitive closure and `unaffected` preserves unrelated sibling releases. A source-free test exercises A→B→C and an unrelated sibling without inventing a detached graph.

**Fundamental limitation:** if an entire history, its typed events, subjects, receipts and hashes are consistently replaced, local replay still cannot prove historical completeness or authentic issuance. Native `export_checkpoint` carries no independently witnessed append-only root, external signature, monotone issuer epoch, or revocation source. **A hash is not an independent custodian.** Every positive external-custody conclusion therefore remains HOLD. Historical `resolve_current_as_of` is a local historical projection, not an external currentness certificate.

### M2 native entrypoints and release/subject split

All five **state-writing** methods inside `M2Repository` now have owner-native preflights: `register_subject`, `register_closure`, `register_release`, `register_representation`, `register_binding`. The three previously unwrapped module helpers `constitute_closure`, `register_representation`, `publish_binding` (and module `register_producer_subject` and `constitute_release`) reach those methods, including when the entrypoint callable is saved before use. This covers all eight prior M2 unwrapped routes at the final repository mutation point.

Direct release registration now checks `ReleaseCore` identity, exact native producer subject/kind/contract, all five closure kinds/members and replay grade. Direct representation checks release subject/producer and virtual/service replay grade. Direct binding checks accepted contract, exact release, representation subject, mode, locator and integrity ref. These fail before native store mutation on a mismatch.

The B5 optional `verify_m2_release_subject_exact(repository, release_ref)` deliberately uses **`resolve_subject_exact(repository, release_ref)`**, which resolves M2 release → `release_subject_ref` → exact producer subject, as confirmed by N04/N04R. It does **not** erroneously call `subject_exact(release_ref)`. It is an explicit cross-check, **not an automatic external issuer**, and existing local B5 staging does not become protected custody by invoking it.

## Frozen oracle / runtime disposition

The 24 frozen S06R expectations are unchanged. No attempt was made to rewrite, loosen, reroute, or claim their success against a different interface. S06T previously observed **26/26 author tests green** for detached S06 but **20 failed / 1 passed** in the frozen independent executor test file; those historic observations are evidence against S06, not results of this branch.

**Commands/exits actually observed in this session:**

- Browser/GitHub API file reads, branch tip and comparison queries, write commits and readback inspections: completed via connected GitHub APIs.
- Static textual inspection: all 17 B5 and five M2 repository method bodies contain their in-method preflight calls; native owner source paths are changed.
- `python -m pytest`, source-free test execution, replayed S06R suite, CI tests, process isolation, live issuer/revocation check: **NOT_EXECUTED**; no Python execution host/worktree was attached and no local shell was used.
- Test result and exit code: **NOT_AVAILABLE**. Added test source is **unverified by execution**. No fictional green test claim.

**Independent next gate:** run the new source-free tests plus existing B5/M2 owner tests and 24 frozen independent acceptance requirements against a pinned candidate worktree. The frozen `s06_trusted_release_replay.py` tests target an intentionally unmodified rejected module, so a separate *independently authored native-owner acceptance mapping* is needed; do not rewrite the frozen oracles to obtain a green result. Review native replay completeness, checkpoint tamper behavior, event/permission issuance, as-of/revocation, saved aliases, and transaction atomicity under a qualified isolated host.

## Hard holds, resources, and scientific claim grade

- **`EXTERNAL_ISSUER_HOLD`**: no competent externally trusted signed grant, validating key/revocation, nonce/as-of/epoch binding, or immutable independently anchored event/checkpoint root available in commission. `require_external_issuer(...)` refuses explicitly in both owners. `PROTECTED_CURRENT` and `EXTERNAL_CUSTODY` **NOT AUTHORISED**.
- **Security boundary not proved:** in-method preflights on source-free local objects do not isolate same-process principals, validate real credentials, prevent all Python private-field mutations, or prove cryptographically authenticated transaction roots. No such positive claim is made.
- **Further semantic/implementation work:** independent issuance and authoritative revocation/epoch policy, per-operation source-scoped permission verification, owner-held externally bound currentness and checkpoint roots, concurrency/atomicity across B5 and M2, full acceptance/cross-branch dependency tests. These are not supplied by text refs or code comments.
- **Model:** GPT-6; requested High effort (actual account/model setting not independently observable).
- **Provider/host:** ChatGPT connected Browser/GitHub API; no local Mac, Codex, subprocess, DeepSeek or harness session; account usage/remaining allowance unknown.
- **Scientific evidence grade:** `SOURCE_FREE_OWNER_CODE_AND_STATIC_INSPECTION_ONLY__NO_RUNTIME_TEST__NO_EMPIRICAL_SCIENTIFIC_GRANT`.
- No survey originals, respondent rows, private source files or protected datasets queried. No G0b/model-use, canonical merge, protected CURRENT, V3 actor or new issuer claimed.
- Independent reviewer required before adoption. No source rights or external custody were minted by this return.

## Terminal

```text
S06F_NATIVE_B5_M2_CODE_PATCH = PRESENT_ON_ASSIGNED_WORKER_BRANCH
B5_PUBLIC_MUTATOR_IN_BODY_GUARDS = 17/17 STATICALLY_CONFIRMED
M2_REPOSITORY_WRITE_GUARDS = 5/5 STATICALLY_CONFIRMED
NATIVE_B5_CHECKPOINT_REPLAY_VALIDATION = SOURCE_PATCHED_NOT_RUNTIME_EXECUTED
EXTERNAL_ISSUER = HOLD_MISSING
PROTECTED_CURRENT = HOLD_NO_GRANT
EXTERNAL_CUSTODY = HOLD_NO_ANCHORED_ROOT
INDEPENDENT_FROZEN_ACCEPTANCE = NOT_EXECUTED_AGAINST_THIS_BRANCH
INDEPENDENT_REVIEW = REQUIRED
ADOPTION = NONE
MERGE = NONE
SCIENTIFIC_CLAIM = SOURCE_FREE_STATIC_ONLY
```

Report the direct verified remote head from final GitHub ref inspection after this file and manifest are committed; do not infer a future SHA from the current working file.
