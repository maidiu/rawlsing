# PYAT960-S2G — ROLE B FOLLOW-UP HANDOFF

## 1. Exact revised artifact

- Branch: `agent/pyat960-s2g-b-r1`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat960-s2g-b`
- Protected base: `6a5c12f04323d74001f9632063ec907f4fc4468e`
- Startup PR948 stage: `7064daa14d93109211629e72d08f3a6e705a0d57`
- A delivery / B base: `eb8f097341738dcc08ae3172fa35aeebcdc061c3`
- A implementation: `fc820533a2a90b948a9e8e80b4f220005e701d4b`
- B code/test cut (`implemented_sha`): `0071aefb05d8ebbd75058a10c5e831d994a2f96f`
- Contract SHA256: `635a423beea158a67653d8c03ea7aee9c158f21986d4d598018d0976db73552b`
- Contract source cut: `63836a168cc99b0ed8f87f7f7a6e76192f7a1898`
- Contract freeze commit (corrected): `63836a168cc99b0ed8f87f7f7a6e76192f7a1898`
- Session: `ses_e3120b9efffegreD5YfH7dOO15` / `opencode-go/deepseek-v4.1-flash#max`
- Code/test changes:
  - `rawlsing_next/pre553_durable_learned_lifecycle.py`
  - `rawlsing_next/tests/test_pyat960_s2g_fresh_process.py`
  - `rawlsing_next/tests/test_pyat960_s2g_b_adversarial.py`
- Return:
  - `WORKER_RETURNS/PYAT960_S2G_B/receipt.json`
  - `WORKER_RETURNS/PYAT960_S2G_B/00_HANDOFF.md`

The return-freeze commit changes only these two return files; code/tests are unchanged from `0071aefb`.

Run:

```bash
python3 -m pytest \
  rawlsing_next/tests/test_pre553_learned_world_composition.py \
  rawlsing_next/tests/test_pre553_learned_empirical_adjudication.py \
  rawlsing_next/tests/test_pre553_learned_product_lifecycle.py \
  rawlsing_next/tests/test_pre553_learned_product_release.py \
  rawlsing_next/tests/test_universal_learned_consumer.py \
  rawlsing_next/tests/test_pyat960_s2g_durable_lifecycle.py \
  rawlsing_next/tests/test_pyat960_s2g_fresh_process.py \
  rawlsing_next/tests/test_pyat960_s2g_b_adversarial.py -q
# 152 passed in 44.94s

python3 -m pytest \
  rawlsing_next/tests/test_pyat940_s2f_durable_closure.py \
  rawlsing_next/tests/test_pyat940_s2f_fresh_process.py \
  rawlsing_next/tests/test_pyat940_s2f_b_negative_and_multisource.py \
  rawlsing_next/tests/test_pyat940_s2f_a_counter_provenance.py -q
# 19 passed in 8.43s
```

## 2. What I independently reconstructed first

I verified the S2-G contract hash at `63836a...`, read PROGRAMMA PYAT, canonical MCR-lite, original #919 S2-G, successor #960, R3C/R3S and A's full handoff/receipt/code/tests. Native owners are read-only and were exercised as-is:

- `pre553_learned_empirical_adjudication.adjudicate_learned_empirical`
- `pre553_learned_product_release` M2 subject/closure/release owners
- `pre553_learned_product_lifecycle.LearnedProductLifecycleExecutor` and checkpoint/replay/as-of owners
- `pre553_learned_world_composition.compose_learned_world` / `evaluate_learned_world_consumer`
- accepted `pre553_durable_empirical_closure` S2-F cold closure
- actual C1/N10E analytical composition owner

## 3. Defects established in A's artifact (all reproduced first)

### B-D1 — cross-chain M1 evidence was not bound to the declared S2-F closure (SEV-1)

I published an internally valid artifact whose M1 bundle/disposition used a foreign native fact/receipt chain, while the consumer determinants pointed at the base accepted S2-F closure. The actual `evaluate_learned_world_consumer` returned:

```text
LEARNED_CONSUMER_EXACT_SUPPORTED
```

with the base consumer hash `2690cdbe...`. The M1 product was not the product of the declared empirical evidence. This is a frozen G1/G2 failure, not a paperwork issue.

