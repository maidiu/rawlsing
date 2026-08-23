# G-SR08 LiTS I source-backed proving court

Status: `COMPLETE__FAIL_CLOSED_AT_PHASE_A_DECODER_PREFLIGHT`

Primary disposition: `LITS1_GSR08_BLOCK__SOURCE_OR_DECODER_NONIDENTITY`

## Holding

The exact LiTS I source is present and byte-identical: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`. The Library ZIP is also exact: `b2e90ee7ceefc230572e89687de28186544308949f8fd33c32b1d0ffb14b8feb`. A non-governing pandas metadata diagnostic independently reports the expected **29,002 × 1,198**, Stata format 113 surface.

The court cannot lawfully cross the decoder gate. The frozen implementation `decode_dta(source_path, encoding="latin1")` imports `pyreadstat`; this execution container has no `pyreadstat`, and `import pyreadstat` fails with:

```text
ModuleNotFoundError: No module named 'pyreadstat'
```

R07's accepted future execution order explicitly says to stop if the governed decoder/config cannot be reproduced. Pandas is therefore not substituted. No hostile fixture, source-specific projection, C11 candidate/release, replay manifest, or frozen-I03 query was executed.

## Preflight facts

- worker branch was exactly `b41b2cc6b3907795813c19292da47c07874317d7` with zero pre-existing delta at launch;
- Authority 38 is newer than Authority 37 but does **not** supersede G-SR08; it hardens semantic non-automation and typed-UNKNOWN preservation;
- accepted C05-R2A facade blob `fe4147853f9a42bd36dc2b5017ed05d7bc9ebf1b` is unchanged;
- accepted C05-R2A test blob `aaa38306558bc9ad0a87c959d777d3f3d87c8395` is unchanged;
- exact source/ZIP identities pass;
- no legacy empirical truth, R5 semantic ownership, C05-R2B, I05 discovery, or WVS7 execution was used.

## Bounded UNKNOWNs retained

The R07 nonblocking unknowns remain exactly bounded: intended source-text encoding, cross-release equivalence, default weight/estimand choice, and durable native-ID semantics beyond source-SHA + zero-based row ordinal replay identity. They were not re-adjudicated because the court stopped before Phase B.

## Runtime witness

Observed preflight peak RSS: **114,312 KiB**. Scratch peak before cleanup: **147,217,559 bytes**; final execution scratch: **0 bytes**. Elapsed to receipt generation: **481 s**. This is **not** a resource-scalability failure; the blocker is missing decoder dependency identity/executability.

## Return token

`PRE553_TRII_LITS1_GSR08_PROVING_RETURNED`
