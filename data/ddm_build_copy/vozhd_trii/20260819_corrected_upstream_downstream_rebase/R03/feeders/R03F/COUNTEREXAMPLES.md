# R03F — WHOLE-DAG TERMINAL STARVATION / CROSS-CELL CHECKSUM COUNTEREXAMPLES

**Court:** Rabochii R03F  
**Repository:** `maidiu/rawlsing`  
**Common launch/base SHA:** `138ded52ae6c7d26e9a3671e39d779965b5dc6f4`  
**Branch:** `agent/vozhd-trii-dr-r03f-terminal-starvation-audit`  
**Authority posture:** non-dispositive feeder; no final architecture selection; D15 upstream remains frozen.

## 1. Terminal-service dead-end counterexample

The R02 DAG is easiest to read as a path toward V3. That reading is unsafe for autonomous discovery.

Construct a minimality pass that removes every object with no downstream runtime consumer. `DiscoveryResultReceipt` then appears to be a dead end because a discovery result does not automatically enter V553-V558 or V3.

That removal starves a D12 terminal service. Autonomous forward social discovery is itself a terminal capability, and its lawful consumers include authoring, branch continuation, replay and separately governed later query/admission flows. It does not need a V3 runtime edge to justify existence.

**Checksum ruling:** R02 survives only if `NO_DOWNSTREAM_RUNTIME_CONSUMER_REQUIRED` is never treated as `NO_TERMINAL_CONSUMER` or retirement authority.

## 2. Later-use temporal-demand counterexample

Start with a lawful direct-V554 admission:

```text
admission A
= exact static/source-time structural proposition
= temporally complete for V554 use U1

A -> V554 -> V555 route R1
```

Now a later V556 rule U2 attempts to relate R1 to a route whose evidence belongs to another governed time/source and claims persistence, reversal, sequence or a cross-time interaction.

The original direct V554 route was lawful for U1. It does not follow that A is globally exempt from V553 forever. The later use U2 creates a new temporal/comparability demand.

**Checksum ruling:** the V553-bypass predicate must be scoped to the governed downstream use chain. If later use requires V553-owned meaning, that use must consume a lawfully temporalized/comparable proposition or fail closed. A stage may not infer cross-time meaning merely because an earlier static use bypassed V553.

## 3. Minority / exact joint geometry counterexample

Let conditioner `C` select 37 respondents in one exact universe. For target tuple `(Q1,Q2,Q3)`, configuration `001` is observed with low support. Unary and pairwise marginals are compatible with more than one possible three-way distribution.

Any downstream optimization that keeps only:

- a modal cell;
- top-k cells;
- unary marginals;
- pairwise marginals;
- an independent-product approximation; or
- a scalar association score

can erase or misstate the supported minority configuration.

R02's thin `V3EmpiricalPossibilityInput` is lawful only because the exact PSEPF remains immutable and dereferenceable. Thin boundary does not mean thin empirical meaning.

**Checksum ruling:** V3 must be able to consume the complete exact requested field geometry. `LOW_SUPPORT`, `OBSERVED_ZERO`, `ZERO_SUPPORT`, `TARGET_UNAVAILABLE`, and semantic absence remain different states.

## 4. Mixed-source state counterexample

For one actor/query:

- `U1` produces a supported source component;
- `U2` produces a conflicting supported component;
- `U3` is `TEMPORAL_NONCOMPARABLE`.

A one-bit or one-enum wrapper state such as `AVAILABLE` or `NO_FIELD` destroys the source-indexed structure. A single numeric mixture destroys it even more strongly.

Frozen D15 law makes disagreement information and composition `NONE_BY_DEFAULT`.

**Checksum ruling:** the V3 intake must preserve or dereference per-source components and their typed states plus the field comparison state. A global lifecycle state may supplement, but never replace, component-level source/negative meaning.

## 5. Provenance-is-not-composition-authority counterexample

Let `U1` and `U2` generate separately lawful structural admissions. V554 and V555 derive separate producer-owned objects. Because R02 preserves exact universe/query/admission provenance transitively, V556 can dereference both chains.

That fact does **not** authorize V556 to claim that the two routes were jointly observed, sampled from one respondent universe, or statistically poolable.

**Checksum ruling:** reference closure answers what produced an object. It does not answer whether independently sourced objects may be composed into a joint empirical/structural claim. Any cross-universe composition needs separate positive compatibility/composition authority or must return a typed denial/noncomparability state.

## 6. Source-insensitive dedup counterexample

Suppose `U1` and `U2` yield textually identical canonical structural proposition strings but differ in universe, sample/estimand, weighting, support, authority, or negative limits.

A V554 duplicate key based only on normalized proposition text + use + rule collapses lawful source plurality and can erase disagreement.

R02's conceptual duplicate identity includes admission lineage, but its exact machine key remains a close-read question.

