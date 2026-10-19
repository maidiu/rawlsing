# SOROK M2 R4 — rule identity and independent counterpart-witness repair

**DISPOSITION: `R4_IMPLEMENTER_EXECUTED_GREEN__FRESH_INDEPENDENT_I2_REQUIRED`.**

**This is a user-directed bounded sourcefree R4 repair candidate. It is NOT an HQ-issued commission/seal, fresh independent I2 acceptance, semantic issuance, B3 integration, CAN/ADP authority, actor-state permission, or production adoption.** Work is isolated in a new branch and a NEW return subtree; original R2/R3, prior reviewer return, accepted laws and governed code are unchanged. The same conversation that performed the R3 independent I2 now implements R4, so its implementation and execution cannot count as an independent R4 acceptance court.

## Source custody and exact target

- Private repository: `maidiu/rawlsing`
- New branch: `agent/rabochii-sorok-20261018-m2r4-rule-witness-repair-userdirect-r1` initialized from exact original R3 `9c1ab2fa172e41c7fb033b5f134b25255d65126c`, not a purported new HQ seal.
- Original R3 kernel Git blob `645308250f54133c1f9d707a5851f689942f18ba`; SHA-256 `838d0852e6b1b28bb733b1eda580b3dc53f5db3d47e3a0caefbd3072022ad45a`; unchanged.
- R4 kernel `candidate/kernel.py` blob `045331889e922274ba0a31bb78d4b110aaba06a1`; SHA-256 **`5b8ac91ca8b3b9afb068493f2a1d6c2dabdc650814ff5f099f0e670d09823940`** (28,458 bytes), verified by independent local hashing and exact remote GitHub blob lookup.
- R4 12-case `test_r4_owner_rule_hostile.py` blob `85fa5794663a9217ec9a3dabec170d076e670f9c`; SHA-256 `b62b841042da187637799952be30164b3ea83f3b453169bb901372227453e28d`, remote blob verified.
- Pin `source_refs.json`, `candidate_vs_r3.patch`, `execution_receipts.json` and `environment_passport_delta.json` for transport and future I2.

## The TWO original fresh-I2 REDs repaired

**RED 1 — arbitrary historical rule hashes laundered by recomputing an unkeyed record digest.**

R3's `_lineage_integrity` checked `digest(data)==rec.hash` but did not authorize `rec.rule_hash`. A record reissued with an attacker-chosen different rule hash and freshly computed digest passed. R4's `_lineage_integrity` now requires `rec.rule_hash == RULE_HASH`, with explicit `HISTORICAL_RULE_IDENTITY_UNQUALIFIED` refusal; the R4 contract/name is `M2_INTERPRETATION_SOURCE_TEMPORAL_IDENTITY@0.4.2_CANDIDATE`. A self-consistent hash of user-controlled data is not itself a grant of rule identity. Old versions fail closed until competent owner migration; no historical record is silently edited to make it green.

**RED 2 — other_P's own testimony masqueraded as independent corroboration.**

R3 required a genuinely distinct action owner and concordant owner fields in `Event`, `Relevance`, and child-observed `History`, but permitted `other_P` to be all three observers of `other_P`'s own t9 action. R4 qualifies other-person relation alternatives only if **(a)** the objective event's `observer`, **(b)** the qualified `Relevance.observer`, and **(c)** the independently registered observed-history `HistoryWitness.observer` are each **different from the actual `e.action_owner`**. The existing independent-from-child constraints remain. This does not require three different observers; it refuses laundering an actor's own action through purportedly independent observation. An actual other-owned event plus independent third-party records still yields all six qualified noncausal possibility modes. This is a bounded sourcefree independence criterion, not a native epistemic or legal issuer.

## Actual execution (Python and pytest)

Python **3.13.5**, pytest **9.0.2**, real isolated filesystem, imported source, subprocess and original unmodified tests. Source binary hashes verified before running. Individual JUnit XML and stdout logs were produced for each suite:

