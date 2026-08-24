# R05 — Routing, Applicability, Respondent Position & P5 Conditioning Court

Status: `ISSUED__NONDISPOSITIVE__SOURCE_SENSITIVE`

## Mission

Revalidate the sufficiency and source-faithfulness of current routing/applicability, respondent/source-position and P5 conditioning authority, with special attention to the distinction between explicit unresolved states and recoverable source evidence.

## Primary authority surfaces

- R10H O06 routing/applicability over all 18,276 implementations;
- R10H O08 respondent/source-position lanes;
- R10I O09 P5 strata/Horizon placement and conditioner dispositions;
- question-wave itinerary and accepted SWID repair lineage;
- respondent source and respondent semantics registries;
- source-native questionnaires, filters, skip instructions, universes and sample design documentation;
- R10F reroute obligations where behavior/static position was distinguished;
- source-specific manual exceptions and family authority.

## Core questions

1. Are O06 routing classes source-backed at the right granularity?
2. For `SOURCE_ROUTING_UNRESOLVED`, is unresolved the correct evidence ceiling, or is exact routing recoverable from existing source material?
3. Are respondent-answer, demographic, country, split-sample, module/ballot and multi-condition predicates distinguished correctly?
4. Are unconditional/source-proven items truly ask-all within their source universe?
5. Are admin/nonrespondent rows prevented from respondent composability?
6. Does O08 correctly separate respondent position, household position, source context, admin/paradata and non-position variables?
7. Are the 18 O08 unresolved rows genuinely unresolved?
8. Are the 28 O09 unresolved conditioner rows genuinely unresolved?
9. Does P5 placement preserve the difference between permitted strata, resolved direct strata and actual activation?
10. Are itinerary/SWID scope rules consistent with current-35 source identity?

## High-risk strata

- all O08/O09 unresolved rows;
- source-native questionnaires with explicit skip/filter text;
- cases where O12 later uses an exact prior-answer predicate despite O06 unresolved on one member;
- historical itinerary/SWID drift;
- modules/ballots/split samples;
- country-specific instruments inside combined datasets;
- parent-child batteries and contingent follow-ups;
- position variables with substantive-looking labels;
- static status variables previously treated as behavior endpoints.

## Sampling

Use common risk protocol.

Additionally:

- full audit of 18 O08 unresolved and 28 O09 unresolved rows where source evidence is accessible;
- deterministic sample of at least 200 O06 `SOURCE_ROUTING_UNRESOLVED` rows, stratified across all families/waves and risk classes;
- at least 50 source-proven conditional predicates across different condition classes;
- at least 50 unconditional/admin classifications as false-certainty checks;
- exact review of known itinerary/SWID divergence cases.

## Required outputs beyond common contract

- `O06_ROUTING_HOSTILE_AUDIT.csv`
- `O06_UNRESOLVED_RECOVERABILITY_LEDGER.csv`
- `O08_POSITION_HOSTILE_AUDIT.csv`
- `O09_CONDITIONER_HOSTILE_AUDIT.csv`
- `ITINERARY_SWID_APPLICABILITY_RECONCILIATION.csv`
- `ROUTING_EXPANSION_RECOMMENDATIONS.md`

## Defect classes

- `ROUTING_PREDICATE_MISREAD`
- `SOURCE_FILTER_OMITTED`
- `FALSE_ASK_ALL`
- `FALSE_UNRESOLVED`
- `FALSE_CERTAINTY`
- `POSITION_VS_SUBSTANTIVE_ERROR`
- `HOUSEHOLD_VS_RESPONDENT_POSITION_ERROR`
- `ADMIN_AS_RESPONDENT_ERROR`
- `P5_CONDITIONER_ERROR`
- `ITINERARY_SCOPE_ERROR`
- `SOURCE_LIMITED_UNRESOLVED`

## Forbidden

- no heuristic ASK-ALL defaults;
- no routing reconstruction from response missingness patterns alone where source documents exist;
- no promotion of P5 placement to actual generated-person state;
- no canonical routing edits;
- no assumption that 10,348 unresolved rows imply 10,348 missing-authority tasks.

## Terminal proposal

R05 must estimate how much of the current unresolved routing/position surface is correctly unresolved, how much is recoverable from existing source authority, and whether any systematic legacy classification defects require targeted expansion.