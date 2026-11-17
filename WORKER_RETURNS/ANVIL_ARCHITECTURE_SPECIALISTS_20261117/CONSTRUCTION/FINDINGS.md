# CONSTRUCTION SPECIALIST — BOUNDED FINDINGS

**Role:** independent CONSTRUCTION specialist against the SAME whole common frame.
**Author frame:** `5a619ff9fa79be9183eb4d4378d42f040ef2bd9b` (AUTHOR_FROZEN, not independently accepted).
**Code cut read:** `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`; physical writer identical at `b830458c3ebfe0a3f0e2d18e516e68b90324c88a`; protected `31291d0` has no `rawlsing_next/pre553_source_direct_parquet_estate.py`.
**Grade:** analytical/source-code trace, sourcefree scoped. No native/source/science/actor/protected adoption; no new full backend; no benchmark executed.

## 0. Result in one paragraph

The present pipeline is not one construction proof; it is at least **two full object-journal representations, two full I02 certifications, one full physical reread, one raw member-hash pass, one cold raw member-hash pass, and one full per-session postings scan**. The minimum lawful reduction is: **one source-derived I02 certificate, one private exact-body journal, one Parquet/Zstd canonical estate, one full physical body/lane proof against that same I02 certificate, one manifest/member-hash publication, and one cold qualification + durable derived postings index**. The duplicate Q2 spool/journal and the frozen writer's second I02 build can be removed only if the physical reread is strengthened to compare every family row/ref/selector to the Q2 certificate; the second check is not removed on speed grounds. The full physical reread, cold member hashing, current/authority guard, typed-negative/replay checks and all 13 families stay. The largest avoidable costs are the second I02 certification (witness: 4.39 GB), the duplicate 3-family journal/spool, and the O(E + N + side-family) per-session index rebuild (witness: 1.30 GB). The witness is a sparse canary, not dense width proof. No 6 GiB or 1/10/100 economic acceptance is claimed.

## 1. Independent check of the S1 frame before using it

I did not treat the S1 commit as accepted. I checked its material claims against the frozen inputs:

- **16 requirement rows:** the 16 IDs and each requirement object in `evidence/S1_FROZEN/S1/FRAME.json` are byte-identical to `ACCEPTED_INSTRUMENT/ANVIL_R7/EVIDENCE/FRAME.json` (same IDs, no object-hash difference). This proves **no narrative drift between the prepared instrument and S1**, not independent review of the narratives against current code/science. The instrument is preparation-only; the S1 frame itself says `AUTHOR_FROZEN_NOT_INDEPENDENTLY_ACCEPTED`.
- **118 identity rows:** counts match exactly: 29 `K1_CAP` + 26 `PYAT_PC` + 14 `P4R` + 10 `SEAM_B` + 8 `SEAM_S` + 8 `ANVIL_L` + 7 `BOUNDARY` + 16 `TERMINAL` = 118. The 26 `PYAT_PC` remain NOT_ADOPTED, the 14 `P4R` remain HELD; the separate 52 T1/T2 contracts, 24 paths and 21 prospects are not additive. No row was promoted by this specialist.
- **Missing common-frame requirement:** the 16 rows cover source semantics, persistence/cold restore, current I03/I05, historical DDM, F1–F4 joint, FF/SEAM future nonpreclusion, authority/revocation, economics, multiway joint, denominator/missing/routing, physical workload, source–I02 revocation, FF/world firewall, terminal holds and no-adoption. They do **not** explicitly cover **crash-consistent publication / interrupted-build recovery**. The actual writer creates the final target directory before the manifest exists; a crash there leaves a manifest-less target that later builds refuse as "already occupied". The user mission explicitly requires interrupted recovery. I therefore return one proposed frame requirement (`REQ-CONSTRUCTION-ATOMIC-RECOVERY`) in `NEW_FRAME_REQUIREMENTS.json`; everything else below uses the frozen frame unchanged.
- **Source bank:** `8523007613d411390a76683fa464002c0f25df83` is a reference copy at base `31291d0`; its two hash mismatches are reference-only. The original upload ZIP `526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332` is the source-byte authority. I did not use bank copies as source truth.
- **Instrument:** `05e81747fb2e5cca042c0d968ba1ae203182556e`, ZIP `701207ec43eb1975e66f6dc324da7a9c786a84800d0ae16e9e2e4526d62daad9`, review `21d39dfa5d5ca95a64251494ff9d4c0f961d4a43`, delivery `f6073d923a3e01caf4c1af54599797f04338d54f` are instrument-preparation evidence only; they are not native/performance/science/architecture/H1 acceptance.

