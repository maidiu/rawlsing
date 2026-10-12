# PYAT HQ280 PV3 C02F — Executed B5 Bypass Court

**TERMINAL:** `HQ280_PV3_C02F_ACTUAL_C02R_BYPASS_RUNTIME_PATCH_COURT_RETURNED__ISSUER_AND_OWNER_ADOPTION_HELD__GITHUB_PUSHED`

**Agent:** Local Python/Rawlsing code implementation worker
**Branch:** `agent/rabochii-pyat-hq280-pv3-c02f-executed-b5-bypass-hostiles-r1`
**Sealed startup (verified):** `72f2612116bfcb041d672ef8e4cd10f24002ef32`
**Authority:** HQD-2026-10-10-280; canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f`; semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390`

**Disposition:** Source-free development candidate only. Non-authorizing, G0b HELD, G1 HELD, CURRENT HELD. No self-adoption. No canonical mutation.

---

## 1. What was actually done

Fixed the C02E test fixture (which attempted to instantiate the abstract `LearnedProductReleaseProtocol`) by constructing `B5.LearnedProductLifecycleSubject` DIRECTLY — the concrete frozen dataclass. No abstract Protocol was ever instantiated.

Executed the full bypass court in three phases:
1. **UNPATCHED** — 13 cases against the raw accepted B5/M2 owners, reproducing every C02R vulnerability
2. **PATCHED** — 14 cases under the C02E test-only mandatory overlay, demonstrating enforcement on direct paths
3. **GENUINE POSITIVE** — 1 case: honest accepted M2 release construction + lifecycle PUBLISHED under a test-only permitted ticket/credential

**Total: 28 cases + 1 positive = 29 results, 0 exceptions, all outcomes recorded from actual owner invocations.**

---

## 2. UNPATCHED results (C02R vulnerability reproduction)

| Case | Attack | Result |
|------|--------|--------|
| A1 | Perimeter positive (baseline) | published=true, authorizing=false |
| B1 | Raw executor K4 bypass | **bypassed=true, publication=PUBLISHED, perimeter_consulted=false** |
| B2 | Raw executor full K5 forgery | **bypassed=true, ceiling_is_forged=true, perimeter_consulted=false** |
| B3 | Raw executor CURRENT selection | **bypassed=true, current_selected_event_present=true** |
| D1 | Attacker-minted M2 release | **published=true, authorizing=false** |
| G6 | Arbitrary ceiling accepted | **published=true, ceiling=urn:c02f:TOTAL_CONTROL** |
| H1 | Checkpoint self-hash | **rehydrated=true, hash_is_self_referential=true** |
| H2 | Checkpoint rehydrates CURRENT | **rehydrated=true, current_selected_event_present=true** |
| L1b | Mutable type gate weakened | **gate_bypassed=true** |
| C2 | Reauthorized mutation admitted | **admitted=true, injected_edge_present=true** |
| H3 | No issuer exists | verification_modules=3 (none are issuers) |

**All C02R vulnerabilities independently reproduced from actual owner invocations.**

---

## 3. PATCHED results (C02E enforcement demonstration)

| Case | Attack | Result |
|------|--------|--------|
| B1-patched | Raw executor without ticket | **refused=true, error=PERIMETER_TICKET_REQUIRED** |
| D1-patched | M2 registration without credential | **refused=true, error=PRODUCER_CREDENTIAL_REQUIRED** |
| H1-patched | Checkpoint self-hash | **refused=true, error=CHECKPOINT_AUTHORITY_REQUIRED** |
| L1b-patched | Type gate mutation | **frozen=true, mutation_succeeded=false** |
| B2b-patched | Demo ticket + forged subject | **bypassed=true** — demo-fixture ticket is NOT issuer authentication |

**Key finding:** The C02E mandatory boundary blocks all direct B5/M2/checkpoint bypass paths. However, a caller-supplied demo-fixture `PerimeterTicket` satisfies the mandatory constructor but does NOT authenticate the subject against owner-held material. The C02 perimeter's expectation comparison remains required for subject-level authentication.

