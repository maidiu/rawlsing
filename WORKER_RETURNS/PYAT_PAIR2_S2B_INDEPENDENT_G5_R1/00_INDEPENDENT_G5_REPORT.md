# PYAT R3 S2-B / P2-02 / #919 — Independent G5 receiving

**Role:** independent nonauthor G5 receiver (`G5_INDEPENDENT_NONAUTHOR_RECEIVER`).
This receiver authored none of the S2-B A/B rounds, the R5 direct builder, the
local repair, or the local runner return.

- **Verdict:** `REVISE_EXACT_DEFECT`
- **Scope of review:** original #919 S2-B / P2-02 under #909 R3/R3C/R3S and
  MCR-lite; sourcefree direct I02 logical/selector certification and compatible
  native I03 selector admission.
- **Not claimed:** S2-C cold persistent Parquet C11 body estate, original35
  source issuance/equivalence, CURRENT permission, P01–P20/T01–T18, native
  production permissions, protected merge, W03/W04.
- **Review branch:** `review/pyat-s2b-independent-g5-20261113-r1`
- **Return directory:** `WORKER_RETURNS/PYAT_PAIR2_S2B_INDEPENDENT_G5_R1/`
- **Evidence grade:** `INDEPENDENT_NONAUTHOR_EXECUTED__SOURCEFREE_DIRECT_I02__NOT_ORIGINAL35`

## 0. Prior independent G5 search

No distinct independent G5 verdict on the exact tested code was found. Remote
refs contain only author/adversarial S2-B branches and the local repair branch:

- `agent/pyat-s2b-r5-local-repair-20261112` = `cc35e0a...` (local execution and
  repair return; explicitly **not** independent G5)
- `agent/pyat-pair2-s2b-a-*` (Agent A author/adversarial R1–R5)
- `agent/pyat-pair2-s2b-b-*` (Agent B author/adversarial R1/R4)
- G5 branches `agent/pyat940-s1b-g5-r1`, `agent/pyat940-s1d-g5-r1`,
  `agent/pyat940-s2f-g5-r1`, `agent/pyat960-s1e-g5-r1`,
  `agent/pyat960-s2g-g5-r1`, `agent/pyat918-s1c-g5-r1` cover other packets,
  not S2-B.
- No `review/*s2b*` or `*s2b*g5*` ref was found.

The local GitHub credential can read repository contents/commits but lacks
Issues/Pull-Requests API permission (`Resource not accessible by personal access
token`, HTTP 403). A verdict published only as an issue/PR comment therefore
could not be inspected. No code/ref evidence of one exists. This receiving was
performed directly. See `evidence/10_PRIOR_G5_SEARCH.txt`.

## 1. G1 — Contract and historical identity

### 1.1 Exact artifact

| Item | SHA |
| --- | --- |
| Repaired tested code/test commit | `155cd1b7244ab22ede804386e6d5253a39fe3587` |
| Local repaired return HEAD | `cc35e0a4e51394961f58b632dec8a149deea21a2` |
| Previous direct-builder implementation | `edd0611d1ea0e80a47692635fe3bd73a079f1bec` |
| PR #979 head | `cc35e0a4e51394961f58b632dec8a149deea21a2` |
| PR #979 merge | `b0357abe24aa6a562dab0b32b11e99c79e2ba010` |
| Protected PRE-MAIN | `6a5c12f04323d74001f9632063ec907f4fc4468e` |

`cc35e0a` is `155cd1b` plus `WORKER_RETURNS/PYAT_PAIR2_S2B_LOCAL_R1/` evidence
only. `git diff --exit-code 155cd1b cc35e0a -- rawlsing_next` exits 0; every
`rawlsing_next` blob under test is the `155cd1b` blob. The PR merge is
`cc35e0a` merged into the Agent A R5 documentation head
`fef8abd4c61508bb85c1797b73006b60c5fe0170`, not PRE-MAIN. PRE-MAIN remains an
ancestor; it was not reset, modified, or merged into.

Changed blobs at the tested cut:

- `_pre553_direct_i02_sourcefree.py` `451727511af7f727b082c518aae2f4a3dbe2ba3a`
- `_pre553_external_i02_certificate.py` `cd5368e46a5f2d6016afc2d421717b4191a03005`
- `test_pre553_direct_i02_sourcefree.py` `cef715f69af2d21243b454787c689da7f0086bbf`
- `test_pre553_external_i02_certificate.py` `7a8a0f5a60c5d5a776cea44f3beea109e0f98ff3`
- `.github/workflows/pyat-pair2-s2b-external-i02.yml` `7b60661e315ea1d528c67a19fa137715acdb144a`

### 1.2 Original I02 semantics conserved

The direct producer receives `SourcefreeDirectI02Sections` (manifest + 13 typed
family streams + lawful typed absences + replay protocol inputs). It does not
call `validate_c11_source_release`, does not construct `C11LogicalRelease`, does
not construct `ReplayManifest.closure_refs` as a tuple, and does not mint the
legacy validation seal. It stores corpus/closure/bindings/selectors/occurrence
rows in SQLite, validates each record through the existing carrier/authority
validators, and reconstructs the historical candidate projection,
`ReplayManifest` and `C11LogicalRelease` SHA-256 identities by streaming sorted
disk rows.

Executed parity against the actual legacy oracle (`validate_c11_source_release`)
is green for the base typed-absence fixture, WeightMeasureFact present, reversed
section order, canonical/component aliases, multi-universe SourceUniverseRelation,
all four optional internal replay families, and a legacy-valid manifest with no
`ReplayManifest` count declaration. The independent probe log is
`evidence/03_PARITY_AND_ATTACK_PROBES.log`.

The direct schema is distinct:
`PYAT_S2B_DIRECT_SOURCEFREE_CANDIDATE_CERT@1` vs the legacy
`PYAT_S2B_EXTERNAL_I02_LOGICAL_SELECTOR_CERT@1`. The ordinary legacy installer
still refuses the direct schema (`cannot impersonate`). The direct installer is
separate.

### 1.3 External-root distinction

`ExternalI02Roots` requires caller-supplied logical and physical SHA-256 values.
`VerifiedExternalI02` requires exact `ExternalI02Roots`, checks the physical bytes,
the header schema/source/replay/release/universe, the closure/selector relations,
and the logical root. A locally rehashed physical file does not authenticate
against the held logical root. The evidence does **not** establish a competent
independent public issuer for those roots; it explicitly names that as an
external authority hold. That is honest and remains held.

## 2. G2 — Actual first consumer

Executed `build_sourcefree_direct_i02`, `VerifiedExternalI02`,
`install_direct_sourcefree_i02_i03`, and the actual native
`_select_respondent_events` / `execute_empirical_query` path.

- The direct certificate's event/selector refs equal the native I03 selector
  output for native, canonical and component targets, all tested state filters,
  multiple occurrences and order.
- The installed native index uses `_DiskSelectedRespondent` for every respondent;
  the selector postings come from the direct certificate while semantic bodies
  are resolved exactly from the already-sealed repository release. Closing the
  certificate after installation refuses typed; the reader does not silently
  fall back to the native release index.
- Full native empirical query, independently reproduced:
  - original: `raw_numerator_support = 2`;
  - changed sourcefree response: `raw_numerator_support = 3` and changed result;
  - exact restoration: `raw_numerator_support = 2` and the original result.
  - `evidence/04_FULL_NATIVE_CHANGED_RESTORED.log`.
- A direct certificate whose reconstructed historical release identity differs
  from the sealed release is refused by the direct installer.

This is the correct S2-B scope: direct I02 logical/selector certification plus
compatible native selector admission. It is not S2-C cold physical body
realization; the sealed body release supplies the bodies.

## 3. G3 — Adversarial falsification

### 3.1 The six previous causal repairs reproduced on the frozen cut

Frozen cut `edd0611` probes, independently executed:

