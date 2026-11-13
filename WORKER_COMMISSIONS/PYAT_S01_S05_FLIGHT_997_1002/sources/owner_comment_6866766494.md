# S2-A / P2-01 — S2-C Browser OWNER GRANT, ONE EXACT PUBLIC-SELECTOR REPAIR

**Decision:** `OWNER_GRANTED_NARROW_PUBLIC_SELECTOR_FIX__EXCLUSIVE_LEASE_REQUIRED__H26_RED_CONFIRMED`.

The existing S2-C Browser owner of [PR #990](https://github.com/maidiu/rawlsing/pull/990), after reading the frozen [S2-A owner-handoff packet](https://github.com/maidiu/rawlsing/blob/1fb9c53f5f0331ed0d630ef3cc13366f837b7292/WORKER_COMMISSIONS/PYAT_S01_S05_FLIGHT_997_1002/S2A_BROWSER_OWNER_HANDOFF.md), [G5 source/receipt](https://github.com/maidiu/rawlsing/blob/c900cf463694a8b21af7f3f8bd8da6a6b23d1d82/WORKER_RETURNS/PYAT999_EARLY_GATES_G5/S2A_receipt.json), and tested implementation, **grants only the necessary S2-A descendant repair of the existing public selector**. Do not introduce an adapter that leaves the defective public selector callable and falsely green.

## Exact grant / custody

- **Original governing packet:** #919 S2-A G1–G5 / #923 H26–H30 / #999. Single accepted G5 defect; no new A/B campaign.
- **Verified tested frozen source:** `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969` (accepted S2-C physical code `b7b697b69f0acea12174937ee824c19ac34ac284`).
- **Exact S2-C-owned target file + Git blob:** `rawlsing_next/pre553_source_direct_parquet_estate.py` @ `0e4b34ce4973bb4d23b6105faea55b9056ecf373`. Identical blob at both frozen cuts.
- **Allowed source symbols only:** `VerifiedDirectEstate.select_events`, `VerifiedDirectEstate._locators`, `VerifiedDirectEstate._events_from_postings`, and *strictly indispensable* private event-body↔locator coverage and bounded ref-order helpers **within the same class/file**. Modifications to other symbols require a separately reproduced existing S2-A predicate breach and new narrow owner decision; not implicitly granted.
- **New S2-A test/receipts:** one new standalone `rawlsing_next/tests/test_pre553_s2a_public_selector_h26.py` (or equivalently uniquely named new S2-A-only test file), plus S2-A worker-owned return artifacts; do not modify accepted S2-C/D tests in place.
- **Competent file owner:** original existing Browser S2-C #990 owner grants this *one descendant file-symbol exception* to the **existing Codex S2-A product implementer under HQ #999**, not to #999 independent reviewer or any other active worker.
- **Exclusive writer:** MUST be an actual uniquely identified Codex S2-A implementation session and clean noncolliding S2-A branch/worktree with verified exclusive lease and current heads; **no real worker/session/lease is confirmed by this GitHub handoff alone**. Existing Codex HQ checks active #997 and #1006 workers and three-worker cap before dispatch. Do not use the S2-C accepted branch, PR #990, the #999 reviewer worktree or any overlapping #997/#1006 lease.
- **Physical schema and writer FROZEN:** no edits to `_row`, `_arrow_schema`, `_Sink`, `_IndexSink`, `write_direct_estate`, manifest construction, event locator format, 13-family Parquet/Zstd layout, source-current/issuer semantics, historical release identities, direct I02, native I03 `DirectEstateI03Session`, native `_select_respondent_events` science, S2-D, or anything protected. Exact accepted S2-C/D SHA and tests remain historical immutable evidence, not modified in place.
- **Post-repair proof scope:** one bounded sourcefree S2-A repair, not production rights, original35, full integrated 100k/6GiB, merge or acceptance of all later packets.

## Mandatory RED and GREEN

**Original independent nonauthor RED:** G5 reviewer `ses_e30c25800ffeT8XbyTuHekRCme`, delivery `c900cf463694a8b21af7f3f8bd8da6a6b23d1d82`, real 4-respondent native witness at `WORKER_RETURNS/PYAT999_EARLY_GATES_G5/s2a_native_witness.py`.

One native-target locator has its `native` field changed while intact event bodies, ref corpus and physical counts remain. Locator hash + manifest digest are coherently re-pinned. `VerifiedDirectEstate.select_events(respondent,target,native_only=True)` **returns 0 instead of 1**, without refusal. The same estate **already refuses** in genuine native `CarrierNeutralResearchExecutor.execute_i03` with `cold I03 event posting lacks exact positional/selector coverage`. Conserve this correct native behavior.

**Required repair:** public `select_events` must establish full event-body↔locator positional/selector correspondence **BEFORE filtering for a supplied respondent/target/states**, including cases where all candidate target-specific postings are poisoned away and selection would otherwise be empty. Reuse the settled native I03 parity rule where appropriate, without a whole resident C11 graph, a new persistent corpus or arbitrary index trust. Each native/canonical/component/state/occurrence mapping is exact. A mere count check or validating only already-selected postings is insufficient.

**Required ordering:** original native `_build_release_index` freezes event tuples in `obj.ref.key` canonical order; the public selector currently uses physical locator order. Restore exact native selection order, maintaining repeated/ranked occurrences and their original multiplicity/identity rather than deduplicating. Do so with bounded memory; a small temporary on-disk sorted index/cursor is acceptable if necessary but not an undisclosed duplicate body corpus.

**Flags and semantics:** preserve `native_only=True` precedence over canonical/component, authorized canonical and component matching, `states=None` (all states) vs `states=frozenset()` (no matches) without skipping integrity validation, respondent/universe/source/current checks, empty valid result vs routing UNKNOWN and explicit as-of/authority held boundaries. No false OBSERVED_ZERO, dropped occurrence, wrong release/ref, issuer promotion or whole-table `pq.read_table(...).to_pylist()`.

**Tests/measure:** independently reproduce the exact G5 RED on original SHA; new test must turn GREEN only against descendant. Additional bounded target-native, canonical, component, state-specific coherent locator poison and valid duplicate-occur/order fixture. Run original native I03 refusal on same poison; normal native oracle/fact/replay, changed legitimate event and exact restore, wrong source/current/root, selected EMPTY/routing UNKNOWN, H26–H30, new S2-A test, existing S2-C + S2-D focused/inherited suites; log actual node counts and results. Measure process-tree peak RSS, scratch/retained, family/source opens, cold/repeated select seconds, and validate boundedness on material local fixture without 100k-respondent claims. No weakening tests.

## Dispatch and close

**Action to existing Codex HQ #999:** use this explicit owner grant to dispatch the **existing Codex S2-A implementation worker** only after verifying live actual exclusive writer/capacity and zero #997/#1006 overlap. Record implementation session ID, model, branch/worktree, exact source blob and writer lease. Worker returns code/test SHA, original RED→GREEN, full focused/inherited results, positive/negative/change/restore and resources. **This comment does not launch a local agent.**

Return exact frozen implementation SHA to the **same distinct independent nonauthor G5 reviewer** `ses_e30c25800ffeT8XbyTuHekRCme` for *one* scoped re-review. On accepted original G1–G5: `S2A_TERMINAL_CLOSED@SHA`; STOP. No S1-A, S2-B/C/D reboot, no #997/#1006 interference or new architecture.

