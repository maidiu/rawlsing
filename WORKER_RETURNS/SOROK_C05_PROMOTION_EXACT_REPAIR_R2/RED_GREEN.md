# C05 R2 immutable RED → corrected proof

**Frozen start / defect base:** `bc45f699a22708aae3df7e34b1ba3b272a362565`
**Defective product blob:** `343cf08a23da7a34305fdbb897102086f2124ee3`
**Corrected product blob:** `d2120fa9f691042336b8ec1f0b7aa9e150ea0b3a`
**Exact correction:** one line in `promote_relation`:

```diff
-    machine = _state_machine(state_changes)
+    machine = _state_machine(scope["changes"])
```

`state_changes` is still used only for the promotion `history_hash` (state
entries, excluding prior `PROMOTE`). The pre-write depth guard now sees the full
verified change list including prior `PROMOTE` episodes.

## 1. Independent reviewer defect probe (byte-identical)

The reviewer’s probe was copied byte-identically to
`newprobes/c05_defect_probe.py`.

- Source: `WORKER_REVIEWS/SOROK_C05_CONTINUING_RELATIONS_G5_R1/newprobes/c05_defect_probe.py`
- Copied blob: `31a888cb9189686d321f29ab27e95aa8fe5f9d9e`
- Copied SHA-256: `1172fec4621c353bee5736423c42e5278dc3a1148112c676cd53f7b687105a70`
- Reviewer-source SHA-256: `1172fec4621c353bee5736423c42e5278dc3a1148112c676cd53f7b687105a70`
- Byte-identical: yes. Expectations/oracle were not edited.

### Base RED (before correction)

Command (literal exit **0** means the reviewer’s bug oracle reproduced):

```text
TMPDIR=$PWD/.local-logs/sorok-c05-promotion-r2/tmp \
PYTHONDONTWRITEBYTECODE=1 \
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
WORKER_RETURNS/SOROK_C05_PROMOTION_EXACT_REPAIR_R2/newprobes/c05_defect_probe.py
```

Literal exit: `0`.

| Field | Base RED |
|---|---|
| `second_call_refusal` | `RELATION_CUSTODY_SEVERED` |
| `wrote_episode_on_refusal` | `true` |
| `scope_severed_after_write` | `true` |
| `c12_verify_unchanged` | `true` |
| before episodes/changes/heads | 49 / 2 / 2 |
| after episodes/changes/heads | 51 / 3 / 3 |
| before/after world events | 14 / 14 |
| before/after perceptions | 42 / 42 |
| before/after checkpoints | 33 / 33 |
| before relation status | `QUALIFIED` |
| after relation status | `HOLD_CUSTODY_SEVERED` |
| first-promotion retry after write | `RELATION_CUSTODY_SEVERED` |

Immutable report:
`evidence/c05_defect_report_RED_at_bc45f699a.json`
SHA-256 `8f5f0a79190068b0ce714ee2d76a6f2e93934f262bfd401e16f4f3f0a853f38d`.

### Post-fix (same probe bytes)

Literal exit: `2` — expected, because the probe’s own oracle still asserts the
old bug (`RELATION_CUSTODY_SEVERED` + write + sever). The literal exit is
preserved separately; the field-level semantic result is corrected.

| Field | Post-fix |
|---|---|
| `second_call_refusal` | `RELATION_PROMOTION_NOT_DEEPER` |
| `wrote_episode_on_refusal` | `false` |
| `scope_severed_after_write` | `false` |
| `c12_verify_unchanged` | `true` |
| before episodes/changes/heads | 49 / 2 / 2 |
| after episodes/changes/heads | 49 / 2 / 2 |
| before/after world events | 14 / 14 |
| before/after perceptions | 42 / 42 |
| before/after checkpoints | 33 / 33 |
| before relation status | `QUALIFIED` |
| after relation status | `QUALIFIED` |
| first-promotion retry after refusal | `UNCHANGED` with original primary ID |

