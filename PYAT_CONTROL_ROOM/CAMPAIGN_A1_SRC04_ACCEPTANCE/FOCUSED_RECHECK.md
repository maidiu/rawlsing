# Campaign A1 SRC04 — focused repair recheck

**Terminal result: `PASS_SCOPED_A1_FIRST_ORIGINAL_C11_POSITIVE`.**

The two prior RED defects are repaired and independently reproduced. The A1
first-original C11 positive is accepted at the source-native, eligible-slice
grade. This is not full original 178-field execution, I03/I05 execution,
semantic adoption, M2 or full scientific readiness.

## Exact repaired candidate

- Repaired candidate: `88b7f3cf111c1537511cf25207e1697c7edf0d52`
  (HQ merge of repair `009a3459b0e2ad392b0ff765be527e10cb8a7ff8` into prior
  review `0daf4aa5d143cc3a4e95984620a39489ed2fa39c`)
- Author/repair artifact: `a7cbfeef20c682c3da202ac858307c196560c12f`
- Candidate source branch: `agent/pyat-campaign-a-src04-original-c11`
- Review branch: `agent/pyat-campaign-a-src04-review`
- Program: `campaign_a_src04/evidence/PROGRAM.txt`, SHA
  `9e292a10df7052afb6db503a96c4b1721472d9030ab33094f8681b6bc8e49b50`
- User grant: `feb8320a149315fdfe74ae97f0aa91a3720aa141e5a1d5cbd5e2b97746c594f1`
  unchanged
- Prior review files remain unchanged:
  `DISPOSITION.json` `6d704424…`, `REVIEW.md` `7d8c7ece…`

## D01 — portable committed program/test path: PASS

- `PROGRAM_PATH` is now the committed `campaign_a_src04/evidence/PROGRAM.txt`,
  not an author-private `.r61` path.
- The new test checks the exact parent (`evidence`) and exact program SHA.
- Exact command in the review checkout:
  `PYTHONPATH=. python3 -m pytest campaign_a_src04/tests -q -o addopts=`
  → **7 passed in 1.00 s**.
- Fresh `git archive HEAD` extraction, with no `.r61` author control checkout:
  → **7 passed in 1.01 s**.
- Author receipt: 7 passed in 1.06 s; HQ 7 passed in 1.29 s.
- No path-renaming bypass: only the committed evidence program is accepted and
  its exact SHA is checked.

## D02 — no direct source stat/hash before admission: PASS

- `load_grant()` no longer calls `source_path.is_file()` or `sha_file(source_path)`.
- Discriminating test patches `Path.is_file` and `runner.sha_file` and asserts no
  source stat/hash occurs during `load_grant()` plus the wrong-source negative;
  it passes.
- Independent recheck probe:
  - after `load_grant()` and `wrong_source_negative`: source stats `[]`, source
    hashes `[]`, wrong-source `REFUSED` with
    `SOURCE_READ_SOURCE_SHA256_MISMATCH`;
  - actual subsequent read through the existing admission:
    SHA `2a48ba4b…`, 7,337 rows, 181 columns, 2 resolver calls,
    `PRE553_CONTENT_BOUND_SOURCE_SNAPSHOT@1.0.0`, content-bound and unlinked.
- No private grant-copy dependency: active code/evidence uses only the committed
  grant; `GRANT_AUTHENTICATION` records only
  `campaign_a_src04/evidence/USER_GRANT.json`. Old author-path records remain
  only in the preserved RED history.

## Unchanged A1 positive

The repair did not change the release or the accepted slice:

- `C11LogicalRelease` `fc111cfa78d0fc23b5c72c1dc4b45c39d35c66c394662d7b901f5422df3370ec`
- source SHA `2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18`
- 42 response fields + country/ser coordinates
- 15 unbound response fields + q701 coordinate excluded; 121 complete fields
  outside the first battery
- 308,154 RespondentEvents, 308,154 routing facts, 14,674 coordinate facts,
  630,990 public objects
- original authority unchanged: 1 replay-protocol ALLOW + 6 DEFER snapshots;
  canonical values withheld, no weight/population claim
- local-only bundle
  `~/Library/Application Support/Rawlsing/campaign-a-src04/releases/SRC04-fc111cfa78d0fc23`
  hashes unchanged:
  public `a47957a1…`, internal `2d9ea42a…`, replay `f13d893f…`,
  receipt `b1333a02…`

No raw respondent cells were printed or committed; the local bundle remains
private. No other original source was read.

## Artifact integrity and RED history

- 17/17 current `RETURN.json` artifact hashes match.
- Old RED history retained at
  `campaign_a_src04/evidence/history/red-92d4f793/MANIFEST.json`
  (`4e21e810…`), 13 files, 13/13 hashes match.
- The prior independently reproduced actual C11 positive, metadata and slice
  evidence remain the accepted unchanged baseline; no redundant expensive
  rebuild was performed.

## A1 acceptance grade and limits

**Accepted:** A1 first original-source C11 positive at the source-native,
eligible 42-field/2-coordinate slice grade, with real SRC04 admission/read and
DEFER semantic authority preserved.

**Not accepted / not claimed:** full 178-field original execution, I03/I05
execution, canonical/directional semantics, weighted/population claims, M2,
FieldForge/V553+/N11/N12/actor/Sorok/J52/W52, or full original scientific
readiness. The next consumer remains the existing I03/I05 owner only under a
separate exact query/operation authority; I03 execution was not required for
this A1 acceptance and remains a separate premise.
