# 03 — Compact storage, qualified queries, currentness and durable recovery

**Basis:** code-exact sourcefree architecture evaluation at `integration/pre-main-reconciliation-r1@1f77f2036427a410429184780ef884ec4f253ad0`; observed W03/W04 receipts from [paused HQ cut `1fb84959874778838ccb1cfb4a374818405c32a2`](https://github.com/maidiu/rawlsing/blob/1fb84959874778838ccb1cfb4a374818405c32a2/WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/hq/BROWSER_HQ_C11_STORAGE_QUERY_DAG_HANDOFF_20261111.md) (blob `0d25fa3fa66bbfe572bd785ff87547d00c46b7d0`). **No runtime or performance tests run in this architectural return.** W03/W04 existing writer/saved-access/legacy-reuse author lanes remain undisturbed and their output unadjudicated by this document.

## A. Physical estate to retain — truth, derivatives, transient work

| Category | Actual material | Persistence/authority law |
|---|---|---|
| **Original retained source** | Exact SAV/DTA bytes, source snapshot SHA, instrument/admin/codebooks, reference authorities and permissions | Remain independent source and semantic determinants under their source/rights owners. C11 does not self-authenticate original questionnaire completeness. |
| **Authoritative canonical C11** | Complete I02-accepted semantic release, release/source/semantic/replay identity, irreducible semantic/authority records, Parquet/Zstd members + exact manifest | Required for *product-qualified* C11 on authorized host (`PERSISTENCE_HELD` otherwise), not required for disposable synthetic fixture. **One canonical release logical estate**, not an extra analytics database truth. |
| **Required scientific products** | Actually accepted full native F1–F4 facts/negatives/discovery receipts, required learned M1/M2/B5 releases and FF01/N9 when lawfully produced | Retain when product/replay/cold consumer requires. Historic scientifically valid fact and current permission are separate. |
| **Derived *optional* physical accelerators** | Existing compact event bodies/selectors; minimal typed respondent/target/state/locator projection; only measured-beneficial bitmap postings/cohort and columnar batches | Source/release/codec/authority/version keyed, byte-verified, disposable, regenerable without changing evidence. No compulsory State-B/State-C index or second permanent corpus. |
| **Ephemeral execution material** | I03 index, risk-qualification witnesses if not worth retention, temporary Arrow batches, DuckDB operators/spills, staged digest/merge runs | Bounded-memory and disk; never silent global cache; delete/secure according to source rights. Track peak transient footprint separately from retained. |
| **Durable work custody metadata** | Batch work identity/state/receipts, expected immutable output refs and locations, publication generations/recovery journal where necessary | Small single-writer or correctly coordinated transaction state; journal not an authority issuer. SQLite only if filesystem/manifest proof cannot safely handle concurrent unit publications. |

The physical claim is **not** one file. It is one *semantic authority* and the smallest defensible portfolio of physical copies.

**All retained bytes:** `S_retained = S_source_if_locally_retained + S_C11 + S_required_results + S_optional_indexes + S_immutable_work_outputs + S_recovery_metadata + S_other_sidecars`. Report separately **peak transient bytes** (Parquet staging, Arrow/spill, sort, tmp, orphan data, test/diagnostics). Do not conceal a second complete event-body cache because the advertised index is small. Use canonical/derived/ephemeral directory inventories and exact release-version retention policy; peak disk can exceed final retained bytes during atomic publication.

## B. What the inspected code actually costs

1. **Decode/transport**: `pre553_physical_decoder.py` L306–406 makes source snapshots; `decode_sav` L825 and `decode_dta` L839 bind physical metadata and typed values. `PhysicalSourceIncidence` can be a transient rich object. A current selected-column read may be economical, but neither a tiny Parquet file nor `R5Codec` obviates decoding, instrument authority or required physical-cell completeness. Inspect reader batch behavior for DTA/SAV and source-specific encoding; any source-native performance claim needs separately permitted original bytes.
2. **Projection and I02**: `pre553_source_backed_c11_facade.py::project_c11_candidate_from_physical_cells` L502 collects `events=[]`, `coords=[]` and `weights=[]`, sorts them and constructs a complete candidate; `pre553_c11_ingest.py::validate_c11_source_release` L743 performs global checks and I02 seal. Merely streaming the physical input does not make *candidate construction and validation* constant memory. A future segmented I02 proof must conserve cross-section/cardinality/collision checks and complete release identity before sealing.
3. **Existing C11 persist**: `pre553_parquet_carrier.py::_relation_objects` L212 materializes per-relation lists, `_write_tables` L228–247 constructs full-row dicts, sorts, canonical logical digest and `pa.Table.from_pylist(rows)` simultaneously. It makes the compact event representation expand again. **This specific bounded-writer fix already belongs to the existing paused W03/W04 worker**, not this architecture author.
4. **Existing C11 reopen**: `_read_rows` L275 uses `pq.read_table(...).to_pylist()`; `reopen` L279–360 rehydrates whole relations, verifies digests, reconstructs objects and invokes `_make_validated_release`. It is authenticated reconstruction, not economical selected access. A scoped verified read session is a distinct I02-owned ABI decision, assigned to the existing saved-access lane first.
5. **Repository/I03**: `C11Repository._commit_validated` L115 stages a copy of exact-object dict and stores I03 indices; `_pre553_query_predicate._build_release_index` L63 scans respondent, event, routing, weight, coordinate objects. Existing compact `_EventRead`/`_RespondentEvents` and `I03GroupedExecutionScope` are real partial memory/computation savings; a new projection must **replace** some of these expensive resident structures, not accompany all of them unchanged.
6. **Native proof**: `_pre553_query_eval._evaluate_index_group` L626 initializes full-domain raw and rational weighted cells, gathers risk and denominator member refs, used object/authority refs and exact state; `_build_fact` L879 finalizes identity/provenance/replay. Even if SQL group-by takes milliseconds, exact witness/fact construction may dominate. No benchmark may time SQL while excluding the real native consumer.
7. **Full Cartesian F4**: `_pre553_query_common._parse_target_plan` L315–391 materializes `itertools.product` into `full_domain` and `domain_keys`, and the evaluator creates full-domain zero maps before scan. Domain arity admission must calculate `D = product(len(component.domain))` with overflow-safe bounded multiplication *before* constructing domain. If present public ABI requires full domain and D exceeds resource budget, return honest resource HOLD. Sparse/factorized complete-domain identity is a *separate semantic-ABI grant*, not this tranche's hidden accelerator.
8. **Grouped reuse**: `pre553_empirical_query.I03GroupedExecutionScope._core_key` L543–579 returns `None` for current runtime binding or runtime-bound index authorities. `evaluate` L594–680 enforces capped groups/member limits. Shared columnar scans must preserve those prohibitions; equal source/question names do not imply equal authorization, denominator or source scope.
9. **Exact arithmetic**: the native weighted path accumulates `fractions.Fraction`. An accelerator may group equal **exact weight identities** and aggregate integers, then use native rational reduction. Floating SQL `SUM(weight)` is not an accepted substitute; survey designs/variance/estimand permissions are separate. Unsupported design-weight topology → native or typed HOLD, never convenient equal weighting.

## C. Measured resource evidence — what it proves and what it does not

W03/W04 handoff's **one** generated narrow 100,000-row / 200,000-event old/new cold comparison:

| Quantity | Protected baseline | Candidate | Interpretation |
|---|---:|---:|---|
| Cold launch → first answer | 681.934 s | 605.164 s | 11.26% faster observed in one scoped comparison; no repeated-query confidence claim |
| Sampled peak process resident | 3,700,494,336 B | 2,841,853,952 B | 23.20% lower in that run, not a whole-build storage proof |
| Construction wall | 399.368 s | 323.329 s | 19.04% faster in one generated shape |

The later **direct saved-artifact** pilot did not reach the required matched query clocks: initial preparation both exceeded 6 GiB; repaired R3 baseline metadata reuse succeeded (peak **1,055,891,456 B**, baseline canonical carrier **154,463,257 B** over 13 files, metadata **23,322,456 B**); candidate construction reached partial persistence and was cap-killed (**6,468,513,792 B** peak sampled, exit −9). A **42,409,491 B** derivative accelerator was present but canonical staging incomplete. There are **no** accepted full-size paired saved-artifact query/repeated-use or candidate total-storage results in these records.

The fixed sampled cap was **6,442,450,944 B** (6 GiB); physical host reported 16 GiB. Sampled monitors can overshoot before SIGKILL; target a material safety margin and report process-tree peaks, not an engine-internal memory budget alone. No automatic 84-run benchmark, blind repeat, cap raise or reduced dataset represented as 100k proof. User priority is compact *total* storage and fast lawful repeated use, even if one-time construction costs modestly more.

## D. Minimal physical read and optional index policy

**State A — canonical only:** accepted C11 Parquet/Zstd + exact source root, authenticated on-demand semantic objects. No extra persistent event table assumed.

**State B — minimal typed projection if measured:** derived keyed rows with:
- `release_ref`/`universe_ref` and source-scoped respondent exact-ref key (dense ID only an *internal* map under that exact universe; cannot leak into published identity);
- native question and separately authorized canonical-question exact refs, component/subitem exact ref;
- **each** event's exact ref, original physical row/variable/occurrence identity, response rank/order/multiplicity and source topology;
- typed value dictionary ID with separate raw-physical and authorized-canonical dictionaries, explicit typed state and routing/applicability sidecar;
- essential coordinate/routing/weight/design locator refs, not an invented flattening of semantics;
- verified pointer to canonical segment/row offset, codec/ABI version and full source/release/semantic/authority determinants.

State B is not a standalone scientific release and cannot silently exclude source-necessary entities. If its body/locator plus canonical compressed source costs *more* than existing compact event representation without useful first-consumer gains, reject it for that source/operation family.

**State C — measured specialist:** compressed value postings or reusable exact cohort/qualified risk witnesses for repeated F2/F3/F4 request shapes, only after stable compatibility and real net savings. Evict by rule on source/release/authority/algorithm change or rights expiration. No permanent all-pairs corpus. Keep empirical product facts durable when required; do not preserve every temporary cohort forever.

**Parquet row groups:** source-local respondent-clustered row groups often help same-person F4 reconstruction; question/value-oriented postings may help selective F1/F2. Neither order is universally optimal. Use bounded controlled row-group sizes (candidate tuning, not asserted optimum), dictionary encoding/Zstd where compatible, and exact event/offset ordering. Measure row groups read, compressed/uncompressed byte ratios, selective scan amplification and random-access count. Avoid duplicate full-order stores unless the repeated workload pays for them. Optionally **co-produce** a provisional skinny projection from the governed writer stream, but it has *no accepted derived identity* until complete I02/C11 seal, postsealing manifest check and independent source-to-segment parity; otherwise build it lazily.

## E. Two-stage physical evaluation, cost function and capability refusal

First `qualify_exact_operation` validates the full relevant universe, risk/routing facts, question association, repeated-event support, source/right/authority, condition direction, target domain and measure. Its audit must include **invalid evidence even for respondents SQL would filter out** (for example unknown risk routing on a nonqualifying condition row). Only then may the physical calculator push down/select/group. A restriction planner returns `SUPPORTED_EXACT(plan, witness)` or `UNSUPPORTED(reason)`; unsupported means **native** if feasible, otherwise truthful `RESOURCE_HELD` or owner HOLD. SQL counts never issue `EmpiricalFact`.

Suggested first accelerated subset: one-source scalar RAW with resolved exact routing and states, including sparse target selection and unconditional/conditioned variants. Exclude composite cross-source, multi-response, weighted design, runtime-bound authority and giant implicit-domain cases until individually proved. The kernel must yield native-equivalent `_Evaluation` (or independently accepted versioned streaming witness), then existing `_build_fact`/replay. Finish with full public fact and first reader, not only grouped numeric counts.

Cost of a portfolio over true issued workload `Q` (never estimate `Q` from arbitrary all-pairs benchmark):

```text
C_total = C_source_build + C_I02 + C_canonical_write + C_saved_open
        + C_optional_index_build + sum_q N_q*(C_auth_q + C_qualify_q + C_calculate_q + C_proof_q)
        + C_required_storage + C_optional_storage + C_invalidation + C_crash_recovery
```

Hard constraints first: exact semantics/identity/negative/fact parity, privacy/current rights, ≤6 GiB whole-tree with headroom, bounded scratch disk and correct required products. Only then minimize measured amortized cost; amortization uses credible `N_q` per source-version/process restart, not hypothetical infinite cache hits. Native baseline, grouped baseline, columnar candidate must be timed on the **same issued entry and actual I03/FF consumer**.

## F. Durable publication, rollback and source/current authorization

Current `ParquetC11Carrier.persist` stages files and replaces the completed payload directory, hashes members and manifest; `reopen` verifies member hashes and logical digests. This is useful atomic-publication capital, **not a proof of all crash points, directory durability, stale external root trust or transactional multi-unit custody**.

**R2 D3 — Fail-closed contained paths before ANY persistence.** At the pinned code cut, `SourceReleaseManifest.__post_init__` (`pre553_c11_ingest.py` L99–113; blob `37cd35fa2e3420a3eea272a2902e96ab9ba38aba`) accepts a nonblank `release_id` without path containment. `ParquetC11Carrier.release_dir` (`pre553_parquet_carrier.py` L209; blob `9dad6713a3aae66717d4ab046e802a72c9b2aa90`) interpolates it as a filesystem path. `persist` L249 calls that method before validating the selector, whereas `reopen` L279–285 rejects separator-bearing release IDs. An absolute path can override `root/releases/<sha>`; traversal can escape it; a symlink under the configured root can redirect writes. Treat this as a static containment defect, **not an executed exploit**.

**Existing W03 writer acceptance contract, not competing implementation:** a **shared, deterministic selector/contained-path validator** must guard `release_dir`, `persist` and `reopen` before any source-derived filesystem access or write; reject absolute paths, slash/backslash, dot-path traversal, drive/UNC prefixes and other invalid names, or use an explicitly approved reversible safe path-component encoding without changing the logical C11 release ID. Anchor the configured private root using a trusted root descriptor; refuse symlink-escaped directory components and member paths; use no-follow/handle-anchored opens and publication or a demonstrably equivalent race-safe method on the supported filesystem; reverify after staging and before atomic rename. Do not treat lexical `is_relative_to` or `Path.resolve()` alone as protection against an attacker swapping a symlink during a multi-step write. Ensure manifests and orphan-adoption names remain contained as well. **No outside-root write, rename, deletion or staged spill** is permissible on invalid selector. Validate without silently breaking old safe release IDs; if legacy logical IDs require escaping, migration/read compatibility is separately explicit.

**P0/T02 host negative:** attempt `/tmp/... `, `../../outside`, `..\\outside`, drive/UNC-qualified and preexisting-symlink-parent selectors with otherwise valid sealed sourcefree releases. The protected test fixture must prove the writer fails *before creating or modifying any outside-root sentinel* and the reader rejects the same selectors. A postwrite reopen failure is not acceptance. The existing W03 writer owns the eventual code patch; the paused W03/W04 HQ has not been resumed here.

**Candidate state machine within existing Batch/Parquet owners:**

```text
PLANNED → CURRENTLY_ADMITTED → STAGING(bytes, expected unit + release identity)
       → VERIFIED(native payload/ref/replay + committed source/issuer scope)
       → DURABLY_PUBLISHED(immutable content identity + fsync/rename/generation)
       → COMPLETED_RECEIPT(only after payload is addressable and verified)
       → CONSUMED(currently entitled first reader)
failure anywhere: no positive completion; detect journal/artifact divergence on recovery
```

Exact atomicity and fsync behavior must be proven for the real filesystem/runtime; don't assume `os.replace` alone guarantees directory metadata survival across power loss. For multi-unit publication, choose **one** controlling completion state: durable immutable output + reconciled native receipt; a SQLite WAL index, if introduced, only locates/coordinates those outputs under a single-owner reconciliation law. It is not an independent source of scientific truth, and network/NFS/WAL assumptions must be proved. No new distributed scheduler.

**Fault matrix:** kill before any stage, during member write, after each member but before manifest, after manifest before rename, after rename before receipt, after receipt write/flush, during consumer lookup, during cached index spill, during orphan adoption. On restart:
- missing/corrupt committed payload **never** accepted from a journal label;
- a complete orphan may be adopted only when exact planned unit, source/release/authority envelope, expected external pin, native semantic payload and **present use** all verify;
- lost stage and partial member is ignored/quarantined; recompute only its invalid dependency units;
- already published completed facts are immutable; correction/revocation issues a new identity or denies current use, never silently edits old result;
- one real receipt per completed unit; exact full manifest retains incomplete/negative/held fates.

**Integrity versus external trust:** a manifest whose hash is computed from its own editable contents detects accidental corruption but not adversarial re-signing by an unauthorized writer. Saved-release and completed-result admission must have externally pinned expected root, trusted original I02 issuer/host decision and present current entitlement. Trust from historical fact hash is **not** present authorization. Keep source-specific spill/encryption/deletion/retention rules with the original rights; default cache/spill is **off** without an approved root. On revocation, deny serving the fact and apply the relevant retention/deletion policy to protected indexes, outputs and spill. Prevent TOCTOU by pinning selected object/descriptor and verifying opened file identity/generation as needed.

**R2 D1 — All-branch current authority, not just completed-cache check.** `pre553_issued_workload.py::resume_joined_workloads` L767–836: `COMPLETED` calls `_completed_entry_view` L741 without fresh `admit`; `PARTIAL` and **absent** entry call `execute_issued_workload` with `_resolver_for(item)` L832–836, which returns historical `item.record`. The existing `admit` L219 then validates a copied historical `CURRENT_GRANTED` record, **not a live issuer**. The P4 implementation must *require* an independently provisioned trusted `CurrentDecisionResolver` for the **whole** resume call; resolve each decision before looking at completed protected payloads, deserializing protected facts, opening source bytes/spills, adopting receipts, or starting any partial/new work. Check the full envelope, original source identity, expected jobs and host/purpose against freshly resolved issuer records, not `item.record.scope`; pass the **same external resolver** to resumed native execution and preserve its per-unit/postcompute checks. Recheck immediately before committed publication or protected serving. Missing/unavailable/changed/revoked issuer, or adapter replaying `item.record` without an independently trusted issuer binding, → fail closed. Keep historical computation authenticity and present-use permission distinct.

**Required 3-branch revocation test:** freeze the historical `item.record.currentness='CURRENT_GRANTED'` and a valid checkpoint; independently revoke at competent issuer; exercise `COMPLETED`, `PARTIAL` and **no checkpoint entry**. All three must refuse *before* source_factory call, restored protected result, cache/spill access, native positive receipt or first-reader serving. Test wrong host/purpose, issuer replacement mid-operation and unauthorized replay of a copied resolver. A completed-only test is expressly insufficient. No permission to create a new issuer authority or assume an outer wrapper exists.

**R2 D2 — Retained empirical product origin:** an authentic `EmpiricalFact`/profile hash and matching risk ref do not prove the source edition. When retaining or restoring a product that is to feed the frozen GT12 FF01 bridge, require independently authenticated **original release → source SHA → universe → fact/replay** evidence and present source/FF target-use permission. The GT12 bridge's fixed source identity must be verified *against the producer's actual origin before a source-bearing relation is emitted*; it cannot be the proof itself. Wrong-source internally valid Q86 facts are refused rather than laundering under Afrobarometer R5. This remains a bounded canary; no generic FF claim.

## G. Smallest decisive sourcefree probes (not claimed executed)

1. **Writer** (existing W03 lane; do not duplicate): forced multibatch mixed schema, late sparse field, empty relation, repeated/ranked events and identity ordering; expected exact canonical digest/member hash and native replay; SIGKILL stage/rename variant; **malformed absolute/traversal/Windows/symlink-escaped release IDs must be rejected before writing any outside-root sentinel**, using identical writer/reopen selector law; compare process-tree RSS and disk high-water against eager baseline. Claim is bounded expanded payload, not necessarily O(1) ordering keys.
2. **Saved read** (after existing saved-access decision): canonical only, fresh process, full external release pin, selected 3 different queries + I05, no source factory invoked; corrupt *unrequested* member to test whole-release integrity policy, wrong release/ref/codec, incomplete route; compare exact public facts and refusals to current eager native.
3. **Proof cost**: separately time admitted workload source preparation, qualified risk walk, physical group, `_build_fact` + replay, JSON/Parquet output, and actual FF01 read; report raw/weighted and F4 topologies, cold and repeated.
4. **Eviction and authority**: one historically CURRENT_GRANTED item but **externally revoked** issuer is submitted as COMPLETED, PARTIAL and ABSENT joined resume; all refuse prior to source access/result reveal even if historic hash verifies, while a genuinely current external issuer enables lawful completion. Cache delete/rebuild yields identical native fact; kill at each publication point and cold reconcile with zero false COMPLETED.
5. **Native high-arity**: huge declared product rejected before allocation; native smaller 3+ joint has identical valid zeros, ZERO_OVERLAP, ZERO_SUPPORT, INAPPLICABLE and unresolved fates. Future sparse-domain form remains an independent owner ABI decision.

**Decision:** use existing C11/compact/Batch owners and the minimum measured physical projection. Do not commission columnar duplication before current W03/W04 writer and read interface receive qualified returns. Qualified fast queries are a second step; true source-native Field Forge ingress is a later distinct scientific step. A completed architecture document is neither performance acceptance nor S3 source permission.
