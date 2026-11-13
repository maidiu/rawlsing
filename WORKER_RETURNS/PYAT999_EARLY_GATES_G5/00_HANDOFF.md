# PYAT999 — S1-A / S2-A independent G5 receiving

## Court A — S1-A cache admission

**Disposition: `ACCEPT_SCOPED@S1A_SOURCEFREE_SEMANTIC_CACHE`**

- Packet: S1-A / P1-01, governing #918.
- Frozen base: `6a5c12f04323d74001f9632063ec907f4fc4468e`
- Tested candidate: **`6286ea700a253ff142104f2e3ee62c9352a07644`**
- RED: `97b1eba95266cb6dc0340022a35f945aaa2c9b38`
- Source/test/workflow blobs:
  - `pre553_source_backed_c11_facade.py` `f29247b33cb78e5f1e620620d6968ab433ce407a`
  - `test_c1_agent_b_cache_differential.py` `d94946349e7f353df3f46adf4c60160db022d5c7`
  - workflow `f740e6a10ac573a9de85d2666d4c4b6c3c25c897`
- Actual first consumer: `build_source_backed_c11_repository` → real
  `execute_empirical_query`.

### Reproduced results

- Focused **34 passed in 3.66 s**.
- Preservation **136 passed in 94.78 s**.
- Independent native witness: cold / warm / clear-recompute all return the same
  exact I03 fact; cold source cell iteration `1`, warm extra `0`, recompute extra
  `1`; one cache entry after rebuild; parent max RSS `98,787,328 B`.
- Concurrent clear/recompute, conflicting valid rebind, first-insert poison,
  row/decoder/routing/occurrence/authority changes, one-shot authority and
  changed-fact/restore tests all pass in the 34 focused suite.

### G1–G5

- **G1 PASS:** exact #918/S1-A base, source/test/workflow and semantic cache
  contract pinned.
- **G2 PASS:** real source-backed I03 cold/warm/recompute and changed/restore.
- **G3 PASS:** hostile cache identity/rebind/clear/TOCTOU/authority cases pass;
  no cache-key authority promotion.
- **G4 PASS_SCOPED:** tiny in-memory cache measurements; durable CAS is
  `NOT_APPLICABLE_PROVED`; 100k/6 GiB is external NOT_RUN.
- **G5 PASS:** reviewer `ses_e30c25800ffeT8XbyTuHekRCme`, not S1-A author or
  B-repair author; all applicable frozen cases pass.

No S1-A product edit was made. Original35/source/current/protected authority
remains HOLD. Integration: **UNMERGED**. Durable details in `S1A_receipt.json`.

## Court B — S2-A native semantic selector

**Disposition: `REVISE_EXACT_DEFECT`**

- Packet: S2-A / P2-01, governing #919; model-only #923 at
  `fc6b75ec83795931df5d8f47d7a31553198ca05a`.
