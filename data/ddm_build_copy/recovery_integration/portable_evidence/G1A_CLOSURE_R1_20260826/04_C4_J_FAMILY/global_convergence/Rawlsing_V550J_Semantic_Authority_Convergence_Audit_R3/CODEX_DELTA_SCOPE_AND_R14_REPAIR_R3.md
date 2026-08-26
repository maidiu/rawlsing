# CODEX DELTA INSTRUCTION R3 — Scope Correction + R14 Source-Integrity Repair

This instruction **supersedes only the conflicting parts** of the earlier assistant-authored Codex goal instruction. Everything else in the prior work order remains in force unless contradicted here.

## 1. Correct the production-wave enumeration immediately

Do not use the earlier prose wave list as authority.

Use the current `wave_authority_registry_35wave_v1.json` as the sole production-scope authority.

Canonical scope:

- Afrobarometer: R1, R5, R9
- Arab Barometer: I, II, V, VIII
- Asian Barometer: W1, W4, W5
- EVS: 1981, 1990, 1999, 2008, 2017
- GSS: 1972, 1973, 1984, 1993, 2002, 2010, 2016, 2024
- Latinobarómetro: 1995, 2011, 2024
- LiTS: 2006, II, III, IV
- South Asia: W1, W2
- WVS: W1, W4, W7

Asian Barometer W6 is excluded.

In particular, disregard the prior assistant instruction that named Arab Barometer IV, EVS 2020, or Latinobarómetro 2005/2023 as production waves. That enumeration was erroneous.

Do not alter production scope to match that old prose instruction.

## 2. Retrieval consequence

The retrieval README reports that standalone Latinobarómetro 2005/2023 native questionnaires were not found.

That is **not a production closure blocker**, because 2005/2023 are not canonical production waves.

Do not spend additional time recovering those waves for this V550J program unless a separate historical/archive task explicitly asks for them.

If native-source recovery is required for Latinobarómetro production authority, target the actual canonical waves: 1995, 2011, 2024.

Likewise target the canonical Arab Barometer and EVS waves from the registry, not the erroneous old list.

## 3. Add a versioned R14/R15 source-integrity successor task

The external semantic audit has now directly verified source defects in several accepted Asian Barometer W4 R14 objects using the native ABS4 core questionnaire recovered in the retrieval package.

Do **not** edit the historical R14 release in place.

Create a versioned successor/overlay that terminally disposes the following objects:

### Withdraw / supersede as misbounded

`ASB-R14-W4-AGREEMENT_Q129_Q132`
- Q129 is standalone.
- Q130-Q133 are the actual native shared battery.
- Supersede joint use with existing `ASB-R14-W4-DEMOCRATIC_ALTERNATIVES_Q130_Q133`.

`ASB-R14-W4-CITIZEN_EMPOWERMENT_Q133_Q137`
- Q133 belongs Q130-Q133.
- Native citizen empowerment battery is Q134-Q138.
- Supersede with existing `ASB-R14-W4-CITIZEN_EMPOWERMENT_Q134_Q138`.

`ASB-R14-W4-AUTHORITARIAN_DEMOCRATIC_VALUES_Q146_Q155`
- Native battery is Q139-Q149.
- Q150 begins Globalization.
- Q155 begins Redistribution.
- Supersede the claimed battery with existing `ASB-R14-W4-AUTHORITARIAN_DEMOCRATIC_VALUES_Q139_Q149`; do not treat Q150-Q155 as part of that battery.

### Withdraw unless alternate native module provenance is demonstrated

`ASB-R14-W4-COVID_IMPACTS_Q139A_Q139D`
- No q139a-q139d COVID grid exists in the cited ABS4 core instrument.
- Current deep implementation catalog resolves none of the claimed members.

`ASB-R14-W4-COVID_JUSTIFIABILITY_Q143A_Q143E`
- No q143a-q143e COVID grid exists in the cited ABS4 core instrument.
- Current deep implementation catalog resolves none of the claimed members.

If an actual country/module-specific source instrument contains these IDs, it must be recovered with exact file hash, locator, wording, routing and implementation crosswalk before any successor may restore the structure.

### Withdraw current relation claim

`ASB-R14-W4-GLOBALIZATION_PAIRED_Q156_Q157`
- Native Q156 = government responsibility to reduce income differences.
- Native Q157 = concern about loss of household major income source.
- Both occur in Redistribution.
- q156a/q157a are absent from the cited core instrument/current deep catalog.
- Preserve real q156 and q157 as independent questions unless a separately governed semantic relation is later authorized.

## 4. Hold/demote redundant W4 union

`ASB-R14-W4-POLITICAL_PARTICIPATION_Q69A_Q77A`

Do not classify the member IDs as phantom: the deep implementation catalog maps them to the real printed Q69-Q77 content.

However, the native questionnaire contains two separate parent stems:

- Q69-Q73
- Q74-Q77

and exact R14 objects for both already exist.

Therefore demote the Q69a-Q77a union from governing source-native joint membership unless a stronger source-native common-parent authority exists.

A later semantic edge may relate the two batteries, but that is not the same thing as pretending the source printed one battery.

## 5. Correct the semantic queue denominator rule

Do not treat every R14 object with `member_count > 1` as source-native J-family authority.

At minimum, objects whose R14 state is `STANDALONE_SUBSTANTIVE` must remain discovery-only unless separately promoted by semantic relation authority.

Current examples in the old 445 queue:

- `ASB-R14-W1-Q018-Q0181-SEPARATE`
- `ASB-R14-W4-Q1-Q5`
- `SouthAsia-R14-W2-Q31-Q32`

For `ASB-R14-W4-Q1-Q5`, native section A is Q1-Q6. If a source-section object is needed, reconstruct the exact Q1-Q6 source parent in a successor. Do not make the existing Q1-Q5 object joint authority.

## 6. Normalize, do not discard, the legacy GSS object

`SOURCE-NATIVE-UNNAMED-272` contains strong native 1984 GSS abortion-battery evidence but lacks normal R14 schema/state/member serialization.

Normalize/crosswalk it through a versioned successor using the cited source and current GSS P3/P3C authority.

Do not infer new semantics and do not delete the evidence.

## 7. Preserve the WVS control case

`WVS-R14-W4-V68-V77` has one member (V77) not matched by the current P2 deep-node enrichment.

Do not interpret that as a source defect.

The native WVS instrument explicitly prints V68-V77 as the unwanted-neighbour battery. Treat this as an implementation-catalog/crosswalk coverage issue if V77 is needed downstream.

## 8. Required outputs

Produce:

- versioned R14/R15 correction overlay/successor;
- supersession ledger for all affected objects;
- before/after source-native joint candidate counts;
- exact source locators/hashes used;
- validator proving historical release unchanged;
- validator proving withdrawn objects cannot enter new joint compilation;
- validator proving replacement objects retain exact native membership;
- updated source-native candidate export;
- updated routing/applicability references where affected;
- exact git diff/status and test results.

Do not yet assign principle/application, goal/means, norm/conduct, reciprocity or other semantic edge types. That remains with the external semantic-authority process.
