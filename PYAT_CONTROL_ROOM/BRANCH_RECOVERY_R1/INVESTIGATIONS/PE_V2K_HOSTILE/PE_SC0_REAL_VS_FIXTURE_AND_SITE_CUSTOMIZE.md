# PE-SC0: real source semantics vs fixture overlay vs sitecustomize

## Verdict first

The 13/13 strict fixture result is **reproduced** and the 9/9 author fault
court is **reproduced**. The overlay is nevertheless **not engineering-ready**:
it accepts altered world values without selection binding, accepts inconsistent
denominators, synthesizes H2 refresh receipts without executing refresh, leaves
`result_hash` over the original rather than enriched receipt, and can be
auto-injected into any Python process by `sitecustomize.py`.

The 13/13 result proves receipt-field presence at fixture grade. It does not
prove that the enriched world, refresh, status or consumer fields are authentic.

## Lineage and exact cuts

| Item | Exact value |
|---|---|
| Startup / review base | `87755f02ec5c37499b09e80db6fbdcc9316a6b15` |
| Current PRE-MAIN recheck | `d0342290b257f85c3e8931f9962e0aecabc84ed3` |
| `rawlsing_next` tree at both cuts | `1d88d3fbb1d18dadfda946d9cd7f309d84afa479` |
| Original PE commit | `e61a26ce24f023a53d6b116bb9eca2fb7b6f8e65` |
| PE source blob | `58484f4c3d9aae148d4116dcf00420c432aefcbd` |
| Strict court blob | `d2fe653dadf94893b0fdfd268f36683f8dfed9af` |
| Author court blob | `92f59875583bf513c6fdbcd3ad7fe2b49e45e212` |
| Overlay return commit | `9c030bf4c239d2e14f2b5a8a02ff7b44906cd0c7` |
| Overlay implementation blob | `1e4c0e63b34192f77bf6554d43afb3c56828b29c` |
| `sitecustomize.py` blob | `3bac38dde1cc49d3a2f85a21ba7984410688d3ff` |
| Original fixture blob | `c9674d5fe9d01621eda0fdb4a999391eba422d92` |
| Patched fixture blob | `83984e7b3719f350cb735a9d80b0a83560576a47` |

The original PE source is not imported by current `rawlsing_next`; the overlay
is a sourcefree branch artifact under
`WORKER_RETURNS/PYAT-R3-PE-SC0-EIGHT-STRICT-REPAIR/`.

## What is real

- The PE request/refusal law in the pinned source is real executable code.
- The C1/N10E numeric geometry is real for the synthetic fixture source. The
  overlay copies the original `consumer_exact_geometry`, not the HQ298 54/60
  world baseline: reverse `P1` 48/64; conception target `yes` 21/30.
- The positive controls are real:
  - forged reversal authority -> `TYPED_REFUSAL` with
    `REVERSED_UNAUTHORIZED_ROLE`, no geometry, no overlay;
  - invalidated current -> `INVALIDATED_CURRENT_REFUSED`, no overlay;
  - as-of at request time -> `FUTURE_TIME_AVAILABILITY_REFUSED`, no overlay;
  - missing producer/consumer and removed negative status fail closed.
- The strict and author test files are byte-identical to the pinned blobs. Only
  the fixture support patch is applied.

## What is fixture-only

| Enriched field | Actual source | Status |
|---|---|---|
| `absolute_horizon`, `native_strata`, `nary`, `f2`, sanctions, categories, alternatives | HQ298 `BASELINE_WORLD` fixture | Test fixture only |
| `binding_echo` | HQ298 generated-binding fixture | Runtime echo; not source |
| `clocks` | HQ298 time axes + PE `request_time` | Synthetic coordinates; actor clock null |
| `scoped_status_rows` | HQ298 negative-state fixture | Test algebra only |
| `n9_values_read_receipt` | HQ298 ProviderA consumer read | Fixture keys/digest |
| `consumer_effect`, `generic_consumers` | HQ298 two fixture consumers | Not a PE empirical consumer or actor |
| `structural_publication_refresh_receipt`, `generated_binding_refresh_receipt` | `_refresh_receipts()` synthesis | **No executed H2 refresh** |
| Reversal authority | Test-only `make_role_reversal_snapshot()` | Unrestricted synthetic issuer |

The overlay itself labels most values `TEST_FIXTURE_ONLY__SOURCEFREE__NOT_OPERATIVE_N9__NOT_MODEL_USE`.
That grading is correct, but it is a limitation, not production semantics.

## `sitecustomize.py` is auto-injection, not a test fixture boundary

`candidate/sitecustomize.py` does only this:

1. insert its own directory into `sys.path`;
2. import `sc0_pe_overlay`;
3. call `sc0_pe_overlay.install()`.

`install()` (`sc0_pe_overlay.py:351`) saves the original PE function and replaces
the module-global `serve_generic_world_situated_possibility` with the overlay
wrapper. There is no environment guard, no `TEST_ONLY` check, no explicit
`pytest` plugin boundary, and no uninstall.

