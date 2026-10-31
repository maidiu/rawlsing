# Original PE vs current PE-SC0 overlay candidate

## Scope and lineage

- Original PE source: commit `e61a26ce24f023a53d6b116bb9eca2fb7b6f8e65`; module
  `rawlsing_next/pre553_postastra_pe_generic_world_possibility.py`, Git blob
  `58484f4c3d9aae148d4116dcf00420c432aefcbd`.
- Original strict court: `rawlsing_next/tests/test_hq297_k9k10_sc0_pe_independent.py`,
  blob `d2fe653dadf94893b0fdfd268f36683f8dfed9af`.
- Original author court: `rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py`,
  blob `92f59875583bf513c6fdbcd3ad7fe2b49e45e212`.
- Current target branch at startup:
  `agent/pyat-r3-pe-sc0-eight-strict-failure-repair-20261031-r1` @
  `5fc1d43e3d5412194d1f1eaa30ff448f84635e99`. This cut does not contain the PE
  candidate source or its strict court.
- PRE-MAIN intake at return start: `87755f02ec5c37499b09e80db6fbdcc9316a6b15`.
  No PE/V2K production source was added by this return.
- HQ298 SC0 port source: commit `b15dbbc4f07ae79e9ffb71e88e91e3b28b35da59`,
  branch `agent/rabochii-sorok-r3-hq298-sc0-value-bearing-port-r1`; the
  runtime files under `candidate/port/` and `candidate/oracles/` are
  13/13 blob-identical to that commit (`repro/port_source_manifest.json`).

The candidate is an **overlay**, not an edit of the pinned PE module. The
overlay runs only after the original PE service returns `EXACT_SUPPORTED`;
the original PE receipt remains the source of numeric C1/N10E geometry and
role/refusal semantics.

## Field-by-field source comparison

| Strict field | Original PE | Overlay candidate | Actual source used |
|---|---|---|---|
| `absolute_horizon` | absent | `fx:AH` | HQ298 `BASELINE_WORLD` fixture value |
| `native_strata` | absent | `["fx:stratum:A", "fx:stratum:B"]` | HQ298 fixture world |
| `nary` | absent | `fx:f1:three-party`, ordered cardinality 3 | HQ298 fixture world |
| `f2` | absent | `fx:f2:separate`, deferred/unbound | HQ298 fixture world |
| `public_sanctions` | absent | fine and exclusion refs | HQ298 fixture world |
| `public_categories` | absent | license and recognized-club refs | HQ298 fixture world |
| `contradictory_alternatives` | absent | two alternatives with witnesses | HQ298 fixture world |
| `binding_echo` | absent | runtime-fact tag, `may_use_as_source_observation: false` | HQ298 generated-binding fixture |
| `clocks` | absent | observation 2008, publication 2010, actor `null`, request `2026-10-14` | HQ298 time axes + PE `request_time` |
| `scoped_status_rows` | absent | all eight required states, `DENIED` mapped to `DENIED_USE` | HQ298 negative-state algebra |
| `native_sampling_unit` | absent | `RESPONDENT` | HQ298 fixture world |
| `native_risk_set_ref` | absent | `fx:risk:asked_eligible` | HQ298 fixture world |
| `original_routing_ref` | absent | `fx:routing:asked` | HQ298 fixture world |
| `structural_publication_refresh_receipt` | absent | H2 publication channel, generation 0, successor ref | HQ298 H2 fixture channel |
| `generated_binding_refresh_receipt` | absent | distinct H2 binding channel, generation 0, successor ref | HQ298 H2 fixture channel |
| `n9_values_read_receipt` | absent | four fixture rule/route keys, digest `c5fd82a9...` | HQ298 consumer `values_read` |
| `n10e_values_read_receipt` | absent | exact PE geometry, not the SC0 54/60 baseline | Original PE/C1 receipt |
| `consumer_effect` | absent | both fixture consumers keyed by consumer id | HQ298 generic fixture consumers |
| `generic_consumers` | absent | nonparent route constraints and conception input-only constraints | HQ298 generic fixture consumers |

## Exact N10E geometry correction

The earlier SC0 port baseline was 54/60. That is **not** the PE consumer
geometry and is not used for `n10e_values_read_receipt`.

Actual PE receipt values used by the overlay:

- Law A nonparent reverse: cell `P1` numerator 48, denominator 64; `P2` 16/64.
- Law A conception scenario: target cell `yes` numerator 21, denominator 30;
  `no` is 9/30.

The overlay copies the full cell list and the denominator record from
`result.receipt.consumer_exact_geometry`. The numerator recorded at the top
level is the direction-appropriate target cell: `P1` for reverse, `yes` for
forward/multi fixture cases.

## Consumer comparison

| Aspect | Original PE | Overlay candidate |
|---|---|---|
| Numeric consumer | Exact C1/N10E receipt, role/target direction preserved | Same original receipt; overlay does not recompute or replace it |
| World values | N9 dependency identity only; no value-bearing world fields | Reads HQ298 fixture rules, AH, routes, categories, sanctions, strata and alternatives |
| Generic consumers | None | Two fixture consumers actually read fixture values: nonparent apprenticeship route constraints and conception-scenario input-only constraints |
| Person/actor output | No actor/person state in the PE contract | `person_generation: NONE`; no generated learner, parent, partner or biography; no actor authority |
| Values-read proof | No consumer values-read receipt | `n9_values_read_receipt` keys/digest plus full `consumer_effect` and `generic_consumers` entries |

## Test-fixture support change

The strict test file and assertions are unchanged. The only test support
change is `candidate/PE_TEST_FIXTURE_AUTHORITY.patch`, which registers one
test-only `TARGET_USE_PERMISSION` `AuthoritySnapshot` for the positive
reverse fixture. Without that snapshot, the repaired reverse path correctly
refuses because the caller's `AuthorityRef` is not a positively scoped issuer
grant. This is **fixture registration only**, not production authority and not
an assertion change.

The patched fixture blob is `83984e7b3719f350cb735a9d80b0a83560576a47`;
the original fixture blob is `c9674d5fe9d01621eda0fdb4a999391eba422d92`.
The pinned PE module remains `58484f4c...` and the strict court remains
`d2fe653d...`.

## Authority boundary

No original survey/response bytes, source release, source owner permission,
operative N9 current, N10W joint model use, actor/person model, N11/N12,
V3 wake, production adoption or merge is claimed. All world and consumer
values are synthetic HQ298 fixture values at grade
`TEST_FIXTURE_ONLY__SOURCEFREE__NOT_OPERATIVE_N9__NOT_MODEL_USE`.
