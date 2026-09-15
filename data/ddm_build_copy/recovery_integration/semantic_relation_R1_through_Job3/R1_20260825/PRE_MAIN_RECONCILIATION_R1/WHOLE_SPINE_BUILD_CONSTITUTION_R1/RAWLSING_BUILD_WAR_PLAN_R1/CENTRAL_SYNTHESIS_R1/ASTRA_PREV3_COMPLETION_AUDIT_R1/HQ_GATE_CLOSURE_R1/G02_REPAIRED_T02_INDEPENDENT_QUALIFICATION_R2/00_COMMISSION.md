# G02 — REPAIRED T02 INDEPENDENT HOSTILE QUALIFICATION R2

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-prev3-gate-g02-repaired-t02-hostile-qualification-r2`

Base / repaired return: `f02336187e50a443d929ff7abbe5dcd5f3950f70`

Exact grain:

`SDTF_R4_REPAIRED_GENERIC_BATCH_ADAPTER_INDEPENDENT_HOSTILE_QUALIFICATION_R2_ONLY`

## Candidate identities

- implementation: `rawlsing_next/sdtf_r4_generic_batch_adapter.py`
- repaired implementation blob: `f6427a42524086194ed6fca9ba2387561ff00891`
- producer test blob: `7b4190601757fa69352d1a990c27242c67226cae`
- V01 repair-regression blob: `a8fcb9f4f0d260f4660b89df0a74493c6dffda8e`

## Mission

Freshly and independently qualify the repaired T02 generic R4 batch adapter against the exact U01 predecessor-lineage blocker and the frozen S03/R4 boundary laws.

The court MUST prove at minimum:

1. forged predecessor hash with absent prior snapshot fails closed;
2. exact co-present predecessor is accepted;
3. wrong-hash predecessor with co-present prior fails closed;
4. identity-invalid/stale supplied predecessor cannot prove lineage;
5. lineage result is deterministic and order-independent;
6. lineage failure is row-local and does not contaminate unrelated valid rows;
7. existing producer boundaries remain green, including no silent N/A, no invented authority/currentness/body, exact duplicate idempotence, conflict quarantine and currentness-evidence closure.

Run the unchanged producer tests and V01 repair regression as supporting regression evidence, plus a fresh G02 hostile qualification test written on this branch.

## PASS law

PASS only if the governed repository court executes all commissioned tests successfully against the exact repaired candidate identities and emits a valid court receipt.

`REPAIR_PASS != INDEPENDENT_QUALIFICATION_PASS`

`PRODUCER_TEST_PASS != INDEPENDENT_QUALIFICATION_PASS`

## Boundaries

No semantic authority creation. No concrete rule minting. No rule-currentness selection. No source/question adjudication. No actor/entity fact materialization. No topology. No V3/person state. No OBL063 revival. No MAIN/PRE-MAIN semantic mutation.

## Successor gate

PASS returns to HQ for adoption of repaired T02. Only HQ adoption may authorize T02 production use and satisfy the generic-layer closure prerequisite.