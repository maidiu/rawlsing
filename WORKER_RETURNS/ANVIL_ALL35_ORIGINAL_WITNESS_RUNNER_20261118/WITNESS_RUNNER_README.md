# ALL35 witness runner — SRC04 preflight

This is a generic metadata-only preflight/caller plan for the shared construction-only candidate; SRC04 is the witness. Other waves use the same config/index/scoped-selection path, with witness accounting applicable only to SRC04. It does not launch a source build or open/stat/hash/decode the original SRC04 path.

Pins: candidate patch `2b139250…` / `9da2a368…`; grant binding `dbeada9a…` / `d1283b6…`; accepted SRC04 reference `ba412536…`; config index `ad3386b7…`; config file `5e107de4…`.

## Preflight result

`DRY_PREFLIGHT_OK__Q217_HELD__SCOPED_CONFIG_READY`

- The full repaired config contains q217 at ordinal 27 with exact residual `UNRESOLVED_EXACT_UNLABELED_CODES`.
- A full-config construction would include the previously held q217 field.
- The accepted 177-response + 3-coordinate selection from the accepted SRC04 receipt is applied as a scoped config; q217 is excluded, all 181 physical slots remain accounted, and the q217 38-cell hold is explicit.
- Exact grant binding remains `REQUEST_ONLY_ALLOWED`; resolver pre/post recheck returned the same decision.
- Accepted body accounting to compare after an authorized run: release `9ddec985…`, 2,619,317 public objects, 7,514 internal records, 1,298,649 events/response positions, 22,011 coordinates, q217 38 unbound / 0 release events.
- Disk floor from 512×600 measured partial bytes: `2 × 1,951,192,968 + 1 GiB = 4,976,127,760 bytes`; actual free at preflight was ~44.3 GB. RAM cap 6 GiB; no writer wall cutoff.
- Producer/reopen plan is separate processes; reopen must occur after the producer exits. No source launch was performed.

## Run

```bash
python3 witness_runner.py \
  --candidate-tree /path/to/exact-frozen-candidate-tree \
  --config /path/to/SRC04/source.config.repaired.v2.json \
  --outdir DRY_RUN
```

The exact grant resolver is imported from the prior additive adapter folder. SRC17 remains construction-only and outside this witness.
