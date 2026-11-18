# Full-width writer exact reuse / cap diagnosis

## Verdict

**`NO_EVIDENCE_SUPPORTED_REPAIR_YET__DECISIVE_MEASUREMENT_REQUIRED`**

The 512×600 run capped inside `writing`:
- wall **600.250 s**, SIGTERM
- partial **1,951,192,968 B**
- **not sealed**, no publication
- sampled RSS 128,729,088 B
- proof SQLite DB **1,789,673,472 B** + journal **8,325,712 B** =
  1,797,999,184 B, about **92.1%** of partial bytes

Bytes are **not CPU evidence**. The cap cause is not attributable yet.

## Exact writer / proof path

Accepted writer at `68aa`:

- `pre553_source_direct_parquet_estate.py`
  - SHA-256 `068fc525…`
  - `_Sink.add/flush/close` 220–265
  - `write_direct_estate` 460–602
  - `_verify_emitted_physical_payloads` 523–525
- `_pre553_direct_i02_sourcefree.py`
  - SHA-256 `b70e9a49…`
  - SQLite proof setup 413–425
  - family validation/insert 441–500
  - hashing/header reconstruction 517–581
- `_pre553_external_i02_certificate.py`
  - `_insert_object` 96–134

The `writing` stage includes, without partition:

1. Parquet Zstd sink writes, 512-row groups, plus event locator;
2. `build_sourcefree_direct_i02` full stream validation and SQLite proof;
3. candidate-projection/replay hash reconstruction;
4. `_verify_emitted_physical_payloads` full re-read;
5. member hashing, fsync and publication.

## Repeated / duplicated work visible

- Sink: `_row` / `canonical_json` body materialization and Parquet write.
- I02 proof: independent object type/carrier/hash validation, SQLite
  `objects`/`closure`/family tables, per-chunk commits.
- Hash reconstruction: sorted SQLite closure/projection reads.
- Verification: re-read of emitted Parquet and comparison to proof.
- Publication: hash every member and fsync.

The large SQLite proof scratch is required evidence. It must not be stripped or
casually bypassed.

## Existing fast path

No accepted W03/#1006 direct-I02 writer fast path was found in the focused
existing returns read. No same-size reuse candidate is established.

A speculative candidate would be to reuse the sink's already materialized row
projection at the tap boundary when populating the I02 proof tables, retaining
the distinct duplicate/occurrence/closure/negative/census proof and exact
external I02. This is **candidate only**; no timing supports it and no owner
grant exists.

## Decisive missing measurement

Split the `writing` span on the preserved writer without a new size/retry:

- tap / `_Sink.add` / `flush` time and counts;
- `build_sourcefree_direct_i02` time and counts;
- verification time;
- member hashing/fsync/publication time.

Current instrumentation provides only:
- `BUILD_STAGES.stage=writing`
- elapsed/RSS/scratch samples
- partial file sizes.

A test-only wrapper around those existing boundaries is the smallest decisive
diagnostic. No product edit is justified before it.

## Source pins

- Capped return: `.../ANVIL_WIDTH512_BOUNDED_CONSTRUCTION_20261118/RETURN.json`
- Partial tree: `.../PARTIAL_TREE.json`
- Source: `9ba991847ec043ab12f00244c4d3a0301ddb0f98`
- Writer: `068fc525b6c117fbb3feba52f740f7e764674ff0b2a78f52e5b649b5fafe643a`
- I02 proof: `b70e9a49b5d0a2445ed76053b04579fa0cbede2717286c7708dfb6f18ff016d2`

Correctness at `aee95429609c372564e996c2d3d3eb30e9253cbf` is not reopened.

## Limits

No build/query/retry, no product edit, no proof stripping, no new canonical
dataset, no source/science/protected/current authority.

**STOP for decisive writer stage timing.**
