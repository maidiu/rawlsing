# EE-P2R6V — WVS7 MATERIALIZER BINDER-SHADOW RECURSION REPAIR

Repository: `maidiu/rawlsing`

## Execution surface
**BROWSER**

## Library access
**NO**

Exact branch:
`agent/rabochii-prev3-ee-p2r6v-wvs-binder-recursion-repair-r1`

Exact base:
`ae8b1db9d8c3288e002950ac01123c70f3138320`

Resolve live HQ first.

Commission-time checkpoint:
`20260919T0327-0400`

Immutable handoff:
`b994ea63d2b9571415677e0d47a16bcd3e8322bf`

Controlling decision:
`HQD-2026-09-19-081`

## Mission

Repair only the exact mechanical recursion defect in:

`WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py`

Current blob:
`3a3e228843656e023673310c26acbd41ecdc1b3b`

The module imports the accepted P2R1 binder `bind_governed_c11_projection`, then defines local `bind_exact_projection_fields` and incorrectly terminates that function with a self-call:

`return bind_exact_projection_fields(fields)`

This causes the observed WVS A/B `RecursionError`.

Repair must preserve the public helper name `bind_exact_projection_fields` while delegating exactly once to the imported accepted P2R1 binder, preferably via an explicit import alias.

No WVS semantic authority, projection authority, country-coordinate law, Lock2 identity, routing law or backend code may change.

## Qualification

Using tiny fixtures / exact accepted authority only, prove:

- no recursive self-call remains;
- exact projection identity remains `838070ff6b85d60d4f26f9153b0507ba425936c11a3de94a18d57bfcd083f24d`;
- coordinate identity remains `4a688332dca6462f357b092e7dfdba1216739139fd74e1c84395420827d153b6`;
- coordinate authority remains `9e7f98a7ad723743771d6bea39077553d2a3920ac4c077e90720bb9e44da029d`;
- exact P2F2/Lock2 law remains unchanged;
- mutation/authority-substitution negatives still fail closed;
- no carrier/outcome/performance access.

Only production file permitted to change:
`WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py`

PASS:
`EE_P2R6V_PASS__WVS7_PROJECTION_MATERIALIZER_BINDER_RECURSION_REPAIRED__EXACT_R6S_AUTHORITY_IDENTITIES_PRESERVED__READY_FOR_HQ_SELECTIVE_FANIN`

BLOCK:
`EE_P2R6V_BLOCK__<EXACT_FIRST_BINDER_OR_PROJECTION_IDENTITY_FAILURE>`

Do not move P2X. Return to HQ.
