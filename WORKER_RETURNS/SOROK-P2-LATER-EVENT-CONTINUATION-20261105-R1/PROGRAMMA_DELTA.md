# PROGRAMMA_DELTA — SOROK P2 later-event continuation repair

**Delta ID:** `SOROK-P2-LATER-EVENT-CONTINUATION-20261105-R1`
**Repair base:** `76fdb624afc7674f088d10c349bfe15ffd0b865a` (immutable)
**Reviewer:** `f1a2872487b3aa492632a497ad7481e8529d937e`
**Product base:** `41bf45813fd0adeffd9b54e1306c2022abe96514`
**Result:** `PASS` focused public-boundary repair.

## Delta

- Public CLI/API now emits an allowlisted public projection/summary with zero
  projection privacy-walker hits. Internal `c9`/`s43`/plan/source/history/
  readset/root fields are available only through separate `*_engineering`
  evidence or `--engineering-out`.
- Observation/default `positive`/`scheduled` no longer calls `project_do_help`.
  Explicit `--do-help` (or `project_do_help()`) executes the user attempt and
  reports the encounter increment.
- Preserved causal primitives and S43/S47 source semantics:
  `produce_input_interval`, `admit_later_event`, `read_later_event`,
  `cold_read`.
- Focused public positive, explicit action, cut/restore, cold/source-intact
  checks pass; 8 focused tests.
- Historical `76fdb624a` evidence remains immutable and accessible in git.

## Not changed

- No product/vendor/projection/fanin/lifecycle/interval/PROGRAMMA working-file
  edit; no protected write or PR697 merge.
- No native C8/C9/C12, CAN008/CAN011, ADP, Pyat or human grant.
- No new motive, rule, weight, world schedule or general absence-life feature.

## Next owner action

Independent review of the exact repair commit and adoption of the public
observation API plus explicit `--do-help` action by HQ fan-in.
