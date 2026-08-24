# Authority Sufficiency & Quality Revalidation — Common Rabochii Contract

Status: `BINDING_FOR_R01_R08`

## Role

Every Rabochii is a **non-dispositive evidence court**. Workers may find, hash, compare, sample, audit, classify, challenge and recommend. They may not silently promote, retire, overwrite or create canonical semantic authority.

HQ/Vozhd alone issues campaign-wide acceptance, rejection, supersession, expansion or missing-authority rulings.

## Mandatory reading order

Each worker must read before substantive analysis:

1. `00_CAMPAIGN_AUTHORITY.md`
2. this common contract;
3. `02_RISK_STRATIFICATION_AND_SAMPLING_PROTOCOL.md`
4. `03_HQ_ADJUDICATION_AND_ESCALATION_PROTOCOL.md`
5. its own `R0X_*_TASK.md`;
6. `AUTHORITY_EXPECTATION_UNIVERSE.csv`;
7. `CURRENT35_AUTHORITY_QUALITY_AND_GAP_LEDGER.csv`;
8. `NORMALIZED_AUTHORITY_BINDING_MATRIX.csv`;
9. `USABLE_UNIVERSE_AND_BINDING_ADJUDICATION.md`;
10. the exact governing authority objects named by its task.

Workers must ground themselves in current checked-in/Library/Git evidence before reasoning from remembered project state.

## Common epistemic distinctions

Never collapse:

- existence vs sufficiency;
- sufficiency vs quality;
- historical acceptance vs current revalidation;
- carrier coverage vs source-meaning coverage;
- source-limited unresolved vs missing work;
- generated discovery vs accepted authority;
- semantic authority vs structural authority;
- source-native fact vs Rawlsing interpretation;
- conflict vs supersession;
- later artifact vs lawful successor;
- exact implementation identity vs concept/equivalence relation.

## Required authority-state vocabulary

Workers must classify findings using only these states unless a task defines a stricter subtype:

- `EXISTS__SOURCE_NATIVE_MECHANICAL__HIGH_CONFIDENCE`
- `EXISTS__HUMAN_OR_MANUAL__ACCEPTED`
- `EXISTS__LEGACY_AGENT__SOURCE_BACKED__NOT_REVALIDATED`
- `EXISTS__LEGACY_AGENT__HOSTILE_SAMPLE_PASS`
- `EXISTS__LEGACY_AGENT__SYSTEMATIC_DEFECT_DETECTED`
- `EXISTS__CURRENT_HIGH_CONFIDENCE__SOURCE_BACKED`
- `EXISTS__GENERATED_OR_DISCOVERY_ONLY`
- `EXISTS__BLOCKED_OR_REVIEW_REQUIRED`
- `EXISTS__CONFLICTING__HQ_ADJUDICATION_REQUIRED`
- `PARTIAL_SCOPE__PARTIALITY_INTENTIONAL`
- `PARTIAL_SCOPE__EXPANSION_REQUIRED`
- `SOURCE_LIMITED__EXPLICIT_UNRESOLVED_IS_CORRECT`
- `UNLOCATED__SEARCH_NOT_EXHAUSTED`
- `MISSING_PROVED__NEW_AUTHORITY_CREATION_REQUIRED_CANDIDATE`

The final `MISSING_PROVED...` state remains only a **candidate** at worker level. HQ must prove it dispositively.

## Evidence hierarchy

When judgments conflict, workers must distinguish evidence classes rather than choosing by recency:

1. exact source-native questionnaire/codebook/methodological evidence;
2. explicit human/manual adjudication with provenance;
3. accepted source-backed governed successor authority;
4. older accepted source-backed authority;
5. deterministic derivation from named authority;
6. generated/heuristic/discovery material;
7. carrier row order/path/mtime/filename recency — **never authority**.

A stronger epistemic class does not automatically supersede a weaker one; same-grain replacement requires an explicit HQ supersession ruling.

## Source-backed challenge rule

Semantic-quality challenges must identify the exact proposition being tested and the exact source evidence relevant to it.

A worker may not call a legacy judgment wrong merely because a newer model prefers a different taxonomy.

A defect requires one or more of:

- contradiction with source wording/context/response topology;
- materially unsupported semantic inference;
- category error against the governed ontology/jurisdiction;
- inconsistent treatment of source-equivalent cases;
- ungoverned equivalence/continuity collapse;
- loss of target, condition, modality, actor, horizon or respondent universe;
- downstream authority requiring a claim not supported by the evidence ceiling.

## Audit row requirements

Every audited item must retain enough identifiers to replay the judgment:

- governing implementation/semantic-unit/relation/assertion ID;
- source family and wave;
- exact variable/question identifier;
- authority object and content identity;
- provenance class/stage where known;
- risk stratum;
- source evidence locator;
- legacy judgment;
- worker finding;
- confidence;
- defect class if any;
- whether the defect is local or lineage/systematic;
- proposed next action.

## Sampling law

Workers may not use convenience samples.

Use the deterministic risk-stratified protocol in `02_RISK_STRATIFICATION_AND_SAMPLING_PROTOCOL.md`.

Any expansion beyond the initial bounded sample must be triggered by the common thresholds or explicitly requested by HQ.

## Disagreement law

Do not average incompatible judgments.

Where source evidence supports multiple interpretations or worker confidence is insufficient, return:

`EXISTS__CONFLICTING__HQ_ADJUDICATION_REQUIRED`

with the competing interpretations and evidence ceilings.

## Authority-creation prohibition

Workers must not write new canonical semantic, driver, directionality, routing, relation or position authority.

If a required obligation appears genuinely absent, the worker must emit a bounded candidate record containing:

- exact required assertion/grain;
- exact consumers that require it;
- exhaustive searches performed;
- source-native evidence checked;
- why derivation from existing authority is impossible;
- whether source evidence itself is sufficient to author it;
- proposed authority-creation scope.

HQ alone decides whether the proof reaches `MISSING_PROVED__NEW_AUTHORITY_CREATION_REQUIRED`.

## Mutation boundary

Allowed writes are restricted to the worker's campaign return directory and bounded evidence/receipt files.

Forbidden during worker courts:

- source survey mutation;
- runtime/compiler mutation;
- canonical authority mutation;
- destructive cleanup;
- row-order deduplication;
- hidden recoding of negative states.

## Required worker outputs

Every worker must produce, at minimum:

- `README.md` — jurisdiction and verdict;
- `EVIDENCE_MANIFEST.csv` — content-addressed inputs used;
- `AUDIT_SAMPLE_OR_CENSUS.csv` — exact reviewed units;
- `FINDING_LEDGER.csv` — machine-readable findings;
- `COVERAGE_AND_QUALITY_SUMMARY.json` — counts by verdict/risk/source;
- `SYSTEMATIC_DEFECT_OR_EXPANSION_TRIGGERS.md` — explicit threshold results;
- `OPEN_HQ_QUESTIONS.md` — only genuine cross-jurisdiction issues;
- `RETURN_ADJUDICATION_PROPOSAL.md` — non-dispositive proposed ruling.

Workers should add task-specific outputs where required.

## Stop condition

Each worker stops after its bounded return is internally validated and committed to its worker branch.

Do not continue into another worker's jurisdiction or attempt campaign-wide closure.