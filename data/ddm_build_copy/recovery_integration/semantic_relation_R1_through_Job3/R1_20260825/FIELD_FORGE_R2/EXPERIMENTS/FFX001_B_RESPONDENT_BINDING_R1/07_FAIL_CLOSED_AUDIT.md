# FFX001-B — FAIL-CLOSED AUDIT

Terminal ruling under audit:

`OBSERVABILITY_LIMIT__NO_EXACT_CURRENT_RESPONDENT_BINDING_ESTABLISHED_AFTER_BOUNDED_SEARCH`

Blocker subtype:

`CURRENT_RESPONDENT_BINDING_NOT_CANONICALLY_REACHABLE_FOR_Q86_CANARY`

## Hard-rule audit

| prohibited move | audit result |
|---|---|
| Treat nonmissing response as proof of exposure and missing response as nonexposure | NOT USED. No response-value inference was admitted. |
| Source/catalog co-presence alone | NOT USED. C04/Contract@2 membership was treated as question-level authority only. |
| `CURRENT_J_CANDIDATE` status alone | NOT USED. Candidate status was not promoted into respondent execution. |
| Routing-ledger positivity without respondent predicate execution | REJECTED AS EXPOSURE PROOF. Q86 positivity establishes predicate authority, not exposure rows. |
| Ungoverned or guessed respondent identity | NOT USED. Absence of governed key caused terminalization. |
| Inferred cross-file row alignment | NOT USED. No historical/current row co-indexing was accepted. |
| Neighboring-wave substitution | NOT USED. Canary remains Afrobarometer R5. |
| Fuzzy variable-name matching | NOT USED. Exact current IDs, Q86A–Q86F codes, predicate IDs, and evidence refs were used. |
| Invented predicate semantics | NOT USED. Predicate AST and native-primary evidence were recovered from C04 sidecars. |
| Dropping country/form/split/instrument restrictions | NOT USED. Named-country restriction is preserved; absence of respondent form/scope binding remains unresolved rather than erased. |
| Treating `MULTIPLE_RESPONSE_SET` as repeated independent prompts | NOT USED. Canary is the genuine repeated-measurement Q86 grid. |
| Assuming all rows in merged release share identical questionnaire exposure | EXPLICITLY REJECTED. Native evidence states Q86 is not asked in five named countries. |
| Silently converting unresolved routing/exposure into false/nonexposed | NOT USED. Unmaterialized exposure stays unresolved/unemitted. |
| Using a historical carrier merely because it contains desired variables | NOT USED. Historical respondent substrate was not promoted without current succession authority. |

## Noncollapse preserved

`CONTEXT_CAPABILITY_OBSERVABILITY != MEASUREMENT_ELIGIBILITY_TOPOLOGY != RESPONDENT_MEASUREMENT_EXPOSURE_TOPOLOGY != RESPONDENT_RESPONSE`

`SOURCE_PRESENCE != ELIGIBILITY != EXPOSURE != RESPONSE`

`CURRENT_J_CANDIDATE != EXECUTABLE_SAME_RESPONDENT_J`

Additional exact nonclaims preserved:

`PHYSICAL_DATA_EXISTENCE != CURRENT_AUTHORITY`

`HISTORICAL_EXECUTABLE_CARRIER != CURRENT_CANONICAL_RESPONDENT_BINDING`

`QUESTION_LEVEL_ROUTING_AUTHORITY != RESPONDENT_LEVEL_PREDICATE_EXECUTION`

`RESPONDENT_RESPONSE_PRESENT != PROOF_OF_EXPOSURE`

`RESPONDENT_RESPONSE_MISSING != PROOF_OF_NONEXPOSURE`

`SOURCE/WAVE_MEMBERSHIP != EXECUTABLE_RESPONDENT_JOIN`

## Exposure-state discipline

The original target proof requested states such as `ELIGIBLE_AND_EXPOSED`, `ELIGIBLE_BUT_NOT_EXPOSED`, `NOT_ELIGIBLE`, and `UNRESOLVED_EXPOSURE` only where current source mechanics genuinely support them.

This worker does not emit respondent-level instances of any of those states, because no governed respondent entity/key was established. `05_EXPOSURE_CLASSIFICATION_RESULT.tsv` therefore contains six canary-member execution-attempt rows, not fabricated respondent rows.

No `ELIGIBLE_BUT_NOT_EXPOSED` state is minted. The named-country restriction can establish question-level nonadministration semantics if applied to a governed respondent country, but that respondent binding is precisely the missing seam.

## Historical substrate audit

W33 current delegated authority explicitly does not resurrect historical J membership, historical V550J denominators, or PostgreSQL semantic ownership. Therefore discovery of historical respondent-capable machinery cannot cure the current binding gap by itself.

The lawful standard remains: exact current succession must bind carrier bytes/identity, respondent key semantics, scope fields, and question-implementation relation before historical executable substrate may participate as CURRENT authority.

That standard was not met within the bounded search.

## Final audit disposition

`PASS__FAIL_CLOSED_TERMINALIZATION`

No respondent exposure rows were emitted, no prohibited inference was used to manufacture them, and the terminal observability limit is narrower than any claim of physical data absence.