| Repair | Frozen observation | Repaired observation |
| --- | --- | --- |
| D1 duplicate manifest declaration | duplicate universe and duplicate authority declarations **ACCEPTED** | typed `ExternalI02IntegrityError` refusal |
| D2 legacy-valid manifest without `ReplayManifest` count | refused | accepted with historical identity parity |
| D3 malformed SQLite certificate | raw `sqlite3.OperationalError` | typed refusal for the tested missing-table case |
| D4 atomic publication `OSError` | raw `OSError` | typed refusal, no destination created |
| D5 wrong authority exception type | raw `C11IntegrityError` | typed `ExternalI02IntegrityError` |
| D6 direct native I03 installer | `ImportError` (no path) | direct installer path and native parity |

Evidence: `evidence/02_FROZEN_SIX_REPAIR_RED.log`,
`evidence/01_TARGETED_SIX_REPAIR_TESTS.log`.

### 3.2 Existing hostile suite remains green

The 129-test court includes refusal for omissions, forged selectors, locally
rehashed physical files, wrong roots, duplicate occurrences, duplicate
declarations, unlawful typed absences, malformed tables, publication failures,
closed readers, swapped SQL sessions, root personas, and stale/missing postings.
Exact valid restoration is asserted in the changed/restored cases.

### 3.3 Exact defect G5-R1 — malformed header leaks an untyped first-reader failure

**Reproducible contract violation.** This is the same threat model as the
accepted D3 test: the attacker modifies the certificate bytes and recomputes
only the physical root; the externally held logical root is unchanged. The cold
verifier must refuse with `ExternalI02IntegrityError`.

At `rawlsing_next/_pre553_external_i02_certificate.py:535-546` the cold verifier
reads `main.header` and executes:

```python
if set(__import__("json").loads(h["coverage"])) != set(M01_M18):
    _fail("M01-M18 missing in certified header")
```

The D3 wrapper catches only `sqlite3.Error` (lines 547-551). If `coverage` is
missing, invalid JSON, `null`, or a number, the verifier raises `KeyError`,
`json.JSONDecodeError`, or `TypeError` before the logical/closure checks. The
outer `except Exception` closes the database and re-raises the raw error.

Independent output (`attacks/attack_malformed_header.py`,
`evidence/05_MALFORMED_HEADER_UNTYPED.log`):

```text
invalid-json UNTYPED_REFUSAL JSONDecodeError Expecting property name enclosed in double quotes
missing-key  UNTYPED_REFUSAL KeyError 'coverage'
json-null    UNTYPED_REFUSAL TypeError 'NoneType' object is not iterable
json-number  UNTYPED_REFUSAL TypeError 'int' object is not iterable
```

This is an incomplete D3 repair: malformed tables are now typed, but malformed
header content is not. It violates the stated "typed refusal at the real first
reader" negative-enforcement contract.

**Required exact repair:** validate the entire untrusted header and certificate
structure in a typed boundary. At minimum, parse `coverage` with an explicit
JSON-object/type check and catch `KeyError`, `TypeError`, `ValueError`/
`JSONDecodeError`, and `Pre553IntegrityError` from the structural/logical
checks, raising `ExternalI02IntegrityError` (retaining the cause). Add a test
that deletes/overwrites `main.header.coverage` with invalid JSON, a missing key,
`null`, and a number, recomputes only the physical root, and requires
`ExternalI02IntegrityError`.

### 3.4 Residual hostile finding G5-R2 — direct installer trusts self-asserted history

This is **not** the primary verdict because it requires replacing the externally
held logical root, contrary to the documented `VerifiedExternalI02` caller
requirement. It is reported because the local return claims a changed direct
certificate is refused against the original sealed release, and the direct
installer has enough information to make that true.

Post-processing a genuine direct certificate to remove one real event plus its
selector, closure and occurrence rows, while preserving the historical header
and recomputing both roots, is accepted by `VerifiedExternalI02` and
`install_direct_sourcefree_i02_i03` against the exact sealed release. The native
selector then returns 1 event where the sealed release requires 2.
`install_direct_sourcefree_i02_i03` checks only the self-asserted reconstructed
header identities and the respondent census; it does not recompute the
historical candidate/replay/release hashes or compare event/selector postings to
the native release. Evidence: `attacks/attack_selector_omission_forged_root.py`,
`evidence/06_SELECTOR_OMISSION_FORGED_ROOT.log`.

