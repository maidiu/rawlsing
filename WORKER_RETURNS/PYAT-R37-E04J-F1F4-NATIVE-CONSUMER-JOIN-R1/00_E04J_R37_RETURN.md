# PYAT R37 E04JR — M1→M2→B5→I4 lifecycle execution, and a BOUNDED HOLD on the E04 consumer join

> ## ⚠ READ THIS FIRST — a prior completion claim in this return is WITHDRAWN
>
> An earlier revision of this document claimed the E04 consumer "consumes the learned
> release selected by B5/I4". **That claim was not supported and has been withdrawn.**
>
> The truth, established by test and by mutation: the lifecycle executes genuinely on the
> real E04 `EmpiricalFact`, but it runs **beside** the consumer, **not into** it. The
> consumer receipt contains no reference to the M2 release, the B5 selection, or the M1
> disposition, and the consumer serves a `PROVIDER_CACHE_READ` populated before the
> lifecycle ran. The two subsystems are joined by adjacency in a Python function, not by
> data flow.
>
> **Verdict: BOUNDED HOLD**, not completion. See `evidence/owner_boundary_hold.json` and the
> owner-boundary court in `tests/test_e04j_lifecycle_join_science.py`.
>
> One test from the earlier revision,
> `test_consumer_uses_the_b5_selected_learned_release`, was **named** for a join its
> assertions never checked. It has been superseded. Do not read that test name as evidence.

**Role.** Existing bounded source-free E04J integration implementer. **NOT** HQ,
**NOT** an independent reviewer, **NOT** the original survey/source issuer, **NOT** a
Field Forge issuer, **NOT** an actor. Independent I2 review follows.

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Branch | `agent/rabochii-pyat-r37-e04j-f1f4-native-consumer-join-r1` |
| Exact return head at start | `9ef085adb1e1fa0f8eede9ff7240ad9630c6998d` |
| Original base | `68873526efe5a39a0849aa401666ac997870f156` |
| Prior E04J return | same branch at `9ef085adb` (PARTIAL / JOINED-LEARNED-PRODUCT HOLD) |

**Prior state partially closed.** The previous E04J packet recorded: Phase A native court
**STAGED ONLY / NOT EXECUTED**, and the learned-product join **NOT BUILT / NOT
EXECUTED**.

* Phase A native court: now genuinely executed, **7/7 pass**.
* Learned-product join: the **lifecycle half is executed** (M1→M2→B5→I4 on the real E04
  fact, both configs, all `RULE_SATISFIED`). The **consumer half is NOT built** — see the
  banner above.

**Verdict: `E04JR_LIFECYCLE_EXECUTED__CONSUMER_JOIN_BOUNDED_HOLD__I2_REVIEW_REQUIRED`**

The earlier verdict `E04JR_SOURCEFREE_LEARNED_PRODUCT_JOIN_EXECUTED__I2_REVIEW_REQUIRED`
is **withdrawn as overstated**: it implied a consumer join that does not exist.

---

## 1. Phase A — the existing native test now executes cold

Command (from the return root, with the root `rawlsing_next` package and
`runtime/` on `PYTHONPATH`):

```
PYTHONPATH="$PWD:$PWD/<ROOT>/runtime" python3 -m pytest -q \
  <ROOT>/tests/test_e04j_native_original_consumer_join.py
```

**Result: 7 passed.** This is a real cold execution against the qualified import
closure — not a staged-only claim.

Imported modules and their exact Git blob preimages (all inside this return's
`runtime/` or the pinned repository root; **0 ambient leaks**):

| Module | Git blob | Location |
|---|---|---|
| `product.service` | `facf1c8691` | `runtime/product/` (retained E04) |
| `product.nonparent` | `2181b832d3` | `runtime/product/` (retained E04) |
| `product.scenario` | `b7e568166c` | `runtime/product/` (retained E04) |
| `product.world` | `06a74caebd` | `runtime/product/` (retained E04) |
| `product.empirical` | `475feb9f9a` | `runtime/product/` (retained E04) |
| `rawlsing_next.pre553_n9_n10w_progressive_candidate` | `84d4041475` | `runtime/aux/` (E03, from `5eb51c686…`) |
| `rawlsing_next.pre553_empirical_query` | `03facecf708` | repo root (pinned) |
| `rawlsing_next.pre553_analytical_composition` | `604c8d591d` | repo root (pinned) |
| `rawlsing_next.pre553_empirical_possibility_provider` | `23167aa252` | repo root (pinned) |
| `rawlsing_next.pre553_empirical_authority` | `ca65a7fd4d` | repo root (pinned) |

