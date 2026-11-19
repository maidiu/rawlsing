# SRC17 SQLite-free construction preparation

Sourcefree/metadata-only operator entry for GSS 1973/SRC17. It reuses the independently accepted SQLite-free streaming writer/reader and checkpoint-capable single-pass module from the isolated SQLite-free integration.

## Preflight

- exact config `ca791189…` / canonical `3f1eb83a…`
- exact construction-only grant `d6272ba6…` and authentication `f7fb429b…`
- grant `CURRENT_GRANTED`, `NONE_RECORDED`
- request exact: true
- source read: false; SQLite normal proof: expected false

## Launch eligibility

**BLOCKED at exact field-mapping gates**, not at grant currentness:

- source-native key slot: ordinal 3, `id` — `SRC17-NATIVE-ROW-KEY` / `DECODE_REQUIRED`
- 51 continuous items — `SRC17-CONTINUOUS-NATIVE-FINITE-RULE` / `NATIVE_FINITE_RULE_REQUIRED`
- 5 administrative/context items — `SRC17-ADMIN-NO-RESPONSE-SLOT` / `RETAINED_ADMINISTRATIVE`

No row-native keys have been decoded and no continuous rules are guessed. The sourcefree fixture passes the SQLite-free writer/reader path; actual SRC17 construction remains ineligible until those exact inputs exist.

## Commands

```bash
python3 src17_operator.py --mode preflight
python3 src17_operator.py --mode sourcefree --root <fresh-private-root>
```

The sourcefree fixture uses 90 rows, repeated/zero/missing/NOT_ASKED/DK values, exact stream roots and fresh native reader. It creates no SQLite file. The actual SRC17 source path/argv is not issued here.
