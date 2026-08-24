# R07 — Cross-Family Source-Native Hostile Validation Court

Status: `ISSUED__NONDISPOSITIVE__INDEPENDENT_CHALLENGER`

## Mission

Act as the campaign's independent hostile validator. Sample consequential legacy semantic/manual authority across all current source families and compare it directly against exact source-native questionnaire/codebook/methodological evidence.

R07 is deliberately less invested in preserving any particular ontology lineage. Its job is to estimate whether older accepted semantic work actually survives contact with the source.

## Scope

Cross-family sample from:

- WVS;
- EVS;
- GSS;
- LiTS;
- Latinobarómetro;
- South Asia;
- Afrobarometer;
- Arab Barometer;
- Asian Barometer;

Audit multiple authority lineages where available:

- P2/R9D/R10G semantic meaning;
- V525b semantic/driver judgments;
- QSMv2/FQRA structural/relation judgments;
- QRA directionality;
- R10F topology/endpoints;
- R10H routing/measurement/position;
- R10I conditioner judgments.

## Independence rule

For each audited item:

1. inspect the source evidence first where practical;
2. write a source-grounded proposition/evidence ceiling;
3. only then compare the existing Rawlsing judgment;
4. record agreement/disagreement and defect class.

This reduces anchoring on legacy authority.

## Primary questions

- How often do accepted legacy judgments materially contradict the source?
- Are defects clustered by authority lineage, family, semantic class or producing stage?
- Does apparent model-age/provenance risk predict error?
- Are explicit unresolved states generally correct or masking recoverable evidence?
- Are newer successor layers materially better than older ones?
- Are there systematic overreach patterns: equivalence collapse, target loss, driver overbreadth, directionality inference, routing certainty, etc.?

## Sampling

Follow common deterministic risk protocol but preserve an independent representative baseline.

Minimum initial audit target: 500 distinct governed assertions, unless source availability prevents this.

Suggested composition:

- 200 high/critical-risk units;
- 200 medium-risk units;
- 100 low-risk/control units;
- all nine source families represented;
- all material legacy semantic/manual provenance classes represented;
- no single family >25% unless justified by denominator weighting.

Do not let other workers hand-pick the sample.

## Evidence standard

Source-native wording/context outranks semantic elegance.

Where original-language and translation authority both exist, preserve whether disagreement is translation-dependent.

Where only variable labels are available, mark the evidence ceiling and do not claim stronger validation than the source permits.

## Required outputs beyond common contract

- `CROSS_FAMILY_HOSTILE_AUDIT.csv`
- `LEGACY_ERROR_RATE_BY_LINEAGE.csv`
- `LEGACY_ERROR_RATE_BY_SOURCE_FAMILY.csv`
- `LEGACY_ERROR_RATE_BY_DEFECT_CLASS.csv`
- `SOURCE_EVIDENCE_CEILING_LEDGER.csv`
- `INDEPENDENT_REVALIDATION_VERDICT.md`

## Severity

- `S0_NO_DEFECT`
- `S1_IMPRECISION_NO_DOWNSTREAM_EFFECT`
- `S2_MATERIAL_LOCAL_SEMANTIC_DEFECT`
- `S3_SYSTEMATIC_OR_HIGH_FANOUT_DEFECT`
- `S4_SOURCE_CONTRADICTION_OR_INVALID_AUTHORITY`

Expansion triggers should use S2+ as material defects, while reporting S1 separately.

## Model-age/provenance rule

Do not infer error solely from the age or capability of the producing agent. Test it.

But explicitly analyze whether defect rates differ by provenance class. If weaker/older agent lineages fail at materially higher rates, that is a valid campaign-level expansion signal.

## Forbidden

- no canonical correction;
- no taxonomy preference without source support;
- no convenience sample;
- no cherry-picking dramatic errors;
- no global error-rate estimate without reporting stratification and uncertainty.

## Terminal proposal

R07 should provide HQ with an empirical answer to the question: **how much confidence should we place in legacy accepted semantic/manual authority, and where is revalidation expansion actually warranted?**