Under the documented external-root trust model an honest external logical root
would reject this corruption. The recommended defense-in-depth repair is to
recompute the direct historical identities from the certificate rows, or compare
the certificate event/selector map to the sealed release's native index, before
installation. This does not change the primary G5-R1 verdict.

## 4. G4 — Actual tests and resource economics

### 4.1 Execution environment

Independent Linux VM: Lima 2.3.0, Ubuntu 26.10, kernel `7.3.0-9-generic`,
x86_64, 2 vCPU, 4 GiB RAM, Python 3.14.8, pytest 9.2.0, pyarrow 26.0.1,
pandas 3.1.1, pyreadstat 1.3.7, `/proc/self/fd` present. This matches the
reported Linux court except Python 3.14.8 vs 3.11.18.
`evidence/09_ENVIRONMENT.txt`.

### 4.2 Full court

Command:

```bash
cd <clean checkout at cc35e0a>
PYTHONPATH=. /usr/bin/time -v .venv/bin/python -m pytest -q \
  -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_external_i02_certificate.py \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py \
  rawlsing_next/tests/test_pre553_verified_semantic_range.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_c11_repository_ingest.py
```

Result: **129 passed in 79.88 s**, exit 0, process max RSS **179,080 KiB**.
Per-file: external 29, direct 26, verified range 26, empirical query 32,
repository ingest 16. `evidence/00_FULL_COURT_129.log`.

The committed local return reports 129 passed in 24.71 s and 143,560 KiB on
Python 3.11.18; the difference is environmental, not a test result conflict.
The Actions run was never executed; the return already says so.

### 4.3 Scale

Independent reruns of the committed one-shot probe:

| Case | Retained SQLite | Build | Cold + select | Python peak | Process max RSS | Sampled workdir+TMP |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 20,000 events / 1 respondent | 126,853,120 B | 86.689 s | 3.085 s | 2,260,709 B | 42,136 KiB | 147,688,854 B |
| 100,000 events / 1 respondent | 638,414,848 B | 307.597 s | 15.883 s | 2,260,594 B | 42,184 KiB | 685,623,193 B |

The 100,000-event run selected 100,000 postings from **one** respondent. It did
**not** run 100,000 respondents, an integrated 6 GiB C11+native+saved pipeline,
an independently aggregated process-tree RSS, a separately instrumented SQLite
scratch peak (the sampler reported 0 scratch bytes), or a live S1-B/E decoder
stream. Those remain named G4 gaps and are not invented as passed here.

The measured S2-B sourcefree requirement is: no legacy release/closure object
graph in the direct builder; constant ~2.26 MB Python builder peak from 2k to
100k events; SQLite disk sorting and retention; ~42 MB process RSS for the
100k-event one-respondent probe; 638 MB retained certificate at 100k events.
This is adequate evidence for the scoped sourcefree logical/selector certificate,
not for a production 100k-respondent or 6 GiB acceptance.

### 4.4 Attribution of the 129-test evidence

The committed `01_G1_G5_RECEIPT.json` reports 129/129 and its SHA256SUMS verify.
The 100k/20k logs are author-run but were independently reproduced here with
matching retained bytes and the same one-respondent cardinality. The direct
native 2→3→2 result and the six frozen repairs were reproduced independently.

## 5. G5 — Terminal receiving

**Verdict: `REVISE_EXACT_DEFECT`.**

The direct sourcefree construction, historical identity reconstruction, native
selector admission, change/restore behavior, external-root model and measured
sourcefree economics are materially strong and preserve the declared S2-B scope.
The packet is not terminally acceptable because the D3 typed-refusal repair is
incomplete: a malformed certificate header still produces raw
`JSONDecodeError`/`KeyError`/`TypeError` at the cold first reader under the same
physical-rehash threat model as the accepted D3 test.

