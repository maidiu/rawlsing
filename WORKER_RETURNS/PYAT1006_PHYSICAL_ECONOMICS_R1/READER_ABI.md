# PYAT #1006 accepted physical/query ABI used by this baseline

## Immutable code pins

- Assigned branch HEAD: `codex/pyat1006-physical-baseline-20261113-r1`
  at `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`.
- Accepted S2-C: `b7b697b69f0acea12174937ee824c19ac34ac284`;
  independent G5 terminal #990.
- Accepted S2-D: `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`;
  independent G5 `ba8d760cd8e31a9baff9b45698bd4117f4baa456`.
- Accepted S2-B: `092db6bc50a6f256756edf8ab1e95981e2d95abe`;
  independent G5 `96ad0fe202ad7cbe5ea98d5e055c010a944b0a79`.

Product blobs at the tested HEAD:

| file | blob |
|---|---|
| `rawlsing_next/pre553_source_direct_parquet_estate.py` | `0e4b34ce4973bb4d23b6105faea55b9056ecf373` |
| `rawlsing_next/pre553_direct_estate_i03.py` | `8b4d5ca2c865e4ef5f5fb609cce15ca3ba64899e` |
| `rawlsing_next/_pre553_direct_i02_sourcefree.py` | `451727511af7f727b082c518aae2f4a3dbe2ba3a` |
| `rawlsing_next/_pre553_external_i02_certificate.py` | `cd5368e46a5f2d6016afc2d421717b4191a03005` |
| `rawlsing_next/pre553_saved_c11_admission.py` | `22749addc1fca5f0b90e12728847c390aafa7a84` |
| `rawlsing_next/pre553_saved_workload_integration.py` | `cc8aa32512378261406d765f0b049c748cb3e11f` |
| `rawlsing_next/pre553_issued_workload.py` | `b02810677ae66231e5e59b09aefe9bd63a31aaa3` |
| `rawlsing_next/pre553_batch_runner.py` | `49e3974c658d66a270815d9faa3798b40d4488b1` |
| `rawlsing_next/pre553_carrier_execution.py` | `ad1164f21f5f7422a03a19b1b856636edb89cb03` |

## Exact derivation note (do not silently replace)

S2-D `9d96a9c...` contains S2-C, but S2-B `092db6b...` is **not** an ancestor
of S2-D.  The direct-I02 sourcefree builder blob is identical
(`451727511af7f727b082c518aae2f4a3dbe2ba3a`).  The external-I02 certificate
blob differs:

- S2-B accepted: `2af16c6d9097333570a3417519995bd8dc7fcaa0`.
- S2-D tested HEAD: `cd5368e46a5f2d6016afc2d421717b4191a03005`.

The S2-D blob is the `6a5c12f...`-derived version with a narrower cold
`coverage` header parsing path; it is not the S2-B accepted stronger typed
header validator.  This baseline used the assigned S2-D tree exactly.  It did
not replace S2-B, cherry-pick a production branch, or re-open accepted S2-C/D.
Any integration that needs the S2-B validator must obtain an explicit owner
handoff and re-run the cold/sourcefree courts at the resulting cut.

## Physical writer

`rawlsing_next.pre553_source_direct_parquet_estate`

- `SourcefreeDirectI02Sections` is the one-shot 13-family input:
  `manifest`, `sections: Mapping[str, Iterable[object]]`, `typed_absences`,
  `replay_protocol_authority_ref`, `replay_protocol_version`,
  `deterministic_tie_order_rules_ref`.
- `write_direct_estate(source, universe_ref, authorized_private_root, *,
  chunk_rows=512, expected_i02=None) -> EstateReceipt`.
- `EstateReceipt(path, manifest_sha256, i02, reconstructed_v1_release_ref,
  family_counts, retained_bytes)`.
- Publishes exactly the 13 family Parquet members, `event_locator.parquet`,
  and `manifest.json`; the temporary I02 proof SQLite is deleted before
  publication.  No full `C11LogicalRelease`, `ReplayManifest.closure_refs`, or
  `C11Repository` is constructed.
- `VerifiedDirectEstate(root, *, exact_path,
  independently_held_manifest_sha256, independently_held_i02,
  current_authorizer)` verifies the held manifest, member hashes, I02 roots,
  event/locator census and row-group topology; `iter_family`,
  `select_events` and `_events_from_postings` are bounded row-group readers.

## Native saved readers

- `pre553_direct_estate_i03.DirectEstateI03Session(estate)` builds the
  execution-local SQLite `events`/`members` posting index and supplies
  `indices_for(query, release_refs)` to the existing native I03 evaluator.
- `pre553_saved_c11_admission.SavedC11Admission.open(*, root, exact_path,
  independently_held_manifest_sha256, independently_held_i02, release_ref,
  runtime_catalog, current_authorizer)` binds the exact estate/release and the
  existing `RuntimeObjectCatalog`.
  - `execute_i03(query_ref=..., predicate_ref=...)`
  - `execute_i05(discovery_authority_ref=...)`
  - `check_current()`
  - `resolve_release_exact(ref) -> SavedReleaseIdentity`
- `pre553_saved_workload_integration.execute_saved_batch(admission, *,
  manifest, predicate_ref_by_query, discovery_authority_ref_by_key,
  prior_receipts=(), max_units=None)` runs the existing native Batch scheduler.
- `pre553_issued_workload.execute_issued_workload(..., saved_admission_factory=...,
  source_factory=None, host=..., purpose=..., allow_test_only=True)` and
  `resume_joined_workloads(...)` exercise NORMAL/COMPLETED/PARTIAL/ABSENT.
- None of these is a new scientific engine.  The native I03/I05/Batch owners
  still own query/predicate/risk/state/replay/fact semantics.

## Ready-to-reuse boundary for #997/#998/#1007

The physical side is ready to accept a **single-pass, source-backed,
one-shot 13-family iterator** and the exact external I02/source/replay/universe
manifest.  The missing #997 work is the authentic source snapshot/decode/
projection tee into those iterators plus the postconsumer receipt/fate join.
This return does not implement or simulate that bridge.  True source decode
time is `NOT_RUN_PENDING_997`; no source rights or original35 claim is made.

#998/#1001/#1007 can reuse the exact `write_direct_estate` /
`VerifiedDirectEstate` / `SavedC11Admission` ABI, held manifest/I02 pins, and
the measured stage boundaries, but must run their own integrated and
independent-resource courts.  This standalone baseline is not #1001
certification.

The follow-through `followthrough_r2/` locality experiment is NOT part of this
accepted ABI.  It is a runtime-only TEST_ONLY override (`EXPERIMENT_NOT_IMPLEMENTED`)
and does not change any accepted reader signature or production file.
