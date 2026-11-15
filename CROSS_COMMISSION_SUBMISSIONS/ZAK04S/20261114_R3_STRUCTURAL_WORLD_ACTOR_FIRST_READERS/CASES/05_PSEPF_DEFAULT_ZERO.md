# PSEPF structural truth cannot self-delegate to actor

**Case identifier:** R3:CASE:05; **T cross-reference:** G1A-FUNC-018_RELATED_ONLY (not a new original T). **Shared seam:** XS:014. **Grade:** EXPLICIT_ZERO_POSITIVE_DEFAULT__NO_NATIVE_ACTOR.

**Precise upstream code:** [rawlsing_next/m5_runtime_rsc_peer_prior.py](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/rawlsing_next/m5_runtime_rsc_peer_prior.py#L1122) (`6a5c12f04323d74001f9632063ec907f4fc4468e`, blob `18735bdb31a220aed032aa722574d685e2bdddf5`, lines 1122-1183)

**Precise downstream code:** [rawlsing_next/v3_psepf_zero_positive_guard.py](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/rawlsing_next/v3_psepf_zero_positive_guard.py#L1) (`6a5c12f04323d74001f9632063ec907f4fc4468e`, blob `e0528d65215cb431196570c38bac4eae94217a1b`, lines 1-69;156-166;304-382)

## Before: input and issuer

Structural context/prior/truth or observer/analyst provenance + request for actor transition. Original historical T equivalence was **not** independently re-executed in this R3 subcourt. Prior R7 original evidence is referenced separately, not imported as an accepted original proof.

## Current transformation and result

PSEPF guard active default AcceptedAuthorityRegistry is MappingProxyType({}) and checks the exact separately accepted authority before any delegate outcome. All decisions preserve actor state, causal cursor, RNG and scheduler zero mutation; even a future positive registry would authorize a separate owner, not mutation inside guard.

**Output:** DENY_ZERO_EFFECT with explicit no-authority reason at frozen default; separate issuer acceptance required.

**Negative / counterexample:** Caller-passed registry-shaped mapping or source class cannot populate immutable default authority; no actor state minted.

**First real importer and ceiling:** No emitted actor transition from guard; downstream accepted owner and exact positive registry both unproved.

**Minimal differential falsifier (NOT_RUN):** Supply valid-looking invented external authority in request without production registry update; guard must deny with zero effect.

**Evidence IDs:** R3:EV:10;R3:EV:11. **Exact operation IDs:** R3:OP:05:BEFORE, R3:OP:05:AFTER. **Shape IDs:** R3:SH:05:BEFORE_IN, R3:SH:05:BEFORE_OUT, R3:SH:05:AFTER_IN, R3:SH:05:AFTER_OUT. **Reader:** R3:READER:05. **Unjoin:** R3:U:05.

## Four-sentence semantic summary

This stage receives Structural context/prior/truth or observer/analyst provenance + request for actor transition. Its implementation PSEPF guard active default AcceptedAuthorityRegistry is MappingProxyType({}) and checks the exact separately accepted authority before any delegate outcome. All decisions preserve actor state, causal cursor, RNG and scheduler zero mutation; even a future positive registry would authorize a separate owner, not mutation inside guard.. The returned structural/actor authority is limited to DENY_ZERO_EFFECT with explicit no-authority reason at frozen default; separate issuer acceptance required. The historical original-to-selected-source-native success and later genuine actor/world effect are unproved; Supply valid-looking invented external authority in request without production registry update; guard must deny with zero effect is the smallest discriminating next check requiring separate authorization.

**Custody:** ZAK-04S is evidence mapper only. Original historical function custody remains PR1053; ZAK-02S source and ZAK-03S current empirical issuer remain distinct; no new actor/FF authority issued.