Reproduced attack: an ordinary Python subprocess with the candidate directory on
`PYTHONPATH` printed:

```text
True
sc0_pe_overlay
```

without importing the overlay itself. Any process that inherits such a path is
monkeypatched. This is a deployment hazard even though the file is not merged
into PRE-MAIN. **Do not merge or globally install `sitecustomize.py`.**

## Test authority is an unrestricted synthetic issuer

The fixture patch registers a `TARGET_USE_PERMISSION` snapshot with:

- `scope_envelope.target_use_refs = EXPLICIT_UNRESTRICTED`
- `scope_envelope.predicate_or_risk_set_refs = EXPLICIT_UNRESTRICTED`
- `effective_time_or_interval = ALL_TIME`

`_competent()` (`sc0_pe_overlay.py:302`) then accepts the same authority ref for
an attacker-selected target/risk pair. The hostile test confirms this. That is
acceptable only as a test double. It is not a real issuer and must not be
registered in a production authority store.

## Integrity defects reproduced

### 1. Altered world accepted without selection binding

`_n9_world()` (`sc0_pe_overlay.py:102`) copies fields from
`bundle["world_receipt"]["world"]` without checking that they hash to the
selection digest or a pinned provider digest. A monkeypatched bundle changed
`absolute_horizon` to `fx:ATTACKER_AH` and public sanctions to
`fx:sanction:attacker`; the receipt carried both while retaining the original
selection digest. This is **invented world data**.

### 2. Inconsistent denominator accepted

`_validate_geometry()` (`sc0_pe_overlay.py:87`) checks only that the first cell
numerator is a `int <= denominator`, and that the denominator record repeats the
same number. It does not check cell sums, per-cell fractions or denominator
membership. A forged geometry with cells `1 + 1` and denominator `100` was
accepted and emitted as the exact N10E denominator. This is a numeric integrity
failure.

### 3. Refresh receipts are synthesized, not executed

`_refresh_receipts()` (`sc0_pe_overlay.py:143`) constructs
`structural_publication_refresh_receipt` and
`generated_binding_refresh_receipt` from the selection digest, time axes and
generated-binding echo. It never calls the provider's
`refresh_publication_generation()` or `refresh_binding_generation()`.

A `NoRefreshProvider` whose refresh methods raise still yields both receipts at
generation 0. The strict court only checks that the fields exist and differ.
This is **fabricated refresh evidence**.

### 4. `result_hash` does not cover the enriched receipt

`EnrichedResult` delegates `result_hash` to the original result through
`__getattr__`. The original property hashes the original receipt ref, while
`result.receipt.ref` is the enriched receipt ref. The hostile test shows:

```text
result.result_hash != hash({request_ref, enriched receipt.ref, result_state})
```

The enriched fields are outside the result identity. A replay/identity consumer
can bind the original receipt while reading enriched material.

### 5. Source-promotion flag is overwritten, not refused

The overlay always writes
`binding_echo.may_use_as_source_observation = False`. If a provider supplies
`True`, the overlay silently suppresses it rather than refusing the contradictory
producer. The output is safe in that field, but the producer fault is hidden.

### 6. Negative-status scope is not validated

A `HELD_AUTHORITY` row with `scope=None` is accepted and copied. The required
state set passes, but the source/risk coordinate is lost. This is shape-only
status algebra.

### 7. Replay is deterministic

The same request produces the same 13/13 enriched receipt hash. PE is a pure
sourcefree boundary with no nonce; replay is not prevented. This is a limitation
of any currentization, not a current production grant.

## Positive controls preserved

- Wrong issuer is refused before enrichment.
- Invalidated current and future as-of are refused by the original PE path.
- Missing producer, severed consumer and removed negative status fail closed.
- `upstream_authorship=True` is refused; only the `may_use_as_source_observation`
  flag is overwritten.
- The original 21/21 author suite remains green with the overlay and patched
  fixture.

## Real-vs-fixture conclusion

Recoverable into a legitimate current sourcefree successor:

- PE refusal law and request/target direction checks;
- exact PE/C1/N10E geometry;
- value-carrying fields **only** under a future owner provider with digest-bound
  world values and real consumer read receipts.

Not recoverable from this overlay:

- operative N9 world identity or source values;
- real H2 refresh events;
- real negative-status determinations;
- a real reversal issuer;
- production result identity over enriched fields;
- a claim that 13/13 means the pinned PE contract is production-ready.

## Engineering / scientific / authority

- **ENGINEERING RED**: 13/13 fixture reproduction is real, but altered-world,
  denominator, refresh, result-hash and sitecustomize defects block acceptance.
- **SCIENTIFIC HOLD**: all world/consumer values are synthetic fixture values.
- **AUTHORITY HOLD**: test-only unrestricted reversal grant is not an issuer;
  no source, actor, model, N9/N10W or production adoption.
