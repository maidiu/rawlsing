# EE-R8C — exact real-source owner executor + final A/B/C bakeoff

Status: **BLOCKED**

Terminal: `EE_R8C_BLOCKED__FROZEN_REAL_SOURCE_OWNER_PREPARATION_CLOSURE_INCOMPLETE__NO_PARTIAL_ABC_BAKEOFF`

Branch: `agent/rabochii-prev3-ee-r8c-production-source-provider-final-bakeoff-r1`

Starting tip: `7254f422dbb0a2aa5b74ac67788d138aae331b97`

## Result

The exact R8B Darwin metric repair remains qualified.  Both exact source
carriers were rehashed locally.  However, the required source×candidate
preparation court cannot qualify all six cells from the frozen R7A/R6B/R6A/R3E
inputs and the immediate declared dependencies of the R4B owners.

The smallest frozen-order blocker is **WVS7 × A**.  The accepted Route-A
owner requires an `R5LongShardedReader`, which is an exact R5 compact-carrier
reader.  The only WVS7 authoritative input here is the exact SAV carrier; no
accepted WVS7 compact carrier, R5-reader binding, or callable preparation
binding is supplied.  Constructing one from the SAV would create the carrier
and projection work that this commission forbids.

The matrix in `01_SOURCE_CANDIDATE_PREPARATION_MATRIX.json` records the
remaining independently proved incompatibilities.  In particular, the
registry-declared LiTS-I Route-B production driver at
`f43c4be11d4f8fa98f538727337ec075d99d03bc` is a byte-exact bootstrap whose
two stored base64 chunks cannot satisfy its mandatory strict decoder.  The
carrier therefore cannot expose its declared effective source without a
loader repair, which is outside this provider-only commission.

No `owner_executor` was added, no source was decoded for a surrogate run, and
no candidate process, lifecycle/replay sequence, telemetry vector, parity
claim, comparison, ranking, or carrier-policy decision was emitted.  A
partial bakeoff is prohibited by the commission.

## Exact verified identities

- WVS7: `WVS Wave 7.sav`, 185,163,494 bytes,
  `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`.
- LiTS-I: `LITS-2006-data.dta`, 139,531,180 bytes,
  `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`.
- R8B-qualified W4 runtime file:
  `rawlsing_next/ee_w4_harness_runtime.py`, SHA-256
  `bf0e72c6a11f60219689458a74ae6b3844a4e620ab6fcd30674c8fbf150f9c39`.
  Its Darwin qualification maps native `ru_maxrss` bytes directly to
  `peak_rss_bytes`; a deterministic probe returned 314,159 for both fields.
- R4B owner pins remain A `d4915e7e6755ba1850756aebff72f982f73a332b`, B
  `7c509c2098d0030f253344eb3f682471378812a8`, and C
  `abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889`, at owner commit
  `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`.

## Bounded evidence

`02_VERIFICATION_RECEIPT.json` records the direct commands, source identities,
and exact observed failure.  `03_verify_ee_r8c.py` validates the return
schema, matrix order, source hashes, and the precise blocker boundary.