No material requirement of the 16 was found missing for the construction question. The recovery gap is the one actual missing common requirement returned for versioning.

## 2. Actual trace at `cea2d4d` (writer unchanged from `b830`)

Exact symbols and what they do:

1. **Source decoder.** `pre553_source_i02_handoff.build_source_i02_handoff` (`pre553_source_i02_handoff.py:987`) verifies the S1-C census before source read (`_verify_census_before_source`, L218), decodes original source under `decode_config_with_source_read_permission` or fixture `decode_sav`/`decode_dta` (L1080-1095), checks source SHA and row count, and runs one bounded physical cell pass (`_project_spooled_families`, L327) into the three-family spool `SPOOL_FAMILIES = RespondentEvent, EmpiricalCoordinateFact, WeightMeasureFact` (L98). The other ten `STATIC_FAMILIES` are held as tuples. Source stats disclose one decode, one cell pass, one key-witness pass, zero full C11 builds.
2. **Q2 I02 certificate.** `_manifest_and_sections` (L829) builds `SourceReleaseManifest` and `SourcefreeDirectI02Sections`; `build_sourcefree_direct_i02` (`_pre553_direct_i02_sourcefree.py:617`, implementation L329) consumes all 13 family iterables once and writes a temporary SQLite certificate with `objects`, `closure`, `bindings`, `selectors`, `scoped_names`, `event_occurrences`, indexes, header, logical root and physical SHA (`_pre553_external_i02_certificate.py:70-235`). This is the genuine source→I02 proof. It is sourcefree, not native acceptance.
3. **Body tee and 13 JSONL journals.** `SourceI02BodyTee` (`pre553_source_i02_streams.py:148`) wraps the sections while Q2's builder consumes them; each object is synchronously passed to `SourceSavedBodySink.emit` (`pre553_source_saved_body_bridge.py:126`), which writes one JSONL record per object to 13 files: `{"family","ref","body"}` where `body = _object_row(obj)`. `SourceSavedBodySink.finish` (L221) verifies counts, absences, manifest, Q2 certificate header and roots, then replays through `_rows` (L150).
4. **Frozen S2-C writer.** `write_direct_estate` (`pre553_source_direct_parquet_estate.py:460`) wraps the replayed sections in `tap` (L490), writes 13 Parquet/Zstd members plus `event_locator.parquet` using `_Sink`/`_IndexSink` (L220/L268), and calls `build_sourcefree_direct_i02` **again** on the wrapped stream (L509) to produce a **second** I02 certificate in `stage/.i02-proof.sqlite`. It compares `expected_i02` roots (L512). It closes writers, checks locator count (L519), then runs `_verify_emitted_physical_payloads` (L329) which reads every Parquet row group, reconstructs each object from `body_json`, recomputes `_row`, checks typed/identity/occurrence lanes, checks each ref against the **second** certificate's `objects` table, inserts every ref into a temporary `seen` SQLite primary key (duplicate detector), and checks event postings/selectors. It then deletes the second certificate, hashes every member with `_hash` (raw bytes, L531-536), writes and fsyncs `manifest.pending`, fsyncs members, creates `target = releases/<sha256(release)>` (L562-567), moves members into it, fsyncs the directory, hard-links the manifest as `manifest.json`, and fsyncs again (L570-587).
5. **Cold verification.** `VerifiedDirectEstate.__init__` (`pre553_source_direct_parquet_estate.py:605`) takes an independently held manifest SHA and exact `ExternalI02Roots`, refuses before hashing if the live current/rights callback is false, checks exact path/content identity, hashes **every member** against the manifest, checks 13 family counts, event/locator counts and row-group topology. `iter_family` (L704), `_locators` (L724), `select_events` (L909) and `_events_from_postings` (L981) read bounded row groups and revalidate body/selector lanes.
6. **Per-session postings index.** `DirectEstateI03Session.__enter__` (`pre553_direct_estate_i03.py:140`) creates a temporary SQLite DB; `_build` (L252) reads all `EmpiricalUniverse`, all `RespondentIdentity`, all `SourceUniverseRelation`, **all events** with full `_validate_event_body_truth` (L191), and scans all `EmpiricalCoordinateFact`, `RoutingEligibilityFact`, `WeightMeasureFact` rows to insert `events`/`members` postings. This is O(N + E + C + R + G) per new session even for one respondent/question. `PreparedI03Session` (`pre553_prepared_saved_i03.py:51`) reuses one built index across I03/I05 operations in one process, but it is process-local and ephemeral.
7. **Admission/currentness.** `SavedC11Admission.__init__`/`open` (`pre553_saved_c11_admission.py:143/256`) re-verifies the estate, binds exact release/catalog, and `check_current` (L309) calls the live estate authorizer before/after each operation. `PreparedI03Session.execute_i03` calls the existing `execute_empirical_query`; `execute_i05` calls `execute_exact_bounded_discovery`. No second evaluator is introduced.