- Tested accepted read-only tree: **`9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`**
  (S2-C `b7b697b69f0acea12174937ee824c19ac34ac284`, S2-D `9d96a9cac`).
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat999-s2a-native-readonly`.
- No product/test/source/prior-return edit.

### Existing native results

- `test_pre553_verified_semantic_range.py`,
  `test_pre553_source_direct_parquet_estate.py`,
  `test_pre553_direct_estate_i03.py`: **57 passed in 5.58 s**.
- Own native witness: real cold S2-C direct estate through
  `CarrierNeutralResearchExecutor.execute_i03` returns the exact oracle fact;
  hidden/duplicate locator poison is refused by `DirectEstateI03Session`;
  no `inventory_refs`; H30 bounded page test passes at its small fixture.

### Exact RED — H26 public selector omission

**File/function:** `rawlsing_next/pre553_source_direct_parquet_estate.py::VerifiedDirectEstate.select_events`

**Input:** A real S2-C direct estate with one target-specific locator row's
`native` field poisoned while every event body and ref remains intact, counts
remain equal, and the manifest/member digest is coherently re-pinned. The caller
supplies the new independently held manifest SHA.

**Expected:** The named selector refuses/rebuilds the damaged secondary index;
native selected count is `1`.

**Actual:** `VerifiedDirectEstate.select_events(respondent, target, native_only=True)`
returns **0** events with **no error**. The actual native
`execute_i03` refuses the same poison with:

```text
DirectEstateError: cold I03 event posting lacks exact positional/selector coverage
```

Thus the real `execute_i03` path is safe, but the public authenticated selector
API silently undercounts a valid selection. This is a direct violation of
S2-A G3/H26, which requires poisoned selectors with intact ref corpus to
refuse/rebuild rather than undercount.

A secondary parity observation is also retained: on a legitimate two-occurrence
fixture, `select_events` returns source/locator order while the original native
selector and `DirectEstateI03Session` SQL path return ref-canonical order.

### Proposed owner-granted correction path

Do not silently edit frozen S2-C as reviewer. Either:

1. obtain the S2-C owner grant to patch
   `VerifiedDirectEstate.select_events` so it validates **every** locator row
   against its body/position before serving (reusing the complete
   `DirectEstateI03Session._build` parity law), or
2. add an approved S2-A adapter (e.g. a new
   `pre553_s2a_validated_selector_adapter.py`) that performs the complete
   locator/body witness before exposing selected events.

Required regression: target-specific native/canonical/component/state locator
poison with intact bodies/refs and corrected counts; assert selector refusal,
native `execute_i03` refusal, and exact untampered restore. Then freeze and
receive at the new SHA.

### G1–G5

- **G1 PASS:** contract/entry, sourcefree direct roots, original selector and
  S2-C/D paths pinned.
- **G2 PASS:** actual `execute_i03` cold fact equals oracle; changed/restore and
  existing full native tests pass.
- **G3 FAIL:** named public selector undercounts under H26 target-specific
  semantic-index poison.
- **G4 PASS_SCOPED_FIXTURE:** H30 no inventory/bounded page test and no
  inventory method; small/medium only; 100k/6 GiB NOT_RUN.
- **G5 FAIL / REVISE:** exact executable first-reader RED and proposed owner
  path; HQ/owner adjudication before repair.

Original35/source science/current/protected merge remain external HOLDs.
S2-A integration: **UNMERGED**. Detailed machine receipt: `S2A_receipt.json`.

## Commands / evidence

```text
S1-A focused:
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_c1_agent_b_cache_differential.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_qualification_r1.py
# 34 passed in 3.66s

S1-A preservation:
PYTHONPATH=. ... test_pre553_source_equivalence.py test_universal_workload.py \
  test_universal_workload_custody.py test_universal_source_byte_custody.py
# 136 passed in 94.78s

S2-A existing:
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat999-s2a-native-readonly
PYTHONPATH=. ... test_pre553_verified_semantic_range.py \
  test_pre553_source_direct_parquet_estate.py test_pre553_direct_estate_i03.py
# 57 passed in 5.58s
```

Evidence files:

- `evidence/s1a_focused_34.txt`
- `evidence/s1a_preservation_136.txt`
- `evidence/s1a_native_witness.json`
- `evidence/s2a_existing.txt`
- `evidence/s2a_native_witness.json`
- `evidence/s2a_selector_order_advisory.out`

## Courts / limits

- Engineering: S1-A accepted at S2_SOURCEFREE; S2-A has one in-scope public
  selector defect, actual native I03 safe.
- Scientific: `NO_ORIGINAL35_SCIENTIFIC_ACCEPTANCE` for both.
- Authority: no source/current/host/actor/protected grant; production and
  original35 remain HOLD.
- S1-A is `TERMINAL_CLOSED@6286ea700a253ff142104f2e3ee62c9352a07644`.
- S2-A is `REVISE_EXACT_DEFECT`; do not automatically repair or reopen broad
  architecture. HQ/owner adjudicates the exact S2-C selector owner path.
- Neither result is protected merge or N11/N12 authority.

## Next indispensable dependency

S2-A owner-granted selector correction (or approved adapter) plus the exact
target-specific poisoned-index regression; then one independent G5 delta
recheck. S1-A needs no further packet work.

## S2-A resource note

The independent small fixture had 4 respondents/4 locator rows; parent max RSS
`108,490,752 B`; the poisoned `select_events` path traced only `12,521 B` at
the small fixture. This is not a 100k/6 GiB or process-tree proof.

## Remote verification

Review content commit `c0971e9af4fcb96b45cf0fa8ee2906f400d1f1f4` was pushed to
`origin/agent/pyat999-early-gates-g5-r1`. Direct remote verification found the
product tree unchanged from S1-A tested `6286ea7` and all three receipt JSON files
valid. See `evidence/remote_verification.txt`.
