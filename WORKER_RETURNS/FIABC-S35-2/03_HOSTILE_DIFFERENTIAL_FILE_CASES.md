# FIABC-S35-2 — Hostile Differential-File Cases

Terminal: `FIABC_S35_2_DERIVATIVE_SOURCE_LINEAGE_AUDITED__ALTERNATE_FILE_EDGES_EXPOSED`

Repository: `maidiu/rawlsing`  
Base: `agent/vozhd-premain-fiabc-wave3-fanin-r1`  
Worker branch: `agent/rabochii-premain-fiabc-s35-2-derivative-lineage-falsifier-r1`

## Controlling holding

`DERIVATIVE_ACCEPTABLE != DIFFERENT_SOURCE`.

The admissible proof chain is:

`derivative identity -> governed derivation/replay -> canonical source SHA`.

A filename, pathname, source-family label, wave label, row count, column count, respondent count, variable-name set, apparent cell equality, or self-asserted `source_sha256` field is not a substitute for that chain.

The governing Source-Native Constitution is stronger than mere content resemblance: exact source bytes remain primary physical evidence until positive source-equivalence certification and separate retirement authority; path/name is never a byte hash; caches, derived aggregates and legacy tables are nonauthoritative unless separately certified for a named use.

## Audit surface

This worker used GitHub/browser repository surfaces only. No local source carrier was opened and no local Codex or measured P2X was run.

The audit covered:

- the exact CLOSED_35 byte inventory and Authority71/72 preparation estate;
- A04 source-estate reconciliation and LiTS-I/WVS7 certification capital;
- Wave-3 I04 runtime packaging and its stable copied assets;
- Wave-3 I05 candidate-neutral oracle contract;
- Wave-3 Q02 local-source/runtime ledger and R6X/oracle protocol;
- Wave-3 I06C preserved-work accounting;
- current Wave-3 backend derivative/reopen paths;
- the generic Parquet C11 carrier;
- the frozen Candidate-C CACC1/CACC2 implementation at its accepted owner commit;
- historical `survey_microdata_reload_manifest_*.json` files;
- `section85/inputs/*.json` source-local selector indexes;
- repository-tree searches for raw SAV/DTA duplicates and cleaned/transcoded/decoded/extracted/cache/carrier surfaces.

No canonical CLOSED_35 raw `.sav`/`.dta` bytes are committed in the Wave-3 tree under duplicate canonical basenames. The dangerous historical alternate files survive instead as path references and build-history evidence.

## HDF-01 — same canonical filename, different bytes

**Construction:** supply a file named `WVS Wave 7.sav` with the expected 97,220 × 613 geometry but change one byte, one value, one missing declaration, or metadata field.

**False equivalence lure:** filename + shape + plausible labels all agree.

**Required result:** reject. The canonical WVS7 root is SHA-256 `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`. Direct WVS materialization and oracle materialization both hash the physical file before semantic execution.

**A/B/C danger:** if only one candidate receives the changed file, equal-work comparison is already invalid even if downstream query outputs happen to match.

## HDF-02 — historical Arab Barometer Wave 2 DTA versus canonical SAV

Historical reload evidence names:

`/Users/matthewsmith/Desktop/Rawlsing/data/Data/Arab Barometer/ABII.dta`

with 12,782 rows and 468 columns.

The CLOSED_35 canonical root is:

`Arab Barometer Wave 2.sav`  
SHA-256 `6529841b97bd56463490d810ad24ceaa4866066d12e4651a7081682d413606a1`.

No repository evidence audited here proves `ABII.dta -> governed conversion/equivalence -> canonical SAV SHA`.

**Required result:** `ABII.dta` is a different source until a positive equivalence chain exists. Matching dimensions are evidentially worthless for identity.

## HDF-03 — historical Asian Barometer W5 merged release

Historical reload evidence names:

`W5 Merged Data/20230505_W5_merge_15.sav`

with the same 26,951 × 308 geometry associated with current Asian Barometer W5.

The CLOSED_35 canonical root is `Asian Barometer Wave 5.sav`, SHA-256 `2576e428ff8de3c8d93a418c9120a1c2955ab7b1f35961d8c18fa562bc4b5e63`.

**Required result:** reject the historical merged release as a substitute until its exact SHA and governed equivalence to the canonical root are proved.

## HDF-04 — producer-versioned EVS files

Historical manifests name producer-versioned sources including:

- `EVS 1981 ZA4438_v3-0-0.sav`;
- `EVS 1999 ZA3811_v3-0-0.sav`.