The existing staged imported closure was **reused and verified, not reconstructed**
(cost policy). The base consumer receipt hash (`52e10a2f…`) cross-checks against the
independently retained E04 native receipt.

---

## 2. Phase B — real lifecycle execution; consumer join NOT built

The prior gap was that the E04 `GenericProgressiveProvider` computed directly from its
synthetic C1/N10E/I03 source and **never dereferenced M1/M2/B5/I4 releases**.
Importing those owners separately would not close the join — and, as this return now
establishes, **the consumer half cannot be closed from inside this worker's scope at
all**. This return builds the **smallest lawful source-free bridge**
(`e04j_lifecycle_bridge.py`) that:

1. executes the **genuine E04 native producer** and re-derives the exact
   `EmpiricalQuerySpec`/`EmpiricalPredicate` it used, then re-executes
   `execute_empirical_query` to obtain the **real `EmpiricalFact` object** whose ref
   equals the E04 `producer_fact_ref` (asserted);
2. wraps those exact objects in the minimum lawful `DiscoveryAuthority` +
   `DiscoveryResultReceipt` + M1 input bundle the M1 owner requires — using the
   **genuine E04 I03 authority snapshots** from the E04 registry so every object's
   authority closure resolves (no forged facts);
3. calls the genuine **M1** `adjudicate_learned_empirical` → `M2`
   (`register_producer_subject`/`constitute_release`) → **B5**
   (REGISTER/PUBLISH/SELECT_CURRENT + audit replay) → **I4** `compose_learned_world`
   (`route=M1_M2_B5`);
4. re-runs the **original E04 `NONPARENT_OPTIONS`** consumer.

Owner code is never reimplemented or replaced. Every returned object identity is the
owner's own.

> **Step 4 does NOT complete a join.** The consumer is re-run, but it is not fed the
> B5-selected release — it has no parameter to receive one (see
> `evidence/owner_boundary_hold.json`). The lifecycle in steps 1-3 and the consumer in
> step 4 are two subsystems that both happen to read the same source. This is the
> bounded HOLD.

### Lifecycle object identities (per config)

| Stage | Base config | Same-marginals config |
|---|---|---|
| E04 `EmpiricalFact` (real native) | `sha256:5cc84da4…` | `sha256:8459e878…` |
| M1 disposition | `RULE_SATISFIED` `sha256:8f42130d…` | `RULE_SATISFIED` `sha256:f9919e52…` |
| M2 release | `sha256:7caba105…` | `sha256:9a2ca348…` |
| B5 current selection | `sha256:57ac7cc1…` | `sha256:2e70fb70…` |
| B5 selected release | == M2 release | == M2 release |
| B5 replay | `REPLAY_VERIFIED` | `REPLAY_VERIFIED` |
| I4 terminal state | `RULE_SATISFIED` | `RULE_SATISFIED` |
| E04 consumer receipt hash | `52e10a2f…` | `0bc36b68…` |
| Consumer final step (Y\|A,B,C=1) | `{0:2, 1:6}` | `{0:1, 1:7}` |

B5's `selected_release_ref` **equals** the M2 `release.ref` in both configs. Read this
precisely: it is an **internal** consistency property of the lifecycle. The selected
release is the exact learned release I4 dereferenced **within the lifecycle**.

> **It does NOT follow that the consumer consumes it — and it does not.**
> The consumer receipt contains no reference to the M2 release, the B5 selection receipt,
> or the M1 disposition. The consumer independently re-derives its empirical support from
> the native source (`REL-e04-base-r1`) and serves a `PROVIDER_CACHE_READ` populated before
> the lifecycle ran. The differential changes every lifecycle object **and** the consumer
> receipt, but these are two independent consequences of the same changed source — **not** a
> single causal chain from the release into the consumer.
>
> The earlier wording here read "the consumer output is bound to it. The differential
> carries through **every** lifecycle object and the consumer receipt." That wording
> implied a join that does not exist. It is withdrawn. See `evidence/owner_boundary_hold.json`.

Conservative effects are correct and unchanged: `consumer_permission_effect`,
`structural_admission_effect`, `causal_truth_effect`, `field_forge_effect`,
`actor_v3_effect`, `source_or_carrier_retirement_effect` are all `False`.

---

## 3. Scientific positive

**Two independent 8-respondent source-local configurations, equal A/B marginal totals,
differing same-respondent joint distributions.**

