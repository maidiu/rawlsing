# RAWLSING HQ CURRENT — POST SPLIT-R2 PROMOTION / PRE MACHINE READINESS

Status: `SPLIT_R2_FANIN_ADOPTED__CANONICAL_SPLIT_CONTROL_PROMOTED__FRESH_MACHINE_READINESS_NEXT__NO_MEASUREMENT_AUTHORIZED`

Checkpoint: `20260925T2059-0400`

Decision: `HQD-2026-09-25-105`

Semantic PRE-MAIN tip:
`2c0ca4a34925278b83b12a2644a87948acfe37d9`

Current protected joined execution:
`16f5e7d5f691e908d85dc1dd26b8a59a29f668f4`

Canonical source-split control:
`agent/vozhd-fiabc-source-split-alternate-runner-r1`
`ed8dabf015d1fd4b4ade9b55816a420b0bc1811e`

Fan-in evidence/docs tip:
`agent/vozhd-fiabc-split-r2-fanin-r1`
`cee9e27d57dc72771d9c3ec5df26493321feeef5`

Physical epoch:
`fc6afc9bc7b287f8fd0654e1da546faee7e6c85491e6735ebe4a161b0db3de35`

Current successor binding:
`WORKER_RETURNS/EE-P2X/10C_DARWIN_DRIVER_SUCCESSOR_BINDING.json`
blob `247725e51ed141cf31c112084590b69953765032`

Fan-in qualification:
- LiTS-I equivalence: PASS
- WVS7 equivalence: PASS
- fan-in: 102 tests + 65 subtests PASS
- protected joined-successor: 86 tests PASS
- zero raw source opens/hashes, decoder calls, production A/B/C launches/outputs, measured P2X
- 10 synthetic SIMPLE_TEST_ONLY process-envelope probes only

Next action:
fresh dual-machine readiness and pair verification against the exact protected joined head, promoted split-control head, epoch, runtime, canonical source SHA, clean checkouts, and fresh empty work roots.

Measurement remains unauthorized. A separate explicit HQ launch authorization is required after readiness/pair PASS.
