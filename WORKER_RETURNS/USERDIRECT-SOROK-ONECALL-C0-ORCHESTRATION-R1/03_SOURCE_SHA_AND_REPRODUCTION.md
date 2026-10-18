# Reproduction, exact source identities, and no-relabel guarantees

## Exact authored and actually executed source

- `onecall_c0.py` 18,378 bytes; SHA256 `3f0da92095f8355c7512d49ac546c846b6026d3775533ba56be7e148e11abfa1`; Git blob SHA-1 `f45e4f5573495f060503f92b7630ec83531ced4d`.
- `test_onecall_c0.py` 12,497 bytes; SHA256 `d9d2038a35510eb11e03b0f333ca0fa60fcf6b3b3127ef0e9b3cce08fb0c930b`; Git blob SHA-1 `7b26c40e9ba3f5e170a8abff24e21e2051257af7`.
- **Complete runnable test/source + JUnit/stdout/cold comparison/passport/manifest ZIP** `ONECALL_C0_SOURCE_TESTS_EVIDENCE.zip`; SHA256 `691b42d08d5ddc0933940b094c9465e329194a9f25e02b685e35c5a042341bdd`.
- Smaller runnable/source/JUnit/comparison ZIP `ONECALL_C0_RUNNABLE_MINIMAL.zip`; SHA256 `82ce78867e9330aa95a4a110c4371a41271013e94805d4e0e2545807a52a4dcf`.
- Pure Python sources-only ZIP `CODE_ONLY.zip`; SHA256 `65d373537511d32de908a9921fc782cddf2531d0142a394d2fe07c98c3ec7b98`.

The conversation's verified sandbox artifacts contain these source bundles; **no binary ZIP has yet been verified as committed to this GitHub return**. Do not infer its existence from this Markdown. Exact source/JUnit can be unpacked locally and run `python -m pytest -q test_onecall_c0.py --junitxml=onecall_junit_replayed.xml`, then run all three modes via `python onecall_c0.py --mode ONE_CALL|TWO_CALL|FIXED_PACKET --out path.json`.

## Pin audit

- Branch sealed `4c7dcb4f31a73f4c260c9b29cdf356067ab284d7`; commission blob `2b8cef16f7c06226082398720ee5cec56e928d3b`.
- October 18 single-call bank `a1681a40b40dd1be5c67ec55857320d9e3a8b3ed`, three docs blob `33b459b633c342dec62e1e47b1eeff8c70759ad7`, `89f12a5291fe1dffc1a6dfe80b00db945fdc1235`, `8871da0870f32700a2604cd7bab92307e2e88426`.
- Historic V3 design PREMAIN `7b1dcb82e0326737b4af172b17f9c2b7e25fd848`; blobs baseline `148640d3a758aeea5ba68fab4dff1bb1e66ad059`, result `dfcc7e4fc7b6e907218d7a368ceb9d269a49206d`, V3 ruling `49095f763c5c371d98bb57a01aaf5f47dc7b1ae1`.
- B3 candidate `47b46a85b9ebb633754866f1e6f1b12db3bd2012`; `developmental_loop.py` Git blob `a8fc1bf2247072e8530e20635cdb575873cf484a`. **NOT IMPORTED.**
- N10W independent R1 `c433be8645ae484a831b2b19bab079055dd6be62`; `00_VERDICT.md` blob `d4652e924ef4a49f55244424228c7f45846ec3ac`. **NOT IMPORTED.**
- Corrected B2 `8f7966d6d0bbb1ea2e57359de9defbcf552268bd`; M2 `5c2fbe14ccfa5027becfabc682206a1e61aaf986`; F2 `a24429906c93446f9d912e7054d48f9f51aee63d`; all were **context/evidence**, not physical dependencies.

**Original F1's 17 native RED cases are completely untouched**: F01 F02 F03 F04 F05 F06 F07 F08 F10 F11 F13 F15 F16 F17 F18 F19 F21. No original F1/F2 runtime claimed. The sourcefree fixture cannot issue real developmental psychology, route probability, Pyat source use or actor events. Pending separate independent I2 review and eventual competent actor owner.
