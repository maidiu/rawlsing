# Rawlsing V550J Semantic Authority Convergence Audit R3

## Status

R3 is a **source-integrity gate and scope correction** over the R2 convergence audit.

It does not install new production authority. It prevents the forthcoming typed semantic edge authority from inheriting a small set of now-proven source-native structure defects.

## Canonical scope correction

The sole governing scope source used here is `wave_authority_registry_35wave_v1.json`.

The authoritative 35-wave production scope is:

- **Afrobarometer:** R1, R5, R9
- **Arab Barometer:** I, II, V, VIII
- **Asian Barometer:** W1, W4, W5
- **EVS:** 1981, 1990, 1999, 2008, 2017
- **GSS:** 1972, 1973, 1984, 1993, 2002, 2010, 2016, 2024
- **Latinobarómetro:** 1995, 2011, 2024
- **LiTS:** 2006, II, III, IV
- **South Asia:** W1, W2
- **WVS:** W1, W4, W7

Asian Barometer W6 remains excluded.

This corrects an erroneous wave enumeration in the previous assistant-authored Codex instruction. In particular, prior references to Arab Barometer IV, EVS 2020, and Latinobarómetro 2005/2023 as production waves must be ignored. The current wave registry is authoritative.

## Retrieval package intake

The user-supplied retrieval package was consumed as evidence:

- filename: `Rawlsing_RETRIEVAL_PACKAGE_UNDER512MB.zip`
- SHA-256: `{retr_sha}`
- size: `{os.path.getsize(retr):,}` bytes

The package is sufficient to continue semantic-authority work. The retrieval README's inability to find standalone Latinobarómetro 2005/2023 native instruments is **not a production blocker**, because those waves are not in the governing 35-wave registry.

R3 does not embed the ~370 MB retrieval ZIP. Its exact hash is recorded in `input_references/INPUT_REFERENCE_MANIFEST_R3.csv`.

## R14/R15 candidate-integrity result

The prior 445-row semantic review queue was slightly overbroad and also contained a small number of source-native objects that fail direct primary-source checking.

R3 disposition counts:

- `SEMANTIC_REVIEW_READY`: **431**
- `DISCOVERY_ONLY_NONJOINT_SOURCE_OBJECT`: **3**
- `PROVEN_MISBOUNDED_SOURCE_STRUCTURE`: **3**
- `SEMANTIC_REVIEW_READY_ROUTING_BLOCKED`: **3**
- `PROVEN_UNSUPPORTED_BY_CITED_NATIVE_INSTRUMENT`: **2**
- `PROVEN_UNSUPPORTED_AND_SEMANTICALLY_MISBOUNDED`: **1**
- `HOLD_REDUNDANT_CROSS_PARENT_UNION`: **1**
- `HOLD_LEGACY_OBJECT_NORMALIZATION`: **1**

Therefore:

- **431** objects are currently ready for typed semantic adjudication under the R3 source-integrity gate.
- **3** additional South Asia objects are semantically reviewable but remain runtime fail-closed because R14 explicitly retains localized blockers.
- **6** objects are now source-proven misbounded/unsupported and must not enter semantic authority as currently represented.
- **1** ASB W4 union is source-real at the member level but lacks a demonstrated single native parent and duplicates two existing exact parent structures; hold/demote it.
- **3** rows are explicitly `STANDALONE_SUBSTANTIVE`; they are discovery material, not governing source-native joint authority.
- **1** GSS abortion battery has strong native evidence but is a malformed legacy object without normalized R14 schema/state; normalize it before compilation.

This means **434 objects remain semantically reviewable now**, but only **431 are currently semantically reviewable without an explicit runtime blocker**.

## Proven Asian Barometer W4 defects

Primary-source checking against the recovered ABS4 core questionnaire proves the following defects:

1. `ASB-R14-W4-AGREEMENT_Q129_Q132`
   - Q129 is standalone.
   - Q130-Q133 are the actual shared alternatives battery.
   - Existing `ASB-R14-W4-DEMOCRATIC_ALTERNATIVES_Q130_Q133` is the source-correct object.

2. `ASB-R14-W4-CITIZEN_EMPOWERMENT_Q133_Q137`
   - Q133 belongs the prior Q130-Q133 battery.
   - Citizen empowerment/political support is Q134-Q138.
   - Existing `ASB-R14-W4-CITIZEN_EMPOWERMENT_Q134_Q138` is source-correct.

3. `ASB-R14-W4-AUTHORITARIAN_DEMOCRATIC_VALUES_Q146_Q155`
   - The native authoritarian/democratic-values battery is Q139-Q149.
   - Q150 starts Globalization.
   - Q155 starts Redistribution.
   - Existing `ASB-R14-W4-AUTHORITARIAN_DEMOCRATIC_VALUES_Q139_Q149` is source-correct.

