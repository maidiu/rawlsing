# SOROK G17 — material-conserving historical continuation and independent lives R1

## 0. Sealed-startup amendment custody

The sealed startup tree at `f68512d05a0d10c7711ca7149f2e12bf891eb6de` contains
only `WORKER_COMMISSIONS/SOROK-20261019-G17-MATERIAL-HISTORY-INDEPENDENT-LIVES-R1/00_COMMISSION.md`.
No `01_...` amendment object was present in the fetched local object store. The
user-supplied 01 amendment text was followed verbatim; the old seal was not
rewritten. HQ should reconcile the HQ-published 01 ref if it exists on another
ref before treating this return as fully amendment-bound.

**FINDING: the G15/G16I material/current-state seam was not conserving current
stock, time or participation. G17 repairs the eight directly material,
participation, time, future-source and joined-terminal defects. The M2 archive
and MP known-counterpart demands are admitted as exact typed coverage HOLDs,
not fabricated positives. The 181/67/75 inherited counts and the entire original
17 + 56 RED set are preserved unchanged. A bounded sourcefree C9 material
handoff is executable; full C9 E1/RULE_A/RULE_T/E2 remains HOLD.**

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Branch | `agent/rabochii-sorok-20261019-g17-material-history-and-independent-lives-r1` |
| Sealed startup | `f68512d05a0d10c7711ca7149f2e12bf891eb6de` |
| G15 parent | `fbc84ba4b5ec8befcf7954357a2ba1c576f5d7a5` |
| G16I review | `683aa56828cda76ea70792a2c8b39cf78624e8dc` |
| Candidate evidence | `a35403cede4f65134da340d46f198f92723db410` |

## 1. Terminal delta

| Court | Before G17 | After G17 |
|---|---:|---:|
| G13 historical 181 (same frozen IDs) | 108 PASS / 73 RED | **108 PASS / 73 RED** |
| G14 on G13 67 | 67 PASS / 0 RED | **67 PASS / 0 RED** |
| G15 prospective author 75 | 75 PASS | **75 PASS** |
| G16I independent 24 | 14 PASS / 10 RED | **22 PASS / 2 RED = 8 repaired + 2 typed coverage HOLD** |
| G17 material consumer court | — | **13 PASS / 0 RED** |
| C9 material handoff | — | **2 PASS / 0 RED; full E1/E2 HOLD** |

The 73 G13 REDs are the **same exact IDs** as the G15 baseline: 17 original
REDs plus all 56 G16I compatibility IDs. No frozen test, waiver or relabelling
was used. The 56 classifications and scientific meanings are preserved in
`evidence/compatibility_56_after.json`; the original 17 preservation is in
`evidence/original_17_after.json`.

## 2. Material/current-state repairs

The candidate state now carries a real versioned current ledger:

* `WORLD_MATERIAL` initialises `material_remaining`; `PROJECT` consumes that
  current stock, not the unchanged world root. A repeated project cannot spend
  6 from stock 5; the second claim is refused with
  `PROJECT_PERFORMANCE_CLAIM_MISMATCH` and the state remains at 2 remaining
  after the lawful 3-unit project.
* `SCHOOLING` checks and decrements current `free_hours`, not the ORIGIN root's
  initial hours. Repeated 30-hour training is refused
  `TRAINING_TIME_UNAVAILABLE`; negative time is impossible.
* `PEER_ROOT`/`PEER_ACTION` carry current `tools_remaining`; a second 2-unit
  return from stock 3 is refused `PEER_TOOLS_UNAVAILABLE` (2 returned total,
  1 remaining).
* All history events require exactly one actor; a silent unperformed second
  participant is refused `SINGULAR_EVENT_REQUIRES_ONE_ACTOR`.
* `continue_person` no longer trusts a caller after-state. It requires the
  actual material event, recomputes cash/free-hours/completed-units, and refuses
  a forged +100000 cash after-state or a participation at effective 1101 as a
  parent of the continuation at 1000.
* `run_pipeline` refuses future-child partition names in the visible joint
  material/context before any proposal, selection, construction or COMMITTED
  causal output: terminal `FUTURE_CHILD_INFORMATION_LEAK`.
* On joined construction failure, the actual failed attempt events are returned
  for evidence, and the terminal cannot COMMIT a second-parent history that
  overspends the material stock (spent 6 > available 5 → `HISTORY_SEARCH_EXHAUSTED`).

These are conservation/authentication/time repairs, not a new psychological
law. The positive material remainder still performs 2 units after the lawful
3-unit project (completed 5), and the independent 2-vs-5 material lives still
reach the same legitimate endpoint with distinct completed work/formation.

## 3. M2 / MP — exact typed coverage HOLD

**M2:** the frozen archive is read-only and hash-pinned, but its 23 historical
events are not replayable under the current G15/G17 event grammar (owner
identity failure; no current `WORLD_MATERIAL` root). G17 does **not** rewrite or
replay that grammar, does not generate a child, and returns
`maternal_continuation_admitted = False`, `continuation_events = []`, with
`LAB_OLDER_CHILD_O1` unchanged. Status: **TYPED_COVERAGE_HOLD_ARCHIVE_GRAMMAR_INCOMPATIBLE**.