The canonical CLOSED_35 files are `EVS 1981.sav` and `EVS 1999.sav` with different authority identities defined by the source-byte inventory.

**Attack:** choose the producer-versioned file because year, dimensions and variable labels match.

**Required result:** reject absent exact release-equivalence proof. EVS 1999 is additionally L2-blocked for producer-authoritative malformed-text repair/alignment; an alternate producer release cannot silently solve that authority problem.

## HDF-05 — EVS trend aggregate masquerading as a wave source

Historical reload evidence names `EVS 1981-2017 TREND ZA7503_v3-0-0.dta` with 224,434 rows and 635 columns.

This is not one of the CLOSED_35 roots. It is a compiled/harmonized multi-wave product.

**Attack:** use the trend file for all EVS candidates because it appears to contain the same years and familiar variables.

**Required result:** hard reject inside CLOSED_35. Admission would require an explicit denominator change plus per-parent canonical SHA lineage, row/source-release provenance, and harmonization authority. A compiled aggregate is not a raw-wave equivalent.

## HDF-06 — South Asia alternate producer filenames

Historical reload evidence names:

- `SA_Wave1/SDSA 2005.sav`;
- `SA_Wave2/SDSA 2013.sav`.

Canonical CLOSED_35 roots are `South Asia Wave 1.sav` and `South Asia Wave 2.sav`, with SHAs `de7b51f9abf455b072555a84c5592e3ac46bb32c4f9f61bc055160f7d871e571` and `6a5329ea16f4546188167edd691e0e6adbeae0737a015470aa26df0e01206f22`.

**Required result:** reject alternate filenames until byte-level equivalence is positively proved.

## HDF-07 — family glob silently expands CLOSED_35

The old Asian Barometer reload manifest also names nine Wave-6 national files that are not in CLOSED_35.

**Attack:** a future loader uses a family-directory glob rather than the canonical registry; Candidate A sees W1/W4/W5 while Candidate B or C additionally sees W6 national files.

**Required result:** hard stop. Source-estate denominator is authority, not filesystem discovery. New source files require explicit source-estate admission and certification.

## HDF-08 — detached WVS structural preimage

Current Wave-3 backend behavior is:

1. when the exact WVS source is exposed, create `wvs7_projection_structural_input.json` from the source;
2. later source-free stages may reopen that durable structural preimage;
3. `materialize_from_structural_input` verifies schema, a semantic self-hash, the asserted canonical source SHA, row count and variable count.

The file's self-hash proves that its fields have not changed *relative to the hash stored in that same file*. It does not, by itself, prove that those fields were emitted by `projection_structural_input_from_wvs_sav` over canonical raw bytes.

**Hostile construction:** create a structurally legal document, alter `B_COUNTRY` values or physical missing declarations, retain the canonical `source_sha256` string, and recompute `structural_input_identity`.

**Required hardening:** source-free reopen must require a parent derivation receipt binding the exact structural-input identity to:

- verified canonical raw WVS SHA;
- exact materializer blob;
- exact derivation operation;
- process/root/candidate ownership;
- creation ordinal before source closure;
- no cross-candidate transfer.

Without that outer proof, a detached structural preimage is an unproved alternate source edge.

## HDF-09 — LiTS-A preserved R5 root path substitution

The Wave-3 dependency ledger names the preserved carrier as `RAWLSING_EE_P2X_LITS_A_R5_ROOT`. The backend opens the path through `R5CompactLongShardedReader`.

The current ledger row does not itself pin that external path to a fixed carrier manifest/member hash.

**Hostile construction:** point the environment variable to an old R5 carrier, a copied carrier, or a carrier built from a noncanonical/earlier LiTS file whose layout is still readable.

**Required result:** before bind, verify exact persistent carrier identity and reconstruct the complete chain:

`carrier member hashes -> carrier manifest/release/replay -> source_artifact_ref 7cac43e2... -> governed projection/workload -> Candidate A preserved-stage identity`.

Path existence is not proof.

## HDF-10 — historical preserved carrier promoted into current law

R6X deliberately preserves old durable transformed carriers and historical C stops. Preservation prevents evidence destruction; it does not requalify that state under the Wave-3 six-cell law.

**Attack:** reuse an old carrier or old stop merely because it survived reconciliation.

**Required result:** historical-only unless current source, candidate, workload, runtime, isolation, operation and determinant compatibility are proved. Historical LiTS-B C11 receipts cannot substitute for fresh B work. Old LiTS-C/WVS-C stops cannot define current C capability.

## HDF-11 — oracle product substituted for candidate work

