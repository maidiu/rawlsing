# Selector-Population Parity Holding

Worker C's audit established that q310/q311 conditioning-population truth is part of the accepted ASTRA substrate, not an optional consequence of P2/P3 outputs.

## Historical authority

Expected selector material is loaded from the immutable ASTRA-D04-R2 source/replay receipt, not asserted into current truth.

## Current derivation

The accepted R5B successor path already executes `f02_source_scan(incidence, f02)` against the retained decoded incidence before reduction. The integration captures that existing scan result and threads it into current normalization. No second source decode was added.

The current scan and historical ASTRA receipt use the exact same F02 canonical row material:
- zero-based row ordinal;
- response state;
- raw native value;
- canonical JSON plus newline hashing.

Therefore exact row-root and selector-root equality is a lawful same-domain comparand.

## Conserved q310 truth

Counts:
- 1: 12340
- 2: 7511
- 3: 9085
- MISSING: 66

Row root:
`a979c15c93502b77979041ffd8451c602f63a7fcbb145106d68a78414be92455`

Selector roots:
- 1: `0a62f6f0e3d78b429022b95c2594a3fcbf053b8af588f0ceb304ac3dafe700d2`
- 2: `0bad1e397f5b74b6136ba82e8d81fc608d1df7124e6ff043048cc5cd91ef9c83`
- 3: `b477bf705a93bb672d9ae670a1daa38013c2aa2841d0c506f722ab1bbdbb2f3d`
- MISSING: `810a81a5663c05dcd0e2f4c2c972f66dc16e7446c87054bb412242632dc57348`

## Conserved q311 truth

Counts:
- 1: 16582
- 2: 4548
- 3: 7826
- MISSING: 46

Row root:
`af193e948fd2199bb784f476475d6dd4c6b96698a01e1804e5a6ce69b93c49aa`

Selector roots:
- 1: `bffb9d2e9da447a27aaf7c8f889a07d5c47389a58ad933d3ea9867f83e127869`
- 2: `43ffb4ef1de60354b9c943135fd0f31ee54d31edbcd3bb6abf147e5bff1dce1f`
- 3: `642a70ba00a4f7292d96267647068c3bfc83f5efc75451ce00a7df4cd2d62837`
- MISSING: `847c4e89a7336a5cb5ac6d73953b87091640231ba7cd5c5376e37044a12a03fb`

## Hostile court

The parity test suite proves fail-closed behavior for:
1. q310 selector-count drift while preserving total rows;
2. q311 selector-count drift;
3. q310 same-domain selector-root drift;
4. q311 same-domain selector-root drift;
5. q310 category permutation preserving total rows;
6. q311 category permutation preserving total rows;
7. MISSING-count drift preserving total rows;
8. unchanged 50/77/49/1 and unchanged P0–P4 material with altered selector substrate.

A selector-substrate mismatch is also proved to stop execution before oracle build.

Selector-population parity: **PASS**.
