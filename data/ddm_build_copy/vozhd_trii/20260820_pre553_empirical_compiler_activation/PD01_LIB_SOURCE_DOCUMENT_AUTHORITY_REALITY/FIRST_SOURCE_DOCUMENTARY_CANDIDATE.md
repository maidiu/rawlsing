# FIRST_SOURCE_DOCUMENTARY_CANDIDATE

## Disposition

`FIRST_SOURCE_DOCUMENTARY_CANDIDATE: WORLD_VALUES_SURVEY__WAVE_7__V6_0_0`

`PENDING_POPULATED_POSTGRES_CONFIRMATION`

This is **not** P05 certification.

## Why WVS W7 wins the documentary first-source court

1. **Exact release identity is unusually strong in the surfaced materials.** The W7 codebook identifies data file version `6-0-0`, dated `2022-05-31`, with DOI `10.14281/18241.24`. Classification: `SOURCE_NATIVE_DOCUMENTED`. Evidence: Library: WVS Wave 7 (2017) Codebook.pdf, p.2 (VERSION 6-0-0, 2022-05-31; DOI 10.14281/18241.24; A_STUDY).
2. **Respondent identity is source-native rather than inferred.** `D_INTERVIEW` is a 9-digit composite containing country, wave and original interview code. Classification: `SOURCE_NATIVE_DOCUMENTED`. Evidence: Library: WVS Wave 7 (2017) Codebook.pdf, p.73 (D_INTERVIEW composite 9-digit interview identity: country + wave + original interview code).
3. **It directly tests typed absence and routing discipline.** The master instrument distinguishes DK, refusal/no answer, filter-based N/A and other missing/N/A; codebook rows additionally use not-asked and question-specific states. Q155 distinguishes “no second answer” from “N/A/no first answer.” Classification: `SOURCE_NATIVE_DOCUMENTED`. Evidence: Library: WVS Wave 7 (2017) Questionnaire.pdf, p.1 (global special codes); pp.11-12 (ranked first/second-choice batteries); Library: WVS Wave 7 (2017) Codebook.pdf, p.51 (Q154/Q155 special states including DK, no answer, not asked, no second answer/no first answer).
4. **It directly tests ordered topology.** Q152/Q153, Q154/Q155 and Q156/Q157 are linked first/second-choice slots. Flattening them into an unordered set is semantic loss. Classification: `SOURCE_NATIVE_DOCUMENTED`. Evidence: Library: WVS Wave 7 (2017) Questionnaire.pdf, p.1 (global special codes); pp.11-12 (ranked first/second-choice batteries).
5. **It has enough battery richness to exercise the D12 frontier.** R14 identifies large grouped W7 families including Q177-Q195, Q64-Q89, Q94-Q105, Q18-Q26 and others; these support real same-respondent joint/cotravel/k-way stress once physical incidence is confirmed. Classification: `LIBRARY_AUTHORITY_SUPPORTED` for the Rawlsing candidate grouping, not populated proof. Evidence: Library: R14_SOURCE_NATIVE_CANDIDATE_INTEGRITY_AUDIT_R3.csv, WVS W7 grouped source-native candidate rows and questionnaire locators; status SEMANTIC_REVIEW_READY where reported; D12 capability requirement Library: Pasted text(20260819-162348).txt, D12/D13/C11 sections; M01-M18 and source-retention law.
6. **It contains nontrivial source plurality inside one release.** Q223 has country-specific category systems and substantive non-vote/no-right/blank-ballot states distinct from nonresponse. This forces C11 to preserve source-local semantics instead of inventing false global equivalence. Classification: `SOURCE_NATIVE_DOCUMENTED`. Evidence: Library: WVS Wave 7 (2017) Codebook.pdf, Q223 codebook row (country-specific party coding; distinct nonresponse/not-applicable states).
7. **Weights are purpose-labeled, not merely numeric.** W_WEIGHT and S018 have different source-documented purposes, and the codebook specifies when their product is appropriate. This is exactly the distinction between “field exists” and “authorized measure basis.” Classification: `SOURCE_NATIVE_DOCUMENTED`. Evidence: Library: WVS Wave 7 (2017) Codebook.pdf, pp.8-9 (W_WEIGHT purpose; S018 equilibrated country weight; product guidance).
8. **Design structure is present but incomplete enough to expose the authority boundary.** I_PSU exists and has typed not-asked/missing states, but the surfaced materials do not establish a full country-specific variance/strata methodology. That makes W7 useful: it forces the compiler to distinguish representable fields from authorized estimands. Evidence: Library: WVS Wave 7 (2017) Codebook.pdf, p.77 (I_PSU Primary Sampling Unit; -4 not asked; -5 missing).

## Why it is not yet documentarily ready for P05

Current readiness: `BLOCKED_AUTHORITY_GAP`.

The blockers are not source triviality; they are exactly the semantic governance seams P05 exists to police:

- complete per-question/per-country routing and risk-set authority is not yet surfaced;
- country-specific target-population/sample-design/variance authority is incomplete;
- exact currently ingested raw W7 artifact checksum/manifest is not established;
- exact D_INTERVIEW→Rawlsing respondent-id linkage is not proven;
- exact source code/value/state/topology→C11 canonical transformation authority is not frozen;
- no populated source→C11 replay/equivalence receipt exists.

D13 explicitly says no current populated source→C11 equivalence has been proven and requires retaining source/native evidence until positive certification. Evidence: Library: Pasted text(20260819-162348).txt, D12/D13/C11 sections; M01-M18 and source-retention law.

## Governing noncollapse

WVS respondent demographics and responses are empirical coordinates/evidence. They are **not** generated structural positions, personas, or actor beliefs. The future reverse product is an uncertainty-bearing positioned-subject empirical possibility field that must later be metabolized through V3; it cannot be short-circuited into actor psyche. Evidence: Library: Pasted text(20260819-162348).txt, D12/D13/C11 sections; M01-M18 and source-retention law and current inert I01 carrier GitHub: rawlsing_next/pre553_empirical_objects.py @ 9188dc9fb7a8b92b981f3d3f94754cd6137d17b1.
