# AUTHORITY CENSUS CAMPAIGN — ITERATION & CLOSURE PROTOCOL

Status: `BINDING_ITERATION_AND_GATE_LAW`

## 1. Campaign loop

The campaign runs as a repeated two-lane evidence loop:

`BROWSER PRE-CENSUS / ADJUDICATION`
`-> HARVEST REQUEST IF NEEDED`
`-> LOCAL EXACT BYTE HARVEST`
`-> USER UPLOAD / BROWSER INSPECTION`
`-> LEDGER UPDATE / LINEAGE ADJUDICATION`
`-> NEXT REQUEST OR EXPECTATION CLOSURE`

The browser branch is the persistent semantic working branch. The local branch may be reused for successive harvest iterations if clean, or a new numbered local branch may be created from the latest HQ-adopted campaign head.

## 2. Harvest request state machine

Each HARVEST request has one state:

- `REQUESTED`
- `LOCAL_SEARCH_IN_PROGRESS`
- `RETURNED_NOT_ADJUDICATED`
- `ADJUDICATED__SUFFICIENT`
- `ADJUDICATED__FOLLOW_UP_REQUIRED`
- `ADJUDICATED__NEGATIVE_EVIDENCE_ACCEPTED`
- `SUPERSEDED_BY_LATER_REQUEST`

No negative local search alone proves authority missing. Browser HQ must combine it with the common-contract search burden.

## 3. Authority expectation closure

Each expectation closes only as one of:

- `EXISTS__ACCEPTED_AUTHORITY_MAPPED`
- `EXISTS__PARTIAL_SCOPE__REMAINING_GAP_EXPLICIT`
- `EXISTS__REVIEW_ONLY__NEW_ACCEPTED_AUTHORITY_REQUIRED_IF_CONSUMED`
- `EXISTS__CONFLICT_REQUIRES_HQ_ADJUDICATION`
- `SUPERSEDED__LOSSLESS_SUCCESSOR_PROVED`
- `NOT_REQUIRED__POSITIVE_EXCLUSION_AUTHORITY`
- `MISSING_PROVED__NEW_AUTHORITY_CREATION_REQUIRED`

No other terminal state is lawful.

## 4. Campaign closure matrix

Before final PASS, browser HQ must demonstrate:

### Coverage

- every authority family required by the master scope is represented in the expectation universe;
- every current-35 source/family scope required by those authorities is covered or positively excluded;
- every known manually/adjudicatively created authority family identified by G1A has a mapped lineage/disposition;
- review-only and negative authority are not silently dropped.

### Physical mapping

- each located byte-bearing authority object has at least one physical-location record;
- duplicate physical copies may remain unresolved for later dedup, but their content identity is recorded where known;
- unique historical objects in RawlsingsExcess are not silently treated as obsolete.

### Epistemic mapping

- each live object has an epistemic class;
- manual vs mechanical provenance is explicit;
- execution eligibility/status is explicit;
- downstream consumer or preservation-only role is explicit.

### Provenance/supersession

- no important historical manual authority is declared disposable merely because a later aggregate exists;
- lossless supersession claims carry positive evidence;
- partial absorption remains partial.

### True-gap proof

For every row in `WHAT_AUTHORITY_STILL_NEEDS_TO_BE_MADE.csv`:

- corresponding expectation exists;
- all relevant search surfaces are recorded;
- local targeted search was performed where local evidence could matter;
- no accepted successor already satisfies the obligation;
- the missing semantic obligation is described narrowly enough to authorize later manual/documentary work without redesign.

## 5. Relationship to dedup/hygiene

Campaign completion does not itself delete files.

Its canonicality/location findings become the semantic input to the future maintenance/dedup campaign.

Only after authority census closure may the parent desk proceed from:

`WHAT EXISTS?`

to:

`WHICH PHYSICAL COPIES CAN SAFELY GO?`

## 6. Relationship to new authority authoring

The final gap ledger becomes the sole default backlog for new/manual authority work spawned by this campaign.

Workers must not broaden a gap while repairing it. If the census says only a bounded routing rule is missing, the later worker may not rewrite the source semantic model.

## 7. PASS / BLOCK

PASS:

`AUTHORITY_CENSUS_PASS__EXISTING_EPISTEMIC_CAPITAL_MAPPED__TRUE_GAPS_EXPLICIT`

BLOCK examples:

- `AUTHORITY_CENSUS_BLOCKED__LOCAL_PAYLOAD_REQUIRED`
- `AUTHORITY_CENSUS_BLOCKED__PROVENANCE_SUPERSESSION_UNRESOLVED`
- `AUTHORITY_CENSUS_BLOCKED__AUTHORITY_EXPECTATION_UNIVERSE_INCOMPLETE`
- `AUTHORITY_CENSUS_BLOCKED__CONFLICTING_ACCEPTED_AUTHORITY`

A BLOCK is preferable to inventing a missing object or falsely declaring supersession.
