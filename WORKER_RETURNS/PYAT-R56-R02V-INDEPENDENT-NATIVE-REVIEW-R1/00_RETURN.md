# R56-R02V — INDEPENDENT NATIVE ACCEPTANCE REVIEW — RETURN

**Disposition:** `REVISE__SCOPED_ENGINEERING_DEFECT_REPRODUCED__NO_GATE_OR_SCIENCE_ACCEPTANCE`
**Commission:** `WORKER_COMMISSIONS/PYAT-R56-FIRST-REPAIR-FLIGHT-R1/R02V/00_COMMISSION.md` at director `485f31e52ca82905dcfbbc79c5f8c8294fb55f49`, blob `14dad45102ce84b48c649699503b39307f84d679`.
**Shared contract:** `REVIEW_SHARED_START_AND_RETURN.md` blob `83bb2e0a8e91e10b56f76209e5f07d2a7543bd36`.
**Candidate reviewed:** `236fd4d1064f7c14113616db300c955294a474ac` (author branch `agent/rabochii-pyat-r56-r02-occurrence-projection-repair-r1`).
**Reviewer branch:** `agent/rabochii-pyat-r56-r02v-independent-projection-review-r1`.
**Return root:** `WORKER_RETURNS/PYAT-R56-R02V-INDEPENDENT-NATIVE-REVIEW-R1/`.

## Session and startup

Fresh native OpenCode session `ses_e9dea5a24ffeBtsLScgC81lfet`, provider
`opencode-go`, model `deepseek-v4.1-flash`, variant `max`, host
`MacBook-Pro.lan` macOS 13.2.1 x86_64, Python 3.11.3. Exact provenance and
independence evidence: `01_SESSION_AND_STARTUP_PROVENANCE.md`. The reviewer
is distinct from the R02 author and from the R00P policy author. The assigned
branch did not pre-exist; the worktree was created from the exact candidate.

## What was actually exercised

The real path was exercised throughout:

```
pre553_source_native_preimage_adapter.materialize_native_preimages
  -> unchanged pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream
  -> unchanged Pre553 C11 validation
  -> unchanged pre553_empirical_query.execute_empirical_query (real I03)
```

No mock returned authored expected values. No production module was edited.
The adapter SHA-256 after the proof witness equals the candidate adapter:
`2cf5e98bc29081678c364d3ff591c71f11ce7ebf3564419af8a26f5f04113b64`.

## Reproduction counts

| Run | Result | Evidence |
|---|---|---|
| Author 15 focused tests (unchanged) | **15 passed** | `evidence/pytest_author15.log` / `.xml` |
| Retained facade + empirical-query suites | **42 passed** | `evidence/pytest_retained.log` / `.xml` |
| Independent positive/consumer tests | **7 passed** | `evidence/pytest_r02v_positive.log` / `.xml` |
| Independent defect reproducers | **2 failed as expected** | `evidence/pytest_defects.log` / `.xml` |
| Full focused file after reviewer additions | **22 passed, 2 failed** | `evidence/pytest_full.log` / `.xml` |
| Proof-integrity AST lint | **PASS** | `evidence/proof_lint.json` |
| Proof-integrity witness, 2 claims | **PASS, assertion-level RED** | `evidence/proof_witness.json` |

The 2 failures are not author-test regressions. They are the independent
reviewer's minimal reproducers for the defect below. The author's 15 tests are
unchanged and still pass.

## Defect D1 (decisive): normalized duplicate respondent key collapses two source respondents

`GovernedRowOccurrencePlan.__post_init__` checks duplicate respondent-key
values **before** the adapter's normalization. The adapter then builds
`{token(key): str(value)}` and assigns respondents without re-checking that
normalized mapping for duplicate values.

With a governed mapping `{0: "1", 1: 1}` and two source respondents (PID 0 and
PID 1 on disjoint occasions), both `str` values are `"1"`. The adapter accepts
the plan, emits one C11 respondent `R56R02:1`, and I03 returns `SUPPORTED`
with `raw_denominator_support = 1` for two source respondents.

Minimal reproducer:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 \
  WORKER_RETURNS/PYAT-R56-R02V-INDEPENDENT-NATIVE-REVIEW-R1/evidence/defect_normalized_respondent_key.py
```

Output (abridged; full output in `evidence/defect_normalized_respondent_key.out.json`):

```
expected_c11_respondents: 2
actual_c11_respondents: 1
actual_c11_respondent_keys: ["R56R02:1"]
event_tuples: [
  ["R56R02:1", 0, "SUBSTANTIVE_RESPONSE", "7"],
  ["R56R02:1", 1, "SUBSTANTIVE_RESPONSE", "9"]
]
i03_fact_state: SUPPORTED
i03_raw_denominator: 1
i03_raw_numerator: 1
row_evidence shows source_respondent "0" and "1" projecting to the same respondent ref
```

This is a false population fact and a direct violation of respondent
conservation. `test_r02v_normalized_duplicate_respondent_key_is_refused`
encodes the required refusal and currently fails with `DID NOT RAISE`.

**Owner:** R02 adapter author. **Required boundary:** normalize mapping keys and
values first, then require a bijection with unique normalized respondent keys
(and reject non-string/ambiguous mapping values), before C11 release
construction. Reviewer did not edit the adapter.

## Defect D2 (same root, less severe): normalized source-key collision is silently last-wins

With mapping `{0: "P0", "0": "P1", 1: "P2"}`, the adapter's token-key
comprehension drops the int key `0` in favor of the string key `"0"`; source
PID 0 is projected as `P1`, not `P0`. No refusal occurs. The mapping is
ambiguous at the normalized source-key level even though the raw Python keys
differ.

Minimal reproducer:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 \
  WORKER_RETURNS/PYAT-R56-R02V-INDEPENDENT-NATIVE-REVIEW-R1/evidence/defect_ambiguous_source_key.py
```

