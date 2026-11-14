# 02 SHARED SUBSTRATE — F5 original-first mechanism analysis

Source identity: historical `25830fe7462bb9e29bc4087e6ae14f3f84cec377` blob `9ac6feb919f45bcd33e6976dcde9dda4c8617895`; protected `6a5c12f04323d74001f9632063ec907f4fc4468e` blob `37cd35fa2e3420a3eea272a2902e96ab9ba38aba`. Historical ID or owner: `V550J respondent-microdata`. Case `R6:C:02_SHARED_SUBSTRATE` is a seam comparison only; **0 canonical historical T identities created**.

## Historical computation
[Historical function `resolve_shared_substrate_requirements L249;canonicalize_shared_respondent_substrate L332;validate_shared_respondent_substrate L517`](https://github.com/maidiu/rawlsing/blob/25830fe7462bb9e29bc4087e6ae14f3f84cec377/data/ddm_build_copy/ddm_v550_shared_respondent_substrate.py) — `data/ddm_build_copy/ddm_v550_shared_respondent_substrate.py`.

**Inputs/denominator/source grain:** V550 base plus V550J joint-only question requirements and respondent-variable normalized response rows

**Transformation (what actually happens):** Union base/joint vars; normalize respondent and response keys; content hash; reject duplicate scalar keys

**Output and learned information:** Shared long respondent×variable substrate, source/wave/country exact

**Negative/admission rules:** Wrong source/wave, absent normalized IDs, duplicate scalar response, changed hash fail

**First selected or statically identified reader:** Prepared-substrate producer imports; V550J runner uses

## Present operation
[Current function `_validate_universe_and_respondent_scope L578`](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/rawlsing_next/pre553_c11_ingest.py) — `rawlsing_next/pre553_c11_ingest.py`.

**Inputs/authority:** EmpiricalUniverse/RespondentIdentity/RespondentEvent sections

**Transformation:** Conserve respondent uniqueness inside one exact universe and disallow cross-universe reuse

**Output:** Accepted C11 typed respondent release if all checks pass

**Negative/refusal:** Duplicate respondent/universe or invalid event namespace denied

**First bounded reader:** C11 release for I03, no old substrate native mapping witnessed

## Differential verdict
**Unproved edge:** Modern retains respondent records; unproved old shared-substrate identity and response semantics migration

**Decisive counterfactual/negative test:** Differential same-source respondent/variable row replay and negative duplicate-key mutation

**Evidence grade:** S1 code-body and static read. No execution witness, no actual same-source source-to-N9-to-Sorok science, no parity certification. These interfaces have different source grains and cannot be called superseded without selected source-reader mechanism verification.
