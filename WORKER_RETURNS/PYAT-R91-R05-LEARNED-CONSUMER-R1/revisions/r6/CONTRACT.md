# R91 R05 R6 coordinator native-input contract

Startup `68b8f33fae7432e968e25f312f265f45c523718c`; same OpenCode author.
Implements the settled High decision coordinator-native-input function.

## NativeGraphSlot actual associations

Slot now carries actual native inputs, not only labels: discovery result +
exact receipt + frontier; recursive handoff + lineage + root/parent; condition
value witness; target arity/order; M1 disposition; M2 release; B5 selection and
currentness requirement; E41 input; and the actual repository/query/predicate/
authority/consumer/model objects needed for owner invocation.

## Coordinator execution

`TrustedNativeGraphCoordinator.execute` uses independently admitted slots
(`admitted_slots`), never request-selected replacements. For each slot it invokes
the actual `compose_positioned_subject_possibility` from admitted objects,
including actual `discovery_result`/receipt or `recursive_handoff`, validates
route/topology/discovery/recursive refs and learned release/currentness, runs the
actual E41 extension from the same inputs and reconciles route/receipt/composition/
consumer, then retains the full native input/output original. The subject request
cannot substitute a prebuilt composition; it may only reference admitted slot
metadata.

## Consumer

`evaluate_learned_world_consumer(..., trusted_graph_reader=...)` uses the
retained original and original components; the complete view/order/m1/m2/B5
association is checked before unchanged N10E. Discovery/recursive/joint R5
positives now run through this path; fake/relabelled E41/data-only views refuse.

## Tests

Actual discovery, recursive and joint consumer through trusted coordinator;
actual E41 discovery/recursive route reconciliation; actual changed evidence
refusal and restore; all prior R05V probes; status/Z16/custody retained.

Limits: full live J42/P41/E04 NOT_REACHED; no source/science/CI/prod/N11/N12/
F6/F7/Sorok/J52/W52/R04 authority. Author candidate only; distinct review follows.
