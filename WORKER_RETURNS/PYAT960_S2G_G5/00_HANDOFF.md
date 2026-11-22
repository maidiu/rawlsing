# PYAT960-S2G — G5 INDEPENDENT NONAUTHOR RECEIVING / REVISE

## 1. Exact artifact and commission

- Packet / old obligation: **S2-G / P2-08** (original #919, successor #960)
- Contract SHA256: `635a423beea158a67653d8c03ea7aee9c158f21986d4d598018d0976db73552b`
- Contract source cut: `WORKER_COMMISSIONS/PYAT_SUCCESSOR_960/contracts/S2-G_v1.md@63836a168cc99b0ed8f87f7f7a6e76192f7a1898`
- Frozen base: `6a5c12f04323d74001f9632063ec907f4fc4468e`
- Startup / PR948 stage: `7064daa14d93109211629e72d08f3a6e705a0d57`
- A prior implementation: `fc820533a2a90b948a9e8e80b4f220005e701d4b`
- B delivery / code cut: `220ebd3311fb0607079ed6a6e9a364d6681e5378` / `0071aefb05d8ebbd75058a10c5e831d994a2f96f`
- A counter code/test cut: `a3d1e33ecad37cd964f3caded37c2fec9360330e`
- Delivery: `6f3a10552e074c3f1fd54c861290c8300c99dbb2`
- Branch / worktree: `agent/pyat960-s2g-g5-r1` / `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat960-s2g-g5`
- Reviewer session: `ses_e30c25800ffeT8XbyTuHekRCme`
- Model: `opencode-go/deepseek-v4.1-flash#max`
- Write allowlist: `WORKER_RETURNS/PYAT960_S2G_G5/` only. No implementation/test/native-owner/earlier-return/controller/other-worktree writes; no reviewer patch.

**Exact diff verified.** `6f3a105..a3d1e33` changes only the A-counter return files; code/test tree is identical. `0071aefb..a3d1e33` changes only `pre553_durable_learned_lifecycle.py` (+43) and new `test_pyat960_s2g_a_counter_subset.py` (+105). No existing M1/M2/B5/world/S2-F/I02/Parquet/query/discovery/FF/C11 owner changed. Adapter Git blob SHA1 at the tested cut: `0d7860271914fb301beb4a4f914cd1c483ba9ad0`.

## 2. Independent reconstruction and review scope

I verified the contract source cut/blob hash and read the original S2-G text, successor #960, R3C/R3S, the A/B/A-counter handoffs and receipts, and the actual adapter/tests in this worktree. The native owner files were read-only and exercised as-is.

The base positive chain is genuine: synthetic native M01 graph → actual M1 adjudication with TEST_ONLY native validator fixture → actual M2 `constitute_release`/closures → actual B5 registration/publication/current selection → actual `evaluate_learned_world_consumer`. The cold path re-runs the actual C1/N10E discovery composition from the accepted isolated S2-F closure.

## 3. Closed decision

**`REVISE_EXACT_DEFECT` at `S2_SOURCEFREE_ISOLATED_FIXTURE`.**

- G1 **FAIL**: the exact source/release contract is not complete at the selected-fact boundary.
- G2 **PASS** for the normal native fact → M1 → M2 → B5 → existing world consumer, changed input and exact restoration.
- G3 **FAIL**: a wrong-source multi-release positive is accepted by the actual first consumer.
- G4 **PASS** at fixture grade for CAS/fsync/crash/recovery/resource/source-open.
- G5 **FAIL**: independent receiving cannot ACCEPT_SCOPED while a reproduced G1/G3 source-release failure remains.
- Integration **UNMERGED**.
- Full original S2-G remains **OPEN / HOLD_EXTERNAL** on accepted S2-E/S2-D, production current/as-of issuer, scientific M1 rule and integrated 100k. No original-task completion tick, protected merge, scientific claim, or production authority.

## 4. What passed independently

### 4.1 Base positive and durable cold path

- Base artifact root `852498f72ed7c1940d55caae0a75bab6869aa854bb83f7a39451debc57be2fe5`
- M1 `9a7f5e31226f4707c2aba6304dd791da1c4d78a5aa3a1661545c22085b8a3fdd`
- M2 `3423ef93f9c6a4de45574ed89b47554b3062b7b0c97d2b373ad907a4f19747b9`
- B5 selection `2dd500392ea3b05ef0903fe4a46977f74627d86bbe0a802f2e663e085c98ef14`
- Consumer `LEARNED_CONSUMER_EXACT_SUPPORTED`, hash `2690cdbeadabb0e90179d726029fa8b765995a15a1da26d7fe72bba0819bd597`
- Fresh child: exact, `source_opens=[]`, `matches_expected=true`, child RSS 41,525,248 B, cold 0.234 s.

### 4.2 Change/restore and refusals

- B01 real native physical-cell change changes S2-F/M1/M2/B5/artifact/consumer and exact restore returns root `852498f7...` and consumer `2690cdbe...`.
- B-D1 cross-chain M1 evidence refuses at cold consume.
- B-D2 unpinned/foreign as-of checkpoint refuses; own pinned checkpoint and retained prefix history pass.
- B-D3 tampered replay/learned-receipt/protocol/M2 provenance refuses under a new self-hash pin.
- A-C01 receipt-fact omission refuses at current code; preserved B-cut RED evidence shows B `0071aefb` accepted the mutant.
- Self-rehashed fake checkpoint, wrong as-of, missing rule/receipt/history/changed M2 dependency, current/as-of/supersession/no-current and crash-before-manifest cases pass their existing focused tests.

### 4.3 Regression and resources

- 153 selected owner/M1/M2/B5/world/S2-G/B/A-counter tests: **153 passed in 51.62 s**.
- 19 S2-F regressions: **19 passed in 9.47 s**.
- 19 focused S2-G/B/A-counter tests: **19 passed in 31.58 s**.
- Independent base resources: retained 32,499 B (31,987 compressed + 512 manifest), logical 283,854 B, peak scratch 31,987 B, parent cold/repeat 0.0692/0.0694 s, parent RSS 112,869,376 B, child RSS 41,525,248 B, source opens 0, cap PASS at fixture grade, integrated 100k NOT_RUN.
- One compressed artifact blob + manifest; no duplicate complete archive.

## 5. Material defect — G5-MR01, multi-release source ownership

**Severity: SEV-0** (incorrect positive source/release claim; at minimum SEV-1 actual first-reader wrong source).

The S2-G adapter checks that the consumer's determinant release appears in:

- the S2-F receipt's declared `source_release_refs` subset;
- the declared S2-F closure release registry;
- the M1 input bundle's `additional_dependency_refs`.

It does **not** check that the exact fact selected by `_validate_discovery_consumption` has that determinant release in its own `source_empirical_provenance_refs`. A multi-release receipt can declare releases A+B and own a fact whose exact provenance is A; the consumer query/witness and M1 additional dependency can use B; the actual existing world consumer accepts.

Reproduction:

```bash
PYTHONPATH=$PWD PYTHONDONTWRITEBYTECODE=1 TMPDIR=<private-proofroot> \
python3 WORKER_RETURNS/PYAT960_S2G_G5/repro_multirelease.py <private-proofroot>
```

Input:

- base accepted native sourcefree S2-F closure (release A = `REL-m01`, `95de34f0...`);
- second real release B = `REL-m01-missing-weight`, `87a5584d...`;
- receipt `source_release_refs` = A+B;
- selected fact exact provenance = A only (`cc3f9b07...`);
- M1 bundle facts from A, `additional_dependency_refs` B;
- consumer query/witness/determinant release B.

Expected: cold consume refuses because the selected fact's exact provenance release A is not the determinant B.

Actual: `exit=1` with `defect_if_accepted=true`; actual existing consumer returns:

- state `LEARNED_CONSUMER_EXACT_SUPPORTED`
- consumer hash `4790c38f7fdcd87386fd1a26e3f281cdfbfb0e792c8f95c29658a640f7c07f92`
- composition `461f512048c9949ed7760366dff155c759b31bf0877d04ec8ef89e99e97925ea`
- multi S2-F root `8ab33706ad8f413f157aecfcfcf261b8a5b442568375bc96d669868cd4b6a040`
- artifact root `32d19b29d2df59356ff25250f0f5d1998a8a61cf4a4c22d4759f16d681ae4e48`
- M1 `18b73963e1ceed396c3f4a250a8363de5bccb2715f73c3f93ab4b3f8e7583fea`
- M2 `53c1e6fa0448aa65039cd74f03871b837b5b9a2f93b0782741774b2ecd1def35`
- B5 `decb1199fd753eaef349879cc06c32c838705bd4271ffac1b7c55308bf90887f`

Owner: `rawlsing_next/pre553_durable_learned_lifecycle.py::consumer_composition` around lines 1281–1305 (after `_validate_discovery_consumption`); `_m1_evidence_binding` line 1234 only checks the determinant release in additional refs.

Minimal repair: after selecting the fact, require the exact determinant release key in that fact's `source_empirical_provenance_refs`, and add a multi-release hostile regression. Preserve the base/M1/M2/B5/current/as-of paths. No new engine, issuer, or broad hardening.

Consequence: the actual first reader can serve a positive product whose determinant source release is not the selected fact's release. This is not counts-only or cosmetic; it is a wrong-source positive.

## 6. Known REDs, concessions and boundaries

- A-C01 B-cut RED is preserved (`0071aefb` accepted mutant root `92ba894b...` with consumer `2690cdbe...`); current `a3d1e33` refuses and the current test passes.
- The authors' own strongest next falsifier (multi-release source ownership) is the exact remaining defect; B's B-D1..B-D4 and A-C01 repairs are genuinely accepted where they go.
- Multi-product history beyond the exercised one-/two-release supersession chains was not independently falsified; a same-release re-registration attempt was blocked by the existing B5 composer before producing a valid artifact, so no defect is claimed there. This is nonblocking.
- A's receipt used `60105d28...` as `contract_frozen_at_sha` from #940; B corrected S2-G to `63836a...`; documentary only.
- Production current/as-of issuer/revocation, accepted S2-E/S2-D, scientific M1 rule, original35, integrated 100k/6 GiB and protected merge remain external holds.
- No original respondent/SAV/DTA/DB bytes opened; synthetic sourcefree fixtures only.

## 7. Return and next turn

- Return: `WORKER_RETURNS/PYAT960_S2G_G5/{receipt.json,00_HANDOFF.md,repro_multirelease.py,repro_resources.py,evidence/}`.
- Independent decision: **REVISE_EXACT_DEFECT**; G5 FAIL; integration UNMERGED; full original S2-G HOLD_EXTERNAL.
- Exact finding goes to HQ/original owner for **one bounded repair/retest** of G5-MR01 only. No broad A/B reconnaissance, no new reviewer, no optional hardening, no reviewer patch. Preserve base/change/restore/current/as-of/refusal evidence; rerun 153 + 19; freeze the new code SHA; a distinct nonauthor G5 re-receives. If the bounded-repair allowance is exhausted, HQ adjudicates the exact unresolved case.

**Stop finite.** No auto-wake, no polling, no original/science/protected grant.
