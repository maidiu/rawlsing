# M04I2 — independent journaled-provenance ancestry repair review

**Overall verdict:** `REVISE_EXACT_CANDIDATE__THREE_JOURNALED_RED_CLASSES_CLOSED__RESIDUAL_UNJOURNALED_ADP017_BYPASS__SCIENCE_HOLD__AUTHORITY_HOLD`.
This is an independent review, not adoption. The M04 candidate is real and closes the three journaled provenance defects exercised by the original 10 fresh RED tests, and it preserves 587/587 inherited positives. It does **not** close the unjournaled ADP017 route: after a journaled revocation, a direct unjournaled `owner.adp017_apply_epistemic_effect` supersession restores an accessible BELIEF and the patched read boundary accepts `REROUTE`.

**Repository:** `maidiu/rawlsing` (PRIVATE)
**Branch:** `review/sorok-r3-m04-claim-ancestry-independent-replay-20261030`
**Sealed commission:** `187fdd11963163dab03c7b061e20067ea1f99134`
**Branch tip at work start:** `7e36cc1509016f8c654a5d8e3cf708656db0727f`
**Target original return:** `2309a73bcea1572f6545d5b26027ddc608bee271`
**Original M04 reviewer:** `3a993abcc0a9f6bd3a1bb003d298d293be199ea6`
**Original M03 author:** `e1f7a74e51201b9614bcc578348b4e9db7be7bd3`
**F3I source court:** `97dbe712e4cce8fedd1632d9ac64b4e57a0ac25e`
**Canonical PRE-MAIN read cut:** `299f41e97a43c67be9cc76a79fa49b48f4e12e54`

**Session:** OpenCode `1.18.34`, model `opencode-go/deepseek-v4.1-flash`, local session variant `max`, device `mainMac` verified by `scutil`; actual session title is the continued `F0R3 postseed authority bypass repairs` (`ses_e72807b76ffeufLz4gsp3C6yVQ`), not the suggested M04I2 rename. Agent name `build`; agent ID not exposed. MAX is local-session evidence only, not a provider-side attestation. Full manifest: `SESSION_LOCATOR.json`.

## Exact source/test identities verified

| Surface | Git blob |
|---|---|
| Original M04 reviewer `00_RETURN.md` | `5840b2f3f551903d61ce00654b8b964c0ea3a545` |
| M04 target `00_RETURN.md` | `dc32b1570cd3ad9ed611d6d1653d261555547e79` |
| M04 target `01_10_RED_NINE_CAN3_DIFFERENTIATION.json` | `ec323a83766bb5c0979addd13defaef1d02c6782` |
| M04 target `02_SOURCE_PATCH_AND_REPRODUCED_TESTS.md` | `366536d69187672d8167d23a99ca461f4d0750fd` |
| M04 target `03_ORIGINAL_M03_M04_OWNER_REVIEW_HANDOFF.md` | `e174724d3bfdacd5aec75a251945749ca13bbe55` |
| M04 reviewer frozen test `review/test_falsifiers.py` | `8add06c66b347e324443c1263771755f6898c7e2` |
| Original M03 candidate `claim_provenance.py` | `2434bda6f4b00e6ea5881291f5422227e8045e74` |
| Original M03 candidate `cell.py` | `3eb2d02aee8dc840e7cac1f99230d7c69adc2f58` |
| M04 patched candidate `claim_provenance.py` | `5ba929f51870b111ca54ca87fdf97338e4295625` |
| Historical CAN3 cutoff used by replay | `ef12349defe22a50e053a7a8080a67ab45673417` |
| Reviewer freeze commit | `3b529996ddd05c3c84225d2054428ff943091aef` |

The M04 target is a five-path return under `WORKER_RETURNS/SOROK-M04-PROVENANCE-ANCESTRY-REPAIR-R1/`; it changes no source outside that return. The patch is a 403-line `claim_provenance.py` overlay; `cell.py` remains blob `3eb2d02a...`.

## What I actually reproduced

Two independent cold reconstructions were created from pinned Git in separate scratch roots. Each reconstructed the reviewer/M02/M01 runtime from absent state, installed the original M03 candidate, ran the baseline, then installed the exact M04 patched helper.

| Court | Baseline (original 2434) | Patched (5ba929) | Exit |
|---|---:|---:|---:|
| Inherited original 413 | 413 PASS | 413 PASS | 0 |
| Inherited M02 100 | 100 PASS | 100 PASS | 0 |
| Inherited M03 author 74 | 74 PASS | 74 PASS | 0 |
| **Inherited total** | **587 PASS** | **587 PASS** | 0 |
| Fresh frozen M04 51 | **41 PASS / 10 FAIL** | **51 PASS / 0 FAIL** | 1 / 0 |
| Historical CAN3 nine (separate replay) | 9 FAIL | 9 FAIL | 1 (replay asserts 9) |