| Court | R4 result |
| --- | ---: |
| Original M2 | 41/41 PASS |
| M3 lawful | 32/32 PASS |
| Original packaged M3 | 3/3 PASS |
| Source preimage | 15/15 PASS |
| Historical exact M3 source-preimage | 3/3 PASS |
| Original local hostile | 11/11 PASS |
| R2 consumed-relation | 14/14 PASS |
| Earlier independent I2 heldout | 2/2 PASS |
| R3 actor-owner authored cases | 14/14 PASS |
| **Unchanged R3 independent I2 hostile six** | **6/6 PASS (previously 4 PASS/2 RED)** |
| NEW R4 author-hostile (three individual witness-field swaps, source replacement, rule mutation, NO_CHANGE, positive controls) | 12/12 PASS |
| **TOTAL** | **153/153 PASS; 0 FAIL/ERROR/SKIP** |

Also reran unchanged original R2 on earlier independent two-case heldout as a genuine negative control: **1 PASS / 1 expected RED**, preserving `CHILD_SELF_ACTION_WRONGLY_ADMITTED_AS_COUNTERPART`.

Standalone reproduction, after SHA-256-verifying and staging the inherited exact pinned suite files beside R4 `kernel.py`:

```sh
PYTHONPATH=. python3 -m pytest -q --import-mode=importlib \
 test_m2.py test_m3_independent.py test_m3_unresolved.py \
 test_source_preimages.py frozen_m3/test_original_preimage.py \
 test_local_hostile.py test_relation_custody.py \
 test_heldout_actor_independence.py test_r3_counterpart_actor_custody.py \
 test_fresh_i2_adversarial.py test_r4_owner_rule_hostile.py \
 --junitxml=verified_r4_full.xml
```

Full standalone execution bundle containing exact local source snapshots, SHA manifest, diff, real logs, JUnit XML, receipts and the original R2 negative is available to the user as `sorok_m2r4_repair_evidence.zip`, 48,772 bytes, SHA-256 `53cfb3aaa8a5bfb325becce654e811eb6200972df02d342b858e0720a36e557c`. **Binary ZIP is NOT committed to GitHub**; GitHub's private connector supports publishing this text candidate and documentary hash references, not direct transfer of that local ZIP. Do not represent the separate archive as a remote repository file.

## Open scientific and authority boundaries — no overpromotion

- **Historical version migration deliberately NOT solved**: R2 `@0.4.0`, R3 `@0.4.1` and R4 `@0.4.2` have different rule hashes; R2/legacy observations may also lack `observed_action_owner`. There is no authorized old-record decoder, source owner history attestation, schema crosswalk or actor-state migration grant. Historical records must be quarantined, not silently rewritten; a separate owner must specify whether and how to append provenance-preserving successor versions.
- **Frozen M1/I2 original binary tar suites NOT RERUN**. Retain documentary 19 M1-on-R2 and 10 I2-on-R2 historical compatibility REDs; not made obsolete or retrospectively passed.
- **Synthetic source custody only.** `fixture_grant()`, `RULE_HASH` and test-only witnesses/issuers cannot counterfeit native ADP015/016/017/019/021, CAN008/011, real contemporaneous actor evidence or authentication. An unkeyed SHA-256 contract digest is not an externally issued runtime signature.
- **B3 boundary:** at most quarantined, read-only sourcefree research possibility enumeration. No canonical merge, interpretation-state mutation under a real actor, native owner grants, validated psychological selection, empirical original35 claims, user wake or product deployment.
- **No repairer self-acceptance.** A separate new reviewer must reconstruct exact R4 bytes, independently reproduce both R3 REDs against unchanged R3, verify 153 controls against R4 plus NEW not-shared heldouts (including cross-owner witness custody and authorized migration refusal), and issue `ACCEPT_SCOPED`, `REVISE` or `HOLD` on its own reviewer branch. A successful test suite alone never self-adopts.

**Terminal:** `R4_SOURCEFREE_REPAIR_VERIFIED_153_PASS__NEW_I2_PENDING__NO_NATIVE_AUTHORITY__NO_SELF_ADOPTION`.
