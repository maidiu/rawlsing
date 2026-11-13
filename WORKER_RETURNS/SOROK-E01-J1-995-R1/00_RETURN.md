# SOROK E01/J1 — three-head composition return

**Final status:** `J1_PARTIAL_EXACT_BLOCKER`  
**Packet:** `E01`, join `J1`, sourcefree grade `SOURCEFREE_S2_ONLY`  
**Failure class:** executable upstream causal chain, missing competent terminal child-event performer (D04/D05 seam).  
**Branch:** `codex/sorok-e01-j1-three-head-20261113-r1`  
**Code/test cut:** `c724d1a89626f3e177acd004c0be20029dc7ade4`  
**Final return head:** the commit containing this file (`git rev-parse HEAD` on the branch).

No protected merge, no fleet resume, no new server/controller/config, no credential or `.env` read, no CG-A `#982`/`#992` import or write, no self-review, no G5, no downstream dispatch.

## 1. Authority read

Read in full:

- `ISSUE_995_FROZEN.md` and the other three contract snapshots (`LATEST_939_SOURCE_CORRECTIONS.md`, `CGA_982_READONLY_BOUNDARY.md`, `CGA_992_READONLY_BOUNDARY.md`).
- The five original frozen programme files under `sorok-adversarial-programme-20261112-r1/frozen_sources`.
- `UM-SOROK R1` from `f5c43c80675f2556e1287bf55d25052d11e8746e`.
- Original `E01` packet from `227ce149fc7864c83c179a7d3ecaef2b92c5bdab` (`tasks[id=E01]`).
- B/C/D handoffs and code at the frozen heads, including `CG_B_RESULT_MATRIX.md`, `AGENT_A_RELAY_HANDOFF.md`, `AGENT_B_PARENT_UPTAKE_HANDOFF.md`, `D03_D04_SEAM.md`, `B04_B_TYPED_JOIN_ADDENDUM.md` and `B05_B_INTERLEAVE_ADDENDUM.md`.

## 2. Exact ancestry and composition

| Role | Exact commit |
|---|---|
| Common ancestor | `1510d835fcf0a35a5b352b27f4daf4b1f0bb6b34` |
| B | `1161e5f74081888bd813825b3df4afab3e2f5ca7` |
| C | `fa80f7a88533dabf70eda7a108e71dc377cbd910` |
| D | `85793cb74a9c2deb66570059a65b3f84b776c72e` |
| B into D | `7e9b3f7e2` |
| C into D+B | `58361bf20` |
| One truthfulness fix + J1 code/tests | `c724d1a89626f3e177acd004c0be20029dc7ade4` |

Verified: `1510d835...` is an ancestor of all three; B and C do not contain each other; D contains neither latest head. Merge bases: D-B `7663067647c945126d183c59cec6c6bfc8a09ab3`, D-C and B-C `1510d835...`.

Both merges were clean and `--no-ff`, preserving B and C as exact parents. After the merges, B's B01–B05 files match B's head byte-for-byte, C's parent/speech/P6 files match C's head byte-for-byte, and D's P3 files match D's head byte-for-byte. Full machine record: `SOURCE_DERIVATION.json`; human derivation: `SOURCE_DERIVATION.md`.

One bounded production edit after the merges: C's inherited `parent_decision.py` reported a `HOLD` action as `physical_admission="VALID_EMPTY"`. It now reports `"HELD"`, matching C's own C03/C04 ABI (`PERFORMED | VALID_EMPTY | HELD`). No refusal, test or currency/lock rule was weakened.

## 3. Mandatory conflicts resolved

- **Currency:** exact B head supplies parent/market/request currency equality and typed `P2_PARENT_PURCHASE`. The J1 `currency_mismatch` scenario decides `DECLINE` with `CURRENCY_MISMATCH`, buys nothing and debits nothing. B04/B05 inherited suites are green at the composition (43 passed), replacing C's frozen-cut 3 B04/B05 failures.
- **Lock order:** C's repaired order is preserved: B04 `_purchase_lock` then parent `_parent_write_lock`, calling the actual unlocked `_purchase_drum_kit`. The J1 performed-purchase positive completes without deadlock; C's inherited consumer and packet suites pass.
- **Period / rent:** B02 `period_progress` qualifies the parent decision. The J1 rent test materializes `period:2026-h1`, charges one 12-unit household rent, refuses a duplicate operation, and leaves parent cash untouched.
- **Parent vs household funds:** parent purchase debits parent cash only; household cash is unchanged. After rent, household affordability becomes `REFUSED_AFFORDABILITY` while a new parent proposal remains `PURCHASE` on parent funds. No conversion or shared budget.
- **Cold seals:** cold reopen yields the same P3 head, one purchase row, one utterance, the same D03 modes and no duplicate rent/P3 event. D03 `store_head.before == after`; no durable target.
- **P3 source pins:** D03's selected closure is unchanged and the J1 outer closure is verified in-test. A changed closure hash refuses. Fresh roots only; older P3 roots remain incompatible and were not migrated.

## 4. Executed tests and raw logs

All runs used `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python`, local pytest, no GitHub Actions. Environment: `oldMac.lan`, Darwin 22.6.0 x86_64, Python 3.11.3, pytest 9.1.1 (`evidence/environment.log`). Model: `opencode-go/deepseek-v4.1-flash`; account/quota/provider billing `UNOBSERVED`.

