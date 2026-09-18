# EE-P2R6B — CONCRETE RELEASE-REALIZATION BINDING ISSUER / VERIFIER PREPARATION

Repository: `maidiu/rawlsing`

Execution surface: **BROWSER**

Library access: **NO**

Exact branch:

`agent/rabochii-prev3-ee-p2r6b-realization-binding-issuer-prep-r1`

Exact base:

`32e224c28d720fce7cdcf6182afb5d327e8a1cf0`

First resolve live `HQ_HANDOFF/LATEST.json` and verify its immutable checkpoint packet.

Read the adopted EE-P2R5A authority and the exact EE-P2R5B mechanical receipt schema/package.

## Grain

`R5A_CONCRETE_REALIZATION_BINDING_ISSUER_AND_VERIFIER_PREPARATION_ONLY`

No carrier access. No actual binding issuance because the accepted successor I02 release does not yet exist.

## Mission

Build the exact deterministic Browser-side issuer and verifier that will later consume the successful local EE-P2R6L/R5B execution receipts and emit one concrete `ReleaseRealizationBinding` candidate under adopted R5A authority.

The future post-local act should be mechanical: provide exact local receipts -> issuer validates -> exact binding candidate emitted -> verifier passes -> return to HQ.

## Controlling R5A identities

- realization authority: `9da19997168612891f59012e69674bac59fbee417d9b30b003171f3074168bf5`
- binding schema: `a1da1ea78dce423ea3520726d0477b058057482d67964056743e08389d9045a0`
- R4A successor clause: `d8e3d9a19fa36599e8cd6b1bc8e82092c425fd9119be478f7ba79335d05a1b3e`
- aggregate R5A: `d9aa476c493810651baefa8bad23990d9dd80812a48670ad2052353f0e7d52a2`

Frozen scope anchor:

`bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297`

Source SHA:

`7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

Accepted base release:

`e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26`

## Controlling R5B package

Read exact R5B return head and at minimum:

- `WORKER_RETURNS/EE-P2R5B/04_SUCCESSOR_RELEASE_RECEIPT_SCHEMA.json`
- `WORKER_RETURNS/EE-P2R5B/05_SUCCESSOR_RELEASE_VERIFIER.py`
- `WORKER_RETURNS/EE-P2R5B/06_LOCAL_EXECUTION_PACKET.json`

The issuer must consume only receipts that pass the exact R5B verifier.

## Required issuer behavior

Input:

- successor release receipt;
- ReplayManifest sidecar;
- M01-M18 sidecar;
- extension-scan sidecar;
- adopted R5A authority material.

Before issuance, prove:

1. R5B verifier PASS;
2. exact source SHA;
3. exact frozen scope anchor;
4. exact accepted base release lineage;
5. exact six F02 selector refs and q310/q311 extension identities;
6. accepted I02 ingest disposition;
7. exact I02 runtime release ref exists and is distinct from frozen scope anchor;
8. exact ReplayManifest;
9. complete M01-M18;
10. exact repository-resolution receipt;
11. no R5B realization/equality claim;
12. no unexpected semantic extension affecting selector truth;
13. exactly zero pre-existing active binding in the authority epoch being prepared.

## Binding candidate law

The future binding must be directional:

`FROZEN_F02_SCOPE_ANCHOR -> ACCEPTED_I02_RUNTIME_RELEASE`

Never equality or aliasing.

It must content-address at minimum:

- exact adopted realization authority ref;
- frozen scope anchor;
- runtime I02 release ref;
- exact source SHA;
- accepted base lineage;
- exact candidate projection identity;
- exact ReplayManifest ref;
- exact M01-M18 closure identity;
- exact repository-resolution evidence;
- exact extension-member identity set;
- exact R4A authority closure;
- status/epoch fields required for uniqueness.

The issuer must not invent the runtime release hash. It comes only from the R5B/R6L accepted I02 receipt.

## Uniqueness / fail-closed law

Prepare a verifier that rejects:

- zero proof closure;
- multiple active positive bindings for same scope/source/authority epoch;
- duplicate scope with different runtime release;
- runtime release == frozen anchor;
- unverified or non-I02 runtime release;
- latest/default/fuzzy/nearest resolution;
- cross-source binding;
- missing F02 member;
- changed selector identity;
- post-outcome mutation;
- wrong R4A/R5A authority identity.

## Current Browser qualification

Because no real successor release exists yet, use a synthetic-but-structural receipt fixture only to test issuer mechanics.

Clearly mark all fixtures NONEMPIRICAL and NONBINDING.

Prove that no real concrete binding is emitted during this commission.

## Required outputs

Write only under:

`WORKER_RETURNS/EE-P2R6B/`

At minimum:

- `00_RETURN.md`
- `01_BINDING_ISSUER_CONTRACT.json`
- `02_REALIZATION_BINDING_ISSUER.py`
- `03_REALIZATION_BINDING_VERIFIER.py`
- `04_POST_LOCAL_INPUT_CONTRACT.json`
- `05_BROWSER_QUALIFICATION_RECEIPT.json`

## PASS terminal

`EE_P2R6B_PASS__CONCRETE_REALIZATION_BINDING_ISSUER_AND_VERIFIER_READY__AWAIT_EXACT_LOCAL_I02_SUCCESSOR_RELEASE_RECEIPTS`

PASS wakes HQ adjudication only.

## Hard forbidden

- no Library/carrier access;
- no actual concrete binding issuance;
- no invented runtime release ref;
- no production evaluator/I05 changes;
- no P2X/BE1 execution;
- no Candidate-C repair;
- no selector remint;
- no D02/F02 workload mutation;
- no Lock1/Lock2;
- no MAIN or semantic PRE-MAIN mutation;
- no rebase or replacement branch.

Run the governed Browser qualification court and return final branch tip, exact artifact identities, run/job/artifact, and exact successor wake.
