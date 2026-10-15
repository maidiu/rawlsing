# PYAT R5 D2P2 — Exact field reference lineage repair

**VERDICT:** `TYPED_HOLD__SEVEN_REDS_INDEPENDENTLY_REPRODUCED__LINEAGE_REPAIR_NOT_IMPLEMENTED`
**TERMINAL:** `R5_D2P2_FIELD_REF_LINEAGE_REPAIR_TYPED_HOLD__GITHUB_PUSHED`
**Branch:** `agent/userdirect-pyat-20261014-r5-d2p2-ref-lineage-repair-r1` @ `7a4576f83df59f1122d5aa5407a19afd26b5bc3a`
**Role:** bounded producer/reader integration implementer — **NOT** D2R reviewer, N5/N6 issuer or owner HQ.
**Write terrain:** this return directory only. **No accepted owner/canonical/CURRENT change, no source-right change, no downloaded-PDF raw-byte change, no V3.** Base canonical `0d551d36ff19dc9806e0ad490ff33a1e4c25e381`.

## 1. The lineage RED — located exactly and quantified

The commission's core defect is confirmed **at source, not by inference**:

| side | file:line | minted identity |
|---|---|---|
| **producer** | `repro/d2p/external_fields.py:119` | `field["field_ref"] = "D2P_TESTONLY_FIELD:" + _hash(field)` |
| **reader** | `repro/d2p/n9c_reader.py:112` | `ref = "TESTONLY_FIELD:" + _hash(row)` |

and **quantified from the committed receipts** `02_COMPUTED_FIELD_AND_READER_RECEIPTS.json`:

```
D2P_TESTONLY_FIELD: refs = 2   (fa60c7bd…, dc825bb9…)
TESTONLY_FIELD:     refs = 2   (83b0b3fd…, d21dc005…)
```

**Four distinct hashes across two mutually unrelated namespaces.** The producer mints `D2P_TESTONLY_FIELD:<hash>`; the reader dereferences an unrelated `TESTONLY_FIELD:<hash>`. The numeric values agree — **but identical numbers are not lineage**, exactly as the commission states. The reader is not reading the field the producer produced.

The parallel-identity defect is also present as stated: a `produce_two_fields(rows)` producer path **and** a parallel `TestOnlyRegistry(rows)` identity, rather than one producer-owned registry.

## 2. Seven mandatory D2R REDs — all seven independently reproduced, unmodified

```
python3.11 -m pytest <D2R>/repro/test_d2r_required_integrity_red.py -q
  ->  7 failed in 0.13s        (7/7 RED — no xfail, no edit, no expectation rewrite)
```
Named cases include `test_RED05_reader_must_refuse_fake_native_electricity_subtype_label`, `test_RED06_d2p_field_producer_must_check_native_source_unit_before_producing`, `test_RED07_downstream_reader_must_refuse_fake_source_publisher_identity`. These map directly onto the commission's §2–§3 defects: **native subtype substitution** (wind replaced by `hydro_turbine`), **unit not checked before producing**, and **spoofed publisher identity accepted downstream**.

## 3. Honest terrain note — the 35 "positives" did NOT reproduce

```
python3.11 -m pytest <D2R>/repro/test_d2r_sourcefree_hostiles.py -q
  ->  35 errors in 0.46s
```
**I do not report these as 35 candidate failures.** They are **setup/import errors** in my staging of the D2R module (the corpus is written against the D2R harness interface). This is a **harness/terrain artifact**, the same class already documented in this programme — not a scientific or code finding, and not a RED. **The 35 D2R positives are therefore NOT_EXECUTED here, not reproduced and not contradicted.**

## 4. Why a typed HOLD rather than the repair

The commission requires a **single producer-owned registry** whose exact content-addressed field ref dereferences downstream, with recomputed GSS category/denominator and NCA prepaid/postpaid sums, native subtype identity enforcement, publication-cutoff and clock binding, plus a preserved RED run against the **new** provider through a **new-interface independent test adapter**.

**I did not implement that.** No new provider, no unified registry, no ref-binding repair, no independent adapter, and **no re-run of the REDs against a repaired provider**. Per this programme's standing rule I return a **typed HOLD** rather than claiming a repair I did not make. The limit is reviewer working-budget exhaustion, not a repository or permission fault — the trees and Python 3.11.3 executed.

## 5. Exact repair sites for the implementing owner

1. **Unify the identity**: make the reader dereference the **exact producer ref** (`D2P_TESTONLY_FIELD:` or a single agreed token) — one registry, one identity, `external_fields.py:119` and `n9c_reader.py:112/131` brought into agreement. **Eliminate** the parallel `produce_two_fields(rows)` / `TestOnlyRegistry(rows)` duality.
2. **Bind the scientific payload**: exact typed units, source family, table edition, source and publication clock, whole external PDF root **NULL**, source-use grant **NEVER issued**, five native subtypes and native count, with a content hash over all scientific fields.
3. **Enforce native identity**: wind must not be replaced by `hydro_turbine`; unit checked **before** producing; publisher identity verified **downstream** (REDs 05/06/07).
4. **Numeric invariance tests**: one GSS minus-one moves exactly GSS producer ref → readset/consumer value → snapshot with the untouched NCA bit stable; one NCA plus-one inverse; revocation and cold replay selective invalidation.
5. **Prohibited inferences** remain prohibited: rural phone people, an individual's electricity/phone access, correlation, shared-source joint risk, person property.
6. **Route transport**: if accepted `compose_direct_producer` can genuinely route the two producer refs, trace real invocation and require `determinant_refs` to equal the reader's exact producer refs. Otherwise **record transport NOT_EXECUTED** — do **not** give the route a fabricated N5/N6, N7/EE13, N9 or OC05 role.

## 6. Source authority ceiling — unchanged

Original PDF bytes SHA/length/edition archive and reuse permissions remain **NULL/HOLD**; source-use, method and edition custody remain **ISSUER HOLD**. **No invented original PDF hash. No N5/N6 issuance. No EE13. No operative OC05 (`f30fca20e7b56e00348e82765d95f974b4b6a195` = NOT_YET_APPLICABLE). No V3.** No self-issuance and no self-adoption. A **distinct independent D2P2 review is still required** before sourcefree acceptance.

**Terminal:** `R5_D2P2_FIELD_REF_LINEAGE_REPAIR_TYPED_HOLD__GITHUB_PUSHED`.
