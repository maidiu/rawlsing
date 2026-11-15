# PYAT W05/P03 — versioned, guarded native physical-order traversal **author candidate**

**2026-11-15. AUTHOR_CANDIDATE / NO ACTUAL TEST RUN / NO INDEPENDENT G5 / NOT PRODUCTION OR PROTECTED.**

## Scope and frozen ancestors

- Parent branch: `integration/pyat998-r6-s2a-joined-staging-20261115-r1` at `18dc7106f032bb86c89503daaefc5616cad29c58`, including independently G5-accepted S2-A public/native canonical-body repair from source cut `ce7704253f6a2381310c3eb2c7412a2d85c5596c` / independent `c18b7e087d5d5b178ed5acc92f9c82250a1743de`.
- Measured old-reader candidate: [#1035](https://github.com/maidiu/rawlsing/pull/1035), independent [#1036](https://github.com/maidiu/rawlsing/pull/1036), accepted experiment at `3e0ed0794498506520ae62c997a5c852ac672061`. 100k selected 543.026s/204125 rowgroup reads baseline → 294.087s/5784 on the author's TEST_ONLY runtime sorted override, exact facts/replay/release at tested scope. **This PR is NOT that independently tested experimental binary.**
- Latest sourcefree baseline writer 100k 3033.723s; 100k I03 selected 562.362s, reverse F2 873.655s, 3-way F4 908.507s; no claim this production candidate meets a speed threshold or 100k/6GiB.
- J5 100 DISTINCT cold queries 51.929s author/65.661s independent on an OLDER reader, B country-sharing unmeasured and not implemented here.

## Actual code change — three existing source files, no new engine

1. `rawlsing_next/_pre553_query_common.py::_ReleaseIndex` adds DEFAULT-FALSE `native_verified_physical_respondent_order` annotation, without altering prior construction/identity field order.
2. `rawlsing_next/pre553_direct_estate_i03.py::DirectEstateI03Session.indices_for` sets TRUE ONLY on native saved index instantiated after authenticated sealed estate/body/posting coverage validation. Uses its existing `RespondentIdentity` dict's saved physical insertion order. No extra Parquet read, SQL table, on-disk body, or scientific authority.
3. `rawlsing_next/_pre553_query_eval.py::_query_respondents` uses physical insertion order exclusively when flag true, and CANONICAL `sorted(..., key=ref.key)` for legacy indexes. It replaces exactly TWO active evaluation loops (_evaluate_index_group_core, _evaluate_indices); deliberately does NOT replace the third respondent sort in `_respondent_root`, which canonically hashes identities. The original #1035 monkeypatch intercepted three sorts but returned canonical for non-respondent objects; this explicit hook is narrower and less invasive.

**This is the minimal source-grounded mechanism.** No `_respondent_family ORDER BY ref` change: #1034 rejected that as the source of cross-respondent thrash. No changing query semantics, risk/member calculations, missing/zero, weights, sorted output, permission/current, malicious source checks, body-to-posting consistency, evaluator or replay.

## Added tests — source-only, EXECUTION NOT YET EVIDENCED

`rawlsing_next/tests/test_pyat1006_verified_native_physical_order.py`:
- unit fallback: unsorted physical mapping yields physical iteration while legacy mapping remains ref sorted, `_respondent_root` identical;
- actual sourcefree saved native I03 vs existing same-source legacy/native oracle `EmpiricalFact` exact IDs/semantic projections/release refs, with the new order flag observed;
- revoked CURRENT refuses before native I03.

**MANDATORY: real qualified executor still required.** On the *current exact head*:
```bash
python -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat1006_verified_native_physical_order.py \
  rawlsing_next/tests/test_pre553_direct_estate_i03.py \
  rawlsing_next/tests/test_pre553_s2a_public_selector_h26.py \
  rawlsing_next/tests/test_pyat991_s2d_five_readers.py \
  rawlsing_next/tests/test_pre553_empirical_query.py
```
Then reuse the accepted #1006 matched 1k/10k/100k retained estate and the independent order-sensitive weighted/F4 tests: **run new production candidate against inherited baseline on exact same fixture, source/manifest/current/readers**. Record wall/CPU/process-tree RSS, rowgroup reads, fact/projection/replay, cold and repeated, changed value/restore, revoked current, wrong root, source scope, forged projected body and missing family. Execute 1/10/100 DISTINCT operations and I05/Batch separately. Full S01–S05/100k genuine source/pilot is a distinct obligation, not inferred.

## Boundaries / owner handoff

- #1006 and [issue comment](https://github.com/maidiu/rawlsing/issues/1006#issuecomment-6891572182) establish an **outstanding exact semantic evaluator/iteration owner compatibility grant**. The user's engineering direction permits an isolated candidate, **not** a competent product owner grant or independent review. Owner must explicitly evaluate this delta before calling it an accepted production reader. No simultaneous edit to #997 issuer, S2-C writer, #999 owner branch or other HQ director.
- The initial 100k selected experiment still takes 294s; this tweak is no proof of economic sufficiency, fast **distinct** query economics, shared preparation, writer improvements, or 100k full vertical.
- The parent #1073 joined G5 is NOT_RUN; inherited accepted component G5 does not certify this new code. Competent owner/same native suite and distinct independent G5 needed. Protected PRE-MAIN rev8 unchanged.
- Original35/native source, rights, science, R03 governed QUERY issuer, FF/SEAM and actor work remain outside this isolated code change.

**NEXT ACTION: qualified executor/owner run exact frozen source-code court; repair only actual fails; then independent reviewer + precise adoption into the existing #998 integration descendant, not a parallel full engine.**
