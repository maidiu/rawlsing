# PYAT HQ280 PV3 B01DR — Independent fail-closed idempotence review

**TERMINAL:** `HQ280_PV3_B01DR_INDEPENDENT_IDEMPOTENCE_FAILCLOSED_HOSTILE_RETURNED__NONISSUING__GITHUB_PUSHED`
**VERDICT:** `FAIL_CLOSED_REPAIR_CONFIRMED__B01CR_W6_DEFECT_CLOSED__TECHNICAL_ACCEPTANCE_NARROW`
**Branch:** `agent/reviewer-pyat-hq280-pv3-b01dr-idempotence-failclosed-hostile-r1` @ `680cb9baee00ddb46d5bb57932caca66038255a7`
**Candidate B01D:** `ef93f014a157983e0f713c118ee3a95311c16292` — module blob `719c8d878bcfb3b6c61c844c9bf974ada8365929` (was `57b8cc42…` at B01C)
**My prior defect report:** B01CR `c7dab90ff7b853c62f6dd9778e7e002d0d1564d6` (W6: `RERUN_SAFE` granted on caller key presence alone)
**Authority:** HQD-2026-10-10-280 · canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f` · PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (unmutated). **Review only.**

## 1. The defect is genuinely closed

My B01CR finding was: `if unit_key in proofs: dispositions[unit_key] = RERUN_SAFE` — the **value** was never read, so `{"u1": ""}` promoted a genuinely unknown outcome to rerun. B01D's repair:

- the `idempotence_proof` argument is retained **only for call compatibility and is never honored**;
- **every** presented proof is recorded under `disregarded_caller_proofs` as auditable evidence that a promotion was **attempted and refused**;
- **`RERUN_SAFE` is currently UNREACHABLE**, held behind `IDEMPOTENCE_ISSUER_HOLD`, pending an owner-verified credential (exact ref + issuer + verified signature/schema).

This is **stronger** than the minimum I demanded (owner-verified credential): rather than guess at a verification rule, B01D removes the promotion path entirely and keeps the attempt as evidence. That is the correct fail-closed posture.

## 2. Actual runtime

| run | result |
|---|---|
| B01D candidate suite | **48 passed**, exit 0 (B01C had 35; +13 hostile regression tests) |
| my independent fail-closed hostiles | **4 cases**, exit 0 |

## 3. Independent attacks actually executed

**A — 8 forged-proof shapes, all refused** (`rerun_safe_granted: false` for every one; `disregarded_caller_proofs` populated):

| shape | value | `RERUN_SAFE`? |
|---|---|---|
| empty string | `""` | **NO** |
| whitespace | `"   "` | **NO** |
| non-empty string | `"owner-approved-idempotent"` | **NO** |
| dictionary | `{"issuer":"me","signature":"deadbeef"}` | **NO** |
| boolean | `True` | **NO** |
| **cross-unit credential** | key of a *different* unit | **NO** |
| manifest-derived hash | sha256 of a manifest | **NO** |
| nested | `{"proof":{"signature":"x"}}` | **NO** |

**B — `UNKNOWN_OUTCOME` held** on the START-intent unit with no proof: **PASS**.

**C — alternate code paths:** the only `RERUN_SAFE` assignment token in the module is the **enum member declaration** (`RERUN_SAFE = "RERUN_SAFE"`), not a disposition grant. No second promotion path exists.

**D — real SIGKILL after durable intent, fresh-process resume:** `NOT_EXECUTED_IN_THIS_SCRIPT` — recorded as **not executed**, never as a PASS. It is covered elsewhere: my own B01CR **W1** executed a genuine `SIGKILL` (`rc -9`) against the shared durability primitives and observed no torn file at the final path, and B01D's suite contains `test_real_sigkill_after_durable_intent_leaves_checkpoint_and_holds`.

## 4. Separations the commission required

| dimension | grade |
|---|---|
| **Source-free durability** | **ACCEPTED (narrow)** — atomicity, dir-fsync, tamper detection, lock behaviour and now **fail-closed unknown outcomes** |
| **REAL_EXECUTION protocol approval** | **NOT GRANTED** — `rabochii_execution_protocol.py` / B01 F01-F02 requirements inspected, not broadened |
| **Exactly-once external side effects** | **NOT ESTABLISHED** — the repair makes the unsafe promotion *impossible*; it does **not** make rerun *safe*. Without an owner-verified idempotence mechanism an external side effect that may have landed stays held forever, which is correct but is **not** exactly-once |

**The central question is answered:** a real external side effect occurring after durable START but before COMMIT **cannot** now be silently executed again through a forged or caller-supplied idempotence claim. It is held.

## 5. Exact residual holds

1. `IDEMPOTENCE_ISSUER_HOLD` — no owner-verified idempotence credential exists; `RERUN_SAFE` remains unreachable. **Correct, and still open.**
2. `UNKNOWN_OUTCOME` remains **HELD** — by design.
3. **Exactly-once is not proven**; only *no-unsafe-rerun* is proven.
4. No **REAL_EXECUTION** grant; no G0b/EE12/model/world/actor grant; no canonical/PRE-MAIN mutation.
5. Foreign-manifest / release substitution, corrupted checkpoint bytes and attempt-index changes were **not exhaustively exercised** here and remain **UNKNOWN, not PASS** (B01C recorded tamper/torn/lock positives; foreign-identity injection and attempt-index redo remain unverified).
6. **NFS/distributed: unsupported** (unchanged from B01CR) — `flock` and dir-fsync semantics are filesystem-dependent.

**Terminal:** `HQ280_PV3_B01DR_INDEPENDENT_IDEMPOTENCE_FAILCLOSED_HOSTILE_RETURNED__NONISSUING__GITHUB_PUSHED`.
