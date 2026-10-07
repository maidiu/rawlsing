# PYAT HQ227 — N10E MODEL-AUTHORITY / MODEL-RULE LIFECYCLE REPAIR — R1

**DISPOSITION:** `N10E_MODEL_AUTHORITY_RULE_LIFECYCLE_BLOCKED_BY_AUTHORITY_MATERIAL`

**BRANCH:** `agent/rabochii-pyat-hq227-n10e-model-authority-rule-lifecycle-r1`  
**COMMISSION TIP:** `18a14e8a36942975b0083e92eea01b4e799c9cf4`  
**STARTUP BASE:** `b5ba9ebfc7bc8e6c07aa8799ce9c76d64d5ca03d`  
**FAIL-CLOSED CODE TREE COMMIT:** `8939c727f51465074dc713b1e3bdb1d8d5a5e4a2`

## Terminal finding

HQ227 cannot lawfully complete the requested model-authority/model-rule lifecycle repair from the installed C1 authority material.

The frozen R2 authority package contains `FIXTURE_ONLY_POSITIONED_SUBJECT_MODEL` for `C1-AT07-MODEL@1.0.0`, with exact AuthorityRef hash `2876572dcb4eba80b52361853047d409323fff0c63228d7e6a361c972e1b38bb`. It preserves real model semantics: ALLOW, the exact-conditional/no-smoothing operation, fixture scope, interpretation fingerprint, model-rule ID, and algorithm ID.

But it is not an owner-native PRE553 `AuthoritySnapshot`. R3 says this explicitly: `C1-AT07-MODEL` is an “existing consumer fixture-only AuthorityRef; not PRE553 AuthoritySnapshot.”

The current fixture helper does not recover missing authority material. `model_authority_snapshot(direction)` starts from the SOURCE snapshot, keeps the SOURCE `authority_content_hash`, then changes constitutive fields to model identity/kind/operations/object families. That is the exact changed-body/reused-hash construction rejected by HQ226.

A local worker can mechanically invent missing snapshot fields and recompute a clean hash, but that would fabricate authority. HQ227 expressly says to fail closed when installed fixture material cannot produce a truthful snapshot. I therefore withdrew the provisional local synthesis and restored all three permitted code/court files byte-for-byte to the commission-tip blobs.

Restored blobs:
- `rawlsing_next/pre553_analytical_replay_dependency.py` — `230bd7efed04a8fecc573812d7fbacb6dd93f86f`
- `rawlsing_next/tests/n10e_provider_replay_lifecycle_runner.py` — `a146874238d04bd705509066da0520af77f9f521`
- `rawlsing_next/tests/test_pre553_n10e_provider_replay_lifecycle_court.py` — `40d61205dc9692c9d867fe1e68c88ce08687d8a5`

## Exact upstream material required

Before HQ227 can reopen, an owner/adjudicator must freeze an owner-native model authority object that determines, without local invention:

- exact owner-recognized `authority_kind`;
- exact `governed_object_families`;
- public `scope_envelope` (the fixture-only preimage has `exact_scope`);
- exact `replay_protocol_ref`;
- canonical snapshot custody fields (`typed_state`, outer refs/dependencies, producer replay root);
- `authority_content_hash` over the exact constitutive AuthoritySnapshot body;
- the model-rule ownership law: either the authenticated authority identity cryptographically commits the full rule semantics, or a separately owned exact model-rule determinant is frozen.

If the lawful model AuthorityRef changes, dependent C1/N10E fixture identities must be re-frozen accordingly.

## Runtime

No adoption-grade runtime claim is made. Running the current N10E lifecycle would seed `AuthorityMaintenanceExecutor` with the known unauthenticated model snapshot, so even a green pytest would not prove the commissioned property. The checked-in generic governed-court workflow also targets unrelated FIABC tests and was not mutated.

## Wake condition

Once owner-native model authority material exists:
1. authenticate baseline snapshot body/ref/hash;
2. bind the full consumed model-rule identity;
3. seal a model successor through the accepted owner;
4. resolve and consume the exact sealed successor snapshot;
5. run the fixed-AuthorityRef/rule-material hostile;
6. execute targeted N10E plus directly dependent owner/provider courts.

**TERMINAL:** `N10E_MODEL_AUTHORITY_RULE_LIFECYCLE_BLOCKED_BY_AUTHORITY_MATERIAL`
