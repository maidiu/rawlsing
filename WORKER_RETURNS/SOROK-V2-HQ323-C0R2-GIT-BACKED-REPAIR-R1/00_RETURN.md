# SOROK VOZHD-2 HQ323 C0R2 — Git-backed native contract repair

**Role.** Bounded source-free implementation worker. **NOT** HQ, **NOT** Pyat owner,
**NOT** independent acceptance reviewer. Independent High/I2 review follows.

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Branch | `agent/rabochii-sorok-v2-hq323-c0r2-git-backed-repair-r1` |
| Sealed startup | `be2822596fc34a3d9e6d04dfb5b4071c1e28184e` |
| Parent capability HOLD | `aac6d7d13ce386598d6e1c147687d9ed64e188b7` |
| C0P author candidate | `154a4dd5615d47f014ca90eb1234b16e983bf5c1` |
| C0I independent review | `2dacd87636352a6c805e03b3d07581193a06264b` |
| Frozen C0I preregistration | `72cc80eb93b4ddf55bb473db40aa3640ceb1e5b4` |
| Native E03 | `0e0ed50dbce2dd1434d3a3c84b937b9a956adba9` |
| Native E04T | `79cb8244a5291218bde17142b93fc2419eade396` |
| Repaired facade blob | `855bb72f494d64083cee706e12f4f3d58c47dec3` |

**Verdict: `C0R2_SOURCEFREE_REPAIR_CANDIDATE_PENDING_I2`**

---

## 1. Mandatory execution preflight — PASSES

The prior Browser worker established that Python was operational but **private
GitHub source transport was not** (1/29 modules staged). This session is a genuine
local Git-backed worktree. Runtime continuity across chats was **not** assumed;
capability was re-verified from Git objects in this session.

| Gate | Result |
|---|---|
| Direct remote branch HEAD == supplied seal | `be2822596fc34a3d9e6d04dfb5b4071c1e28184e` — **match** |
| Parent chain includes C0R HOLD `aac6d7d13` | **yes** |
| `python3 --version` | 3.11.3 |
| `python -m pytest --version` | 9.0.2 |
| `git rev-parse --show-toplevel` | real worktree |
| `git cat-file -e 0e0ed50d…` (E03) | **PRESENT** |
| `git cat-file -e 79cb8244a…` (E04T) | **PRESENT** |
| Native29 staged via proven `c0p_stage_runtime.py` | **29/29** |
| Blob preimage / SHA-256 / bytes / commit+path crosscheck vs C0I manifest | **29/29 all fields match** |
| Total closure bytes | **859,712** (exact) |
| Real imported `module.__file__` inside pinned runtime | **29/29**, **0 ambient leaks** |
| Frozen C0I court loaded without edit | blob `419f5cf1e82fb3f5817f78d48fce79265dd8d3f7` == preregistration blob |
| Both courts executable **before** implementation change | **yes** |

A working shell without object access is not an executing environment. Here the
object store is genuine and both pinned commits are present, so the
`CAPABILITY_HOLD_GIT_OBJECT_OR_TEST_CLOSURE_UNAVAILABLE` condition is **not**
triggered.

---

## 2. Three original REDs reproduced on the unmodified facade

| RED | Test | Baseline |
|---|---|---|
| **R1** portability | `test_port_runtime_binding_uses_actual_imported_native_module_tree` | **RED** |
| **R2** two contracts | `test_facade_exposes_two_distinct_owner_contract_receipts_not_two_N9_clients` | **RED** (`{'N9'} != {'N9','N10E_N10W'}`) |
| **R3** SC0 transport | `test_facade_receipt_roundtrips_frozen_SC0_envelope_not_only_a_consumer_hash` | **RED** (16 missing fields) |

Baseline frozen court: **47 PASS / 3 RED = 50**. Baseline author court: **49/49**.

---

## 3. Repairs

### R1 — runtime and provenance portability

Removed the hardcoded `RUNTIME = Path("/tmp/c0p-runtime")`. The runtime is now
derived from the **actual imported native module tree**:

```python
RUNTIME = Path(nonparent.__file__).resolve().parent.parent
```

