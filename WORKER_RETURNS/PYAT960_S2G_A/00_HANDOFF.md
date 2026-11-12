# PYAT960-S2G — ROLE A GO-FIRST HANDOFF

## 1. Exact artifact

- Branch: `agent/pyat960-s2g-a-r1`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat960-s2g-a`
- Protected base: `6a5c12f04323d74001f9632063ec907f4fc4468e`
- Startup / B base: `7064daa14d93109211629e72d08f3a6e705a0d57`
- **Implementation SHA:** `50c2e33b48a040835e9981a822901186f0cc1ba0`
- Contract SHA256: `635a423beea158a67653d8c03ea7aee9c158f21986d4d598018d0976db73552b`
- Contract source: `WORKER_COMMISSIONS/PYAT_SUCCESSOR_960/contracts/S2-G_v1.md@63836a168cc99b0ed8f87f7f7a6e76192f7a1898`
- Session: `ses_e3120ba1cffeO1w43uU5MLh4yq` / `opencode-go/deepseek-v4.1-flash#max`
- Changed paths:
  - `rawlsing_next/pre553_durable_learned_lifecycle.py` (new)
  - `rawlsing_next/tests/test_pyat960_s2g_durable_lifecycle.py` (new)
  - `rawlsing_next/tests/test_pyat960_s2g_fresh_process.py` (new)
  - `WORKER_RETURNS/PYAT960_S2G_A/`
- No existing M1/M2/B5/world/S2-F/I02/Parquet/query/discovery/FF/C11 file was modified.

Run:

```bash
python3 -m pytest \
  rawlsing_next/tests/test_pre553_learned_world_composition.py \
  rawlsing_next/tests/test_pre553_learned_empirical_adjudication.py \
  rawlsing_next/tests/test_pre553_learned_product_lifecycle.py \
  rawlsing_next/tests/test_pre553_learned_product_release.py \
  rawlsing_next/tests/test_universal_learned_consumer.py \
  rawlsing_next/tests/test_pyat960_s2g_durable_lifecycle.py \
  rawlsing_next/tests/test_pyat960_s2g_fresh_process.py -q
# 147 passed in 31.79s

python3 -m pytest \
  rawlsing_next/tests/test_pyat940_s2f_durable_closure.py \
  rawlsing_next/tests/test_pyat940_s2f_fresh_process.py \
  rawlsing_next/tests/test_pyat940_s2f_b_negative_and_multisource.py \
  rawlsing_next/tests/test_pyat940_s2f_a_counter_provenance.py -q
# 19 passed in 7.22s
```

## 2. Governing contract

S2-G / P2-08 requires an external durable custody/current/as-of seam around the
existing M1/M2/B5 learned product chain, not a new engine: an actual native
sourcefree fact must reach the real M1 family adjudicator, M2 `constitute_release`,
B5 registration/publication/current selection, and the existing
`evaluate_learned_world_consumer`; a fresh process must reopen the exact product
and as-of/current state; a coherent fake checkpoint and stale/revoked/wrong
purpose issuer must refuse; no self-hash may grant CURRENT; no second B5 replay
engine or complete product archive is permitted.

The accepted S2-F closure is the input. Full S2-E/S2-D integration and a real
production current issuer are external holds, so this is a sourcefree isolated
fixture-grade candidate, not terminal native/science acceptance.

## 3. Strongest achieved result

- Native M01 graph → actual M1 adjudication (TEST_ONLY native validator fixture)
  → actual M2 release → actual B5 REGISTER/PUBLISH/SELECT_CURRENT → actual
  `evaluate_learned_world_consumer`.
- Durable artifact:
  - root `852498f72ed7c1940d55caae0a75bab6869aa854bb83f7a39451debc57be2fe5`
  - artifact `bb14f54c88515f8c0e0d1806afc0457fa1439d9c4212ad07381b9f7bc8df23eb`
  - M1 disposition `9a7f5e31226f4707c2aba6304dd791da1c4d78a5aa3a1661545c22085b8a3fdd`
  - M2 release `3423ef93f9c6a4de45574ed89b47554b3062b7b0c97d2b373ad907a4f19747b9`
  - B5 selection `2dd500392ea3b05ef0903fe4a46977f74627d86bbe0a802f2e663e085c98ef14`
  - checkpoint `327a56898cdf8cae9ca1fa3bd778e1d3ede88faea2c5b88f06ed16ec2a69794d`
  - consumer `LEARNED_CONSUMER_EXACT_SUPPORTED`, hash
    `2690cdbeadabb0e90179d726029fa8b765995a15a1da26d7fe72bba0819bd597`
- Fresh Python subprocess with no native fixture import:
  - opens the artifact with external root pin;
  - reopens the accepted S2-F closure;
  - reruns the actual C1/N10E discovery composition without source repository;
  - calls the actual learned/world consumer;
  - reports exact consumer hash, `source_opens=[]`, matches_expected=true.
- Exact changed/restored product root; supersession/as-of event and checkpoint
  history; true NO_CURRENT preservation.
- Hostile: missing M1 bundle/determinant/family rule, missing history, changed
  M2 dependency, self-rehashed fake checkpoint, wrong root, wrong as-of,
  revoked/stale/wrong-purpose issuer, wrong selection/key, missing pointer,
  crash before manifest all refuse.
- 147 owner+S2-G tests PASS; 19 S2-F regression tests PASS.

## 4. Own hostile findings and repairs

1. **Cold consumer cannot be a fabricated `AnalyticalCompositionResult`.**
   The actual consumer requires a retained native original. Repaired by
   rerunning the actual C1/N10E discovery composition in the fresh process from
   the accepted S2-F closure, not constructing a composition record.
