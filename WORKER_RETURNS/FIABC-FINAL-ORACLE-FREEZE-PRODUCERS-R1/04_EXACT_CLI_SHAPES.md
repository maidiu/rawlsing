# Exact Final-Launch CLI Shapes

The final launch pack can invoke the committed module directly. These commands contain no inline Python glue.

Assume:

```bash
REPO=/path/to/rawlsing
WORK_ROOT=/path/to/fiabc-work
LITS_PATH=/path/to/LITS-2006-data.dta
```

Run from `$REPO`.

## 1. B03 — source-free standard WVS oracle

```bash
python -m rawlsing_next.fiabc_final_oracle_freeze_producers standardize-wvs \
  --r1m WORKER_RETURNS/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/07_FRESH_WVS_ORACLE.json \
  --output "$WORK_ROOT/court/oracles/WVS7.standard.json" \
  --freeze-sequence 30
```

This command reads no raw WVS source.

## 2. B05 — local candidate-neutral LiTS oracle

```bash
python -m rawlsing_next.fiabc_final_oracle_freeze_producers produce-lits \
  --repo-root "$REPO" \
  --source "$LITS_PATH" \
  --work-root "$WORK_ROOT" \
  --output "$WORK_ROOT/court/oracles/LITS_I.standard.json" \
  --freeze-sequence 30
```

This is the only producer in this lane allowed to read a survey source, and it is to be run later by the user locally before any candidate cell starts.

## 3. B06 — final two-source T3 freeze

```bash
python -m rawlsing_next.fiabc_final_oracle_freeze_producers freeze-t3 \
  --lits-oracle "$WORK_ROOT/court/oracles/LITS_I.standard.json" \
  --wvs-oracle "$WORK_ROOT/court/oracles/WVS7.standard.json" \
  --work-root "$WORK_ROOT" \
  --output "$WORK_ROOT/court/t3/frozen-upstream.json"
```

Then bind the existing launch consumers to:

```bash
export RAWLSING_EE_P2X_FROZEN_UPSTREAM_RECEIPT="$WORK_ROOT/court/t3/frozen-upstream.json"
```

The standard WVS command must be run only after the final integrated live standard-oracle constants carry the accepted successor WVS constitution. If they remain predecessor constants, the producer intentionally fails closed.