This is a narrow, reproducible first-reader contract violation, not an
architecture redesign. Required repair: typed header/structure parsing and a
regression test for invalid/missing/non-object `coverage`. The residual
self-asserted-root selector-omission finding (G5-R2) is a recommended
defense-in-depth check against the direct installer's sealed-release claim; it
does not replace the primary G5-R1 defect.

No additional author duel or architecture redesign is requested beyond the exact
typed-refusal repair and its test.

## 6. Outstanding original-source/authority holds

- original35 source equivalence: **HELD**
- CURRENT permission: **NOT ISSUED**
- P01–P20 / T01–T18: **HELD**
- S2-A receiving: **PENDING**
- S2-C cold physical body estate: **NOT BUILT** (separate packet)
- W03/W04: **PAUSED**
- protected merge: **NONE**
- native production permissions: **NONE**
- competent external direct-certificate root issuer: **NOT ESTABLISHED**

## 7. Reproduction commands

```bash
# Full court
cd <checkout at cc35e0a>
PYTHONPATH=. .venv/bin/python -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_external_i02_certificate.py \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py \
  rawlsing_next/tests/test_pre553_verified_semantic_range.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_c11_repository_ingest.py

# Six repair-focused tests
PYTHONPATH=. .venv/bin/python -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py::test_s2b_a5_direct_duplicate_manifest_declarations_refused \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py::test_s2b_a5_direct_legacy_valid_manifest_without_replay_count \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py::test_s2b_a5_direct_cold_verifier_typed_refusal_on_missing_direct_tables \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py::test_s2b_a5_direct_publication_oserror_typed_no_clobber \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py::test_s2b_a5_direct_wrong_authority_is_typed_refusal \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py::test_s2b_a5_direct_historical_identity_installs_native_i03_selectors \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py::test_s2b_a5_direct_changed_restored_native_i03_eligible_output \
  rawlsing_next/tests/test_pre553_external_i02_certificate.py::test_s2b_a5_direct_sourcefree_drives_full_native_i03_query

# Primary exact defect
PYTHONPATH=. .venv/bin/python \
  WORKER_RETURNS/PYAT_PAIR2_S2B_INDEPENDENT_G5_R1/attacks/attack_malformed_header.py

# Residual forged-root finding
PYTHONPATH=. .venv/bin/python \
  WORKER_RETURNS/PYAT_PAIR2_S2B_INDEPENDENT_G5_R1/attacks/attack_selector_omission_forged_root.py
```

## 8. Evidence index

All under `WORKER_RETURNS/PYAT_PAIR2_S2B_INDEPENDENT_G5_R1/`:

- `01_G5_RECEIPT.json` — machine receipt
- `evidence/00_FULL_COURT_129.log` — independent 129-test run
- `evidence/01_TARGETED_SIX_REPAIR_TESTS.log` — targeted repaired tests
- `evidence/02_FROZEN_SIX_REPAIR_RED.log` — frozen-cut six-defect probes
- `evidence/03_PARITY_AND_ATTACK_PROBES.log` — parity/alias/optional/universe/native probes
- `evidence/04_FULL_NATIVE_CHANGED_RESTORED.log` — 2→3→2 native query
- `evidence/05_MALFORMED_HEADER_UNTYPED.log` — primary exact defect
- `evidence/06_SELECTOR_OMISSION_FORGED_ROOT.log` — residual forged-root finding
- `evidence/07_SCALE_20000.log`, `evidence/08_SCALE_100000.log` — independent scale
- `evidence/09_ENVIRONMENT.txt` — VM/tool environment
- `evidence/10_PRIOR_G5_SEARCH.txt` — prior-G5 ref search
- `evidence/11_ISSUE_NOTIFICATION.md` — issue/HQ/S2-C notification text
- `attacks/attack_malformed_header.py`, `attacks/attack_selector_omission_forged_root.py`
- `SHA256SUMS`
