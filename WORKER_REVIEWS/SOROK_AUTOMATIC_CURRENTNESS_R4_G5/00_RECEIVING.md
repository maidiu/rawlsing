# SOROK automatic currentness R4 — focused independent receiving

**Engineering:** `ACCEPT_SCOPED_SOURCEFREE`
**Scientific:** `HELD`
**Authority:** `HOLD_SOURCE_AUTHORITY`
**Full original claim:** `NOT_ESTABLISHED`
**Accept scoped:** `true`
**Accepted target:** `ACCEPT_SCOPED_SOURCEFREE@e3c2349dac018e8339b99abda87af68ebe1fb9b8`

**Reviewer:** `ses_e2186e745ffecK1Ilg4cw26pVu` (same distinct nonauthor)
**Author:** `ses_e21a481bfffefyvpxaeFaAOFvQ`
**Frozen corrected source:** `e3c2349dac018e8339b99abda87af68ebe1fb9b8`
**Final worker artifact/report:** `bf40e8ccf4f41235f17d4ab3a56787cb8537aa49`
**Runtime blob:** `1df8c98b87323f48cdfc6c5f6da4c82846bfa447`
**Test blob:** `e19e1241aa2e34d4a037f73cd9dca5222833f9d1`
**Focused R4 test blob:** `b3bb1fa938fe2adb716fcbfd85e6595d39f2502d`
**R3 RED:** `b83438438dcb82eec43d23f170cf5672269edf54` / evidence
`a49be6e8bf728262dad62753f3066e99351b7af9` (preserved)
**Review job:** `sorok-programma-automatic-currentness-r4-receiving-20261116-r1`
**Receipt bound path:** `WORKER_REVIEWS/SOROK_AUTOMATIC_CURRENTNESS_R4_G5/REVIEW_RECEIPT.json`

This is one focused R4 receiving after the launch-enrollment/session correction.
It is not a #1095 G5 rerun, not a review-of-review, and not a new author cycle.
Product and frozen #1095 code/source were read-only. All mutations were in
reviewer-owned sandbox pair/config/state under the R4 lease. The author live
pair/config was read only for custody. No author private key, identity file,
capability value, or registry secret was read, copied, or printed by this
reviewer. The 34-test run used a reviewer-generated sandbox key/identity, not
the live key.

## 1. Exact R3 bypass reproduced and closed

I copied the exact old R3 fake-launcher bytes (`sha256
c596188f68e4228e8a4a7bc7b5aa9072e42eb8df8690965d3431f837659f7252`) and ran
them against a frozen `0b2664a8` old-source worktree:

- Old source: `attest-launch` exit `0`, `TRUSTED_LAUNCH_ATTESTED`; the
  fabricated REVIEWER run was intaked with exit `0` — the R3 RED is reproduced.
- Corrected source, exact old fake: `attest-launch` exit `1`,
  `TRUSTED_LAUNCH_ACTUAL_SESSION_MISMATCH`; fake review exit `1`,
  `UNTRUSTED_CONTROLLER_RUN`.
- Corrected source, matching-session fake
  (`fake_attest_launch.matching_session.py`, sha256
  `7ede7468bd093f2ce570947cbe034e48bf52e5e75e4dfbb3f71b8ec396126b1b`):
  `attest-launch` exit `1`, `LAUNCHER_PROOF_REQUIRED`. Matching the expected
  session does not replace installed-launcher proof.

The actual installed patched launcher
`/Users/matthewsmith/.local/share/rawlsing-controller/local-automation/64d52127/launch.py`
has fixed SHA-256
`cfd180ac3bfc4ef60ea226d7a6975cc08ecb27600e68597a96f5719e9ca2c3b2` and
auto-attested a reviewer-owned sandbox qualification run (`exit 0`,
`TRUSTED_LAUNCHER_ATTESTATION`, correct launcher path/hash, live process tree).
The actual R4 review job is enrolled as `REVIEWER` for expected session this
reviewer and source `e3c2349d` in the live trusted-launch registry. The
reviewer public `attest-launch` route cannot mint without the fixed local
launcher proof.

## 2. Session, source and operator boundaries

The corrected runtime now binds:

- `job.session == binding.session == binding.expected_session` and the
  registry’s actual session;
- review `job.session == receipt.reviewer_session`, distinct from
  `receipt.author_session`;
- `receipt.implementation_commit == binding.expected_source_commit`;
- exact verdict equality, not prefix;
- high-risk operator enrollment/state maintenance to a signed operator
  authorization; unsigned enrollment fails;
- public material events, fake worker/reviewer runs and public live
  observations fail their trusted-route checks.

