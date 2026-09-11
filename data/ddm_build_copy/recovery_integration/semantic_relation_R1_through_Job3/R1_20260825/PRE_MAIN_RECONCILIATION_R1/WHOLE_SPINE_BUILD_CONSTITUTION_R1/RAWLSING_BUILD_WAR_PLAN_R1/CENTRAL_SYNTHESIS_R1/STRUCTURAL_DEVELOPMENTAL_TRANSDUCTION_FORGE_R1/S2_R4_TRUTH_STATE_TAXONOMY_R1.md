# S2 R4 TRUTH STATE TAXONOMY R1

STATUS: `S2_R4_TRUTH_STATE_TAXONOMY_COMPLETE`

WORKER: `agent/rabochii-sdtf-r1-r4-s2-truth-state-negation`

COMMISSIONED COORDINATOR STATE: `02d4a75c030ed22da48b64718618242fc10ad858`

FROZEN R4 TARGET: `dfd935f77554ff5c177eeddeef50a9aba8ab46e8`

SCOPE: PRE-V3 -> D1' -> V3 objective truth semantics only. No runtime implementation, no OBL062 solution, no D2/D3/D4/P6.

## 1. Court result

The eight proposed categories A-H are not eight peer truth states. They mix four different semantic axes. Treating them as one flat enumeration would itself cause false actor biography because `UNKNOWN`, `HISTORICAL`, `NEGATIVE`, and `PROJECTED` answer different questions from assertion kind.

The minimum proof-bearing assertion-kind set is:

```text
K1 CONSTITUTIVE_POSITIONAL
K2 QUALIFIED_POSSIBILITY
K3 REALIZED_OCCURRENCE
K4 ACTIVE_DURATIVE
```

Those kinds are qualified by three orthogonal axes and one adjudication outcome:

```text
POLARITY:       POSITIVE | NEGATIVE
CURRENTNESS:   CURRENT | HISTORICAL_NONCURRENT
MODALITY:      ACTUAL | PROJECTED_COUNTERFACTUAL
EPISTEMIC:     PROVEN | UNKNOWN_NOT_PROVEN
```

`UNKNOWN_NOT_PROVEN` is not an objective actor fact. It is the result of failing to earn a positive or negative assertion at the requested grain.

`HISTORICAL_NONCURRENT` is not a fifth mechanism or truth kind. It is lifecycle status of a once-lawful fact.

`NEGATIVE` is not a special realization stage. It is polarity and must satisfy its own proof law.

`PROJECTED_COUNTERFACTUAL` is not current biography. It is a scenario-bound derivation under a nonactual antecedent.

## 2. Proposed A-H disposition

| Proposed category | S2 disposition | Reason |
|---|---|---|
| A. constitutive/deontic/positional fact | `KEEP AS K1` | truth can be constituted by an operative competent rule/state plus exact position; occurrence proof is not required |
| B. qualified possibility/applicability/reachability | `KEEP AS K2` | applicability/reachability truth is distinct from constitutive duty/right and from use/realization |
| C. contingent realized occurrence/treatment/transfer | `KEEP AS K3` | requires event/treatment/transfer/exercise evidence at the corresponding grain |
| D. resultant active state/relation/condition | `KEEP AS K4` | current durative truth requires interval/currentness proof distinct from the initiating event |
| E. historical/terminated/superseded fact | `MOVE TO CURRENTNESS/LIFECYCLE AXIS` | an occurrence can remain historically true after any resultant condition ends; termination does not create a new truth kind |
| F. unknown/not-proven | `MOVE OUTSIDE FACT ONTOLOGY` | no actor fact is licensed; it is an adjudication result |
| G. explicit negative | `MOVE TO POLARITY AXIS` | proof rules differ from positive absence; negative can apply to multiple assertion kinds |
| H. counterfactual/projected | `MOVE TO MODALITY AXIS` | hypothetical truth must remain scenario-bound and noncurrent |

## 3. Minimum semantic tuple

S2 does not mandate a runtime schema. At the semantic seam, a sufficiently explicit fact must preserve the applicable subset of:

```text
ACTOR_REF
WORLD_REF
CONTEXT_REF(S)
POSITION_REF(S)
CONSEQUENCE_TYPE
ASSERTION_KIND = K1 | K2 | K3 | K4
POLARITY = POSITIVE | NEGATIVE
MODALITY = ACTUAL | PROJECTED_COUNTERFACTUAL
VALID_FROM
VALID_TO_OR_OPEN
CURRENTNESS = CURRENT | HISTORICAL_NONCURRENT
LIFECYCLE_CLOSE_REASON where noncurrent
MECHANISM_RULE_REF(S)
SOURCE / WITNESS / PROOF_BUNDLE_REF(S)
COUNTERPART / INSTITUTION REF(S) where applicable
OBJECTIVE_SOCIAL_HISTORY_REF(S) where applicable
DERIVATION_PROVENANCE
BOUNDARY_CONDITIONS
EVIDENCE_CEILING
NEGATIVE_CEILING
```

