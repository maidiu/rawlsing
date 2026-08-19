# SV3C HOSTILE FIXTURES — EFFECTIVE TIME / SOURCE STATE / NEGATIVE ADMISSION

**Authority:** non-dispositive feeder evidence for SCRV3.  
**Expected global property:** no fixture may create actor truth directly from source-state or time convenience.

## H01 — nearest-time alignment

Given:
- actor-fact snapshot effective time = 2000-01-01;
- source component U1 scope = 1998;
- source component U2 scope = 2002;
- V3 decision effective time = 2001;
- no exact authority establishes either source scope as the lawful alignment for the decision.

Attack: select U2 because 2002 is numerically nearest, or U1 because it is the nearest nonfuture source.

Expected:
- `EFFECTIVE_TIME_NONCOMPARABLE` or exact equivalent;
- no PSEPF semantic read;
- no nearest-source fallback;
- actor state unchanged.

## H02 — backdating future evidence

Given a V3 decision effective at 2005 and a source field whose evidence/availability begins in 2010.

Attack: use the 2010 field because it exists in the current repository, then label the result as a 2005 decision input.

Expected:
- hard V3 decision-time rejection;
- `EFFECTIVE_TIME_NONCOMPARABLE` or stronger integrity/temporal denial;
- current repository availability does not become historical availability;
- no retroactive actor mutation.

## H03 — latest-source substitution

Given:
- requested source universe U1 returns `TARGET_UNAVAILABLE`;
- a newer or broader source U2 contains the target;
- no source-applicability authority says U2 substitutes for U1.

Attack: silently replace U1 with U2 because U2 is newest, broadest, local, or highest support.

Expected:
- preserve U1 `TARGET_UNAVAILABLE`;
- U2 may only enter through a separately governed request;
- no substitution, no pooled field, no actor effect.

## H04 — source-majority voting

Given:
- U1 supports configuration C;
- U2 supports configuration C;
- U3 supports D or is noncomparable;
- no operation-specific source-composition authority exists.

Attack: choose C by 2-of-3 vote or by strongest support.

Expected:
- `SOURCE_CONFLICT` and/or `SOURCE_COMPONENT_NONCOMPARABLE` preserved;
- no majority or support winner;
- no actor belief/response assignment;
- exact components remain separately dereferenceable.

## H05 — LOW_SUPPORT promoted to certainty

Given a lawful component with `LOW_SUPPORT`.

Attack:
- treat it as certain because it is the only available source;
- convert low support to a default actor belief or high-confidence candidate weight.

Expected:
- `LOW_SUPPORT` preserved;
- owner read allowed only if an exact owner rule explicitly admits weak evidence;
- no certainty promotion;
- no default actor truth.

## H06 — ZERO_SUPPORT promoted to actor impossibility

Given `ZERO_SUPPORT` for the exact conditioner/risk set.

Attack:
- set actor probability to zero;
- forbid an otherwise lawful V3 history as metaphysically impossible;
- replace the missing empirical conditional basis with a nearest cohort.

Expected:
- `ZERO_SUPPORT` preserved as no empirical conditional basis;
- no PSEPF-derived actor impossibility;
- no nearest-cohort fallback;
- any independently lawful V3 candidate remains governed by its actual owner.

## H07 — null / not-asked coerced to zero

Given a source target that is unasked, inapplicable, unavailable, or null by routing.

Attack: serialize the missing target as numeric zero and then treat it as `OBSERVED_ZERO` or `ZERO_SUPPORT`.

Expected:
- preserve the exact target/routing negative such as `TARGET_UNAVAILABLE`;
- null remains distinct from substantive zero;
- no numeric actor effect.

## H08 — source conflict collapsed into one field

Given two supported source components with materially different exact J-way distributions.

Attack:
- average them;
- retain only modal agreement cells;
- select the most recent source;
- expose a single wrapper state `AVAILABLE`.

Expected:
- both source components remain canonical;
- comparison state remains conflict/disagreement;
- no silent composition;
- wrapper-level availability cannot erase per-source state.

## H09 — scheduler-time conflation

Given:
- ADP-021 `current_effective_time = 2026`;
- the V3 decision being replayed has `decision_effective_time = 2005`;
- a 2026 PSEPF exists.

Attack: because the scheduler runs now, substitute the 2026 field for the historical decision.

Expected:
- scheduler time coordinates execution only;
- replay uses the exact historical PSEPF and snapshot refs;
- mutable/current/latest substitution fails closed;
- no history rewrite.

## H10 — stale actor snapshot requires upstream requery

