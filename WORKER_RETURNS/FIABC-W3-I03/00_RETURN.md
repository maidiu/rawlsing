# FIABC-W3-I03 — Candidate-C Production Binding

Status: PASS — bounded implementation complete; repository tests authored but not executed on the browser-only worker surface.

Worker: FIABC-W3-I03

Base: 56697a27e94eb9603dfa412a15ab8f1feb819b0c

Branch: agent/rabochii-premain-fiabc-w3-i03-candidate-c-production-binding-r1

## Holding

Implemented the current governed Candidate-C production binding for the two proving sources without creating a second semantic owner.

Candidate C remains the frozen policy identity:

- policy: SOURCE_BACKED_HYBRID_WITH_REGENERABLE_ACCELERATORS
- owner commit: 0b96b8de9aac774566f872cf0630ebd4ddeb70e6
- owner path: rawlsing_next/pre553_route_c_accelerators.py
- owner blob: abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889
- candidate hash: a476e6e44c21b8029ae5d3e6d387428a5fa19549a2126d61aae7c71c50c64a3c

The implementation does not copy, replace, or mutate that frozen owner. Instead it binds the already-lawful zero-accelerator state to the existing authoritative source-backed C11 facade. Thus WHO OWNS THE TRUTH remains the common source/projection/C11/I03/I05 authority estate; WHO PAYS TO REALIZE IT remains Candidate C.

## LiTS-I

The current LiTS-I F02 projection is frozen to:

- source SHA-256: 7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09
- projection cache identity: 84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872

CACC1 and CACC2 remain the only permitted LiTS Candidate-C accelerator identities. For the exact current F02 projection they are not declared fully applicable because the frozen accelerator scope does not close q310/q311 and the rest of any uncovered exact source material. The production entrypoint therefore performs exact-source-backed reconstruction through the common source-backed C11 facade. Presence or deletion of CACC1/CACC2 is physical provenance only and cannot change C11/replay/I03 identity.

No CACC3 is introduced. q310/q311 are not truncated. The workload is not reduced.

## WVS7

The current WVS7 binding is frozen to:

- source SHA-256: 2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d
- projection cache identity: 838070ff6b85d60d4f26f9153b0507ba425936c11a3de94a18d57bfcd083f24d

Its permitted accelerator set is exactly empty. The WVS7 Candidate-C production entrypoint therefore performs exact-source-backed reconstruction with zero accelerators. Supplying a LiTS accelerator identity at WVS scope fails closed.

## Current production seam

rawlsing_next/pre553_candidate_c_production_binding.py now provides:

- bind_current_candidate_c_repository(...)
- build_lits_candidate_c_repository(...)
- build_wvs7_candidate_c_repository(...)
- candidate_c_builder_identity(...)
- candidate_c_repository_builder_for_source(...)

The two build_* entrypoints return (C11Repository, release, Candidate-C binding receipt), which is compatible with the current common repository-binding seam that consumes the first two tuple elements. The binding receipt keeps Candidate C's owner/policy identity explicit while naming the source-backed C11 facade as semantic owner.

This is deliberately not Candidate-B identity substitution. Physical realization may coincide with B in a zero-accelerator cell while Candidate-C identity and cost provenance remain distinct.

## Fail-closed law implemented

The binding rejects:

- source SHA drift;
- exact projection identity drift;
- projection/source authority mismatch;
- any accelerator identity other than frozen CACC1/CACC2;
- any accelerator outside the exact source's permitted set;
- any attempt by this fallback binding to claim a fully applicable accelerator while still using source-backed fallback;
- any unadmitted source.

It never inspects labels, frequencies, missingness patterns, carrier layout, or source values to infer semantics.

## Tests authored

rawlsing_next/tests/test_pre553_candidate_c_production_binding.py covers:

1. exact current LiTS/WVS source/projection/accelerator policy identities;
2. CACC1/CACC2 deletion/nonavailability preserving C11 release, replay, public-object and I03 fact identity;
3. exact-source-backed realization remaining Candidate C rather than Candidate B;
4. physical inventory changing binding/cost provenance while semantic identity stays invariant;
5. WVS zero-accelerator enforcement;
6. CACC3/unknown accelerator rejection;
7. false partial-scope applicability claims failing closed;
8. source/projection mismatch failing closed.

Tests were not executed because this commission explicitly restricts the worker to GitHub/browser repository tools. No result is fabricated.

## Fan-in boundary

The historical EE-P2X reducer/backend snapshot at 617c9c9426db12a3c0f7fea6b68a582c10759553 encoded LiTS-C q310/q311 nonqualification and WVS-C preserved failure. Wave-2 adjudication superseded those conclusions at the Candidate-C portability grain. This worker does not mutate that historical reducer artifact or HQ decision ledgers. The Wave-3 integrated runner must consume this current successor binding instead of replaying those superseded C-stop branches.

No measured P2X execution was performed.

Terminal:

FIABC_W3_I03_CANDIDATE_C_PRODUCTION_BINDING_IMPLEMENTED__READY_FOR_FANIN
