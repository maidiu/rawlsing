# SOROK M2 R3 — fresh independent I2 return

**DISPOSITION: REVISE.** Original 135/135 author cases independently PASS; 6 NEW held-out cases yield 4 PASS and 2 RED. Reviewer did not repair the candidate, self-adopt, issue actor authority, or mutate production.

## Custody

- Private repository: `maidiu/rawlsing`
- This reviewer branch sealed startup: `a9f2ca4ebac6067845e9821459a69e383931f5dd`, initially containing only the commission
- Exact reviewed R3 commit: `9c1ab2fa172e41c7fb033b5f134b25255d65126c`
- Reviewed kernel Git blob SHA-1: `645308250f54133c1f9d707a5851f689942f18ba`
- Independently materialized and imported kernel SHA-256: `838d0852e6b1b28bb733b1eda580b3dc53f5db3d47e3a0caefbd3072022ad45a`, 27,840 bytes
- Original R2 commit: `e8f375e9feae187e8a1add2343100ca05d9fffc4`, reconstructed original kernel SHA-256 `88bb8c65dfd88efd1843f16e1bb6d51e1fa01a0dc1fdccb13e03a9b2b394d8d3`, 27,303 bytes
- Independent preceding R2 hostile court: `e8b2d6be5ba243729f387cda4048cc30a52664d2`; historical M3 original source-preimage court: `49dfcb30971310756a12f659961600d9f2eb4a11`
- Actual Python 3.13.5, pytest 9.0.2, isolated filesystem and subprocess; private GitHub connector supplied explicitly copied exact source; no automatic checkout mount.
- Reviewer is not an R2/R3 author. The selected reasoning-effort setting was not independently visible through runtime tools.

## Independent author closure

Original M2 **41 PASS**; M3 lawful **32 PASS**; packaged M3 **3 PASS**; source-preimage **15 PASS**; original historical M3 **3 PASS**; prior hostile **11 PASS**; R2 relation **14 PASS**; earlier independent R2 I2 held-out **2 PASS**; new R3 author actor-owner cases **14 PASS**. **Total: 135 PASS, 0 failures/errors/skips**, unchanged original test bytes and SHA-256-verified R3 loaded kernel. Actual JUnit `author_135_R3.xml` SHA-256 `b7ce09b0ec327fd94a441605c8a41748256b70dda0912f658d59a79fc1c1b8e7`.

Exact original two-case I2 held-out against original R2: **1 PASS / 1 RED**, `CHILD_SELF_ACTION_WRONGLY_ADMITTED_AS_COUNTERPART`; JUnit `heldout_R2.xml` SHA-256 `47871e972992254fa4479bb5fd9350bb967103f775b695a4b1ddcd8badd15a1f`. Same unchanged held-out against R3: **2 PASS**, JUnit `heldout_R3.xml` SHA-256 `be3b5fd6ca7dca47b21ef0d928a5c793da7b7ab314dc9a9ada30f3bfed0db9af`. Both other_P and other_Q valid action-owner positives passed in author and earlier independent suites.

## Six fresh adversarial cases (not R3 author cases)

Exact newly authored source `test_fresh_i2_adversarial.py` SHA-256 `b9c01d20fe6b2d771246fd7b1b36671b9dbda8bddae062fd6c96df8196c471de`, six actual pytest cases: **4 PASS, 2 RED**; JUnit `heldout_fresh_i2.xml` SHA-256 `c51902eb619f14039c441c103a0b482b528fc0be9875536d8bacc3260208453e`. Preserve REDs verbatim, do not modify candidate or expected assertions.

**NEW RED 1: historical rule identity.** Take a genuinely committed t6 interpretation, replace its `rule_hash` with `DIFFERENT_UNISSUED_RULE_HASH`, recompute unkeyed content digest for internal consistency. `validate(scene)` passes and `eligible(scene,tampered,'later')` fails to refuse. `_lineage_integrity` checks rec hash/version/preimages but does not check admitted `rec.rule_hash` against historical rule identity. R2 0.4.0 → R3 0.4.1 requires explicit migration/authorization rather than accepting arbitrary re-hashed rule claims.

