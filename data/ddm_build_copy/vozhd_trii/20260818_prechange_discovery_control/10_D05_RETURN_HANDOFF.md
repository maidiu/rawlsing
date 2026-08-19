# D05 RETURN HANDOFF — POPULATED EMPIRICAL SUBSTRATE REALITY

You are the returning Rabochii for **Vozhd Trii D05**.

Repository:

`maidiu/rawlsing`

Continue work ONLY on the existing branch:

`agent/vozhd-trii-d05-empirical-substrate`

Original worker base:

`bf9a0434eb2096d5c4725cf483ec757fd319b6af`

Do **not** recreate the branch from current parent. Do not modify production code.

## RETURN DISPOSITION

`RETURN_REQUIRED__NOT_CLOSED`

Your substantive fail-closed verdict remains provisionally accepted:

`BLOCKED_MISSING_POPULATED_DATA_ACCESS`

The court is being returned because the execution/evidence contract was not completed and controlled evidence identity was misreported.

Before changing anything, read the current parent review authority on:

`agent/vozhd-trii-prechange-discovery-control`

especially:

- `09_D01_D06_REVIEW_ADJUDICATION.md`
- `DISCOVERY_REGISTER.json`
- the original `06_FIRST_WAVE_LAUNCH_REGISTER.md`
- your existing `courts/D05/RESULT.md`

Where the second-pass parent review conflicts with the earlier intake, the second-pass review controls.

## MISSION

Return D05 in a form where **another worker who obtains populated production or production-equivalent database access can execute the empirical audit without making new semantic decisions**.

Do not infer populated facts from DDL, code shape, artifact names, expected schemas, or historical reports.

If populated data remain unavailable, the final substantive environment verdict may remain:

`BLOCKED_MISSING_POPULATED_DATA_ACCESS`

But the **audit apparatus itself must be complete and executable**.

## BINDING GOVERNING LAW

Read and obey:

- `RAWLSING_GOVERNING_SPIRIT.md`
- `TERMINAL_DEMAND_ENVELOPE.md`
- `ARCHITECTURE_PASS_LAW.md`
- current Vozhd Trii control files listed above

Preserve the distinction among:

- source evidence;
- populated empirical fact;
- diagnostic computation;
- structural interpretation;
- actor position;
- lived exposure;
- actor belief/identity;
- expression.

No retention redesign, schema redesign, ingestion repair, V550 redesign, or architecture recommendation is authorized.

## REQUIRED CORRECTIONS

### 1. Repair controlled evidence identity

Your existing `RESULT.md` reports incorrect expected SHA256 values for the two controlled schema attachments.

The parent-controlled identities are:

- `Rawlsing_WVS_public_schema.sql`
  - SHA256 `2c3f4a9ebec1e6c0cf62e8827ab982e52243c5c8899c961cd0e30b489573ec76`
- `Rawlsing_WVS_authority_reconcile_schema.sql`
  - SHA256 `57e8c58c9444be9c34df54765e1801a9819f7a15fd02ddaa9a8e194e57596877`

Correct your result and machine-readable provenance.

If you believe a distinct byte source was actually inspected, prove that exact source and SHA separately. Do not silently substitute one evidence object for another.

### 2. Supply the missing required outputs

Under:

`data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/courts/D05/`

produce at minimum:

- `RESULT.md`
- `RESULT.json`
- `AUDIT.sql` or an equally exact read-only executable audit program if SQL alone cannot lawfully express a required check
- `EXPECTED_OUTPUT_SCHEMAS.json`

If additional helper scripts are required, keep them inside this D05 directory and make their invocation deterministic.

### 3. Make the audit kit mechanically executable

The audit must specify:

- exact required relations/views/files;
- exact columns used;
- exact grain of every output row;
- exact join keys;
- exact distinctness/uniqueness assumptions being tested rather than assumed;
- exact null/special-state treatment;
- exact numerator/denominator law for every rate;
- exact threshold or classification law where a verdict depends on a threshold;
- exact failure code when a required relation, column, source artifact, or materialized cache is unavailable.

A future completing worker must not have to decide what you “probably meant.”

## REQUIRED EMPIRICAL AUDIT COVERAGE

The execution kit must cover at least the following.

### A. Respondent identity and response multiplicity

Measure by source/wave/country and question where applicable:

- respondent counts;
- blank/missing respondent identifiers;
- duplicate respondent rows;
- duplicate respondent×question scalar-response keys;
- repeated responses;
- apparent multiselect/multirow response structures;
- whether duplicate collapse would be information-losing.

Do not classify legitimate multirow structures as corrupt duplicates merely because they violate scalar uniqueness.

### B. Source/wave/country physical coverage

Measure:

- populated source families;
- raw waves;
- canonical waves;
- countries;
- respondent counts and response-row counts by scope;
- source/wave/country scopes present in authority/mapping surfaces but absent empirically, and vice versa.

### C. Same-respondent cotravel support

Measure the physical ability to support same-person cross-question analysis:

- question respondent counts;
- pairwise overlap counts/rates;
- scopes with no usable overlap;
- overlap loss introduced by downstream views if measurable;
- whether respondent IDs remain stable across the relations current V550/V550J actually read.

Do not attempt exhaustive all-question pair materialization if that is computationally explosive; an exact bounded/auditable program may emit sufficient summaries plus an explicit query for arbitrary requested pairs. State the law precisely.

### D. Position-coordinate completeness

