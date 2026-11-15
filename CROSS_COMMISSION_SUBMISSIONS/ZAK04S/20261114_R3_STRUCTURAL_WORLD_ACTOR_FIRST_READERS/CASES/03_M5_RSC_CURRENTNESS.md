# V558 ResolutionResult → M5 current RSC

**Case identifier:** R3:CASE:03; **T cross-reference:** G1A-FUNC-018_RELATED_ONLY (not a new original T). **Shared seam:** XS:013;XS:014. **Grade:** PROTECTED_RSC_FIRST_READER_FOUND__NOT_EXECUTED_HERE.

**Precise upstream code:** [rawlsing_next/m4_v557_v558_publication_repository.py](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/rawlsing_next/m4_v557_v558_publication_repository.py#L1361) (`6a5c12f04323d74001f9632063ec907f4fc4468e`, blob `8ec5c8e1c1a3cb7e998bb6cf0972ac87f396e360`, lines 1361-1487)

**Precise downstream code:** [rawlsing_next/m5_runtime_rsc_peer_prior.py](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/rawlsing_next/m5_runtime_rsc_peer_prior.py#L195) (`6a5c12f04323d74001f9632063ec907f4fc4468e`, blob `18735bdb31a220aed032aa722574d685e2bdddf5`, lines 195-308;530-703;887-977;1038-1122)

## Before: input and issuer

Complete V558 ResolutionResult plus hash-bound CURRENT currentness with basis/time/authority. Original historical T equivalence was **not** independently re-executed in this R3 subcourt. Prior R7 original evidence is referenced separately, not imported as an accepted original proof.

## Current transformation and result

M5 re-runs resolve_v558 and verifies exact result, currentness receipt state CURRENT tied to that resolution, requires RESOLUTION_COMPLETE or COMPLETE_VALID_EMPTY and all selections SELECTED. It signs RSC with exact closure, producer, provenance, permission and negative/deferred digests, validating identical recomputation; it has no actor state input.

**Output:** ResolvedStructuralContext and RSCValidationReceipt; structurally valid complete-empty may still have zero selected factual basis.

**Negative / counterexample:** PARTIAL_TYPED_DEFERRED, missing authority, stale currentness, changed source hash, nonselected receipt, forbidden actor ref must refuse RSC; no 'presence means current'.

**First real importer and ceiling:** M5 bind_structural_peer_use is actual next code function; non-test selected call not observed; existing tests are synthetic.

**Minimal differential falsifier (NOT_RUN):** One exact M4 receipt that changes CURRENT→STALE while same context index persists; RSC creation must fail instead of reusing prior CURRENT.

**Evidence IDs:** R3:EV:04;R3:EV:06;R3:EV:07;R3:EV:08. **Exact operation IDs:** R3:OP:03:BEFORE, R3:OP:03:AFTER. **Shape IDs:** R3:SH:03:BEFORE_IN, R3:SH:03:BEFORE_OUT, R3:SH:03:AFTER_IN, R3:SH:03:AFTER_OUT. **Reader:** R3:READER:03. **Unjoin:** R3:U:03.

## Four-sentence semantic summary

This stage receives Complete V558 ResolutionResult plus hash-bound CURRENT currentness with basis/time/authority. Its implementation M5 re-runs resolve_v558 and verifies exact result, currentness receipt state CURRENT tied to that resolution, requires RESOLUTION_COMPLETE or COMPLETE_VALID_EMPTY and all selections SELECTED. It signs RSC with exact closure, producer, provenance, permission and negative/deferred digests, validating identical recomputation; it has no actor state input.. The returned structural/actor authority is limited to ResolvedStructuralContext and RSCValidationReceipt; structurally valid complete-empty may still have zero selected factual basis. The historical original-to-selected-source-native success and later genuine actor/world effect are unproved; One exact M4 receipt that changes CURRENT→STALE while same context index persists; RSC creation must fail instead of reusing prior CURRENT is the smallest discriminating next check requiring separate authorization.

**Custody:** ZAK-04S is evidence mapper only. Original historical function custody remains PR1053; ZAK-02S source and ZAK-03S current empirical issuer remain distinct; no new actor/FF authority issued.