**NEW RED 2: action-owner self-witness laundering.** At t9 keep genuine other_P action owner with independently witnessed earlier project; make `Event.observer`, `Relevance.observer`, and child's observed `HistoryWitness.observer` all `other_P` (refresh objective event reference). `validate()` passes and all six relation modes become eligible despite no immediate witness independent of the acting other_P. R3 repaired child-own-action eligibility, but its independent-witness checks compare against the child, not independently against the action owner. Either refuse such fixtures or obtain an explicit competent owner ruling accepting action-owner testimony; cannot claim native independent observation by test-only label.

**Four new PASS:** (3) alternative unconsumed relation receipt can lapse after proposal while exact consumed readset is retained; (4) later t10 observation and clock cannot authorize t9 relevance; (5) consumed action-owner receipt replacement after append fails historical continuation with `SOURCE_PREIMAGE_IDENTITY_COLLISION`; (6) `NO_CHANGE` retains exact state, wrong synthetic grant refuses. No false positive acceptance implied by those four passes.

## Frozen M1/I2 and native ceilings

Frozen original M1 37 / I2 23 binary tar suites **NOT RERUN**. Keep historically reported **19 M1-on-R2 and 10 I2-on-R2** compatibility RED names unresolved; do not mark them green or erase historical 0.4.0 record schema differences. The three historically strict M3 source-preimage controls are 3/3 PASS in this bounded test only.

B3 ceiling while REVISE stands: **read-only quarantined source-free `validate/eligible/propose` possibility research**, with relation admission defects flagged; no authoritative durable append, schema migration, actor adaptation, memory issuance, canonical integration, production use, or source35/empirical interpretation. Synthetic `fixture_grant()`, `RULE_HASH`, `TEST_ONLY` issuers and fixture hashes are NOT native ADP authorizations. Native ADP019/021 objective occurrence/time, ADP015 other-person relations, ADP016/017 memory/access, CAN008/011 psychological selection/owner effects require separately qualified competent source and actor owners. Neither native cryptographic signatures nor actual psychology was exercised.

Disposition can advance only after separate R3-successor author repairs two REDs against unchanged heldout, records an explicit old schema/RULE_HASH migration contract, and a **new** independent scientific court adjudicates actor-owner vs observer rights. This reviewer may not do the repair or self-adopt.

## Actual commands and evidence

```sh
PYTHONPATH=. python3 -m pytest -q --import-mode=importlib test_m2.py test_m3_independent.py test_m3_unresolved.py test_source_preimages.py frozen_m3/test_original_preimage.py test_local_hostile.py test_relation_custody.py test_heldout_actor_independence.py test_r3_counterpart_actor_custody.py --junitxml=author_135_R3.xml
PYTHONPATH=. python3 -m pytest -q --import-mode=importlib test_fresh_i2_adversarial.py --junitxml=heldout_fresh_i2.xml
# From isolated r2_negative source tree, original R2 exact kernel:
PYTHONPATH=. python3 -m pytest -q --import-mode=importlib test_heldout_actor_independence.py --junitxml=heldout_R2.xml
```

The complete local standalone source/pytest/JUnit evidence archive is `sorok_m2r3_fresh_i2_evidence.zip` (delivered alongside this review), 74,011 bytes, SHA-256 `fd1969a5801331ca01ff34fca4526a1ffa9cebd991434629162486d89bedf0c9`. The archive contains full executed test suite, newly authored code and source hash manifest; remote connector metadata alone is not represented as execution. `execution_summary.json` and the sanitized 00D environment passport will accompany this return.

**Terminal: `REVISE__R3_135_PASS__2_NEW_I2_RED__NATIVE_AUTHORITY_UNPROVEN__NO_ADOPTION`.**
