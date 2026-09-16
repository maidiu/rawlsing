# EE-R2C — GOVERNED RETURN

Worker: `EE-R2C`

Branch: `agent/rabochii-prev3-ee-r2c-response-semantic-batch-registry-r1`

Commission tip: `e6e7c8cf5d24a76814d04f63fe9ae6c1d4e6a993`

Grain: `PARTITION_EXACT_18012_CLASS_C_RESPONSE_SEMANTIC_RESIDUALS_INTO_FINITE_SOURCE_DOCUMENTARY_AUTHORITY_UNITS_AND_FREEZE_DISPATCH_REGISTRY_ONLY`

Terminal: `BLOCKED__PREDECESSOR_18012_SELECTOR_CARRIER_REPLAY_AND_RECEIPT_ARE_INTERNALLY_INCONSISTENT`

## Smallest exact blocker

EE-R2C cannot lawfully freeze the required exact 18,012-row accounting because the accepted N04-R4A exact-selector materials disagree at the byte/hash level.

At N04-R4A commit `238800fe20f257194530916514289492601eeff1`:

- `02_SELECTED_18012_MASK.zlib.b64` has blob `b3f857019ceaa8c1da081f3b5bfab07cbb3f8ef2`, 102 file bytes, 101 stripped bytes, and stripped SHA-256 `a1488b811a77c5a64f030c56bfa5a7e4a5d3ac6939f82b5690eb5630a2f22302`.
- That does **not** equal the R4A replay/receipt expected stripped SHA-256 `2b22305dda73bcf27d5d5de3c2adbd674e544ab09d37141467834529404c161d7`.
- The committed 101-byte stripped payload is not valid canonical Base64 (`Excess padding` under strict decode); permissive Base64 decoding produces bytes that fail zlib decompression.

The R4A replay itself gives an independent deterministic selector rule: select N04-R3 status code `3`. The accepted predecessor vector at commit `8e0266703bbf3b060abcd6fbe53c7ef6c49062c5` is valid and matches every R4A hard-coded predecessor check:
- stripped vector Base64 SHA-256 `8241edb2bf043105e0eae12dfa8dd312ff14ca09d37141467834529404c161d7`;
- raw vector SHA-256 `f3bb9f06508f7eb26d1ee01e6bc865377637da34f5a60b4118006cc5d8a8d283`;
- 18,276 bytes with counts `{1:41, 2:22, 3:18012, 4:159, 5:42}`.

But applying the R4A replay's own exact rule `bytes(1 if code == 3 else 0 for code in predecessor_vector)` yields:
- 18,276 mask bytes;
- 18,012 selected rows;
- raw mask SHA-256 `58f5fc12b968fad266e75e17be9f21d727d684535d0a78bb5e5ff5196d1c112e`;
- selected one-based ordinal stream = 97,135 bytes, SHA-256 `769fc7c501f60797dd91aae184517edd76b50740db66f9340b6d42884ff3e021`.

Those values also disagree with the R4A replay/receipt hard-coded expected mask SHA `58f5fc1288588874235288e046c1797968263303135af8ceb58cc37da48c112e`, expected ordinal bytes `98,754`, and expected ordinal SHA `c6092adb1a55233b8b372222639dcac0c7de8bb4ceff06a07d9e7d1ffe40db6c`.

EE-W3 head `cf609f6447d0bb8d07de14c5116e6b6dfdf4f943` repeats the 18,012 count and the R4A expected ordinal hash, but does not publish an independent exact 18,012-ID carrier that resolves this mismatch.

## Authority consequence

The **count** 18,012 is reproducible from the accepted N04-R3 vector, but the exact commissioned **identity set** is not unambiguously frozen by the accepted N04-R4A / EE-W3 materials. Choosing the replay-derived selector and replacing the inconsistent R4A carrier/receipt would be predecessor repair, outside EE-R2C's organizational-only authority.

Therefore EE-R2C does not freeze a batch registry, full row accounting, dispatch graph, semantic binding, or objectization. The smallest successor action is a competent predecessor repair/reseal that identifies one exact 18,012-ID selector carrier and reconciles the R4A replay/receipt hashes.

`01_BLOCKER_RECEIPT.json` records the exact evidence. `02_VERIFY_BLOCKER.py` mechanically checks the inconsistency from the two accepted predecessor commits.

Library access was not used. MAIN and semantic PRE-MAIN are unchanged.