Post-fix report:
`evidence/c05_defect_report_POST_FIX.json`
SHA-256 `ebdf5da8e665598ae5859ce4e1dd9a186891786a56f6dfe398d9b0bbff37c720`.

Logs:
`evidence/logs/c05_defect_probe_RED.stdout.log` and
`evidence/logs/c05_defect_probe_POST_FIX.stdout.log`; timings in the matching
`.time.log` files.

## 2. Focused author assertion test (same path)

Test:
`tests/test_c05_promotion_repair_r2.py`

It asserts:

1. first depth-2 promotion succeeds (`RECORDED`, depth 2);
2. the same original operation retry returns `UNCHANGED` with the same primary
   episode ID and no row delta;
3. a different new operation at depth 2 on the already-promoted scope refuses
   `RELATION_PROMOTION_NOT_DEEPER`;
4. episode/change/head/world-event/perception/checkpoint counts are unchanged;
5. dated history and the real-event relation context remain byte-exact and
   `QUALIFIED`;
6. the original operation retry still returns `UNCHANGED`;
7. C12 store verification remains `ok`;
8. a fresh process reopens with exact history/context/counts and an `UNCHANGED`
   original-operation retry.

### RED before correction

`evidence/logs/c05_r2_focused_RED.log`
SHA-256 `05c3c1951ba1abfdcd5616fd03774683cc91cbebe8aea22eb8678ae1de52c969`

Result: `1 failed`, exit 1. Failure was the exact defect: expected
`RELATION_PROMOTION_NOT_DEEPER`, actual `RELATION_CUSTODY_SEVERED`.

### GREEN after correction

`evidence/logs/c05_r2_focused_GREEN.log`
SHA-256 `95e2c4474bc480f1c3ef3eff6544101cd20cd3b43773ca6f12400f84c083ce71`

Result: `1 passed`, exit 0.

## 3. Normal/negative/cold independent 89-check probe (byte-identical)

The reviewer’s full normal/negative/cold probe and its two helper imports were
copied byte-identically:

| File | Git blob | SHA-256 |
|---|---|---|
| `newprobes/c05_probe.py` | `c89e22a7c4ba683fe99994f2833b8b710e888401` | `1f44fef5f7648215db72eed2cc805f778cfbbadda0c9a830ea592397c5132fb7` |
| `newprobes/c05_observe.py` | `e588b00afed41d4556a63497a3f9aa8b57ace66f` | `94cfa307161df9597103e01617a1625359213a7f71c4e48befb1ab4106f40850` |
| `newprobes/c05_cold_child.py` | `7feae9d8091d65fec612dddd4051f3b00e3a3bbc` | `230d85a841f96161b4033244ad6206992e66c8bda681026fa85bbbc58dfbb8ff` |

Each SHA-256 equals the reviewer’s source byte-for-byte. Oracle and fixtures
were not rewritten. Result after the correction: **89/89 checks pass**, exit 0,
cold child exit 0, cold snapshot exact, cold retry `UNCHANGED`. Report
`evidence/c05_probe_report.json` SHA-256
`b072782c595876485e1a92c2699c7768d8ac017cb03fb99276fdbf8b633f6a7d`.

The probe’s `coherent_append_only_relation_accepted` observation is the
reviewer’s pre-existing disclosed boundary: a caller able to append a coherent
change+head through the public C12 store is accepted as caller-authorized
sourcefree input. It is not owner authentication, independent perception,
native ADP-015/C4 authority or actor truth. It is not a new claim or a repaired
defect.

## 4. Isolation note

The reviewer probes hardcode
`.local-logs/sorok-c05-independent-g5/` (including the 89-check probe’s
cold-child `TMPDIR`). To keep writes inside the R2 lease, a temporary symlink
redirected that path to
`.local-logs/sorok-c05-promotion-r2/probe-red-scratch/`. Probe bytes and
oracles were not edited. The RED report was copied to its immutable name before
the post-fix run overwrote the probe’s default report path.
