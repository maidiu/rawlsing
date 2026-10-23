# R61-R08V R3 frozen expectations

Frozen before inspecting R3 candidate code or author R3 conclusions.
UTC freeze: 2026-10-23T14:10:00Z.
Reviewer branch: agent/opencode-pyat-r61-r08v-r3-independent-review-r1.
Startup/candidate: 84704f4a775d0419ad4a08c8c687bc815df47adc; code 3e5a53ce8905a361bce5a1ef9ddea05638b86f99.
Commission: 706e7857842cdd08a82e09f33937ade89778e86c:WORKER_COMMISSIONS/PYAT-R61-GENERIC-REPAIR-FLIGHT-R1/R08V/revisions/r3/00_COMMISSION.md.
R3 repair commission: ba6f6ce90612e033813ba779fb4d7cf0e098a8d3:WORKER_COMMISSIONS/PYAT-R61-GENERIC-REPAIR-FLIGHT-R1/R08/revisions/r3/00_REPAIR_COMMISSION.md.
Original R08: R08/00_COMMISSION.md and R08/NODE.json at the startup tree.
Prior R2 review: db356748251c01e237df3a360a532ed8ffe45ec6:WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r2/ (EXPECTATIONS, RETURN, defects, probes, outcomes, witness, JUnit).
Inputs read before freeze: R08V R3 commission, R08 original commission, INPUTS/CONTRACTS.md, INPUTS/USER_GRANT.json, R3 repair commission, prior R2 review and inherited probes/observations.
Role: distinct reviewer session, not author ses_e98c8dfe6ffewNYOqJpvqK21a6, not source/science issuer, not production/CI authority.
Model/account: opencode-go/deepseek-v4.1-flash, variant max, existing user-selected account. Same provider account is not institutional scientific independence.
Budget: 35 minutes, bank by 25; no model/provider/account change, no extra sessions or subagents.

## E1 Candidate custody and allowed diff

- HEAD at review start must equal 84704f4a775d0419ad4a08c8c687bc815df47adc and the named branch must be the reviewer branch.
- Code under qualification must equal 3e5a53ce8905a361bce5a1ef9ddea05638b86f99 for the two R08 allowlist files: rawlsing_next/pre553_universal_evidence_binding.py and rawlsing_next/tests/test_universal_evidence_binding.py.
- Diff 3e5a53ce..84704f4a must be confined to the author's own WORKER_RETURNS/PYAT-R61-R08-IMPLEMENTATION-R1/revisions/r3/ artifacts; the candidate commit must not change code.
- Diff f419e9a4 (prior code) ..3e5a53ce must be confined to the two allowlisted code/test paths plus author R3 report artifacts; no native-owner, evaluator, archived-return, HQ, workflow, config or lockfile edits.
- The author-claimed report hashes (00_RETURN.md, RESUME.md, junit.xml, manifest.json, proof_witness.json, and reviewer_probes_replay.xml if claimed) must be independently recomputed and match; manifest must explicitly exclude itself.
- Reviewer writes only WORKER_RETURNS/PYAT-R61-R08-INDEPENDENT-REVIEW-R1/revisions/r3/; .r61 stays untracked; candidate/native-owner/archived files remain immutable.
- Direct remote must resolve the reviewer branch to the exact pushed final SHA.

Falsifiers: wrong startup or branch, unreachable blob, dirty/out-of-allowlist candidate diff, self-inconsistent author manifest, unreproducible import/test.

## E2 Actual public issuance/admission boundary

- The R3 claim is a concrete TrustedOwnerAdmission/TrustedAdmissionAuthority implementation with default TEST_ONLY pinned authority and full-content evidence admission. Audit the actual minting/admission code, not only the 24 old probes.
- Test every intended public issuer/admission path: default constructor/factory, explicit key/pin path, any exported helper/factory, caller-created authority/root, caller-supplied key or source-visible deterministic/test default secret.
- A public helper, known source constant, caller-configured issuer, caller-authored root, caller-claim label, or caller-created authority that lets untrusted request/cache input mint an accepted admission is not external trusted issuance.
- A deterministic test default key is legitimate only if it is unusable as untrusted subject-facing issuance; protected-host trusted configuration may be accepted only when the public subject/cache API cannot supply/mutate it. Distinguish trusted host caller precondition from subject-facing evidence ingestion.
- Verify default authority pin/key provenance is trusted configuration outside untrusted request/cache material; source-visible derivation from caller data fails.
- Copied, relabeled, re-signed, or rehashed admissions must not transfer authority between distinct context/evidence/content identities.
- Private parent-memory/hostile-same-UID attacks remain excluded; ordinary public API and known source constants do not.

