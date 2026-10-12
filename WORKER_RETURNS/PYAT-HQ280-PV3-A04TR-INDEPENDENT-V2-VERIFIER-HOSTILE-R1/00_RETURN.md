# PYAT HQ280 PV3 A04TR — Independent V2 verifier hostile acceptance

**TERMINAL:** `HQ280_PV3_A04TR_INDEPENDENT_V2_VERIFIER_HOSTILE_RETURNED__NONISSUING__GITHUB_PUSHED`
**GRADES (kept separate):**
- `TECHNICAL` — **ACCEPTED (narrow), with one exact test defect**
- `INDEPENDENT_EXPECTATION_PROVENANCE` — **STRUCTURALLY SOUND / NOT EXTERNALLY SEALED**
- `REAL_CONSUMER` — **NOT ESTABLISHED**
- `SOURCE_ISSUER` — **NOT ESTABLISHED**

**Branch:** `agent/reviewer-pyat-hq280-pv3-a04tr-independent-v2-verifier-hostile-r1` @ `be553023c985c3e7f7a407c97773363b5440482c`
**Candidate A04T:** `c1df9842b7531146f1d8e215f216915b9039e4d7` — verifier module blob `996c8e907f2befde93af09b60154b610c1ffeb63`
**Authority:** HQD-2026-10-10-280 · canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f` · PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (unmutated). **Review only — no candidate/owner/canonical edits.**

## 1. Actual runtime — 43/44, and the 44th is exactly explained

`pytest rawlsing_next/tests/test_pre553_original_workload_v2_verifier_candidate.py -q` → **43 passed, 1 failed** (I did **not** accept 44 as sufficient, and I did not accept the green majority either).

The failing case is `test_accepted_owners_a04_a04s_a05_untouched`, which asserts:

```python
r = subprocess.run(["git","diff","--name-only",
                    "b68de0dd35a9885efcb46bcd8ec9cbe41dabf500","--","rawlsing_next/"])
assert r.stdout.strip() == ""
```

Its diff scope `rawlsing_next/` **necessarily contains the candidate's own two new files**, so the assertion **cannot pass on the branch as committed**. The actual output is:

```
rawlsing_next/pre553_original_workload_v2_verifier_candidate.py
rawlsing_next/tests/test_pre553_original_workload_v2_verifier_candidate.py
```

**These are A04T's own additions — nothing else.** Two consequences, and they point in opposite directions:

1. **The owners ARE untouched.** The diff names only the candidate's own files, so A04/A04S/A05 are exonerated *by the very output that fails the test*. I verified this on a clean branch state (`git checkout HEAD -- rawlsing_next/`), so it is not an artifact of my worktree.
2. **The assertion is defective**: a self-referential "accepted owners untouched" check whose scope includes the artefact under review. It must exclude the candidate's own paths (or use an explicit owner allow-list). **I report this as a candidate test defect, not as owner modification** — and I explicitly decline to spin the single failure into either a false defect or a false pass.

A04T's claim of "44 passed" is therefore **not reproducible on the committed branch**; the honest independent count is **43 passed / 1 failed**, with the failure fully accounted for.

**Runtime:** Python 3.11.3, macOS 13.7.8 x86_64, real Git worktree, actual subprocess execution (the 40 s runtime is the suite's real C11→Route B/I03/I05→Batch chain, not a mock).

## 2. The verifier design is genuinely the right shape (credited)

A04T does the thing my A04SR review demanded, and it does it correctly:

- it takes a **separately authored frozen expected payload containing raw fields only**;
- it **recomputes** every identity itself — `reconstruct_item_key`, `reconstruct_semantic_op_key`, `reconstruct_dispatch_op_key`, `reconstruct_expected_key`, `reconstruct_consumer_obligation_key`, `reconstruct_attempt_key`, `reconstruct_output_identity` — and treats **any divergence from independent recomputation as an error**;
- it **does not demand equality with legacy A05 keys** (exactly as the commission instructed), which is the correct response to my A04R `NOT_CLOSED` finding: rather than coerce A05 keys, it verifies in its own versioned V2 grammar;
- it carries the identities A05 could not: `SEMANTIC_OP_CLASSES`, `DISPATCH_CLASSES`, `MEASURE_KINDS = {RAW, GOVERNED_WEIGHTED}`, `EXPECTED_STATES = {RUNNABLE, HELD, DENIED, SOURCE_NONAPPLICABLE}`, `FORBIDDEN_NULL_SOURCES`, `NEVER_SUCCESS_CLASSES`.

**This closes the A04R/A04SR interoperability objection at the technical level**: the incompatibility is resolved by a **versioned native verifier** instead of a translation layer. That is the resolution I named as honest.

## 3. What is NOT established

**3a. Independent expectation provenance — `STRUCTURALLY SOUND / NOT EXTERNALLY SEALED.`** The verifier forbids *deriving* the expected set from produced output (it recomputes from raw fields and flags divergence). But **"reconstructed consistently afterward" and "established independently beforehand" are indistinguishable by recomputation alone** — a payload authored after the run, then re-expressed in raw fields, recomputes just as cleanly. Absent an **external custodian** holding the payload before execution, with an authenticated, candidate-unsettable time source, provenance remains **not proven**. This is the same hold I recorded in A04SR and WVF; recomputation does not close it.

**3b. Real consumer — `NOT ESTABLISHED.`** I did not observe an actual downstream C1/Field Forge/learned consumer executing on a produced product. Consumer obligations remain an **independent set** and cannot be satisfied by a receipt the same candidate fabricates.

**3c. Source issuer — `NOT ESTABLISHED.`** No competent external issuer is exercised.

## 4. Hostiles I could and could not execute — stated honestly

**Executed:** full candidate suite on a clean branch state; the exact failing assertion's real `git diff` output; source inspection of the reconstruction/refusal grammar (states, measure kinds, forbidden null sources, never-success classes, dispatch/semantic domains).

**NOT executed here, and recorded as UNKNOWN rather than PASS:** injected omissions/extras, conditional-order substitution, RAW/weighted collision, false nulls, job-identity collision, self-certified manifest and fabricated consumer receipt **through the real chain**. The suite's own hostile file claims 336 lines covering these, and the chain is real, but **I did not independently drive each mutation**, and I will not convert "the candidate tested it" into "I tested it". Closing this requires a re-run with my own mutated raw-field payloads — the minimal next act.

**Terminal:** `HQ280_PV3_A04TR_INDEPENDENT_V2_VERIFIER_HOSTILE_RETURNED__NONISSUING__GITHUB_PUSHED`.
