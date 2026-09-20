# FIABC-W3-I05 — Independent Parity Oracle — Governed Return

Worker: `FIABC-W3-I05`  
Repository: `maidiu/rawlsing`  
Branch: `agent/rabochii-premain-fiabc-w3-i05-independent-parity-oracle-r1`  
Base branch: `agent/vozhd-premain-fiabc-wave2-fanin-r1`  
Base SHA: `56697a27e94eb9603dfa412a15ab8f1feb819b0c`  
Return path: `WORKER_RETURNS/FIABC-W3-I05/`

## Disposition

IMPLEMENTED at browser/GitHub code-contract grain.

The independent A/B/C parity oracle now exists as a current candidate-neutral PRE553 module. It freezes expected truth before candidate output, rejects candidate-owned dependencies, compares every candidate independently to the same immutable oracle, preserves exact source/workload/authority/replay/negative-state identities, and refuses to treat self-replay or pairwise candidate equality as expected truth.

WVS7 source-derived expected results are deliberately **not claimed materialized** in this commission. The implementation contains the exact materialization contract and source-hash/frontier guards; real WVS source materialization remains a local mechanical step after integrated fan-in.

Terminal:

`FIABC_W3_I05_INDEPENDENT_PARITY_ORACLE_IMPLEMENTED__SOURCE_MATERIALIZATION_PENDING_LOCAL_EXECUTION`

## Exact Wave-2 obligation implemented

This worker implements only `IMP10 / Independent parity oracle` from the Wave-2 implementation ledger.

Governing specification inputs:

- `WORKER_RETURNS/FIABC-W2-B02/01_PARITY_ORACLE_CONTRACT.md`
- `WORKER_RETURNS/FIABC-W2-B02/02_PARITY_ASSERTION_MATRIX.csv`
- `WORKER_RETURNS/FIABC-W2-B02/03_HOSTILE_ORACLE_FIXTURES.csv`
- `WORKER_RETURNS/FIABC-W2-L01/00_RETURN.md`
- `WORKER_RETURNS/FIABC-W2-L01/02_COMPARISON_TERMINAL_ADJUDICATION.md`
- `WORKER_RETURNS/FIABC-W2-L02/00_RETURN.md`
- `WORKER_RETURNS/FIABC-W2-L02/01_P2X_AUTHORITY_BOM.csv`
- `WORKER_RETURNS/FIABC-W2-L02/03_CLAIM_SCOPED_ANTI_OMISSION_PROOF.md`

No Wave-2 architectural holding was reopened.

## Present owner / call-surface finding

The audited P2X execution surface at ref `617c9c9426db12a3c0f7fea6b68a582c10759553` contains the defective current S03 behavior in:

`rawlsing_next/ee_p2x_darwin_stage_backend.py::_s03`

That implementation freezes its putative oracle only after S01 has already produced candidate state, then invokes `_i03(binding)` twice through the same candidate binding and maps that one self-replay equality bit across semantic, ExactRef, replay, fail-closed, and frontier/typed-negative parity dimensions.

That is the exact Wave-2 B02 false-PASS class. It proves deterministic self-replay only.

The required Wave-3 base `56697a...` does not contain that later divergent P2X backend file. This worker therefore does **not** import or recreate the later runner merely to patch it. It implements the court-owned oracle as a stable PRE553 production module that the integrated P2X S03/gate must consume after fan-in. The exact integration binding is recorded in `04_INTEGRATION_BINDING_CONTRACT.md`.

## Implementation

### Current production module

Added:

`rawlsing_next/pre553_independent_parity_oracle.py`

The module provides:

- `FreezeContext` — fail-closed causal-order contract:
  - `candidate_outputs_seen == 0`;
  - `candidate_owned_roots_consulted == []`;
  - no candidate-owned state reuse;
  - freeze ordinal must precede any known first-candidate-output ordinal.
