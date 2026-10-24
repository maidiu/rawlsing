# R91 R05 R4 native graph execution/custody contract

Startup `737f1b143963352f201973140002d6f66dbabcaa`; same OpenCode author.
Implements the settled High decision c618dc28... without new architecture.

## Custody and API

- Actual C1 compose calls now retain a canonical in-process original under a
  unique composed identity. A subject-supplied composition/view cannot mint that
  original by rehashing.
- `NativeGraphSlot`, `NativeGraphExecutionRequest`,
  `TrustedNativeGraphCoordinator.execute(request)` and
  `BoundNativeProductGraph(original_ref, view, projection_hash)` provide the
  trusted execution/custody roles.
- The coordinator executes admitted slots using trusted executors, checks each
  result's query/predicate/consumer/model/route/source/release against the slot,
  retains the complete original projection separately, and returns a view.
- `evaluate_learned_world_consumer(..., trusted_graph_reader=...)` accepts only a
  `BoundNativeProductGraph`, resolves the retained original, compares the full
  submitted view (all slots, order, identities), and evaluates the original
  components. Missing/wrong/rehashed/duplicate/omitted view components refuse.
- Raw compatibility graph calls still require each component to match a retained
  actual native original; forged topology/route/discovery/recursive metadata
  cannot pass.

## Graph/status

- Slot count is distinct from each native query's joint target arity; joint
  count/order derives from actual topology.
- Discovery/recursive route refs must exist in the retained original; direct
  routes cannot claim them.
- E41 result must be actual type, route must equal its receipt route, composition
  hash must match retained component, consumer hash must match.
- Exact N10E support requires producer and analytical states SUPPORTED and
  denominator/evidence agreement; disagreement yields typed state with axes,
  cells, Z16 and no exact support.

## Finite tests

Actual M01/M1/M2/C1/N10E positive, two-component direct graph, trusted coordinator
positive and view-substitution refusal, retained duplicate/forged/fake-E41/
status-inconsistency refusals, plus all prior R05V probes. Actual I05/MX01R2 C1
fixtures are not linked to the same M1 disposition by existing source fixtures;
if needed, the exact missing fixture/caller is a learned M1/M2/B5 disposition
built from the AT10/AT11 native source graph. No fabricated linkage.

Limits: full live J42/P41/E04 NOT_REACHED; no original science/source, F6/F7,
CI/prod, N11/N12, Sorok, J52/W52 or R04 dependency. Author candidate only.
