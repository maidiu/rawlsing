# P0 ANVIL stream → actual native I03 code candidate

## Evidence boundaries

Prior #1185 at `0f0af6568f20e10c78e92cecab31e6a74eff54d8`: **18/18 sourcefree preflight PASS**, executed on user's Mac (after restoring a sparse-checkout test fixture); separate MainMac checks confirmed all fourteen physical Parquet members' hashes and row counts for BOTH saved SRC04 and SRC16 estates. The 22 old Linux-/proc-bound direct-SQLite tests refused under macOS host limitations; they are not new stream failures. Actual SRC04/SRC16 I03 remained unexecuted.

## New executable code — NOT YET TESTED at this new HEAD

- `rawlsing_next/pre553_anvil_stream_native_i03.py` provides `VerifiedAnvilStreamEstate`: uses exactly independent held R2 manifest/source/all-seven stream roots plus live CURRENT callback; rechecks whole manifest hash and exact 14 member hashes, all canonical Arrow family/event-locator schemas, 13-family footer counts, event-vs-locator row-group parity; immutable proof. Its `iter_family` and `_events_from_postings` reuse **existing** native direct estate row decoders and per-event selector/body verifier. Native output requires final member rehash and CURRENT recheck.
- `rawlsing_next/pre553_direct_estate_i03.py` now strictly whitelists exact `VerifiedDirectEstate` or `VerifiedAnvilStreamEstate`; it runs the same `DirectEstateI03Session._build`, indexing, routing, target, weight and `execute_empirical_query`. Direct-I02's existing certificate check is unchanged. Stream release identity is **the exact actual `C11_STREAM_SOURCEFREE_RELEASE` root**, and stream replay is explicitly named `ANVILStreamReplayRoot@1` derived from the held **bare digest**, NOT a fictitious `C11Internal:ReplayManifest` or historical v1 C11 seal.
- Entry: `execute_anvil_stream_i03(estate=...,runtime_catalog=...,query_ref=...,predicate_ref=...)`, requiring an existing exact positive query, authorized predicate and exact scope; no invented QUERY or authority.
- `rawlsing_next/tests/test_pre553_anvil_stream_native_i03.py`: **8 new sourcefree test instances authored, NOT EXECUTED** (SRC04/SRC16-shaped synthetic physical streams; actual native I03 first reader; independent source/root, tampered member before/after admission, CURRENT before/after, foreign query, immutable proof). Reuses the existing `_Sink/_IndexSink` test-only physical writers, avoiding macOS's direct-S2B Linux-only proof dependency. No original respondent data and no new QID registration.

## Shortest next real operation

In the **existing #998 P0 OpenCode worker**, test the new sourcefree court and existing 18 at a single exact HEAD. Under the two **separately held `CURRENT_GRANTED` R2 MainMac decisions**, then open the two *unmodified* existing estates with exact held native `HeldStreamPins` and a live authority guard, and attempt only an actually issued governed I03 query. If no lawful query has been issued, preserve typed `QUERY_NOT_ISSUED` and continue permissible I05 discovery; if actual footer schemas differ, report precise `STREAM_PHYSICAL_SCHEMA_MISMATCH` instead of aliasing columns. Preserve manifest, member digests, native facts/replay identities, minority and missing states and no cross-wave pooling. No source rebuild.

**Still NOT demonstrated:** real-wave I03/I05/Batch, S04/DHIKR, FF01, C4/C5/C6, S05, original-source science, independent G5, protected paired CURRENT_PROGRESS or SOROK actor rights. I05/Batch exact type unions remain separately to be integrated after positive native I03; this candidate alone does not finish the full vertical.
