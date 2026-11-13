# S2-B P2-02 — exact G5-R1 local repair return

**Disposition: `REPAIR_COMPLETE__PENDING_SAME_INDEPENDENT_G5_RECHECK`.**
This author return does not self-issue G5. Until the same independent nonauthor
receipt exists: `S2B_G5=REVISE_EXACT_DEFECT`, `S2B_TERMINAL_CLOSED=FALSE`.

## 1. Exact artifact and custody

- Original packet: S2-B / P2-02 / #919 under #909 R3/R3C/R3S.
- Frozen source/test base: `155cd1b7244ab22ede804386e6d5253a39fe3587`.
- Local author return-only base: `cc35e0a4e51394961f58b632dec8a149deea21a2`.
- Independent G5-R1 report: `acfd5b516a5ae8177730aeb672b846fe4e22fdfe`
  (`review/pyat-s2b-independent-g5-20261113-r1`).
- Isolated repair branch:
  `agent/pyat-s2b-g5-r1-repair-20261113-r1`.
- **Code/test repair SHA:**
  `092db6bc50a6f256756edf8ab1e95981e2d95abe`.
- Repair commit parent: `155cd1b7244ab22ede804386e6d5253a39fe3587`.
- Protected PRE-MAIN `6a5c12f04323d74001f9632063ec907f4fc4468e` untouched.
- No protected merge, no S2-C writer, no W03/W04 edit, no resource-model
  redesign, no external-root trust-model change.

### Lease / duplication check

`logs/12_LEASE_AND_DUPLICATION_CHECK.txt` records the check performed before
authoring:

- no remote repair-like ref existed;
- no G5-R1 repair PR existed;
- issue #919 had no repair launch after the commission comment;
- only the prior local author return and the independent review branch contain
  the frozen base.

The isolated worktree/branch above is the only writer. No `BLOCKED_LEASE` or
runtime hold applies.

## 2. Primary G5-R1 defect and repair

`rawlsing_next/_pre553_external_i02_certificate.py`,
`VerifiedExternalI02.__init__`, cold header boundary.

### RED on the frozen source/test base

The independent attack (`attacks/attack_malformed_header.py`) was rerun on the
frozen implementation. It recomputes only the caller-held physical root while
retaining the independently expected logical root:

```text
invalid-json UNTYPED_REFUSAL JSONDecodeError Expecting property name enclosed in double quotes
missing-key  UNTYPED_REFUSAL KeyError 'coverage'
json-null    UNTYPED_REFUSAL TypeError 'NoneType' object is not iterable
json-number  UNTYPED_REFUSAL TypeError 'int' object is not iterable
```

`logs/00_RED_REVIEWER_ATTACK_FROZEN.log`.

The new regression test was also run against the frozen production tree and
failed at the same raw `json.JSONDecodeError`
(`logs/01_RED_REGRESSION_TEST_FROZEN.log`).

### GREEN on the repair

The cold header boundary now:

- requires `coverage` to be present text;
- parses it explicitly as JSON;
- requires a JSON object, not a list/string/number/null;
- requires exactly the original `M01`–`M18` key set;
- requires every atom body to be a non-empty list of non-empty strings;
- raises `ExternalI02IntegrityError` with `from exc` for malformed JSON;
- preserves the existing `sqlite3.Error` typed handling;
- closes the SQLite DB on every refusal path.

The same four independent attack inputs now return typed refusal:

```text
invalid-json TYPED_REFUSAL ExternalI02IntegrityError certified M01-M18 coverage header is not valid JSON
missing-key  TYPED_REFUSAL ExternalI02IntegrityError certified M01-M18 coverage header missing or non-text
json-null    TYPED_REFUSAL ExternalI02IntegrityError M01-M18 missing or malformed in certified header
json-number  TYPED_REFUSAL ExternalI02IntegrityError M01-M18 missing or malformed in certified header
```

`logs/02_GREEN_REVIEWER_ATTACK_REPAIRED.log`.

