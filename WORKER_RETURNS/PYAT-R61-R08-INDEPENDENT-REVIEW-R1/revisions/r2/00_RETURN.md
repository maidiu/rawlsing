# R61-R08V R2 independent review — return

Verdict: **REVISE (bounded critical default-ingress defects).** R2 does repair the
prior named request-label attacks, the actual provider/evaluator/cold path, typed
condition/value/order refusal and the valid-product aggregate conflation. It does
not repair the public default trust boundary: a caller can construct an
`AdmittedEvidenceContext` that relabels the unchanged real producer with forged
source/edition/digest/design/clock/role/direction/permission labels and obtain
`SUPPORTED`, and the default self-sealed cache ingress accepts a forged
same-source evidence preimage and serves denominator 999 through the actual
consumer reader. Those are finite local defects at the callable grain, so the
callable is **not** ACCEPT_SCOPED_LOCAL. No maintained non-test caller exists at
this cut; full J42/P41/E04 adoption remains NOT_REACHED as an owner/integration
permission gap, not a local defect and not a claim of delivery.

## Exact custody

- Startup/candidate: `f419e9a4b16638cf2de7700da60ab2a7e71986d9`.
- Code commit: `abf77ee10691adccb1127abd78aec49c6623ea37`.
- Branch: `agent/opencode-pyat-r61-r08v-r2-independent-review-r1`.
- Module blob: `88e66ddd5de3c588e54470bf9aebcf2326d4f7d7`
  (`rawlsing_next/pre553_universal_evidence_binding.py`).
- Test blob: `5f05634ca49916eb7faf4ecf5a04895c11bd0dcc`
  (`rawlsing_next/tests/test_universal_evidence_binding.py`).
- Native owner blobs used unchanged: provider `23167aa25291fb148b1e3cf210ac33fe7769b783`,
  analytical composition `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`,
  positioned evaluator `62e5eced47b64512f47b004e3e13a6ef3fe21de7`,
  empirical objects `a61365b994e5c3c50de0f598fcf40e90abf757b6`,
  AT07 fixture `0e384f72fa615dc72a0dcb08a36472a64b7b1e4a`.
- Author R2 manifest hashes independently recomputed and matched 5/5:
  `00_RETURN.md` `c57408d0...`, `RESUME.md` `7d2b7031...`,
  `junit.xml` `741f4210...`, `proof_witness.json` `0b8a7c01...`,
  `reviewer_probes_replay.xml` `14e296e3...` (prefixes shown; full hashes in
  `proof_witness.json`).
- Allowed diff: between corrected R2 startup `7beffc6d86bcd5585a63ea2c1afa6262bc9ca208`
  and `f419e9a4b`, changed paths are exactly the two allowlisted code/test files
  plus `WORKER_RETURNS/PYAT-R61-R08-IMPLEMENTATION-R1/revisions/r2/`. Root v1
  author report bytes differ from `ad9c3088` because of the pre-R2 A0/A1
  supplement at `7beffc6d8`; the prior review tree at `1cc09784b` was not edited
  and the R2 window is clean. No candidate/native-owner/HQ file was modified by
  this reviewer.

## What R2 actually repairs (replayed)

- Prior hostile request labels changed against the original binding now refuse
  as `IDENTITY_MISMATCH`/`NO_EXACT_BINDING`; bool/int/null values, extra/reordered
  conditions, edition/digest/as-of/direction/role/design/weight/risk mutations
  all fail the same consumer assertion (retained hostile 8/8 now pass).
- Actual canonical provider and the unchanged
  `evaluate_positioned_subject_possibility` are still called; AT07 forward
  arithmetic is independently 54 yes / 6 no over denominator 60.
- Fresh-process cold replay of the full-K cache reproduces denominator 60 and the
  same consumer result hash; changed request clock/permission/edition does not
  hit the cache.
- `VALID_NULL`, `DIFFUSE`, `VALID_EMPTY` and `OBSERVED_ZERO` now reduce to
  distinct `*_PRODUCTIVE` states; `ZERO_SUPPORT`/`UNKNOWN` are not exact
  all-support; Z UNRESOLVED keeps denominator 16; an actual supported positive
  remains `EXACT_SUPPORT`.
- Author suite 26/26 and retained prior reviewer probes 19/19 replay green.

## Critical remaining defects

### D1-R2. Caller-owned `AdmittedEvidenceContext` relabels the real producer

The context is caller-constructed. `EmpiricalProducerBinding.__post_init__`
(`rawlsing_next/pre553_universal_evidence_binding.py:936-960`) checks only the
source-universe, release, risk-set, target and authority refs; the remaining
labels are only compared request-to-context, not to any owner object.
`mismatch_reason` (`:962-1010`) therefore accepts a request and context that
agree with each other on forged labels.

