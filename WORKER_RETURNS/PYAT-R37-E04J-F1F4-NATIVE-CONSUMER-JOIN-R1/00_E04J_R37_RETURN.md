# PYAT R37 E04JR — the REAL M1→M2→B5→I4→E04 consumer join

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

**Prior state closed.** The previous E04J packet recorded: Phase A native court
**STAGED ONLY / NOT EXECUTED**, and the learned-product join **NOT BUILT / NOT
EXECUTED**. Both are now physically executed.

**Verdict: `E04JR_SOURCEFREE_LEARNED_PRODUCT_JOIN_EXECUTED__I2_REVIEW_REQUIRED`**

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

## 2. Phase B — the real lifecycle join (built, not just imported)

The prior gap was that the E04 `GenericProgressiveProvider` computed directly from its
synthetic C1/N10E/I03 source and **never dereferenced M1/M2/B5/I4 releases**.
Importing those owners separately would not close the join. This return builds the
**smallest lawful source-free bridge** (`e04j_lifecycle_bridge.py`) that:

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
4. re-runs the **original E04 `NONPARENT_OPTIONS`** consumer so its `values_read` is
   observed against the B5-selected release.

Owner code is never reimplemented or replaced. Every returned object identity is the
owner's own.

### Evidence the join is real (per config)

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

B5's `selected_release_ref` **equals** the M2 `release.ref` in both configs — the
selected release is the exact learned release I4 dereferenced, and the consumer output
is bound to it. The differential carries through **every** lifecycle object and the
consumer receipt.

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
(denominator 8) yields base `{0:2,1:6}` → same-marginals `{0:1,1:7}`; the change
propagates through the real fact → M1 → M2 → B5 selection → E04 consumer receipt.

**What changes:** E04 empirical fact, M1 disposition, M2 release, B5 selection, source
universe identity, consumer empirical step and consumer receipt hash.

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

* **Risk denominator** — reported as 8 with 8 denominator member refs; not substituted.
* **Minority alternative** — retained with support, not pruned.
* **Same-respondent joint** — denominator-member based; no cross-person link invented.
* **Cross-person identity** — never claimed; `route_probability` stays `None`.
* **No-support vs missing artifact** — support loss yields a typed no-support /
  unavailable state, not a fabricated null; an empirically measured null remains a
  positive product only after competent measurement.
* **Wrong condition role** — refused, not guessed.
* **Current vs historical selection** — invalidation flags the old receipt for fresh use
  while historical evidence stays intact.
* **Missing immutable release / wrong release root** — compose with absent M1
  disposition is `BLOCKED`, `m2_release_ref is None`.
* **Cold replay / stale evidence** — replay `REPLAY_VERIFIED`; a second independent join
  re-derives the identical selection.
* **F4 / I05 boundary** — honest: the join proves the learned product reaches E04; it does
  **not** by itself claim I05 recursion or F4 co-travel success.

---

## 5. Execution summary (four separate courts, real pytest)

| Court | Cases | Result |
|---|---:|---|
| Phase-A independent anti-drop oracle | 6 | **6 pass** |
| Phase-A native E04 consumer court (inherited, unchanged) | 7 | **7 pass** |
| Phase-B lifecycle-join science | 6 | **6 pass** |
| Hostile boundaries | 10 | **10 pass** |
| **Total** | **29** | **29 pass, 0 fail** |

Full JUnit: `evidence/e04j_full_junit.xml`. Exact lifecycle object identities:
`evidence/lifecycle_object_identities.json`. Sanitized environment passport:
`environment_passport.json`.

**OpenCode quota / billed usage:** **UNKNOWN** — not measurable from inside this bounded
session; reported UNKNOWN per cost policy rather than guessed.

---

## 6. Honest limits and prohibitions

* The join is a single discovered product through one lifecycle. It is **not** an
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
| `tests/test_e04j_lifecycle_join_science.py` | Phase-B science court |
| `tests/test_e04j_join_hostiles.py` | hostile boundary court |
| `tests/test_e04j_native_original_consumer_join.py` | Phase-A native court (unchanged) |
| `tests/test_e04j_independent_no_drop_oracle.py` | Phase-A independent oracle (unchanged) |
| `evidence/e04j_full_junit.xml` | full 29-test JUnit |
| `evidence/lifecycle_object_identities.json` | exact M1/M2/B5/I4/E04 object identities, both configs |
| `evidence/phase_a_import_receipts.json` | imported module `__file__` + Git blob receipts |
| `evidence/native_e04j_junit.xml` | Phase-A native court JUnit |
| `environment_passport.json` | sanitized environment passport |
