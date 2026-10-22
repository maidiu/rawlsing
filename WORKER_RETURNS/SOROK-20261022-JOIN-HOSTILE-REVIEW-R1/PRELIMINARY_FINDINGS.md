# JOIN-V preliminary independent findings

**STATUS:** `PRELIMINARY_REVISE__ROOT_LINEAGE_AND_SOURCE_BINDING_NOT_PROVEN__AWAIT_JOIN_E_EXACT_SHA`
**CANDIDATE:** `13dfd6bad54ec19b4bdf31159e54fb6052d5440d`
**BRANCH:** `codex/sorok-join-v-20261022`
**WRITE SCOPE:** `WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/**`
**ROLE:** independent hostile reviewer, not JOIN-E, J, E, Sorok HQ or native authority.

## Verdict so far

The untampered single-root path does work: the candidate builds one J product root, enacts or omits A's material inspection, attaches the E first-session branch, refuses help after performed inspection, accepts help after omission, survives cold reopen, and preserves an independent attention surface. Ten independent positive tests pass.

The same-root lineage and persistence claims are not proven. Seven independent hostile tests fail on the frozen candidate. The candidate's `open()` trusts `session.json` for `product_root` and `branch_id`, and `R31JProduct.reopen()` accepts a plain R29P product root with no J binding. The reopened session can report `verify().ok=true` while the product root, branch, source and material state differ from the recorded session. One attack mutates the donor product's `bp2_join.json`.

The final candidate verdict is **PENDING** until HQ/human supplies the exact JOIN-E return SHA. This preliminary verdict is already sufficient to request a revision before final acceptance.

## P1. `open()` does not bind the product root or branch to the session

`joined/session.py:58-61` reads `meta["product_root"]` and `meta["branch_id"]` from the mutable session file and passes both directly to `R31JProduct.reopen()`. `meta["state_root"]` is never checked. `R31JProduct.reopen()` checks only `bp4_join_state.json` and `bp2_join.json`; it does not require `r31j_source`, `r31j_actor_snapshot`, or a `GM01_SOURCE` episode.

| Reproducer | Frozen candidate result | Expected |
|---|---|---|
| Create session A (`omit`) and session B (`e2`), rewrite A's `product_root` to B's product. | `open()` succeeds; product root is B; `meta.material_performance` still says `omit`; source `a_e2_performed=true`; tools `0`; `verify=true`; `do_help=false`. | Foreign or mismatched product root refused, or provenance mismatch reported. |
| Create a plain R29P `FirstSession` donor, point a JOIN session at that product root and `first_session` branch. | `open()` succeeds; `product.source={}`; `pre_c9_binding={}`; `verify=true`; `do_help=true`; donor's `bp2_join.json` is mutated with `r31j_source`, `r31j_actor_snapshot`, `r31j_c8_state_digest`, `r31j_e1_event_hash`, `r31j_target_id`. | R29P fallback refused; no mutation of a non-J root. |
| Fork branch `alt`, rewrite `branch_id` to `alt`. | `open()` succeeds on `alt`; `verify=true`; `do_help=true`. | Only the recorded sealed branch accepted; fork/substitution refused. |
| Move the session directory and open the moved path. | Raw `ValueError: R31J_TIME_COORDINATE_HOLD` because the absolute `product_root` points into the old location. | Either rebind to `state_root/product` or raise a typed session/root refusal. |

Minimal reproductions are `tests/test_join_v_hostile.py::test_different_product_root_is_refused`, `::test_r29p_product_root_is_refused_without_mutating_donor`, `::test_tampered_branch_id_is_refused`, and `::test_relocated_session_root_is_refused_or_rebound`.

The R29P result is the strongest counterexample: a session claiming `SOROK_SAME_PERSON_JOIN@1` opens with no J source and admits material help, while C12 verification still reports `ok=true`.

## P2. The persisted J source is not bound to the C12 `GM01_SOURCE` episode

`R31JProduct.reopen()` loads `r31j_source` from `product/bp2_join.json`, a mutable JSON sidecar. `JoinedSession.open()` then calls `verify()`, but the source is not compared with the `GM01_SOURCE` episode or any C12 digest. Tampering the sidecar changes the live `session.product.source` while C12 verification remains green.

Reproducer: start `omit`, edit `r31j_source` in `bp2_join.json` to `b_operation=REFUSE_TOOL`, `b_quantity=0`, `b_to_actor=TEST_ONLY_FOREIGN_ACTOR_A`, `b_actor=TEST_ONLY_FOREIGN_ACTOR_B`, then reopen.

Observed:

