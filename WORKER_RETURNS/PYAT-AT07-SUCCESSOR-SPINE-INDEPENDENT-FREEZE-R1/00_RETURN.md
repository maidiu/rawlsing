# PYAT AT07 successor spine: independent freeze R1

Disposition: **PASS_AT07_SUCCESSOR_SPINE_INDEPENDENTLY_FROZEN__INDEPENDENT_REVIEW_REQUIRED**.
Terminal: `AT07_SUCCESSOR_SPINE_INDEPENDENT_FREEZE_RETURNED__HQ_ADJUDICATION_REQUIRED`.

For HQ: this package independently freezes the complete forward and reverse direct AT07 C1-02 identity preimages. It is submitted for independent review and HQ adjudication; it is not self-adopted.

| Direction | Successor SHA-256 | Unchanged historical R8 SHA-256 |
|---|---|---|
| forward | `01c381d3f3c386cfc22fd2f57b8e2c244771ddf1529d4f8ab8c7b1cf41bd50dd` | `03610f9d91b23cfb6f862dc91b5de92c7f4e4b8e44a53b9efdacb1cf73af6b9e` |
| reverse | `a3bd7e85ae14babb5ac5a12b0bcc57a8cdf3eccf8f43394895903dc43aca40ca` | `1202822cf98d802c04440328496dc64ee02e6d6030a3da6c9bf10ef1a6490a3c` |

## Navigation

- [01 — input custody](01_PINNED_INPUTS.json): 24 exact Git blobs, SHA-256 byte checks, original paths/commits, canonical primitive, source law and independence disclosure.
- [02 — frozen field law](02_OLD_NEW_PREIMAGE_FIELD_MANIFEST.json): static 38-to-44 key enumeration and exact six additions, frozen before successor digest derivation.
- [03 — complete forward object](03_FORWARD_SUCCESSOR_PREIMAGE.json) and [04 — complete reverse object](04_REVERSE_SUCCESSOR_PREIMAGE.json).
- [05 — versioned successor spine](05_SUCCESSOR_SPINE.json): immutable historical/current lineage and both successor digests.
- [06 — field-level succession matrix](06_DERIVATION_AND_SUCCESSION_MATRIX.json): all 44 fields in each direction, stable labels, JSON pointers, exact field-value hashes and source-law references.
- [07 — independent procedure](07_ORACLE_PROCEDURE.py): stdlib-only generation, verification and mismatch hostiles.
- [08 — hostile results](08_ORACLE_PROCEDURE_HOSTILES.json): 44/44 rejected, zero false accepts.
- [09 — execution receipt](09_EXECUTION_RECEIPT.json): exact tested commit, runtime, clean status, commands, results and persisted byte checksums.
- [10 — final disposition](10_FINAL_DISPOSITION.json): remaining review/adoption boundary.
- [Forward derivation materials](FORWARD_DERIVATION_PREIMAGES.json) and [reverse derivation materials](REVERSE_DERIVATION_PREIMAGES.json): full independent query, binding, 16-field witness, evidence, model-rule and consumer-result preimages; generated 100 synthetic rows and accepted upstream custody.
- Canonical digest inputs are [forward](FORWARD_SUCCESSOR_CANONICAL.json) and [reverse](REVERSE_SUCCESSOR_CANONICAL.json). Each file is exact UTF-8 JSON with no trailing newline. Historical canonical preimages are also persisted and reproduce both R8 digests.
- `INPUTS/` contains byte-identical inert copies of all cited blobs, including historical/current owner laws and provider custody. These files are never imported or executed.

## Independence and derivation

Commission: `f23a3ac051b18415e107b85dd2d4314ed169e712`, based from `87029d349c8a7385cb673060a8e5decd4eb528ff`. Astra's `A_VERSIONED_SUCCESSOR_SPINE` ruling is pinned at `a2e7767ecec9ecb6d241861628759f2e933920d5`. The adopted C1-02 analytical owner is blob `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b` at `bc661188b51e995d9f5d74e55c4e37d2ba358a17`.

The known join forward hash `01c381d3f3c386cfc22fd2f57b8e2c244771ddf1529d4f8ab8c7b1cf41bd50dd` was disclosed by the commission. It was not an input to the procedure, not copied as expected truth, and not compared to the generated oracle in this lane. No reverse successor digest was supplied; it was independently derived here.

1. Verify exact Git blob and SHA-256 identity for all 24 frozen inputs. Inspect both owner identity dictionaries statically with Python AST. Freeze their complete field sets before successor hashing.
2. Read accepted R8 producer query/fact/replay refs as conserved upstream custody. Independently rehash literal R8 predicate AST and outer projection. No producer, composition, fixture or consumer production function runs.
3. Rehash the R2/R3 authority and relation materials. Construct the consumer subject, seven-field binding, consumer query and complete 16-field witness from the pinned caller/consumer laws. Verify the conserved R8 query and witness identities.
4. Materialize exactly 100 synthetic rows: P1/yes 54, P1/no 6, P2/yes 8, P2/no 32. Independently reconstruct respondent, routing and response-event identities and the used-object provenance/dependency closure. Preserve canonical exact-ref order.
5. Select direction-specific denominator members; recompute cells and reduced exact rational probabilities. Construct full evidence, model rule and consumer result materials under static frozen laws. Verify both conserved R8 evidence refs.
6. Independently construct all 38 historical composed fields. Their complete canonical bytes reproduce both R8 historical digests. Add exactly six current direct-path fields: discovery receipt/handoff/lineage arrays empty, discovery frontier null, joint count 1, joint order `SEMANTIC_ORDERED`. Hash the complete 44-key successor material.
7. Verify persisted canonical bytes and every derivation material. Attack omissions and wrong values for each addition in each direction, source/release/witness/authority refs, serialization/key/array ordering, old-owner substitution and frozen input blobs. All 44 attacks must reject.

The primitive is an independent JSON-only Python stdlib equivalent of pinned `pre553_empirical_objects.py` canonicalization: recursive sorted string keys, preserved arrays, UTF-8, compact separators, unescaped Unicode, forbidden floats/NaN, SHA-256. Production identity projection is not shared. Exact fractions are reduced to literal `$exact_fraction` integer arrays.

## Conservation and downstream boundary

All 38 historical fields remain canonically equal in each direction. No existing field changes, no keys are removed. The six additions cause a new composed digest; historical digests are not aliases of the successor. Nested witness class evolution is distinguished from this top-level delta; its literal 16-field AT07 material remains conserved.

Both original R8 spine bytes and every source/authority/relation freeze remain unchanged. The source law stays yes 54/60 forward and P1 54/62 reverse. `rawlsing_next/**` is untouched; all writes remain under this return directory. No raw sources, AT17 requalification, provider execution or C1-03 join were accessed/run. Evidence and consumer-result identities do not bind the composed identity and remain conserved. Downstream provider/AT17 identities that bind the successor are deliberately left to a separately authorized lane after independent review and HQ adoption.

## Reproduction

Run from any working directory with Python 3.11.3, using this package's absolute procedure path:

```text
python3 <package>/07_ORACLE_PROCEDURE.py generate
python3 <package>/07_ORACLE_PROCEDURE.py verify
python3 <package>/07_ORACLE_PROCEDURE.py hostiles
```

`generate` deterministically writes only core artifacts in this package. `verify` and `hostiles` are read-only. The receipt identifies exact commands and the final tested artifact commit. The subsequent receipt-only commit avoids a circular self-referential commit hash; the worker's final return identifies and verifies the published final SHA.