*Source-local fixture oracle (Phase A, independent, frozen):* two 8-record configs with
identical marginals (A=1: 4, B=1: 4) but different joints — concordant
P(B=1|A=1)=**1**, minority P(B=1|A=1)=**3/4**. Equal marginals cannot substitute for
joint evidence; replay digests differ; minority support is not flattened. **6/6 pass.**

*Native lifecycle carrier (Phase B):* the E04-authorized forward query `Y|A=B=C=1`
(denominator 8) yields base `{0:2,1:6}` → same-marginals `{0:1,1:7}`. The change
propagates through the real fact → M1 → M2 → B5 selection (**within the lifecycle**).
The consumer receipt changes too, but **as an independent consequence of the same changed
source**, not as a result of the lifecycle feeding it.

**What changes:** E04 empirical fact, M1 disposition, M2 release, B5 selection, source
universe identity, consumer empirical step and consumer receipt hash.
**What is *not* shown:** any causal path from the selected release into the consumer.

**What properly remains invariant:** target-share denominators (8 in both),
structural routes, `route_probability = None` with
`NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL`, all conservative authority effects.

The E04 fixture authorizes only `Y|A,B,C` (forward) and separately-granted reverse
`A|Y`; `B|A` is **refused** (`TARGET_CONDITION_ROLE_AUTHORITY_UNAVAILABLE`). So the
lifecycle carrier uses the authorized `Y|A,B,C=1` grain while the 1→3/4 relation is
demonstrated by the independent source-local oracle at its own authorized grain. Both
are lawful; they are different queries and are reported as such.

---

## 4. Challenged boundaries (hostile court, 10 tests)

All ten now assert **direct, falsifiable facts** looked up from the native objects —
no conditional or `or True` fallbacks.

* **Risk denominator** — `denominator == 8`, `denominator_member_refs` length 8,
  `risk_set_ref.object_id` ends `R_ALL`.
* **Minority alternative** — the `0` cell survives with support ≥ 1 and
  `uncertainty != NO_SUPPORTED_EVIDENCE`.
* **Same-respondent joint** — every denominator member is a distinct
  `C11Internal:RespondentIdentity`; member count equals denominator, so no respondent is
  double counted and no abstract count stands in for the joint. (The native step exposes
  no `same_respondent_joint_ref`; this is the genuine same-respondent basis.)
* **Cross-person identity** — measure is `RAW; unweighted; no causal inference`,
  `dependencies == ['empirical']`, single source universe, `actor_executions == 0`,
  `model_calls == 0`, `new_issuer is False`, `route_probability is None`.
* **No-support vs fabricated null** — support loss gives
  `PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT` / `PARTIAL_TYPED_EMPIRICAL_SUPPORT` with the two
  shallower steps `EXACT_SUPPORTED` and the deepest step `ZERO_SUPPORT`, denominator `0`,
  `NO_SUPPORTED_EVIDENCE`, `cells == []` — a typed zero-support, never a manufactured 0/0.
* **Wrong condition role** — `B|A` raises `TARGET_CONDITION_ROLE_AUTHORITY_UNAVAILABLE`.
* **Current vs historical selection** — invalidation puts the exact consumer receipt hash
  in `invalidated_for_fresh_use`, the post-invalidation snapshot hash genuinely differs,
  and `historical_receipts_retained is True` with the hash still in `old_receipt_hashes`.
* **Missing immutable release / wrong release root** — compose with absent M1 disposition
  is `BLOCKED` with `m2_release_ref is None`.
* **Cold replay / stale evidence** — replay `REPLAY_VERIFIED`; a second independent join
  re-derives the byte-identical selection ref.
* **F4 / I05 boundary** — precise and falsifiable: on the `M1_M2_B5` route the I4 receipt
  has `route_taken == "M1_M2_B5"` and `m01_execution_receipt_ref is None` and
  `m01_object_graph_ref is None`, so **no M01/I05 recursive evidence was consumed**; the
  `semantic_ceiling` explicitly withholds `NO_PRODUCT_RELEASE`, `NO_CURRENTNESS`,
  `NO_STRUCTURAL_ADMISSION`, `NO_CAUSAL_PROMOTION`, `NO_PERSON_OR_V3_STATE`.

### Mutation check — are these guards load-bearing?

Deliberately breaking a pinned runtime source and confirming the suite fails
(`evidence/hostile_mutation_check.json`; runtime restored from git, blobs re-verified):

