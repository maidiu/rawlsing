# SQL_PROBE_AUGMENTATIONS

## Baseline review status

`PD01_POPULATED_PROBES.sql` (or another PD01-named equivalent) was **not located in the recursive repository tree at exact head `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`**. Therefore this file does not claim to amend a reviewed baseline. It records only source-native additions/corrections that any physical probe battery must include. Evidence: GitHub repository tree maidiu/rawlsing @ 9188dc9fb7a8b92b981f3d3f94754cd6137d17b1. Court rule: Library: Pasted text(20260820-183309).txt, lines 1-490 (especially 37-58, 143-171, 173-426, 442-490).

No SQL below was executed by this court.

### A1 — Prove WVS W7 respondent-table linkage before using surrogate ids

```sql
SELECT
  COUNT(*) AS demo_w7_rows,
  COUNT(s.id) AS linked_microdata_respondents,
  COUNT(*) - COUNT(s.id) AS orphan_demo_ids
FROM public."respondentsDemoWVSW7" d
LEFT JOIN public.survey_microdata_respondents s
  ON s.id = d.respondent_id;

SELECT s.source, s.wave, s.dataset_id, s.source_file, s.country_code,
       MIN(s.survey_year) AS min_year, MAX(s.survey_year) AS max_year,
       COUNT(*) AS respondents
FROM public.survey_microdata_respondents s
JOIN public."respondentsDemoWVSW7" d ON d.respondent_id = s.id
GROUP BY 1,2,3,4,5
ORDER BY 1,2,3,4,5;
```

Required because W7 source identity is not the Rawlsing surrogate id: `D_INTERVIEW` has source-native composite semantics. Evidence: Library: WVS Wave 7 (2017) Codebook.pdf, p.73 (D_INTERVIEW composite 9-digit interview identity: country + wave + original interview code); schema Conversation upload: Rawlsing_WVS_public_schema(1).sql:L6450-L6459.

### A2 — Probe source-native identity/design/weight variables as raw incidence

```sql
SELECT r.var_code,
       COUNT(*) AS rows,
       COUNT(r.value_raw) AS numeric_rows,
       COUNT(r.value_text) AS text_rows,
       COUNT(DISTINCT r.respondent_id) AS respondents
FROM public.survey_microdata_responses r
JOIN public."respondentsDemoWVSW7" d ON d.respondent_id = r.respondent_id
WHERE r.var_code IN ('D_INTERVIEW','A_WAVE','B_COUNTRY','I_PSU','W_WEIGHT','S018')
GROUP BY r.var_code
ORDER BY r.var_code;
```

Zero rows are evidence of non-retention only after exact var-code aliases are checked in the canonical/alias authority tables; do not infer absence from one spelling.

### A3 — Typed absence occupancy must remain distinct

```sql
SELECT r.var_code,
       COUNT(*) FILTER (WHERE r.value_raw = -1) AS code_minus_1,
       COUNT(*) FILTER (WHERE r.value_raw = -2) AS code_minus_2,
       COUNT(*) FILTER (WHERE r.value_raw = -3) AS code_minus_3,
       COUNT(*) FILTER (WHERE r.value_raw = -4) AS code_minus_4,
       COUNT(*) FILTER (WHERE r.value_raw = -5) AS code_minus_5,
       COUNT(*) FILTER (WHERE r.value_raw IS NULL AND r.value_text IS NULL) AS null_rows,
       COUNT(*) AS total_rows
FROM public.survey_microdata_responses r
JOIN public."respondentsDemoWVSW7" d ON d.respondent_id = r.respondent_id
GROUP BY r.var_code
ORDER BY r.var_code;
```

Compare each variable to its exact codebook semantics; numeric equality alone does **not** license a global meaning for a negative code. W7 global/source examples: Library: WVS Wave 7 (2017) Questionnaire.pdf, p.1 (global special codes); pp.11-12 (ranked first/second-choice batteries); Q155: Library: WVS Wave 7 (2017) Codebook.pdf, p.51 (Q154/Q155 special states including DK, no answer, not asked, no second answer/no first answer).

### A4 — Rank-slot retention and first/second-answer risk set

```sql
WITH x AS (
  SELECT r.respondent_id,
         MAX(r.value_raw) FILTER (WHERE r.var_code='Q154') AS q154,
         MAX(r.value_raw) FILTER (WHERE r.var_code='Q155') AS q155
  FROM public.survey_microdata_responses r
  JOIN public."respondentsDemoWVSW7" d ON d.respondent_id=r.respondent_id
  WHERE r.var_code IN ('Q154','Q155')
  GROUP BY r.respondent_id
)
SELECT q154, q155, COUNT(*) AS n
FROM x
GROUP BY q154, q155
ORDER BY q154, q155;
```

Run analogous pairs for Q152/Q153 and Q156/Q157. The receipt must preserve source-specific “no second answer” versus “no first answer” semantics, not merely row presence. Evidence: Library: WVS Wave 7 (2017) Questionnaire.pdf, p.1 (global special codes); pp.11-12 (ranked first/second-choice batteries); Library: WVS Wave 7 (2017) Codebook.pdf, p.51 (Q154/Q155 special states including DK, no answer, not asked, no second answer/no first answer).

### A5 — Scalar primary-key topology warning

```sql
SELECT conname, pg_get_constraintdef(oid)
FROM pg_constraint
WHERE conrelid = 'public.survey_microdata_responses'::regclass
  AND contype = 'p';
```

Expected schema contract is `PRIMARY KEY (respondent_id, var_code)`. This proves only the representation constraint, not source parity. For every source topology that can produce multiple same-var events, demand either separate native var codes with explicit topology authority or a C11 event-identity carrier. Schema: Conversation upload: Rawlsing_WVS_public_schema(1).sql:L7377-L7382. D13 burden: Library: Pasted text(20260819-153505).txt, hostile burden section: required replay inputs, scalar duplicate-key/event/routing deficits.

