# SCR553 HOSTILE TEST ORACLE

**Contract:** `SCR553_V553_TEMPORAL_JURISDICTION_V1`  
**Purpose:** finite adversarial oracle for V553 local contract conformance.  
**Production implementation:** not authorized here.

Every fixture below is normative for later implementation/conformance work. A test may use synthetic exact refs; it must not rely on populated production data.

| ID | Hostile fixture | Required result |
|---|---|---|
| H553-001 | Supply a raw `EmpiricalFact` ref directly to V553. | `REJECT_NO_V553_OBJECT__RAW_EMPIRICAL_FACT_FORBIDDEN`; zero `TEMPORAL_*` objects. |
| H553-002 | Supply a legacy V552/V552J row/packet without an exact `StructuralEmpiricalAdmission`. | Reject semantic intake; compatibility fields cannot reconstruct admission. |
| H553-003 | Exact admitted 1985 proposition; use asks only same-scope bounded structural use and requests no new temporal operation. | `V553_NOT_REQUIRED_FOR_THIS_USE`; zero V553 semantic objects. |
| H553-004 | Same admission as H553-003 later used by a different governed use asking persistence to 1995 with exact second participant/rule. | Re-evaluate per use; V553 is required for the later use. Earlier direct use creates no exemption. |
| H553-005 | Admission contains timestamp/history metadata but target use requires no new temporal semantic. | No V553 transit and no no-op key/observation. |
| H553-006 | Cross-wave comparison required but temporal comparison rule ref is absent/unknown. | No positive relation; typed `TEMPORAL_LIMIT(MISSING_TEMPORAL_AUTHORITY)` where owned. |
| H553-007 | Two distinct source universes, same year and same labels, but no source-comparability authority. | Preserve source plurality; no positive relation/harmonization; `TEMPORAL_LIMIT(MISSING_SOURCE_COMPARABILITY_AUTHORITY)`. |
| H553-008 | Exact source relation says `NONCOMPARABLE`. | `TEMPORAL_LIMIT` with `NONCOMPARABLE`; no delta/trend/pooled result. |
| H553-009 | Cross-source comparison rule exists, but required estimand compatibility is missing. | `TEMPORAL_LIMIT(MISSING_ESTIMAND_COMPATIBILITY_AUTHORITY)`; no positive relation. |
| H553-010 | Cross-source comparison rule exists, but required measure compatibility is missing. | `TEMPORAL_LIMIT(MISSING_MEASURE_COMPATIBILITY_AUTHORITY)`; no positive relation. |
| H553-011 | Request a same-respondent longitudinal relation across records with no respondent-linkage authority. | `TEMPORAL_LIMIT(MISSING_RESPONDENT_LINKAGE_AUTHORITY)` or out-of-jurisdiction no-positive result; never infer linkage. |
| H553-012 | Request that V553 pool two source universes or manufacture a joint estimand. | `NO_POSITIVE_V553_OUTPUT__OUT_OF_JURISDICTION`; no pooled/composed object. |
| H553-013 | One admitted observation is exact zero; another is missing. | Zero remains `TEMPORAL_OBSERVATION` measurement; missing becomes typed limit/negative. They are not equal. |
| H553-014 | Omit exact source input but place a newer compatible-looking run in repository. | Fail closed. No `latest` discovery or substitution. |
| H553-015 | Exact requested 1995 participant is absent; a 1994/1996 observation exists. | Fail closed / typed missing-scope limit. No nearest-year substitution or interpolation unless an explicit exact rule requests and governs that derivation. |
| H553-016 | Two candidate observations share canonical labels but have different source universe refs. | Keep distinct. Label equality does not collapse keys/observations or establish comparability. |
| H553-017 | Exact relation participants are supplied in reverse order for an ordered delta rule. | Different request/semantic identity or rule rejection; participant order may not be silently sorted. |
| H553-018 | Same order-insensitive operation with participants supplied in different physical list order and rule explicitly declares order-insensitive. | Canonical identity normalizes deterministically and replays to identical semantic IDs. |
| H553-019 | Same labels/values but temporal rule authority digest changes. | New semantic identity/replay basis. Historical object is not rewritten and latest authority is not substituted. |
| H553-020 | Referenced admission content hash mismatches object content. | Fail closed; zero positive V553 objects. |
| H553-021 | Request `RUPTURE`/`PERSISTENCE`/`DRIFT` with no deterministic governed relation rule. | Missing-authority/valid-empty limit; never infer from pattern/score/readiness. |
| H553-022 | A readiness/harmonization/probe score is high but semantic authority is missing. | Score has zero authority effect; fail closed. |
| H553-023 | A `TEMPORAL_LIMIT` is replayed with all exact refs unchanged. | Same limit state/reason, same semantic hash, same object ID. |
| H553-024 | A valid TEMPORAL_LIMIT exists for use U; downstream attempts to treat absence of positive V553 relation as positive absence of relation. | Forbidden. Typed limit remains distinct from positive assertion of absence. |
| H553-025 | A valid TEMPORAL_LIMIT exists for use U; downstream attempts to bypass it using direct admission for the same temporal demand. | SCR553 side rejects semantic downgrade; M1 must prove SCR554 negative precedence blocks direct positive basis. |
| H553-026 | Same admission participates in two uses: U1 needs no V553 meaning; U2 needs a derived interval. | U1: zero V553 objects. U2: derived `TEMPORAL_KEY` if rule positive; otherwise typed limit. |
| H553-027 | Temporal relation tries to infer structural source→target direction from the sign of a delta. | Reject inference; temporal direction and structural direction remain distinct. |
| H553-028 | Cross-source temporal comparability is positive; consumer treats that as permission to sample/pool/join respondents. | Forbidden. Temporal comparability grants none of those authorities. |
| H553-029 | Upstream admission is `ADMISSION_DENIED` but its ancestral EmpiricalFact is positive. | No positive V553 output. Raw ancestral fact cannot bypass the admission state. |
| H553-030 | Upstream admission is `NEGATIVE_AUTHORITY_ONLY`; V553 operation rule does not own a more specific temporal limit. | Preserve upstream negative by exact ref; zero invented positive or invented V553 negative semantic. |
| H553-031 | Derived interval uses an unlisted third observation discovered from repository. | Fail. Every semantic derivation participant must be explicit in request/rule identity. |
| H553-032 | Same exact request is replayed under different filesystem ordering or timestamps. | Same decision and object IDs; filesystem/wall-clock differences are nonsemantic. |

## Oracle invariants

A passing implementation must prove all of the following simultaneously:

```text
NO_RAW_FACT_BYPASS
NO_UNIVERSAL_V553_TRANSIT
NO_OBJECT_GLOBAL_V553_EXEMPTION
NO_HIDDEN_LATEST_OR_NEAREST_TIME_SELECTION
NO_SOURCE_EQUIVALENCE_BY_LABEL_OR_TIME
NO_POOLING_OR_LINKAGE_BY_TEMPORAL_COMPARABILITY
UNKNOWN_COMPARABILITY_FAILS_CLOSED
TEMPORAL_LIMIT_IS_FIRST_CLASS_AND_REPLAYABLE
OBSERVED_ZERO != MISSING != VALID_EMPTY != NONCOMPARABLE
DETERMINISTIC_CONTENT_IDENTITY_AND_REPLAY
```

Passing current historical row-shape tests is insufficient if any invariant above fails.
