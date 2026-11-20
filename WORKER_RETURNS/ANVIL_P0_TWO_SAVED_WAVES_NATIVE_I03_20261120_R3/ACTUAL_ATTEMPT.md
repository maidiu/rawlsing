# Actual cold native-stream admission — per wave

## Executable

Controller-held private launcher, Python 3.11, run from the P0 worktree:

```bash
/usr/bin/time -l env PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 \
  python3 -B "$P0_PRIVATE_PROOF_DIR/r3_actual_stream_attempt.py"
```

Private launcher SHA-256:
`7b8d9bc411b56b92e4664279818d3fcbaa8481f16af2138ea6c9d8e850522c6e`

The launcher read only the independently held custody and the existing scoped
R2 MainMac decision. It did not request a new permission and did not print
private paths, manifests, respondent values, or sensitive counts.

## Sequential results

### SRC04 — Arab Barometer Wave 1

- Cold bridge admission: `VERIFIED`
- Stream release kind: `C11_STREAM_SOURCEFREE_RELEASE`
- Native replay kind: `ANVILStreamReplayRoot@1`
- Governed issued query: `QUERY_NOT_ISSUED`
- Native I03: `NOT_ATTEMPTED_NO_LAWFUL_ISSUED_QUERY`
- I05/DISCOVERY: `NOT_ATTEMPTED_NO_COMPATIBLE_AUTHORITY_PATH`
- S04/DHIKR/FF01/C4/C5/C6: `NOT_REACHED`
- First fault: none

### SRC16 — GSS1972

- Cold bridge admission: `VERIFIED`
- Stream release kind: `C11_STREAM_SOURCEFREE_RELEASE`
- Native replay kind: `ANVILStreamReplayRoot@1`
- Governed issued query: `QUERY_NOT_ISSUED`
- Native I03: `NOT_ATTEMPTED_NO_LAWFUL_ISSUED_QUERY`
- I05/DISCOVERY: `NOT_ATTEMPTED_NO_COMPATIBLE_AUTHORITY_PATH`
- S04/DHIKR/FF01/C4/C5/C6: `NOT_REACHED`
- First fault: none

## Why no I03 execution

The cold physical bridge is now positively admitted for both actual estates.
The missing prerequisite is a lawful governed query, not a carrier or current
permission. There is no exact issued QUERY/predicate/authority artifact for
either wave, and the R2 decision is not a scientific compiler/issuer decision.
The current #1084 v2 path requires its original frozen compilation inputs,
which are not present. No query was manufactured and no evaluator was called.

Discovery is likewise not run: R2 grants local analysis but does not provide an
exact compatible discovery authority/path over this saved stream.

## Resource

- Wall time: 5.78 s
- Max RSS: 186,597,376 bytes
- Peak memory footprint: 199,090,176 bytes
- Swaps: 0
- Live current-guard checks: 3,068
- Respondent values emitted: 0
- Original `.sav` source opened: false
- Rebuild/projection/schema alias: none
