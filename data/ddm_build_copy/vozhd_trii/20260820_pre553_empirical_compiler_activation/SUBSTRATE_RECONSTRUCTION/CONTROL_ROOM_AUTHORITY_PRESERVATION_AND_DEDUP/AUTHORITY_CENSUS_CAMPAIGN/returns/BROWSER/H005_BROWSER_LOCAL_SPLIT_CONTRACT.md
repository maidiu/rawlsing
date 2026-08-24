# H005 Browser/Local Split Contract

Status: `ACTIVE__BROWSER_AVAILABILITY_INVENTORY_PUBLISHED__LOCAL_DELTA_ONLY`

Recorded: 2026-08-23

## Governing division of labor

HARVEST-005 is split because the original order mixed two different capability domains.

The local machine is uniquely needed to search the live filesystem roots:

- `/Users/matthewsmith/Desktop/Rawlsing`
- `/Users/matthewsmith/Desktop/RawlsingsExcess`

Browser HQ is better suited to the cross-carrier relational computation and adjudication.

The governing equation is:

`H005_REQUIRED_EVIDENCE - BROWSER_AVAILABLE_EXACT_EVIDENCE = H005L_LOCAL_DELTA_SCOPE`

The normative Browser availability list is:

`H005_BROWSER_AVAILABLE_EVIDENCE_INVENTORY.csv`

## Browser evidence already held

Browser has the exact returned bytes of all four prior harvest packets:

- H001 ZIP SHA `e283735f6af208578b373a2e30d8df7fc8ad3f86edc05874fa43e4be9092db78`
- H002 ZIP SHA `70789a6556f70c2c6be0771defe00fec918b7e64514e37d82744493431f1dc37`
- H003 ZIP SHA `0ad166ec3da232f56a5a0c9612862e99b2091e8ba80626bc76417e7a4524e461`
- H004 ZIP SHA `b7ce4c0de1aea7db1e08d4c4faf3447f22809b62b95800502f0f3ee52c0c7abd`

These are not merely summaries. Browser can inspect every exact member.

Browser also has three Library-side discovery indexes materialized and hash-bound:

- `rawlsing_full_tree.txt` SHA `3fcc51f1a125f2a1eff90d932133cc033fb1145432b9e25ae3f9542ed09ea145`
- `Rawlsing_and_RawlsingsExcess_tree_sha_size_date.txt` SHA `1e93b7774ffffc977bc80b940becdd7576cda10c6bb4a0c211b01a5634da6668`
- `Rawlsing_repo_tree_dates_sizes_sha256.txt` SHA `8064b2a6d5fdd7cb3916aedbea59f74728b3dddf7b08ba9384531d95d5cd9c44`

Browser additionally has connected GitHub access to current/preserved governed authority surfaces listed in the availability inventory.

## H005L — local responsibility

The local worker is an evidence-retrieval worker only.

It must:

1. search the two local roots exhaustively enough to identify H005-responsive identity carriers;
2. hash responsive files before deciding whether bytes are needed;
3. compare each content identity against `H005_BROWSER_AVAILABLE_EVIDENCE_INVENTORY.csv`;
4. return exact bytes only for content Browser does not already have, or when a distinct local physical occurrence is itself necessary provenance;
5. return manifest-only occurrence rows for identical Browser-held SHAs when local-path evidence matters;
6. prioritize the unresolved Browser-availability classes explicitly marked `BAV-GAP-*`.

It must **not** perform the global candidate-universe join, cross-carrier coverage computation or final collision court.

## H005B — Browser responsibility

Browser HQ owns:

- construction of the candidate question-occurrence universe;
- carrier schema/identity inspection;
- indexed/relational joins across carriers;
- explicit one-to-many/many-to-one/ambiguous membership preservation;
- collision census under each historically used identity coordinate;
- per-family/wave coverage counts;
- identity-law adjudication after mechanical evidence is complete;
- Trii/Chetiri implications and next dependency.

Browser should use relational/indexed operations such as DuckDB, Polars, pandas merge/hash indexes or equivalent. Naive candidate-by-carrier nested scans are forbidden as an implementation pattern.

## Content-addressed exclusion rule

A local path is **not** new evidence merely because the path is new.

If a local responsive file has a SHA already listed as Browser-held exact bytes:

- record the local occurrence if provenance matters;
- do not duplicate its bytes in the return ZIP.

If the SHA differs:

- it is a distinct evidence candidate;
- return the bounded exact bytes when H005-responsive;
- do not infer newer/better/canonical from path or mtime.

## Known high-priority local delta targets

The current Browser inventory does not yet positively establish an exhaustive exact-byte set for:

- `questions_master.csv`;
- current final-codebook/question-index identity surfaces;
- local-only distinct FQRA/QSM/QSMv2 identity-bearing variants;
- source-native question/variable identity indexes or manifests needed to bind normalized rows to source occurrences.

Those classes are the main reason H005L still exists.

## Noncollapse law

H005L and H005B must preserve disagreement.

Neither worker may:

- invent `question_uid`;
- deduplicate ambiguous rows;
- choose authority by recency/path/row order;
- infer question equivalence from similar text;
- treat `uncovered` as `missing authority`;
- repair `d62`;
- create new semantic/driver/structural authority.

## Terminal handoff

H005L returns the local evidence complement.

H005B then combines:

`H001-H004 exact bytes + Browser GitHub authority + Browser Library indexes + H005L delta`

and produces the actual current-35 identity/coverage baseline.