`test_r02v_ambiguous_normalized_source_key_is_refused` encodes the required
refusal and currently fails with `DID NOT RAISE`. The same normalization fix
should reject duplicate normalized source keys.

## Independent positive coverage beyond the author's one fixture

- 4 respondents x 3 occasions, interleaved physical row order, alternative
  occurrence labels (`alt-zero`/`alt-one`/`alt-two`), exact tuples and
  prospective I03 domain, `SUPPORTED` denominator 4, 12 events.
- 3 respondents x 2 occasions with one missing SCORE cell; exact
  `MISSING` tuple; I03 query including `MISSING` returns `SUPPORTED` with the
  exact typed-missing cell. A substantive-only query does not invent support.
- 4 respondents x 2 occasions with per-occasion different values; omission,
  occurrence-field remap, and value replacement each change/refuse the same
  frozen downstream query; a fresh restored subprocess reproduces the baseline
  fingerprint.
- S1 seven-row rectangular scalar path: 7 exact tuples, `SUPPORTED`
  denominator 7, cell counts 3/4.
- S2 person-unit and household-unit packages separately: each `SUPPORTED` at
  denominator 3 with distinct release refs; mixed-unit package refused
  `CROSS_UNIT_POOLING_UNAUTHORIZED`.
- MR1 `MULTISELECT` and RANK1 `ORDERED_SEQUENCE`: exact I03 consumption with
  `SUPPORTED` denominator 2; unadministered rule held and not projected.
- Envelope preservation/collision checks for the `source_missing_declaration`
  use (see adjudication).
- Incomplete order fields: no false support; I03 returns
  `INTEGRITY_FAILURE`/`UNRESOLVED`.

The exact per-run source, release, and fact identities for the 4x3 and 3x2
missing cases are in `evidence/r02v_independent_receipt.json`; example source
SHA values are `9b8acd92...` and `d2d82e07...` (full values in the receipt).

## Open-challenge adjudication summary

Full adjudication: `03_R02V_OPEN_CHALLENGE_ADJUDICATION.md`.

1. **Binding envelope:** bounded compatible use inside this exact
   adapter→facade→C11→I03 path; original declaration nested verbatim, raw
   value/state unchanged, occurrence keys collision-free in tested cases. It is
   **not** a general `PhysicalCell` substitute: strict receivers
   `fiabc_lits_i_representation_authority.authorized_banked_raw_value` and
   `fiabc_lm2_r1e_common_c11._cells` reject the wrapper. The exported
   `physical_stream` is transformed, not raw. R02 should name this boundary
   explicitly before reuse.
2. **Event-ID domain:** author's `domain_from_bundle()` is circular and
   mishandles missing values. Independent source-derived prospective domain
   added and exercised; it catches omission/remap/value faults. Candidate
   production behavior is correct for the tested cases.
3. **Administration/form:** correct supported-scope boundary; repeated scalar
   FORM refused as ambiguous; unadministered held; MR/rank consumed through
   I03.
4. **S2:** separate-unit positives were verified directly (not only refusal);
   no lawful household/person link claimed.
5. **Source stability:** per-process source bytes vary; exact per-run hashes
   are recorded and expectations are source-derived. Deterministic binary not
   required.
6. **Gate:** R00E not used; no gate-qualified integration claim.

## Engineering / science / authority

**Engineering:** core repeated adapter→C11→I03 conservation works for the
well-typed governed mapping and varied fixtures, but acceptance is blocked by
the normalized mapping-collision false fact (D1) and the silent ambiguous key
selection (D2). Disposition: **REVISE**, ordinary code defect, same R02 owner.
No external dependency; not HOLD.

**Science:** TEST_ONLY synthetic sourcefree only. No original SAV/DTA,
original respondent data, original35, E_pre, F1–F8, learned/world, actor,
N11, or N12 issuance. No scientific meaning is promoted from the synthetic
values.

**Authority:** The commission/R57 technical appointment and exact candidate
were verified. No production adoption, protected CI, R03/compiler/lowering,
R04.byte/R04.joined, R05/R06, original-source, or N11/N12 claim is made. J52/
W52 remain USER_STOPPED. R03/compiler/original science holds are unchanged.

## Next action

Return D1/D2 to the same R02 implementer. After repair, rerun the two defect
tests (they must pass), the 7 independent positives, the 15 author tests, the
42 retained tests, and the proof-integrity witness. The reviewer has completed
this finite pass; no second broad review is requested.
