# Artifact Audit — Full Question Relation Authority Final R1

Status: `DEEP_AUDIT__FINAL_R1_CANONICAL_RELATION_AUTHORITY_WITH_EXPLICIT_BLOCKERS`

## Identity

Historical directory:

`Rawlsing_Full_Question_Relation_Authority_Final_R1_20260814/`

Recursive directory SHA-256:

`2cae7bb0cbd8c1717bdd85f0d876ca3f2ce3ee36b7429d1595a68cf61bd3b101`

Historical ZIP:

`Rawlsing_Full_Question_Relation_Authority_Final_R1_20260814.zip`

ZIP SHA-256:

`4faf97fccfd6cefe8842f0fe4a95ce58fdc1c3aa77c50203703112e3c49e09e0`

Key member identities from the sealed historical tree:

- `00_README_FIRST.md` — `5dd35248cf971aee6fd69cbee606486001412b8c14bc41d2b3475801576792ac`
- `AUTHORITY_STATUS_COUNTS_FINAL_R1.csv` — `77bbad54d1c138126979017a075725c08171d166d64a130fee2b2bd042744c4b`
- `BLOCKED_QSMV2_IMPLEMENTATIONS_41_R1.csv` — `aebe07c1fe47aa7804e09819d3822eed5003641bd98a54135fd5e9db1cec05c7`
- `BLOCKED_QSMV2_UNITS_21_R1.csv` — `4114b0f1ff3a236ac910bfff9be1c5e608721d0a92ccb0f0982e3a38cdbc4c4c`
- `CANONICAL_COORDINATE_REGISTRY_FINAL_R1.csv` — `26ed57fa615c51c3e52ae7b7f5042a1c7d7020602ba37d4e1294e101287c9471`
- `QSMV2_INTEGRATED_UNIT_AUTHORITY_3196_R1.csv` — `80af2ece8e8f9b669ef405ba2b506d68e8e36facc404609cc539b3419a5c48fb`
- `QSMV2_STRUCTURAL_AUTHORITY_LEDGER_4438_R1.csv` — `054034b1beb5f8f43e8075a29b8180c3249a1efd15ef0f7de7b29d0a1b97287f`
- `QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv` — `0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13`
- `question_structural_mapping_live_PLUS4_FINAL_APPLIED_R1.csv` — `c223d9c9b9a817dcfa7c7fda6a9a7cbc9d31277c21b4de0f1c0af1025de7217f`

## What it was for

This release reconciles the **entire 18,518-row July-19 QSM universe** with:

- QSMv2 relational semantic-unit adjudication;
- manual authority;
- frozen QRA precedent;
- source/wave scope dispositions;
- explicit blocking where structural/source/identity authority remains insufficient.

It exists because a populated QSM row is not the same thing as a governed relation-authority row.

## Actual authority surface

The full authority table has **18,518 rows and 99 columns**. It retains original question/semantic fields while carrying provenance and authority material including:

- canonical source/wave/scope;
- manual and P2 authority fields;
- semantic lane/role/subrole;
- response topology and binding status;
- directionality/polarity/calibration;
- position conditioning;
- six structural coordinates;
- authority status;
- QSMv2 unit/component/terminal-owner state;
- blocked-coordinate state;
- governed payload hashes.

QSMv2 integrated:

- **3,196 / 3,196 relational semantic units**;
- **4,438 / 4,438 source implementations** structurally adjudicated and block-bound;
- **4,397** formerly blocked rows promoted to `GOVERNED_QSMV2_RELATION_AUTHORITY`;
- **41 implementations across 21 units** remain `BLOCKED_STRUCTURAL_MAPPING_AUTHORITY`.

Together with earlier accepted authority, **4,622 rows** are fully governed relation rows.

Final authority-status counts:

- `GOVERNED_NON_DIRECTIONAL_DISPOSITION`: 12,611
- `GOVERNED_QSMV2_RELATION_AUTHORITY`: 4,397
- `GOVERNED_ADMINISTRATIVE_DISPOSITION`: 966
- `EXCLUDED_INACTIVE_WAVE`: 259
- `GOVERNED_MANUAL_RELATION_AUTHORITY`: 173
- `FROZEN_ACCEPTED_GSS`: 52
- `BLOCKED_STRUCTURAL_MAPPING_AUTHORITY`: 41
- `BLOCKED_SOURCE_AUTHORITY`: 10
- `BLOCKED_IDENTITY_OR_AUTHORITY_JOIN`: 9

Final hostile QA reports **4,886 checks and 0 failures**.

## Governing provenance

The package explicitly names these governing inputs and hashes:

- July-19 QSM input — `7b4f93a3224f360d7daca9eeff2c02b48407c12d53ad128c87dc0585b9080fec`
- QSM Full Authority Checkpoint R2 — `4bbc559835e6e6d2bbbe868898d230a8f99edae9f0ef78eae7e5d55d429fa696`
- QSMv2 Cycle1 Vozhd Integrated Authority R1 — `bf37fe0ec726a8a7d42572e2e461f14851984a5198cb022086e676495d85b4db`
- QSMv2 Cycle2 Vozhd Integrated Authority R1 — `6371de5454dfc1ef095a0e0e41db4c9e8571aadb4a6e3022b21fa954b2c42262`
- QSMv2 CrossSource Owner Adjudication Return R1 — `2ba9dc3ad14540f5dc46a6fd7955035deed4ed58de5ba9d5859bac0315dd43dc`

## Quality judgment

`VERY_HIGH_CANONICAL_FAIL_CLOSED`

The significant feature is not merely the number of governed rows. The package retains distinct terminal states rather than filling every blank to obtain apparent completeness.

It also preserves the frozen 236-row QRA regression and prevents worker/inference namespace leakage into active authority.

## Completeness judgment

`FULL_18518_ROW_UNIVERSE_WITH_EXPLICIT_UNRESOLVED_STATES`

This is a full-universe disposition surface, **not** a claim that all rows became relation authority.

Explicit limitations include:

- 259 Asian Barometer W6 rows remain excluded;
- 41 rows remain structural-mapping blocked;
- 10 remain source-authority blocked;
- 9 remain identity/authority-join blocked.

That is strength, not incompleteness disguised as success.

## Irreducible concepts to conserve

### 1. Full-universe disposition != universal positive authority

Every implementation can receive a governed terminal disposition without every implementation becoming admissible relation evidence.

### 2. Manual/frozen/adjudicated provenance is an epistemic class

Later DAG products may normalize representation, but they must not erase whether a decision came from manual authority, frozen precedent, governed QSMv2 adjudication, source authority, or unresolved state.

### 3. Partial-coordinate knowledge is legal

Blocked implementations may retain explicitly governed coordinates while unresolved coordinates remain blank. Do not collapse this into all-or-nothing row validity.

### 4. Non-directional/admin/excluded rows remain meaningful dispositions

`NOT_RELATION_EVIDENCE` is not equivalent to “missing data.”

### 5. Structural ownership must be explicit

A populated structural coordinate inherited from a stale or heuristic QSM is not automatically governed.

### 6. Cross-source semantic units and source-local block structure coexist

The integrated block authority explicitly supports source-local native subblocks rather than falsely inheriting grouping cross-wave by semantic similarity alone.

## What this does NOT automatically supersede

The breadth of the 99-column table is substantial, but **field presence is not proof of lossless supersession** of every older authority-production system.

In particular, this audit does not yet certify that FQRA losslessly replaces:

- full P3/P3A/P3C proposition-family revision/genealogy/promotion machinery;
- V550J executable joint-configuration authority;
- routing predicate compilation;
- response-option authority;
- respondent identity/join authority;
- V552J component-vector law;
- source-native topology/risk-set authority.

Those require explicit lineage proofs.

## Trii/Chetiri disposition

`PRIMARY_SHARED_RAWLSING_SEMANTIC_STRUCTURAL_AUTHORITY_INPUT`

Any replacement PRE553 DAG must either consume this authority/successor directly or prove field- and decision-level lossless succession. Statistical rediscovery from source evidence is not a lawful replacement for the adjudicated authority in this release.
