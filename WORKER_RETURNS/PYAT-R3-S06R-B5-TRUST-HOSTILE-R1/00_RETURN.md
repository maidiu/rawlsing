# PYAT R3 S06R — Independent B5/M2 security hostile review

**SECURITY DECISION: REJECT / BLOCK B5/M2 TRUST ADOPTION.**
**Functional disposition: S06 is a standalone source-free sketch, NOT an integrated verifier over the accepted B5/M2 owners.**
**Terminal:** `PYAT_R3_S06R_SECURITY_REJECT__CALLER_CONTROLLED_TRUST__UNAUTHENTICATED_HISTORY__NO_OWNER_COVERAGE__NO_EXECUTOR_RECEIPTS`.

- **Frozen candidate:** `4fec074c7e40a8b233055ffd1d80dbede293c9c4`, parent `7f29aec36d24f16da52d84f17c00f08db3a55434`.
- **Review branch:** `agent/reviewer-pyat-r3-s06r-b5-trust-hostile-r1`, independently rooted at `7f29aec36d24f16da52d84f17c00f08db3a55434`, not the candidate.
- **Pre-test freeze:** `7e96914ed6c9a186d5de8a778e8396e46a741eb2` was committed and pushed BEFORE the candidate test Python module was read. It contains 24 hostile acceptance expectations and a source-free executable test artifact. Candidate README/return material with author test names had been seen, but the actual test source had not been read.
- **Execution boundary:** Browser/GitHub source inspection only. Local environment check found `python3`, `git`, but NO DeepSeek harness binary/credential and NO Rawlsing worktree. The user-requested distinct isolated DeepSeek/Python host is unavailable; tests are **NOT RUN**, zero new pytest passes/exit claims. Only author-reported 26/26 PASS seen.
- **No changes to author code, accepted owner code, V3, semantic authority, CURRENT, or external credentials.**

## Independently adjudicated security defects

| Grade | Finding | Candidate lines | Security conclusion |
|---|---|---|---|
| **CRITICAL** | Every state-changing method `withdraw`, `invalidate`, `supersede`, `revoke`, `invalidate_descendants` and `select_current` accepts caller-supplied `trusted=True` as entire "verifier" | 193–288 | Complete caller-bypass of S06's purported trust gate; no issuer, role, entitlement, audience or capability checked |
| **CRITICAL** | `from_checkpoint(require_independent_auth=True, external_auth_token="anything")` passes its "independent auth" branch for **any nonempty string** | 128–186, especially 166–168 | Neither issuer nor signature, subject, action, source, scope, expiry, epoch, replay root nor revocation checked |
| **CRITICAL** | Both event and state hashes and event_count are freely recomputable from attacker-supplied JSON. No external signed root, append witness or preimage custody. | 60–68, 111–187 | Consistently rewritten history/state can be admitted, notwithstanding detectable *inconsistent* rewrites. "Dual hash" does not supply independent evidence |
| **CRITICAL** | S06 imports **no accepted B5/M2 owner**; it mutates only its own `_state`/`_events`. Existing B5 and M2 APIs remain direct public mutators. | entire 314-line candidate; compare canonical owner modules | Cannot protect accepted B5/M2 state; N04R's 9 unwrapped B5 and 8 unwrapped M2 methods and two partial checks are not closed |
| **HIGH** | `invalidate_descendants` loops a single `supersessions` mapping and processes only `old_ref == release_ref` | 275–288 | A→B→C fails to invalidate C; no determinant-edge transitive closure, cycle/sibling/multiple-root semantics |
| **HIGH** | `epoch` and `revoked` checkpoint payload fields are **not included in either hash**, except when redundantly reflected in selection state. Unrelated revoked entries or a new unselected epoch can be substituted. | 111–187, 193–226 | No independent epoch/revocation issuer. `current_epoch` is caller supplied; future arbitrary epoch passes. No selected-release publication/validity check |
| **HIGH** | Public `append_event` bypasses the `trusted` kwarg entirely; unknown event kinds appended without typed rejection | 86–109 | Caller can create PUBLISHED/SELECTED events and security-relevant projections directly |
| **HIGH** | `get_state` shallow-copies top level while leaking mutable nested publication/selection maps; `events` tuple holds mutable dicts | 188–191, 310–314 | External callers can mutate the would-be trusted in-memory state/event objects without verified owner operations |
| **HIGH** | Native owner checkpoint is `LearnedProductLifecycleExecutor.export_checkpoint` with `checkpoint_hash`, typed subject, events, selection receipts, validity, release/determinant/replay state. S06 uses unrelated ad hoc `event_history_hash`, `state_projection_hash`, strings and `epoch` | canonical lines 2630–2844 vs S06 111–187 | Valid B5 owner checkpoint does not directly roundtrip through S06; M2 subject/release identity and permission not verified |
| **HIGH** | `verify_trust_mode(PROTECTED_CURRENT)` and `IMMUTABLE_SNAPSHOT` return allowed without verifying any actual scope/authority | 299–308 | "Mode" is an uncredentialed enum, not evidence of CURRENT or immutable custody |
| **MEDIUM** | `cold_replay` checks self-reconstruction of its own events; does not prove accepted B5 replay, event completeness or independent provenance | 290–297 | Useful source-free consistency smoke check only |

## What remains of scientific/engineering value

S06 defines clear vocabulary for four evidence modes and a toy state transition model, and rejects certain *inconsistent* modifications (bad hash, altered saved state without matching events, fixed-count truncation); EXTERNAL_CUSTODY is always refused. These are useful **development-only assertions**, not competent cryptographic, administrative or owner-embedded security. Nothing in S06 authenticates a real release. Existing N04R/P02R documented owner defects remain open against this new wrapper.

**Frozen deliverables:** `01_FROZEN_INDEPENDENT_SECURITY_HOSTILES.json` (24 cases), `repro/test_s06r_independent_hostiles.py` (source-free adversarial pytest to run on qualified host), `02_DEFECTS_AND_CODE_PROOF.md`, `03_OWNER_CONTRACT_AND_COVERAGE.md`, `04_MINIMAL_OWNER_INTEGRATED_REPAIR_SPEC.md`, `05_SECURITY_DECISION.json`, `06_EXECUTION_AND_PROVENANCE.json`.

**Security disposition:** adoption **NO**, immutable/current issuance **NO**, model-use authority **NO**, external-custody assertion **NO**, source execution **NO**, V3 **NO**. Freeze/retain the security court; only a future independently verified **owner-integrated** candidate with real authority and authorized execution evidence can pass.
