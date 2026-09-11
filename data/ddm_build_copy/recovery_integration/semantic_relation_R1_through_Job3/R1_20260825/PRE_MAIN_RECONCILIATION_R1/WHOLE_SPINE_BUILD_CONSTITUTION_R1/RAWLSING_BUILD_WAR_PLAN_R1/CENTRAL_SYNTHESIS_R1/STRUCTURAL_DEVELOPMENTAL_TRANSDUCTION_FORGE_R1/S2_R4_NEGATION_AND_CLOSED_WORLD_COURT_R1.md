# S2 R4 NEGATION AND CLOSED WORLD COURT R1

STATUS: `S2_R4_NEGATION_CLOSED_WORLD_COURT_COMPLETE`

FROZEN R4 TARGET: `dfd935f77554ff5c177eeddeef50a9aba8ab46e8`

## 1. Governing polarity law

S2 preserves the final R3 review correction without dilution:

```text
NO POSITIVE EVIDENCE != NEGATIVE EVIDENCE
MISSING POSITIVE WITNESS != DENIAL
EXPIRED POSITIVE WITNESS != NON-OCCURRENCE
SUPERSEDED POSITIVE WITNESS != NEGATIVE
INVALIDATED PROOF != PROVED OPPOSITE
```

A negative actor fact is licensed only by one of three routes:

1. explicit competent negative evidence;
2. an explicit competent denial/rejection/termination/non-occurrence witness whose semantics actually prove the negative proposition claimed;
3. a provenance-bearing, rule-authorized closed-world negative inference at the exact grain.

Failure of positive proof alone yields `UNKNOWN_NOT_PROVEN`.

## 2. Explicit negative proof

Examples of direct negative proof can include, when source semantics are competent and exact:

```text
BENEFIT_DENIED
APPLICATION_REJECTED
PAYMENT_VOIDED_OR_NOT_ISSUED
CONTACT_ATTEMPT_FAILED_WITH_EXACT_NONCONTACT_SEMANTICS
TASK_CANCELLED
OBLIGATION_TERMINATED
CHANNEL_UNAVAILABLE
```

The negative proposition must not be broader than the witness.

Examples:

```text
APPLICATION_REJECTED
!= ACTOR NEVER APPLIED

OBLIGATION_TERMINATED AT t
!= ACTOR NEVER HAD THE OBLIGATION

PAYMENT NOT ISSUED FOR PERIOD p
!= ACTOR HAS NEVER RECEIVED BENEFIT

CHANNEL UNAVAILABLE DURING i
!= NO RELATION EXISTS
```

## 3. Closed-world negative prerequisites

Absence of a positive record may become negative truth only if **all** applicable conditions below are proved:

1. **competent owner** — the source is authoritative for the exact proposition/event/state type;
2. **exact grain** — actor, counterpart/institution, context, event/state type, and queried time/interval are exactly scoped;
3. **complete universe declaration** — the competent owner explicitly establishes that all positive instances at that grain are obligatorily represented in the queried universe;
4. **full temporal coverage** — the source covers the entire interval relevant to the claim;
5. **reconciliation closure** — posting, ingestion, reporting, appeal, correction, or other owner-defined latency has closed for the queried interval;
6. **identity integrity** — actor/counterpart/entity keys are resolved without material ambiguity;
7. **channel closure** — either no lawful alternate channel exists outside the governed source universe, or the emitted negative is explicitly restricted to that source-bounded universe;
8. **absence-to-negative authorization** — the current governed rule explicitly authorizes this closed-world inference for the exact proposition;
9. **no source gap** — no outage, partial extract, known reporting omission, retention truncation, data-loss interval, or other coverage defect intersects the query;
10. **current source/rule version** — the completeness and negative semantics are valid for the relevant historical interval;
11. **provenance** — the derived negative carries source, rule/version, query grain, coverage interval, reconciliation state, and closed-world basis.

If any required condition fails:

```text
NO RECORD -> UNKNOWN_NOT_PROVEN
```

not negative biography.

## 4. Seven no-record tests