- `build_lits_i_oracle(...)` — binds accepted immutable ASTRA-D04-R2 truth to current candidate-neutral exact refs/authority without turning ASTRA into a new current semantic owner.
- `materialize_wvs7_oracle(...)` — verifies exact WVS source bytes, accepts only a candidate-neutral semantic materializer, validates the exact Lock2 workload, then freezes the complete oracle before candidate execution.
- `freeze_oracle(...)` / `verify_frozen_oracle(...)` — canonical content addressing plus mutation detection.
- `validate_candidate_observation(...)` — candidate-vs-oracle validation only.
- `validate_three_way_parity(...)` — requires A, B, and C each to match one immutable source-local oracle.

### Exact frozen anchors

LiTS-I is pinned to:

- source SHA-256 `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
- source shape `29,002 × 1,198`;
- projection identity `84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872`;
- C11 release `e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26`;
- C11 replay `6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd`;
- immutable ASTRA-D04-R2 commit `e631de162c582423639b7067a4f36b29f8aa4d89`;
- 50 candidates / 77 roles;
- frontier seal `ca47c52f925b126878cd9e0be433bd6a28bec5a8623784bfbf5eaf7523b21bea`;
- terminal states `49 EVALUATED_SUPPORTED + 1 EVALUATED_VALID_EMPTY`;
- learned product `47d36b1459c2458c480b58631d2c78af68be4dde44015a9220b09177b1eeb28d`;
- semantic replay `301735d4563314a0d7c133fa1afbb0ca57679b3fad887c66e77a909494779eb5`.

WVS7 is pinned to:

- source SHA-256 `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`;
- source shape `97,220 × 613`;
- Lock2 `8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`;
- Lock2 replay `b1aa437406d94b1f81f0ef3c81b885a2fd542749d2e5441747897c016a5dd490`;
- DiscoveryAuthority `24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab`;
- EmpiricalUniverse `f9b1cdffc5783ace87d258ebe2ae1c75040ce786c373e255f53da4be4259d95e`;
- risk set `0bf6a655a35617bec3e54f4d547e89282920e7835e406dcb43b3456774ab87d7`;
- RAW/unweighted measure basis `6ed5d61b77c8d77affeb4b49b55c2cc23a4c25dbd65d02719c6ab7a3069a3c79`;
- the exact ordered 46 candidate hashes from EE-P2F2;
- exact named family shape:
  - 10 `UNARY_SOCIAL_FORK`;
  - 1 `PAIR_RESPONSE_COTRAVEL`;
  - 10 `BRANCH_CONDITIONED_DISTRIBUTION`;
  - 25 `BOUNDED_K_WAY_RESPONSE_CONFIGURATION`.

A 46-item substituted frontier therefore cannot pass merely by preserving cardinality.

## Oracle contents and invariants

Every frozen oracle binds:

- exact source identity;
- exact court/Lock refs;
- exact transitive semantic authority closure;
- projection/C11 release/replay refs where applicable;
- complete ordered I05 frontier;
- one typed expected fact record per frontier member;
- exact I05 terminal coverage;
- learned empirical product identity;
- semantic identity;
- replay identity;
- exact output identity;
- exact-ref manifest;
- replay/dependency manifest;
- the Wave-1/Wave-2 negative-state distinctions;
- authority-closure digest;
- frontier digest;
- candidate-neutral build provenance;
- immutable freeze receipt.

The oracle is comparison evidence only. It does not mint or alter an `EmpiricalFact`, source meaning, routing meaning, discovery authority, or structural authority.

## Semantic-owner proof

This implementation does not create a second semantic owner.

Allowed oracle dependencies are restricted to:

- exact source;
- accepted semantic authority;
- common semantic producers;
- accepted immutable prior empirical products;
- court-neutral inputs.

Candidate output, candidate repositories, candidate caches, candidate sessions, candidate transformed carriers, majority vote, first-successful-candidate truth, and fuzzy/latest/default authority resolution are rejected.

Thus:

`WHO OWNS TRUTH = accepted upstream PRE553/source authority`

while:

`WHO ADJUDICATES PARITY = court-owned immutable oracle`

and:

`WHO PAYS TO REALIZE IT = candidate A/B/C lifecycle`.

## Negative-state preservation

The frozen oracle explicitly preserves the required distinctions:

- physical missingness != semantic response state;
- `ROUTING_UNKNOWN` / `RULE_UNAVAILABLE` != inapplicable/nonmember;
- typed `UNKNOWN`, `MISSING`, `NOT_APPLICABLE`, `NONCOMPARABLE`, `DEFERRED`, `VALID_EMPTY`, and `INTEGRITY_FAILURE` remain distinct;
- no-event, all-missing, empty multiselect, and incompatible topology remain distinct;
- source relation is distinct-by-default unless exact positive relation authority exists;
- `VALID_EMPTY` is not unresolved/unavailable/integrity failure;
- `DENIED` / `NONCOMPARABLE` may not be scalarized;
- `BLOCKED` / manual-review is governance state, not empirical data.

## Hostile tests added

Added:

`rawlsing_next/tests/test_pre553_independent_parity_oracle.py`

Fifteen focused tests cover:

1. positive three-way same-oracle matching;
2. self-replay PASS with oracle fact mismatch;
3. candidate A copied into B/C slots;
4. A/B agreement with C absent;
5. partial frontier omission;
6. collapsed negative state;
7. stale authority closure;
8. stale replay root;
9. candidate-owned oracle dependency;
10. oracle freeze after candidate output;
11. frozen-oracle mutation;
12. wrong WVS source bytes before semantic execution;
13. WVS neutral materializer consulting candidate-owned state;
14. same-cardinality WVS frontier substitution;
15. BLOCKED/VALID_EMPTY anti-collapse contract.

## Tests not executed in this commission

No Python test process was executed.

Reason: the commission restricts this worker to GitHub/browser repository tools and forbids local-machine Codex. The available GitHub connector supports repository mutation/inspection but does not provide a Python execution surface. The exact commands for later execution are in `02_TEST_COMMANDS.md`.

No test result is fabricated.

## WVS7 materialization state

The WVS7 source-derived oracle has **not** been materialized here.

This is required behavior, not a failure: B02 expressly requires real WVS expected results to come from the exact source bytes plus frozen candidate-neutral authority before A/B/C output exists. Those source bytes are a local execution dependency.

`03_WVS7_LOCAL_MATERIALIZATION_PROTOCOL.md` supplies the deterministic procedure. The local operation must write the frozen oracle before any candidate lifecycle begins and must not mount oracle-created state into any candidate.

## Exact blockers

1. `WVS7_ORACLE_SOURCE_MATERIALIZATION_PENDING_LOCAL_EXECUTION` — exact source bytes/runtime are required; no browser result is claimed.
2. `P2X_S03_INTEGRATION_BINDING_PENDING_WAVE3_FANIN` — the audited defective S03 lives on a later divergent execution branch, not the mandated Wave-3 base. HQ must bind the integrated runner to this module rather than transplanting that divergent backend wholesale.
3. Tests are `NOT_EXECUTED_IN_BROWSER_REPO_TOOLING`; commands are supplied for the integrated/local qualification surface.

No semantic-authority blocker was found for the frozen LiTS-I/WVS7 P2X claim scope.

## Boundary audit

This worker did not:

- run measured P2X;
- mutate HQ handoffs or decision ledgers;
- mint source semantics;
- change I03 or I05 semantic ownership;
- create CACC3 or WVS accelerators;
- alter the frozen workload;
- infer semantics from labels, frequencies, layout, or missingness;
- replace frozen candidate identities;
- claim WVS outcomes without source execution;
- treat pairwise candidate agreement as oracle truth.

## Terminal

`FIABC_W3_I05_INDEPENDENT_PARITY_ORACLE_IMPLEMENTED__SOURCE_MATERIALIZATION_PENDING_LOCAL_EXECUTION`
