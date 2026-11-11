# External postcommit evidence boundary

## Required distinction

The final `MCR_COMPLETION_EVIDENCE_BEGIN/END` block must bind the exact candidate
SHA while remaining outside that candidate's defining commit. A file committed in
the same tree cannot be cryptographic proof that it was emitted after that commit.
The validator therefore enforces only what repository/file evidence can support:

- exact candidate checkout;
- contract/source identity and 12-ID no-drop;
- committed per-ID output/evidence bytes and digests at the candidate;
- evidence return path is not tracked at the candidate.

It does **not** claim wall-clock ordering, author identity, CI provenance or
stronger external publication. The result field is explicitly
`REPOSITORY_TRACKING_ONLY__NO_TIMESTAMP_OR_STRONGER_PROVENANCE`.

## Corrected commands

Pre-dispatch:

```
python3 CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py \
  WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/MCR_EXECUTABLE_LAUNCH.md
```

Final return:

```
python3 CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py \
  WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/MCR_EXECUTABLE_LAUNCH.md \
  --verify-return RECEIVING_EVIDENCE.md \
  --candidate-sha "$(git rev-parse HEAD)" --evidence-root .
```

`RECEIVING_EVIDENCE.md` must be untracked at the candidate or outside the
candidate checkout. A PR/CI comment surface can be represented by a separately
materialized external evidence file with equivalent repository exclusion; no
new checker or authority gate is created.

## Historical original

The frozen `PYAT_W03_W04_MCR_C_Commission.md` remains immutable with SHA-256
`ddc6273adcc9aeb1b7e75c7d82897dde929adffea152e7f57dc5254fa32f0166`.
Its original `no_drop_check` command is preserved as historical text and returns
RED on the unfenced file. The executable presentation is the separate launch
artifact; the original is not claimed to have passed.

## Limits

- No final `RECEIVING_EVIDENCE.md`, delivered IDs, 12 same-head PASS records or
  final postcommit block is fabricated here.
- No whole-MCR acceptance; final same-SHA code/economic receiving remains open.
- CC-F01/F02/F03/F04 and economic measurements remain outside this repair.