Proven in a truly isolated worktree: `m.RUNTIME.resolve() ==
Path(product.nonparent.__file__).resolve().parent.parent`, and an AST scan of the
executed code finds **no `/tmp` literal binding**. No relocation harness edit is
required (`port_module(relocate=False)` now passes).

### R2 — genuinely distinct N9 vs N10E_N10W contracts

The two owner contracts are now materialised as **separately identifiable SC0
envelopes**, not two receipts both tagged `N9`:

| Owner | Contract version | Envelope |
|---|---|---|
| `N9` world-selection | `GENERIC_WORLD_SELECTION@1.0.0` | `WorldReceipt` |
| `N10E_N10W` ordered-possibility | `GENERIC_ORDERED_POSSIBILITY@1.0.0` | `PossibilityReceipt` |

* `consume_nonparent` is **bound** to `N9`; `consume_conception_proposals` is bound
  to `N10E_N10W`. `{a.contract, b.contract} == {N9, N10E_N10W}`.
* **Both** contracts are exposed to **both** consumers via `receipt.contracts`, so
  neither consumer is denied either owner. This is not mere tagging: each envelope
  carries the genuine owner output (N9 selected-snapshot fields and selection
  records; N10E_N10W ordered steps and source universe), and they differ in
  content, not only in a label.
* The native refusal is preserved: `route_probability` stays `None` with
  `NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL`. The two owners are never merged.

`contract` (the owner binding tag) and the envelope's `contract` (the contract
version identifier) are two different facts; both are published and neither hides
the other.

### R3 — literal SC0 two-contract WorldReceipt transport

`as_dict()` returns the literal `GENERIC_WORLD_SELECTION@1.0.0` envelope with
**all 17 required fields** populated (16 were missing): `clock`, `demand_ref`,
`dependency_closure`, `generated_criteria_echo`, `grade`, `issuer_and_use`,
`native_scopes`, `payloads`, `receipt_ref`, `refresh`, `request_id`, `selection`,
`snapshot_ref`, `state`, `values_read_refs`, `repository_refs`, `contract`.

The `PossibilityReceipt` carries all **20** of its required fields.

**No producer or issuer semantics were invented.** Every field is derived from
genuine native output:

* `selection` / `payloads` — one record per genuinely published N9 selected-snapshot
  field (5 real fields with their `field_ref`, `selection_record_refs`, `payload`,
  `payload_hash`, `public_rule`), not a synthetic filler.
* `native_scopes` — `native_unit`, `native_geography`, `release_ref`, `risk_set_ref`,
  `field_time` from `catalog.empirical_identity()`.
* `values_read_refs` — the consumer's actual `values_read` source refs.
* `repository_refs` — the real producer module blob preimage.
* `clock` — the **four-clock rectangle** (`observation_effective`,
  `publication_knowledge`, `actor_event`, `request_currentness`) plus `mode =
  KNOWLEDGE_AS_OF`, mutually distinguishable, not one value copied. The existing
  native two-clock cases are explicitly **insufficient**; this four-clock proof is
  graded separately in §5.
* `grade = TEST_FIXTURE_ONLY` and `issuer_and_use` atoms `TEST_ONLY_CONTEXT`
  throughout. `model_use_ref` is `null` — no model use is claimed.

**Typed holds where adopted law does not issue.** `generated_criteria_echo` is an
empty array: no `GENERATED_RUNTIME_FACT_REF` is issued by the adopted law here, so
none is fabricated. `same_respondent_joint_ref` is `null` — no cross-source
respondent joint exists and none is invented. `composition_mode = "REFUSED"` and
`alternatives` carries the native's own
`NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL`. Forward `Y|A` (18/32) and the
separately granted reverse `A|Y` (18/29) remain source-grant-scoped: the envelope
reports `direction = FORWARD_CONDITIONAL` and never extrapolates to automatic
reversal.

---

## 4. Execution after repair

| Court | Before | After |
|---|---:|---:|
| Original C0P author tests (unchanged) | 49 / 49 | **49 / 49** |
| Frozen C0I independent assertions (unchanged) | 47 / 50 + 3 RED | **50 / 50** |
| C0R2 adversarial court (new) | — | **23 / 23** |

