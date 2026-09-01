# QIMPL → RESPONDENT BINDING TRACE

## Bounded trace object

Family: `Afrobarometer`
Wave: `R5`
Current question implementation: `question_impl.phase0.391123a4e7d3c8f0fd3b`
Raw variable: `Q73D`
Current routing disposition: `POSITIVE_EXECUTABLE_ROUTING_AUTHORITY`
Predicate: `C04P.f751f53c113a339f2cb8`
Compiled predicate: `COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN} AND RESPONDENT_HAS_PAID_EMPLOYMENT == True`
Source evidence grade: `NATIVE_PRIMARY`

## Arrow court

| Arrow | Required proof | Result | Exact reason |
|---|---|---|---|
| 1 | CURRENT qimpl identity | PASS | exact `question_impl.phase0.391123a4e7d3c8f0fd3b` exists on the current routing surface |
| 2 | qimpl → exact source implementation | PASS | Contract@2/current source backreference fixes Afrobarometer / R5 / Q73D |
| 3 | exact source implementation → CURRENT respondent carrier measurement | **FAIL** | no currently authorized respondent-grain carrier/column identity was proved |
| 4 | measurement → exact respondent key | **FAIL** | no current respondent carrier means no current respondent-key owner can be established for this row |
| 5 | respondent key → exact row source/wave/country/form/split identity | **FAIL** | Contract@2 has source-level scope identity, not a current respondent-row identity carrier |
| 6 | qimpl → exact routing predicate | PASS | predicate `C04P.f751f53c113a339f2cb8` is exact and deterministic at specification grain |
| 7 | predicate fields → actual respondent input values | **FAIL** | current predicate specification names `COUNTRY_ALPHA3` and `RESPONDENT_HAS_PAID_EMPLOYMENT`; no governed respondent input carrier is identity-bound to them |
| 8 | deterministic predicate execution on actual respondent | **BLOCKED BY 3/7** | synthetic/replay predicate validity is not execution on a governed respondent row |
| 9 | predicate truth → actual measurement exposure/opportunity | **NOT PROVED** | exposure cannot be inferred from response, source presence, or routing-spec existence |
| 10 | exposure → response value/state | **NOT REACHED** | response state is separately downstream of exposure |

## First broken arrow

`CURRENT_SOURCE_IMPLEMENTATION → CURRENT_RESPONDENT_CARRIER_MEASUREMENT`

Typed seam:

`CURRENT_RESPONDENT_CARRIER_NOT_CANONICALLY_REACHABLE`

The trace deliberately does not infer that Q73D was unasked, missing, unanswered, or empirically absent for any historical respondent. It proves only that current Rawlsing authority does not presently furnish the row-level identity bridge required for FIELD FORGE respondent execution.
