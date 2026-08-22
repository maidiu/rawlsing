# PREP71 R09 — FUTURE EXECUTION ORDER

Status: **PREPARATORY ONLY — DO NOT CERTIFY**

Assigned exact sources:

- `WVS Wave 1.sav` — `051bf450568f44181559a5b2bfbe58b4f05b58bc806643d0c63353c937ff0824`
- `WVS Wave 4.sav` — `c6757ed187655c8b9af88ae4c23c00f066696a641af2f316b4343272ea1d4a0a`

`WVS Wave 7` is outside this packet and must remain outside this court.

## Mandatory execution order

1. **Source SHA gate**
   - Refuse execution unless the exact source bytes match the SHA above.
   - Bind every replay assertion to exact source SHA + zero-based source row ordinal.

2. **Decoder/config gate**
   - Use the governed SAV path with source-declared/accepted UTF-8 handling.
   - Preserve raw numeric storage before formatted display, SPSS user-missing declarations/ranges, system-missing state, variable labels, value-label dictionaries, variable ordinal/name/type, display metadata, and reader/config provenance.
   - No source-specific compatibility override is authorized for W1 or W4.

3. **Hostile physical fixtures**
   - **W1 first:** execute `W1_S007_DISPLAY_STORAGE_SEPARATION`; assert raw `320120001` and the measured 9–10 digit range survive while `F2.0` remains separately retained display metadata. Any width-derived truncation/redefinition is fail-closed.
   - Execute the remaining W1 row-identity, typed-missing, all-system, ordered-slot, routing and weight-surface fixtures.
   - **W4 compound court:** execute both V3 identity fixtures, then the all-row typed-missing set, then `W4_PARTY_LOCAL_PARALLEL_VIEW`. Assert source row ordinal survives; all four all-row typed-missing columns survive; equal raw vectors do not merge variables or value-label dictionaries.
   - Execute W4 ordinary V218, ordered-slot, V2A and all-system fixtures.

4. **Metadata/topology fixtures**
   - Reconcile exact variable ordinals/names/types, missing declarations, display metadata, label dictionaries, ordered slots, source coordinates and weight/design candidate surfaces.
   - Presence of all-row missingness is never permission to delete a variable.

5. **Documentary semantic assertions**
   - Apply source-native questionnaire/codebook authority only to claims explicitly documented.
   - Where W4 questionnaire intent (“V3 … identifying each respondent in the given country”) conflicts with exact snapshot injectivity, raw physical evidence governs replay; retain the documentary intent as documentary evidence, not as a key constraint.
   - Keep every `AUTHORITY_GAPS.csv` row unresolved until its named later authority is supplied or a later governed adjudication explicitly permits preservation-as-unknown.

6. **Exact carrier/C11 equivalence assertions**
   - Prove the future carrier preserves exact raw value/state/metadata/dictionary/topology information required by frozen source-native law.
   - No semantic state may be inferred from a physical missing state merely because a label looks semantic.

7. **Negative / fail-closed fixtures**
   - Reject: W1 S007 truncation/format parsing; native-ID substitution for row ordinal; user/system missing collapse; all-row-column elision; vector-based variable deduplication; dictionary collapse; cross-wave numeric-code meaning transfer; default-weight selection without authority.

8. **Future disposition gate**
   - Only after all prior gates may a later authorized court choose a certification disposition.
   - This PREP71 packet itself does not certify either source.