### Pass/materialization ledger (current)

Let `N` = respondents, `W` = physical source cells/respondent, `E` = RespondentEvent objects, `C` = EmpiricalCoordinateFact, `R` = RoutingEligibilityFact, `G` = WeightMeasureFact, `Q` = QuestionVariableBinding/static objects, `M = N+Q+E+C+R+G+S` all 13-family objects, `B` = canonical body bytes, `P` = retained Parquet bytes, `I_q2` = Q2 certificate bytes, `I_w` = writer second-certificate bytes, `I_idx` = session postings bytes.

| # | Pass | Objects/bytes | Independence |
|---|---|---|---|
| 0 | original-source prehash (original only) | source bytes | independent binding check |
| 1 | decode + census + projection | `N*W` cells | independent source read |
| 2 | Q2 3-family spool write | `E+C+G` objects | source materialization |
| 3 | Q2 I02 build | `M` objects, `I_q2` | **genuine source→I02 proof** |
| 4 | 13-family journal write | `M` objects, `J` | exact body transport |
| 5 | journal replay | `M` objects, `J` | transport exactness |
| 6 | Parquet write | `M` objects, `P` | canonical retention |
| 7 | second I02 build | `M` objects, `I_w` | **duplicate certification** |
| 8 | physical reread `_row` parity | `M` objects, `P` read | **genuine persisted-body proof** |
| 9 | build member hashes | `P` raw | manifest publication |
| 10 | cold member hashes | `P` raw | **independent cold integrity** |
| 11 | session `_build` | `N+E+C+R+G` read, `I_idx` write | **cold semantic+postings qualification** |
| 12 | query | selected row groups + output | selected proof per operation |

The same event/coordinate/weight bodies are written at least twice (Q2 spool and 13-family journal), re-parsed twice, and certified twice. The 100k witness's 5.26 GB staging + 4.39 GB temporary writer I02 + 1.30 GB session index are consistent with this ledger, but the Q2 certificate size is not separately reported and must not be assumed free.

## 3. What is genuinely independent and what is duplicate

**Keep (independent proof obligations):**

- source prehash/decode/census/projection and source SHA/row/count checks;
- Q2 I02 certificate: object identity, semantic hash, authority closure, universe/respondent/question/event relations, selectors, replay/release reconstruction, logical+physical roots;
- exact body transport identity: family/ref/body per object, family counts, typed absences, manifest/replay metadata;
- physical Parquet body/lane/locator proof against the exact certificate (full reread, not sampling);
- manifest construction + raw member SHA-256 + fsync/no-clobber;
- cold independent member hashing against an independently held manifest SHA and exact I02 roots;
- current/rights/revocation callback before and after materializing operations;
- typed negative states, occurrence/repeat topology, denominators/risk sets, replay/tie/authority refs.

**Duplicate representation/conversion (candidate reduction):**

- Q2's 3-family spool plus the bridge's 13-family journal for the same three families;
- the frozen writer's second full I02 build from a journal that is already checked line-by-line against the Q2 certificate; root equality is a **composition check**, not a second independent source observation;
- the per-session full body/locator and side-family rescan for immutable bytes already covered by the cold manifest hash and the build-time full physical proof;
- recomputing `_row` for every event at a chunk-boundary in `tap` (`writers[family].pending[-1] if pending else _row(...)`), a micro-conversion, not an integrity issue;
- event locator columns duplicating event-body selector columns; the locator is a derived accelerator, not a second canonical evidence source.

**Do not remove merely because slow:** the full physical reread, member hashing, cold hashing, current guard, duplicate-ref `seen` check, event/locator positional proof, negative/replay checks. The reduction is lawful only if the physical reread is redirected to the **Q2 certificate** and strengthened to compare all family selector fields, ref kind/object_id/digest, not just event fields.

