# DR-R03 — HOSTILE ATTACK PLAN

**Campaign:** `VOZHD_TRII_CORRECTED_UPSTREAM_DOWNSTREAM_REBASE`  
**Target under attack:** accepted R02 candidate direct-DAG topology  
**Execution mode:** six parallel hostile feeders + parallel stage-evidence preparation + one synthesis court  
**Worker base:** use the exact common launch SHA issued by the parent Vozhd; every R03 feeder and evidence-prep branch must share that base.

## 1. Objective

R03 must answer one question:

> Can the R02 direct-DAG topology survive an adversarial whole-machine attack without starving terminal capability, duplicating authority, leaking semantics across ontologies, losing provenance/replay/source identity, or retaining boundaries that do no unique work?

R03 is not a confirmation pass. Every feeder should assume its assigned R02 holding is wrong and try to construct the strongest lawful counterexample.

## 2. Candidate DAG under attack

### Structural temporal class

```text
EmpiricalFact
-> StructuralEmpiricalAdmission
-> V553
-> V554
-> V555
-> V556
-> V557
-> V558
-> ResolvedStructuralContext
-> V3
```

### Structural non-temporal / temporally-complete class

```text
EmpiricalFact
-> StructuralEmpiricalAdmission
-> V554
-> V555
-> V556
-> V557
-> V558
-> ResolvedStructuralContext
-> V3
```

### Reverse possibility class

```text
objective actor fact refs
-> ActorComparabilityService
-> ActorComparatorReceipt
-> EmpiricalQueryEngine / PossibilityFieldService
-> PSEPF
-> V3EmpiricalPossibilityInput
-> V3
```

### Expression class

```text
V3 generated / actor-accessible truth
-> V2
-> application
```

## 3. Attack matrix

| Attack ID | Primary feeder | Target holding | Hostile construction | Required success criterion |
|---|---|---|---|---|
| A01 | R03A | V553 bypass for non-temporal class | Construct an apparently static admission whose lawful V554 use actually requires cross-time comparability, derived interval, temporal noncomparability, or sequence semantics | Either route safely fails closed or R02 boundary is qualified |
| A02 | R03A | V553 required predicate | Construct admission with timestamps/history metadata but no new V553-owned meaning | Prove no-op V553 object is rejected as numbering-only transit |
| A03 | R03A | direct V554 edge | Construct lawful static structural use and remove V553 | No terminal structural meaning/provenance is lost |
| A04 | R03A | dedup/precedence | Feed same proposition through direct admission and V553-temporalized route | Duplicate semantic use is deterministically rejected or unified by exact equivalence identity |
| A05 | R03A | temporal negative authority | Use ambiguous/noncomparable time scopes | No direct-V554 route silently treats unknown comparability as temporal completeness |
| B01 | R03B | V554 necessity | Attempt `StructuralEmpiricalAdmission -> V555` or later | Must expose loss of V554 affordance/applicability semantics or falsify R02 |
| B02 | R03B | V555 necessity | Remove V555 and feed V554 object directly into V556 | Must expose loss of atomic mediator/channel/receiver route semantics or falsify R02 |
| B03 | R03B | V556 necessity | Remove V556 and publish V555 routes directly | Must expose loss of governed cross-route interaction/topology/attractor-prerequisite semantics or falsify R02 |
| B04 | R03B | V557 necessity | Remove V557 and let V558 ingest producer objects | Must expose loss of runtime-use governance/permission narrowing/reference-closure proof or falsify R02 |
| B05 | R03B | V558 necessity | Remove V558 and let V3 resolve producer objects directly | Must expose loss of immutable stage-blind repository/index/resolution boundary or falsify R02 |
| B06 | R03B | no-bloat | Identify any retained stage boundary whose only work is copy/transport/version numbering | Mark as removal/merge candidate for synthesis |
| C01 | R03C | transitive provenance | Remove copied QuerySpec/weight/admission fields from V555/V556 | Exact provenance must remain dereferenceable |
| C02 | R03C | standalone V558 | Package V558 without raw V553-V556 stage directories | Repository must resolve producer refs/content or fail closed with exact missing object |
| C03 | R03C | source universes | Use conflicting source universes and overlapping labels | No silent pooling, collapsing, or respondent-identity inference |
| C04 | R03C | authority versioning | Replay old structural object after authority update | Old object must dereference exact historical authority snapshot |
| C05 | R03C | measure/risk-set provenance | Strip convenience copies and replay from transitive graph | Exact measure/risk-set semantics must remain recoverable where required |
| C06 | R03C | ReplayReceipt status | Attempt to use ReplayReceipt as causal/runtime prior | Must fail as audit/replay-only |
| D01 | R03D | discovery leakage | Feed DiscoveryResultReceipt directly into structural runtime | Must fail without exact EmpiricalFact + StructuralEmpiricalAdmission |
| D02 | R03D | raw empirical leakage | Feed EmpiricalFact directly to V553/V554 | Must fail absent admission |
| D03 | R03D | PSEPF structuralization | Publish PSEPF through V557/V558 structural repository | Must fail type/authority checks |
| D04 | R03D | possibility->psyche | Treat PSEPF mass/rank as actor belief, identity, response, memory, or knowledge | Must fail without V3 developmental causality |
| D05 | R03D | comparator->prior | Use ActorComparatorReceipt as V3 developmental prior | Must fail; receipt is mapping provenance only |
| D06 | R03D | structural context->persona | Feed ResolvedStructuralContext directly to V2/app as voice/persona truth | Must fail; V3 realization remains mandatory |
| D07 | R03D | V557/V558 reownership | Mint semantically rewritten producer copies for publication/resolution | Must expose duplicated authority/divergence risk |
| E01 | R03E | wrapper elimination | Remove V3EmpiricalPossibilityInput and make PSEPF own V3 lifecycle/use/metabolism applicability | Must show ownership leak or prove wrapper redundant |
| E02 | R03E | wrapper bloat | Copy PSEPF cells/geometry into V3EmpiricalPossibilityInput | Must expose duplicate authority/staleness/divergence risk |
| E03 | R03E | lifecycle | Reuse field after actor objective facts or effective time become stale | Must produce typed refresh/stale behavior rather than silent reuse |
| E04 | R03E | negative-state intake | NO_COMPARATOR / AMBIGUOUS / ZERO_SUPPORT / LOW_SUPPORT / NONCOMPARABLE | Must not synthesize nearest cohort/default belief |
| E05 | R03E | divergent lives | Hold PSEPF and ResolvedStructuralContext equal for two actors; vary lawful V3 history | Architecture must permit divergent developed states |
| E06 | R03E | V2 nonconsumption | Attempt direct PSEPF/comparator/source-disagreement personalization in V2/app | Must fail as persona/voice authority |
| F01 | R03F | whole-machine starvation | Trace every D12 terminal service and whole-machine demand through candidate DAG | No capability relies on an object/edge removed by minimality |
| F02 | R03F | minority/plurality | Use supported minority/multimodal/joint empirical geometry | Direct-DAG path must not flatten before V3 possibility use |
| F03 | R03F | source disagreement | Use mutually conflicting but separately lawful universes | Both structural and possibility lanes preserve lawful distinction/negative authority |
| F04 | R03F | world/actor separation | Push structural and empirical priors as hard as possible toward actor state | V3 remains causal realization boundary |
| F05 | R03F | cross-cell contradiction | Independently challenge A-E's most favorable assumptions | Produce explicit conflict ledger for synthesis |

