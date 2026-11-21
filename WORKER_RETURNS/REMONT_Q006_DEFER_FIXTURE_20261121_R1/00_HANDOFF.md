# Q006 persisted-DEFER fixture — exact earliest fault

## Result

**`PERSISTED_DEFER_FIXTURE_BUILT__PRODUCT_IMPORT_FAULT`**

The canonical persisted-DEFER fixture was built and tested at exact
`851cdc0d5c97d1a8a140dce5bbbdb803cf6a972d`. No product code was changed.

The fixture:

- uses the existing physical `_Sink`/`_IndexSink` carrier format;
- writes a historical `SOURCE_SEMANTICS_TOPOLOGY` `DEFER` AuthoritySnapshot;
- writes an `EmpiricalUniverse` whose authority refs include that exact DEFER;
- uses the seven recorded codes `1,2,3,4,97,98,99`, explicit system missing,
  and an absent respondent;
- writes exact family rows, locator, manifest and independent pins.

## Exact earliest fault

After fixture construction the actual candidate import fails:

```text
ImportError: cannot import name 'HeldRecordedOperation' from
'rawlsing_next.pre553_anvil_stream_recorded'
```

The installed cut no longer exports the `HeldRecordedOperation` class used by
the actual recorded entry test. This is a product-code cut fault, not a
fixture fault; no monkeypatch or local substitute was used.

No original SRC04/SRC16 body was read. No real query or I03 was run.

## Test

`rawlsing_next/tests/test_pre553_anvil_stream_recorded_defer_fixture.py`

The test builds the fixture first, asserts the persisted DEFER/universe and
manifest, then reaches the product import fault. JUnit and run logs are in this
return.

## Next

A separate product author must restore/export the intended
`HeldRecordedOperation` surface at the exact candidate cut; this fixture is
canonical and can be replayed unchanged.
