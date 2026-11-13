# PYAT999 S2-A — one exact public-selector repair

## Decision

**`S2A_PUBLIC_SELECTOR_REPAIRED__G5_PENDING`**

The accepted S2-C direct estate's public selector now completes the native
body/locator positional and selector coverage check over every event row
**before** respondent, target or state filtering, refuses a coherently
re-pinned poison, and returns selected events in native canonical-ref order
without deduplicating distinct occurrences.

This is an author return. It is not independent G5 acceptance and does not
claim production source, scientific issuance, CURRENT, original35, 100k/6 GiB
or protected merge.

## Exact artifact

- Branch: `agent/pyat999-s2a-public-repair-r1`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat999-s2a-public-repair`
- Startup: `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`
- Code/test cut: **`1cb7977b78022f8def26b769714b4c7ac519ece0`**
- Return content commit: `17e1471550c7e77228a40607d9eaaeef4b3fc971`
- S2-C accepted executable: `b7b697b69f0acea12174937ee824c19ac34ac284`
- Contract source cut: `WORKER_COMMISSIONS/PYAT_S01_S05_FLIGHT_997_1002/sources/owner_comment_6866766494.md@66c9dd38fa31d075b99b1bdbf90ca03a56f29b08`
- Starting target blob: `0e4b34ce4973bb4d23b6105faea55b9056ecf373`
- Repaired target blob: `dca76c98f6c097bb8d79316087eaf548b1b45594`
- New test blob: `cdadb84531659a0dc9264b740e12d9f084e5380b`

Changed code/test paths only:

- `rawlsing_next/pre553_source_direct_parquet_estate.py`
- `rawlsing_next/tests/test_pre553_s2a_public_selector_h26.py`

No writer, schema, manifest, layout, locator schema, native I03/I05,
`DirectEstateI03Session`, native `_select_respondent_events`, S2-D, science,
current, issuer, accepted test or prior-return file was changed. No adapter
was added.

## Original independent RED — reproduced before edits

The exact reviewer witness from `c900cf463694a8b21af7f3f8bd8da6a6b23d1d82`
was preserved verbatim at:

- `WORKER_RETURNS/PYAT999_S2A_PUBLIC_REPAIR/baseline/reviewer_s2a_native_witness.py`
- `WORKER_RETURNS/PYAT999_S2A_PUBLIC_REPAIR/baseline/reviewer_s2a_native_witness.json`
- `WORKER_RETURNS/PYAT999_S2A_PUBLIC_REPAIR/baseline/reviewer_s2a_native_witness.out`

It was run on the pristine `9d96a9cac` worktree before any source edit. A real
sourcefree 4-respondent/4-locator estate had one target-specific locator
`native` field poisoned while every event body/ref and physical count stayed
intact; the locator hash and independently supplied manifest digest were
coherently re-pinned.

Baseline output:

| Measure | Baseline |
|---|---:|
| Native selected count | `1` |
| Normal public selector count | `1` |
| Poisoned public selector count | **`0`** |
| Poisoned public selector raised | **No** |
| Same estate native I03 | **Refused** |
| Native I03 error | `DirectEstateError: cold I03 event posting lacks exact positional/selector coverage` |
| Body/ref corpus unchanged | `true` |
| Selector peak traced bytes | `12,521` |
| Parent max RSS | `103,579,648 B` |

The original review script is not a green regression: it expects a dictionary
0-vs-1 observation. The new test is assertive and requires the public selector
to raise a typed `DirectEstateError` for the same poison.

## Repair

### Complete coverage before filtering

`VerifiedDirectEstate.select_events` now stages selected refs through a private
`_stage_validated_public_selector` helper. For every row group it reads the
`RespondentEvent` body selector columns and the `event_locator` row group and
checks, position by position:

- row-group and row count equality;
- `locator.group == gid` and `locator.offset == local offset`;
- `locator.ref == body.ref`;
- exact respondent, native, canonical, component and state equality to the
  reconstructed body columns;
- total count equality to the committed event/locator census;
- duplicate exact event-ref refusal (the native `events` table is unique by
  ref; distinct occurrence refs remain distinct).

This validation happens **before** the respondent/target/state selection
predicate. It therefore runs for `states=frozenset()` and when every candidate
target posting would otherwise be poisoned away. No event is yielded until the
full validation pass succeeds.

### Native canonical order with bounded memory

Selected locator rows are written to a disposable SQLite table containing only
`ref, respondent, native, canonical, component, state, gid, offset`. A
`SELECT ... ORDER BY ref` cursor supplies the existing `_events_from_postings`
reader. This matches native `_build_release_index` / `DirectEstateI03Session`
ref-canonical order, preserves multiple distinct occurrence rows, and does not
deduplicate them. The temporary table is deleted on generator completion or
exception; it is not a second persistent body corpus. No whole-table
`pq.read_table`, C11 graph or eager event inventory is introduced.

### Semantics preserved

- `native_only=True` wins over canonical/component.
- Authorized canonical and component matching remain exact.
- `states=None` includes all states; `states=frozenset()` returns empty only
  after complete integrity validation.
- Exact respondent/target refs, source/universe/root and live current checks
  remain in force.
- Empty valid selection remains distinct from routing `UNKNOWN`.
- Selected bodies are still reconstructed and validated by the existing
  `_events_from_postings` path.

## Green evidence

New test file:
`rawlsing_next/tests/test_pre553_s2a_public_selector_h26.py`

Verbose:
`WORKER_RETURNS/PYAT999_S2A_PUBLIC_REPAIR/evidence/green_h26_5_verbose.txt`
— **5 passed in 3.01s**.

Covered:

1. **H26 exact target-native poison**: public selector refuses before a subset;
   empty `states` also refuses; native I03 refuses the same poison; untampered
   estate restores the exact public refs and complete native fact/release
   oracle.
2. **H27 authorized canonical/component aliases and order**: two same-
   respondent, same-value occurrence events are returned in native canonical
   ref order, no dedupe; `native_only` precedence, canonical/component aliases,
   `target=None`, `states=None` and empty states are checked; canonical,
   component and state locator poisons refuse.
3. **H28 empty vs routing UNKNOWN**: a genuinely event-empty respondent yields
   no events while the native fact remains nonpositive/unknown, never
   `OBSERVED_ZERO`.
4. **Changed legitimate native event and exact restore**: changed public refs
   and changed native I03 facts; original root restores exact public refs and
   full native facts/release refs.
5. **Current/wrong source**: revoked current refuses; wrong source pins refuse;
   restored current resumes exact behavior. Existing H29 root/keyspace tests
   remain green.

## Tests actually run

### S2-A focused + new regression

- Darwin: **62 passed in 9.86s**
- Linux existing qualified Lima s2b: **62 passed in 13.58s**
- Logs: `evidence/darwin_s2a_focused_62.txt`,
  `evidence/linux_s2a_focused_62.txt`

### S2-C focused

- Darwin: **31 passed in 7.54s**
- Linux: **31 passed in 8.81s**
- Logs: `evidence/darwin_s2c_focused_31.txt`,
  `evidence/linux_s2c_focused_31.txt`

### S2-C inherited

- Linux existing qualified Lima s2b: **91 passed in 41.85s**
- Log: `evidence/linux_s2c_inherited_91.txt`
- Darwin: 59 passed, 32 host-blocked because `VerifiedExternalI02` requires
  Linux `/proc/self/fd`; this is a host-capability hold, not a product pass.
  Log: `evidence/darwin_s2c_inherited_91_host_blocked.txt`

### S2-D focused preservation

- Darwin: **31 passed in 21.70s**
- Linux: **31 passed in 55.46s**
- Logs: `evidence/darwin_s2d_focused_31.txt`,
  `evidence/linux_s2d_focused_31.txt`

No accepted test was edited, skipped or weakened. The full accepted 202
court and 100k benchmark were not run.

## Resource evidence

Probe: `WORKER_RETURNS/PYAT999_S2A_PUBLIC_REPAIR/resource_probe.py`  
Results: `WORKER_RETURNS/PYAT999_S2A_PUBLIC_REPAIR/resource.json`

Synthetic material local fixture: **256 respondents / 256 events**, sourcefree,
not 100k.

| Measure | Value |
|---|---:|
| Retained estate bytes | `9,758,503` |
| Peak disposable selected-index bytes | `16,384` |
| Estate-open family opens | `2` |
| Public-select family opens | `3` |
| Public-select row-group reads | `257` |
| Public-select body reconstructions | `1` |
| Cold public select | `0.1340 s` |
| Repeated public select | `0.1315 s` |
| Cold native I03 | `0.8156 s` |
| Repeated native I03 | `0.7867 s` |
| Selected count | `1` |
| Selected refs equal repeat | `true` |
| Native I03 fact | `SUPPORTED` |
| Native I03 repeat equal | `true` |
| Parent peak RSS | `153,587,712 B` |
| Fresh-child peak RSS | `60,567,552 B` |
| Fresh-child cold select | `0.1325 s` |
| Fresh-child source opens | `[]` |
| Source-extension opens | `[]` |
| Full C11 builds | `0` |
| `pq.read_table` fallbacks | `0` |
| 6 GiB cap | PASS at material local fixture |
| Integrated 100k/6 GiB | **NOT_RUN** |

The child is one fresh process, not a multi-process tree. Source opens count
original-source extensions only; estate Parquet opens are the authenticated
reader. Scratch is the disposable selected-ref index, not a retained body
corpus.

## Courts

- **Engineering:** repaired at sourcefree material local grade; G1–G3 pass,
  G4 pass scoped fixture. G5 is pending the distinct nonauthor reviewer.
- **Scientific:** `NO_ORIGINAL35_SCIENTIFIC_ACCEPTANCE`; sourcefree TEST_ONLY.
- **Authority:** no new source, current, host, actor, issuer or merge grant;
  only the exact owner-granted S2-C public-selector exception.
- **Integration:** **UNMERGED**.

## Self-critique

- The public selector now scans every event row on every call. At 256
  respondents this is ~0.13 s and a 16 KiB disposable index; 100k behavior is
  not proved.
- The legacy private `_locators` helper remains in the file but is no longer on
  the public path; it should not be mistaken for the repaired public selector.
- Public selector and native I03 implement the same parity law in separate code;
  they are independently tested, not a single shared helper.
- The H26 regression uses a re-pinned manifest with intact bodies; it does not
  prove all source-native/original35 conditions.
- The Darwin S2-C inherited host block is handled by the existing Lima run, not
  by changing tests.
- No independent G5 has occurred. The author cannot self-accept.

## Holds / next actor

Original35/source science/rights, production CURRENT/host/actor issuer,
integrated 100k/6 GiB and protected merge remain external holds.

The same distinct nonauthor reviewer `ses_e30c25800ffeT8XbyTuHekRCme` receives
exact implementation SHA **`1cb7977b78022f8def26b769714b4c7ac519ece0`** once,
for one scoped independent G1–G5 re-review. No additional A/B round. On
accepted original G1–G5, the reviewer may issue `S2A_TERMINAL_CLOSED@SHA`;
the author does not.