**MP:** `F_EXISTING` and `REL_ADMITTED_F_EXISTING` are exact archive refs, but no
source-qualified second-parent history for F_EXISTING is materialised. G17 does
not mint `LAB_SECOND_PARENT_CAND_*` as F_EXISTING, does not duplicate the actor
or event, and preserves the exact `SHARED_HISTORY_CONTRADICTION_HOLD` with
`no_duplicate_actor_or_event=True` and unchanged mother history. Status:
**TYPED_COVERAGE_HOLD_KNOWN_COUNTERPART_HISTORY_NOT_MATERIALIZED**.

These two account for the 2 REDs in the G16I 24 court; they are admitted
coverage HOLDs, not material defects and not fake positives.

## 4. C9 material handoff

`c9_handoff_consumer.py` reads an actual performed material action, checks the
material event is an actual causal parent, recomputes the after-state, and
refuses a severed material parent (`SEVERED_MATERIAL_SOURCE`) or a nonconserving
after-state. It issues no route probability, selection weight, person, child or
E2 authority. `e2_later_authority = HOLD_UNISSUED`.

This is a material handoff only. Full C9 E1/RULE_A/RULE_T/E2 remains a separately
owned HOLD (see §7).

## 5. Falsifiable same-edge proof

Seven sibling-witness claims, all with baseline PASS and same-node assertion RED:

| Claim | Fault | Result |
|---|---|---|
| `G17_STOCK_LEDGER_EDGE` | project ignores `material_remaining` | `TARGET_ASSERTION_FAILED` |
| `G17_FREE_HOURS_CLOCK_EDGE` | schooling checks root hours | `TARGET_ASSERTION_FAILED` |
| `G17_TOOL_STOCK_EDGE` | peer action checks initial tools | `TARGET_ASSERTION_FAILED` |
| `G17_PARTICIPATION_AFTERSTATE_EDGE` | forged after-state accepted | `TARGET_ASSERTION_FAILED` |
| `G17_FUTURE_CHILD_PARTITION_EDGE` | future-child guard disabled | `TARGET_ASSERTION_FAILED` |
| `G17_JOINED_TERMINAL_STOCK_EDGE` | joined terminal overspend | `TARGET_ASSERTION_FAILED` |
| `G17_C9_MATERIAL_HANDOFF_EDGE` | material parent check disabled | `TARGET_ASSERTION_FAILED` |

The shared proof gate returned
`MECHANICAL_PROOF_GATE_PASS_NOT_SCIENTIFIC_ADOPTION`; all sources were restored.
Post-gate cold G17: **13/13 PASS** at seeds 0 and 1; post-gate G16I 24: **22/2
expected HOLD**; post-gate G15 75: **75/0**; post-gate 181: **108/73 same IDs**.

## 6. Three independent dispositions

**ENGINEERING — BOUNDED_ACCEPT.** 8/10 G16I material/participation/time/future/
terminal counterexamples repaired; 2/10 typed coverage HOLD; 181/67/75 preserved;
7/7 proof witnesses; C9 material handoff accepted at its bounded grain. Full C9
E1/E2 and physical C11 are not claimed.

**SCIENTIFIC — BOUNDED_ACCEPT_METHOD / GENERAL_HOLD.** Current material
conservation, authenticated performed action/time and materially different
finite lives are demonstrated at the tested sourcefree grain. No calibrated
psychological rate, native person, parent, child, biology or general life
formation is established. Independent material 2/5 histories are real finite
variation, not general population science.

**AUTHORITY — HOLD.** No original survey/source, native person/child/biology,
model/actor issuance, ADP/CAN rule, RULE_A/RULE_T, C9 E2, N11/N12, V3, C11 weld
or production adoption is issued. The original 17 REDs and all 56 compatibility
REDs remain historical evidence; this worker cannot self-adopt.

## 7. Proposed action and owner

1. Sorok HQ intake of this bounded material repair and the 56/17 preservation map.
2. Competent ADP015/020/CAN008/CAN011 or Sorok HQ owner: materialise a
   source-qualified M2 continuation grammar and MP F_EXISTING second-parent
   history, or formally accept the two typed coverage HOLDs. Do not fabricate
   the missing history.
3. C9P/C9PI and the CAN/ADP owners: issue the C9 E1/RULE_A/RULE_T/E2 authority;
   the current handoff remains `HOLD_UNISSUED`.
4. A later independent I2/HQ scientific acceptance; G17 is not self-accepted.

## 8. Evidence and cost

JUnit: `evidence/g15_181_post_gate/` (181 = 108/73), `evidence/g15_75_post_gate.xml`
(75/0), `evidence/g16i_24_post_gate.xml` (22/2 HOLD), `evidence/g17_post_gate_cold_0.xml`,
`evidence/g17_post_gate_cold_1.xml` (13/0), plus pre-gate copies.
Source/custody: `evidence/source_custody.json`,
`evidence/material_court_receipts.json`, `evidence/coverage_matrix.json`,
`evidence/compatibility_56_after.json`, `evidence/original_17_after.json`.
Proof: `tests/test_g17_material_history_consumer.py.proof.json`,
`evidence/proof_gate_changed_receipt.json`.
Candidate: `candidate/lab_sgi1/` (19 modules), `candidate/data/`,
`candidate/run_candidate.py`, `c9_handoff_consumer.py`.

Local warm Git/pytest, no paid API call observed; cash/quota **UNKNOWN**. Final
remote reviewer SHA is verified by direct `git ls-remote` readback and bound in
`PUBLICATION_RECEIPT.json`.

**C4:** bounded material/current-state and independent-life method repair;
full scientific genealogy HOLD. **C9:** material handoff only; E1/E2 HOLD.
**C12:** no pipeline-generated native person. **C11:** not welded.