Repair: cold consumption now requires the retained M1 input bundle, disposition fact/receipt/query/predicate refs, consumer discovery receipt/query/predicate and source release to be exact members of the declared S2-F closure, and the bundle preimage to match the disposition's `input_bundle_ref`.

### B-D2 — unpinned/foreign as-of checkpoint accepted (SEV-1)

`resolve_as_of_checkpoint` accepted an unpinned checkpoint from a different executor with the same selection key and returned a learned-product release that was not in the artifact's retained history. Pinning the foreign checkpoint to its own self-hash also worked. This violates the independent as-of trust boundary.

Repair: `resolve_as_of_checkpoint` now requires `expected_checkpoint_hash`, verifies supplied event refs are a prefix of the retained event history, and verifies supplied selection/no-current receipts are subsets of retained history before replay.

### B-D3 — B5 replay/learned-receipt/protocol history not verified (SEV-1)

A coherently rewritten B5 replay receipt with one event removed was accepted at open and the artifact served exact supported. A tampered learned-receipt event list, a tampered B5 protocol view (`product_family_ref`), and a tampered learned-receipt M2 closure ref were also accepted under a new self-hash pin.

Repair: `open_learned_lifecycle` now verifies the replay receipt against `executor.audit_replay()`, the learned receipt event refs against all retained events for the M2 release, the learned receipt M2/determinant/replay/explanation roots against reconstructed M2/M1 objects, and every protocol-view field against the retained B5 subject/M2 closures/M1 outcome.

### B-D4 — A's changed-input test was not same-chain native evidence (SEV-1 evidence gap)

A's G02 changed the M1 family-rule/validator tag/fixture while retaining the same underlying facts. It proved a different rule label, not a changed native fact reaching M1/M2/B5/first reader.

Repair: added B01, which changes real native physical cells in the same M01 route, publishes a changed S2-F closure, builds the changed M1 bundle from that changed native output, composes M2/B5, and consumes the changed closure. It then restores the exact base artifact.

## 4. Independently verified strengths of A (conceded)

- The overall durable M1/M2/B5/world-consumer shape is correct and preserved.
- A's base artifact root `852498f72ed7c1940d55caae0a75bab6869aa854bb83f7a39451debc57be2fe5`, identity `bb14f54c...`, M1 `9a7f5e...`, M2 `3423ef...`, B5 `2dd500...`, checkpoint `327a5689...` and world consumer hash `2690cdbe...` are exact and unchanged by B's repairs.
- A's external-pin, atomic CAS/staging, crash rollback, supersession/no-current, TEST_ONLY attestation refusals and 147 owner/S2-G tests reproduce.
- The 19 S2-F regressions still pass.

## 5. B proof of improvement

### Same-chain native change and restore (G2)

Real physical-cell change in the same M01 route: R1/X 1→0 and R2/X 0→1.

| Identity | Base | Changed |
|---|---|---|
| S2-F root | `eae60b4aaec326ddd028419c640713e20abe347347e1d242ee9a65d6872152e2` | `586d39bd2a774f179d937ae19840288d5c4a510c4054da21a0a2e20403e7b546` |
| M1 disposition | `9a7f5e31226f4707c2aba6304dd791da1c4d78a5aa3a1661545c22085b8a3fdd` | `9687134b208e5142bd60efe111de736000f56a8719e34ee0762f527134712494` |
| M2 release | `3423ef93f9c6a4de45574ed89b47554b3062b7b0c97d2b373ad907a4f19747b9` | `5ec7935ca13b221c9d3a0e1174d6a7e43a69aa807d30d161ca4c90e2b734ff2a` |
| B5 selection | `2dd500392ea3b05ef0903fe4a46977f74627d86bbe0a802f2e663e085c98ef14` | `b81a25b026baf1f0472b47b2f1af172136d665d76dfed4920a1b2e824a0093b7` |
| Artifact root | `852498f7...` | `84e99c5fd2ef492b9d2ae8dd6ca043d6a94677a8dff454a9641de28a0c86f291` |
| World consumer hash | `2690cdbe...` | `4cef580c7e79c6ca2ce647749723c17040d9d2f5821a296708084c1bab2f6be7` |

Restoring the original artifact returns `published=false`, the exact base root and the exact base consumer hash.

### Hostile RED → GREEN