### A6 — Q223 country-specific code preservation

```sql
SELECT d.country_code, r.value_raw, r.value_text, COUNT(*) AS n
FROM public.survey_microdata_responses r
JOIN public."respondentsDemoWVSW7" d ON d.respondent_id=r.respondent_id
WHERE r.var_code='Q223'
GROUP BY d.country_code, r.value_raw, r.value_text
ORDER BY d.country_code, r.value_raw, r.value_text;
```

Interpret only against the country-specific codebook list. Do not globally merge substantive no-right/would-not-vote/blank-ballot states with nonresponse. Evidence: Library: WVS Wave 7 (2017) Codebook.pdf, Q223 codebook row (country-specific party coding; distinct nonresponse/not-applicable states).

### A7 — Weight-name separation and source-var provenance

```sql
SELECT w.weight_name, w.weight_type, w.source_var, w.source, w.wave,
       w.is_primary, COUNT(*) AS rows,
       COUNT(w.weight_value) AS valued_rows,
       MIN(w.weight_value) AS min_weight,
       MAX(w.weight_value) AS max_weight
FROM public.survey_weight_fact w
JOIN public."respondentsDemoWVSW7" d ON d.respondent_id=w.respondent_id
GROUP BY 1,2,3,4,5,6
ORDER BY 1,2,3,4,5,6;
```

The receipt must show whether W_WEIGHT and S018 are distinct. `is_primary=true` must not be treated as source authority for all estimands. Source purposes: Library: WVS Wave 7 (2017) Codebook.pdf, pp.8-9 (W_WEIGHT purpose; S018 equilibrated country weight; product guidance).

### A8 — PSU occupancy and typed design absence

```sql
SELECT r.value_raw, r.value_text, COUNT(*) AS n
FROM public.survey_microdata_responses r
JOIN public."respondentsDemoWVSW7" d ON d.respondent_id=r.respondent_id
WHERE r.var_code='I_PSU'
GROUP BY r.value_raw, r.value_text
ORDER BY r.value_raw, r.value_text;
```

Specifically retain `-4 not asked` and `-5 missing`. Do not claim strata/variance design from PSU alone. Evidence: Library: WVS Wave 7 (2017) Codebook.pdf, p.77 (I_PSU Primary Sampling Unit; -4 not asked; -5 missing).

### A9 — Raw→canonical mapping/provenance occupancy

```sql
SELECT raw_source, raw_wave, canonical_source, canonical_wave,
       identity_match_type, COUNT(*) AS mappings,
       COUNT(*) FILTER (WHERE authority_source_path IS NULL) AS missing_authority_path,
       COUNT(*) FILTER (WHERE authority_row_identity IS NULL) AS missing_authority_row
FROM rawlsing_authority_reconcile_ar_20260719t213835z.question_structural_mapping_provenance
GROUP BY 1,2,3,4,5
ORDER BY 1,2,3,4,5;

SELECT canonical_source, canonical_wave, response_topology,
       directional_certification_status, authority_semantic_role,
       COUNT(*) AS questions
FROM rawlsing_authority_reconcile_ar_20260719t213835z.canonical_question_registry
GROUP BY 1,2,3,4,5
ORDER BY 1,2,3,4,5;
```

Schema only: Conversation upload: Rawlsing_WVS_authority_reconcile_schema(1).sql:L36-L53,L84-L95. Any NULL authority path/row must be adjudicated before P05 source-equivalence certification.

### A10 — Same-respondent k-way stress surface

```sql
WITH w7 AS (
  SELECT r.respondent_id, r.var_code, r.value_raw, r.value_text
  FROM public.survey_microdata_responses r
  JOIN public."respondentsDemoWVSW7" d ON d.respondent_id=r.respondent_id
  WHERE r.var_code IN ('Q177','Q178','Q179','Q180','Q181')
), p AS (
  SELECT respondent_id,
         MAX(value_raw) FILTER (WHERE var_code='Q177') AS q177,
         MAX(value_raw) FILTER (WHERE var_code='Q178') AS q178,
         MAX(value_raw) FILTER (WHERE var_code='Q179') AS q179,
         MAX(value_raw) FILTER (WHERE var_code='Q180') AS q180,
         MAX(value_raw) FILTER (WHERE var_code='Q181') AS q181
  FROM w7 GROUP BY respondent_id
)
SELECT q177,q178,q179,q180,q181,COUNT(*) AS n
FROM p
GROUP BY 1,2,3,4,5
ORDER BY n DESC,1,2,3,4,5;
```

This is a reconstructibility stress, not a structural interpretation. R14 identifies Q177-Q195 as a source-native grouped battery; governing D12/D13 requires higher-order joint capability. Evidence: Library: R14_SOURCE_NATIVE_CANDIDATE_INTEGRITY_AUDIT_R3.csv, WVS W7 grouped source-native candidate rows and questionnaire locators; status SEMANTIC_REVIEW_READY where reported; Library: Pasted text(20260819-162348).txt, D12/D13/C11 sections; M01-M18 and source-retention law.

### A11 — Exact source-file/release provenance must be hash-bound externally

The SQL schema exposes `dataset_id` and `source_file`, but not an immutable file checksum on `survey_microdata_respondents/responses`. The finite receipt must therefore pair database occupancy with an exact raw artifact manifest/checksum from source authority or a retained Rawlsing manifest. Until that exists, M17/M18 remain open. Schema: Conversation upload: Rawlsing_WVS_public_schema(1).sql:L6450-L6494. D13: Library: Pasted text(20260819-162348).txt, D12/D13/C11 sections; M01-M18 and source-retention law.