---

## 4. Genuine positive

`POSITIVE_genuine_m2_published`: honest accepted M2 release construction + lifecycle PUBLISHED under a test-only permitted ticket/credential.

- publication = PUBLISHED
- authorizing = false (non-authorizing, as required)
- grade = `DEMO_FIXTURE__NOT_OPERATIVE_CREDENTIALS`

**No competent issuer exists.** The ticket and credential are demo fixtures satisfying the mandatory boundary's type requirements, not operative credentials. This proves the boundary's positive path works without claiming issuer authentication.

---

## 5. Fix vs C02E

The C02E fixture attempted `B5.LearnedProductLifecycleSubject.from_protocol(TestLearnedProductReleaseProtocol(...))` — instantiating a `runtime_checkable` Protocol directly, which Python 3.11 refuses with "Protocols cannot be instantiated".

**C02F fix:** construct `B5.LearnedProductLifecycleSubject(...)` directly with all 15 required fields + 3 optional fields. The concrete frozen dataclass accepts keyword arguments for every field. No abstract type is ever instantiated.

Additionally fixed:
- `ProducerSubject` (M2) does not have `determinant_set_hash` or `replay_root_ref` — those are B5-level fields
- `EXPECTATION_KEY_TYPES` mutation detection now uses `MappingProxyType` check
- `patch_active` tracking now uses `patch_module._PATCH_ACTIVE` (module reference, not static import)

---

## 6. Residual holds (unchanged, not granted)

1. **PRODUCER-ISSUER HOLD** — no accepted issuer/credential exists; M2 registration is unauthenticated by construction
2. **ENFORCEMENT-SURFACE HOLD** — the mandatory boundary is a test-only overlay, not adopted in accepted owners
3. **DEMO-FIXTURE TICKET ≠ AUTHENTICATION** — a caller-supplied `PerimeterTicket`/`ProducerCredential`/`CheckpointAuthority` dataclass satisfies the mandatory type requirement but is not issuer authentication. The C02 perimeter's expectation comparison (owner-held expected identity vs observed subject) remains the only subject-level authentication mechanism, and it is itself a tautology (R3)
4. **REPLAY HOLD** — `REPLAY_COMPLETE` remains an owner-held claim
5. **AUTHORITY HOLD** — semantic AuthoritySnapshot refs remain owner-held
6. **G0b/CURRENT HOLD** — no operative grants

---

## 7. What a mandatory adopted owner change would need

1. **Trust principal** — an issuer that signs/attests `PerimeterTicket` and `ProducerCredential` such that a caller cannot forge them
2. **Independent checkpoint validator** — verifies checkpoint hashes without trusting the caller's self-computed hash
3. **Owner adoption** — the accepted B5/M2 owners must be modified to require these credentials (currently UNADOPTED)
4. **Tautology closure** — the C02 perimeter's expectation must be authored independently of the construction it authenticates (currently derived from it)

**None of these exist today.** The C02E/C02F candidates are development-grade demonstrations of the enforcement surface, not production credentials.

---

## 8. Return contents

- `00_RETURN.md` — this file
- `01_REAL_CONCRETE_FIXTURE_AND_CALLERS.md` — the fixed fixture and caller graph
- `02_UNPATCHED_VS_PATCHED_OWNER_HOSTILES.json` — exact UNPATCHED vs PATCHED results
- `03_TRUE_POSITIVE_AND_FAKE_CREDENTIAL_NEGATIVES.json` — genuine positive + fake credential probes
- `04_ISSUER_AND_MANDATORY_OWNER_PATCH_HOLDS.md` — what an adopted owner change would need
- `05_MANIFEST.json` — file manifest
- `repro/c02f_bypass_court.py` — the executable bypass court (29 cases)
- `repro/logs/bypass_court.json` — exact court output (JSON)