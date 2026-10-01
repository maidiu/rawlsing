# PYAT N10E — P6 PROOF / EXECUTION PROVENANCE CORRECTION — R1 — RETURN

**Disposition:** `PASS_PROOF_AND_PROVENANCE_CORRECTED__NARROW_INDEPENDENT_REREVIEW_REQUIRED`

**Terminal:** `N10E_PROOF_PROVENANCE_CORRECTION_RETURNED__HQ_ADJUDICATION_REQUIRED`

Branch: `agent/deepseek-pyat-hq144-n10e-proof-provenance-correction-r1`
Commission tip: `a7f7eecdeaee58e4d8021b7c571b4956e6301464`
Independent review return corrected against: `b89268d1824409d20a91a37a0a3ff7751a7ae75a`
Review disposition addressed: `CHANGES_REQUIRED` (REV-N10E-001, -002, -003)

This is a **narrow proof/provenance correction**. It is not adoption, not a merge, and
not a re-litigation of the accepted review findings.

---

## 1. REV-N10E-001 — vacuous changed-source proof: REPAIRED

`test_p6_geometry_is_recomputed_not_fixed_when_the_empirical_slice_changes` previously
built `narrowed_rows` but re-ran the **unchanged** canonical case. It passed only
because the canonical denominator (60) happened to equal `len(narrowed_rows)` (60), so
it proved nothing about changed geometry — exactly as the review found.

The test now constructs a **second, genuinely different source-free empirical law**
through the same fixture procedure and runs the **real public provider** against it.

| Law | Rows | Forward denominator | Forward cells | Exact fractions |
|---|---|---|---|---|
| canonical AT07 | 100 | 60 | yes 54 / no 6 | 9/10, 1/10 |
| changed source law | 110 | **70** | yes 54 / **no 16** | **27/35, 8/35** |

The changed law appends 10 `POSITION=P1, ANSWER=no` respondents. Both target domains,
the risk-set construction and the conditioner grain stay identical; only the empirical
response law changes.

**Proof obligations met**

- The provider really consumes changed input: a second repository/release/query/
  predicate/witness/case is built from the changed rows and passed to
  `provide_empirical_possibility_slice`.
- Geometry follows the changed product: `raw_support == 70` and cells
  `{yes:54, no:16}`, differing from canonical and equal to the independently frozen
  changed oracle.
- It still flows through the accepted seam: the changed evidence **is** the
  composition's `possibility_slice_evidence_or_null`, the consumer result **is** the
  composition's `consumer_result_or_null`, and the receipt reports
  `generated_evidence_identity_is_producer_derived == True`.
- Nothing is fabricated to match: `changed evidence.raw_support == changed producer
  fact.raw_denominator_support == composition.raw_denominator_support`.
- **Control:** the changed law's reverse direction shares the unchanged 62 respondents,
  so its counts do **not** move (62; P1 54 / P2 8). This rules out "any second case
  returns something different".

**An authority subtlety the correction surfaced.** The canonical AT07 query authority
is *explicitly* scoped to exactly one universe ref, so the changed-source universe was
refused with `Pre553AuthorityError('exact authority scope does not include
source_universe_refs')` → typed `UNAVAILABLE / MISSING_REQUIRED_AUTHORITY`. The
provider did **not** coerce or bridge it. The fixture therefore builds a changed-source
query authority whose explicit scope names the changed universe — no implicit widening,
no `latest`/`default` fallback, canonical authority untouched.

**No provider change was required.** The provider implementation blob is
byte-identical before and after this correction:

```
23167aa25291fb148b1e3cf210ac33fe7769b783
```

so `COUNTEREXAMPLE_REQUIRES_PROVIDER_REOPEN` does **not** apply.

## 2. REV-N10E-002 — one final execution record: RECONCILED

Because the provider test file changed, the exact commissioned four-file court was run
**once** on the correction branch:

```
python -m pytest \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py \
  rawlsing_next/tests/test_pre553_empirical_possibility_provider.py -v

88 passed in 15.14s
```

| Court | Tests |
|---|---|
| `test_pre553_analytical_composition.py` | 13 |
| `test_pre553_empirical_query.py` | 32 |
| `test_source_backed_positioned_subject_possibility.py` | 13 |
| `test_pre553_empirical_possibility_provider.py` | 30 (1 corrected) |
| **Total** | **88 passed, 0 failed, 0 errors, 0 skipped** |

That command, count and duration are now the **only** final record and agree across
`00_RETURN.md`, `06_EXECUTION_RECEIPT.json` and `08_FINAL_PYTEST_OUTPUT.txt`. The
earlier durations (20.01s, 19.09s, 22.84s, 16.44s) are marked superseded rather than
deleted, and are not presented as final anywhere.

## 3. REV-N10E-003 — stale provenance language: REWRITTEN

The sentence claiming the commission tip was unobtainable has been removed from the
final limitations list and replaced by an explicit `historical_provenance_note`. It
preserves the full truth: early local unavailability (no origin credential), work
beginning from the declared accepted base, credentials later becoming available, the
branch being fetched and confirmed as the issued tip, the rebase onto it, and a lawful
final ancestry. It is context, not a standing blocker.

## 4. Accepted review findings preserved

Not reopened and not weakened: provider seam; no handwritten-evidence bypass; owner
blob preservation (`26f3380c…`, `62e5ece…` both re-verified byte-identical); forward
and reverse slice proof; P3 determinant closure; receipt identity well-foundedness; P5
fail-closed behavior; P7 replay; authority ceiling; and the absence of any AT33,
real-source, structural-world or actor/person claim.

## 5. Write allowlist conformance

Changed files (all inside the allowlist):

- `rawlsing_next/tests/test_pre553_empirical_possibility_provider.py`
- `rawlsing_next/tests/n10e_empirical_slice_fixture.py`
- `WORKER_RETURNS/PYAT-N10E-EMPIRICAL-SLICE-PROVIDER-R1/00_RETURN.md`
- `WORKER_RETURNS/PYAT-N10E-EMPIRICAL-SLICE-PROVIDER-R1/03_FIXTURE_AND_ORACLE_FREEZE.json`
- `WORKER_RETURNS/PYAT-N10E-EMPIRICAL-SLICE-PROVIDER-R1/05_HOSTILE_AND_REPLAY_AUDIT.json`
- `WORKER_RETURNS/PYAT-N10E-EMPIRICAL-SLICE-PROVIDER-R1/06_EXECUTION_RECEIPT.json`
- `WORKER_RETURNS/PYAT-N10E-EMPIRICAL-SLICE-PROVIDER-R1/07_FINAL_DISPOSITION.json`
- `WORKER_RETURNS/PYAT-N10E-EMPIRICAL-SLICE-PROVIDER-R1/08_FINAL_PYTEST_OUTPUT.txt`
- `WORKER_RETURNS/PYAT-N10E-PROOF-PROVENANCE-CORRECTION-R1/**` (this return)

Not modified: `rawlsing_next/pre553_empirical_possibility_provider.py`; the fresh-process
runner; both accepted owners; the independent review return directory; any C1-02
terrain; any HQ/control file.

## 6. Not claimed

- No AT33 / full progressive-world completion claim.
- No real-source qualification; the fixture remains synthetic and source-free.
- No structural-world, actor/person/V3, smoothing, or new proxy authority.
- No broadening of the provider.
- Not adoption: this is a branch-local correction requiring narrow independent re-review.

## 7. Next

Narrow independent re-review of the corrected P6 changed-source proof and the
reconciled single-run record, then HQ adjudication.