| Mutation | Result |
|---|---|
| `route_probability=None` → `0.5` (fabricate a merged cross-person probability) | **10 failed — guard bites** |
| positive-branch `state` → forced `EXACT_SUPPORTED` | **equivalent mutant — inconclusive, claim WITHDRAWN** |
| `consume()` gains a `release_ref` parameter | **boundary test 1 FAILS — bites** |
| consumer gains a third `values_read` channel | **boundary test 2 FAILS — bites** |
| selected release stamped into consumer receipt | **boundary test 4 FAILS — bites** |

**Correction to the previous revision.** That revision reported the second mutation as "a
real, disclosed coverage gap". **That was wrong.** `consumed.result_state` already
evaluates to `'EXACT_SUPPORTED'` on every supported step, so hardcoding it was a **no-op** —
an equivalent mutant. A byte-identical output diff confirmed zero divergence. A test cannot
be blamed for failing to catch a mutation that changes nothing. **No coverage gap is claimed
anywhere in this return.**

**Second correction.** Two boundary mutations were initially reported as "did not bite".
Those runs were invalid: the anchor strings did not match the source, so the edits never
applied and the "passed" runs were baseline re-executions. Re-run with verified anchor
assertions, both bite. Recorded because the failure mode — reading a pass from a mutant
that was never written — is exactly what a mutation check exists to prevent.

**Net position:** four biting mutations, one withdrawn as equivalent.

---

## 5. Execution summary (four separate courts, real pytest)

| Court | Cases | Result |
|---|---:|---|
| Phase-A independent anti-drop oracle | 6 | **6 pass** |
| Phase-A native E04 consumer court (inherited, unchanged) | 7 | **7 pass** |
| Phase-B lifecycle-join science | 12 | **12 pass** |
| Hostile boundaries | 10 | **10 pass** |
| **Total** | **35** | **35 pass, 0 fail** |

Phase-B grew from 6 to 12: six **owner-boundary** tests were added, and the two
overclaiming join tests they replaced were removed. The boundary tests assert the HOLD
*holds* and are deliberately falsifiable — an owner adding a release hook, a third read
channel, or release-borne evidence forces them to fail.

Full JUnit: `evidence/e04j_full_junit.xml`. Lifecycle object identities:
`evidence/lifecycle_object_identities.json`. Boundary evidence:
`evidence/owner_boundary_hold.json`. Sanitized environment passport:
`environment_passport.json`.

**OpenCode quota / billed usage:** **UNKNOWN** — not measurable from inside this bounded
session; reported UNKNOWN per cost policy rather than guessed.

---

## 6. Honest limits and prohibitions

* **THE CONSUMER JOIN IS NOT BUILT — bounded HOLD.** The lifecycle executes on the real
  E04 fact; the consumer does not consume the selected release. See the banner at the top
  and `evidence/owner_boundary_hold.json`. This is the headline limit of this return.
* The lifecycle runs one discovered product through one lifecycle. It is **not** an
  original35 source grant, not all-35 occupancy, not N11/N12.
* Statistical conditionals are **source-local empirical associations**, not causal
  mechanisms, not an independent person's propensity, not policy route probability.
* **K9/K10 NOT_RUN** — not a prerequisite to this join and not claimed.
* No original survey/source permission, production promotion, Field Forge semantics,
  model route probabilities, N11/N12, Sorok actors or V3. No self-acceptance.

**Independent I2 review follows.** This return is reviewer-ready author evidence, not
method adoption.

---

## 7. Artifacts

| Path | Contents |
|---|---|
| `00_E04J_R37_RETURN.md` | this document |
| `e04j_lifecycle_bridge.py` | smallest lawful source-free integration bridge |
| `tests/test_e04j_lifecycle_join_science.py` | Phase-B science court + **owner-boundary court** |
| `tests/test_e04j_join_hostiles.py` | hostile boundary court |
| `tests/test_e04j_native_original_consumer_join.py` | Phase-A native court (unchanged) |
| `tests/test_e04j_independent_no_drop_oracle.py` | Phase-A independent oracle (unchanged) |
| `evidence/e04j_full_junit.xml` | full 35-test JUnit |
| `evidence/owner_boundary_hold.json` | **BOUNDED HOLD** receipt: the four structural reasons the consumer join cannot close |
| `evidence/hostile_mutation_check.json` | mutation record, incl. two withdrawn corrections |
| `evidence/lifecycle_object_identities.json` | exact M1/M2/B5/I4/E04 object identities, both configs |
| `evidence/phase_a_import_receipts.json` | imported module `__file__` + Git blob receipts |
| `evidence/native_e04j_junit.xml` | Phase-A native court JUnit |
| `environment_passport.json` | sanitized environment passport |
