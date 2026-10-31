# Integration and rollback

## Integration status

**NOT INTEGRATED. NO PRODUCTION MERGE. NO PRE-MAIN WRITE.**

- Branch: `agent/pyat-r3-pe-sc0-eight-strict-failure-repair-20261031-r1`
- Startup: `5fc1d43e3d5412194d1f1eaa30ff448f84635e99`
- Write surface: only
  `WORKER_RETURNS/PYAT-R3-PE-SC0-EIGHT-STRICT-REPAIR/`
- The pinned PE module, original strict court, author court, production fixture,
  `rawlsing_next/` and PRE-MAIN are unchanged.
- The only fixture change is the test-only support patch in this return, applied
  to a disposable extracted tree.

The overlay is not production wiring. It is injected by `sitecustomize.py` only
when the temporary court tree is on `PYTHONPATH`. It must not be installed
globally or added to a production environment.

## Reproduce the court

From this return directory:

```bash
./repro/run_original_red.sh
./repro/run_overlay_courts.sh
```

`run_original_red.sh` extracts the exact PE commit and shows the preserved
**21 author passed / 4 strict passed / 9 strict failed** baseline.

`run_overlay_courts.sh` extracts the same commit, applies only the test fixture
support patch, copies the overlay and HQ298 port, and shows:

- author: **21 passed**
- strict: **13 passed**
- overlay positive/fault negatives: **9 passed**

Both scripts use `mktemp` and remove the temporary tree unless
`KEEP_WORK=1` is set.

## If an owner wants to integrate the semantics

This return does not authorize or perform integration. A lawful successor
would need:

1. A new PE contract revision owned by the original PE/SC0 owner.
2. Real owner-provided N9 values, not HQ298 fixture values.
3. An exact source/release and N9 issuer authority trail.
4. A real reversal issuer registry entry, not the test-only fixture snapshot.
5. Real H2 publication/binding refresh semantics, not fixture generation-zero
   receipts.
6. A production consumer decision and actor/person boundary review.
7. A new strict court pin for the successor blob; the current pin
   `58484f4c...` must not be silently changed.
8. Independent I3 hostile review at the exact pushed SHA.

Do **not** satisfy a production request by shipping `sitecustomize.py`, the
test fixture authority patch, or copied fixture values. Those are evidence
artifacts only.

## Rollback

### This return

Nothing outside the return directory was changed, so rollback is simply to
stop using or delete this branch/return. No production rollback is required.

If a reviewer checked out this branch, it can be removed without touching
PRE-MAIN:

```bash
git worktree remove --force /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-r3-pe-sc0-eight-20261031-r1
```

Do not run that command while retaining uncommitted work.

### Temporary court tree

`repro/run_original_red.sh` and `repro/run_overlay_courts.sh` clean their own
`mktemp` trees on exit. To inspect, rerun with `KEEP_WORK=1` and remove the
printed `COURT_TREE` manually.

### Overlay injection

If `sitecustomize.py` or the overlay path was accidentally placed on a global
`PYTHONPATH`, remove that path. The original PE module then runs without the
overlay and returns the preserved 4/13 strict red; no hidden receipt enrichment
remains.

### Future integrated successor

If a future owner integrates a successor and later needs to roll back, revert
only that successor's source commit through the owner's normal review process.
This branch has no production commit to revert.

## Verification/readback

After push, verify the remote branch directly:

```bash
git ls-remote origin refs/heads/agent/pyat-r3-pe-sc0-eight-strict-failure-repair-20261031-r1
```

The exact pushed tip SHA is reported in the completion message and is
intentionally not self-referenced inside its own commit.

Required readback:

- remote branch SHA equals `git rev-parse HEAD`;
- `git status --short` shows only this return directory before commit;
- `git diff --name-only 5fc1d43e...HEAD` shows no `rawlsing_next/` or PRE-MAIN
  source mutation;
- the six required files are present;
- `repro/test_summary.json` matches the served receipts.

## Risk register

| Risk | Control |
|---|---|
| Overlay mistaken for production PE repair | Explicit grade, no source edit, no merge, integration section forbids global install |
| Fixture values mistaken for real N9/source | `TEST_FIXTURE_ONLY`, synthetic refs, provenance on every receipt, science hold |
| Test fixture authority grant mistaken for real issuer | Patch is test-only; forged reversal refuses; no production registry change |
| SC0 54/60 baseline mistaken for PE geometry | `n10e_values_read_receipt` copies actual PE cells; tests assert 48/64 and 21/30 |
| Hidden source/actor promotion | Binding echo `may_use_as_source_observation: false`; `person_generation: NONE`; fault test rejects promotion |
| Stale receipt after invalidated current | Original PE refusal path preserved; fault test confirms no enrichment |
| Missing producer/consumer silently green | Fail-closed overlay validation; four targeted fault negatives |
| Test assertions changed to obtain green | Strict blob `d2fe653d...` unchanged; only fixture support patch is disclosed |
