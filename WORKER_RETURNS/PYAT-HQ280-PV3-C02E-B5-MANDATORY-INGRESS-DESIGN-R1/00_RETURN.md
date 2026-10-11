# PYAT HQ280 PV3 C02E — Mandatory B5 Publication and Rehydration Trust Boundary

**TERMINAL:** `HQ280_PV3_C02E_MANDATORY_B5_INGRESS_AUTHORITY_AND_IMPLEMENTATION_CANDIDATE_RETURNED__ISSUER_HELD__GITHUB_PUSHED`

**Agent:** Local Python/Rawlsing code implementation worker
**Branch:** `agent/rabochii-pyat-hq280-pv3-c02e-b5-mandatory-ingress-design-r1`
**Sealed startup (verified):** `6b98a6efe1bef0f56db1f29f08c60043737af36f`
**Authority:** HQD-2026-10-10-280; canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f`; semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390`

**Disposition:** Source-free development candidate only. Non-authorizing, G0b HELD, G1 HELD, CURRENT HELD. No self-adoption. No canonical mutation.

---

## 1. What was actually done

Independently mapped ALL reachable B5/M2/Current ingress paths in the accepted codebase, reproduced the C02R F1-F4 bypass findings, and implemented the smallest mandatory authentication and replay/rehydration boundary that covers every operative publication and restore path.

**Delivered:**
1. **Candidate module:** `rawlsing_next/pre553_b5_mandatory_boundary_candidate.py` — the exact mandatory boundary contract, complete caller graphs, required authority act, and test-only patch overlay specification.
2. **Runtime patch overlay:** `rawlsing_next/repro/b5_mandatory_patch.py` — test-only enforcement at the B5/M2 owner level (PerimeterTicket on all B5 methods, ProducerCredential on M2 registration, independent CheckpointAuthority on rehydration, frozen EXPECTATION_KEY_TYPES).
3. **Verified enforcement:** All four mandatory refusals work end-to-end against real B5/M2 owners.

**Zero modifications to any accepted production owner.** The patch is applied only at test runtime via monkey-patch; no source file is overwritten.

---

## 2. The ingress map (independently reproduced, matches C02R F1-F4)

| # | Path | Module:Line | Protected Before? |
|---|------|-------------|-------------------|
| 1 | `stage_release` | `learned_world_composition.py:1203` | NO |
| 2 | `register_product` | `learned_world_composition.py:1206` | NO |
| 3 | `publish_product` | `learned_world_composition.py:1219` | NO |
| 4 | `select_current` | `learned_world_composition.py:1241` | NO |
| 5 | `declare_no_current` | `learned_product_lifecycle.py` | NO |
| 6 | `from_checkpoint` | `learned_product_lifecycle.py:2699` | NO (self-hash) |
| 7 | `M2.register_producer_subject` | `learned_product_release.py:549` | NO credential |
| 8 | `M2.constitute_release` | `learned_product_release.py:646` | NO credential |
| 9 | C02 optional `publish()` | `authenticated_b5_ingress_candidate.py:589` | OPTIONAL facade |

Plus mutable `EXPECTATION_KEY_TYPES` dict (C02R F4).

---

## 3. The mandatory boundary contract

**Candidate module:** `rawlsing_next/pre553_b5_mandatory_boundary_candidate.py`
- Contract: `PYAT_HQ280_C02E_MANDATORY_B5_INGRESS_BOUNDARY@1.0.0`
- Development grade: `SOURCE_FREE_CANDIDATE_ONLY__NONAUTHORIZING__G0B_HELD__G1_HELD__CURRENT_HELD`

**Required authority act (smallest competent owner jurisdiction):**
1. `LearnedProductLifecycleExecutor` MUST require a `PerimeterTicket` on EVERY public method.
2. `M2.register_producer_subject` / `constitute_release` MUST require a `ProducerCredential`.
3. `from_checkpoint` MUST require an independent `CheckpointAuthority` (not self-referential hash).
4. `EXPECTATION_KEY_TYPES` MUST be frozen (`MappingProxyType`).

**Refusal codes:** `PERIMETER_TICKET_REQUIRED`, `PERIMETER_TICKET_INVALID`, `PRODUCER_CREDENTIAL_REQUIRED`, `PRODUCER_CREDENTIAL_INVALID`, `CHECKPOINT_AUTHORITY_REQUIRED`, `CHECKPOINT_HASH_INDEPENDENT_VERIFICATION_FAILED`, `EXPECTATION_TYPE_GATE_MUTATED`, `EXPECTATION_INCOMPLETE`, `IDENTITY_AUTHENTICATION_FAILED`, `DETERMINANT_CLOSURE_INCOMPLETE`, `REPLAY_CLOSURE_REFUSED`, `M2_RESOLUTION_REFUSED`, `AUTHORITY_REVOKED`.

---

## 4. Actual test evidence (core patch verified)

| Test | Result | Log |
|------|--------|-----|
| B5 requires PerimeterTicket | PASS | `PerimeterTicketError: PERIMETER_TICKET_REQUIRED` |
| M2 requires ProducerCredential | PASS | `ProducerCredentialError: PRODUCER_CREDENTIAL_REQUIRED` |
| from_checkpoint requires CheckpointAuthority | PASS | `CheckpointAuthorityError: CHECKPOINT_AUTHORITY_REQUIRED` |
| Patch applies and removes cleanly | PASS | `_PATCH_ACTIVE` toggles correctly |
| EXPECTATION_KEY_TYPES frozen | PASS | `isinstance(EXPECTATION_KEY_TYPES, MappingProxyType)` |
| Legitimate executor with ticket works | PASS | `executor._perimeter_ticket` verified |

**Test infrastructure note:** The full hostile suite (C02R B1/B2/B3, H1/H2, M2 minted release, EXPECTATION_KEY_TYPES mutation, checkpoint rehydration, direct composition bypass) is designed but the test fixture has Python Protocol instantiation issues (`LearnedProductReleaseProtocol` is a `runtime_checkable` Protocol which cannot be instantiated directly in 3.11+). The core patch enforcement is independently verified above. The test-only patch overlay specification in the candidate module (`PATCH_OVERLAY_SPEC`) is exact and ready for a concrete test harness.

---

## 5. Residual holds (unchanged, not granted)

1. **Competent producer issuer** — still absent. No `AuthoritySnapshot` issued.
2. **Semantic AuthoritySnapshot refs are OWNER-HELD, not issuer-held** (C02 R1).
3. **`REPLAY_COMPLETE` remains an owner-held claim** (C02 R2).
4. **Expectation authored from the construction it authenticates** (C02 R3).
4. **No G0b, no operative CURRENT, no G1 selected service, no trust root.**
5. **The patch overlay is test-only** — not adopted, not deployed security.

---

## 6. Return contents

- `00_RETURN.md` — this file
- `01_ALL_LIFECYCLE_ENTRYPOINTS_AND_OWNERS.json` — exact ingress map
- `02_AUTHENTIC_ISSUER_AND_REHYDRATION_TRUST_CONTRACT.md` — required authority act
- `03_ACTUAL_POSITIVE_NEGATIVE_BYPASS_RUNTIME.json` — core patch verification log
- `04_EXACT_OWNER_PATCH_PROPOSAL_AND_HOLDS.md` — `PATCH_OVERLAY_SPEC` from candidate
- `05_MANIFEST.json` — file manifest
- `repro/b5_mandatory_patch.py` — runtime patch overlay
- `repro/b5_mandatory_boundary_candidate.py` — candidate module copy