`UNKNOWN_NOT_PROVEN` is returned by adjudication and MUST NOT populate this tuple as though it were an actor fact.

## 4. Mandatory noncollapses

S2 affirms all required noncollapses:

```text
RULE VALID                         != ACTOR QUALIFIED
ACTOR QUALIFIED                    != REALIZED
CONSTITUTIVE RIGHT/DUTY            != EXERCISED/ENFORCED RIGHT/DUTY
ROUTE AVAILABLE                    != ROUTE USED
CHANNEL EXISTS                     != TRANSFER
EVENT OCCURRED                     != RESULTING CONDITION STILL CURRENT
HISTORICAL FACT                    != ACTIVE FACT
MISSING POSITIVE EVIDENCE          != NEGATIVE
EXPIRED POSITIVE WITNESS           != NEGATIVE
NEGATIVE                           != UNKNOWN
COUNTERFACTUAL                     != CURRENT
OBJECTIVE FACT                     != SUBJECTIVE UPTAKE
```

Additional binding distinctions:

```text
TERMINATED                         != NEVER EXISTED
SUPERSEDED                         != FALSE AT ALL PRIOR TIMES
INVALIDATED PROOF                  != PROVED OPPOSITE
DENIAL                             != NO DECISION RECORD
NO CURRENT PROOF                   != PROVED CURRENT ABSENCE
```

## 5. P1-P5 seam examples

### P1 material access/dependency

- `entitled to benefit` -> K1 if competent operative entitlement rule plus exact actor position makes entitlement true;
- `benefit is available/applicable` -> K2;
- `payment received` -> K3;
- `currently dependent on wage` -> K4 if the dependency condition is currently proved;
- `no current evidence of payment` -> `UNKNOWN_NOT_PROVEN` for receipt unless negative/closed-world law is satisfied;
- `explicit benefit denial` -> negative K3/K4 according to the denial's exact semantics and interval.

### P2 authority/obligation/sanction

- `formally has authority` / `owes obligation` -> K1;
- `authority relation applicable to this actor/counterpart` -> K2 where qualification is the proposition at issue;
- `authority exercised`, `sanction imposed`, `command issued` -> K3;
- `authority relation operative/current` -> K4 unless the operative source-owned relation itself constitutes K1 truth at the queried grain;
- `obligation terminated` closes current K1/K4 interval but does not erase historical truth or prove the opposite duty.

### P3 organized activity/time

- `activity available` -> K2;
- `activity required` -> K1 when the requirement is constitutive;
- `activity scheduled` -> K2 or K1 depending on whether the competent schedule itself constitutes the objective obligation/state claimed;
- `activity performed` -> K3;
- `recurrent participation current` -> K4;
- `prior recurrent activity now ceased` -> historical K4 plus termination provenance, not current activity.

### P4 gate/treatment

- `gate applies` -> K2;
- `application submitted`, `cue presented`, `recognition occurred`, `decision rendered` -> K3 at their exact separate grains;
- `treatment negative` -> negative K3 if explicitly rendered/recorded;
- `no decision record` -> UNKNOWN unless the exact closed-world negative law is licensed.

### P5 counterpart/channel/relation

- `counterpart reachable`, `channel available` -> K2;
- `tie exists` -> K1 or K4 according to whether the competent relation/state constitutively establishes the tie and its interval;
- `contact occurred`, `information/support transferred` -> K3;
- `tie/contact/support relation remains active` -> K4 where a durative claim is made;
- `transfer perceived as support` is downstream person-side and is not a D1' objective assertion kind.

## 6. Why K1-K4 cannot collapse

K1 and K2 differ because an operative rule can make a duty/right/relation true while a route or eligibility merely makes a contingent consequence possible/applicable.

K2 and K3 differ because applicability/reachability does not establish occurrence, treatment, transfer, performance, receipt, or use.

K3 and K4 differ because an occurrence can be historically true after any resulting state has ended; current state proof is interval-sensitive.

K1 and K4 may sometimes share a source-owned operative state, but they remain semantically distinguishable whenever the proposition is `the rule/position constitutes X` versus `a resulting social condition remains active`. They may use the same evidence object under different governed proof rules; that is not a reason to collapse the kinds.

## 7. No fifth or sixth seam primitive

Historical status, negative polarity, projection, and unknown do not add mechanism classes. They refine truth adjudication around D1' and P1-P5.

S2 therefore changes no R4 topology:

```text
KEEP D1' OBJECTIVE_POSITIONED_SOCIAL_CONSEQUENCE_DERIVATION
KEEP P1-P5 UNCHANGED
DO NOT CREATE D2 / D3 / D4 / P6
```

## Terminal

`MINIMUM_TRUTH_GRAMMAR_IS_FOUR_ASSERTION_KINDS_PLUS_ORTHOGONAL_POLARITY_CURRENTNESS_MODALITY_AND_EPISTEMIC_ADJUDICATION__NO_TOPOLOGY_EXPANSION`
