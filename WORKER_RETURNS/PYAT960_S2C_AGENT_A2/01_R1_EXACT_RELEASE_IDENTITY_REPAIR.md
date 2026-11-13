# PYAT S2-C Agent A2 R1 — exact release-identity repair return

**Scope:** bounded causal repair of the local runner's exact A2 native-I03 first-consumer failure; preserve B-F01–F04 and original S2-C G1–G5. No new commission, no original35 grant, no protected merge.

## Immutable evidence and ancestor

- Original A2 frozen executable: `1d42f63ab62568e61f77f5d3f27d9df6008f91e3` — local qualified Linux runner **27 collected, 22 PASS, 5 FAIL**, native direct sourcefree/v1 release identity mismatch; inherited **91/91 PASS**. Not a VM or PyArrow failure. Original frozen SHA is unchanged.
- Independent local runner observed `i02.release = C11_DIRECT_SOURCEFREE_RELEASE|...`, while the native I03 oracle needed `C11LogicalRelease|...`. In the S2-B temporary SQLite certificate `header.reconstructed_v1_release_ref` **exactly equals the native oracle**. That certificate was deleted before the old Parquet manifest persisted this identity.
- Runner's uncommitted **simulation** of a minimal persistence/binding correction produced **27/27 focused + 91/91 inherited PASS**, with independent H1/H2/H3 native fact/restore tests green. This is **not** executable evidence for the committed R1 descendant.
- A2 R1 executable code + tests exact SHA: `8375e260e55da09b3c5a89122839d8c7deba67bb`. This return is a later documentation-only commit. Branch `agent/pyat960-s2c-agent-a-counter-20261113-r1`, draft [PR #990](https://github.com/maidiu/rawlsing/pull/990), base frozen B `4c998d40a3d6925657df2fabd649a98123e8dffd` on isolated review base. Protected PRE-MAIN, B branch/PR #987 and paused W03/W04 untouched.

## Exact applied correction

1. **Preserve both legitimate release identities.** The direct-I02 `ExternalI02Roots.release` stays unchanged, with kind `C11_DIRECT_SOURCEFREE_RELEASE`. It is not renamed as, or promoted to, a native v1 validation seal.
2. **Bind the actual historical identity before deleting proof scratch.** `write_direct_estate` reads only `reconstructed_v1_release_ref` and supporting exact header identities from the temporary source-direct I02 certificate, only after verifying its bytes against the S2-B `i02.physical` SHA-256. Exact header release/source/replay/universe/schema/source-manifest/reconstructed-replay must agree. The reconstructed ref is validated as `C11LogicalRelease` with the original declared release ID and a canonical SHA-256 digest.
3. **Persist that identifier in the existing single physical manifestation.** The durable `manifest.json` now includes `reconstructed_v1_release_ref`; it is bound to the independently held manifest SHA. The ordinary `EstateReceipt.reconstructed_v1_release_ref` and `VerifiedDirectEstate.reconstructed_v1_release_ref` expose this scoped historical identity. No permanent SQLite or duplicated body store is added.
4. **Use the right identity at actual native I03 consumers.** `CarrierNeutralResearchExecutor.__post_init__` and `DirectEstateI03Session.indices_for` compare/bind the historical v1 ref instead of trying to parse `i02.release` as a `C11LogicalRelease`. The direct I02 proof/manifest identity and sourcefree authority limits remain separately enforced.
5. **Correct the original faulty test.** Assert `receipt.reconstructed_v1_release_ref == native_oracle_release_ref` AND `receipt.i02.release != native_oracle_release_ref.key`. The fresh-interpreter test still transports externally pinned roots and actual query/authority preimages, not a reconstructed full C11 repository.
6. **Add two adversarial negatives.** A rehashed/repinned physical manifest attempting to substitute the direct release as historical v1 must refuse; a modified SQLite historical-release header after the S2-B physical digest is computed must refuse before Parquet publication and leave no committed release.

## Executable coverage and proof ceiling

B's preserved four correct repairs and all its old tests remain in the descendant. A2's five physical typed-lane forgeries also remain. New code changes are limited to the physical estate writer/reader, native I03 binder, session, and focused tests; original I03 math/evaluator, historical repository and scientific issuer were not edited in R1.

**R1 new tests NOT_RUN.** There is no new qualified Linux runner execution yet. Historical runner results apply only to the immutable old SHA and the runner's disposable simulation.

Run **exact** R1 executable SHA `8375e260e55da09b3c5a89122839d8c7deba67bb` in an isolated read-only Linux Lima worktree:

```bash
PYTHONPATH=. python3 -m pytest -vv -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_source_direct_parquet_estate.py \
  rawlsing_next/tests/test_pre553_direct_estate_i03.py

PYTHONPATH=. python3 -m pytest -vv -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py \
  rawlsing_next/tests/test_pre553_external_i02_certificate.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py
```

Expected collection if all fixtures import: **29 focused** (formerly 27, plus two new negatives), **91 inherited**. Record real collection counts, exit status, full traceback, SHA/blobs and all negative cases; do not mark expected counts as observed.

Independent native H1/H2/H3 hostile rerun should prove complete exact `CarrierNeutralResearchExecutor.execute_i03` fact identity and semantic projection, fresh Python interpreter with source/repository absent, legitimate changed fact and exact original restoration, complete routing/denominator/provenance/replay, no `C11Repository` construction or `pq.read_table` whole-file fallback, wrong root/source/authority refusal and source-family one-read counts. B's 2,048-event cost remains only historical evidence; gather new R1 resource/disk/RSS if possible.

## Remaining obligations / no false acceptance

- Sourcefree G2 first-consumer R1 execution and nonauthor G5 remain **NOT_RUN**. If tests fail, report the exact cause for one bounded repair. The runner's 27/27 simulation is NOT a passed R1.
- A historical v1 exact *ref* is now persisted, **not** a complete replay closure or a minted v1 seal. Exhaustive bounded replay/legacy reconstruction still requires evidence.
- S1-E/Q2 body feed and S2-B G5 scientific/source authority, original35 and host/CURRENT rights, source-native integration, full 100k respondent / 6GiB economics, concurrent filesystem TOCTOU/recovery and S2-D I05/Batch remain open. A lambda-true sourcefree test is not issuer competence.
- Stop adversarial coding once actual frozen G1–G4 and distinct G5 reach their legitimate scope; no optional hardening tournament.

**Disposition:** `A2_R1_CAUSAL_IDENTITY_REPAIR_COMMITTED__NEW_TESTS_NOT_RUN__NATIVE_I03_G2_PENDING__G5_PENDING__NO_MERGE`.
