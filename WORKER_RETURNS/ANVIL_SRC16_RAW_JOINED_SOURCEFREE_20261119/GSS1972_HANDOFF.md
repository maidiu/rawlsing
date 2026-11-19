# SRC16 joined sourcefree candidate — GSS1972 construction handoff

## Frozen inputs and patch order

Base runtime: the pinned `MEASUREMENT_PREP` sourcefree runtime tree.
Patch order is exact:

1. `patches/01_handoff_raw_lane.patch`
2. `patches/02_query_predicate_guard.patch`
3. `patches/03_i05_unresolved_repair.patch`
4. `patches/04_saved_batch_prior_cache.patch` (corrected OWNER `aaa8a548…`, SHA `71b12874…`)

Patch SHA-256 values and pre/post file hashes are frozen in
`JOINED_EVIDENCE.json`. `SETUP.sh` reproduces the isolated candidate.

## Sourcefree joined proof

```bash
"$RETURN/SETUP.sh" "$PRIVATE_ISOLATED_TREE"
cp "$RETURN/joined_trace.py" "$PRIVATE_ISOLATED_TREE/joined_trace.py"
cd "$PRIVATE_ISOLATED_TREE"
ANVIL_IMPLEMENTER="$PRIVATE_ISOLATED_TREE" \
ANVIL_TRACE_SCRATCH="$PRIVATE_TRACE_SCRATCH" \
PYTHONPATH="$PRIVATE_ISOLATED_TREE" \
python3 -B joined_trace.py
```

The trace creates one sourcefree saved estate, cold-opens it, and traverses
I03, I05 and saved Batch. It does not read original GSS data.

## GSS1972 construction (owner only; not run here)

Private values are owner-supplied and are not published:

```bash
ANVIL_CANDIDATE_TREE="$PRIVATE_ISOLATED_TREE" \
ANVIL_CANDIDATE_PATCH="$PRIVATE_CANDIDATE_PATCH" \
ANVIL_SRC16_GRANT_DIR="$PRIVATE_SRC16_GRANT_DIR" \
ANVIL_SRC16_CONFIG="$PRIVATE_SRC16_CONFIG" \
ANVIL_SRC16_SOURCE_PATH="$PRIVATE_EXACT_SRC16_SOURCE" \
PYTHONPATH="$PRIVATE_ISOLATED_TREE:$PRIVATE_R1_RETURN/common:$PRIVATE_R1_RETURN" \
python3 "$PRIVATE_R1_RETURN/generic_cli.py" --mode src16-run --root "$PRIVATE_WORK_ROOT"
```

This routes the existing common source adapter into the common supervisor:
producer, producer termination, fresh native reader, existing caps/progress/logs.
The fresh reopen is the reader child in that run; no second reader path or new
durable corpus is introduced.

## State

- Sourcefree joined composition: PASS.
- Original GSS1972 execution: **NOT RUN**.
- I05/Batch sourcefree traversal: actual existing owners, tiny fixture only.
- Mapped parity: exact, including cardinality/multiplicity/refs/payload and
  mutation failure.
- Typed unresolved: I03 `UNRESOLVED`; I05 `EVALUATED_UNRESOLVED` /
  `COVERAGE_LIMITED`; valid empty remains distinct.
- Authority denial: existing `DirectEstateError` in both I05 and prior-receipt
  Batch probes.
- No source, protected refs, frozen runtime edit, second backend, or DHIKR.