The immutable LiTS ASTRA-D04-R2 learned product is a lawful candidate-neutral expected-truth reference because I05 verifies its canonical LiTS source replay and immutable identities.

**Attack:** copy that accepted product into one or more candidate result slots.

**Required result:** fail. Oracle provenance may be derivative; candidate empirical work must still be freshly executed. `DERIVATIVE_ACCEPTABLE` at the oracle layer does not authorize result substitution.

## HDF-12 — compatibility-decoded file becomes a new source

Accepted source law allows latin1/compatibility decoding for bounded physical execution, including LiTS I-IV and the problematic EVS 1999/2008 physical reads. That is reader configuration, not source-text semantic authority.

**Attack:** save the compatibility-decoded table to CSV/DTA/Parquet, then treat the saved file as the new canonical source because its rows look correct.

**Required result:** reject unless the persisted derivative has its own content identity and a governed replay to the exact raw-source SHA. The original raw bytes remain authoritative. EVS 1999/2008 semantic text blockers remain unresolved by mere decoding.

## HDF-13 — source-local selector index crosses releases

`section85/inputs/*.json` records variable/question names but no source SHA, release identity or replay root.

**Attack:** apply an index built for one release to an alternate release with the same variable names.

**Required result:** the selector file may be a nonauthoritative fixture only after an outer exact-source binding. Matching variable names never prove source equivalence.

## HDF-14 — CACC1/CACC2 treated as full LiTS source

The frozen Route-C accelerators have comparatively strong determinant lineage:

- CACC1 binds exact LiTS source SHA, decoder identity, projection authority, slot ledger, governed projection, accepted C11 release, replay and authority closure; its manifest also hashes physical and logical content.
- CACC2 binds the CACC1 determinant plus discovery authority, predicate catalog, risk partition, production operation and frontier.

That makes them acceptable **derivatives at their qualified scope**.

It does not make them the LiTS source. Current F02 needs q310/q311 and other material outside frozen CACC1/CACC2 scope, so Wave-3 I03 correctly requires exact-source fallback.

**Attack:** let Candidate C use CACC while A/B use the complete source.

**Required result:** reject current full-F02 equivalence even though the accelerator itself has valid provenance. This is the exact meaning of `DERIVATIVE_ACCEPTABLE != DIFFERENT_SOURCE`: provenance is necessary but scope equivalence is separately necessary.

## HDF-15 — stable runtime copy drift

I04 copied three runtime assets into stable paths byte-for-byte and recorded their Git blobs:

- LiTS runtime materializer: `9406bacfd928393f6a159a46216aa1f7ec129f34`;
- WVS runtime package: `e04e84b76f8b4eb53905276dd025938bf2e5f6fe`;
- WVS projection materializer: `11b28416aac5a4899706150721f2f8ac8bb6ee43`.

**Attack:** replace a stable-path file with a semantically similar or newer copy while keeping the same pathname.

**Required result:** fail on Git blob drift. Here pathname is intentionally subordinate to byte identity.

## HDF-16 — extracted subset appears sufficient

**Construction:** make a subset containing only the rows/variables currently queried and produce outputs identical to the full canonical source.

**Required result:** reject as source equivalence absent a governed subset derivation whose scope is explicitly authorized and whose parent is the canonical raw SHA. Output agreement does not prove source identity, and omitted source-native state can matter under later invalidation/replay.

## Falsifier verdict

The estate supports three distinct conclusions:

1. **Proved bounded derivatives exist.** WVS runtime packaging, accepted LiTS projection/C11/replay products, exact Git-banked LiTS runtime authority, generic Parquet C11 carriers, and qualified CACC artifacts carry real identity/provenance law. They are not automatically "different sources."
2. **Historical alternate files genuinely exist.** Old reload manifests expose alternate producer/release files and an EVS trend aggregate without SHA bridges to the CLOSED_35 roots. They must remain alternate/unproved.
3. **Current derivative reuse still has two high-value binding obligations.** The external LiTS-A R5 root and detached WVS structural preimage need explicit parent-chain receipts at the live execution boundary. Neither should be allowed to derive equivalence from path, geometry, self-hash, or asserted source-SHA metadata alone.

The controlling admission rule for S35 and the later live transposition should therefore be machine-enforced:

```text
CANONICAL RAW SOURCE
  --exact byte SHA-->
GOVERNED DERIVATION / REPLAY RECEIPT
  --binds producer + determinants + parent SHA + scope-->
DERIVATIVE IDENTITY
  --exact consumer binding-->
CANDIDATE

Any missing arrow = STOP.
```
