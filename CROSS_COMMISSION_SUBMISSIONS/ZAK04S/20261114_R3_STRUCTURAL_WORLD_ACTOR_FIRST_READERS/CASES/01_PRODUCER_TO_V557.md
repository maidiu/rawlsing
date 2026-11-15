# M1 F1/F2/B1 source use → V557 narrowed governance

**Case identifier:** R3:CASE:01; **T cross-reference:** G1A-FUNC-017_RELATED_ONLY (not a new original T). **Shared seam:** XS:012. **Grade:** PROTECTED_STATIC_TRANSFORM_EXISTS__ISSUER_OPEN.

**Precise upstream code:** [rawlsing_next/m4_m1_evaluation_binding.py](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/rawlsing_next/m4_m1_evaluation_binding.py#L165) (`6a5c12f04323d74001f9632063ec907f4fc4468e`, blob `dfc91d93d7d23d9d6cfe6d601d7d5734e7d5042f`, lines 165-294)

**Precise downstream code:** [rawlsing_next/m4_v557_v558_publication_repository.py](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/rawlsing_next/m4_v557_v558_publication_repository.py#L86) (`6a5c12f04323d74001f9632063ec907f4fc4468e`, blob `8ec5c8e1c1a3cb7e998bb6cf0972ac87f396e360`, lines 86-110;479-531)

## Before: input and issuer

Validated source-bound StructuralObject with producer_allowed_uses and exact M1 lineage. Original historical T equivalence was **not** independently re-executed in this R3 subcourt. Prior R7 original evidence is referenced separately, not imported as an accepted original proof.

## Current transformation and result

An admitted relation M1 produces exact V554 F1/F2/B1 structural objects only with a sealed validated producer-use binding. V557 govern_v557 must choose a subset of the producer uses and its governance-state ceiling; ALLOW_CONTEXT_ONLY cannot include ACTIVE_CAUSAL.

**Output:** V557GovernanceRecord with decision-state, exception-state and <=producer permission; no actor or native source proof.

**Negative / counterexample:** Caller supplied producer_allowed_uses, forged active causal atom or governance widening must fail; no assumed issuer from permission enum.

**First real importer and ceiling:** build_v557_publication_bundle and V558 RepositoryEntry, code imports only; no selected native publication.

**Minimal differential falsifier (NOT_RUN):** Take two structurally identical exact objects with different permitted use ceilings; prove CONTEXT-only cannot be published as ACTIVE_CAUSAL with same source issuer.

**Evidence IDs:** R3:EV:01;R3:EV:02. **Exact operation IDs:** R3:OP:01:BEFORE, R3:OP:01:AFTER. **Shape IDs:** R3:SH:01:BEFORE_IN, R3:SH:01:BEFORE_OUT, R3:SH:01:AFTER_IN, R3:SH:01:AFTER_OUT. **Reader:** R3:READER:01. **Unjoin:** R3:U:01.

## Four-sentence semantic summary

This stage receives Validated source-bound StructuralObject with producer_allowed_uses and exact M1 lineage. Its implementation An admitted relation M1 produces exact V554 F1/F2/B1 structural objects only with a sealed validated producer-use binding. V557 govern_v557 must choose a subset of the producer uses and its governance-state ceiling; ALLOW_CONTEXT_ONLY cannot include ACTIVE_CAUSAL.. The returned structural/actor authority is limited to V557GovernanceRecord with decision-state, exception-state and <=producer permission; no actor or native source proof. The historical original-to-selected-source-native success and later genuine actor/world effect are unproved; Take two structurally identical exact objects with different permitted use ceilings; prove CONTEXT-only cannot be published as ACTIVE_CAUSAL with same source issuer is the smallest discriminating next check requiring separate authorization.

**Custody:** ZAK-04S is evidence mapper only. Original historical function custody remains PR1053; ZAK-02S source and ZAK-03S current empirical issuer remain distinct; no new actor/FF authority issued.
