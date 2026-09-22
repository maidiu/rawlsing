# PREMAIN CLOSED35 — EVS1999 TYPED-MISSINGNESS PRESERVATION REPAIR — R1

Repository: `maidiu/rawlsing`

**AGENT TYPE: BROWSER / GITHUB / SOURCE-FREE CODE REPAIR ONLY**
**MODEL: GPT-5.6 Sol High**

Branch:
`agent/rabochii-premain-closed35-evs1999-typed-missingness-repair-r1`

Exact base:
`fe6714ed66c5f5c4e0440b6ea9f0f83e63c4f262`

Read the accepted Wave-1 HQ fan-in at:
`agent/vozhd-premain-closed35-contract-audit-wave1-fanin-r1`

The audit proved one concrete source-free preservation defect in the current EVS1999 realization:

- the exact reader contract uses `user_missing=True`;
- `R35_REQUIRED_PHYSICAL_DIMENSIONS` does not currently require typed missingness;
- no typed-missing-state preservation projection is exposed by the realization contract.

## Mission

Repair only that preservation boundary.

Required result:

1. the EVS1999 realization contract explicitly preserves the decoder's typed physical missing state/declaration wherever the generic R35 physical contract requires it;
2. the repair does **not** infer any particular EVS1999 raw code to be user missing, system missing, substantive, routed, or semantic;
3. the repair does not change documentary semantics, routing, weights, replay identity, encoding law, or bounded UNKNOWN policy;
4. source-free hostile tests prove that a candidate realization which collapses user/system/ordinary physical state cannot satisfy the EVS1999 contract;
5. existing EVS1999 preservation obligations remain exact.

Use existing integrated realization modules with already-correct typed-missingness preservation as **structural examples only**.

## Prohibitions

Do not use the user's Mac.
Do not open/materialize EVS1999 SAV or any raw survey carrier.
Do not execute real-source decoding.
Do not infer missing codes from labels, metadata examples, distributions, or neighboring releases.
Do not touch PRE553 generic semantics unless a minimal generic defect is independently proven.
Do not mutate governed branches or sibling branches.
Do not run Candidate A/B/C, real I05, measured P2X, or P3.

## Required outputs

Own only:
`WORKER_RETURNS/PREMAIN-CLOSED35-EVS1999-TYPED-MISSINGNESS-REPAIR-R1/`

Return:

- `00_RETURN.md`
- `01_PATCH_SCOPE.md`
- `02_HOSTILE_TESTS.md`
- `RETURN.json`

Commit code + tests + return packet and push.

Terminal only if green:

`PREMAIN_CLOSED35_EVS1999_TYPED_MISSINGNESS_REPAIR_R1__SOURCE_FREE_REPAIR_PASS__NO_SOURCE_EXECUTION__NO_CANDIDATES_RUN`
