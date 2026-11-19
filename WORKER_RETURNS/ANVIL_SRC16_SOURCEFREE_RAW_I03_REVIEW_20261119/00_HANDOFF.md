# SRC16 sourcefree raw / I03 independent review

## Verdict

**DEFECT — mapped parity is only a subset check and can silently lose mapped support.**

`common/shared_raw_lane_test.py:181` uses `raw_mapped <= base_mapped`.
The independent probe found:

- SAV raw substantive signatures: 1
- SAV base substantive signatures: 2
- raw subset of base: true
- raw equals base: false
- test `mapped_matched_rows`: **true**

The raw fixture deliberately strips one mapped response rule, but the test
never compares mapped cardinality or full signature equality. A mapped row can
disappear while the test passes. Smallest fix: require `raw_mapped == base_mapped`
and compare both counts, or preserve all base mapped rules in the raw lane
fixture/signature proof.

## What passes

The exact sourcefree raw round-trip passes for the two fixture shapes:
SAV 3 events, DTA 4 events, unresolved/missing preserved, raw witness present,
invalid physical state refused, cold reopen true. No raw tokens or source reads.

The actual saved I03 guard passes:
- unresolved mixed before denominator 1/risk 2 → after denominator 0/risk 0 held;
- unresolved NOT and positive similarly held;
- known missing NOT unchanged;
- standalone diagnostic unchanged;
- mapped NOT remains legitimate `ZERO_SUPPORT`;
- held results are not consumed as true zero.

## Coverage not proven

`i03_consumer_guard_test.py:151` builds only a single-target query `("Y",)`;
no target/joint case is exercised. Raw signatures include native/canonical/
component/occurrence fields, but no fixture explicitly varies those matches.
This is bounded sourcefree evidence, not full coverage.

No original source, private census, frozen-tree edits, author-branch edits,
raw token publication, or source reads were performed.
