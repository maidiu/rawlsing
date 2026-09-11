# S2 R4 CURRENTNESS SUPERSESSION TRANSITION COURT R1

STATUS: `S2_R4_CURRENTNESS_SUPERSESSION_TRANSITION_COURT_COMPLETE`

FROZEN R4 TARGET: `dfd935f77554ff5c177eeddeef50a9aba8ab46e8`

## 1. Scope

This court specifies only truth/currentness lifecycle semantics necessary to determine whether a D1' objective fact is current, historical, unknown, or projected. It creates no D2 and no independent temporal/life-course owner.

## 2. Core currentness law

For any actual fact F at query time q:

```text
CURRENT(F,q)
requires
  proof law for F's ASSERTION_KIND satisfied
  AND q within the fact's lawfully established validity interval
  AND no competent closing/superseding/invalidating fact defeats currentness
  AND any required freshness/recurrence/persistence conditions are satisfied.
```

If currentness cannot be established:

```text
DO NOT CARRY FORWARD F
DO NOT FLIP F NEGATIVE
RETURN UNKNOWN_NOT_PROVEN_CURRENT
```

unless a competent lifecycle witness independently proves historical closure/noncurrentness.

## 3. Lifecycle operation matrix

| Operation | K1 constitutive/positional | K2 qualified possibility | K3 realized occurrence | K4 active durative |
|---|---|---|---|---|
| `VALID_FROM` | starts operative rule/position truth when all applicability conditions hold | starts qualified applicability/reachability interval | event time/start of occurrence | starts active condition/relation/activity interval when establishment proof succeeds |
| `VALID_TO` | closes constitutive applicability at boundary | closes qualification at boundary | bounds occurrence if durative event; event remains historical | closes active interval; later current assertion requires new/re-established proof |
| `EXPIRY` | expires rule/source/status support; does not prove opposite | expires qualification support | does not erase event already competently proved; may expire provisional event evidence if evidence semantics so state | ends support/currentness unless separate lawful persistence proof exists; never implies negative by itself |
| `SUPERSESSION` | successor rule/state controls prospectively according to competent precedence | successor route/gate/configuration controls prospectively | later record may correct/supersede event interpretation if owner law authorizes; preserve provenance | prior state no longer sustains currentness after successor takes effect |
| `TERMINATION` | closes duty/right/relation when exact source semantics make termination operative | may close eligibility/route applicability | termination itself can be a K3 event | explicitly closes K4 state/relation/activity interval |
| `INVALIDATION` | removes invalid basis according to source law; do not infer opposite | removes qualification basis | may retract unsupported/corrupt event claim; do not infer non-occurrence unless separately proved | removes current proof; current result becomes unknown unless separate proof exists |
| `NEW WITNESS` | may refresh/confirm or establish successor version | may refresh qualification/currentness | adds/updates occurrence evidence | can refresh, extend, re-establish, or close currentness according to governing rule |
| `RULE CHANGE` | re-evaluate K1 under new operative rule; old fact becomes historical if prior interval remains valid | re-evaluate applicability; do not auto-promote/demote realization | does not retroactively erase a valid historical occurrence absent explicit retroactive authority | may close/alter active state if rule constitutes it; otherwise state owner semantics control |
| `POSITION CHANGE` | close/re-evaluate position-dependent K1 | close/re-evaluate actor qualification | historical occurrence remains historical | close/re-evaluate position-dependent K4; derive new state only from new lawful inputs |
| `TRANSITION` | treat as externally admitted change that may close old bindings and require fresh derivation | invalidate/rebind qualifications affected by changed context/position | transition event can be K3 only if competently witnessed | close/rebind affected current states; do not create downstream development or D2 |

## 4. Historical truth law

A fact may be historically true while noncurrent.

```text
HISTORICAL(F) means:
  F was lawfully true/realized for a prior exact time/interval,
  and the historical proof has not itself been invalidated.
```

Examples:

- a payment occurred last month but no current payment is proved;
- an authority relation existed before transfer;
- a recurrent activity was active during a prior interval and has ceased;
- an application was rejected at a past gate decision;
- a benefit entitlement existed under an earlier rule.

Historical truth must retain its original polarity and interval. It cannot be promoted to current merely because it remains in history.

## 5. Stale-fact prevention

Every current query must be evaluated against the current lifecycle boundary. Implementational caching is outside S2, but semantically no cached actor fact can outrank its proof/currentness contract.

Binding rule:

```text
PRIOR POSITIVE FACT
+ LATER TIME
!= CURRENT POSITIVE FACT
```

unless currentness is established by:

1. a direct current witness; or
2. a governed persistence-to-termination proof satisfying S2's strict K4-B law; or
3. for K1/K2, continuing operative rule/state/applicability proof over the query time.

## 6. Supersession law

Supersession requires competent owner semantics identifying which prior fact/rule/state is displaced and from what time.

A successor fact must not silently rewrite prior intervals unless the competent source explicitly carries retroactive correction authority.

Default:

```text
OLD FACT valid [a,b)
NEW SUPERSEDING FACT valid [b,...)
```

not:

```text
NEW FACT was always true
```

Unresolved precedence among competent sources yields `UNKNOWN_NOT_PROVEN` at the disputed grain.

## 7. Rule change and actor fact change are separate

```text
CONSTITUTION CURRENT
!= MECHANISM RULE CURRENT
!= RULE APPLICATION CURRENT
!= ACTOR FACT CURRENT
```

A new rule can require re-derivation without proving that a contingent event occurred. A continuing rule cannot extend a stale event witness. A rule repeal can close a constitutive entitlement/duty if the rule constitutes that fact, but it does not erase receipts, decisions, contacts, or performances that historically occurred.

## 8. Position/context transition law

When an externally grounded position/context transition occurs:

```text
1. identify current facts whose proof depends on the changed position/context;
2. close or mark noncurrent those whose validity no longer survives;
3. preserve historically valid prior intervals;
4. bind the new position/context;
5. re-run ordinary D1' derivation under current competent rules and sources;
6. do not auto-flip polarity;
7. do not infer subjective response or durable development.
```

This is lifecycle invalidation/rederivation, not D2.

## 9. Counterfactual lifecycle firewall

Projected facts carry:

```text
PROJECTED_COUNTERFACTUAL
SCENARIO_REF
NONACTUAL_ANTECEDENT(S)
PROJECTION_HORIZON
RULE/SOURCE PROVENANCE
```

They are never marked `CURRENT` in ordinary actor biography.

Example:

```text
IF actor entered position X,
THEN under current rule R actor would have obligation Y.
```

Lawful output:

```text
PROJECTED_COUNTERFACTUAL(K1 obligation Y | position X)
```

Unlawful output:

```text
CURRENT_ACTUAL(K1 obligation Y)
```

If position X later becomes actual, the system MUST perform a fresh actual derivation against the then-current rule, source, position, context and time. A prior projection is evidence of neither actual entry nor current obligation.

## 10. Negative currentness

Negative facts are interval-bound too. An explicit denial, unavailability, no-current-obligation fact, or other negative does not persist forever merely because no later positive appears.

It must satisfy its own currentness/persistence law. Expiry of a negative proof yields unknown, not positive.

## Terminal

`CURRENTNESS_IS_ASSERTION_KIND_SPECIFIC_AND_INTERVAL_BOUND__SUPERSESSION_TERMINATION_INVALIDATION_CLOSE_OR_REMOVE_CURRENT_SUPPORT_WITHOUT_POLARITY_FLIP__TRANSITIONS_TRIGGER_REDERIVATION_NOT_D2__COUNTERFACTUAL_NEVER_PROMOTES_TO_CURRENT`
