# P3 compression evidence — bounded mechanical return

**Worker:** `sorok-p3-compression-evidence-r1`  
**Branch:** `agent/sorok-p3-compression-evidence-20261106-r1`  
**Startup / protected:** `7db475fb29c0977d2c368dc2f83b5471f0a59460` / `c852d7516e23fcb6cf2215e9be7c5fa268503516`  
**Scope:** sourcefree TEST_ONLY metadata sidecar only.

## Verdict

**PASS_SCOPED**

Implemented the frozen compression API in `p3/compression.py`; it is pure,
source-preserving, and has no world, P2 owner, psychological, memory or claim
writer. Tests pass against compact nonrespondent documents. Actual P2 wrapper
integration and integrated acceptance remain HQ's responsibility.

## Exact API

```python
preflight(spec, *, identity, proposal, catalog) -> dict
bind(spec, *, identity, proposal, catalog, realized) -> dict
```

`identity` is `StateIdentity.document()`; `proposal` is
`EventProposal.document()`; `realized` is the actual
`RealizedEvent.document()` from the accepted P2 owner; all are plain JSON.

`preflight` returns the detached validated `spec` and has no effects.

`bind` returns content-addressed metadata with `status`:

- `BOUND` — actual P2 event, actor-observed accessible projection, and any
  claimed actual interval are all bound. `actual_event_ref` uses the native
  `e1_event_id`; `actual_event_hash` uses `e1_event_hash`; `perception_refs`
  are content hashes of the actual P2Owner perception projection; interval
  receipt hash/status are included where present.
- `HELD` — the actual native event or actor access/perception is unavailable;
  or a claimed accumulated interval is missing/not performed. No positive
  exposure, no psychological effect and no false `NO_CHANGE` is emitted.

Wrong source, grade, source hash, source identity/time, proposal/context hash,
owner identity/clock, actual event actor/branch/hash, readset/receipt or actor
access binding is refused. Unsupported fields are refused.

### Spec fields

`envelope_id`, `proposal_hash`, `representation_form`, `represented_window`
(`from_clock`, `to_clock`, `coverage_basis`), `recurrence_basis_refs`,
`participation_refs`, `material_relation_refs`, `observed`, `unobserved`,
`selection_basis`.

Supported forms:

- `SINGULAR_OCCURRENCE`
- `REPRESENTATIVE_EPISODE`
- `ACCUMULATED_INTERVAL`
- `RETROSPECTIVE_CRYSTALLIZATION`

Canonical source-free catalog kinds:

- `ACTOR_PARTICIPATION`
- `MATERIAL_RELATION`
- `RECURRING_RELATION` (representative basis)
- `BOUNDED_INTERVAL` (accumulated basis)
- `HISTORICAL_SOURCE` (retrospective basis)

Each source document has `hash`, `grade=SOURCEFREE_TEST_ONLY`, `root`, `actor`,
`branch`, `kind`, `from_clock`, `to_clock`, `data`; `hash` must equal
`digest(document excluding hash)`.

### Example output fields

`envelope_id`, `envelope_hash`, `spec_hash`, `status`, `held_reason`,
`sourcefree_grade`, `identity`, `proposal_hash`, `representation_form`,
`represented_window`, `source_ref_hashes`, `actual_event_ref`,
`actual_event_hash`, `native_status`, `actor_access`, `actual_interval_ref`,
`actual_interval_hash`, `actual_interval_status`, `perception_refs`, `observed`,
`unobserved`, `selection_basis`, `psychological_effects=[]`,
`no_psychological_effects=true`, `no_state_mutation=true`,
`memory_or_claim_issued=false`, `adp016_017_authorized=false`.

See `evidence/compression/API_EXAMPLE.json` for a concrete BOUND example.

## Tests

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
PYTHONPATH=WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1 \
python3 -m pytest \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_compression.py \
  -q -o addopts="" -p no:cacheprovider
```

Observed: **22 passed in 0.11s**.

Coverage includes all four forms, exact source hash/grade/identity/time,
form-specific source kind/window requirements, wrong proposal/context/
identity/clock bindings, actual event actor/branch/hash/readset/receipt checks,
the actual interval requirement for accumulated intervals, HELD on absent actor
access, rejection of user-view markers, rejection of `global_multiplier`,
`witness_count`, fabricated event IDs and automatic-effect fields, purity, and
deterministic content addressing.

## Implementation pins

- `p3/compression.py`: `5219fd21ec9461468b508e2208c1e09ac0dcf9f1e76cc9fe8d0603f8fbcb8efb`
- `tests/test_compression.py`: `a69c21b4609a9ca2aa386086133d8a369bda964bceb082e50794e33572fb0e27`
- Accepted P2Owner: `fd98a757a102faae78b5b9e520cf7ce07d518d5f62942bea3279b696a13401d0`
- Contracts: `9aabbc9f14c55234b5c3612dcc3a7e8165d835e06ea2cc5f72af98d5e6472f2d`
- ABI: `424a956d6de5b207633d45112fee4fa6125b290a4ed012697672a41a91408468`
- Integration contract: `0c728671db1c8271e27be48872678adef89de7eea9e92e6c59d3ad7c5c0806af`
- Architecture: `14335b360865b45c2e917aa3d7ab7548f51e3e139c5cb5b81e1fbd699c7db9b5`
- E1 candidate: `ee1ff298fe7e57277c34a5af16df33165743d84f` (candidate only)
- S1 candidate: `5a505a911509073eb38102f0022f445e7ec602e5` (candidate only)

## Known limitations / retained holds

- No actual P2 batch was re-run. Tests use compact contract-compatible
  nonrespondent documents; HQ integrated tests must exercise real
  `RecursionCycle -> BatchEngine -> P3Owner -> P2Owner`.
- Compression is metadata only. It does not write P2 state, world state,
  psychological state, memory, claims or canonical history.
- An actual interval is required for `ACCUMULATED_INTERVAL`; it is validated
  as an actual P2Owner interval receipt with identity/time-window source basis
  and status, not generated here.
- `REPRESENTATIVE_EPISODE` requires a separately sourced recurring relation;
  no repeated acts or witness counts are manufactured.
- `RETROSPECTIVE_CRYSTALLIZATION` requires a fixed historical source before the
  present event; it does not form or recall an ADP-016 memory.
- `observed`/`unobserved` are scope metadata, not event admission or memory
  claims.
- No source/native/science/human authority is issued. No ADP-016/017 memory or
  claim authority; no production registry or protected receiving.

## Evidence / commit

- `evidence/compression/TEST_RESULTS.json`
- `evidence/compression/SOURCE_PINS.json`
- `evidence/compression/PASSPORT.json`
- `evidence/compression/RECEIPTS.json`
- `evidence/compression/API_EXAMPLE.json`
- `evidence/compression/pytest.log`
- `evidence/compression/MANIFEST.json`

**Commit:** `PENDING_ARTIFACT_COMMIT`  
After commit, push and verify this exact branch, then stop. This author pass is
not independent acceptance.
