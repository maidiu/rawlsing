# R61-R08V R3 independent review — return

Verdict: **REVISE (critical public issuance/admission defect).** R3 adds the
named `TrustedOwnerAdmission`/`TrustedAdmissionAuthority` objects and closes the
two *exact* R2 probes: a caller context with no admission now refuses, and a
self-sealed cache entry with no admission now refuses. Positive actual-provider,
unchanged-evaluator and cold-cache replay remain live (author 28/28, retained
R1/R2 probes 24/24, reviewer positive control passes).

The actual public trust boundary does not hold. The default is an accepting
authority whose HMAC key is a source-visible constant, and its public
`issue_producer`/`issue_evidence` factories are usable by any caller. A caller
can therefore mint an admission for a forged full context (source/edition/
digest/design/direction/role/clock/permission) and obtain `SUPPORTED` from the
unchanged real producer; independently, a caller can re-sign forged same-source
evidence (denominator 999) with the same default key and the default cache
import serves it through the actual consumer reader. This is the concrete
implementation delta the commission ordered tested beyond the 24 old probes, and
it fails at the callable grain. Full J42/P41/E04 integration remains NOT_REACHED
as before (unchanged owner/allowlist boundary, no archived file edited).

## Exact custody

- Startup/candidate: `84704f4a775d0419ad4a08c8c687bc815df47adc`.
- R3 code commit: `3e5a53ce8905a361bce5a1ef9ddea05638b86f99`.
- Branch reviewed: `agent/opencode-pyat-r61-r08-evidence-binding-r1`; reviewer
  branch `agent/opencode-pyat-r61-r08v-r3-independent-review-r1`.
- Module blob: `759c5978a6ad876e2d013f3d98c06c6ccb8dd270`
  (`rawlsing_next/pre553_universal_evidence_binding.py`).
- Test blob: `db85977af03842cb3946e5cca6f74049516d4a69`
  (`rawlsing_next/tests/test_universal_evidence_binding.py`).
- Candidate diff `3e5a53ce..84704f4a` is exactly the author's six
  `WORKER_RETURNS/PYAT-R61-R08-IMPLEMENTATION-R1/revisions/r3/` report files; no
  code changed after the code commit.
- Code diff `f419e9a4..3e5a53ce` is exactly the two allowlisted code/test paths.
- Author manifest hashes independently recomputed and matched 5/5:
  `00_RETURN.md` `459d0fb2...`, `RESUME.md` `c1be631c...`, `junit.xml`
  `0534623f...`, `proof_witness.json` `6ddaa109...`,
  `reviewer_probes_replay.xml` `bb8494c1...` (full hashes in
  `proof_witness.json`). Manifest self-exclusion is explicit.
- Native owners used unchanged: provider `23167aa2...`, composition `604c8d59...`,
  positioned evaluator `62e5eced...`, empirical objects `a61365b9...`, AT07
  fixture `0e384f72...`.
- Reviewer wrote only `WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r3/`;
  `.r61/` stayed untracked; no candidate/native-owner/archived/HQ file edited.

## What R3 actually repairs (replayed)

- Prior R2 D1 probe (`caller-owned context` with **no** admission) now returns
  `UNKNOWN` / `OWNER_ADMISSION_UNRESOLVED`; consumer read raises
  `EvidenceAssociationError`.
- Prior R2 D2 probe (self-sealed same-source evidence with **no** admissions) now
  raises `EvidenceCacheIntegrityError` before import.
- Legitimate canonical admission + actual AT07 provider/evaluator gives
  yes=54/no=6/denominator=60; fresh-process imported cache reproduces 60 and the
  same consumer result hash (reviewer positive control passes; author suite
  28/28).
- Retained prior R1/R2 controls replay 24/24 green, including typed condition/
  value/order, status axes, observed zero, Z UNRESOLVED16, E04 fixed semantics
  and reach observations.

## Critical remaining defects

### D1-R3. Default public authority mints forged-context admissions

`R61_TEST_ONLY_OWNER_ADMISSION_KEY` is a source-visible constant
(`pre553_universal_evidence_binding.py:1345`), the module exports a live default
`R61_TEST_ONLY_OWNER_ADMISSION_AUTHORITY` (`:1532`), and `EvidenceResolver()`
uses it whenever no authority is passed (`:1578-1584`). `bind` accepts a
producer admission verified by that same public authority (`:1601-1607`).

A caller builds a forged `AdmittedEvidenceContext` and matching request
(`FORGED_SOURCE`, dataset/wave, edition `1999-01`, forged byte digest,
instrument, units, estimand, weight, design, uncertainty, direction
`ANSWER_YES_TO_POSITION`, role `REVERSE_AUTHORIZED`, consumer use, grammar,
custody, 1999 clocks, forged permission), then calls the public
`R61_TEST_ONLY_OWNER_ADMISSION_AUTHORITY.issue_producer(context_ref=forged_ref,
owner_identity_material=binding.owner_identity_material())`. The unchanged real
forward P1 producer resolves `SUPPORTED`, denominator 60, provenance
`CANONICAL_PRODUCER`; `EvidenceConsumerReader` reads denominator 60. Observed:
`outcomes/r3_observations.json` key `forged_context_public_mint`; probe
`probes/test_r08v_r3_issuance_boundary.py::test_default_public_authority_must_not_admit_forged_caller_context`.