For every empirical position field current V550 may read, including the current position-field inventory where present, measure:

- nonblank coverage;
- cardinality;
- typed/untypeable missingness where available;
- respondent coverage by source/wave/country;
- whether position rows multiply or drop response rows under joins.

Do not infer structural ontology from shared field names.

### E. Weights

Measure:

- availability of primary weights;
- missing/zero/negative/nonfinite weights;
- multiple-primary-weight anomalies;
- coverage by source/wave/country;
- respondent linkage.

A scalar weight column does **not** establish design-based inference authority. Keep empirical availability separate from normative weighting law.

### F. Response topology and typed absence

Where current physical columns permit it, measure:

- substantive responses;
- DK;
- refusal;
- IAP/inapplicable;
- not asked;
- blank/other special states;
- response-option authority coverage;
- raw response values not represented by current canonical semantics.

Do not collapse absence categories merely to simplify reporting.

### G. Canonical identity / authority joins

Audit:

- raw question identity → canonical question identity;
- raw wave → canonical wave;
- country-scoped mapping identity;
- multiplicity on `question_structural_mapping` / authority joins;
- row loss or multiplication through facet-ready views;
- scopes where authority metadata can attach ambiguously or at weaker grain than the governing resolver.

### H. Raw substrate → facet-ready preservation

Where the populated relations exist, compare raw respondent/response incidence to the exact current facet-ready relation used by V550.

Measure at minimum:

- respondent preservation;
- response-row preservation;
- question preservation;
- source/wave/country preservation;
- multiplicative joins;
- dropped rows;
- response-value mutation if observable;
- position/weight attachment failures.

### I. Shared V550/V550J respondent substrate

If the actual materialized shared respondent substrate for the same run/build is available, audit it separately.

Compare it against its upstream populated source at respondent×question grain and classify:

- retained columns;
- dropped columns;
- dropped rows;
- response-state preservation;
- respondent identity preservation;
- question identity preservation;
- weight preservation;
- position/context preservation;
- joint-only/base-only selection effects;
- duplicate/multiselect loss;
- provenance/hash consistency.

Do **not** call it source-equivalent merely because its manifest says complete or its logical hash validates.

### J. Source-native / ingest loss

Only if the exact source-native/ingest artifacts corresponding to the populated snapshot are available, compare them to the database substrate.

If they are unavailable, return a typed blocker for source-native equivalence rather than inferring no loss.

## REQUIRED OUTPUT TABLES

Your existing result promised these outputs. Preserve them or replace them only with a strictly more explicit machine-readable decomposition:

- `SOURCE_WAVE_READINESS.csv`
- `POSITION_FIELD_COMPLETENESS.csv`
- `QUESTION_OVERLAP_SUMMARY.csv`
- `WEIGHT_COVERAGE.csv`
- `IDENTITY_JOIN_AUDIT.csv`
- `RESPONSE_MULTIPLICITY_AUDIT.csv`

`EXPECTED_OUTPUT_SCHEMAS.json` must define every column, grain, type, nullability expectation, and metric meaning for each output.

If an output cannot be populated without live data, the audit kit must still define its exact schema and generating query.

## SOURCE-EQUIVALENCE VERDICT LAW

Do not force a positive or negative source-equivalence classification when required evidence is absent.

Your machine-readable result must separately classify at least:

1. database internal respondent/response replay sufficiency;
2. facet-ready relation replay sufficiency;
3. shared V550/V550J substrate replay sufficiency;
4. source-native equivalence.

Each classification must be one of a finite declared vocabulary such as:

- `PROVED_SUFFICIENT_FOR_DECLARED_CAPABILITY_SET`
- `PROVED_INSUFFICIENT__INFORMATION_LOSS_IDENTIFIED`
- `PARTIALLY_TESTED__OPEN_DIMENSIONS`
- `BLOCKED_MISSING_REQUIRED_ARTIFACT`
- `BLOCKED_MISSING_POPULATED_DATA_ACCESS`

If you use a different vocabulary, define it exactly.

Do not claim **all future lawful conditional queries** are reconstructible unless you have proved the retained substrate preserves the information required for the declared query class. D13 owns final retention/replay proof.

## RESULT.JSON MINIMUM CONTENT

`RESULT.json` must include at minimum:

- court ID and branch;
- original audited base;
- final verdict;
- populated-data-access status;
- exact evidence objects + SHA256 where applicable;
- exact audit-program files;
- required input relations/files;
- output artifacts and schemas;
- blockers;
- empirically established facts, if any;
- explicitly unadjudicated facts;
- source-equivalence classifications by layer;
- downstream courts unlocked or still blocked.

## PROHIBITED SHORTCUTS

Do not:

- substitute schema existence for populated coverage;
- substitute code reachability for actual materialization;
- infer respondent overlap from question counts;
- infer uniqueness from primary-key intent when querying can test it;
- treat missing data as a zero observation;
- treat multiselect/repeated response as corruption without authority;
- infer source equivalence from shared column names;
- invent database results;
- redesign the storage architecture.

## CLOSURE CONDITION

D05 may close empirically only if populated/source artifacts sufficient for the requested measurements are actually available and tested.

If they remain unavailable, D05 may still return a **contract-complete blocked result** only when the audit kit, schemas, provenance identities, and blocker taxonomy above are complete enough for deterministic execution by the next worker.

The parent will separately decide whether that contract-complete blocked state is sufficient to unblock any dependency. Do not declare downstream courts unlocked yourself.