```json
{"opened": true,
 "loaded_b_operation": "REFUSE_TOOL",
 "loaded_b_quantity": 0,
 "loaded_b_to_actor": "TEST_ONLY_FOREIGN_ACTOR_A",
 "loaded_b_actor": "TEST_ONLY_FOREIGN_ACTOR_B",
 "episode_b_operation": "SHARE_TOOL",
 "episode_b_quantity": 1,
 "episode_b_to_actor": "TEST_ONLY_R31J_A",
 "episode_b_actor": "TEST_ONLY_R31J_B",
 "verify": true,
 "accepted": true}
```

The normal source uses R31J actor labels (`TEST_ONLY_R31J_A/B`), while the product actors are BP1 actors (`TEST_ONLY_BP1_R26V_ACTOR_A/B`). The candidate has no explicit source-actor-to-product-actor mapping or equality check. Whether the J labels are intended aliases or a separate namespace is not documented in the candidate; the foreign-label tamper is accepted.

A correct fix should treat the C12 `GM01_SOURCE` episode (or a digest bound by C12) as the source authority, or refuse a sidecar whose source differs from that episode. The sidecar must not be rewritable by `reopen()` before verification.

## P3. Typed refusal and partial-construction gaps

- `JoinedSession.open()` on a directory without `session.json` raises raw `FileNotFoundError`, not `SessionRefusal(SESSION_NOT_FOUND)`.
- `JoinedSession.start()` after `session.json` loss but with an existing product root raises raw `RuntimeError: R31J_PREC9_REFUSED:c8_exclusive_append:C8_OCCURRENCE_NOT_ADMITTED`. The root is not retried automatically, but the refusal is opaque and leaves an orphan product root.
- `JoinedSession.open()` on a relocated root raises raw `ValueError`, not a typed refusal.
- A crash between `_attach_new()` (which writes the R30A session metadata) and `_save_join_meta()` would leave a valid non-JOIN `session.json`; `start()` then refuses `SESSION_EXISTS` and `open()` refuses `WRONG_PRODUCT_LINEAGE`, leaving no automatic recovery path. This is inferred from the write order, not injected as a process-kill test.

These are hardening findings, not the primary acceptance blocker. The primary blockers are P1/P2.

## P4. The candidate's two-test oracle is too weak for the claimed edge

The candidate's own test asserts `session.product.source['b_performed'] is True`. B's `REFUSE_TOOL` record also has `performed=True`; the J source sets `material_feasible_after=False` and `b_quantity=0`. The assertion therefore does not prove that B shared the tool. The independent test `test_refusal_source_is_red_and_share_source_green` demonstrates both cases have `b_performed=true`, while `b_operation`, `b_quantity`, `material_feasible_after`, A's tool state and E admission distinguish them.

The candidate's test does not exercise:

- a foreign/missing product root or R29P fallback;
- a tampered branch;
- a tampered `r31j_source` sidecar;
- source-actor identity;
- missing/orphan/relocated session refusal;
- attention invariance on the same product state;
- B ignorance/offscreen, private boundary, contact/no-contact, cold reentry beyond one omission session.

The candidate's 2/2 passes are real for the narrow positive path, but they are not a denominator for the integration claims.

## Independent positives that pass

| Test | Result |
|---|---|
| `test_enacted_material_source_and_omission` | PASS |
| `test_performed_material_action_severs_and_new_omission_restores` | PASS |
| `test_refusal_source_is_red_and_share_source_green` | PASS |
| `test_same_root_source_identity_and_c12_episode` | PASS |
| `test_repeated_reopen_does_not_duplicate_gm01_or_checkpoints` | PASS |
| `test_cold_child_process_reopens_same_source_and_attention` | PASS |
| `test_attention_invariant_objective_speech` | PASS |
| `test_private_ignorance_and_b_offscreen` | PASS |
| `test_lawful_contact_and_no_contact` | PASS |
| `test_warm_and_cold_import_order_preserve_result` | PASS |

Details:

- Performed E2 consumes A's shared tool and E refuses help; omission preserves the tool and E accepts. A fresh omission restores the positive.
- B-refusal source (`b_operation=REFUSE_TOOL`, `b_quantity=0`, `material_feasible_after=false`) is RED at E; B-share source (`SHARE_TOOL`, quantity 1, feasible true) is GREEN.
- The normal source equals the C12 `GM01_SOURCE` episode; `pre_c9_binding` carries the B event ref/hash and `native=false`.
- Three in-place reopens do not duplicate GM01 episodes, events, checkpoints, or perceptions; counts remain `{episode: 3, world_event: 2, checkpoint: 6, perception: 6}` for the tested omission product.
- A cold child process reopens the same source, branch, root, attention and accepted help.
- With a byte-identical copied product, `focused` and `distracted` produce the same user event, speech event, contract hash and speech text; only the phenomenal surface gesture/ambient presentation differs.
- Private cash/intimacy probes use boundary strategies with `no_private_tokens=true` and `no_private_values=true`; after B moves to the market, A answers `UNKNOWN_B` rather than claiming B's offscreen activity.
- Contact is refused before help and granted after help; the performed-E2 session refuses both help and contact.
- Normal import order and E-first import order produce the same accepted help, source and C12 verification.

