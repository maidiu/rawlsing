# M5 validated structural peer use is not actor effect

**Case identifier:** R3:CASE:04; **T cross-reference:** G1A-FUNC-018_RELATED_ONLY (not a new original T). **Shared seam:** XS:014. **Grade:** PROTECTED_STATIC_PEER_FIRST_READER__ACTOR_CAUSAL_EDGE_FORBIDDEN.

**Precise upstream code:** [rawlsing_next/m5_runtime_rsc_peer_prior.py](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/rawlsing_next/m5_runtime_rsc_peer_prior.py#L977) (`6a5c12f04323d74001f9632063ec907f4fc4468e`, blob `18735bdb31a220aed032aa722574d685e2bdddf5`, lines 977-1122)

**Precise downstream code:** [rawlsing_next/m5_runtime_rsc_peer_prior.py](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/rawlsing_next/m5_runtime_rsc_peer_prior.py#L1122) (`6a5c12f04323d74001f9632063ec907f4fc4468e`, blob `18735bdb31a220aed032aa722574d685e2bdddf5`, lines 1122-1183)

## Before: input and issuer

Current validated RSC; separately declared V3 structural peer requirement; exact selected resolution keys. Original historical T equivalence was **not** independently re-executed in this R3 subcourt. Prior R7 original evidence is referenced separately, not imported as an accepted original proof.

## Current transformation and result

bind_structural_peer_use validates exact RSC validation receipt and V3 peer-owner declaration, required resolution keys and requested use membership in selected resolver atom; receipt's effect is STRUCTURAL_CONTEXT_ELIGIBILITY_ONLY__NOT_V3_MUTATION_PERMISSION, actor_state_effect=False.

**Output:** M5 StructuralPeerUseReceipt with no actor-state, no causal-history, no route sampling.

**Negative / counterexample:** Missing peer declaration or use not contained in each RSC entry raises; even an allowed ACTIVE_CAUSAL use atom does not mutate an actor by itself.

**First real importer and ceiling:** M6 imports RSC and peer receipt types expressly to forbid them as behavioral sources.

**Minimal differential falsifier (NOT_RUN):** Grant allowed CONTEXT and inspect preserved actor state/memory, then request ungranted ACTIVE_CAUSAL; deny and preserve zero actor effect.

**Evidence IDs:** R3:EV:07;R3:EV:09. **Exact operation IDs:** R3:OP:04:BEFORE, R3:OP:04:AFTER. **Shape IDs:** R3:SH:04:BEFORE_IN, R3:SH:04:BEFORE_OUT, R3:SH:04:AFTER_IN, R3:SH:04:AFTER_OUT. **Reader:** R3:READER:04. **Unjoin:** R3:U:04.

## Four-sentence semantic summary

This stage receives Current validated RSC; separately declared V3 structural peer requirement; exact selected resolution keys. Its implementation bind_structural_peer_use validates exact RSC validation receipt and V3 peer-owner declaration, required resolution keys and requested use membership in selected resolver atom; receipt's effect is STRUCTURAL_CONTEXT_ELIGIBILITY_ONLY__NOT_V3_MUTATION_PERMISSION, actor_state_effect=False.. The returned structural/actor authority is limited to M5 StructuralPeerUseReceipt with no actor-state, no causal-history, no route sampling. The historical original-to-selected-source-native success and later genuine actor/world effect are unproved; Grant allowed CONTEXT and inspect preserved actor state/memory, then request ungranted ACTIVE_CAUSAL; deny and preserve zero actor effect is the smallest discriminating next check requiring separate authorization.

**Custody:** ZAK-04S is evidence mapper only. Original historical function custody remains PR1053; ZAK-02S source and ZAK-03S current empirical issuer remain distinct; no new actor/FF authority issued.
