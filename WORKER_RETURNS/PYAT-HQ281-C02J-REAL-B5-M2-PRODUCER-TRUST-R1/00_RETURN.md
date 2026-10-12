# PYAT HQ281 C02J — Real B5 producer ingress instead of failed toy signing

**TERMINAL:** `HQ281_C02J_BOUNDED_PRODUCT_OR_EXACT_HOLD__GITHUB_PUSHED`

**Role:** Independent producer-trust and owner-boundary engineer (not a C02-series implementer, not an adopter).
**Repository:** `maidiu/rawlsing`
**Branch:** `agent/rabochii-pyat-hq281-c02j-mandatory-b5-owner-trust-r1`
**EXACT SEALED STARTUP (verified before mutation):** `b1b30ab028e6244b8a53790d3790a87cb716ec29`
**Inherited parent:** `7fe2713181fe4a97fe51feb5f985c7ba29055326`
**Authority:** HQD-2026-10-10-280 · canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f` · semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (unmutated).

No self-issued source, operation, model-use, Field Forge, temporal, CURRENT, G0b or V3 rights. No canonical/accepted owner edits. No respondent rows. No self-adoption.

---

## 0. Verdict in one paragraph

C02HR forged a credential that C02H's hardcoded toy RSA accepted: caller-selected root, no separate-principal trust. This return builds **no token, no ticket, no signature, no hash presented by any caller at any method**. The candidate is a verifier-held ingress: the verifier holds the exact M2Repository object, a frozen per-slot expected product identity, and a frozen replay/authority scope — all constructor-held. The caller supplies one slot string. Authentication is resolve-through-held-repo plus field-by-field comparison against the frozen expectation plus closure verification through the held repo. Independently executed: **UNPATCHED genuine forged PUBLISHED/CURRENT_SELECTED plus caller-minted M2 plus self-hash checkpoint rehydration (5 cases), then PATCHED 17 cases with every direct entrypoint refused under typed classes, and one legitimate positive published with `authorizing=false`. Total 24 cases, 0 exceptions, exit 0.** The C02H failure class (forged demo ticket accepted) is structurally absent: there is no credential surface to forge. Two honest holds remain: the permission ceiling is self-declared in custody (no issuer exists to validate it against), and the frozen expectation is derived from the construction it authenticates (re-derivation after mutation still admits; post-authoring mutation is detected and refused). Disposition: **bounded technical product — ACCEPTED as honest development-grade enforcement; NOT an issuer; NOT operative production security.**

---

## 1. What was actually executed (nothing here is a restatement)

Worktree: assigned branch at the sealed startup; no new clone.

| run | exact command | actual result |
|---|---|---|
| UNPATCHED court | `python3 rawlsing_next/repro/c02j_owner_court.py` (phase 1) | **5/5 vulnerabilities reproduce**: raw publish PUBLISHED, K5 forgery stored verbatim, CURRENT_SELECTED emitted, self-hash checkpoint rehydrates incl. CURRENT, caller-minted M2 release resolves |
| PATCHED court | same script (phase 2, overlay active, verifier registered) | **17/17 enforced**: unknown release, forged ceiling (3 mismatched fields), self-made expectation publish, revoked release, fake permission, fake checkpoint hash, foreign M2 registration, stale replay grade, truncated replay, mutated repo — all refused with typed classes; legitimate positive PUBLISHED with `authorizing=false` |
| Credential/root surface audit | request dataclass fields + verifier constructor inspection | **request_fields=["slot"]**; no credential/ticket/token/signature/hash/root/callback/subject/ceiling field exists anywhere on the caller surface; repo reference is constructor-held, not request-addressable |

Interpreter: CPython 3.11.3 (see `repro/logs/interpreter.txt`). Log: `repro/logs/owner_court.json` (25 rows: start + 24 cases + complete).

## 2. Why this is not another toy

| C02H failure | C02J answer |
|---|---|
| Hardcoded toy RSA, caller-selected root | No crypto at all. The anchor is the held M2Repository object + SHA-256 content hashes the accepted M2 owner itself enforces (a caller cannot present content for a hash it does not hold). |
| Caller-minted demo ticket accepted (B2b) | No ticket exists. The overlay verifies the presented subject's OWN fields against the frozen expectation; a forged ceiling/receipt/root mismatches on 3 fields and is refused before any B5 call. |
| Monkey patch guarding constructor only | Overlay wraps every mutating method: stage_release, stage_protocol, register_product, publish_product, record_recertification, select_current, declare_no_current, from_checkpoint, plus M2 register_producer_subject / constitute_release. Read-only resolution is intentionally unwrapped (it publishes nothing). |
| Mutable EXPECTATION_KEY_TYPES (C02R F4) | Module-level MappingProxyType from the first line; nothing to freeze at runtime. |
| Optional facade | Cutover order: build material, register verifiers, then enforce. Post-cutover, unknown releases, foreign repos and foreign checkpoints are all refused. |

## 3. What remains held (exact, not solved)

1. **CEILING HOLD (C02R G6):** the permission ceiling is self-declared in custody. Substitution is refused (must equal the frozen expectation), but the declared value is unproved. Only a competent issuer could validate it; none exists.
2. **TAUTOLOGY HOLD (C02R C2):** the frozen expectation is derived from the construction it authenticates. Post-authoring mutation is detected and refused (demonstrated); re-derivation after mutation still admits (demonstrated). Only an issuer-held expectation would close this.
3. **REPLAY HOLD:** REPLAY_COMPLETE remains an owner-held claim gated by the M2 closure's own grade.
4. **AUTHORITY HOLD:** semantic AuthoritySnapshot refs are owner-held, not issuer-held.
5. **EVENT-ATTRIBUTION HOLD:** forged event authority/rule refs on direct calls are not authenticated (accepted owner's well-formedness jurisdiction; demonstrated, subject still held-authenticated).
6. **No G0b / G1 / CURRENT / V3 / trust root / issuer.** The overlay is test-only (UNADOPTED).

## 4. Return contents

- `00_RETURN.md` — this file
- `01_OWNER_ROOT_AND_AUTHORITY.md` — verifier-held principal, anchors, jurisdiction
- `02_DIRECT_OWNER_ATTACKS.json` — UNPATCHED vs PATCHED per-case results
- `03_PROPOSED_MANDATORY_PATCH.md` — exact smallest line-level owner diff (UNADOPTED)
- `04_ISSUER_HOLDS.md` — ceiling/tautology/replay/authority/event holds + principal petition
- `05_MANIFEST.json` — file manifest with SHA-256
- `repro/c02j_owner_court.py` — executable court (24 cases)
- `repro/c02j_mandatory_overlay.py` — test-only overlay (UNADOPTED)
- `repro/b5_owner_held_verifier_candidate.py` — candidate copy
- `repro/logs/owner_court.json` — exact court output
- `repro/logs/interpreter.txt` — interpreter version