The 10 baseline failures are exactly the three original classes: 4 cross-cell NONE owner substitutions, 4 partial rollback/non-terminal transitions, 2 fully rehashed pre-state ancestries. The patched 51/51 includes those same frozen assertions unchanged. The nine historical CAN3 cases remain nine failures, with their names and source class preserved; they are not repaired, reclassified or counted in the 51 or 587.

The fresh baseline and patched JUnit, the second cold JUnit pair, the historical nine JUnit, the source-identity manifest, and the staging log are preserved under `WORKER_RETURNS/M04I2-R3/evidence/`. Exact counts and hashes are in `01_REPLAY_JUNIT_AND_SOURCE_HASHES.json`.

## Material independent counterexample: unjournaled ADP017 route remains open

The patch's `validate_journaled_transition_ancestry()` checks that each journaled `ADP017_COMMIT` transition remains present with its recorded pre-state and post-state. It does **not** require every current `ctx.epistemic_transitions` entry to have a journal entry, nor does `validate_consumption()` require the terminal transition to be journaled. The author's own Limits section says direct unjournaled ADP017 calls are covered only to the extent exercised by the frozen tests; the frozen 51 do not exercise this route.

Executed counterexample (`candidate/m04i2_unjournaled_probe.py`):

1. `Cell().prepare('CERTAIN','BELIEF')` creates one journaled ADP017 transition.
2. A real journaled `SUPERSEDE_EXACT_RECORD` to `CLAIM_INACCESSIBLE` revokes first-person access. Journal: 2 ADP017 entries; state: 2 transitions.
3. Directly call `owner.adp017_apply_epistemic_effect` with `SUPERSEDE_EXACT_RECORD` back to `CLAIM_ACCESSIBLE`, targeting the revoked effect, **without journaling**. Journal stays at 2; state grows to 3; active stance is one accessible BELIEF.
4. `read_owner(..., '1998-11-20T09:00:00Z')` returns `{'memory':'BUFFER','epistemic':'REROUTE'}` with disposition `BOUND_CANONICAL_CLAIM_WITH_NATIVE_STATE`.

Observed on both the original helper and the patched helper, with the same result:

```json
{
  "before_direct": {"state_transitions": 2, "journaled_adp017": 2, "active_stances": 1, "accessibility": "CLAIM_INACCESSIBLE"},
  "after_direct": {"decision_state": "APPLIED_EPISTEMIC_TRANSITION", "state_transitions": 3, "journaled_adp017": 2, "active_stances": 1, "accessibility": "CLAIM_ACCESSIBLE"},
  "result": {"read": "ACCEPTED", "streams": {"memory": "BUFFER", "epistemic": "REROUTE"}, "disposition": "BOUND_CANONICAL_CLAIM_WITH_NATIVE_STATE"},
  "exit": 2
}
```

A second variant that appends a forged-pre-state unjournaled transition (rather than using the owner API) also passes the patched read boundary. The primary counterexample is the direct owner API route because it uses a valid current pre-state and a real owner operation; the only missing custody element is the journal commitment. The patch closes journaled ancestry but not the unjournaled terminal transition.

**Required correction direction for the original author (not implemented here):** require every terminal transition used for consumption to have exactly one matching journaled `ADP017_COMMIT` entry, and reject any state transition not represented in the journal (or otherwise bind the terminal transition and `payload.after` to the committed journal). The reviewer does not author this repair or accept a verbal promise.

## Three courts

- **ENGINEERING: `REVISE` for the exact candidate as a complete journaled-provenance repair.** `ACCEPT_SCOPED` is warranted for the three journaled classes and the 587/587 + 51/51 evidence. The unjournaled ADP017 route is a material RED counterexample, so the overall claimed repair cannot be accepted as closed.
- **SCIENTIFIC: `HOLD`.** The work is sourcefree TEST_ONLY; no native CAN3/ADP/Pyat actor, world, acquisition or human calibration is issued or verified.
- **AUTHORITY: `HOLD`.** Original M03/M04 author, original M04 reviewer and CAN3 issuer retain their decisions. No owner CAS, canonical C9/CAN3 adoption, PRE-MAIN fan-in or QF2 start is authorized by this review.

## Original owner / canonical C9 compatibility

- The patched helper is compatible with the reconstructed **TEST_ONLY M01/M02/M03 harness** and passes its frozen tests; it is inside the helper source grant exercised by the tests.
- It does **not** establish compatibility with canonical C9 production source. The M04 target changes only return artifacts; no original CAN3/ADP/C9 source is modified. Canonical C9/CAN3 compatibility and any native first consumer remain original-owner decisions, not inferred from this test-only overlay.
- The nine historical CAN3 failures remain the original issuer's separate court. They are not evidence for or against the unjournaled route, and this review does not reclassify them.

