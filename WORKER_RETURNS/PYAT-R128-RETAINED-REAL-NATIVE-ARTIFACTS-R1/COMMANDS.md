# R128 — exact execution commands

All commands were run from
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01` with `PYTHONPATH=.`.
No raw survey source is referenced.

## 1. Verify the exact retained checkpoint

```sh
CHECKPOINT=/Users/matthewsmith/Desktop/Rawlsing/LOCAL_CUSTODY/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/payload/PREMAIN-FIABC-LITS-FINAL-CANONICAL-CLOSURE-SOURCE-RETRY-R1/court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json
stat -f '%z' "$CHECKPOINT"
shasum -a 256 "$CHECKPOINT"
```

Expected: `3404445161` bytes and
`2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`.

## 2. Bounded streaming extraction/rehydration

```sh
PYTHONPATH=. python3 \
  WORKER_RETURNS/PYAT-R128-RETAINED-REAL-NATIVE-ARTIFACTS-R1/runtime/stream_retained_native.py \
  --checkpoint "$CHECKPOINT" \
  --private .r61/r128-retained-native/private \
  --out WORKER_RETURNS/PYAT-R128-RETAINED-REAL-NATIVE-ARTIFACTS-R1
```

Resume after an interrupted extraction (skips already indexed object refs):

```sh
PYTHONPATH=. python3 \
  WORKER_RETURNS/PYAT-R128-RETAINED-REAL-NATIVE-ARTIFACTS-R1/runtime/stream_retained_native.py \
  --checkpoint "$CHECKPOINT" \
  --private .r61/r128-retained-native/private \
  --out WORKER_RETURNS/PYAT-R128-RETAINED-REAL-NATIVE-ARTIFACTS-R1 \
  --resume
```

This command:
- verifies the whole checkpoint hash and the canonical closure body hash;
- streams `material.canonical_empirical_object_closure.preimage_fragments.item`
  and `...public_object_preimages.item` with ijson;
- hydrates only one public object at a time and calls the existing
  `materialize_public_object` constructor;
- verifies exact content identity and round-trip;
- writes private compressed objects under
  `.r61/r128-retained-native/private/objects/`;
- writes only nonperson refs/counts to `OBJECT_GRAPH.json` and
  `NATIVE_VALIDATION.json`.

Maximum extraction RSS observed: `1040838656` bytes. No full checkpoint
`read_bytes` or full JSON load is performed.

## 3. Existing M1 consuming-edge attempt

```sh
PYTHONPATH=. python3 \
  WORKER_RETURNS/PYAT-R128-RETAINED-REAL-NATIVE-ARTIFACTS-R1/runtime/attempt_consumer.py \
  --private .r61/r128-retained-native/private \
  --out WORKER_RETURNS/PYAT-R128-RETAINED-REAL-NATIVE-ARTIFACTS-R1
```

The reached owner call is
`build_m1_adjudication_input_bundle(...)`. It refuses with
`M1IntegrityError: conflicting exact authority snapshot preimages` before an
M1 bundle or family-rule dispatch exists. The command also performs the real
object identity/reference severance and restoration probes.

## 4. Owner pins

- Schema/closure reference: final-success commit
  `045d62709bb65084f3ae7b3dda062dfedfa942b4`;
  `rawlsing_next/fiabc_final_oracle_freeze_producers.py` blob
  `37eeccb91477c5f4f76a91bf491624d4398ad384` (not invoked through its unsafe
  full-file loader).
- Existing constructor: `rawlsing_next/pre553_carrier_execution.py` blob
  `e7cda773e6a2426bfa12b22790fd8e005fe75153` (identical at the final-success
  commit and the working HEAD).
- Object identity law: `rawlsing_next/pre553_empirical_objects.py` blob
  `a61365b994e5c3c50de0f598fcf40e90abf757b6` (identical at both pins).
- M1 owner: `rawlsing_next/pre553_learned_empirical_adjudication.py` at the
  working HEAD; the refusal is emitted by the existing owner, not a wrapper.

## 5. Private custody

`.r61/r128-retained-native/private/`:

- `objects/<schema>/<content_hash>.json.gz` — 234 exact canonical object
  preimages;
- `preimage_fragments.json.gz` — 58 canonical fragments;
- `c11_release.json.gz` — exact 100,644,200-byte release retention document;
- `astra_shaped_empirical_summary.json` — historical summary, separate from
  native objects;
- `object_index.jsonl` — nonperson refs/counts/edges metadata;
- `material_tail.json`, `closure_metadata.json` — small closure/material
  metadata.

No heavyweight object or fragment is committed to Git.
