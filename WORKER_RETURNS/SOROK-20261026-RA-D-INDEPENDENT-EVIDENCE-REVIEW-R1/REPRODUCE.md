# Reproduce this review

All commands are local and sourcefree. No provider call, raw data, production edit or native grant is involved. The source archive is disposable and is not committed.

## 1. Isolated worktree

```sh
git worktree add -b agent/reviewer-sorok-20261026-ra-d-independent-runtime-evidence-r1 \
  "$REVIEW_WORKTREE" 007d94a155cd42a89de35b141fec5ca2139f6365
```

## 2. Recreate the exact source archive

Set `RAD_REVIEW_ARCHIVE` to a disposable directory (for example under `$TMPDIR`).

```sh
mkdir -p "$RAD_REVIEW_ARCHIVE"
git archive c821b488b3a9a3f0fa01b1981989cc17af637dc1 \
  WORKER_RETURNS/SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1 \
  WORKER_RETURNS/SOROK-20261024-S37-INTEGRATED-CONSUMER-R1 \
  WORKER_RETURNS/SOROK-20261024-S39-GENERATED-RESPONSE-R1 \
  WORKER_RETURNS/SOROK-20261024-S40-GENERATED-NATIVE-SPEECH-R1 \
  WORKER_RETURNS/SOROK-20261024-S41-CONTINUING-PERSON-EVENTS-R1 \
  WORKER_RETURNS/SOROK-20261024-S42-ONGOING-EVENT-CONSUMER-R1 \
  WORKER_RETURNS/SOROK-20261024-S43-HISTORICAL-LANGUAGE-CONSUMER-R1 \
  WORKER_RETURNS/SOROK-20261024-S44-SAMPLED-ROOT-CONSUMER-R1 \
  WORKER_RETURNS/SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1 \
  WORKER_RETURNS/SOROK-20261025-S46-INTERVAL-PARTICIPATION-CONSUMER-R1 \
  WORKER_RETURNS/SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1 \
  WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1 \
  WORKER_RETURNS/SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1 \
  WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1 \
  WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1 \
  | tar -x -C "$RAD_REVIEW_ARCHIVE"

git archive 515b9a8ee45672c97051df4efef679117a679525 \
  WORKER_RETURNS/SOROK-20261025-S50-HISTORICAL-V3-ACTOR-RECOVERY-R1 \
  | tar -x -C "$RAD_REVIEW_ARCHIVE"

mkdir -p "$RAD_REVIEW_ARCHIVE/.git"   # path-discovery marker for vendored M35 bootstrap
```

## 3. Focused test suites

```sh
for suite in \
  SOROK-20261024-S39-GENERATED-RESPONSE-R1 \
  SOROK-20261024-S44-SAMPLED-ROOT-CONSUMER-R1 \
  SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1 \
  SOROK-20261025-S46-INTERVAL-PARTICIPATION-CONSUMER-R1 \
  SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1 \
  SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1 \
  SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1 \
  SOROK-20261025-S50-HISTORICAL-V3-ACTOR-RECOVERY-R1 \
  SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1 \
  SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1; do
  python3 -m pytest "$RAD_REVIEW_ARCHIVE/WORKER_RETURNS/$suite/tests" -q
done
```

Expected: 10, 10, 21, 17, 17, 12, 13, 5, 13, 13 = **131 passed**.

## 4. Reviewer probes

```sh
RAD_REVIEW_REPO="$REPO" RAD_REVIEW_ARCHIVE="$RAD_REVIEW_ARCHIVE" \
  python3 scripts/reviewer_source_identity.py

RAD_REVIEW_ARCHIVE="$RAD_REVIEW_ARCHIVE" \
  python3 scripts/reviewer_probe.py

RAD_REVIEW_ARCHIVE="$RAD_REVIEW_ARCHIVE" \
  python3 scripts/reviewer_v3_functions.py
```

Expected highlights:

- `reviewer_source_identity.json`: 183/183 S52 Python files exact; five ancestor divergences; S50 31/31 exact.
- `reviewer_probe_result.json`: material chain values and `s52_verifier_defect_reproduced=true`.
- `reviewer_v3_functions.json`: V3 functions present; one-year pressure-flow history and memory; roundtrip exact.

## 5. Entrypoints

```sh
(cd "$RAD_REVIEW_ARCHIVE/WORKER_RETURNS/SOROK-20261025-S50-HISTORICAL-V3-ACTOR-RECOVERY-R1" && python3 run_s50.py)
(cd "$RAD_REVIEW_ARCHIVE/WORKER_RETURNS/SOROK-20261024-S44-SAMPLED-ROOT-CONSUMER-R1" && python3 run_s44.py)
(cd "$RAD_REVIEW_ARCHIVE/WORKER_RETURNS/SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1" && python3 run_s45.py)
(cd "$RAD_REVIEW_ARCHIVE/WORKER_RETURNS/SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1" && python3 run_s47.py)
(cd "$RAD_REVIEW_ARCHIVE/WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1" && python3 run_s51.py)
(cd "$RAD_REVIEW_ARCHIVE/WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1" && python3 run_s52.py)
```

## 6. Required external roots

The S37/S51/S50 bootstraps contain hard-coded default roots. They must be present or overridden exactly as recorded in `SOURCE_INDEX.json`:

- G18 historical source at `64fec28c…`;
- JOIN-E source at `7bf2da30…`;
- language mediation at `8d2920da…`;
- historical V3 bundle at the archive identity `953c9149…` and the 31-file identity manifest.

Relevant environment overrides used by the S37 bootstrap include `S37_M35_RETURN`, `S37_JOIN_E_RETURN`, `S37_LANGUAGE_RETURN`, `S37_S36_RETURN` and `M35_BP2_VENDOR`. The S50 bootstrap also resolves the historical V3 root and identity manifest from its own source; see `SOURCE_INDEX.json` and `logs/reviewer_source_identity.json`.

## 7. Notes

- The archive and runtime state are disposable and are not committed.
- The reviewer probe writes only to system temporary directories.
- The S52 hostile RED is intentionally a failing invariant: `reviewer_probe_result.json` records both the bypass and the control that rejects the same tamper.
- No source file was edited.
