# SOROK P2 FINAL CUT — INDEPENDENT QUALIFICATION

## VERDICT

**ACCEPT_SCOPED_TEST_ONLY** for final integrated head `4b2fed81c3f513eb4262ad5de277ce519c74c614`.

Actual compatibility holds. This is not a blanket acceptance of older standalone surfaces, not a native/human/security grant, and not a protected merge.

## PRESERVED CUTS

- Accepted integrated `25d40806` — review `332e00cb` ACCEPT_SCOPED_TEST_ONLY.
- Interval repair `76d5a3d13e0219c1a085ebadd55071de2dd90e7d` — review `3e04b6c7` ACCEPT_SCOPED_TEST_ONLY.
- Later repair `b71624f21d0bc638e8817f3929cc6c01ab8b0f61` / code `4bdba46c` — review `3e04b6c7` ACCEPT_SCOPED_TEST_ONLY.
- Old interval `7a`/`89b334` REVISE, old later `76`/`f1a287` REVISE, historical `bdad` REVISE remain preserved.

## ACTUAL 25d → 4b2 COMPATIBILITY

- Delta is exactly 73 files, all under the P2 interval/later/fanin returns; zero non-P2/product path changes.
- `p2_product_fanin` code, `run_fanin_cli.py` and fanin tests are unchanged between accepted `25d` and final `4b2` (`0` diff files).
- Imported component trees at `4b2` exactly match accepted repair sources:
  - lifecycle `79b90e4` tree `1eda53e4`
  - interval `76d5a3d1` tree `f7bd1c51`
  - later `b71624f2` tree `67f01db8`
- Product and projection trees are unchanged. Fanin authored source manifest: `12/12` files hash-match.
- First-consumer call compatibility confirmed: repaired interval still exposes the `apply_explicit_interval` ABI used by fanin; repaired later primitive methods remain compatible; fanin uses its own public opportunity allowlist and explicit lifecycle DO_HELP. No new unreviewed logic is imported into the fanin.
- Fanin source metadata authored before review still labels component closures pending; exact trees are now accepted by `3e04b6c7` and this final-cut review. No code change.

## EXACT EXECUTED PROBE (FINAL HEAD)

Snapshot was extracted only under `.local-logs/p2-final-cut-review/` from Git at `4b2fed81`.

```text
python3 -B .local-logs/p2-final-cut-review/probe_fanin_final.py
# all CLI/callable checks true
```

Verified on exact `4b2`:
- Imports/origins pinned to final snapshot; same `S47Session` across fanin/lifecycle/interval/later; typed components valid.
- Public CLI allowlist clean: no `root_hash`, `root_id`, private projection keys or forbidden markers.
- Interval/later/opportunity observation: no auto DO_HELP; encounters `0 -> 0`.
- Explicit DO_HELP: exactly one canonical attempt, `0 -> 1`; ACTUAL refuses.
- Outside cold block and local return: no canonical store/world/clock mutation.
- Later event 3 history uses event 2; exact C9 source preserved; S43 language ACCEPTED; cold continuity true.
- Public final CLI `new`, `say`, `exit`, blocked SAY, `return`, final `verify` all pass.

Reused: accepted `25d` 7-test/cold-probe evidence and `3e04` focused repair oracles. NOT_RUN: full 7/8/6/55 suites, broad source census, new framework/unrelated probes.

## SIMULTANEOUS FINAL RECEIVING DELTA

Published record `a61dab8343181b0975c76496d0007e2b3a92bba0` was inspected because it is actually published at origin. It adds only its receiving-return directory; no product change. It explicitly states it is not independent acceptance and not merge permission, and that final head `4b2` was not independently accepted at author time. Its guide portion is outside this product review. This qualification accepts the exact product head; it does not infer or authorize protected receiving/merge.

## RETAINED LIMITS

- Non-gating interval `PUBLICATION_RECEIPT` final-readback placeholders remain documented; no fix spawned.
- Old standalone interval/later public surfaces remain historical REVISE; only their exact repaired trees imported into final fanin are accepted here.
- Raw component engineering methods remain non-public/opt-in; final fanin public allowlist is clean.
- No native C8/C9/C12, CAN008/CAN011, ADP, Pyat, B-owned context, human usability, external delivery, security/tamperproof, general concurrency or PRE-MAIN/protected-write acceptance.
- No product/guide/global-config/protected branch edits; all work under `.local-logs` and this review return.

## EVIDENCE

- `READBACK.json` — exact head/bases/verdict/hashes.
- `PROGRAMMA_DELTA.json` / `.md` — compact owner-intake delta.
- `evidence/FINAL_HEAD_PROBE.json` — exact 4b2 CLI/callable probe.
- `evidence/IMPORT_TREE_COMPAT.json` — 73-file delta, unchanged fanin code/tests, exact component trees.
- `evidence/FANIN_SOURCE_AUDIT.json` — 12/12 fanin source files.
- `evidence/RECEIVING_DELTA_INSPECTION.json` — published simultaneous receiving record inspection.
- `evidence/COMMANDS_AND_RESULTS.json` — executed and NOT_RUN record.
- `evidence/RETAINED_LIMITS.json` — preserved old findings and holds.
- `evidence/SOURCE_HEAD.json` — exact cut/component/base heads.