## FINDING → INTERPRETATION → ACTION → OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| Patched 51/51 and 587/587 reproduce in two cold roots; baseline 41/10 and 587/587 reproduce too. | The three journaled defects are closed at the tested grain; the patch does not break inherited positives. | Preserve these exact results for the original owner/reviewer. | M04/M03 author + independent reviewer. |
| After a real journaled revocation, an unjournaled direct ADP017 supersession restores accessible BELIEF and `read_owner` accepts REROUTE. | The patch checks journaled transitions but not that every terminal transition is journaled; the author's own limit is exploitable. | Original author must add a terminal/journal coverage check and new adversarial tests; re-review exact bytes. | M03/M04 author; original CAN008/ADP016/017 owners; new reviewer. |
| Nine historical CAN3 cases remain 9 FAIL separate from 51/587. | They are original source-cut negatives, not part of this patch. | Keep red; original CAN3 issuer decides separate court. | Original CAN3 issuer. |
| The patch is a test-only overlay, not canonical C9 source. | Test success cannot establish native science or canonical production compatibility. | Keep scientific/authority HOLD; no merge/adoption. | Original owners + incumbent HQ. |

## DONE / REMAINING / CRITICAL BLOCKERS / LARGEST PRODUCTIVE MOVE / FLIGHT / DELTA

- **DONE:** exact source/test/reviewer/negative readback; two cold reconstructions; baseline 41/10 and 587/587; patched 51/51 and 587/587; historical nine replayed as nine failures; independent unjournaled ADP017 counterexample reproduced on original and patched helpers; session locator recorded.
- **REMAINING:** original author correction for the unjournaled route; new frozen adversarial tests; original M03/M04 owner disposition; original CAN3 issuer disposition of the nine historical failures; distinct re-review of the corrected exact SHA; any owner CAS.
- **CRITICAL BLOCKERS:** material unjournaled ADP017 bypass remains; no original-owner acceptance; no native CAN3/C9 authority; no canonical compatibility; no protected owner CAS.
- **LARGEST PRODUCTIVE MOVE:** the original author adds a journal-coverage/terminality check (every consumed terminal transition must be journaled exactly once with the committed pre/post state), adds an independent test for the direct unjournaled route, and re-runs 587/587 + 51/51 + 9 historical before any re-review.
- **FLIGHT:** no original author/reviewer branch, canonical PRE-MAIN/main, PR514/516/519/521, QF2, native source or other active worker was modified. No model switch. The reviewer worktree is isolated.
- **DELTA:** the M04 candidate's tested journaled repair is confirmed, but a material unjournaled terminal-transition bypass is now demonstrated with exact executable evidence; the candidate is not accepted as a complete repair.

## Commands actually run and exits

```text
python3 repro/stage_independent.py                     # exit 0, M03_PINNED_SOURCE_CLOSURE_READY
python3 repro/install_candidate.py                     # exit 0, OWNED_CANDIDATE_INSTALLED
python3 review/run_fresh.py                            # baseline exit 1, 41 passed/10 failed
python3 repro/run.py after original_413                # exit 0, 413 passed
python3 repro/run.py after independent_100             # exit 0, 100 passed
python3 repro/run_author.py                            # exit 0, 74 passed
python3 repro/run_historical.py                        # exit 0 (asserts 9 failures), 9 failed
# install patched 5ba929 helper
python3 review/run_fresh.py                            # exit 0, 51 passed
python3 repro/run.py after original_413                # exit 0, 413 passed
python3 repro/run.py after independent_100             # exit 0, 100 passed
python3 repro/run_author.py                            # exit 0, 74 passed
python3 repro/run_historical.py                        # exit 0 (asserts 9 failures), 9 failed
python3 candidate/m04i2_unjournaled_probe.py --runtime .../repro   # exit 2, read ACCEPTED
```

The second cold root repeated the staging, baseline 41/10, patched 51/51, inherited 413/100/74, and historical 9 with the same exits.

## NOT_RUN / not claimed

- No original native CAN3/ADP016/ADP017/SCI05/Pyat actor, survey, response corpus or production execution.
- No original CAN3 test re-execution; the historical nine are a replay of the retained JUnit evidence, not a fresh native run.
- No canonical C9/CAN3 production compatibility test, merge, adoption, owner CAS or protected fan-in.
- No QF2 start, no PR/PRE-MAIN mutation, no source/science grant, no self-review.
- No provider-side MAX attestation; only local OpenCode session configuration and local machine-name evidence.

## No self-adoption

This return is input to incumbent HQ and the original owners. The author of the M04 candidate is not this reviewer; this reviewer does not accept its own findings. No branch, CI result, file name or filled field confers source or scientific authority.
