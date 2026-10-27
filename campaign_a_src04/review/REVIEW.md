# Campaign A1 — SRC04 independent acceptance review

**Verdict: `REVISE`.**

The actual SRC04 original-source read and the C11 slice release are real and were
independently reproduced. The campaign return is **not yet a clean accepted A1
evidence packet** because the committed focused-test/runner path is not portable
in the review checkout and the runner performs a direct source SHA read outside
the existing source-read admission. Both are bounded runner/evidence repairs;
the independently reproduced C11 positive remains valid at its stated slice.

## Exact identity and governing inputs

- Candidate: `92d4f793d0ef5de58f21e23b1ad0fa286fa74a01`
- Author/branch: `agent/pyat-campaign-a-src04-original-c11`
- Review branch: `agent/pyat-campaign-a-src04-review`
- Candidate remote SHA: `92d4f793d0ef5de58f21e23b1ad0fa286fa74a01`
- Governing program: `9e292a10df7052afb6db503a96c4b1721472d9030ab33094f8681b6bc8e49b50`
- User grant: `feb8320a149315fdfe74ae97f0aa91a3720aa141e5a1d5cbd5e2b97746c594f1`
- Control commit: `2d2814df614018dbca5687839fe562d16bf900e7`
- Source: `SRC04`, `/Users/matthewsmith/Desktop/Rawlsing/data/Data/Arab Barometer Wave 1.sav`,
  SHA `2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18`,
  7,337 rows × 181 columns, 178 configured response slots.

The grant and program hashes were checked against the committed evidence and the
control commit before candidate claims were used. No other original source was
read during this review. No respondent cells or row-wise objects were printed or
committed.

## Independent evidence actually obtained

### Authentic source read

A fresh private probe used the existing
`decode_with_source_read_permission` admission with a resolver tied to the pinned
user grant/program/control identity. It read only the authorized SRC04 path and
returned:

- source SHA `2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18`
- 7,337 rows, 181 columns
- two resolver calls
- `PRE553_CONTENT_BOUND_SOURCE_SNAPSHOT@1.0.0` custody, content-bound and
  snapshot-path-unlinked
- physical metadata digest `1ef1739f290e69ccb74b0bbd0486e8338e8eae6224c924e520e0da141f5cc3be`

The independent metadata check compared all 181 config slots against the actual
incidence and the R154 metadata witness: ordinals, names, storage types, labels,
value labels, missing declarations, source SHA, crosswalk count/names and item
identity all matched. This is not a fixture or source-free substitute.

### Actual C11 positive

The same probe independently re-derived the eligible slice from the observed
cell/value bindings and rebuilt the native release through
`build_validated_c11_release_from_config`:

- `C11LogicalRelease` `fc111cfa78d0fc23b5c72c1dc4b45c39d35c66c394662d7b901f5422df3370ec`
- source manifest `8f8015a1c7c13ac24609693551f51c964feeae9d2ff9097be9b9ca55c5b76d71`
- replay manifest `ca70d58e2b2f4881dfe7809862d0c005c6e015753175fbcd937ff218546d22bb`
- 42 `QuestionVariableBinding`, 7,337 `RespondentIdentity`
- 308,154 `RespondentEvent`, 308,154 `RoutingEligibilityFact`
- 14,674 `EmpiricalCoordinateFact`
- 630,990 public objects / 7,379 internal records
- zero canonical response, coordinate or question values emitted
- zero weight facts

The selection matched the author exactly: 42 response slots (ordinals 3–26 and
28–45), ordinals 1/2 (`ser`, `country`) coordinates, 15 unbound response slots
(27, 46–55, 175, 176, 179, 180), q701/ordinal 158 excluded, and 121 complete
response fields outside the first battery explicitly not selected. All 178
response slots and all 181 physical slots are accounted. The choice is a
structural first-battery slice, not an outcome-selected example.

### Negatives and restoration

Independently reproduced:

- wrong source decision → `SOURCE_READ_SOURCE_SHA256_MISMATCH` before opening the
  sentinel path; no source read by the admission for that negative;
- full 178-response configured release → `SourceBackedC11FacadeError` on an
  unbound observed value/state;
- canonical-retained q101 slice → `C11IntegrityError` because canonical mapping
  authority is `DEFER`;
- positive slice restored to the exact `fc111cfa...` release hash.

### Local durability

The local-only bundle
`~/Library/Application Support/Rawlsing/campaign-a-src04/releases/SRC04-fc111cfa78d0fc23`
was resolved and checked without publishing it:

- public_objects `a47957a1d0b4e6df29195f70b1c3d122cc69b1a8a484b60bbe072d9eff126edd`
  (630,990 lines)
- internal_records `2d9ea42a36e9b326f65f3ed5219ddf84a9fdb7d634ff8e459cc3e8892bc89538`
  (7,379 lines)
- replay_manifest `f13d893f363753ad0d17bbf58c5a8bd51fcb12334daf85232b4365d66f96d09e`
- receipt `b1333a021c28f0a4fe3a8272d469d9dab2ecb619cf08fcae3fdf18246fb9d8c9`

The public object distribution is exactly 308,154 RespondentEvent,
308,154 RoutingEligibilityFact, 14,674 EmpiricalCoordinateFact, 7 AuthoritySnapshot
and 1 EmpiricalUniverse. No non-null canonical value and no weight fact was found.

## Demonstrated failures — `REVISE`

### D01 — committed focused tests do not run in the review checkout

Exact command:

```sh
PYTHONPATH=. python3 -m pytest campaign_a_src04/tests -q -o addopts=
```

Actual result in the review worktree: **2 failed, 3 passed in 0.97 s**.

```
CampaignError: governing PROGRAM.txt is absent
run_campaign_a_src04.py:158
FAILED test_committed_grant_is_the_pinned_human_grant
FAILED test_wrong_source_refuses_before_source_open
```

The runner hardcodes `PROGRAM_PATH = ROOT / ".r61/campaign-a-src04/PROGRAM.txt"`.
That author-private file is absent here; the exact governing program is present
at `.r61/campaign-a-src04-review/PROGRAM.txt` (SHA matches). Supplying that path
in-process makes the same tests pass **5 passed in 0.73 s**, confirming this is a
path-resolution/portability defect, not a test-logic failure. The committed
`TEST_RESULTS.json` claiming 5 passed is therefore not reproducible from the
committed checkout.

Minimal owner/repair: Campaign A1 runner/evidence. Resolve the program from a
committed/pinned evidence copy or an explicit verified review/control path (not
an author-private `.r61` path), rerun the exact command, and update the test
receipt/return.

### D02 — direct source SHA read outside the existing admission

`run_campaign_a_src04.py` `load_grant()` does:

```python
source_path = Path(document["source_path"])
if not source_path.is_file():
    ...
if sha_file(source_path) != EXPECTED_SOURCE_SHA256:
    ...
```

before constructing the source-read request/resolver. The direct-read probe
recorded the SRC04 path in `sha_file` calls before any
`decode_with_source_read_permission` resolver call. This is a source-byte read
outside the existing admission and breaks the runner's claimed
zero-I/O-before-current-permission property and the
`NEGATIVE_WRONG_SOURCE.before_source_io` claim. The actual positive decoder call
is correctly made through the existing admission; the preflight hash is the
defect.

Minimal owner/repair: Campaign A1 runner. Remove the direct source `is_file`/SHA
preflight; let the SHA-checked physical decoder/admission verify the exact source
after the current resolver. Re-run the positive/replay and the wrong-source
negative through the repaired path.

## Scope qualification

This review accepts the **C11 source-native, eligible-slice positive** separately
from all broader claims:

- original semantic authority remains `DEFER`; the release withholds canonical
  values and makes no canonical/directional/weighted/population claim;
- no fixture or synthetic original universe/authority is present;
- no original empirical workload, I03/I05 execution, FF, CI/prod, N11/N12,
  Sorok/actor or J52/W52 action occurred;
- no original source bytes or row-wise objects are committed; the release is
  local-only;
- 42 fields are a legitimate first battery, not a claim that all 178 configured
  fields are ready.

## Next consumer and held premise

The C11 release is available to the existing I03/I05 owner only if that path is
separately authorized. It is not I03/I05-executed here. The existing I03
operation-successor owner requires an exact `EmpiricalQuerySpec`, an adopted
positive predicate/operation-successor authority, runtime catalog identity and a
historical parent snapshot; canonical/directional semantics remain held under
`DEFER`. I05 learned production is further downstream and not attempted. No new
semantic ALLOW or downstream workload is issued by this review.

## Next necessary action

1. Repair D01 (portable program resolution) and D02 (no direct source preflight
   outside admission), commit/push the bounded runner/evidence repair.
2. Re-run the exact focused test command and the repaired primary/replay and
   wrong-source/restore checks in a clean checkout.
3. Re-review only the affected boundary. The already reproduced C11 release
   `fc111cfa...` need not be rebuilt unless the repair changes its identity/path.
