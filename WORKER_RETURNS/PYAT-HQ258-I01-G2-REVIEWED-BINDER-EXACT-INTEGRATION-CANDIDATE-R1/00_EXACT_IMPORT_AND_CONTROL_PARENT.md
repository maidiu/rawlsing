# HQ258 I01 — exact import and control parent

**DISPOSITION: `INTEGRATION_CANDIDATE_READY_FOR_HQ`**
**TERMINAL:** `HQ258_I01_RETURNED__NO_SELF_ADOPTION`

**Branch:** `agent/space-bunny-pyat-hq258-g2-binder-reviewed-exact-integration-candidate-r1`
**Commission tip:** `97adfeb89ae357ae7a9baba13159946cc5973c6b` — direct origin HEAD matched ✅ (no STOP)
**Control parent:** `761291ffc24c79e5f64c5fa8625182dd05215524` ✅ matches commission
**Candidate commit:** `105510d9ee45bf18ea1086e55221700ecf7ec2b4`
**Imported from:** reviewed frozen P02 `cb4a8c5548dbe559825681e4a9f9d49af2ac7e8d`

---

## 1. Live sealed HQ258 resolved via origin — the STOP check passed

The commission required reading the HQ258 `CURRENT.json` active worker row and comparing direct
origin HEAD, stopping on mismatch.

**Live control** `f57be2d9e221eb089e3475b5f5be40ca41544510`
→ checkpoint `20261008-PYAT-HQ258-G2-INDEPENDENT-REVIEW-ACCEPTED-I01-E03-ISSUED-R1`
→ next action `LAUNCH_HQ258_I01_G2_EXACT_BLOB_INTEGRATION_CANDIDATE_AND_E03_…_IN_PARALLEL__KEEP_EE14_T1_HOLD`

The active worker row named this branch, `commission_tip = 97adfeb8…`, and
`observed_head_at_checkpoint = 97adfeb8…`.

| check | result |
|---|---|
| local HEAD vs direct origin HEAD | **identical** ✅ |
| commission tip vs CURRENT.json row | **identical** ✅ |
| **STOP condition triggered** | **NO** |

Note the live `next_action` carries **`KEEP_EE14_T1_HOLD`** — consistent with this lane granting no
EE14 use. Branch-local pointers were not used.

## 2. Pre-import verification (nothing required a STOP)

| check | result |
|---|---|
| both target blobs present in the object store | ✅ |
| both target blobs matched the commission exactly | ✅ |
| source P02 SHA `cb4a8c55…` present and reachable | ✅ |
| all four binder module dependencies present at my tip | ✅ |
| **dependency drift** | **none** |

Verified independent identities **before** touching anything:

- binder blob at P02 = `848d2d0eedb04b792747e9d6aaa49bb39d108a2c` ✅
- test blob at P02 = `cdb4dc22fd1b403dee69bee626a43b6bc41c2b0a` ✅

## 3. The import — byte-exact, by Git object read

Method: `git cat-file blob <sha> > path`. **No reimplementation, no cherry-pick, no content
edit, no worker return folders.**

| file | before | after | bytes | identity |
|---|---|---|---|---|
| `pre553_service_f8_source_scope_binding.py` | `4ba00b8e…` | **`848d2d0e…`** | 54073 → **56186** | ✅ match |
| `test_pre553_f8_receipt_permission_identity_hq254.py` | **ABSENT** | **`cdb4dc22…`** | — → **16864** | ✅ match |

sha256 of the binder moved `0a5d3020…` → `5221d8c2…`, which is exactly the reviewed candidate value.

### Diff is exactly the reviewed guard

```
binder : +33 / -0   (single BINDING_PERMISSION_IDENTITY_MISMATCH refusal block)
test   : added (was absent at this tip)
```

**Zero existing lines modified.** No refusal precedence change, no set-semantics change, no
permission granted, no model use added, no EE14 grant, no C1 custody claim.

## 4. The candidate was committed FIRST, then tested

Per the commission, the two-code-file candidate was committed before any test run, and every
oracle was executed at that **clean committed HEAD** with a clean worktree
(0 non-pycache dirty entries).

Committed blob identities re-read at the candidate HEAD: binder `848d2d0e…`, test `cdb4dc22…` —
both still exact.

## 5. Banked oracles — every expected result met

| run | exit | expected | actual |
|---|---|---|---|
| new imported court | 0 | 16 | **16 passed** ✅ |
| four adopted baseline courts | 0 | 199 | **199 passed** ✅ |
| combined | 0 | 215 | **215 passed** ✅ |
| differential regression | 1 | — | **380 passed**, 9 pre-existing collection errors |
| no-import-drift probes | 0 | — | honest/mismatch behaviour identical to reviewed |

The 9 collection errors are absent `pandas`, absent `pyarrow`, and one absent unrelated harness
module — pre-existing, unrelated to this lane, and present on this tree before any import.

## 6. No-import-drift probes (re-run on the imported code)

| probe | observed |
|---|---|
| honest match `[A]` | **BOUND**, material records `perm-A` |
| mismatch unrelated `[B]` | **REFUSED** `BINDING_PERMISSION_IDENTITY_MISMATCH` |
| mismatch subset `[A]` of receipt `[A,B]` | **REFUSED** `BINDING_PERMISSION_IDENTITY_MISMATCH` |
| honest reverse order `[B,A]` of `[A,B]` | **BOUND** — order-insensitive, exactly as reviewed |
| refusal-code occurrences in live binder | **1** |
| live binder sha256 | `5221d8c2257ab1e8ec45289a30c57ba9ed4956b8609a890e80343718a6e9c66b` |

The imported candidate behaves identically to the independently reviewed blobs.

## 7. No reimplementation, no unrelated edits

Changed source paths, exactly two, both inside the commissioned writable terrain:

```
rawlsing_next/pre553_service_f8_source_scope_binding.py            +33 / -0
rawlsing_next/tests/test_pre553_f8_receipt_permission_identity_hq254.py   added
```

No other production file, no other test, no `HQ_HANDOFF`, no accepted semantic authority, no
control merge or push, no raw survey, no actor/V3, no native F7, no AT07 issuer/root, no new
model-use permission.

## 8. Decision reserved to HQ

This worker wrote no canonical `HQ_HANDOFF` or accepted semantic authority and did not merge or
push control. Under single HQ lease, HQ may now authorize a guarded control integration that
preserves review ancestry and the diff, and records the exact adopted behaviour.

This candidate grants **no EE14 service use**, certifies **no C1 provenance**, and certifies
**no currentness**. The EE14 T1 HOLD remains in force per the live `next_action`.