Why: the author test signs an admission over the *canonical* context while
binding a forged context, so it tests a mismatched pair, not the public minting
path. Because the default key is in source and `issue_producer` is public, the
caller can sign exactly the forged pair. Matching caller issuer/claim is not
external trust; the default path is subject-facing.

### D2-R3. Default ingress accepts evidence re-signed with the public default key

Cache import verifies producer/evidence admissions with the same default public
authority (`:1978-2080`). A caller takes a legitimate exported producer
admission, builds forged same-source evidence (`raw_support=999`, yes=999,
no=0), and calls public
`R61_TEST_ONLY_OWNER_ADMISSION_AUTHORITY.issue_evidence(producer_admission=...,
evidence=forged)`. The evidence admission binds `evidence_ref` plus the
SHA256 of the forged complete evidence material, so the content digest check
passes. Default `EvidenceResolver().import_authenticated_cache(...)` accepts;
`resolve` returns `SUPPORTED`, denominator 999, provenance `AUTHENTICATED_CACHE`;
`EvidenceConsumerReader.read()` serves denominator 999 with
`admission_grade=TRUSTED_OWNER_EVIDENCE_ADMISSION_HMAC_SHA256`. Observed:
`outcomes/r3_observations.json` key `forged_evidence_public_resign`; probe
`probes/test_r08v_r3_issuance_boundary.py::test_default_ingress_must_reject_evidence_resigned_with_public_default_key`.

Secondary hardening: `issue_evidence` (`:1464-1490`) checks only
`producer_admission.authority_id`, not the producer token/owner binding, so an
evidence factory accepts a copied/forged producer admission before the later
verify step. This is dominated by the public-key defect but should not be
presented as independent issuance.

## Missing function and bounded decision

The missing function is **external trusted issuance of admissions**: a key/pin
(or attestation) that is trusted configuration outside the process/subject and
is not derivable from source or caller material. Repackaging the same
source-visible key as `TEST_ONLY` does not supply it, and a resolver option for
a caller-supplied `TrustedAdmissionAuthority` is host configuration, not
issuance for the default subject-facing path. This requires one bounded
stronger-engineering decision: either (a) make the default resolver accept no
admission authority and fail closed/typed-UNKNOWN unless a host injects an
externally pinned authority with a non-source-visible key, or (b) require an
external issuer attestation the request/cache subject cannot mint. Do not add a
fourth canary patch or another probe-name-specific branch, and do not downgrade
the threat model for green.

## Positive capability and status controls

The positive path is real and is not being denied: canonical admitted context ->
actual provider -> unchanged `evaluate_positioned_subject_possibility` ->
values-read, independently 54 yes / 6 no / denominator 60; cold replay of a
legitimate exported cache reproduces 60 and the consumer hash. Reviewer
`test_legitimate_canonical_admission_and_cold_replay_remain_positive` passes.
VALID_NULL/DIFFUSE/VALID_EMPTY/OBSERVED_ZERO, ZERO_SUPPORT, UNKNOWN and
Z UNRESOLVED16 remain distinct in the replayed retained controls.

## Reach

- Covered at the assigned callable grain: full-K evidence binding, actual
  provider/evaluator/consumer values-read, authenticated-cache positive replay,
  typed request/condition/order refusal, status reduction.
- NOT_REACHED (unchanged, by identity; not re-archaeologized): live J42
  `E41ProviderAdapter.step` adoption, live P41 progressive adoption, repaired
  live E04 terminal success assertion. Prior reach evidence remains at
  `db3567482` / `1cc09784b` and the historical blobs named there; no archived
  return was edited and no full-progressive PASS is claimed.
- No original source/science/CI/production/N11/N12/F6/F7/F8/actor/Sorok or
  J52/W52 authority; original35/1890 and Z UNRESOLVED16 unchanged.

## Commands and exits

```text
/usr/local/bin/python3 -m pytest -q rawlsing_next/tests/test_universal_evidence_binding.py rawlsing_next/tests/test_pre553_analytical_composition.py --junitxml=.../junit/author_replay.xml
exit 0; 28 passed, 0 failed/error/skipped, 6.97 s

PYTHONPATH="$PWD:$PWD/.r61/r3" /usr/local/bin/python3 -m pytest -q -p r61_fixture_paths <prior R1/R2 probes> --junitxml=.../junit/retained_probes_replay.xml
exit 0; 24 passed, 0 failed/error/skipped, 6.05 s

PYTHONPATH="$PWD" /usr/local/bin/python3 -m pytest -q .../probes/test_r08v_r3_issuance_boundary.py --junitxml=.../junit/reviewer_r3_issuance.xml
exit 1; 2 failed (D1-R3, D2-R3), 2 passed (positive cold control, old missing-admission refusal), 0 error/skipped, 1.85 s
```

Inherited C1 fixture JSON was materialized read-only from the pinned candidate
blobs for replay only; it is not a candidate edit and is not committed.

## Process and limits

Reviewer model/account: `opencode-go/deepseek-v4.1-flash`, variant max, existing
user-selected account. Distinct reviewer session/worktree from author
`ses_e98c8dfe6ffewNYOqJpvqK21a6`; same provider account is not institutional
scientific independence. All evidence is TEST_ONLY source-free. No model/
provider/account change, no extra session/subagent, no author repair, no
self-adoption. No original data, source/science issuance, production/CI,
N11/N12, F6/F7/F8, actor, Sorok or J52/W52 authority. Final branch commit and
direct-remote readback are reported after push.
