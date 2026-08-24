# Authority Revalidation — HQ Adjudication & Escalation Protocol

Status: `BINDING__HQ_ONLY_DISPOSITIVE`

## HQ role

Vozhd/HQ is the sole dispositive court for this campaign.

Worker outputs are evidence and proposed findings. They become project authority only through explicit HQ adjudication recorded in the Control Room.

## HQ input discipline

HQ must ingest every worker return as a content-addressed packet/commit and record:

- worker branch and exact start/end SHA;
- files returned;
- exact hashes where applicable;
- denominator audited;
- sampling protocol compliance;
- source-evidence classes used;
- expansion triggers fired;
- proposed verdicts;
- open cross-worker conflicts.

No worker return may be accepted merely because it is internally confident or syntactically complete.

## Cross-worker overlap is intentional

The workers have different jurisdictions but deliberate overlap. Examples:

- R02 semantic meaning and R03 driver/facet may disagree over category boundaries;
- R04 response/directionality may expose semantic defects relevant to R02;
- R05 routing may expose source-context loss relevant to R06;
- R07 source-hostile validation may challenge any legacy lineage;
- R08 provenance may downgrade the confidence class of authority reviewed elsewhere.

HQ must preserve these disagreements until reconciled against source evidence.

## Reconciliation order

For each disputed or incomplete authority class:

1. establish the exact required consumer obligation and grain;
2. establish the exact existing authority object(s) and provenance;
3. establish source-native evidence ceiling;
4. compare worker findings at the same grain;
5. determine whether the issue is coverage, quality, provenance, jurisdiction or execution inheritance;
6. determine whether a targeted expanded audit is required;
7. only then issue an authority-family disposition.

## HQ terminal classifications

Use these dispositions at authority-family / lineage / bounded-class grain:

- `REQUIRED_SCOPE_FULLY_COVERED__QUALITY_REVALIDATED`
- `REQUIRED_SCOPE_FULLY_COVERED__QUALITY_ACCEPTABLE_WITH_BOUNDED_DEBT`
- `REQUIRED_SCOPE_FULLY_COVERED__LEGACY_QUALITY_NOT_YET_REVALIDATED`
- `PARTIAL_SCOPE__PARTIALITY_INTENTIONAL__JURISDICTION_COMPLETE`
- `PARTIAL_SCOPE__EXPANSION_REQUIRED`
- `SOURCE_LIMITED__EXPLICIT_UNRESOLVED_IS_CORRECT`
- `LEGACY_AUTHORITY__HOSTILE_SAMPLE_PASS`
- `LEGACY_AUTHORITY__SYSTEMATIC_DEFECT_DETECTED`
- `CONFLICT_REQUIRES_TARGETED_EXPANSION`
- `CONFLICT_RESOLVED__EXISTING_AUTHORITY_UPHELD`
- `CONFLICT_RESOLVED__SUCCESSOR_REQUIRED`
- `UNLOCATED__SEARCH_NOT_EXHAUSTED`
- `MISSING_PROVED__NEW_AUTHORITY_CREATION_REQUIRED`

## Creating successor authority after a defect

A systematic defect does **not** automatically authorize replacement authority.

HQ must separately establish:

1. the affected assertion grain and denominator;
2. why the existing authority is materially defective;
3. why a narrower correction is insufficient;
4. the source evidence from which a corrected assertion can lawfully be authored;
5. the provenance and review standard for the successor;
6. downstream consumers requiring replay;
7. explicit preservation of the superseded historical assertion and supersession edge.

If the source itself cannot resolve the question, the correct disposition may remain `SOURCE_LIMITED__EXPLICIT_UNRESOLVED_IS_CORRECT` rather than authoring certainty.

## Expansion court

When a worker fires an expansion trigger, HQ decides among:

- `NO_EXPANSION__DEFECT_BOUNDED`
- `EXPAND_WITHIN_LINEAGE`
- `EXPAND_WITHIN_SEMANTIC_CLASS`
- `EXPAND_WITHIN_SOURCE_FAMILY`
- `FULL_LINEAGE_CENSUS_REQUIRED`
- `CROSS_WORKER_JOINT_COURT_REQUIRED`

Expansion orders must name exact denominators and stop conditions.

## Legacy-agent quality

Model/agent pedigree is a risk factor, not itself evidence of error.

HQ may classify a lineage `LEGACY_AGENT__SOURCE_BACKED__NOT_REVALIDATED` because its production provenance warrants additional scrutiny. It may not reject the lineage simply because a newer model is stronger.

Conversely, historical project acceptance does not exempt source-backed semantic judgments from hostile review.

## Coverage sufficiency gate

For every required authority class, HQ must explicitly record:

- consumer requirement;
- required denominator/grain;
- observed covered denominator;
- whether partiality is intentional;
- whether uncovered units are inapplicable, source-limited, blocked, unlocated or genuinely missing;
- whether expansion/new authority is required.

No phrase such as `full carrier coverage` may substitute for this contract.

## Quality gate

For every authority lineage that materially supplies semantic/manual judgment, HQ must record one of:

- source-native/mechanical — semantic revalidation not applicable;
- explicit human/manual with adequate accepted provenance;
- legacy source-backed hostile-sample pass;
- current high-confidence source-backed revalidated;
- systematic defect detected and bounded;
- quality still untested / campaign incomplete.

## Schema-migration gate

The physical schema/migration/replay court remains blocked until all **material** authority classes needed by recovered runtime/compiler capabilities are either:

- sufficiently covered and quality-certified;
- intentionally bounded with jurisdiction proved;
- explicitly source-limited/unresolved and carried fail-closed;
- or governed by a bounded successor-authority creation plan.

The physical schema may preserve unresolved authority, but it may not prematurely canonize an unreviewed legacy lineage as if its quality had been established.

## Required HQ outputs

After worker returns:

- `HQ_WORKER_RETURN_ADJUDICATION_LEDGER.csv`
- `AUTHORITY_REQUIREMENT_SUFFICIENCY_MATRIX.csv`
- `LEGACY_AUTHORITY_QUALITY_CERTIFICATION_LEDGER.csv`
- `SYSTEMATIC_DEFECT_AND_EXPANSION_LEDGER.csv`
- `SOURCE_LIMITED_UNRESOLVED_LEDGER.csv`
- `PROVED_MISSING_AUTHORITY_LEDGER.csv`
- `SUPERSESSION_AND_SUCCESSOR_AUTHORITY_PLAN.csv`
- `AUTHORITY_REVALIDATION_FINAL_ADJUDICATION.md`
- updated Control Room front doors and schema gate state.

## Terminal campaign gate

The campaign closes only when HQ can answer, without reconstructing chat:

- What authority does Rawlsing need?
- What exact scope does it need?
- What existing authority supplies it?
- How was that authority produced?
- Has its semantic quality been revalidated to an adequate standard?
- What remains intentionally unresolved?
- What is genuinely deficient?
- What new authority, if any, is now lawfully authorized?
- What must the future physical substrate preserve, supersede or fail closed on?