Falsifiers: untrusted input mints SUPPORTED/AUTHENTICATED admission through default/key/factory public path; caller-created authority accepted; known default secret usable by subject; authority copied/relabeled to another context; admission validates only mutual caller agreement.

## E3 D1 full-context binding

- All full-context identity/meaning/design/permission/clock fields must bind the real owner object or an independently admitted exact context/binding.
- Attempt old/new context relabel (source, dataset, wave, edition, digest, instrument, units, estimand, weight, design, uncertainty, direction, role, consumer use, grammar, custody, observation/reference/as-of/publication clocks, permission) with matching request labels.
- Missing/unresolved owner anchor must yield typed refusal/unresolved, never SUPPORTED; target/depth fallback is forbidden.
- Previously repaired typed condition/value/order checks and valid status behavior must remain intact.

Falsifiers: caller-built context plus matching request resolves SUPPORTED with forged labels against the unchanged real producer; missing determinant still resolves; relabeled admission accepted.

## E4 D2 default cache/evidence admission

- Default public cache ingress must authenticate the full actual evidence content, not merely verify a self-seal, a request-K preimage, or evaluator replay over supplied forged evidence.
- The evidence producer/content identity must be independently admitted (trusted binding/evidence hash or issuer) and the complete content digest verified; rebuild/check against the actual producer where available.
- Attempt same-source denominator/values forge with re-sign/rehash (including denominator 999), cross-source transposition, wrong-K association, stale/current/as-of/typed/order substitution, issuer substitution, and semantical relabeling through the intended public APIs.
- A cold process must replay the exact validated positive for the exact K and must refuse or legitimately change after material change; stale positives must not resurrect.
- If the default is intentionally association-only, it must not resolve as authenticated or serve subject-facing values; self-sealed candidate input must be typed refusal.

Falsifiers: default accepts self-sealed/re-signed same-source forged evidence; hash-only preimage; forged denominator/values reach EvidenceConsumerReader; stale positive after permission/clock/currentness/source change; CACHED label without validated exact-K replay.

## E5 Positive capability and actual evaluator

- A real owner-bound actual provider result plus the unchanged evaluate_positioned_subject_possibility must be invoked, returned object inspected, and values-read witnessed.
- Independently recompute the positive arithmetic from the source-free AT07 fixture and compare with consumer values.
- A legitimate independently frozen synthetic admission (external to the request/cache subject material) must still serve the exact same-consumer values.
- Meaningful same-consumer severance/mutation/refusal/restoration must change the assertion; all-refuse is not capability.
- Fresh-process authenticated-cache replay must reproduce the positive values.
- Eligibility/execution/result axes remain separate; SUPPORTED, VALID_NULL, DIFFUSE, VALID_EMPTY, OBSERVED_ZERO, ZERO_SUPPORT and UNKNOWN stay distinct; Z UNRESOLVED denominator16 and all-missing semantics unchanged.
- Full maintained J42/P41/E04 integration remains NOT_REACHED and is not claimed; exact prior reach evidence retained by identity, not re-archaeologized.

Falsifiers: output hash/marker only, no actual evaluator call/returned object, unrelated default E04 success substituted, severance leaves same productive assertion, valid products conflated, no positive control.

## E6 Independent replay

- Replay the focused author suite (claimed 28) and meaningful retained prior controls (the 19 prior reviewer probes where still applicable, plus inherited author baseline) with reviewer-owned JUnit, exact imports/blobs, commands, exits and skips.
- Replay prior R2 failures (D1 caller context relabel, D2 same-source 999 cache) against the R3 candidate.
- Add reviewer R3 probes for the actual issuance/admission boundary beyond the old probe names: default/key/factory, caller-created authority, known secret, copied/relabeled admission, full-content evidence forge/re-sign, legitimate external frozen admission, cold replay, severance/restoration.
- Include assertion-level mutation/restoration, not import crashes. Author claims are not qualification.

## E7 Verdict and reach

- ACCEPT_SCOPED_LOCAL only if E1-E6 hold at the exact justified callable grain.
- Otherwise REVISE with exact public reproductions and trust preconditions.
- If central admission still fails, state the missing function once and whether a bounded stronger-engineering decision is necessary; do not prescribe a fourth canary patch or broad court; do not downgrade the threat model for green.
- Do not conflate author-local test issuance with admitted issuer authentication or original authority.
- Original35/1890 and global F6/F7/F8 unchanged; J52/W52 stopped; no source/science/CI/prod/N11/N12/Sorok/actor authority; no self-adoption; no author repair.

Falsifiers: unreached path claimed delivered; archived J42/P41/E04 edited or treated as live; green obtained by threat-model downgrade or by vacuous refusal; verdict beyond finite evidence.
