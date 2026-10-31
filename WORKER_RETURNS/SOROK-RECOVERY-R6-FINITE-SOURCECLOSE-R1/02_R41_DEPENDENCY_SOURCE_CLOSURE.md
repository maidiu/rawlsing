# R41/W41 objective-world dependency source closure

## 1. Exact source cut and identities

| Item | Exact value |
|---|---|
| Branch | `agent/rabochii-pyat-r41-w41-objective-multifield-temporal-n9-r1` |
| Cut | `b0a68e4ff5d5e2ca62b080376fda6b5f5431a6c2` |
| `objective_world.py` | blob `79a91fc027d4be5428e19ef7a14cac0c19e96e4d`; SHA-256 `66feab937ac168254ecb5bdea15d9fb9cb4ef3d7facdad0ab6eff4fcf9b1a096`; 15,203 bytes |
| `w41_bootstrap.py` | blob `af09f3724e8a5496acb40bf7a3e74e5b47598fa9`; SHA-256 `9ffc5dbac035b3131ac935e8493aaab666330ca8033b8f137491c95f65332b3a` |
| `native_owners.tar.gz` | 3,629,731 bytes; SHA-256 `996df032812585d67400ba75b036dfc7b1a9b2f31dde69b4371d5b45f6f22710` |
| Owner pins | 133 entries in `owner_pins.json`; archive membership 133 |
| Archive composition | 127 Python files + 3 JSON fixture files + 3 other metadata entries |
| Runtime import closure | 91 loaded modules in `evidence/imports.json`; 87 have exact owner pins; 4 are the top-level driver/bootstrap modules |
| Current PRE-MAIN | `5fc1d43e3d5412194d1f1eaa30ff448f84635e99`; exact R41 path absent |

`reconstruct_owners.py --verify` was executed in an isolated temporary copy:
`{"verified_files": 133}`. Every archive member was checked against the owner
pins; no preimage mismatch occurred. This is a sourcefree closure check, not a
native source read.

## 2. Direct dependency graph of `objective_world.py`

22 direct import statements / 17 project-local or native modules:

```text
w41_bootstrap
rawlsing_next.pre553_empirical_objects
rawlsing_next.m4_v557_v558_publication_repository
rawlsing_next.field_forge_conditional_support
rawlsing_next.gt12_c_to_d_relation_bridge
rawlsing_next.gt12_d_to_m4_typed_bridge
rawlsing_next.pre553_repo_native_current_payload
rawlsing_next.gt12_e2b_publication_governance_binding
rawlsing_next.pre553_hq297_n9c_two_field_reader
world_join
product.nonparent
product.scenario
two_epoch_world
f6p_partial_bound_evidence_consumer
f6p_fixtures
ee1_temporal_owner
ee1_fixtures
```

`w41_bootstrap.py` reconstructs the 133-file pin archive and prepends:

```text
owners/native
owners/wv1
owners/wv1/vendor
owners/native/rawlsing_next/tests
owners/f6p
owners/f6p/oracle
owners/f6p/tests
owners/ee1/runtime
```

The archive pin distribution is:

| Owner group | Files |
|---|---:|
| `owners/native` rawlsing_next/C11/M4/M5/F6/N9 modules | 76 |
| `owners/ee1` temporal owner/tests/fixtures | 26 |
| `owners/wv1` selected-world/product/two-epoch modules | 21 |
| `owners/f6p` F6 evidence modules | 10 |
| **Total** | **133** |

The dependency closure includes `pre553_hq297_n9c_two_field_reader.py` and the
N9C tests/fixtures. It does **not** create an issued N9/N10W transport. The N9
reader remains the same test-only two-field reader identified by RCF-D.

## 3. Actual input, transformation and output

`objective_world.py` supplies:

- `retained_context()`: retained Afro R5 Q86B/Q86A GT2 context through the
  actual FF → admission → V554 → M4 path; 36 cells, 23 observed zeros, 19,210
  common-exposure denominator; B1 publication null; M5 CURRENT held.
- `position_context()`: exact J04 BEN0002/Q73A reconstruction, not a fresh
  respondent read; expected fact content hash
  `c823a816ce6f71431c99b1a466c7313f3766e5d1e7832fc36b6a31f15835dd02`.
- `independent_fields()`: native N9C fixture read of GSS rural household
  lighting and NCA mobile-data subscriptions, preserving different units and
  not joining them as persons.
- `f6_evidence(case)`: all W1-W8 F6P evidence outcomes, including partial
  bounds, unsupported cases and no point when unsupported.
- `ObjectiveWorld.read(mode, budget)`: seven rule families × three clock modes
  × four budgets = 84 synthetic original-client views.
- `temporal_methods()`: nine V553/EE1 cases; measured pairs and Ghana delta
  remain null/HOLD.
- `purpose_refusals()`: `CONCEPTION_SCENARIO_PROPOSALS` and
  `N9_SELECTED_WORLD` remain refused under the exact test-only permission.

Versioned output:

```text
W41_READONLY_SOURCE_QUALIFIED_WORLD@1
current_historical_asof_world_consumer_receipts.json (39,212,431 bytes)
source_field_and_structural_owner_inventory.json
multifield_nonpooling_and_bounds_receipts.json
measured_temporal_eligibility_and_method.json
```

No source-native probability, actor, memory, N11/N12 or measured trend is
issued.

## 4. First actual consumer

The branch-local first caller is `capture_products.py`:

```text
capture_products.py
  -> objective_world as w
  -> w.product()
  -> validate 84 worlds, 8 F6 cases, 2 fields, GT2 and J04 paths
```

The first test consumer is `tests/test_native_world.py`. The future external
consumer is named only in `P41_A41_HAND_BACK.json`:

```text
P41: objective_world.ObjectiveWorld.read(mode, budget=5)
     contract W41_READONLY_SOURCE_QUALIFIED_WORLD@1
```

This is a handback, not an active PRE-MAIN importer. Current PRE-MAIN contains
an R42 commission reference to the R41 cut, but no executable call path. There
is **no current PRE-MAIN first consumer**.

## 5. Executed selected tests

In an isolated temporary copy, after source inspection:

```sh
python3 reconstruct_owners.py --verify
# {"verified_files": 133}

PYTHONPATH="$PWD" python3 -m pytest -o addopts='' -q tests/test_native_world.py
# 26 passed in 70.20s, exit 0
```

The 26 selected tests cover retained FF context, F6 partial evidence, temporal
rule revisions, selected-release divergence, M4 resolution, J04 exact position,
five independent rule families, all eight F6 cases, N9C unit/geography
preservation, purpose refusals, archival/revocation and missing-weight
refusal.

NOT_RUN: the author-reported full 94 core + 33 EE1 + 1 temporal regression
suite; `capture_products.py` (it writes a 39 MB receipt and generates all 84
views); any provider call, raw survey read, native N11/N12 execution or
production integration.

## 6. Source closure recommendation

**R41 source/dependency closure: CLOSED for reading and source safety.**
All direct imports resolve to the 133 pinned archive files or to the top-level
R41 bootstrap/driver files; the archive hash, membership and all 133 preimages
verify. The selected 26-test subset passes.

**R41 engine/product closure: HELD.** The harness is `UNWIRED_SOURCE_PRESENT`
at current PRE-MAIN. It is a read-only client/harness, not the PRE-V3 objective
world release root, not a native N11/N12 service, and not a current Sorok C0
consumer. Its F6 evidence is a separate sourcefree contract; no F6→N9 join is
authorized.
