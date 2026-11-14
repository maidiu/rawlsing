# 05 ASSOCIATION LANE REGISTRY — F5 original-first mechanism analysis

Source identity: historical `25830fe7462bb9e29bc4087e6ae14f3f84cec377` blob `e90470f12dc6fb98d874af989854b83e8bc61067`; protected `6a5c12f04323d74001f9632063ec907f4fc4468e` blob `5b67e3f98a5faf95a6c82700af2346fef6e306a5`. Historical ID or owner: `R4 V550J association lane`. Case `R6:C:05_ASSOCIATION_LANE_REGISTRY` is a seam comparison only; **0 canonical historical T identities created**.

## Historical computation
[Historical function `AssociationLaneRegistry.classify L164;classify_required L201`](https://github.com/maidiu/rawlsing/blob/25830fe7462bb9e29bc4087e6ae14f3f84cec377/data/ddm_build_copy/ddm_v550j_registry_classifier.py) — `data/ddm_build_copy/ddm_v550j_registry_classifier.py`.

**Inputs/denominator/source grain:** Source, canonical wave, country and variable code vs governed registry

**Transformation (what actually happens):** Classify exact first, then prefix, then regex matching lane, in source-scope

**Output and learned information:** Typed association lane / publishability authority

**Negative/admission rules:** No match => named association_lane_authority_missing

**First selected or statically identified reader:** V550J compiler verifies association lane for source candidate

## Present operation
[Current function `SourceRelationResolver.require L701`](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/rawlsing_next/pre553_source_relations.py) — `rawlsing_next/pre553_source_relations.py`.

**Inputs/authority:** Exact source-universe relationships and operation scopes

**Transformation:** Verify source relationship permission, not respondent association lane classifier

**Output:** OperationGuardReceipt only

**Negative/refusal:** Missing required source relation/authority refuses

**First bounded reader:** I03 guarded composite query, no V550J association reader shown

## Differential verdict
**Unproved edge:** Source code association score/meaning cannot be reconstructed from generic relation permission

**Decisive counterfactual/negative test:** Exact/prefix/regex precedence and actual association output consumer with source IDs

**Evidence grade:** S1 code-body and static read. No execution witness, no actual same-source source-to-N9-to-Sorok science, no parity certification. These interfaces have different source grains and cannot be called superseded without selected source-reader mechanism verification.
