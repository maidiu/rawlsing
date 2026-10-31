# Test receipts and fault negatives

## Historical P41

Exact branch `f27d1101048638bba395143a48efb7ef00bfcda4`, extracted to an isolated
temp tree; sourcefree only.

```bash
cd WORKER_RETURNS/PYAT-R41-P41-GENERIC-PROGRESSIVE-N10E-N10W-SERVING-R1
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests
```

| Court | Result | Exit |
|---|---|---|
| P41 suite | **19 passed** | 0 |
| P41 after witness restore | **19 passed** | 0 |

Three exact proof-gate witnesses were rerun against the historical tree using
the frozen `.proof.json` manifests; each mutates the actual runtime, requires the
named assertion to fail, and restores the file:

| Witness | Fault path | Result |
|---|---|---|
| W1 N10E computed edge | `runtime/p41_service.py` | `BOUNDED_MUTATION_DETECTED`, exit 0 |
| W2 N9 structural edge | `runtime/p41_service.py` | `BOUNDED_MUTATION_DETECTED`, exit 0 |
| W3 selection/currentness edge | `runtime/staged_native/pre553_learned_product_lifecycle.py` | `BOUNDED_MUTATION_DETECTED`, exit 0 |

## Current E03 / C1 / N10E / F8

Run from the review worktree at `8e44ca9c...`:

| Court | Result | Exit |
|---|---|---|
| Current E03 `test_pre553_n9_n10w_progressive_candidate.py` | **18 passed** | 0 |
| Current C1 + N10E + F8 (`test_source_backed_positioned_subject_possibility.py`, `test_pre553_analytical_composition.py`, `test_pre553_empirical_possibility_provider.py`) | **69 passed** | 0 |
| Current learned-world composition | **30 passed** | 0 |

## Selected-world

Exact historical tip `ed34944e253b78714a28d72b8ca2a6521ce15930`:

| Court | Result | Exit |
|---|---|---|
| `test_pre553_selected_world_progressive_contract.py` | **24 passed** | 0 |
| `test_r3_s02_seam_witness.py` | **26 passed / 1 failed** | 1 |

The failure is preserved exactly:

```text
test_s00c_change_source_owned_synthetic_numeric_values_changes_result
KeyError: 'exact_probabilities'
```

The consumer returned `REFUSED / PRODUCER_VALUE_IDENTITY_MISMATCH` because the
changed numeric cells were still bound to the old selected-world contract. The
original failing receipt is not erased or rewritten.

## Bounded selected-world repair

`sourcefree_adapter/selected_world_repair.py` and
`tests/test_selected_world_repair.py`:

| Test/operation | Result |
|---|---|
| Original cells 3,1,1,3 -> Q86B=1 conditional | 3/4 |
| Rebound cells 3,1,2,2 -> same conditional | 1/2 |
| Same denominator / different contract hash | PASS |
| Old contract + changed channels | `SOURCE_VALUE_CONTRACT_MISMATCH` |
| Zero denominator vs missing step | `ZERO_SUPPORT` vs `NO_SUPPORT` |
| Cold restore identical exact read | PASS |
| Tampered cold payload | refused |
| Live tamper/restore | refused then green |
| Court | **5 passed**, exit 0 |

## Current P41-style adapter

`sourcefree_adapter/p41_current_service.py` calls current E03, which calls
current N10E→C1→F8.

| Test/operation | Result |
|---|---|
| Exact current chain 32→16→8, 9/16→5/8→3/4 | PASS |
| Three F8 consumptions exact | PASS |
| As-of / publication / rule-clock metadata | changed without empirical geometry change |
| Empirical revocation | consumer read `REFUSED`, progressive chain remains exact |
| Historical archival receipt | `archival_only=True`, fresh use false |
| Cold restore exact | PASS |
| Tampered receipt hash | `RECEIPT_HASH_MISMATCH` |
| Replay deterministic | same content-addressed receipt |
| Court | **5 passed**, exit 0 |

Adapter runner:

```bash
cd WORKER_RETURNS/PYAT-P41-R08-RECOVERY
./repro/run_sourcefree_adapters.sh
```

Result: **5 passed + 5 passed**, exit 0.

## R08 evidence binder

Exact current-provider harness:

```bash
./repro/run_r08_current_binder.sh
```

| Court | Result | Exit |
|---|---|---|
| R08 author suite against current `rawlsing_next` | **113 passed** | 0 |
| R8 targeted refusal probes | **8 passed** | 0 |

The script extracts the exact binder/test blobs, current `rawlsing_next`, exact
C1 fixtures, and R8 review probes into a temp tree. It does not commit or load the
118 KB binder into production.

Covered refusals: missing live producer pin, attacker issuer/fabricated envelope,
forged caller context, stale/unauthenticated cache, altered evidence/query/rule
objects, unsafe cache/self-seal, callable substitution, descriptor pin mismatch,
missing verifier, legacy binding-pin migration, and cold replay.

## Fault/negative summary

| Fault | Named red | Restore |
|---|---|---|
| P41 W1 N10E computed edge | named test assertion fails | P41 19 pass after restore |
| P41 W2 N9 structural edge | named test assertion fails | P41 19 pass after restore |
| P41 W3 selection/currentness | named test assertion fails | P41 19 pass after restore |
| Selected-world source value change under old contract | `SOURCE_VALUE_CONTRACT_MISMATCH` | new contract 1/2 green |
| Selected-world stale/tampered payload | refused | cold restore green |
| P41 current empirical revoke | `EMPIRICAL_SCOPE_REVOKED` | historical receipt retained; progressive still exact |
| P41 current receipt tamper | `RECEIPT_HASH_MISMATCH` | valid receipt green |
| R08 cache/issuer/evidence mutations | exact typed refusal | positive/cold replay green |

## NOT_RUN / NOT_CLAIMED

- No original survey/respondent data; no source-native execution.
- No actor/Sorok/V3 execution.
- No native C compilation/execution.
- No live P41/J42/E04 whole-service consumer.
- No current production E03/P41/R08 receiver; GAP CARD remains.
- No N10W global installation or N9 owner acceptance.
- No production merge or adoption.

## Overall

**10 current/p41/selected adapter tests pass; 19 historical P41 pass; 3/3
severance witnesses pass; 18 current E03 pass; 24/24 selected-world pass with
1/27 seam RED preserved; 69 C1/N10E/F8 pass; 30 learned-world pass; 113/113 R08
author tests and 8/8 R8 probes pass.** These are sourcefree scoped results, not
native source or production adoption.
