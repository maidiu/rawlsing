# SOROK R4 M04R — terminal ADP017 journal-coverage repair

## Identity and verdict

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Branch | `agent/sorok-r4-m04-unjournaled-adp017-terminal-repair-20261030` |
| Worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-r4-m04-unjournaled-adp017-terminal-repair-20261030` |
| Source base | `299f41e97a43c67be9cc76a79fa49b48f4e12e54` |
| M04 author cut | `2309a73bcea1572f6545d5b26027ddc608bee271` |
| M04I2 reviewer cut | `09497812e417001657c40575e6476466cdddef1c` |
| Original M04 reviewer | `3a993abcc0a9f6bd3a1bb003d298d293be199ea6` |
| Device | `oldMac` verified by `scutil --get ComputerName`; hostname `oldMac.lan` |
| Harness / model | OpenCode `1.18.34`; `opencode-go/deepseek-v4.1-flash`, local session variant `max`; provider-side effort not independently attested |
| Worktree isolation | no active writer/process collision; only this branch written |

**Terminal:** `M04R_SOURCEFREE_ACCEPT_SCOPED_CANDIDATE__ORIGINAL_REDS_AND_NINE_CAN3_PRESERVED__NO_ADOPTION`

Observed FINDING: the M04 patch closes the three journaled provenance classes but leaves an unjournaled terminal ADP017 restore. After a journaled revocation to `CLAIM_INACCESSIBLE`, a direct `owner.adp017_apply_epistemic_effect(SUPERSEDE_EXACT_RECORD)` back to `CLAIM_ACCESSIBLE` leaves journal at 2, transitions at 3, and `read_owner` returns `REROUTE`. A forged unjournaled pre-state variant also passes. Causal INTERPRETATION: the read boundary joined journal entries to existing transitions but did not require the consumed restorative terminal to be journaled, nor verify its pre-state against the last journal record. Proposed HQ ACTION: owner and independent review of the bounded terminal check. Accountable OWNER: original M03/M04 author and CAN3/ADP017 owner; incumbent HQ appoints a distinct reviewer.

## Exact repair

Candidate `claim_provenance.py` adds:

- duplicate journal-coverage rejection (`CLAIM_TRANSITION_JOURNAL_DUPLICATE`);
- for an accessible/active consumed terminal: an unjournaled `SUPERSEDE_EXACT_RECORD` is refused `CLAIM_TRANSITION_UNJOURNALED`;
- an unjournaled terminal whose pre-state differs from the last journaled `payload.after` is refused `CLAIM_TRANSITION_PRESTATE_ANCESTRY`;
- the M04 journal-to-transition pre/post checks and orphan rejection remain.

A blanket “all selected-claim transitions journaled” rule was rejected because it broke lawful original native ADD/WITHDRAW assertions in the 587/74 suites. The final rule targets the exact restorative terminal and forged-pre-state routes.

- Candidate helper blob `d9efd3f5ba0d06430ef99f114072ba91ef32f1fc`, SHA-256 `ef551f5ad0c927dffb37554d8aaf8c00a611877242b550fbc541ea5089151f4c`.
- Candidate test blob `fa728cc89375e581c4c5ee326c940fa8562a58a1`, SHA-256 `0f1bb3978657f402f54623f548776612f6ca73768e5764317f0b0805317424bc`.

## Actual RUN results

| Court | Result |
|---|---|
| Original inherited 587 (413 + 100 + 74) | **587 PASS**, 0 failures/errors/skips |
| Original fresh M04 51 | **41 PASS / 10 FAIL** |
| M04 patched baseline 51 | **51 PASS** |
| M04R candidate 51 | **51 PASS**, fresh-process replay **51 PASS** |
| M04R inherited 587 | **587 PASS**, repeated fresh-process |
| Historical CAN3 nine | **9 FAIL preserved**, separate court |
| New adversarial journal tests | **4 PASS** |
| Direct unjournaled probe | before: `read ACCEPTED`, journal 2 / transitions 3; after: `REFUSED CLAIM_TRANSITION_UNJOURNALED`, rollback unchanged |
| Forged unjournaled pre-state probe | before: `read ACCEPTED`, journal 1 / transitions 2; after: `REFUSED CLAIM_TRANSITION_PRESTATE_ANCESTRY`, rollback unchanged |

Exact commands, JUnit counts/hashes and source identities are in `02_SOURCEFREE_PATCH_AND_TEST_RECEIPTS.md`; counterexamples are in `01_JOURNAL_TERMINAL_COUNTEREXAMPLES.json`.

## Three courts

- ENGINEERING: **PASS SCOPED CANDIDATE** — exact original 41/10 and 587/587 reproduced; 51/51 and 587/587 after patch; both unjournaled routes refused; four new adversarial tests pass.
- SCIENTIFIC: **HOLD** — sourcefree TEST_ONLY helper; no native CAN3/ADP016/ADP017/SCI05/Pyat actor, world, practice or A0–A5 claim.
- AUTHORITY: **HOLD** — no merge, adoption, owner transfer or canonical C9/C12 compatibility. Nine historical CAN3 failures remain original-owner RED.

## Artifacts

- `00_RETURN.md`
- `01_JOURNAL_TERMINAL_COUNTEREXAMPLES.json`
- `02_SOURCEFREE_PATCH_AND_TEST_RECEIPTS.md`
- `03_ORIGINAL_OWNER_INDEPENDENT_REVIEW_HANDOFF.md`
- `SESSION_LOCATOR.json`
- `candidate/claim_provenance.py`
- `candidate/tests/test_m04r_journal_coverage.py`

The exact pushed return SHA is the HEAD of this branch and is reported with the final return message.

DONE: original 587/41-10/51/9 reproduced; bounded repair; 51/51 and 587/587; nine preserved; four adversarial tests; both probes refused; source/test hashes and session locator. REMAINING: original owner replay/disposition, independent reviewer at exact SHA, CAN3 owner handling of nine historical failures. CRITICAL BLOCKERS: owner CAS and native/C9 authority; none block the bounded engineering candidate. LARGEST PRODUCTIVE MOVE: reviewer replays candidate `d9efd3f5…` against the frozen reviewer test and probes. FLIGHT: sourcefree local Git/Python only; no PRE-MAIN, PR #514/#516/#519/#521, native source or other worker touched. DELTA: the unjournaled restorative terminal and forged-pre-state routes are closed under the same `read_owner` consumer while all original positives and nine historical failures remain.