## 4. Minimum recommendation (bounded, for architect adjudication)

**R1. One I02 certificate, used by the writer as the proof DB.**
Adapt `write_direct_estate` to accept an already-built Q2 certificate (path + exact `ExternalI02Roots`) and to skip its internal `build_sourcefree_direct_i02`. Keep `tap`/`_Sink`/`_IndexSink` and the full `_verify_emitted_physical_payloads`; strengthen that verifier to compare, for **every family**, `ref`, `kind`, `object_id`, `content_hash/digest`, `family`, `universe`, `respondent`, `native`, `canonical`, `component`, `state` to the Q2 `objects` row, and keep the event selector/occurrence/posting checks and `seen` primary key. This preserves source→cert and persisted→cert while removing the second full certification. If the Q2 certificate cannot be retained/qualified, keep the second certification as the fallback; do not sample.

**R2. One private 13-family exact-body journal.**
Use one journal in the existing `_object_row` format, written once from the same Q2 source objects, read by the writer after the certificate. Reuse/merge the Q2 3-family spool rather than writing those bodies twice; delete the journal after commit. The Q2 certificate must still be built from the source-derived stream, not from a re-parsed journal, so source truth does not collapse into the transport format.

**R3. Full physical proof once, cold qualification once, index once.**
Keep the build-time full reread. At first cold open, perform the full event/locator and side-family body/cert parity once and persist a small `qualification.json` bound to `manifest_sha256` + I02 roots + code/schema version. Subsequent fresh processes verify member hashes + qualification receipt + current authority and open a **derived, content-addressed, versioned, regenerable postings index**; if the index or receipt is absent/corrupt/unbound, rebuild from canonical after full qualification. This is not a second canonical source and does not excuse the first full check.

**R4. Atomic publication and interrupted recovery.**
Replace the current "create target, move members, then manifest" sequence with one fully fsynced stage directory and a single atomic directory rename to `releases/<content-id>` where the filesystem permits it; if an exclusive claim is required, use a lease containing host/PID/start-time and return a typed `ORPHAN_REQUIRES_OPERATOR` rather than deleting a possibly active target. GC only typed scratch (`.s2c-stage-*`, `.s1e-*`, `.i02-proof.sqlite`) with a proven-dead lease; never delete a completed or another writer's release. This repairs the actual `target.mkdir`-before-manifest orphan window and closes the missing frame requirement.

**R5. Multi-country/wave and partition geometry.**
Use one immutable estate per exact `EmpiricalUniverse`/country-wave-instrument release; do not pool bodies across waves. Keep `SourceUniverseRelation` typed absence/authority and native single-universe refusal (`indices_for` requires the exact single universe). A separate catalog/relations index may span universes, but queries must use exact relation authority and separate denominators; no cross-wave person/body join. Partition by exact universe, then respondent/question/occurrence within the event file; do not use country-name strings as identity.

**R6. Canonical body vs typed projections.**
Keep `body_json` as the sole canonical body; typed selector/occurrence/raw lanes and `event_locator.parquet` are derived, verified accelerators. Do not add SQLite/DuckDB/Stone as a canonical body store. A future version may split canonical body-only members from derived projections, but that is an unapproved format rewrite now. The present same-member layout is acceptable if the derived lanes are explicitly labeled and verified against `body_json`; the body remains authoritative on any mismatch.

**R7. Chunk/dictionary geometry.**
The current chunk default 512 and Zstd/dictionary are safe, bounded choices. Larger row groups (1,024–4,096) may reduce row-group/footer/index overhead, but increase per-selected-event read amplification. This is a measurement question, not a fashion choice; do not change it without a small fixed sourcefree witness that includes narrow and wide queries. No threshold is invented here.

**R8. Build once vs retain vs reopen.**
Retain canonical bodies + manifest + derived index. Do not retain the second I02 certificate or the journal on the hot path. Retain the Q2 certificate only if the owner requires re-verifiable source comparison at rest; otherwise retain its exact roots plus a proof receipt. If retained, the Q2 certificate is an archive/proof artifact, not a query source and not a second body corpus. The 4.39 GB second-I02 scratch is the largest demonstrated removable build cost; the 1.30 GB per-session index is the largest demonstrated repeated cost.

## 5. Cost and density (analytical, not measured by me)

