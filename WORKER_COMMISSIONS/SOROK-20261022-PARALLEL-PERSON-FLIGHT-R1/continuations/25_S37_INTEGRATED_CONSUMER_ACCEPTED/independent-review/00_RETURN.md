# S37 cold C9 tamper closure — ACCEPT_SCOPED

Decision: **ACCEPT_SCOPED**.

## Exact cut

- Corrected candidate: `e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9`.
- Branch: `codex/sorok-s37-integrated-source-response-language`.
- Prior rejected cut: `e2063e3e2305b307d47a99fa9834d898f1ae9094`.
- Base: accepted S36 `8da78d8031a06a4bd7e1297fd713e573299c0860`.
- M35 `4170fbf…`, language `8d2920d…`, JOIN-E `7bf2da3…` unchanged.

Reviewed in a disposable clone; no product edits, provider/model calls,
controller-attachment changes, or native/science action.

## Reproduced checks

```text
PYTHONPATH=<S37 return> M35_JOIN_E_RETURN=<warm JOIN-E> \
  python3 -B -m pytest -q <S37 return>/tests -p no:cacheprovider
32 passed in 3.14s
```

Preserved reviewer oracle `SOROK_REVIEW/S37/oracles/s37_c9_tamper.py` was run
against checkout `e1f3c1d` and now returns **PASS**: the re-sealed C9 response
status tamper is refused at cold open with `S37_VERIFY_FAILED`; the oracle's
static `cut` label remains the prior candidate, but the actual checkout used was
`e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9`.

The repair now:

- requires a serialized body hash, when present, to equal the exact row key
  (`C9_RESPONSE_ROW_KEY_MISMATCH` / `C9_RECEIPT_ROW_KEY_MISMATCH`);
- keeps legitimate hash-omitted C9 serialization readable by supplying the row
  key and validating the seal;
- validates response status/route/reason against the sealed S35 outcome;
- applies the same common loader binding to receipt rows.

The 32 focused tests retain share/refusal positives, exact same E1/actor map,
M35 preimage rejection, C9 `NO_CHANGE`/`NO_PROPOSAL`, targetless C12, actual
reader/valid-empty, language, and lawful cold reopen. No broad review campaign
was reopened and M35/language/S36 accepted boundaries were not re-reviewed.

## Receipt

- 32-test output: `evidence/s37-e1f3-tests32.out` SHA-256 `58530699…`.
- Oracle output: `evidence/s37-e1f3-tamper.json` SHA-256 `9858f2c5…`;
  PASS, cold open refused.
- Corrected `s37/reader.py` SHA-256 `1da9ea45…`; tamper test SHA-256
  `d92ce038…`.
- Preserved oracle SHA-256 `930e6ba3…`.
- No live provider/domain/native/production action was performed.