4. `ASB-R14-W4-COVID_IMPACTS_Q139A_Q139D`
   - The cited core instrument contains no q139a-d COVID grid.
   - Q139 is a single authoritarian/democratic-values item.
   - All four claimed implementation members are absent from the current deep P2 catalog.
   - Withdraw unless an alternate country/module instrument with exact provenance is recovered.

5. `ASB-R14-W4-COVID_JUSTIFIABILITY_Q143A_Q143E`
   - The cited core instrument contains no q143a-e COVID grid.
   - Q143 is a single speech-control attitude item.
   - All five claimed implementation members are absent from the current deep P2 catalog.
   - Withdraw unless exact alternate-module provenance is recovered.

6. `ASB-R14-W4-GLOBALIZATION_PAIRED_Q156_Q157`
   - Q156 is government responsibility to reduce income differences.
   - Q157 is concern over household income loss.
   - Both are in Redistribution, not a globalization paired-followup structure.
   - q156a/q157a are absent from the cited native core/current P2 catalog.

A seventh object, `ASB-R14-W4-POLITICAL_PARTICIPATION_Q69A_Q77A`, is not a phantom: its implementation members map to real printed Q69-Q77 content. But the questionnaire has **two distinct parent stems** (Q69-Q73 and Q74-Q77), both already represented by exact R14 objects. R3 therefore holds the union as redundant/cross-parent rather than calling it source-native joint authority.

## Queue construction correction

Three multi-member R14 records included in the old 445-row queue are themselves classified `STANDALONE_SUBSTANTIVE`:

- `ASB-R14-W1-Q018-Q0181-SEPARATE`
- `ASB-R14-W4-Q1-Q5`
- `SouthAsia-R14-W2-Q31_Q32` / current object-id spelling in the ledger

The fact that a source object serializes multiple columns/rows does not make it J-family authority. R3 removes such rows from the governing joint denominator while preserving them as discovery candidates where a later typed semantic relation might independently justify joint use.

`ASB-R14-W4-Q1-Q5` also demonstrates why this matters: native section A is Q1-Q6, with country present/past/future Q1-Q3 and family present/past/future Q4-Q6. The five-member object should not silently become a joint family merely because it has five members.

## P2 comparison remains a diagnostic, not a veto

R14-to-P2 structure support across the old queue is:

- `EXACT_P2_STRUCTURE_MATCH`: 227
- `R14_SUBSET_OF_P2_STRUCTURE`: 81
- `NO_P2_STRUCTURE_SUPPORT`: 80
- `P2_STRUCTURE_SUBSET_OF_R14`: 43
- `PARTIAL_OVERLAP`: 14

A P2 mismatch is **not** itself evidence that R14 is wrong. R14 is later and in many cases has stronger native-questionnaire grounding.

Conversely, exact P2 support does not create V550J authority.

The comparison is retained as a provenance/triage signal only.

A useful control case is `WVS-R14-W4-V68-V77`: one member (V77) failed the current P2 deep-node match, but the native WVS instrument explicitly prints V68-V77 as one unwanted-neighbour battery. R3 therefore treats that as a P2/catalog coverage gap rather than a source-structure defect.

## Consequence for the semantic-authority build

The semantic adjudication should proceed from `SEMANTIC_EDGE_ADJUDICATION_QUEUE_R3_SOURCE_INTEGRITY_GATED.csv`, not the R1 445-row queue without source-integrity gating.

No R14/P2/P3 historical artifact should be edited in place.

The six proven ASB defects require a **versioned source-native correction successor/overlay** before production compilation.

The semantic authority may continue in parallel for the 431 clean-ready structures and the 3 routing-blocked structures, because their semantic meaning can be adjudicated separately from runtime composability.

## Important limit of R3

R3 has performed direct primary-source verification for the proven ABS4 defects and structural/provenance diagnostics across all 445 queue rows. It has **not** manually reopened every cited native questionnaire page for every one of the 445 structures.

Therefore `SEMANTIC_REVIEW_READY` means:

> no source-structure defect has been demonstrated by the current integrity checks; proceed source-first in semantic adjudication.

It does not mean:

> every R14 locator has been independently recertified by R3.

That stronger recertification should be driven by semantic-edge adjudication and by anomaly signals, rather than blindly rereading every questionnaire.

## Next semantic step

Proceed with typed semantic adjudication over the gated queue. For each structure:

1. verify source-native membership when the edge depends on exact battery boundaries;
2. determine whether joint observation preserves information unavailable from isolated V551 atoms;
3. assign a primitive semantic relation only if justified;
4. assign ordered member roles;
5. retain respondent composability/routing as a separate authority dimension;
6. reject wrong-ownership structures even where the source battery itself is valid;
7. preserve source-negative and unresolved evidence explicitly.