The R2 material probe returns **7 fixed / 0 gaps / PASS** on this source. The
un enrolled fake REVIEWER probe returns `UNTRUSTED_CONTROLLER_RUN`. The 34-test
suite (17 original + 11 R3 + 6 R4) passes with a reviewer-generated sandbox
trust root. The exact old fake witness, corrected exact fake, matching-session
fake and installed-launcher positive are preserved under `evidence/`.

## 3. Live source and external holds

Authenticated live GitHub refs/SHA and PR status were observed in a reviewer
sandbox: 16 refs, repo/PR reads `200`, issue reads `939/1008/1010 = 403`,
`REF_SHA_ONLY` coverage. The four current items remain visible:

- `GITHUB_STATUS_UPDATED_SOURCE_UNAVAILABLE issue:939`
- `GITHUB_STATUS_UPDATED_SOURCE_UNAVAILABLE issue:1008`
- `GITHUB_STATUS_UPDATED_SOURCE_UNAVAILABLE issue:1010`
- `GITHUB_PR_STATUS_ADVANCED pr:1095`

The issue/comment `403` remains a genuine source-authority/connector-scope HOLD,
not a code failure and not a claim of full issue/comment currentness. The real
PR #1095 status advance remains unreconciled by design. Required CI remains
`UNAVAILABLE_BILLING` / `PENDING_PROTECTED_CI_AND_ADOPTION`; local checks are
not reported as GitHub Actions PASS. The accepted scope is exact operational
currentness within the trusted local operator/controller boundary, with these
external data/CI holds.

## 4. Actual R4 lifecycle custody

The actual author R4 job completed (PID 93975) and the installed hook recorded
`REAL_MECHANISM_WORKER_RETURN_INTAKEN`. The author live pair generation 53 has
`mechanism_worker_return.execution_state = RETURNED_REVIEW_PENDING` with exact
`e3c2349d` source, runtime/test blobs and return SHA `2b5c8bdd…`, while the
mechanism review remains `PENDING_EXTERNAL_NONAUTHOR_REVIEW`. The actual R4
review job is prebound as `REVIEWER` to this session and source and is enrolled
in the live registry with `TRUSTED_LAUNCHER_ATTESTATION`. This is not a
fixture. The R3 `REVISE` remains historical, not acceptance of R4.

## 5. Historical and whole-claim boundaries

The state preserves 27 B01–G04 tasks, 21 G/M/T decision nodes, original
144/38/83/304/100 scope, seven protected P3/P4/P5/P6/MI/MII/MIII foundations,
B05 #1089 / C04 #1062 / C05 #1091 scoped pins, G03-I0 scoped accepted with full
G03 held, CG-A #1066 outside the 27 DAG, Browser #1008/#1010 terminal bounded
and #1012 not launched, #939 STOP/no dispatch, and B05/C04/C05 full-claim
decision blockers. No scoped → whole-original, sourcefree → native,
candidate → protected, merge → complete, or local-operator → science/human
authority inference is made. Protected CI/adoption, native science, actor
knowledge, human authority and full original currentness remain HELD.

## 6. Checks performed (macOS, existing Python; not Actions)

- 34 tests: **34 passed**, exit `0`, 5.79 s with reviewer `TMPDIR` and
  reviewer-generated sandbox launcher key/identity.
- Frozen #1095 verifier `--self-test --status`, plain, `--no-git --status`:
  exit `0` each.
- MCR py_compile and `--self-test`: exit `0` each.
- Canonical PROGRAMMA verifier: exit `0`.
- Pyat product visibility plain and `--self-test`: exit `0` each.
- Changed `WORKER_COMMISSIONS`: zero; selector not applicable.
- Exact old fake witness RED; corrected exact and matching-session GREEN
  refusals; installed launcher positive; R2 material `7/0`; fake reviewer
  refusal.
- Live sandbox startup/status/what-next exit `2` with the four source items;
  `what-next` returns B01 `RECEIVE` with owner/prerequisites; live observation
  time/digest persists across the follow-up status.
- Author R2 material/fake-review evidence and historical R1/R2/R3 reds retained.

## 7. Verdict and STOP

Engineering is **ACCEPT_SCOPED_SOURCEFREE** for the exact operational
currentness mechanism at the local trusted operator/controller boundary. The
public fake-launcher and actual-session bypass is closed; the installed
launcher proof and exact session/source/receipt binding are demonstrated; the
R2 material and 34-test evidence support the accepted scope. Scientific
authority remains HELD. Authority remains `HOLD_SOURCE_AUTHORITY` for the
unavailable issue/comment connector coverage; protected CI/adoption and native/
full authority remain external holds.

This acceptance is not a full-original, native, protected or production claim.
After the actual reviewer process exits, the installed hook must intake this
receipt and HQ must run a fresh-process startup/status for the final readback.
**STOP.**
