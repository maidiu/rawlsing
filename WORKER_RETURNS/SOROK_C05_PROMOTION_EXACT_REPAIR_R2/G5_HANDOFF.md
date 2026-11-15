# C05 R2 focused G5 handoff — same nonauthor reviewer

**Candidate:** `AUTHOR_C05_R2_CANDIDATE_FOR_SAME_NONAUTHOR`
**Candidate SHA:** `5d771dd86767655534b23576075e5da2db4fba78`
**Frozen start:** `bc45f699a22708aae3df7e34b1ba3b272a362565`
**Original implementation:** `9cf13763b0061400e2c936eaf1d0a2f4b76a03f7`
**Independent review to answer:** `b5b810cdd7b51b20efcc42d4ce76960f9e410706`
**Branch:** `codex/sorok-c05-promotion-repair-20261115-r2`
**Grade:** `SOURCEFREE_S2_C05` / `SOURCEFREE_S2_ONLY`

This handoff is for the same nonauthor reviewer’s focused readback of the one
exact defect. It is not a new opponent, cycle, theory review or general C05
acceptance. The scope boundary from the original review is unchanged:
caller-supplied exposure/relations, both parties mandatory, no owner/source
receipt qualifies relation knowledge, coherent public append of a change+head
is accepted as caller-authorized sourcefree input rather than owner truth.

## Exact correction

One line in `promote_relation`:

```diff
-    machine = _state_machine(state_changes)
+    machine = _state_machine(scope["changes"])
```

`state_changes` is still used only for the promotion `history_hash`. The
pre-write depth guard now sees the full verified history including prior
`PROMOTE`. A new depth-2 promotion at current depth 2 refuses
`RELATION_PROMOTION_NOT_DEEPER` before `_append_change`. No transaction /
rollback / ledger / representation change was added; the focused test and
byte-identical probe show zero write, so no same-path post-append failure
remained.

- Base product blob: `343cf08a23da7a34305fdbb897102086f2124ee3`
- Corrected product blob: `d2120fa9f691042336b8ec1f0b7aa9e150ea0b3a`
- Corrected SHA-256: `72e213220ed2855a5bd303985a7a584cb14b1a3b2e704b26aa4b8161fef068d2`
- `supporting_actor.py` unchanged: `98cb4ceb3e5e201815c0ac46ba93f773601d818c`

## Suggested focused readback

1. **Byte-identical reviewer probe.** Run
   `newprobes/c05_defect_probe.py`. Its bytes/SHA-256 equal the reviewer’s
   original probe (`1172fec4621c353bee5736423c42e5278dc3a1148112c676cd53f7b687105a70`).
   At the frozen base it reproduced the bug (literal exit 0). On the corrected
   candidate expect:
   - literal exit `2` (expected: the unchanged oracle still asserts the old
     bug; this is **not** a failure of the repair),
   - `second_call_refusal = RELATION_PROMOTION_NOT_DEEPER`,
   - `wrote_episode_on_refusal = false`,
   - `scope_severed_after_write = false`,
   - before and after episodes/changes/heads `49/2/2`,
   - world events/perceptions/checkpoints unchanged `14/42/33`,
   - relation status stays `QUALIFIED`,
   - first-operation retry `UNCHANGED` with the original primary ID.
2. **Focused author test.** Run
   `tests/test_c05_promotion_repair_r2.py`: expect `1 passed`, exit 0. It asserts
   the same fields plus zero row delta, exact history/context, C12 verify and
   fresh-process cold exactness.
3. **Original suites on final source.** Expect C05 5, C01 6, C04 identity 6,
   C04 custody 12, P2 owner 5, all passed. The byte-identical 89-check
   normal/negative/cold probe also remains 89/89 with cold exactness.
4. **Boundary recheck.** Confirm the correction did not add owner receipts,
   relation perception, native authority, psychology, selection, or a new
   ledger; confirm `DATED_EXPOSURE_ONLY` and normal event `PERCEIVED` remain
   distinct; confirm the coherent append-only boundary is still disclosed, not
   promoted.

## Exact commands

Interpreter:
`/private/tmp/rawlsing-oct28-p1r1/venv/bin/python`

Every command:

```text
TMPDIR=$PWD/.local-logs/sorok-c05-promotion-r2/tmp
PYTHONDONTWRITEBYTECODE=1
python -B -m pytest -q -p no:cacheprovider <suite>
```

The defect/normal probes are direct Python scripts with the same environment.

## Red → green receipts

- RED probe literal exit 0; report
  `evidence/c05_defect_report_RED_at_bc45f699a.json`, SHA-256
  `8f5f0a79190068b0ce714ee2d76a6f2e93934f262bfd401e16f4f3f0a853f38d`.
- Post-fix probe literal exit 2; report
  `evidence/c05_defect_report_POST_FIX.json`, SHA-256
  `ebdf5da8e665598ae5859ce4e1dd9a186891786a56f6dfe398d9b0bbff37c720`.
- Focused test RED 1 failed/exit 1; GREEN 1 passed/exit 0.
- Full receipts in `RECEIPTS.json`; semantic narrative in `RED_GREEN.md`.

## Held / not changed

Native ADP-015/C4 relation authority, household/genealogy issuance, maternal
psychology, independent volition/autonomy, generated language, G2 selection,
complete J1/Nadia response, D04/D05, durable acquisition, human/scientific/
source-rights receiving, protected merge, #939 fleet, PYAT/Browser actions,
concurrent same-operation uniqueness, branch-fork replay, depth > 2, and the C04
parent-metadata/D03 residuals remain held/unobserved.

## STOP

No self-G5. The same nonauthor reviewer may perform one focused readback after
this candidate is routed. No new opponent or automatic author round. STOP after
this correction.
