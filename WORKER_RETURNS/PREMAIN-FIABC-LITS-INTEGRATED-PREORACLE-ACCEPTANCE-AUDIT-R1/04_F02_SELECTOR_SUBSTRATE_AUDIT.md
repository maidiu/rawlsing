# Court 6 — q310 / q311 Selector Substrate

## Result

**PASS**

This court was audited at the actual hashing-material level.

## Current path

The current LiTS neutral path uses the same already-decoded `incidence`.

It replays immutable accepted R5B/F02 source-scan code and obtains `selector_scan` before current I05 parity normalization.

Accepted R5B owner:

`648a39ad5bed42f66e066410af5869604d29c12d`

Frozen F02 scanner blob:

`7b45b277164fa90c3da739aab26b516f7a8cb8dc`

The scanner selects q310/q311 from the retained incidence, enumerates source-order rows and hashes for every row:

```
{
  "row_ordinal": <zero-based source-order ordinal>,
  "response_state": "SUBSTANTIVE_RESPONSE" | "MISSING",
  "raw_native_value": 1 | 2 | 3 | null
}
```

as canonical JSON plus newline.

It computes:

- one all-row SHA256 per question;
- one SHA256 per exact category 1/2/3/MISSING;
- exact counts.

## Historical domain

Accepted historical D04 lineage identifies exact G02 execution producer blob:

`7a9b8b53e36041b453eb62e7a22a52ff0d392c16`

Its `scan_f02_selectors(records)` independently uses the **same actual canonical row material**:

```
{"row_ordinal": i, "response_state": state, "raw_native_value": value}
```

with zero-based source-order enumeration and the same typed native rule:

- None/NaN → MISSING/null
- integral 1/2/3 → SUBSTANTIVE_RESPONSE/integer
- other material rejected.

Thus historical and current roots genuinely occupy one hash domain. The parity label:

`F02_SOURCE_ROW_ORDINAL_NATIVE_VALUE@1.0.0`

is supported by the implementations.

## Exact accepted q310

Counts:

- 1 = 12340
- 2 = 7511
- 3 = 9085
- MISSING = 66

All-row root:

`a979c15c93502b77979041ffd8451c602f63a7fcbb145106d68a78414be92455`

Selector roots:

- 1 — `0a62f6f0e3d78b429022b95c2594a3fcbf053b8af588f0ceb304ac3dafe700d2`
- 2 — `0bad1e397f5b74b6136ba82e8d81fc608d1df7124e6ff043048cc5cd91ef9c83`
- 3 — `b477bf705a93bb672d9ae670a1daa38013c2aa2841d0c506f722ab1bbdbb2f3d`
- MISSING — `810a81a5663c05dcd0e2f4c2c972f66dc16e7446c87054bb412242632dc57348`

## Exact accepted q311

Counts:

- 1 = 16582
- 2 = 4548
- 3 = 7826
- MISSING = 46

All-row root:

`af193e948fd2199bb784f476475d6dd4c6b96698a01e1804e5a6ce69b93c49aa`

Selector roots:

- 1 — `bffb9d2e9da447a27aaf7c8f889a07d5c47389a58ad933d3ea9867f83e127869`
- 2 — `43ffb4ef1de60354b9c943135fd0f31ee54d31edbcd3bb6abf147e5bff1dce1f`
- 3 — `642a70ba00a4f7292d96267647068c3bfc83f5efc75451ce00a7df4cd2d62837`
- MISSING — `847c4e89a7336a5cb5ac6d73953b87091640231ba7cd5c5376e37044a12a03fb`

## Current provenance

The current selector scan is produced from the current retained incidence.

Historical ASTRA constants are used only on the expected side.

No second source decode exists for selector parity.

## Hostile tests

The integrated court contains explicit failures for:

- q310 count drift;
- q311 count drift;
- q310 root drift;
- q311 root drift;
- q310 category permutation with total preserved;
- q311 category permutation with total preserved;
- MISSING/category shift with total preserved;
- selector drift while 50/77/49/1 and P0–P4 remain unchanged;
- selector failure preventing oracle construction.

This court is closed.
