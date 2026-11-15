# EXISTING SEMANTIC RESOURCE INVENTORY R1

Status: `HQ_PRESERVATION_INVENTORY__EVIDENCE_AND_LOCATOR_MAP__NOT_NEW_SEMANTIC_AUTHORITY`

Purpose: preserve the source/question-semantic resource excavation performed immediately before HQ succession so a new HQ does not mistake the post-generic campaign for a blank-slate semantic-mapping exercise and does not repeat archaeology already completed.

This inventory is a **locator/status preservation artifact**. It does not promote historical evidence to current authority, does not resolve supersession, does not create semantic equivalence, and does not activate PSC lanes.

## 1. Governing finding

Rawlsing already contains a large manually/documentarily adjudicated semantic world. The next campaign must begin by **inventorying, reconciling, and compiling existing semantic capital**, not by rereading ~18k question strings as though no prior semantic work exists.

The strongest recovered workload fact is from Library artifact `DDM_SEMANTIC_SALVAGE_WORKLOAD_AUDIT_R7G.md` (`file_000000003dfc81f7b5d21a40d47ac9dd`, version 1):

- conservative relational semantic audit universe: **3,331 units**;
- class A — current governed QRA anchor: **190**;
- class B — full historical structural review, no fallback semantic match: **954**;
- class C — full historical structural review with fallback semantic matching present: **2,098**;
- class D — partial structural-review coverage: **4**;
- class E — legacy QSM mapping only: **77**;
- class F — cold source review, no legacy QSM and no located structural review: **8**.

Binding interpretation: **8 cold != only 8 needing judgment.** The audit explicitly says most remaining work is reconciliation/adjudication over prior semantic work, not first-pass discovery from blank source material. Fallback-cluster lineage remains retrieval evidence only and cannot establish equivalence/driver/facet/axis/target authority.

## 2. Existing authority object model

Library artifact `AUTHORITY_OBJECT_MODEL.md` (`file_000000005fb0820d84693fada1207929`, version 1) records distinct layers that MUST NOT be collapsed:

1. source question/response authority — exact question identity/text, source/wave/country applicability, role/subrole, directionality where authorized, response semantics, routing, source-local continuity, structural/position roles and provenance;
2. P3A proposition-candidate authority — deterministic candidates/obligations, not canonical family truth;
3. P3C canonical proposition authority — canonical families, revisions, membership, variants/exclusions, genealogy and adjudication;
4. V550J source-native joint-configuration authority — exact respondent-level joint configuration rules;
5. V550/V551/V552 execution authority — execution consumes authority and **cannot create upstream semantic authority**.

Preservation law:

`EXECUTION_ARTIFACT != UPSTREAM_SEMANTIC_AUTHORITY`

`SOURCE_DOCUMENTATION != RAWLSING_SEMANTIC_AUTHORITY`

`PORTABLE_SOURCE_EXECUTION != AUTOMATIC_SEMANTIC_AUTHORITY`

## 3. Authority census already exists

Library artifact `AUTHORITY_OBJECT_CENSUS.csv` (`file_00000000364c822fa90c6077300d0260`, version 1) is already an authority-object census and must be treated as a high-value PSC01 input, not rediscovered from filenames.

Material rows recovered during this excavation include:

- current recovered `question_structure_register.csv` carrier: **18,792 rows / 35 family-wave pairs**; manual/source topology + source-structure classification + semantic-driver fields; historical/manual authority with remaining driver-provenance/succession caveats;
- Full Question Relation Authority R1: **18,518 rows**, live canonical within its jurisdiction;
- QSMv2: **3,196 semantic units / 4,438 implementations**, live canonical subauthority for its exact scope;
- QRA: frozen directional/polarity precedent within R1;
- negative/block/review authority: current first-class semantic input;
- response-scale registry: current accepted response-scale authority;
- V550/V551 response-semantics binding: accepted execution authority derived from named upstream authority.

Critical ceiling: the census itself records that FQRA is **not a lossless successor of the historical question-structure register**. Different authority surfaces have different jurisdictions.

## 4. Exact authority reference map already exists

Library artifact `EXISTING_AUTHORITY_REFERENCE_MAP.csv` (`file_000000001ccc81f5b233fc06ceee33aa`, version 1) supplies exact locators and, where measured, identities for accepted authority/evidence objects.

Recovered entries include:

- A01 — Full Question Relation Authority R1;
- A02 — FQRA SHA manifest;
- A03 — 35-wave question relation registry;
- A04 — V550/V551 response-semantics binding;
- A05 — response-scale encoding registry;
- A06/A07 — accepted WVS7 source-native topology/applicability evidence;
- A08/A09 — official WVS7 questionnaire/codebook documentary authority;
- additional exact fail-closed gap witnesses.

Use this map as a locator/provenance input. Verify live GitHub paths/blobs and current authority status before consumption.

## 5. GitHub authority carriers verified during this excavation

The following carriers were verified on `integration/pre-main-reconciliation-r1`:

### Full Question Relation Authority R1

Path:
`data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv`

Git blob:
`e4f79f47417077c840f985d37e9341f068e3cf8f`

The containing authority directory also includes exact integrated QSMv2 carriers and negative/status surfaces, including:

- `QSMV2_INTEGRATED_UNIT_AUTHORITY_3196_R1.csv` — blob `1b4b1991136814ce475502a941253f7a3724a8db`;
- `QSMV2_INTEGRATED_IMPLEMENTATION_BLOCKS_4438_R1.csv` — blob `8af5550f5b51d4bc7288351e44f8f03a9adad3f6`;
- `BLOCKED_QSMV2_UNITS_21_R1.csv` — blob `8c1c8ca2d0ee37a28a247464b69f7891ded3cccf`;
- `BLOCKED_QSMV2_IMPLEMENTATIONS_41_R1.csv` — blob `8bb58c4a65381689c15831cd0fc9c3da1ec9c63d`;
- `CANONICAL_COORDINATE_REGISTRY_FINAL_R1.csv` — blob `796e94947240cc1200d6c70c0822695407f99c85`;
- `GOVERNING_PROVENANCE_R1.csv` — blob `08e07a74e2b58a1e72bf55a215780f57175e3d8a`;
- `FINAL_HOSTILE_QA_R1.json` — blob `2aa8a71e73ab2b4fc976ee4e81605aaf2f79b386`.

### V550/V551 response semantics binding

Path:
`data/ddm_build_copy/authority/v550_v551_response_semantics_contract_binding_v1.csv`

Git blob:
`ef77bcbe61385a10fe28b67c15a13f4f794e58e0`

### Response-scale encoding registry

Path:
`data/ddm_build_copy/authority/response_scale_encoding_registry_35wave_active_v1.csv`

Git blob:
`2a45215854d1feb4ba0a779edcb29479143ab613`

Any locator present only in Library census/reference material but not independently verified on the current control branch during this excavation remains `LOCATOR_PRESENT__LIVE_PATH_NOT_YET_REVERIFIED`, not absent and not current by assumption.

## 6. Historical question-structure/manual authority is not disposable

Library census evidence identifies a recovered current `question_structure_register.csv` carrier with **18,792 rows / 35 family-wave pairs** and historical/manual source-topology and source-structure meaning. Manual core preservation has been substantially proved, while some driver-semantic lineage and succession remain separately governed.

Library artifact `P10_G1A_MANUAL_AUTHORITY_PRESERVATION_RECLOSURE_RETURN.md` (`file_000000006040822fa6ee9d9ff7ed58f4`, version 1) records that:

- the S14/QSR historical manual ancestry and exact 18,792-row register lineage were recovered;
- Layer A canonical recovery was positively resolved;
- Layer B recovery reservoir and Layer D executable memory were recovered;
- historical itinerary manual-authority succession remained blocked/unresolved at that court;
- V525b / d62 mixed semantic-driver lineage retained unresolved assertion-grain succession debt.

Therefore PSC01 must preserve **authority surface + jurisdiction + succession status**, not simply pick the newest-looking file.

## 7. Recovered typed semantic-relation layer is distinct from flattened question authority

Library recovery evidence records a semantic-relation corpus whose jurisdiction is not identical to FQRA/QSMv2.

Verified recovery invariants include:

- Job3 terminal positive typed relations: **1,190**;
- Job3 new accepts: **552**;
- Job3 rejects: **697**;
- Job3 blocks: **15**;
- O12 parent positives: **638**;
- R16F positives: **144**;
- strict source-first T06 positives: **64**;
- T15 positives: **188**;
- R16F wave×rule cells: **315**.

Library artifact `04_ACCEPTANCE_TESTS.md` (`file_0000000087c881f58be2ccba28274646`, version 1) freezes these acceptance invariants and the epistemic laws:

- REJECT != empirical non-correlation;
- BLOCKED != negative;
- typed semantic negative != empirical anti-correlation;
- zero positive coverage != absence;
- source proximity / lexical similarity / embeddings / shared driver-facet != relation authority;
- semantic relation truth and empirical co-travel remain independent layers.

Other recovered audits explicitly warn that FQRA's applied question/implementation coordinate surface does **not** by itself contain the full typed relation objects, relation roles, nonedges, blocked edges, open-world coverage, and source-first T06/T15 distinctions.

PSC01/PSC02 must therefore inventory this recovered layer rather than reconstruct relations from flattened coordinates.

## 8. Existing workflow implication for PSC01-PSC03

The post-closure campaign MUST begin from these facts:

1. semantic capital already exists at multiple grains;
2. the workload is primarily **authority reconciliation and compilation**, not blank-slate NLP interpretation;
3. only exact accepted authority can be compiled into T03 production intake;
4. historical/manual/recovered objects that are not current remain evidence/provenance/review inputs, not silently promoted truth;
5. negative, blocked, review-required, superseded and outside-jurisdiction states are first-class terminal statuses;
6. one authority surface must not silently supersede a different-jurisdiction surface;
7. unresolved succession is a finite adjudication queue, not permission to regenerate meaning from question text.

## 9. Required successor use

Before commissioning PSC01, successor HQ MUST consume this inventory alongside:

- `00_HQ_READINESS_DOCKET.md`;
- `01_DORMANT_DISPATCH_DOCKET.json`;
- the Library authority census/reference artifacts named above;
- the live GitHub carriers verified above.

PSC01 should treat `AUTHORITY_OBJECT_CENSUS.csv` and `EXISTING_AUTHORITY_REFERENCE_MAP.csv` as seed inventories to verify/reconcile, not as complete/current truth by fiat.

## 10. Anti-loss law

`KNOWN_SEMANTIC_CAPITAL != BLANK_SLATE_QUESTION_TEXT`

`HISTORICAL_OR_RECOVERED_AUTHORITY != AUTOMATICALLY_CURRENT_AUTHORITY`

`CURRENT_SCHEMA_CAN_CARRY_REF != MANUAL_AUTHORITY_PRESERVED`

`FQRA_JURISDICTION != COMPLETE_HISTORICAL_SEMANTIC_RELATION_JURISDICTION`

`SALVAGE_LINEAGE != AUTOMATIC_PROMOTION`

`RECONCILE_AND_PRESERVE_BEFORE_REINVENTING`
