# EE-R3A — Response Selector Reseal governed return

Status: `PASS__CANONICAL_18012_RESPONSE_SELECTOR_RESEALED__HQ_ADOPTION_REQUIRED`

Exact grain: `DETERMINISTICALLY_RESEAL_ONE_CANONICAL_18012_ID_SELECTOR_FROM_ACCEPTED_N04_R3_STATUS_VECTOR_AND_CANONICAL_LEDGER_ONLY`

Branch: `agent/rabochii-prev3-ee-r3a-response-selector-reseal-r1`  
Commission tip: `61fcf0135f71c3c37424af5a6756142ced891333`  
Library: `NO`

## Holding

The accepted N04-R3 18,276-row status vector and accepted N03-R2/N01-R2 canonical ledger order were reproduced without semantic inference. Applying exactly `status_code == 3` selects 18,012 canonical ledger positions.

The N04-R4A selector carrier/hash fields are inconsistent with that literal derivation. EE-R3A supersedes only those mechanical selector-carrier/hash fields. It does **not** supersede or re-adjudicate N04-R4A's accepted semantic conclusion that the selected 18,012 rows had no accepted exact response-category-semantics identity join at that prior grain.

## Current HQ authority observed

`HQ_HANDOFF/LATEST.json` resolved to checkpoint `20260916T1214-0400`, handoff commit `d24f377f2fb4bcf7d7e2a29941a925b983e42f42`, semantic PRE-MAIN tip `1dcd2a79dd6d4208738f655ab7fe4e71c219e354`.

HQ records EE-R3A as the local repair for EE-R2C and wakes response-semantic batch partitioning only after adoption of this PASS.

## Frozen predecessor identities

- canonical ledger authority: `3eaf9918e66b9d4bbc3a1c12598baca20c9d594d`
- ledger rows / unique IDs: `18,276 / 18,276`
- ledger canonical JSONL SHA-256: `0ac4cd90c19c859438ec12ddfa69c37e9b9c85607884e0f4ea93bc6b52493723`
- row order: accepted N01-R2 deterministic carrier/replay order; **no sorting**
- N04-R3 status-vector authority: `8e0266703bbf3b060abcd6fbe53c7ef6c49062c5`
- status-vector raw SHA-256: `f3bb9f06508f7eb26d1ee01e6bc865377637da34f5a60b4118006cc5d8a8d283`
- status-vector encoded stripped SHA-256: `8241edb2bf043105e0eae12dfa8dd312ff14ca09d37141467834529404c161d7`
- counts: `1=41, 2=22, 3=18,012, 4=159, 5=42`

## Exact resealed selector

Selection law: `SELECT_CANONICAL_LEDGER_POSITION_I_IFF_N04_R3_STATUS_CODE_I_EQUALS_3`

Selected count: `18,012`

### Exact ID selector carrier

`02_SELECTED_18012_ID_SELECTOR_CONTRACT.json` is lossless and repo-safe. It binds the immutable canonical ledger identity to the exact selected one-based ordinal carrier. Replaying those ordinals against that ledger reconstructs the complete 18,012-ID stream in canonical order.

- reconstructed full-ID LF stream bytes: `756504`
- reconstructed full-ID LF stream SHA-256: `582dc702d1c974b5e57931c2462468523cf73ddf997c00f05dc5e5c0e95ba7b0`

### Mask

- raw bytes: `18,276`
- raw SHA-256: `58f5fc12b968fad266e75e17be9f21d727d684535d0a78bb5e5ff5196d1c112e`
- zlib9/Base64 bytes: `504`
- zlib9/Base64 SHA-256: `6636108094f8a67d902ccfe5390cf8b3670da09d19f5c84877cbe8cb4730b012`
- carrier: `03_SELECTED_18012_MASK.zlib.b64`

### One-based ordinal stream

`04_SELECTED_18012_ORDINALS_COMPLEMENT.json` is a lossless complement carrier over the fixed universe `1..18,276`; only 264 ordinals are excluded. Its reconstruction yields the canonical selected ordinal stream:

- raw bytes: `97135`
- raw SHA-256: `769fc7c501f60797dd91aae184517edd76b50740db66f9340b6d42884ff3e021`
- selected ordinals: `18,012`
- excluded ordinals: `264`

## N04-R4A mechanical supersession

Superseded:
- mask raw SHA-256 `58f5fc1288588874235288e046c1797968263303135af8ceb58cc37da48c112e` → `58f5fc12b968fad266e75e17be9f21d727d684535d0a78bb5e5ff5196d1c112e`
- mask encoded SHA-256 `2b22305dda73bcf27d5d5de3c2adbd674e544ab09d7fbb35aa7a7138dc7674db` → `6636108094f8a67d902ccfe5390cf8b3670da09d19f5c84877cbe8cb4730b012`
- ordinal stream bytes `98,754` → `97135`
- ordinal SHA-256 `c6092adb1a55233b8b372222639dcac0c7de8bb4ceff06a07d9e7d1ffe40db6c` → `769fc7c501f60797dd91aae184517edd76b50740db66f9340b6d42884ff3e021`

Preserved:
- exact-bound count `0`
- typed residual count `18,012`
- residual `NO_ACCEPTED_EXACT_RESPONSE_CATEGORY_SEMANTICS_IDENTITY_JOIN`
- newly production-bindable count at that prior grain `0`

## Replay / second-run proof

`05_REPLAY_EE_R3A.py` independently replays the accepted N03-R2 ledger, rechecks the N04-R3 status vector, applies only `status_code == 3`, and proves equality to the compact ID-selector contract, ordinal carrier, and committed mask. Two fresh derivations were identical before sealing. Compact replay identity: `f820cf4f698709c92303bb39ea01d7cbb88ddf55fe6a84060da36c1d54a346f6`.

## Boundaries preserved

Response-semantics inference/repair: `NONE`. Membership widening: `NONE`. Routing/T03/Field Forge/V3/MAIN/semantic PRE-MAIN mutation: `NONE`.

## Exact successor wake

After HQ adopts this exact PASS, wake `EE_R2C_RESPONSE_BATCH_PARTITION_RERUN` on this resealed selector. This return does not itself perform response-semantic batching or semantic repair.

Terminal: `EE_R3A_PASS__CANONICAL_18012_RESPONSE_SELECTOR_RESEALED__R2C_SUCCESSOR_PARTITIONING_READY_AFTER_HQ_ADOPTION`