## 4. Feeder output contract

Each R03A-R03F feeder must create under its assigned directory:

1. `RESULT.md`
2. `RESULT.json`
3. `ATTACK_LEDGER.csv`
4. `COUNTEREXAMPLES.md`
5. `SURVIVING_HOLDINGS.csv`
6. `SYNTHESIS_HANDOFF.json`

Minimum `ATTACK_LEDGER.csv` columns:

```text
attack_id
target_r02_holding
constructed_case
required_authority
observed_result
failure_mode
severity
r02_holding_status
required_qualification
stage_close_read_dependency
evidence
```

Every attack must end in one of:

- `SURVIVES`
- `SURVIVES_WITH_QUALIFICATION`
- `FALSIFIED`
- `BLOCKED_MISSING_AUTHORITY`
- `DEFER_TO_STAGE_CLOSE_READ`

No blank or rhetorical attack rows.

## 5. R03A plan — temporal routing

R03A must build an explicit truth table over at least these dimensions:

- single-time snapshot;
- governed effective interval already present;
- interval requires derivation;
- cross-wave comparison;
- cross-source time equivalence;
- persistence/drift/change/reversal/rupture request;
- temporal noncomparability;
- missing/ambiguous time authority;
- same proposition available both direct and temporalized.

The return must produce a proposed finite routing predicate suitable for later V553/V554 close-reads, but that predicate remains non-dispositive until synthesis.

## 6. R03B plan — stage necessity

For each V554-V558 stage:

1. remove it conceptually;
2. route lawful producer objects to the next consumer;
3. list every lost semantic or governance operation;
4. distinguish real semantic loss from serialization/implementation inconvenience;
5. attempt a minimal substitute using direct earlier authority;
6. if substitute is sufficient, mark the boundary as a genuine removal/merge candidate.

R03B must not preserve a stage because its current implementation already exists.

## 7. R03C plan — provenance and source plurality

R03C must construct at least:

- one multi-universe conflicting-source fixture;
- one historical-authority-version replay fixture;
- one standalone V558 closure fixture with raw stage dirs absent;
- one transitive measure/query/admission dereference fixture;
- one broken/missing-content-addressed-ref fixture;
- one attempted cross-universe respondent join without authority.