| Command scope | Result | Log |
|---|---|---|
| New J1 composition suite | **10 passed in 156.25s** | `evidence/j1_three_head_join.log` |
| B01+B02+B03+B04+B05 inherited | **43 passed in 442.42s** | `evidence/cg_b_combined_inherited.log` |
| D02 inherited (22) | **22 passed in 757.93s** | `evidence/d02_inherited.log` |
| D01 + D03 + selected P3 + P4 + P5 | **107 passed, 1 skipped in 309.04s** | `evidence/d01_d03_p3_p4_p5_inherited.log` |
| C02 inherited | **12 passed in 91.15s** | `evidence/c02_inherited.log` |
| C03/C04 consumer + C02/C03 packet | **14 passed in 224.48s** | `evidence/c03_c04_inherited.log` |
| C01 + P2/recursion inherited | **13 passed in 169.38s** | `evidence/c01_p2_inherited.log` |

Totals observed locally: **221 passed, 1 skipped**. All are at or after code cut `c724d1a8...`; the J1 suite was also rerun at that cut. No failure is hidden.

## 5. What the J1 suite proves

Positive (`test_j1_full_chain_and_cold_reopen`):

```text
B03 feasibility ADMISSIBLE
 -> C03 parent PURCHASE admitted
 -> B04 purchase PERFORMED (parent cash 100 -> 60; one ownership/one history row)
 -> C04 public SPEECH committed (one event)
 -> C12 child speech receipt
 -> normal P6 child_speech_experience via situated.recent_speech
 -> D03 immediate uptake, joint_check, store head unchanged
 -> later P3 response streams under the same P3 organization
 -> cold reopen: one purchase, one utterance, same modes, unchanged P3 head
```

Negative/counterfactual coverage in the same suite:

- tight space -> `REFUSED_SPACE`; noise -> `REFUSED_NOISE`; unknown acoustics -> `HOLD/UNKNOWN_ACOUSTICS`; insufficient parent cash -> `INSUFFICIENT_PARENT_CASH`; currency mismatch -> `CURRENCY_MISMATCH`;
- low household cash -> household feasibility `REFUSED_AFFORDABILITY` but parent purchase still performed on distinct parent funds;
- same actual speech under recognized vs imposed P3 histories -> `joint_check` vs `private_check`, and later P3 response streams match;
- child absent -> `NOT_PERCEIVED`; D03 `HELD_NOT_PERCEIVED`, no text/modes;
- altered receipt event/text/speaker -> exact refusal; severed event -> `CHILD_UPTAKE_EVENT_SEVERED`; parent decision remains readable and no P3 write occurs;
- hidden reason, parent cash and decision basis are absent from child/D03 public output; P6 user `view`/`say` do not expose the parent utterance (inherited C test);
- D03 `eligible_modes` are never promoted to an act.

## 6. Exact blocker and smallest next action

**Discovered missing performer:** no existing sourcefree owner or rule turns D03 `immediate_response` into a chosen, admitted, performed child event. D04 and D05 are `QUEUED_UNLAUNCHED`; `D03_D04_SEAM.md` requires an explicit target rule/writer and a distinct later performed consumer. The composed output therefore reports:

```text
subsequent_event.status = SUBSEQUENT_CHILD_EVENT_HELD_NO_COMPETENT_PERFORMER
subsequent_event.performed = false
subsequent_event.admitted_event = null
subsequent_event.eligible_modes_are_candidates_not_actions = true
```

**Smallest owner-specific next job:** one bounded successor packet with (1) D04 explicit sourcefree target/recruiter rule + smallest authorized target writer, and (2) D05 distinct later performed child-event consumer with a severance negative. Alternatively, one explicitly authorized sourcefree child-event performer with its own source/authority. It must consume D03 fields and must not relabel modes as actions. Until then, J1 remains a partial exact blocker. Details and reproduction: `J1_SEAM_BLOCKER.md`.

## 7. Dependency impact

Machine matrix: `DEPENDENCY_IMPACT.json`; compact delta: `PROGRAMMA_DELTA.json`.

- B01–B05: preserved; B04 currency and B05 rent are now composed with C03/C04.
- C01–C04: preserved; one HOLD label corrected; C04 normal P6 child experience is the J1 perception input.
- D01–D03: preserved; D03 is connected, still read-only and durable-formation `MISSING_RULE`.
- D04/D05: absent and blocking the terminal J1 act.
- E01/J1: upstream chain proven, terminal performed event held.
- E02/J2 and downstream: not started. No CG-A `#982`/`#992` overlap or write.

## 8. Artifacts

- `j1_join.py`, `test_j1_three_head_join.py`
- `SOURCE_DERIVATION.md`, `SOURCE_DERIVATION.json`
- `PROGRAMMA_DELTA.json`, `DEPENDENCY_IMPACT.json`
- `J1_ABI.md`, `J1_SEAM_BLOCKER.md`
- `evidence/*.log` (commands/results/environment)

## 9. Honest limits

- Sourcefree engineering only. No native CAN/ADP/PYAT psychology, no actor/human/science/rights acceptance, no protected merge, no independent G5.
- Parent speech text and hidden reason remain caller-supplied; no parent language-generation owner exists.
- P3 source pins are selected-file-level, not a Byzantine whole-repo signature.
- Older P3 roots remain incompatible; no migration.
- Provider token/USD cost is `UNOBSERVED`; only local pytest wall times are claimed.
- No claim that the child actually chose or performed a later event; that is exactly the held seam.