**Preservation:**

* Named genuine native consumer receipt hashes unchanged: nonparent
  `52e10a2fd0ce21b30f535b2786d45d4bd88817f174caa006e5ba7f0589d851ec`, scenario
  `33251a740daff14a0920c4375b0b8577842cf812f5444e07b8313f5730fc3fde`.
* 29/29 native producer identities preserved (unmodified pinned blobs).
* Accepted source ceilings, reverse-query permission boundaries preserved.
* No modification to frozen independent tests, accepted Pyat source, original
  survey data, V3 actors, production semantic law or PRE-MAIN.

**Adversarial coverage:** default staging, changed actual import paths, forged
versions, false issuer/readset/permission, missing/dependent fields, date clock
rectangles, no-support and revocation, reverse ungrant, same/native two consumers.

---

## 5. Honest remaining limitations

1. **Four-clock proof is graded, not complete.** The envelope populates all four
   clocks and `mode = KNOWLEDGE_AS_OF`. The adopted native law supplies
   `valid_at` / `published_asof` / `field_time` / `publication` but **no independent
   archival known-at upper bound and no effective/discovered-at revocation
   timestamps**. `actor_event.caller_owns_time` is `true` because the caller owns the
   scene time — that is a statement about the caller, not a historical entitlement
   reconstruction. The existing native two-clock cases remain the only executed
   clock rectangles; the four-clock envelope is structural, not a temporal-accuracy
   claim.
2. **`generated_criteria_echo` is empty by typed HOLD.** Not a defect in transport;
   the adopted law issues no `GENERATED_RUNTIME_FACT_REF`. Populating it would
   require an unissued producer.
3. **`grade = TEST_FIXTURE_ONLY` throughout.** Nothing here is source-observed.
   No national inference, no person, no cohort estimand, no cross-survey respondent
   joint.
4. **`same_respondent_joint_ref` is `null`** and `composition_mode = REFUSED`.
   Forward `Y|A` and separately granted reverse `A|Y` are source-grant-scoped; no
   generic automatic reversal is implied.
5. **K9/K10 are NOT_RUN.** Execution is not a prerequisite to the three-RED repair.
   They are not claimed.
6. **`request_id`, `receipt_ref.id` and several `urn:test:e04:…` identifiers** are
   receipt identities of this sourcefree facade, not producer-issued object ids.
   Their `hash` fields are genuine `semantic_hash` values over the real content.
7. **`selection[].decision` maps `SUPPORTED_TEST_ONLY -> SELECTED`** and anything
   else to `DEFERRED`. This is a faithful reading of the native field state, not a
   new selection law.

---

## 6. Return package

| Path | Contents |
|---|---|
| `00_RETURN.md` | this document |
| `staging/runtime/` | the 29-module byte-verified pinned native closure |
| `evidence/native29_verification.json` | 29/29 blob SHA-1 + SHA-256 + bytes + commit/path crosscheck |
| `evidence/actual_import_identities.json` | 29/29 real imported `__file__` receipts |
| `evidence/artifact_manifest.json` | SHA-256 of every published artifact |
| `environment_passport.json` | sanitized environment passport |
| `junit/author49_baseline.xml`, `junit/author49_after.xml` | author court before/after |
| `junit/c0i50_baseline.xml`, `junit/c0i50_after.xml` | frozen independent court before/after |
| `junit/adversarial.xml` | new adversarial court |
| `tests/test_c0r2_adversarial.py` | new adversarial court source |
| `05_REMOTE_VERIFICATION.json` | remote SHA receipt |
| Modified (allowed terrain) | `WORKER_RETURNS/SOROK-R3-HQ319-C0P-GENERIC-PORT-POSITIVE-R1/repro/c0p_two_contract_port.py` (the sourcefree C0P facade) |

**Not modified:** inherited C0I independent oracle (frozen test copied to a
noncommitted temp location only), accepted Pyat native producer source, original
surveys, PRE-MAIN/current reports, semantic registry, production code, actor state,
parent-genealogy issuing authority, prior C0R HOLD contents.

**No self-acceptance. No automatic K9/K10 dispatch. No semantic adoption.**
Independent High/I2 review follows this author return.
