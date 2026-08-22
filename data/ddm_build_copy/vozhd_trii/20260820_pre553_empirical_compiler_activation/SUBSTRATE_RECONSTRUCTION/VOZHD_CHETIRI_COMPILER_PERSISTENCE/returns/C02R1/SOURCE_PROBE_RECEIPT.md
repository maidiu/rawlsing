# VC4 C02-R1 — SOURCE PROBE RECEIPT

Status: `BLOCKED_BEFORE_RAW_READ__EXACT_SOURCE_UNAVAILABLE`
Exact start HEAD: `29ab03d57074086e55870e1feee1b94820aee3ba`
Worker branch: `agent/vozhd-chetiri-c02r1-occurrence-topology-proof`

## Required source scope

The launch-time governed census is the exact 35-row `SOURCE_BYTE_INVENTORY.csv`: 35 mandatory source snapshots, 31 SAV and 4 DTA. C02-R1 requires complete scope. One mandatory source unavailable at execution defeats a complete-scope FD certificate.

## Exact blocking source

Source: `WVS Wave 7.sav`

Checked-in expected identity:
- format: `sav`
- bytes: `185163494`
- SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Authority 61 additionally freezes:
- expected shape: `97,220 x 613`
- decoder: `decode_sav(source_path)`
- encoding override: `NONE`
- authorized Library transport: `WVS Wave 7.sav.zip`

These are expected/governed identities. C02-R1 did not claim an execution-time hash match because the source bytes were unavailable.

## Availability checks before any raw read

1. **Mounted execution filesystem** — the governed local `/Users/matthewsmith/Desktop/Rawlsing/data/Data` corpus was not mounted; WVS7 was not available through the mounted runtime source surface.
2. **ChatGPT file library, raw-source search** — recursive SAV/DTA inspection exposed only a subset/candidates; `WVS Wave 7.sav` was not available. Candidate files were not opened and were not promoted to exact sources by filename/size resemblance.
3. **ChatGPT file library, authorized ZIP transport** — exact-title search for `WVS Wave 7.sav.zip` returned no match; recursive ZIP listing was paginated to exhaustion through the `W...` filename region with no such transport.
4. **Connected Google Drive** — searches for `WVS Wave 7`, `WVS`, `Wave 7`, and exact `WVS Wave 7.sav.zip` did not surface the required source/transport.

## Probe actions actually executed

- raw-source reads: `0`
- raw-source SHA calculations: `0`
- metadata decodes: `0`
- targeted cell/value reads: `0`
- occurrence/topology scans: `0`
- source mutations: `0`

This does not violate the “verify SHA before every source read” law: there was no source read.

## Why partial probing stopped

The court is complete-scope, not sample-scope. Once one mandatory CLOSED_35 source was unavailable, opportunistic probing of other accessible candidates could not establish the required complete-scope certificate. Continuing could create partial evidence that cannot change the exact disposition and could invite unlawful extrapolation across the missing source.

Therefore all non-WVS7 inventory members are recorded as `NOT_PROBED_AFTER_TERMINAL_COMPLETE_SCOPE_STOP`. This is **not** a finding that those sources are unavailable.

## Court consequence

`C02R1_BLOCK__EXACT_SOURCE_UNAVAILABLE`

No source-specific FD/non-FD conclusion was issued. This receipt proves none of:
- `SOURCE_CELL == SEMANTIC_OCCURRENCE`
- `UNKNOWN_EXCEPTION_DOMAIN == SPARSE_EXCEPTION_DOMAIN`
- `UNPROVED_DERIVABILITY == FULL_EVENT_TABLE_REQUIRED`
- `FULL_EVENT_TABLE_EXISTENCE == SEMANTIC_NECESSITY`

The exact M04/M05 proof question remains open until the complete governed source scope is executable and hash-verifiable.
