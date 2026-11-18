# R3_RECHECK — exact remaining counterexamples

## G4-A — Identity keys include mutable state, so contradictions can be distinct records

**Claim:** `R3_FIELD_AND_ADAPTER_CONTRACT.md` §2.3–2.6 defines
`event_key` with `response_state` (lines 44–48), `routing_key` with
`applicability_state`/`routing_state` (52–55), `coordinate_key` with
`coordinate_state` (59–63), and `weight_key` with `weight_state` (67–70).
It says duplicate event key → refusal and conflicting routing/coordinates/
weights at the same key → refusal.

**Failure:** if state is part of the identity key, two records for the same
stable event/coordinate/weight identity that disagree on state have different
keys and are not duplicates. The contract therefore does not establish the
required contradiction refusal. The actual evaluator catches routing state
conflicts in `_routing_fact_for` and weight multiplicity in `_weight_for`, but
that is evaluator behavior, not the proposed view contract; the contract must
not let a contradiction become a distinct valid record.

**Smallest correction:** separate stable identity keys from mutable content:
event identity `(universe, respondent, native question, canonical/component,
event group/id, occurrence/topology)`; routing identity `(universe, respondent,
question/target, risk set, routing rule)`; coordinate identity `(universe,
respondent, native coordinate, canonical coordinate, effective time)`; weight
identity `(universe, respondent, weight basis, effective scope, source/design/
estimand authority)`. Treat state/value as content, and refuse multiple
differing contents for one identity unless an exact declared version/authority
distinguishes them.

## G4-B — `SelectionMembership` count-only cannot supply exact risk/denominator refs

**Claim:** `R3_FIELD_AND_ADAPTER_CONTRACT.md` line 107 defines
`selection_membership(...) -> SelectionMembership (candidate refs + nonselected
count)`; the corrected decision §3.3 says it stores candidate refs and
complement counts, not facts/denominators/evidence.

**Actual evaluator:** `_pre553_query_eval.py` `_build_fact` sets
`risk_set_member_refs=evaluation.risk_members` and
`denominator_member_refs=evaluation.denominator_members`; `_evaluate_index_group`
loops all `_query_respondents(index)` and appends full respondent refs. An
`EmpiricalFact` therefore requires the complete ordered risk/denominator member
refs, not a count.

**Failure:** a reusable selection object containing only candidate refs and a
complement count cannot construct the full nonselected membership needed by the
native fact. The contract says the adapter “must expose the full risk population
and nonselected members,” but the `SelectionMembership` payload contradicts
that. Count-only reuse is diagnostic, not fact construction.

**Smallest correction:** `SelectionMembership` must carry exact ordered
risk/denominator member refs (and complement membership refs), or the adapter
must always materialize the complete `_ReleaseIndex` membership needed by the
native evaluator. Keep counts only as statistics; do not use them to build
facts.

## G4-C — “Bounded by selected row groups” does not account for full risk/denominator cost

**Claim:** `R3_FIELD_AND_ADAPTER_CONTRACT.md` lines 125–129 says the derived
view is “Disk/RAM bounded by selected partition/row groups; no full object
graph,” while also requiring full risk population and nonselected members.

**Actual evaluator:** `_ReleaseIndex` carries full `respondents`,
`events_by_respondent`, `coordinates_by_respondent`, `routing_by_respondent`,
`weights_by_respondent`; `_evaluate_index_group` evaluates every respondent and
needs routing/weight membership for all of them before it can append exact
risk/denominator refs. A selected-row-group view cannot both bound RAM to the
selected rows and expose the complete universe/routing/denominator membership
unless a qualified full membership index or full routing/weight scan is added.

**Failure:** the contract makes a bounded-RAM claim without accounting for the
full routing/weight/denominator cost. It does say “No Q-reduction claim before
measurement,” but the bounded-RAM declaration is still unsupported for exact
full-domain facts.

**Smallest correction:** distinguish selected page reads from the full
universe/routing/denominator membership scan. State the full cost or require a
qualified compact index, and do not claim bounded RAM or Q reduction for
full-domain facts until measured.

## G2 — External artifact lookup/scope/refusal is not concrete

**Claim:** the corrected field map says original-language option/form/ballot,
household/roster, PSU/strata/variance and numeric uncertainty are “external
source/codebook/design artifact by exact identity; else typed absent/hold”
(`R3_FIELD_AND_ADAPTER_CONTRACT.md` §1; decision §5.1).

**Failure:** the C11-versus-external-versus-absent field map is now accurate,
but no concrete external artifact type, exact ref kind, lookup/join from
`native_question_ref`/`instrument_release`/`source_artifact_import_lineage`,
authority/current check, scope, permission or refusal protocol is defined. A
search of the product schema named by the contract finds no `ExternalArtifact`
or codebook resolver. “External by exact identity” is a rule, not a demonstrated
lookup/join/scope/refusal route.

**Smallest correction:** add an `ExternalSourceArtifact` contract (exact ref
kind/content hash, lookup key from native ref/version/source identity,
authority/current/rights, scope, typed absent/RIGHTS_HELD/refusal), or mark the
external lookup `UNPROVEN_HOLD` and do not grade those fields
`CONCEPTUALLY_ACCOMMODATED` until specified.

## G1 — FF01-k split is correct; the proposed contract is still category-level

**Resolved part:** the old claim is retracted; `R3-RES-023` and corrected
decision §5.4 correctly separate FF01-2 (fixed Q86B→Q86A, two-participant,
count-only, no ratios) from proposed FF01-k. The proposed FF01-k names
roles/order/keys, direction-specific numerator/denominator/routing/weights/
coverage/typed states, producer facts, permission ceiling, prospective
consumer, and owner-held method/eligibility/ratio.

**Remaining issue:** `R3_FIELD_AND_ADAPTER_CONTRACT.md` contains no exact
FF01-k field/receipt schema; the decision gives category bullets, not a named
`FF01KProduct` with exact role/ordering/ref fields, receipt, and consumer
interface. This is close to the required conceptual contract but not yet the
same standard as the exact C11 field/adapter table.

**Smallest correction:** add the exact FF01-k field/receipt table (role/order
refs, direction-specific risk/weight/coverage/typed-state fields, receipt and
prospective consumer); keep method/eligibility/ratio owner-held. No
implementation is required for this documentary grade.
