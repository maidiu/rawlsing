# HQ120-D — current legacy compatibility gaps

## Holding

`rawlsing_next/pre553_legacy_compat.py` is correctly narrow.

It is a **fail-closed migration/parity adapter**, not a successor semantic stage and not a license to re-run or revive V550-V552 serial architecture.

Its own module law says retained *meaning* may migrate only after the caller supplies a canonical semantic projection and an exact parity receipt under a named pinned authority. Artifact shape, filenames, ancestry, field-name coincidence, numeric coincidence, or provenance reachability do not create parity.

## Exact current enabled mappings

At base `1dd7d3be87940cd3830f9b7f269b99e3ff5cb0cd`, the compatibility registry enables only bounded exact mappings with named authority:

| Mapping | Legacy family | Current target semantic kind | Disposition |
|---|---|---|---|
| `V550_RESPONSE_SEMANTICS_EXACT` | V550 | `PRE553_RESPONSE_SEMANTIC_PROJECTION` | enabled under pinned V550/V551 response-semantics authority |
| `V551_METRIC_SOURCE_STATE_EXACT` | V551 | `PRE553_METRIC_SOURCE_STATE_PROJECTION` | enabled under the same exact pinned authority |
| `R1_ATP_W135_SHARED_RESPONDENT_RELATION_EXACT` | R1 | `PRE553_SHARED_RESPONDENT_RELATION_PROJECTION` | enabled only for the exact pinned R1 authority/study/source |

Those are compatibility bridges into current meaning. They do not establish that the old runtime remains current.

## Deliberately disabled blanket mappings

The module explicitly disables:

| Mapping | Reason |
|---|---|
| `V550J_OBJECT_PARITY` | P04 does not name object-specific J-neutrality authority |
| `V551J_OBJECT_PARITY` | P04 does not name object-specific J-neutrality authority |
| `V552_OBJECT_PARITY` | no blanket V552 carrier-equivalence authority |
| `V552J_OBJECT_PARITY` | no J/V552J blanket carrier-equivalence authority |

This is **not** evidence that the current DAG lacks homes for the information.

It means a historical artifact cannot be declared equivalent wholesale.

## Current-native homes for information that blanket parity cannot import

Historical information should be decomposed into its actual current semantic owner:

- source-native response/question meaning -> `GovernedC11Projection`, `QuestionVariableBinding`, response/coordinate/weight rules;
- source/wave/universe identity -> `EmpiricalUniverse`;
- same-respondent identity -> `RespondentIdentity` + exact predicate/join semantics;
- cross-universe linkage/composition -> `SourceUniverseRelation` / P07;
- joint target topology/order/domain -> I03 `EmpiricalQuerySpec.target_arity_and_topology`;
- per-component role/order/multiplicity and authority vector -> `ComponentAuthorityVectorReceipt`;
- scalar projection -> only the current component-vector scalarization rule;
- discovered candidates/frontiers/branch ancestry -> `DiscoveryAuthority`, `DiscoveryResultReceipt`, `DiscoveryBranchReplayBinding`;
- learned validation -> M1 exact family-rule adjudication;
- immutable product release -> M2;
- learned-product currentness/invalidation -> B5;
- actor-independent structural relation -> Field Forge family-specific producer/refusal;
- downstream structural use -> exact PRE-V3 consumer-specific admission/permission;
- replay/provenance -> current replay/determinant/dependency closures.

This is the correct anti-amputation route: preserve semantic function while refusing obsolete stage identity.

## Compatibility gaps that remain real

### 1. J-family object parity

No blanket V550J/V551J parity authority is current.

If a historical J object must itself be reused as a carrier, it needs an object-specific exact semantic projection and authority proving parity.

Otherwise reconstruct/preserve its constitutive information in current native objects.

### 2. V552/V552J object parity

No blanket V552/V552J equivalence is current.

A historical structural-pressure/status object cannot become a current structural relation or learned product merely because its fields look familiar.

Any retained meaning must land in the competent current owner with the competent current authority ceiling.

### 3. Scalar packet shortcuts

Historical scalar values cannot bypass the current component-vector law.

If the old value represented a multi-component authority dimension, current migration must preserve the vector unless exact complete/nonempty/unanimous scalarization authority is proved.

### 4. Provenance is not semantic equivalence

The current adapter correctly rejects the idea that shared lineage or an ancestor hash proves semantic parity.

Likewise, P07 treats provenance/harmonization relation kinds as nonauthorizing for equivalence/linkage/composition.

### 5. Retired runtime fallback

The compatibility adapter explicitly rejects:
- retired-runtime fallback;
- V558-current-runtime-context fallback;
- profile/persona shortcuts;
- ambiguous carrier identity.

Those rejections are part of current correctness, not missing functionality.

## Relationship to I4

I4 should consume **current producer-owned objects**, not legacy artifacts merely blessed by filename/stage ancestry.

If an exact legacy parity receipt lawfully yields a current semantic projection, the resulting current exact ref may enter the normal producer/dependency/determinant closure.

I4 does not need:
- legacy family fields;
- V550/V551/V552 stage fields;
- J/non-J switches;
- legacy scalarization switches.

Adding those would reintroduce serial-architecture coupling that the current producer-owned DAG intentionally removed.

## Final classification

`CURRENT_LEGACY_COMPAT = NARROW_EXACT_MIGRATION_BRIDGE`

`DISABLED_BLANKET_PARITY != CURRENT_DAG_OWNER_GAP`

`MIGRATE_MEANING_TO_CURRENT_OWNER__DO_NOT_MIGRATE_RETIRED_STAGE_IDENTITY`