The court must state exactly which reference classes must be physically present in the standalone repository and which may be transitively dereferenced from immutable objects.

## 8. R03D plan — ontology leakage

R03D uses hostile type confusion.

For every source object, attempt every tempting illicit promotion:

```text
DiscoveryResultReceipt -> structural fact
EmpiricalFact -> structural fact
StructuralEmpiricalAdmission -> generated actor position
PSEPF -> actor disposition/belief
ActorComparatorReceipt -> actor prior
ReplayReceipt -> causal input
ResolvedStructuralContext -> V2 persona/voice
```

For each, identify the exact boundary/authority that must reject it. If rejection depends only on prose rather than a typed/authority seam, flag `NEGATIVE_AUTHORITY_HARDENING_REQUIRED`.

## 9. R03E plan — V3 boundary

R03E must treat the PSEPF as immutable upstream evidence and ask what V3-specific semantics are impossible to place lawfully elsewhere.

The thin wrapper survives only if it uniquely owns at least:

- actor/decision binding;
- V3 effective/use time;
- lifecycle/current/stale/refresh-required state;
- metabolism authority applicability;
- typed intake-negative state;
- replay/intake identity.

It must not own empirical field geometry or comparator semantics.

R03E must also prove that equal upstream priors do not imply equal developed actors.

## 10. R03F plan — independent checksum

R03F must not specialize in one stage. It must read the terminal-demand/whole-machine authority and trace end-to-end capability.

Its return should contain:

- terminal capability -> required upstream object -> direct/transformed edges -> final consumer;
- starvation point if any;
- bloat/duplication point if any;
- cross-cell contradiction with R03A-E if any.

R03F is the insurance policy against all specialist feeders sharing the same blind spot.

## 11. Concurrent stage-evidence preparation plan

Run these in parallel with R03A-F:

### EP553
Focus: current temporal families, adapters, V552/V552J compatibility, temporal key/observation/relation/limit schemas, tests.

### EP554
Focus: affordance rule registry, eligible basis classes, direct-DAG intake capability, rule signatures, precedence/dedup machinery, tests.

### EP555
Focus: one-F1 route grain, mediator/channel/receiver semantics, reference contract, tests.

### EP556
Focus: route-ID base edges, interaction/topology/attractor prerequisites, transitive-reference handling, tests.

### EP5578
Focus: publication/use governance, monotone permission narrowing, mixed-producer references, standalone repository/index/resolver, referential closure, tests.

### EPV3
Focus: objective actor fact authorities, current upstream intake, event-sourced lifecycle, developmental proposal/state-transition ownership, replay, V2 render boundary, tests.

Each evidence cell returns only facts and unresolved seams.

## 12. R03 synthesis plan

After all six hostile feeders return:

1. build `R02_HOLDING_ADJUDICATION_MATRIX.csv` for H01-H10;
2. build `ATTACK_CONFLICT_LEDGER.csv` where feeders disagree;
3. adjudicate every R02 edge as:
   - `SURVIVES`
   - `SURVIVES_WITH_QUALIFICATION`
   - `REMOVED`
   - `ADDED`
   - `UNRESOLVED_FOR_STAGE_CLOSE_READ`;
4. publish one candidate whole-machine broad DAG;
5. publish exact stage-close-read questions;
6. use stage evidence packs to avoid rediscovery, but do not let evidence-pack recommendations bind architecture;
7. issue a parallelized close-read campaign with explicit seam barriers rather than historical stage sequence.

R03 synthesis passes only if every material attack is dispositioned and no contradiction is silently averaged away.

## 13. Expected close-read parallelization after R03

Subject to R03 synthesis, the default next wave should be:

```text
                    R03 SYNTHESIS
                         |
          +--------------+--------------+
          |                             |
   STRUCTURAL CHAMBER             DEVELOPMENTAL CHAMBER
          |                             |
    V553 + V554 seam               V3 intake/boundary
          |                             |
   V555 and V556 where            V2 negative boundary
   inputs permit parallel                |
          |                             |
      V557/V558 --------------------------+
          |
          v
       WHOLE-MACHINE CLOSURE
```

The exact close-read dependency graph is a synthesis output; do not hard-code unnecessary serialization now.

## 14. Stop conditions

R03 synthesis returns one of:

`HOSTILE_BROAD_DAG_CLOSED__STAGE_CLOSE_READS_READY`

or

`HOSTILE_BROAD_DAG_FAILED__EXACT_REOPEN_OR_MISSING_AUTHORITY_REQUIRED`

If a feeder is permanently blocked, preserve the blocked fact and let synthesis decide whether the unknown prevents broad closure. Do not wait indefinitely or invent evidence.