Given:
- PSEPF F0 was built from objective actor snapshot S0;
- a later committed V3 generated fact changes a comparator-relevant actor fact;
- a subsequent empirical possibility decision requires the changed comparator fact.

Attack: reuse F0 by only changing the V3 intake timestamp.

Expected:
- `UPSTREAM_REQUERY_REQUIRED`;
- a new comparator/query/PSEPF request is required;
- old F0 remains immutable/replayable;
- V3 cannot repair the upstream conditioner locally.

## H11 — use-class change requires rebind, not requery

Given:
- immutable field F remains empirically valid for the actor/source/time context;
- only V3 use class or metabolism-use binding changes;
- source/query/comparator facts are unchanged.

Attack: regenerate PSEPF merely because V3 use class changed, or silently reuse the old binding.

Expected:
- `STALE_OR_REBIND_REQUIRED`;
- new exact V3 binding may point to the same immutable F if lawful;
- no upstream recomputation is inferred;
- old intake binding remains replayable.

## H12 — missing metabolism authority

Given a perfectly aligned, supported, source-consistent PSEPF but no exact `V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY` binding or no owner read-permission row.

Attack: consult the field anyway because all empirical checks pass.

Expected:
- `MISSING_METABOLISM_AUTHORITY` or `OWNER_READ_PERMISSION_MISSING`;
- `NO_PSEPF_TRANSITION_EFFECT`;
- actor state unchanged.

## H13 — immutable hash mismatch

Given a V3 intake that names field hash H1 while the resolved object bytes hash to H2.

Attack: accept by matching human label, source name, query text, or latest locator.

Expected:
- `INTEGRITY_FAILURE`;
- hard reject;
- no fuzzy repair;
- no actor mutation.

## H14 — noncomparable component silently dropped

Given:
- U1 = supported and time-aligned;
- U2 = `SOURCE_COMPONENT_NONCOMPARABLE`;
- the canonical PSEPF request is multi-source and no exact owner rule requests U1 alone.

Attack: discard U2 and proceed as if the original multi-source field were fully admissible.

Expected:
- U2 remains in the canonical state vector;
- generic multi-source operation is denied or no-effect absent exact authority;
- a separately source-scoped U1 operation is lawful only if the owner contract explicitly names U1 and does not claim composition.

## H15 — historical replay versus newer field

Given:
- historical decision D0 used actor snapshot S0 and field F0;
- a later lawful field F1 exists for a later snapshot/time;
- replay D0 exactly.

Attack: use F1 because it is newer or currently preferred.

Expected:
- exact historical S0/F0/authority binding is used;
- F1 is irrelevant to D0 replay unless the replay specification itself is a new counterfactual request;
- replay identity is stable;
- no latest substitution.

## H16 — same timestamp, different semantic clock

Given:
- actor snapshot time, source field period end, V3 decision time and scheduler time all serialize to `2020-01-01`;
- their authority identities differ.

Attack: collapse the four fields into one `effective_time` and omit clock-role identity.

Expected:
- rejection of ambiguous replay/admission identity;
- equal values do not merge semantic clocks;
- receipts retain clock role and owner.

## H17 — conflict plus low support

Given:
- U1 supports C at high support;
- U2 supports D at low support;
- both are lawful source components.

Attack: erase U2 because low support makes it inconvenient, then claim consensus.

Expected:
- U2 remains `LOW_SUPPORT` and disagreement remains visible;
- low support may affect an explicitly governed owner rule but cannot erase source conflict by itself;
- no majority/strength winner.

## H18 — all negatives coexist

Construct an intake carrying:
- one `NO_COMPARATOR` lineage;
- one source `TARGET_UNAVAILABLE`;
- one source `LOW_SUPPORT`;
- one `SOURCE_COMPONENT_NONCOMPARABLE`;
- stale V3 binding;
- missing metabolism authority.

Expected:
- action precedence yields no semantic read/no actor effect;
- all owner-scoped states remain preserved in the receipt/state vector;
- the highest-priority action reason does not semantically overwrite lower-priority negatives.

## Pass criterion

The hostile suite passes only if:

```text
no nearest/latest/backdated evidence substitution survives
AND
scheduler time never becomes empirical evidence time
AND
upstream requery and V3 rebind remain distinct
AND
all required per-source typed states survive
AND
LOW_SUPPORT != ZERO_SUPPORT != OBSERVED_ZERO != null
AND
source conflict is never majority-voted away
AND
missing metabolism authority yields zero PSEPF transition effect
AND
historical replay never consults mutable latest state
```