## Provenance and import closure

- Candidate source manifest: **444/444** vendored files match their recorded Git blobs; 0 missing, 0 mismatched. Candidate-owned files are outside that manifest as expected.
- Candidate files:
  - `joined/session.py` SHA-256 `0562fb0405cbe1f989ec10e4ce865c54bc712559757c877342fc1d1d46027956`
  - `tests/test_join.py` SHA-256 `ca57802caccce9d37547fb10f8c3df2595accb6b4e51d1d600d62b68153ca6fd`
  - `SOURCE_MANIFEST.json` SHA-256 `7cfcb4679e36b522e83cc7120dbc166ce61dd220099c2aca8f5c9ddb5252c126`
  - `RESUME_CHECKPOINT.md` SHA-256 `7c03d345bddb03bdb75e99a595dac68da9494890134f7db73c5b0002a63bcad2`
- Frozen test hashes are in `FROZEN_ORACLES.json`.
- Normal import resolves `bp4`, `bp2p4`, `r29p`, `r26e` from `vendor/j`; `r30a` and `r31e` from `vendor/e`. E-first resolves the common closure from `vendor/e/...`; common files are byte-identical (`bp4` `18de93276f6a35e0…`, `bp4.world` `848bb6d3e3e0375a…`, `bp2p4.product` `55c99dffb8cc7ab6…`, `r29p.product` `cf1882ace97ef30d…`, `r26e.c12_integrity` `534780fe4631caad…`), and the behavioural result is identical. No functional import-order contamination was found in the untampered path.
- Inherited suites, separate processes: R31J **8/8 PASS**, R31E **15/15 PASS**, R30A **10/10 PASS**. The candidate's own suite is **2/2 PASS**.
- Candidate test denominator remains 2 distinct tests; no inherited 155/202 or final JOIN-E cut was promoted.

## Cross-root observation (not counted as the primary failure)

Two fresh builds of the same frozen `omit` scenario in different roots had the same B/E1/C8 source hashes but different C9 target and consumed-state hashes, and could select different `EXPLAIN_WORK` template variants. In-place cold reopen preserves one root's target and speech. The candidate records only a commit-level `j_source_ref`, not a canonical source identity hash, so "same person" across newly built roots is not demonstrated. This is a residual identity/root question; it is not used to claim a hard failure because the commission's tested claim is same-root source/actor identity.

## Courts

| Court | Preliminary verdict | Ceiling |
|---|---|---|
| **ENGINEERING** | `PRELIMINARY_REVISE` | Positive single-root material/encounter path works; root lineage, branch, R29P fallback and sidecar source binding are not proven and two attacks mutate/accept foreign state. |
| **SCIENTIFIC** | `HOLD__NO_ISSUANCE` | Only TEST_ONLY sourcefree material/encounter behavior; no psychology, acquired practice, subjective personhood or A5 claim. |
| **AUTHORITY** | `HOLD` | No native CAN/ADP/C8/C12/Pyat/C11/C5, protected keys, external provider or human A5 grant. |

## Required revision before final acceptance

1. Bind `open()` to `state_root/product` and the sealed branch; reject foreign product roots, R29P fallbacks, branch rewrites and relocated roots with typed refusals.
2. Make `R31JProduct.reopen()` read-only and require a non-empty J binding plus a `GM01_SOURCE` episode; never write `r31j_*` fields into a donor root on open.
3. Treat the C12 `GM01_SOURCE` episode or a C12-bound digest as the source authority; reject a sidecar that disagrees. Bind source actor labels to the product/seed actor IDs or document and enforce the mapping.
4. Add typed missing-session, orphan-root and moved-root refusals; do not leave an opaque C8 failure after a failed/lost session.
5. Extend the author's oracle beyond `b_performed=true`: assert `b_operation`, `b_quantity`, `material_feasible_after`, source-to-episode equality, root/branch identity and the hostile cases above.
6. Re-run these frozen tests against the exact JOIN-E return SHA; final verdict remains `PENDING` until that cut exists.
