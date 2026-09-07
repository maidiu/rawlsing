# GT34 OBL055 H1 — FRESH INDEPENDENT HOSTILE REVIEW R1

## Terminal

`FAIL__GT34_OBL055_ACCEPTANCE_BOUND_REPLAY_CONSTITUENTS_NOT_RECONSTRUCTED__IN_GRAIN_SUCCESSOR_REPAIR_REQUIRED`

The frozen OBL055 repair candidate is **not lawful for HQ adoption consideration**.

## Frozen target

- repair evidence tip: `04fe6ba92d3c87aa53e021fb7fdcd8b5edf31bc1`
- semantic candidate before court seal: `a854ac9cfa8ac7820c16ba371aff59ab284cc212`
- successor implementation blob: `fa169dbb525475c17b2495a5b35aa300aa809881`
- frozen W2 implementation blob: `54d9acba40f0eb1db8bb03aec3c1bb900f849588`
- HQ OBL056 authority hash: `6c9ab99a7d89835e7fdf405511abd7d6d66ced54b6e2fd8ef1863be842f39123`
- HQ OBL056 implementation blob: `49538b9c36e58e19a6dc293ecac5bc2dff58eebe`

## Freshness

Attack matrix frozen before hostile test authoring:

- matrix commit: `9676c19b72c0b90e675163597c798945407c4a29`
- attack families: `36`

Fresh hostile surface/court seal:

- hostile surface commit: `c13c3cc45de528ed4a59941256d8b8243c7d768a`
- hostile court tip: `a254475799b9f2864438646d45a8ed09da6481e6`

## Governed evidence

- workflow run: `34158297302`
- job: `101854605478`
- protocol self-test: `20 passed`
- hostile bounded court: `65 passed, 10 failed`
- receipt artifact: `10031712899`
- artifact ZIP SHA-256: `f3ce140d931122fc3de57588cdc5e47e86747e8fee84717ae29fdcea1239f71e`

## Exact defect family

The repair correctly rejects caller-self-issued OBL056 acceptance, receipt/role/registry mutation, currentness laundering, contact-role reuse, proximity laundering, and removal of fixed OBL056 authority/registry/rule provenance.

However, `validate_record` authenticates several replay constituents only by requiring a content-addressed pointer to be present in record provenance. An attacker can replace that pointer, canonically re-address the affected OBL055 replay manifest, and then recompute the lower W2 candidate/record/event identities. The forged record is accepted because the exact original source evidence object is not reconstructed and revalidated.

The ten proved manifestations are:

1. causal-use semantic evidence ref swap;
2. causal-use authentication ref swap;
3. subject-ingress authentication ref swap;
4. ADP-008 phase-state receipt ref swap;
5. ADP-008 phase authentication ref swap;
6. applicability authentication ref swap;
7. contact-occurrence semantic ref swap;
8. contact-occurrence authentication ref swap;
9. contact-independence semantic receipt ref swap;
10. contact-independence authentication ref swap.

## Jurisdiction

`WHOLLY_IN_GRAIN_OBL055_REPLAY_RECONSTRUCTION_DEFECT`

No new underlying semantic authority is required. OBL056 remains sufficient at its adopted acceptance-binding grain. The smallest lawful successor repair is to carry enough exact source evidence material in the replay manifests to reconstruct and rerun the already-existing W2 source validators during `validate_record`, while preserving the W2 record contract, transition machinery, authority ceilings, and zero-positive current boundary.

## Gates

- OBL055: `NOT_ADOPTED`
- positive V3 execution: `NOT_AUTHORIZED`
- project-current first-canary OEE: `NOT_AUTHORIZED`
- OBL031: `BLOCKED_ON_OBL055_HQ_ADOPTION`
- OBL032: `BLOCKED_ON_OBL031_CENTRAL_CLOSURE`
