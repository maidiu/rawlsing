# Positive and fault-negative receipts

All execution was sourcefree and fixture-grade. No original survey/response
bytes, production source, actor/world permission or PRE-MAIN mutation was used.
No assertion was skipped, xfailed or replaced.

## Exact-tree construction

`repro/run_overlay_courts.sh` performs this fixed sequence:

1. `git archive e61a26ce... rawlsing_next` into a temporary tree.
2. Verify the PE module blob `58484f4c...`, strict court `d2fe653d...`, author
   court `92f59875...` and original fixture `c9674d5f...`.
3. Apply only `candidate/PE_TEST_FIXTURE_AUTHORITY.patch`; verify the patched
   fixture blob `83984e7b...`.
4. Copy `candidate/sc0_pe_overlay.py`, `candidate/sitecustomize.py`,
   `candidate/port/` and `candidate/oracles/` into the temporary tree.
5. Run with `HQ297_EXACT_PE_ROOT=<temp-tree>`, `PYTHONPATH=<temp-tree>`,
   `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`.

The overlay does not modify the PE module. `test_pinned_pe_module_stays_byte_identical`
independently checks blob `58484f4c...` during the overlay court.

## Original pinned PE: red receipt

Command:

```bash
./repro/run_original_red.sh
```

| Court | Actual result | Exit |
|---|---|---|
| Author 21 | **21 passed** | 0 |
| Independent strict 13 | **4 passed / 9 failed** | 1, expected |

The nine original failures are the eight SC0 value-bearing/schema assertions
plus `test_strict_reverse_scoped_issuer_forgery_must_refuse`. They are preserved,
not converted to xfail.

Artifacts: `repro/original_author_21.log`, `repro/original_author_21.junit.xml`,
`repro/original_strict_4_of_13.log`,
`repro/original_strict_4_of_13.junit.xml`,
`repro/original_strict_exit.log`.

## Overlay candidate: green receipt

Command:

```bash
./repro/run_overlay_courts.sh
```

| Court | Actual result | Exit |
|---|---|---|
| Author 21 | **21 passed** | 0 |
| Independent strict 13 | **13 passed** | 0 |
| Overlay positive + fault negatives | **9 passed** | 0 |

Console summary (timings vary per run; the committed logs are authoritative):

```text
21 passed
13 passed
9 passed
```

Artifacts: `repro/author_21.log`, `repro/strict_13.log`,
`repro/overlay_faults.log`, the corresponding `*.junit.xml` files, and
`repro/test_summary.json`. JUnit summary:

| Suite | Tests | Failures | Errors | Skipped |
|---|---:|---:|---:|---:|
| `original_author_21` | 21 | 0 | 0 | 0 |
| `original_strict_4_of_13` | 13 | 9 | 0 | 0 |
| `author_21` | 21 | 0 | 0 | 0 |
| `strict_13` | 13 | 0 | 0 | 0 |
| `overlay_faults` | 9 | 0 | 0 | 0 |

## Positive overlay tests

| Test | Actual evidence |
|---|---|
| `test_positive_overlay_uses_pe_reverse_geometry_not_world_baseline` | Reverse `P1` numerator 48 / denominator 64; clocks exact; overlay grade/provenance present |
| `test_positive_overlay_keeps_conception_pe_denominator` | Target `yes` 21/30, `no` 9/30, denominator is not 60 |
| `test_pinned_pe_module_stays_byte_identical` | PE blob remains `58484f4c...` |

## Fault negatives

| Test | Fault injected | Actual result |
|---|---|---|
| `test_wrong_issuer_refuses_before_enrichment` | Forged unissued reversal `AuthorityRef` | `TYPED_REFUSAL`; `REVERSED_UNAUTHORIZED_ROLE`; geometry `None`; no `sc0_overlay` or values-read field |
| `test_invalidated_snapshot_gets_no_stale_clock_or_value_enrichment` | `n9_snapshot_state = INVALIDATED` | `TYPED_REFUSAL`; `INVALIDATED_CURRENT_REFUSED`; no `clocks`, no `scoped_status_rows`, no overlay |
| `test_missing_producer_fails_closed` | Remove `world_receipt` from bundle | `Sc0OverlayContractError: MISSING_WORLD_SELECTION_DIGEST` |
| `test_consumer_severance_fails_closed` | Remove nonparent consumer effect | `Sc0OverlayContractError: MISSING_CONSUMER_EFFECT:NONPARENT_APPRENTICESHIP_ENTRY` |
| `test_generated_binding_echo_source_promotion_fails_closed` | Set `upstream_authorship = True` | `Sc0OverlayContractError: GENERATED_BINDING_ECHO_SOURCE_PROMOTION` |
| `test_missing_publication_clock_fails_closed` | Remove `time_axes.published` | `Sc0OverlayContractError: MISSING_PUBLICATION_CLOCK` |

These tests prove the overlay fails closed rather than fabricating a receipt
when the authority, currentness, producer or consumer evidence is missing.

## Test-fixture authority patch

`candidate/PE_TEST_FIXTURE_AUTHORITY.patch` adds a test-only
`make_role_reversal_snapshot()` and registers it in the positive fixture
registry. This is required to exercise a **lawful** positive reverse path after
the `_auth` defect is closed. It changes no strict assertion and does not grant
production authority. The strict court blob stays `d2fe653d...`; only the
fixture setup blob changes from `c9674d5f...` to `83984e7b...`.

## Not run / not claimed

- Full HQ298 K9 8/K10 28 port court: **NOT RERUN** in this return. The runtime
  port and oracles are blob-identical to `b15dbbc4...`; only the overlay path
  exercising the port is executed here.
- Native source/U/E, original survey bytes, source-release proof, real
  actor/world state, N10W joint model use, N11/N12 and V3 wake: **NOT RUN**.
- Production integration or PRE-MAIN merge: **NOT PERFORMED**.
- The 13/13 green is a sourcefree overlay result against the pinned PE source,
  not evidence that the pinned PE contract itself implements SC0 semantics.