2. **A self-hash checkpoint/pointer is not current authority.**
   Current is only returned through a TEST_ONLY external attestation whose root
   is pinned independently. Revoked/wrong-purpose/stale checkpoint/wrong
   selection/key/wrong pin all refuse.
3. **An artifact root alone does not prove M1 integrity.**
   Added exact M1 input-bundle and family-rule preimages, content-hash checks,
   and disposition/receipt/M2/B5 ref closure checks on open.
4. **As-of claims can be inconsistent.**
   An attestation whose as-of predates the current selection refuses; historical
   event/checkpoint as-of resolves only the product current at that point;
   pre-selection as-of returns `UNKNOWN_CURRENTNESS`.
5. **Same-chain source identity.** The cold composition checks the persisted
   S2-F root, discovery receipt, producer query/predicate, release ownership and
   closure release identity before consuming.
6. **Crash/recovery.** Staged manifest/blob publication with fsync, dead
   staging/temp cleanup, visible-artifact rollback, and no-pointer recovery.

## 5. Unresolved challenges

- No real production current/as-of issuer or revocation service; TEST_ONLY
  attestation only. This is an external authority HOLD.
- No real M1 scientific family validator; the rule is a TEST_ONLY native fixture.
  No scientific/original35 claim.
- Full accepted S2-E complete producer/saved reader and full joined S2-G remain
  absent; integrated 100k/6 GiB NOT_RUN.
- The changed-input test uses a different actual native M1 adjudication fixture,
  not a mutation of one raw fact inside a single batch. The lifecycle property
  (different product/selection, exact restore) is proven.
- The cold consumer reruns the discovery route from S2-F, not the full
  source-backed direct/saved-reader route.

## 6. Likely attack surfaces

1. Build a coherently rewritten B5 checkpoint plus a new external pin and see
   whether current/as-of can be made to accept a different productive story.
   The old pin must reject it; no production issuer exists to distinguish it.
2. Remove/replace `m1_evidence.input_bundle` or family rule and rehash the
   artifact; verify open's exact projection checks.
3. Change one M2 closure member or release dependency and recompute the artifact
   root; verify `M2Repository.register_release`/consumer refusal.
4. Try an M1 disposition with a different `family_rule_binding_ref` but same
   receipt/M2/B5 refs; verify no silent productive admission.
5. Try a current attestation with a valid artifact root but stale/foreign
   selection receipt, key, purpose, checkpoint hash or pre-selection as-of.
6. Try an artifact from one S2-F closure with determinants pointing to another
   closure/receipt/release; verify cold source/release ownership check.
7. Try a no-current artifact and confuse `consume(require_current_selection=False)`
   with current service; `consume_current` must remain the only attested path.

## 7. Rejected alternatives

- **Constructing `AnalyticalCompositionResult` directly from identity material.**
  Rejected: `native_composition_original` custody would be absent and the actual
  consumer would refuse `COMPONENT_NOT_RETAINED_NATIVE_ORIGINAL`. Re-ran the
  actual composition owner instead.
- **Treating the B5 checkpoint hash as CURRENT.** Rejected: local self-hash is
  not an external issuer. Added a separate TEST_ONLY attestation interface.
- **A second B5 replay engine or M2 product archive.** Rejected: reused
  `export_checkpoint/from_checkpoint`, M2 constructors and the existing
  consumer; stored one compressed content-addressed product preimage.
- **Editing native owners to accept a shortcut.** Rejected; existing APIs
  already accept exact reconstructed objects. Adapter-only changes.
- **Claiming full S2-G.** Rejected: S2-E/S2-D, production issuer, scientific rule
  and integrated 100k are explicit holds.

## 8. Proof boundaries

- Grade `S2_SOURCEFREE_ISOLATED_FIXTURE`; no original35, source-native, 100k,
  production current, scientific, actor, or protected merge claim.
- G1-G4 candidate PASS at fixture grade; **G5 NOT_RUN**, `DELEGATED_CANDIDATE`.
- Integration `UNMERGED`; no protected receiving.
- M1 validator is TEST_ONLY; no scientific acceptance.
- Current/as-of interface is TEST_ONLY and externally pinned; production issuer
  is a HOLD.
- One compressed artifact blob + tiny manifest; no duplicate complete product
  estate. Source opens 0 in the observed fresh consumer.
- 147 owner/S2-G tests and 19 S2-F regressions pass at this SHA.

## 9. Resource evidence

- Artifact retained: 32,499 bytes (31,987 compressed blob + 512 manifest).
- Logical preimage: 283,854 bytes.
- Cold open 0.103 s; consumer 0.061 s; repeat 0.059 s.
- Process peak RSS: 106,831,872 bytes.
- Source opens: 0.
- Rows: 3 B5 events, 5 M2 closures, 25 M1 determinant material keys, 2 artifact
  files.
- 6 GiB cap PASS at fixture grade; integrated 100k NOT_RUN.

Evidence:

- `WORKER_RETURNS/PYAT960_S2G_A/evidence/s2g_evidence.json`
- `WORKER_RETURNS/PYAT960_S2G_A/evidence/selected_147.txt`

## 10. Status

- `implemented_sha = 50c2e33b48a040835e9981a822901186f0cc1ba0`
- `evidence_grade = S2_SOURCEFREE_ISOLATED_FIXTURE`
- `G1-G4 = PASS` candidate at fixture grade
- `G5 = NOT_RUN`, no self-issued acceptance
- `disposition = HOLD_EXTERNAL` for full original S2-G
- `stop_state = READY_FOR_RECEIVING`
- `integration = UNMERGED`
- `ABI = LOCAL`; affected tasks S2-E/S2-G/S1-D are dependency holds.

B must independently read the original contract and this full handoff/code/tests,
attack and repair the same descendant, then A counters once. Distinct nonauthor
G5 is still required. Stopping finite; no polling or auto-wake.
