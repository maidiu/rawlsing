# CONTROL ROOM — LOCAL DUAL-ROOT SHA SNAPSHOT — 2026-08-23

Status: `NONDESTRUCTIVE_INVENTORY_EVIDENCE__DELETE_PLAN_NOT_YET_AUTHORIZED`

Input manifest supplied from the user's local machine:

`Rawlsing_and_RawlsingsExcess_tree_sha_size_date.txt`

Generated:

`2026-08-23T15:27:12.888083-04:00`

## 1. Root identities

### Rawlsing

Path:

`/Users/matthewsmith/Desktop/Rawlsing`

Recursive tree SHA-256:

`30acc5b1e24cacfc8fe116762d15511f8afbd862fd8043b7a9a4135205603455`

Parsed regular-file count from supplied manifest:

`65,791`

Parsed regular-file bytes:

`30,763,909,398`

### RawlsingsExcess

Path:

`/Users/matthewsmith/Desktop/RawlsingsExcess`

Recursive tree SHA-256:

`dc6c8f9291a75a6fdfad9178be091c5a15fa0eb1bf7a4642c82ca9864e582247`

Parsed regular-file count from supplied manifest:

`47,625`

Parsed regular-file bytes:

`3,744,462,764`

## 2. Exact duplicate opportunity — preliminary

Parsing exact SHA-256 identities from the supplied manifest yields:

- `19,446` non-empty duplicate SHA groups;
- `58,201` redundant file instances beyond one survivor per SHA group;
- theoretical duplicate-byte ceiling of approximately `13.81 GiB` if every extra instance were deletable;
- `6,965` duplicate SHA groups cross the Rawlsing / RawlsingsExcess root boundary;
- theoretical duplicate-byte ceiling associated with cross-root groups of approximately `8.07 GiB`.

These are STORAGE-OPPORTUNITY numbers only.

They are NOT deletion authorization because self-contained packages, active worktrees, path-specific consumers, immutable provenance bundles, and unresolved canonicality can require repeated bytes.

## 3. High-confidence exact-identity witnesses already visible

### Question structure register historical duplicate

SHA-256:

`15f7b5613b7cb106c2d2db233925891d5392917b66eee19c1a5eff8e0655585b`

Size:

`26,582,348`

The supplied manifest contains multiple exact copies of this historical register.

A later local register exists with different SHA:

`9139c1ab77bf47a872f63ccae7784f3631f03a3e02a936b4ac41e75580c45219`

Size:

`26,582,238`

Therefore later vs historical register is NOT a dedup decision. It is G1A provenance/supersession work.

### Question-wave itinerary duplicate

SHA-256:

`866eb3ab25fbd9479781c15a0aecbb00a9d547fdc947cc443e8b904262b86eb3`

Size:

`11,059`

The same bytes occur across multiple historical/current manifest trees.

### 35-wave question/response authority archive duplicate

SHA-256:

`6723390b5bde5cae77a791a3078f7d3b8a4034f17f298751cf5e37224436c767`

Size:

`33,760,022`

The same immutable ZIP is repeated across multiple handoff/evidence trees.

This is a strong candidate for whole-archive deduplication after exact canonical survivor/path checks, because deleting a redundant whole archive preserves the internal self-contained package semantics of the retained copy.

### questions_master_drivers duplicate

SHA-256:

`d62accad0e956f739eada0718e4fb222429e7a90ed7889fff6f4f292b1a8a011`

Size:

`16,864,669`

Multiple exact copies exist.

A separate older recovered driver bundle also contains a DIFFERENT `questions_master_drivers.csv` with different SHA/size and is therefore not an exact duplicate and must not be deleted under dedup law merely because the filename matches.

## 4. Immediate control-room consequence

The preservation/dedup desk SHALL use the supplied SHA manifest as the first global physical-copy census.

The first local dedup campaign should prioritize:

1. byte-identical whole archive copies;
2. byte-identical extracted verification/build copies with a retained immutable parent archive;
3. obvious scratch/cache duplicates;
4. cross-root RawlsingsExcess duplicates with canonical Rawlsing survivors;
5. repeated loose authority objects only after G1A canonicality/supersession closure.

The campaign SHALL NOT begin by deleting manual-authority artifacts merely because many copies exist.

First establish canonical semantic ownership; then remove physical redundancy.

`DUAL_ROOT_SHA_SNAPSHOT_ADMITTED__DEDUP_OPPORTUNITY_LARGE__DESTRUCTIVE_PHASE_NOT_YET_AUTHORIZED`