**Checksum ruling:** exact equivalence must retain source/universe/estimand/measure/authority distinctions wherever they are semantically material. Canonical labels do not prove semantic equivalence.

## 7. Negative-authority disappearance counterexample

An EmpiricalFact is denied structural admission, or admission is `NEGATIVE_AUTHORITY_ONLY`, or V553 emits a temporal limit/noncomparability state. Therefore no positive V554 affordance is published.

Later, a resolver sees no positive object and interprets this as ordinary absence of pressure or relation.

That is false. `DENIED`, `NONCOMPARABLE`, `UNKNOWN`, `VALID_EMPTY`, and a positive assertion of absence are distinct.

**Checksum ruling:** required negative/limit authority must survive standalone V557/V558 closure and resolver semantics. Missing positive object is not itself a negative fact.

## 8. Same priors, divergent lives counterexample

Two actors receive:

- identical `ResolvedStructuralContext`;
- identical immutable PSEPF references;
- identical objective comparator facts at intake.

Their later lawful encounter, relationship, exposure, action, event and random histories differ.

An implementation that maps `field.mass` directly to belief or response makes the two lives collapse toward the same state and violates the frozen developmental boundary.

**Checksum ruling:** the broad topology can preserve divergence, but corrected terminal behavior remains `BLOCKED_MISSING_AUTHORITY` until `V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY` governs how empirical possibility constrains proposals/selection without assigning actor state.

## 9. Indirect V2 leakage counterexample

No direct PSEPF -> V2 edge exists. Nevertheless, V3 may expose an opaque audit/provenance reference in an actor-accessible render envelope. V2 then dereferences that ref and adjusts tone, persona, confidence, belief expression or voice based on source disagreement, PSEPF geometry, or structural context.

The direct-edge prohibition has been bypassed without adding a formal edge.

**Checksum ruling:** audit/provenance refs crossing the V3 render boundary must be explicitly non-render/non-persona and non-dereferenceable for expression semantics. V2 may express only V3-generated actor-accessible truth.

## 10. Standalone-reference terminal failure counterexample

V558 contains content-addressed locators for producer objects, but one semantically required object is absent from the standalone package:

- an admission authority snapshot;
- an EmpiricalUniverse manifest;
- an exact QuerySpec;
- a negative/limit object; or
- another referenced producer object.

The locator graph is syntactically intact but terminates in unavailable content. Reconstructing from labels or substituting the latest authority changes historical meaning.

**Checksum ruling:** R02 transitive-reference minimality is sufficient only if standalone closure is proven over every semantically required positive and negative object/authority. Missing content or hash mismatch fails closed.

## 11. Direct-DAG over-optimization counterexample

A narrow optimizer defines unique work as creating a new producer-domain ontology. It then proposes removing:

- V557 because it creates governance rather than structural-domain meaning;
- `V3EmpiricalPossibilityInput` because it creates lifecycle/use admission rather than empirical geometry; or
- DiscoveryService because its result need not feed runtime.

All three deletions can preserve bytes while removing required authority or terminal semantics.

**Checksum ruling:** the no-bloat test must count unique governance, admission, lifecycle, negative-authority, and terminal-service effects as real unique work. `No new producer-domain object family` is not a deletion theorem.

## 12. Cross-cell conflict ledger for synthesis

R03F did not consume R03A-R03E returns and therefore does not attribute claims to workers it has not read. It instead records the independent positions that must be compared against their returns by synthesis.

| Conflict ID | Specialist-favorable assumption to challenge | R03F independent checksum position | Synthesis treatment |
|---|---|---|---|
| CF01 | A bypass classification fixed once at initial admission/use | A later governed use may introduce a new V553 temporal/comparability requirement | Preserve as explicit conflict if R03A treats bypass as object-global |
| CF02 | C transitive provenance closure is enough wherever all refs resolve | Dereferenceability is not cross-source composition authority; negative authority must also be closed | Compare with R03C source/standalone findings |
| CF03 | E one wrapper-level availability/negative state is enough | Mixed source components require source-indexed positive/negative/comparison meaning | Compare with R03E exact input schema proposal |
| CF04 | E broad V3 edge is sufficient to certify terminal divergence | Edge survives, but corrected developmental behavior remains blocked until metabolism authority exists | Synthesis decides whether blocker prevents broad closure |
| CF05 | B no-bloat can remove boundaries that add no producer-domain ontology | Unique governance/lifecycle/terminal-service ownership counts as unique work | Compare with R03B stage-removal proposals |
| CF06 | E/D opaque audit refs are harmless once direct edges are forbidden | Indirect V2 dereference can recreate empirical/structural -> persona leakage | Compare with R03D/R03E negative-boundary findings |

These conflicts are deliberately **not adjudicated here**. R03 synthesis owns reconciliation.
