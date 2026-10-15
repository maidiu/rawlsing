# Sorok HQ310 OC4 — source-free custody repair candidate

**Disposition: IMPLEMENTATION_RETURNED__TEN_OC3_REDS_CLOSED__REVIEW_REVISE__FOUR_NEW_CONTENT_ONLY_SIGNATURE_CONTRACT_REDS__NO_ADOPTION.**

Role: bounded implementation worker, NOT independent I2 acceptance or custody issuer.
Exact branch startup `506a3182dc75d25226cc8a80690b879fbb9894a2`; pinned OC2 author `a61d5794271038fb20c94a75eaee401a66613ce9`; independent OC3 reviewer `9cd47a829473a6e92392582b4f01f2c564aa5dce`.

## Genuine execution
Exactly pinned original custody module Git blob `f117f380c524db5b1eae0ce280be23f1c4bf2c23`, OC1 31 + OCR1 45 + OC2 19 tests, and OC3 36 tests were reconstructed. OCR1 and OC3 evidence archives were authenticated and OC3 archive `068b158363b96d5a7cdc03eb059efb8a8d159b26` had matching SHA256 `7a3d7913a5c388569f654aaf83a0a64c9b16de28065551a3e7a7d3749be33837`. Six source blobs plus the OC3 source checked against exact native Git blob SHA-1 identities.

| Executed unchanged source court | Pre | Post |
|---|---:|---:|
| Inherited OC1 31, OCR1 45, OC2 19 | 89 PASS / 6 RED | included in 131 |
| Original OC3 36 | 26 PASS / 10 RED | 34 PASS / 2 RED |
| Combined original 131 | 115 PASS / 16 RED | 121 PASS / 10 RED |
| New OC4 source-free controls | — | 36 PASS / 0 RED |

**All ten original OC3 REDs B02–B04, C05–C06, D04–D05 and E05–E07 are now PASS without changing OC3 test source.** Original six historical REDs stay retained without editing or xfail. Four older positive cases now become RED because bare `content_digest` signatures lack required capsule identity; see action register. **Do not claim 131 green or I2 acceptance.** This is a principled compatibility collision requiring a competent future owner.

## Bounded implementation
`repro/custody_protocol.py` is the exact executed source `af2b7e943018077cb36808b5af1cd67704624bec`. Full canonical dataclass capsule envelope commitment binds capsule ID, purpose, lawful set, version, freeze and remaining digests. The test-only signer must explicitly supply `capsule=c` to sign; source-free `require_second_signature` rejects raw content-only signing. This necessarily invalidates four older positive assertions. `MockSigner.verify` retains standalone mock verification without promoting it to real authority.

Local escrow adds `unblinded_at` to the UNBLIND journal proof and checks materialized `capsule_id`, holder, timestamp, ledger and state equality. Blind three-arm blocks type-check nonce and arm, refuse whitespace and nonhashable arms. Strict projection rejects nonstring menu/context and normalizes Unicode combining variants such as U+034F in lexical leak checks while preserving benign words and generated packets.

Runtime: Python 3.13.5, pytest 9.0.2, isolated filesystem and subprocess verified. Source-free only. The remote repository contains the runnable patch and OC4 36 new controls; all original sources remain in their pinned original commits. Full pre/post JUnit, stdout, original test source and per-case JSON matrix are retained in the delivered local `OC4_EXECUTED_EVIDENCE.tar.xz` artifact; they are not claimed to be included in this report until independently attached and verified.

## Limits
TEST_ONLY fixture keys are deterministically public; holder registration is in-process and self-issued. The ledger has no independently protected durable anchor, OC3 C07 remains NOT_REACHED, and no real institution/custodian, semantic issuance, model/provider grant, source use, production event, V3, physical world or human-perception authority exists. I2 independent review must be separately dispatched by HQ after complete return.