The regression test
`test_s2b_g5r1_malformed_coverage_header_typed_refusal` covers invalid JSON,
absent key, null, number, array, string, empty object, missing/extra atom,
empty body, non-text token and non-array body, and reopens the untouched valid
certificate with real cold selector selection after every refusal
(`logs/03_GREEN_REGRESSION_TEST_REPAIRED.log`).

No `BaseException` catch was added. The semantic logical-root schema and the
external logical/physical root trust model are unchanged. No fallback source
access or integrity-check bypass was added.

## 3. Regression court

Full inherited court, final branch:

```bash
PYTHONPATH=. .venv/bin/python -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_external_i02_certificate.py \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py \
  rawlsing_next/tests/test_pre553_verified_semantic_range.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_c11_repository_ingest.py \
  --junitxml=s2b-g5r1-full.xml
```

**130 passed, 0 failed, 0 skipped** in 35.69 s; process max RSS 143,456 KiB
(`logs/04_FULL_COURT_130.log`, `logs/05_FULL_COURT_130.xml`). This is the
original 129 tests plus the G5-R1 regression test.

Targeted D1–D6, native 2→3→2/restore and G5-R1:
**9 passed** (`logs/06_TARGETED_D1_D6_AND_G5R1.log`).

Independent historical parity probes remain green: candidate projection,
historical replay ref and historical `C11LogicalRelease` ref are equal for the
base, weights, reversed order, aliases, multi-universe relation, all optional
internal families and the no-ReplayManifest-count case
(`logs/07_PARITY_PROBES.log`).

Direct native I03 full-query conservation remains 2 → 3 → 2 with exact
restoration (included in the targeted test log).

## 4. Resource behavior

The repair only touches the cold header parsing path. Builder resource behavior
is unchanged.

- 2,048 one-shot events / 1 respondent: retained 13,135,872 B; build 9.701 s;
  cold verify + 2,048 selects 0.294 s; Python peak 2,233,151 B; process max RSS
  42,500 KiB (`logs/08_MATERIAL_2048.log`).
- 100,000 one-shot events / **1 respondent**: retained 638,414,848 B; build
  508.827 s; cold verify + 100,000 selects 24.633 s; Python peak 2,231,538 B;
  process max RSS 40,424 KiB; sampled workdir+TMP peak 685,625,126 B
  (`logs/09_SCALE_100000.log`).

The 100k run is not a 100k-respondent or integrated 6 GiB proof. During this
session the VM root ext4 reported errors and remounted read-only; `/tmp`
tmpfs was used, and `SQLITE_TMPDIR` had to be set before Python startup. The
earlier retained-byte value 638,414,848 B is preserved. Build/cold times are
environment-degraded and are not presented as a performance improvement.

## 5. G5-R2 status

G5-R2 remains **NONBLOCKING and unchanged**. A caller that fraudulently replaces
the independently held logical root as well as the physical root can still
present a header-preserving selector-omission certificate; the direct installer
accepts it and native selection can return 1 where the sealed release requires
2. `logs/10_G5R2_NONBLOCKING_UNCHANGED.log` records this unchanged behavior.

This is future root-issuer/integration defense-in-depth, not part of this
repair. It is not marked native/production accepted.

## 6. Required next step

Send the exact code/test SHA
`092db6bc50a6f256756edf8ab1e95981e2d95abe` to the **same** independent
nonauthor G5 receiver from
`review/pyat-s2b-independent-g5-20261113-r1` for the exact R1 recheck only:

- rerun the original four malformed-header attacks;
- rerun the valid direct cold selection/restore;
- rerun the selected original native/129 court and this branch's full court;
- verify code/ABI/source equivalence;
- return `ACCEPT_SCOPED@S2_SOURCEFREE_DIRECT_I02` or
  `REVISE_EXACT_DEFECT` with a new reproducible in-scope first-reader breach,
  or `HOLD_EXTERNAL` only if genuinely indispensable.

No fresh broad G5 hunt and no additional reviewer chain.
