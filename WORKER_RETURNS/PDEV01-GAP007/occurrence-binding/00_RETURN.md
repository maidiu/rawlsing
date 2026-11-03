# GAP-007 P1 conditional/joint occurrence binding — sourcefree attempt

**Base commit:** `d3d6e48791623478fd1d838c7e95a72b77b5cd74`
**Review read:** `3aa57b99a` in sibling `pyat-pdev01-gap007-review`
**Mode:** TEST_ONLY sourcefree; existing governed C11 projection/catalog and R03
`OccurrenceKey` construction reused.
**Verdict:** `HOLD_FIRST_EXACT_INPUT_MISSING`; no positive execution.

## Result

P1 preserves all 840 operations and the exact plan identity
`e0d4180cbfc43a1ddc5965ff20afb9cb284676c6c4981d9681d3e35121ac59ea`.

The 420 conditional/joint entries are fully accounted:

- CONDITIONAL: 210
- JOINT: 210
- `TYPED_REFUSAL`: 420
- Executed: 0
- Unsupported entries: 420

The accepted frozen source/C11 projection was rebuilt:

- Source SHA-256: `5009f3c9272dcbfb15a48b17cfff51f9afa67e60d6a2c1364c9aa07bc6732e4f`
- Rows/columns: 12 / 71
- Release: `64cf774b408686394c8caf9969f442b518e365d04c924bafefb6204239c9bf03`

## First exact input missing

**Artifact:** a governed P1 `SourceItem` → C11/R03 occurrence binding record with
exact `item_id`, `option_id`, `form_id`, `repeat_id`, addressed by
`SourceGrant.item_registry_ref`.

**Owner:** the P1 source-grant/ItemRegistry owner named by
`SourceGrant.item_registry_ref` (`urn:test:programma:itemregistry:g00` for the
first wave). The R03 policy/risk-set/direction owner is downstream.

Evidence:

- `0 / 420` P1 source items have an exact `SourceItem` identity in C11.
- `420 / 420` source-variable codes match C11 question codes, but that is a
  name/code match, not an exact `ExactRef`/occurrence identity.
- `0 / 35` P1 ItemRegistry URIs have registry content in the checkout.
- C11 carries scalar occurrence rules with only `kind/index`; it does not carry
  the P1 `SourceItem` refs or an option/form/repeat mapping.
- R03 `OccurrenceKey` candidates for `Q00A/Q00B` are therefore name-only
  candidates; they are not accepted exact identities.
- R03 `GrammarPolicy`, authorized direction grants, risk-set/denominator,
  form-scope/administration and joint/marginal query refs are also absent.

## Additional gates recorded

- P1 wave source identity vs C11 source: `0 / 420` equal. This is recorded as
  the existing TEST_ONLY source-identity substitution used by the prior GAP007
  distribution binding, not claimed as an exact production identity.
- Condition/joint value `0` occurs in 210 entries; C11 response domain is
  `1,2,3`, so even after identity resolution those values are not available.
  Value `1` occurs in 210 entries and is domain-available.
- C11 catalog probe successfully built two one-target query/predicate objects
  (`Q00B` target, `Q00A` condition). No conditional/joint query was fabricated;
  this probe is catalog-only and not execution.

## Files

- `replay_occurrence.py` — reproducible attempt.
- `01_ACCOUNTING.json` — all 420 entries, C11/R03 candidates, gates, counts.
- `attempt.stdout.log` — actual run output.
- `test_occurrence.py`, `test_occurrence.log`, `test_occurrence_junit.xml` — 3
  focused tests passed.
- `02_COMMANDS.md` — exact commands.
- `RECEIPTS.json` — file hashes.

No original source, production edit, policy, occurrence mapping, scientific
result, merge, CI or adoption was created. Distinct independent review remains
required for any positive execution claim; this return makes none.