- Current witness (cited): 100k-shape, 3.245 events/respondent → ~324.5k events; writer 3033.723 s; retained 310.16 MB; staging 5.26 GB; temporary writer I02 ~4.39 GB; native session index ~1.30 GB; one pre-W05 selected query 562.362 s. This is sourcefree, cut-specific, not native/production acceptance.
- Retained/staging amplification: 5.26 GB / 310.16 MB ≈ 17×; 4.39 GB / 310.16 MB ≈ 14×. These are disk figures, not RSS.
- The 3.245 events/respondent canary realizes only about 0.25–0.54% of a 600–1,300-slot instrument per respondent if one event per slot is assumed; it is not a dense-width workload. A 600-slot, 100k-respondent fully realized survey would be ~60M events; 1,300 slots ~130M, before repeated/ranked occurrences. Routing/missing reduces that, but the canary is a lower bound, not a representative 100k production claim.
- Current pass count is analytic: one source cell pass; Q2 spool write/read for 3 families; Q2 I02 build; 13-family journal write; journal replay; Parquet write; **second I02 build**; full physical reread; member hash; cold member hash; full session scan. The proposed minimum removes the second I02 build and one duplicate 3-family journal representation, and makes the session scan a one-time qualification plus index build.
- Asymptotics: source O(N·W) cells (bounded streaming); Q2 I02 O(M) disk rows (with SQLite indexes, not a full in-memory graph); Parquet O(M); physical proof O(M); cold hash O(P); qualification/index O(N+E+C+R+G) once; each later query O(selected row groups + output facts), not O(E). Multi-universe cost is additive per exact universe; no cross-wave pool.
- RSS: current writer's documented `cache_size=-2048`, `temp_store=FILE`, chunked row groups and bounded row-group reads are the right pattern; the 4.39 GB/1.30 GB/5.26 GB figures are disk artifacts, not proof of 6 GiB RSS. The Q2 projection still holds static family tuples (`RespondentIdentity`, questions, routing, authorities) in memory; this is residual O(N+Q+R+Wt) RSS and is not eliminated by journaling. No 6 GiB claim is made.

## 6. All 13 families and the native contract that must survive

The canonical body is the exact object row from `_object_row`/`_object_from_row` (`pre553_parquet_carrier.py:89/131`), which reconstructs the existing `CanonicalSemanticObject`/`C11InternalRecord` and validates object identity/content hash. The 13 families and the concrete semantics they carry:

1. **EmpiricalUniverse** — country/geography, raw/canonical wave, field/reference time, population/sample frame, sampling design, respondent namespace, source lineage, harmonization authority; no cross-wave pseudo-person.
2. **RespondentIdentity** — scoped respondent, source-native key ref or typed absence, identity-map authority/absence; no stratum→individual identity.
3. **QuestionVariableBinding** — native question, instrument version, canonical/component refs or typed absence, semantic/topology authority; preserves native option/code/form/translation/language/routing meaning.
4. **RespondentEvent** — exact raw response value, canonical value if authorized, value-transform authority, native/canonical/component refs, event group/id, response topology, multiplicity/order/rank fields, response state; repeated/ranked occurrence is not a first-value pivot.
5. **RoutingEligibilityFact** — eligible/applicable/not asked/inapplicable/routing unknown/rule unavailable, risk-set ref, routing rule, parent predicates, member-set replay; separate denominator bases.
6. **EmpiricalCoordinateFact** — coordinate facts, raw/canonical value, unit/taxonomy, effective/reference time, coordinate state, normalization/semantic authority; typed UNKNOWN/MISSING is not zero.
7. **WeightMeasureFact** — exact weight representation, weight state, source/design/estimand/normalization authority, effective scope; nonpositive/invalid weights are not silently 1.0.
8. **AuthoritySnapshot** — exact authority ID/version/content hash/kind, decision state, governed operations/families, scope, effective time, parents/negatives/supersession, replay protocol; no LATEST/fuzzy authority.
9. **SourceUniverseRelation** — relation kind, exact universe refs, relation authority, overlap/nonduplication evidence, composition estimands, dedup rule, negative limits; DISTINCT_BY_DEFAULT / no pooling unless authorized.
10. **EmpiricalPredicateReplayBinding** — predicate grammar authority, typed AST ref, predicate hash, coordinate/question/value refs, risk set, target, scope, measure basis.
11. **ComparatorReplayBinding** — comparator state, actor-fact ref or typed absence, effective time, comparator rule, resolved predicate, cardinality ambiguity, source scopes; DEFERRED is explicit.
12. **DiscoveryBranchReplayBinding** — search family, candidate universe, grammar, risk/measure scope, algorithm identity, coverage/pruning contract, deterministic parameters, RNG state, parent/winning/pruned refs; branch/memoization replay.
13. **StructuralAdmissionReplayBinding** — empirical fact/query, predicate/risk/target/scope/measure, provenance, structural authority, producer use, negative limits, transformation replay; FF02/N9/N10W future boundary; not survey opinion as power.

