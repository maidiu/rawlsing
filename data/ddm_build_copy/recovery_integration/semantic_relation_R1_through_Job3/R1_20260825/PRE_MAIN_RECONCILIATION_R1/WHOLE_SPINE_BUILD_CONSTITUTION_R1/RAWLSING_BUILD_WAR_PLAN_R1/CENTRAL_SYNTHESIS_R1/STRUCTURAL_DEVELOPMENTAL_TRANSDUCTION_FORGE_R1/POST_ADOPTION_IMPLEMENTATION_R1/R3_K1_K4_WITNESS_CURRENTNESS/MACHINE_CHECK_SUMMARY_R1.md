# MACHINE CHECK SUMMARY R1

Candidate content was executed before repository commit from an isolated local workspace using the exact bytes whose Git blob identities are recorded below.

## Compile/static check

Command:

```text
python -m py_compile rawlsing_next/sdtf_r4_witness_currentness.py
```

Result: `PASS`.

Implementation tested Git blob:
`06c8a2259436e7209bad4e4b3f8c314b18446fe6`

## Focused court

Command:

```text
PYTHONPATH=<candidate-root> python -m pytest -q rawlsing_next/tests/test_sdtf_r4_witness_currentness.py
```

Result:

```text
...............                                                          [100%]
15 passed in 0.07s
```

Focused test tested Git blob:
`e3ccedf6ffd694aa01728b8282582e5229b6bc4f`

## Direct proof properties exercised

- current witness accepted only with exact current authority refs;
- replaced authority/dependency -> stale/replay-required proof surface;
- revoked witness -> fail closed;
- unknown decisive authority state -> `UNKNOWN_NOT_PROVEN`;
- stale Path-A proof cannot be consumed;
- Path-B continues across unrelated replay churn but not owner/source revision;
- Path-B overlap + complete closure coverage + no defeating fact are all mandatory;
- failed/stale/revoked positive proof never proves the negative;
- bare `ACTIVE` does not force K4 classification.

Repository-side verification after commit must match the two recorded Git blob identities; otherwise this machine result does not attach to the committed candidate.
