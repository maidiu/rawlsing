# AS2A LiTS-I Shared Source Certification Return

Status: `AS2A_LITS1_SHARED_CERTIFICATION_STILL_BLOCKED__PART_A_PASSED__PART_B_EXECUTION_DEPENDENCY_REQUIRED`

## Role / authority

`TRII_ROLE_RECONFIRMED`

Live Trii HEAD:
`04a0109aa170c6041b199e5c6130a39a8e0f6029`

Coordination HEAD:
`0f61b3840ddae78f4a5df30cde22b1bc82aaec2e`

This court is a `SHARED_PREREQUISITE`. No A/B/C route is selected or ranked.

## Exact source

LiTS-I source SHA-256:
`7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

Observed bytes:
`139531180`

Questionnaire SHA-256:
`b94bdcf4a9f2e2e025bf35e5364f79acf0b1f5fa05c035064e674fa58a921eae`

The uploaded normalized 1,198-row codebook has SHA-256:
`400ad9cf8b0b350a8ba1a2a778346f190ef2bba710145e648a12fc9ff464fc44`

It is not byte-identical to the previously banked raw codebook member `91698cbc22d7498c3587bcacd7f96be47323d2bc9867cec5103e954e5099eb0c`. It was used only as an alignment aid after proving its exact 1,198-variable order matches the DTA; semantic decisions are grounded in Authority 82 + source questionnaire + accepted authority.

## Part A

`PART_A = PASS`

Respondent-role bridge:
`urn:rawlsing:pre553:as2a:lits1:respondent-role-bridge:sha256:1d4249a2bdbd373503c68f60b3c83882428ca3c2b3f3e37cb5178ad76e4f0d80`

Bridge hash:
`1d4249a2bdbd373503c68f60b3c83882428ca3c2b3f3e37cb5178ad76e4f0d80`

Governed source-specific projection-authority identity:
`urn:rawlsing:pre553:as2a:lits1:governed-c11-projection-authority:sha256:aa8b4c0fd75d277db0ccedb4ea6e2570f1c48ba63b74cd3940927138bbe23fa0`

Projection hash:
`aa8b4c0fd75d277db0ccedb4ea6e2570f1c48ba63b74cd3940927138bbe23fa0`

Disposition counts:

- 893 `SOURCE_PRESERVED_NONPARTICIPATING__SELECTED_RESPONDENT_OUTSIDE_BOUNDED_PROVING_SCOPE`
- 175 `SOURCE_PRESERVED_NONPARTICIPATING__HOUSEHOLD_OR_REPORTER_CONTEXT`
- 65 `PROJECT_RESPONDENT_EVENT__SELECTED_RESPONDENT__BOUNDED_PROVING_SCOPE`
- 42 `SOURCE_PRESERVED_NONPARTICIPATING__IDENTITY_SELECTION_OR_DERIVED_PROVENANCE`
- 18 `SOURCE_PRESERVED_NONPARTICIPATING__INTERVIEWER_OBSERVATION`
- 3 `SOURCE_PRESERVED_NONPARTICIPATING__WEIGHT_CANDIDATE__RAW_PROVING_SCOPE`
- 2 `PROJECT_EMPIRICAL_COORDINATE_FACT__SOURCE_SCOPED`

`UNACCOUNTED_LITS1_SOURCE_SLOT = 0`

`UNRESOLVED_RESPONDENT_ROLE_REQUIRED_FOR_PROVING_SCOPE = 0`

`UNRESOLVED_ROUTING_APPLICABILITY_REQUIRED_FOR_PROVING_SCOPE = 0`

The bounded proving scope is RAW/unweighted, single-release, observed-source-sample only. It uses 65 unconditional selected-respondent Section-3 response slots (Q3.01-Q3.14 excluding conditional Q3.15) plus raw source-scoped `country` and `tablec` coordinates. All other source slots are preserved without forced semantic promotion.

## Part B

`PART_B = BLOCKED_BEFORE_GOVERNED_DECODER`

The exact source bytes are present, but the frozen decoder implementation requires `pyreadstat`. The current Python 3.13 environment has no `pyreadstat`, no local/system `readstat` runtime, and package installation cannot resolve external package DNS.

No alternate parser was substituted.

Therefore no truthful source-specific `C11SourceReleaseCandidate`, `C11LogicalRelease`, `ReplayManifest`, `C11Repository`, hostile-fixture execution, I03 certification receipt, or full-source resource receipt can be issued yet.

Smallest exact residual blocker:

`AS2A-B01__PYREADSTAT_EXECUTION_DEPENDENCY_SUPPLY`

The same court can resume immediately once a compatible CPython 3.13 Linux x86_64 `pyreadstat` runtime/wheel is supplied. Part A does not need to be reopened.

## Gate disposition

`FIRST_ACCEPTED_REAL_SOURCE_SOURCE_BACKED_C11_RELEASE = NO`

`C05R2B_UNLOCK_CONDITION = NOT_SATISFIED`

`AS2A_LITS1_SHARED_CERTIFICATION_STILL_BLOCKED`

Smallest residual blocker set:
`{AS2A-B01}`

No route selected.
