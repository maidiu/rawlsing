# FIABC-W3-I01 — Governed Diagnostic Successor Return

Worker: `FIABC-W3-I01`  
Repository: `maidiu/rawlsing`  
Branch: `agent/rabochii-premain-fiabc-w3-i01-diagnostic-successor-r1`  
Base: `56697a27e94eb9603dfa412a15ab8f1feb819b0c`  
Obligations: `IMP01` + `IMP03`  
Terminal: `FIABC_W3_I01_DIAGNOSTIC_SUCCESSOR_IMPLEMENTED__READY_FOR_FANIN`

## Holding

The Wave-2 F012 and F018 quantitative diagnostic-operation gaps are implemented as a new current PRE553 diagnostic-only producer without moving source, empirical, discovery, or structural semantic ownership.

The current upstream truth owner remains the governed I03 `EmpiricalFact` / `EmpiricalQuerySpec` surface. The new operation consumes that exact surface and emits a separate content-addressed `PRE553_DIAGNOSTIC_PRODUCT`; it does not add a public empirical semantic family and cannot masquerade as `EmpiricalFact`.

The current call surface is:

`rawlsing_next.pre553_diagnostics.produce_governed_diagnostics(...)`

Replay is:

`rawlsing_next.pre553_diagnostics.replay_governed_diagnostics(...)`

## Implemented F012 operation

`rawlsing_next/pre553_diagnostics.py` independently implements, from exact governed arity-2 contingency material:

- entropy reduction;
- mutual information;
- normalized mutual information;
- Cramér's V;
- cell-level uplift;
- cell-level lift.

The producer accepts only exact numeric material from the governed I03 projection. Binary floats are forbidden from identity-bearing inputs. Metric output is deterministic exact-fraction material where algebraically rational and fixed-precision canonical decimal text where logarithms/square roots are required.

The independent current formula contract is explicit in the product:

- entropy and MI: Shannon information, base 2;
- NMI: `MI / max(H(X), H(Y))`, with zero when the denominator is zero;
- Cramér's V: `sqrt(chi2 / (N * min(r-1,c-1)))` over positive-support dimensions;
- uplift: `P(Y|X) - P(Y)`;
- lift: `P(Y|X) / P(Y)`.

Historical V550 code was used only to establish inherited function grain. It was not imported and is not a current owner. In particular, the current NMI contract uses one coherent log base for numerator and entropy denominator rather than copying historical implementation details mechanically.

## Implemented F018 quantitative diagnostic portion

The same governed diagnostic product carries the F018 quantitative association surface and an optional quantitative joint-confidence component.

Joint confidence requires all of the following explicit exact inputs:

- focus joint cell;
- support ratio;
- completion rate;
- effective-N ratio;
- pattern probability;
- one or more exact determinant refs.

The score contract is:

`mean(clamp01(support_ratio), completion_rate, effective_n_ratio, pattern_probability) * 100`.

No component is defaulted or inferred. In particular, I01 does not compute, select, or synthesize effective-N. That remains the sibling I02 operation. If exact confidence components/determinants are absent, association diagnostics remain available where lawful and joint confidence remains explicitly `UNCERTAINTY_UNQUANTIFIED`.

## Exact identity / replay closure

Every diagnostic product identity binds:

- exact I03 fact ref;
- exact query ref;
- exact source release refs;
- exact inherited authority refs;
- I03 fact replay ref;
- fact producer replay root;
- query producer replay root;
- exact support determinant refs when supplied;
- exact joint-confidence determinant refs when supplied;
- source empirical provenance refs;
- typed source/support states;
- formula contract and metric values.

The replay ref hashes the exact determinant core. The product hash then binds that replay ref. Constructor validation recomputes both hashes, and all identity-bearing nested product material is recursively frozen.

## Negative-state law

The implementation does not turn missing or negative states into numerical zero.

- `NONCOMPARABLE`, `UNAVAILABLE`, `UNRESOLVED`, `INTEGRITY_FAILURE`, and `VALID_EMPTY` propagate as typed product states with null diagnostics.
- Positive non-joint facts yield `NOT_APPLICABLE`, not zero association.
- Explicit governed underpowered state requires an exact determinant ref and remains `UNDERPOWERED`; point diagnostics may remain visible but are typed `AVAILABLE_UNDERPOWERED_DIAGNOSTIC_ONLY`.
- `UNCERTAINTY_UNQUANTIFIED` remains explicit while independently computable point-association diagnostics remain available.
- Once an input claims arity-2 joint topology, malformed contingency material fails closed as an integrity error rather than being relabeled not-applicable.

## No second semantic owner

No existing I03, I05, discovery, structural-admission, source-authority, candidate, or terminal module was modified.

The diagnostic product is deliberately outside the canonical public empirical ontology. `assert_diagnostic_only_use(...)` permits only reporting and non-controlling ranking. It rejects empirical/I03 truth, I05 frontier membership/control, structural authority/admission, semantic interpretation, and source semantics.

Existing owners independently reinforce the boundary:

- `EmpiricalFact` already rejects diagnostic scores masquerading as empirical truth.
- I05 already rejects diagnostic ranking that controls frontier reachability.
- I04 structural admission requires an actual `EmpiricalFact`, not a diagnostic product.

The new hostile tests exercise all three boundaries.

## Test status

A focused hostile test module was added at:

`rawlsing_next/tests/test_pre553_diagnostics.py`

It defines 21 pytest cases after parameter expansion.

Tests were not executed in this worker session because the governed execution surface is GitHub/browser repository tooling only; no shell/test runner is exposed there, and the commission explicitly forbids switching to local-machine Codex. No CI status checks are attached to the current implementation tip. Exact post-fan-in commands are recorded in `02_TESTS_AND_EXECUTION_PROTOCOL.md`.

No measured P2X execution was performed.

## Blockers

No unresolved implementation blocker remains inside I01 scope.

The only cross-worker dependency is intentional: a non-null joint-confidence value for a workload that requires effective-N must receive the exact effective-N ratio/determinant produced under I02's separate authority contract. Until then the lawful I01 state is `UNCERTAINTY_UNQUANTIFIED`, not a guessed number.

## Terminal

`FIABC_W3_I01_DIAGNOSTIC_SUCCESSOR_IMPLEMENTED__READY_FOR_FANIN`
