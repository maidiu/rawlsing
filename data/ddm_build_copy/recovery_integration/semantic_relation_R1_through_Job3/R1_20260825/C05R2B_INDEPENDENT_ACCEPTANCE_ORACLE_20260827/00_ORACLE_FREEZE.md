# C05R2B Independent Acceptance Oracle — Frozen Lane 02

Status: `C05R2B_INDEPENDENT_ACCEPTANCE_ORACLE_FROZEN`

This package was derived on branch `c05r2b-independent-validation-oracle-20260827` from exact start
`40e27a552eadeab89d101b2ed0267fa939a283a0` **before any Lane 01 provisional or final implementation/result was read**.

It freezes acceptance law, identities, exact candidate membership, typed-state distinctions,
common I03/I04 targets, replay/fresh-process parity, source/decode accounting, and Route-B
session-boundary/persistence requirements.  It does **not** freeze or predict any production
I05 candidate result.

Primary machine oracle: `C05R2B_ACCEPTANCE_ORACLE.json`.

Validator:
`python validate_c05r2b_receipts.py --run1 RUN1.json --run2 RUN2.json`

Synthetic hostile self-test:
`python validate_c05r2b_receipts.py --self-test`

The self-test fabricates only synthetic validator fixtures.  Those fixtures are not empirical
evidence and confer no learned-world or structural authority.

## Frozen headline identities

- LiTS-I SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- AS2B C11 logical release hash: `e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26`
- AS2B ReplayManifest: `6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd`
- AS3R2 DiscoveryAuthority: `98d52062a0acc04a1949053a8f83397621e810950ff70ceff0260b68d17fd28c`
- AS3R2 official frontier: `84349595622ed6eec5bd6af60de5b74df26ae6752ae64e40d7595fd7560b7d67`
- Candidate count / required covered count: `82 / 82`
- AS3 common I03 oracle: `e5555061eed45aad81cb5d0b014db54899f72167e0cd1d70911528e02f6bd93c`
- AS3 common typed-nonpositive I04 oracle: `e69f49c705b79bf469e67ee12b705747693a260e67c9cc1b9262900a89b5c33e`
- Route-B spec: `51836c44c7400a0d11f514c2bca4c21dd201461667728ed3335bc9ffd2462810`

## Critical laws

Frontier construction is complete before empirical evaluation.  No result may affect reachability.
No score/top-k/unary/frequency/diagnostic pruning is lawful.  All 82 frozen identities must receive
an exact terminal coverage state and receipt.

Typed negatives/nonpositives remain typed.  Row absence is not a terminal state; integrity failure
cannot be laundered into coverage.  I04 must preserve
`MISSING_STRUCTURAL_ADMISSION_AUTHORITY / MISSING_AUTHORITY / positive product NONE`.

Route B may retain only the exact primary source, governed semantic authority, provenance/replay
receipts, and genuinely accepted learned/structural products.  Decoded frames, transformed execution
bundles, mask banks, and persistent transformed empirical carriers are forbidden after the frozen
session boundary.

Two fresh processes are required and semantic/replay identity must match exactly.