| Query | Default S2 result | When explicit negative can be licensed |
|---|---|---|
| `NO PAYMENT RECORD` | `UNKNOWN` | authoritative exhaustive payroll/benefit ledger for exact actor, payment type and period; all issuance/receipt records mandatory; reconciliation closed; no alternate payment channel or negative explicitly source-scoped |
| `NO CALLBACK RECORD` | `UNKNOWN` | only if callback obligations/results are exhaustively logged in a competent closed system for the exact request/window and all alternate channels are excluded or scoped away |
| `NO CONTACT RECORD` | `UNKNOWN` | only under mandatory exhaustive contact logging for the exact actors/channel/interval; ordinary relationship/contact data are not closed world |
| `NO COMMAND RECORD` | `UNKNOWN` | only if the authoritative system requires every command of the claimed type to be recorded and the actor/scope/interval is complete; informal/off-system command possibility otherwise defeats closure |
| `NO TASK RECORD` | `UNKNOWN` | only if the source is the exhaustive authoritative task-assignment/performance system at the exact claimed grain and reporting is complete |
| `NO SUPPORT RECORD` | `UNKNOWN` | ordinarily remains unknown because support can be informal/off-ledger; at most a narrower `NO_PROGRAM_RECORDED_SUPPORT_TRANSACTION` may be licensed by an exhaustive program ledger |
| `NO APPLICATION RECORD` | `UNKNOWN` until closure proved | may become `NO_APPLICATION_SUBMITTED_IN_THIS_GATE_UNIVERSE` when official intake is exhaustive, actor identity exact, submission window and late-ingest period closed, and alternate submission channels are absent/included |

## 5. Negative polarity across assertion kinds

Negative polarity does not erase assertion kind.

Examples:

```text
K1 NEGATIVE: actor is not entitled under an explicit competent exclusion/operative status rule
K2 NEGATIVE: route is explicitly unavailable / gate explicitly does not apply at the queried grain
K3 NEGATIVE: application explicitly rejected / payment explicitly not issued / contact explicitly failed where source semantics prove non-occurrence
K4 NEGATIVE: relation/condition is explicitly inactive or terminated for the queried interval
```

S2 does not require every domain to support every negative form. The governing rule must authorize the exact negative output type.

## 6. Termination is lifecycle closure, not unrestricted negation

A termination witness proves that a prior/current fact ceased according to its exact semantics. It supports:

```text
FACT F WAS CURRENT BEFORE t
FACT F IS NOT CURRENT AFTER t, subject to exact closure semantics
```

It does not automatically prove:

```text
OPPOSITE(F) IS CURRENT
F NEVER EXISTED
NO RELATED FACT EXISTS
```

Thus `OBLIGATION_TERMINATED` closes the obligation interval; it does not by itself create a new opposite obligation.

## 7. Expiry and supersession

Expiry, supersession, or invalidation of positive proof can remove current support. They never create negative polarity by themselves.

```text
EXPIRED POSITIVE WITNESS -> UNKNOWN CURRENTNESS unless separate lawful closure/currentness proof exists
SUPERSEDED POSITIVE WITNESS -> follow competent successor/supersession law; if unresolved, UNKNOWN
INVALIDATED POSITIVE WITNESS -> retract unsupported assertion; do not emit opposite
```

Historical truth is retained only to the extent its historical proof remains valid.

## 8. Unknown law

S2 requires `UNKNOWN_NOT_PROVEN` whenever the requested proposition is not positively or negatively earned at the exact grain, including:

- missing positive evidence with no closed-world authority;
- stale/expired evidence with no lawful currentness proof;
- partial interval coverage;
- source outage or incomplete extract;
- unresolved identity or actor/position/context binding;
- unresolved conflict among competent sources;
- unknown rule applicability;
- unknown closure/reconciliation status;
- an unfulfilled counterfactual antecedent queried as current fact;
- data retention limits that make absence ambiguous;
- any case where the negative proposition is broader than the negative witness.

`UNKNOWN_NOT_PROVEN` is epistemic restraint. It is not a fact to be sent downstream as though the actor objectively possesses an `unknown` social condition.

## 9. Sparse-data firewall

No domain may silently switch to closed-world reasoning because data are sparse, structured, tabular, institutional, or machine-readable.

A missing row, null cell, zero count, absent event token, or expired witness has no negative actor semantics unless the exact governed closed-world contract supplies them.

## 10. Negative facts and V3

A lawfully proved objective negative can be an objective social fact within D1' only at its exact grain. It does not imply actor awareness, felt deprivation, appraisal, motive, response, or learning.

```text
OBJECTIVE BENEFIT DENIAL != ACTOR KNOWS DENIAL
NO TRANSFER PROVED != FELT UNSUPPORTED
APPLICATION REJECTED != APPRAISAL OF REJECTION
TERMINATED AUTHORITY != SUBJECTIVE LOSS OF CONTROL
```

Any downstream ingress remains governed by existing V3 boundaries and the open non-event ingress dependency.

## Terminal

`NEGATIVE_TRUTH_REQUIRES_EXPLICIT_COMPETENT_NEGATIVE_PROOF_OR_EXACT_RULE_AUTHORIZED_CLOSED_WORLD_COMPLETENESS__ALL_OTHER_ABSENCE_REMAINS_UNKNOWN__SPARSE_DATA_NEVER_BECOMES_BIOGRAPHY`