`ReplayManifest` is a reconstructed digest, not a 14th body family. F1–F4 true same-person k≥3, directional denominators, minority/recursive and occurrence/repeat semantics are carried by the event/coordinate/routing/weight families and the native evaluators; the physical layer must not replace them with pairwise/marginal products.

## 7. Future nonpreclusion that constrains now

- **FF01/FF02:** keep descriptive source facts separate from structural/material authority refs; never let a survey frequency or physical projection become FF02 power. The 13-family body preserves the refs; FF science remains owner-held.
- **F6/F7:** preserve numeric uncovered mass vs guard, neutral/signed and certification vs coverage distinctions; do not infer coverage from a hash or a weight. Cross-source comparability/time is carried by universe/coordinate/routing/weight fields, not a global pool.
- **N9/N10E/N10W/PRE-V3/N11/N12:** preserve exact person/position/occurrence/time refs and separate world/actor readers; no survey→actor identity/motive, no fictional→observed or cross-wave person join.
- **SEAM/SOROK:** `SourceUniverseRelation`, event occurrence and authority refs must remain available for Other→encounter/access/learned-activity/world-history, but the construction does not implement or authorize actor/world science. SOROK's `sorok_history.owner.HistoricalWorld` remains a separate owner; no source→actor promotion.
- **F26:** exact caller/invalidation remains `K1-CAP-24`/`P4R-R02`/`PYAT-PC-R11-21`; do not invent a body or claim closure.

## 8. Findings vs interpretations vs owner holds

**Findings (source-code/static):** duplicate Q2 spool + 13-family journal; duplicate second I02 build; full physical reread currently checks the second certificate; per-session full scan; writer target-mkdir-before-manifest orphan window; writer `tap` chunk-boundary `_row` recomputation; 16 rows identical to instrument FRAME; b830 and cea2d4d writer identical; 31291 lacks the writer file; 118 counts exact.

**Interpretations (analytic, contestable):** removing the second I02 preserves independence only if the physical reread is strengthened against Q2 and remains full; a one-time cold qualification + durable index is not weakening immutable-byte integrity; 1,024–4,096 chunk rows may improve overhead but need measurement; transient Q2 certificate + retained roots/receipt can satisfy cold restore while keeping compact total retention.

**Owner/Browser holds:** whether a transient Q2 certificate (not retained) satisfies REQ-AUTHORITY-RECOVERY's independent source comparison; whether a derived durable index is acceptable and how it is bound/invalidated; whether the manifest schema may add a qualification/proof receipt; whether to adopt the proposed crash-recovery frame requirement; any native/source/actor/science/FF/world/F26 decision. These are not decided here.

## 9. Strongest reverser and smallest lawful test

**Strongest reverser:** if the Q2 certificate cannot be independently held/qualified as the writer's proof DB, or if the physical verifier cannot compare every family body/selector to it without a second representation, then the second I02 certification must stay. In that case the minimum is only the one-journal reduction + cold qualification/index, not the one-certificate reduction.

**Smallest lawful discriminating test (not run):** a fixed sourcefree fixture with all 13 families, at least one repeated/ranked event, one typed absence, one weight absence, one routing-unknown and one cross-universe distinct relation; build with (A) current two-certificate path and (B) one-certificate path; assert identical Q2 roots, identical persisted member hashes, identical native I03/I05 facts/replay/negative/revocation results, and inject one body/selector/locator corruption plus one crash before manifest. Measure build time, peak disk, process-tree RSS, cold open, 1/10/100 operations. This is a witness, not a production/native acceptance.

## 10. No final architecture acceptance

This is one bounded construction return, not the integrated architecture, not independent C, not H1, not protected adoption. The architect must adjudicate this against the query specialist and the whole frame. All 26 NOT_ADOPTED / 14 HELD / 52-24-21 / F26 / native-source-actor-science holds remain.