Observed: a context/request pair naming `FORGED_SOURCE`, `1999-01`, a forged byte
digest, instrument, units, estimand, weight, design, uncertainty, direction
`ANSWER_YES_TO_POSITION`, role `REVERSE_AUTHORIZED`, forged grammar/custody,
1999 clocks and a forged permission still resolved `SUPPORTED`, denominator 60,
provenance `CANONICAL_PRODUCER`, and `EvidenceConsumerReader.read()` accepted the
forged labels. The actual producer was the unchanged forward P1 producer.
Probe: `probes/test_r08v_r2_hostile.py::test_caller_owned_context_labels_cannot_relabel_real_producer`
(fails as expected on this candidate).

### D2-R2. Default self-sealed cache accepts forged same-source evidence and serves 999

`export_cache` (`:1624-1660`) includes evidence/query/rule material, but
`import_authenticated_cache` (`:1662-1842`) verifies only self-consistency and
replays the evaluator on the supplied evidence. It does not authenticate the
evidence preimage against the actual producer, and the evidence `raw_support` /
geometry are not tied to `evidence_ref` content. With an empty
`trusted_binding_hashes` and no issuer — the public default — a resealed entry
using the victim K and a forged same-source evidence preimage imports and serves
the forged denominator.

Observed: `import_accepted: true`, `result_state: SUPPORTED`, `denominator: 999`,
consumer read `denominator: 999`, trust grade
`FULL_K_PRODUCER_ASSOCIATION_SHA256`. Cross-source transposition is now rejected
(retained probe), but same-source semantic substitution with rehashed
denominator/cells is not. Probe:
`probes/test_r08v_r2_hostile.py::test_self_sealed_same_source_denominator_999_must_refuse`
(fails as expected on this candidate).

D3 from the prior review is repaired at this grain (status probe 2/2 passes).

## Reach and exact remaining boundary

- Covered: callable `EvidenceRequest@2` K -> binding -> actual provider/evaluator
  -> `EvidenceResult`/`SupportSummary`, exact-K cold replay, typed request
  refusal, valid-product status reduction, unchanged E04 fixed-semantics
  observation.
- NOT_REACHED: live J42/P41 progressive adoption and a repaired E04 terminal.
  `git grep -l pre553_universal_evidence_binding f419e9a4b -- '*.py'` finds only
  the module and its own test. Historical J42 (blob `40f1e9f6...`) records a
  synthetic evaluator trace without calling the evaluator; historical P41 (blob
  `7d42810...`) consumes trace entries by index with a
  `CACHED_PRODUCTION_CONSUMPTION` fallback; archived E04 (blob `2181b83...`)
  still returns top-level success for a `ZERO_SUPPORT` step. These are archived
  recovery targets outside the R08 allowlist, not live adopted production.
- Remaining full-progressive issue is a separately granted owner/integration
  amendment (adapter step, service per-step K/provenance, E04 terminal proof),
  not a local module import failure and not authority to edit archived returns.

## Commands and exits

```text
/usr/local/bin/python3 -m pytest -q rawlsing_next/tests/test_universal_evidence_binding.py rawlsing_next/tests/test_pre553_analytical_composition.py --junitxml=.../junit/author_replay.xml
exit 0; 26 passed, 0 failed/error/skipped, 7.016 s

PYTHONPATH="$PWD" /usr/local/bin/python3 -m pytest -q probes/test_r08v_baseline.py probes/test_r08v_hostile.py probes/test_r08v_e04_fixed_semantics.py probes/test_r08v_reach.py --junitxml=.../junit/retained_probes_replay.xml
exit 0; 19 passed, 0 failed/error/skipped, 5.126 s

PYTHONPATH="$PWD" /usr/local/bin/python3 -m pytest -q probes/test_r08v_r2_hostile.py --junitxml=.../junit/reviewer_r2_hostile.xml
exit 1; 1 passed, 2 failed (D1-R2, D2-R2), 0 error/skipped, 0.995 s

PYTHONPATH="$PWD" /usr/local/bin/python3 -m pytest -q probes/test_r08v_r2_status.py --junitxml=.../junit/reviewer_r2_status.xml
exit 0; 2 passed, 0 failed/error/skipped, 0.384 s
```

Retained fixtures require exact inherited C1 report JSON; they were materialized
read-only from the pinned HEAD blobs for replay and are not candidate edits.

## Process and limits

Reviewer model/account: `opencode-go/deepseek-v4.1-flash`, variant max, existing
user-selected Global account; harness PID 92739, attended, OS isolation not
proven. Distinct session/worktree from author `ses_e98c8dfe6ffewNYOqJpvqK21a6`;
same provider account is not institutional scientific independence. All evidence
is TEST_ONLY source-free; no original data, source/science/CI/production/N11/N12
or Sorok authority, no model/provider change, no extra session or subagent, no
author repair or self-adoption. Original35/1890/globalF6F7F8 and Z UNRESOLVED16
are unchanged. Final branch commit and direct-remote readback are reported after
push.
