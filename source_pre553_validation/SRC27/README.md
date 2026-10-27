# R157 LITS lane return (SRC27–SRC30)

This lane binds the four LiTS DTA waves to the frozen R157 source-configuration
interface. It does **not** read original respondent files, execute an original
source, or issue an original empirical workload.

## What is here

- `rawlsing_next/source_configuration/data/SRC27/` — canonical builders for the
  lane and the SRC27 config/item ledger/exact-name correspondence.
- `rawlsing_next/source_configuration/data/SRC28/`,
  `.../SRC29/`, `.../SRC30/` — source configs, full item-accounting ledgers and
  exact-name correspondence records.
- `source_pre553_validation/SRC27..SRC30/` — separately identified
  nonrespondent fixtures, fixture configs, pre-call oracles, actual validation
  traces, exception ledgers and per-source build manifests.
- `source_pre553_validation/SRC27/LANE_RETURN.json` — lane-wide paths, hashes,
  native results, counts, residuals and next integration edge.

## Bindings

Every response-bound item with finite source value labels is serialized as a
native question/response slot with its exact source value labels, missing/special
states, topology and explicit routing state. Items whose P2 row records
`blocked_response_authority_gap` are retained in full but held with that exact
premise; they are not called “unselected” or “outside slice.” Weights, native
row keys and form/administration remain exact scoped unknowns/held because their
required authority/facts are absent. Geographic/admin coordinates are copied
raw only.

Routing is explicit:

- `UNCONDITIONAL_SOURCE_PROVEN` → `ELIGIBLE_APPLICABLE`
- `ADMIN_OR_NONRESPONDENT` → `NOT_ASKED` (administrative route, not a respondent
  eligibility claim)
- conditional/unresolved/multi/country/split → `ROUTING_UNKNOWN`

Only bound items with a known unconditional or administrative route are in the
original config's declared supported-question set. All bound items remain
serialized with their exact rules and typed routing state.

## Reproduce

```sh
PYTHONPATH=. python3 rawlsing_next/source_configuration/data/SRC27/lits_full_bindings.py
PYTHONPATH=. python3 source_pre553_validation/SRC27/run_validation.py
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py -q -o addopts=''
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_p3.py -q -o addopts='' \
  -k 'not r154_loader_delegates_prepared_construction_not_issued_workload and not r154_prepared_path_wrong_source_refusal_and_restore'
```

The two deselected P3 loader tests require a tracked `WORKER_RETURNS/.../r154_load.py`
file that is skip-worktree and absent in this worktree; that file is outside the
LITS write terrain and was not modified.

## Native result and limits

The four nonrespondent fixture releases pass the frozen factory, source-backed
C11 validator and repository path with fixture-only authority. Original source
execution is `NOT_PERFORMED_UNDER_R157_PREPARATION`; fixture validation does not
establish original scientific results or execution permission. See each
`validation_results.json` and `exception_ledger.json` for exact call traces,
refusals, skips and residuals.
