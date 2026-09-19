# EE-P2R6V — WVS7 MATERIALIZER BINDER-SHADOW RECURSION REPAIR

Status: `QUALIFICATION_PENDING__DO_NOT_ADOPT_YET`

Branch:
`agent/rabochii-prev3-ee-p2r6v-wvs-binder-recursion-repair-r1`

Commission tip:
`9cf312c74000c163a124cf32ca0893275c5b02ee`

Production candidate:
`a500440ee904af98a14df72d1f1cb5a4b9f02728`

Production file:
`WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py`

Production mutation is exactly two lines:
- alias accepted P2R1 `bind_governed_c11_projection` as `_bind_governed_c11_projection`;
- preserve public `bind_exact_projection_fields` and delegate exactly once to that imported alias.

Frozen expected identities:
- projection: `838070ff6b85d60d4f26f9153b0507ba425936c11a3de94a18d57bfcd083f24d`
- coordinate slot: `4a688332dca6462f357b092e7dfdba1216739139fd74e1c84395420827d153b6`
- coordinate authority: `9e7f98a7ad723743771d6bea39077553d2a3920ac4c077e90720bb9e44da029d`
- Lock2/tie order: `8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`

Qualification surface:
`rawlsing_next/tests/test_ee_p2r6v_wvs_binder_recursion.py`

Court spec:
`.rabochii/court_spec.json`

Governed court PR:
`#416` targeting held P2X base `ae8b1db9d8c3288e002950ac01123c70f3138320`.

No Library, source carrier, empirical outcome, or performance access is authorized or performed.
P2X is not moved.

Terminal remains pending until governed Browser court receipt is observed.