- Foreign M1 evidence artifact: opens under its own pin, cold consume raises `M1 input bundle discovery_receipts is not drawn from the declared S2F closure`.
- Unpinned foreign as-of checkpoint: `DurableLearnedLifecycleUntrusted`.
- Pinned foreign as-of checkpoint: `DurableLearnedLifecycleRefusal: as-of checkpoint is not on the retained event history`.
- Tampered replay receipt: `retained lifecycle replay ref differs from learned receipt`.
- Tampered learned-receipt event refs: `learned receipt event refs do not match the retained product history`.
- Tampered protocol view: `B5 protocol view product_family_ref differs from the retained B5 subject`.
- Tampered learned-receipt M2 authority closure: `learned receipt authority_closure differs from the retained M2 closure`.

### Resources (honest labels)

- Retained disk: `32,499` bytes (`31,987` compressed blob + `512` manifest).
- Peak disk for the fresh single-artifact root: `32,499` bytes.
- Peak scratch: `31,987` bytes.
- Logical preimage: `283,854` bytes.
- Fresh child process-tree peak RSS: `41,558,016` bytes.
- Parent test process self peak RSS: `115,941,376` bytes.
- Cold child elapsed: `0.2231 s`; cold wall: `0.6027 s`; repeat consume: `0.0637 s`.
- Source opens in fresh child: `0`.
- 6 GiB cap: PASS at fixture grade; integrated 100k/6 GiB: NOT_RUN.
- Rows: 3 B5 events, 5 M2 closures, 25 M1 determinant material keys, 2 artifact files.

The child process RSS, parent self RSS and retained/peak disk are reported separately; the child RSS is not mislabeled as a multi-process tree benchmark.

## 6. Self-attacks on B's repairs

- Cross-chain M1 artifact: refused at cold consume; base artifact still exact.
- Unpinned and pinned foreign as-of checkpoints: both refused; own pinned checkpoint and retained prior history pass.
- Coherently self-rehashed replay/receipt/protocol/M2-closure tampering: all refused; unmodified artifact still serves exact.
- Real native physical-cell change: changed product/consumer and exact restore.
- Full 152-test owner/adapter/B suite and 19 S2-F regressions: PASS.
- Fresh-child exact consumer with zero source opens and measured RSS.

## 7. Self-disclosed weakest point / missing proof

The M1 evidence binding is enforced at cold consume, not at publication. A foreign M1 artifact can be stored, but it cannot serve through the declared first consumer. The changed-native proof is a sourcefree synthetic physical-cell change in the same native owner route, not accepted S2-E/S2-D or source-native data. The current/as-of issuer is TEST_ONLY with a caller-supplied external pin; there is no production issuer or revocation service. The M1 validator is a TEST_ONLY native fixture, not science. The B5 replay/protocol checks bind the stored artifact to retained owner objects, but a fully coherent rehash plus a caller-supplied new pin is a different artifact by construction; the external pin is the sole trust anchor.

## 8. Remaining external holds

- Accepted complete S2-E/S2-D upstream and full joined S2-G: absent.
- Production current/as-of issuer and revocation service: absent.
- Real M1 scientific family validator/science rule: absent.
- Original35 source/measurement/U/Epre and scientific issuer: not read or claimed.
- Integrated 100k/6 GiB: NOT_RUN.
- Independent nonauthor G5: NOT_RUN.

Engineering grade: `S2_SOURCEFREE_ISOLATED_FIXTURE`; `READY_FOR_RECEIVING` for the isolated candidate, `HOLD_EXTERNAL` for the full original S2-G. Integration `UNMERGED`; G5 `DELEGATED_CANDIDATE`, not PASS.

## 9. Challenge to Agent A

Attack the repaired boundaries:

1. Publish an artifact whose M1 bundle facts are a **subset** of the S2-F closure but not the chain that produced the retained determinant receipt; verify whether the new binding catches the receipt/fact relation.
2. Build a multi-release S2-F closure where the determinant receipt and M1 bundle use one release but the composition uses another; verify the source-release binding.
3. Construct a multi-product B5 history where a learned receipt's event refs are a valid product subset but not the complete product history; verify the event/M2 closure checks.
4. Try a fully coherent rehash plus a new external pin; explain precisely why the external pin remains the only trust anchor.
5. Re-run the cold world consumer on the repaired base and changed roots; confirm `2690cdbe...` and `4cef580c...` respectively.

Then submit the frozen B head to a distinct nonauthor G5. No broad reconnaissance or optional hardening.
