# Adversarial forgery and residual holds

**Scope:** independent sourcefree replay at `5b3e657…` with only the F2 two-blob overlay. No production, native, PRE-MAIN or author runtime was used. This document distinguishes a repaired content-preimage check from authenticity/completeness guarantees it does not provide.

## 1. Original RED and repaired GREEN

The original verifier `bp2p4/c12_verify.py` blob `b8e7cf397dbbbc37aa0a63ce9e0d7ba27a509cd3` excludes only `hash` from the episode preimage. `C12Store.append_episode` hashes the episode body and then appends `episode_id = TEST_ONLY_BP4_EP_ + hash`. On a real SAY row, the original verifier therefore returns:

```text
episode:0:body_hash_mismatch
```

The immutable focused test uses the same assertion and fails against that original blob. The repaired verifier `c1699c8d…` excludes `hash` and `episode_id` for episodes and separately requires the stored id to equal `TEST_ONLY_BP4_EP_` plus the body hash. The same test passes, and the full suite is 38/38.

This is a correct bounded repair of the original BP2P4JI `REVISE`; it is not native or acceptance authority.

## 2. Independent tamper and forgery probes

Probes were run by this reviewer against fresh `JoinedProduct` instances, not by transcription of the author return.

| Probe | Exact manipulation | Observed |
|---|---|---|
| Episode body tamper | Drop `episode_no_update`; rewrite `episode.body.event_id` | `ok:false`, `episode:0:body_hash_mismatch` |
| Episode id forgery / legacy form | Rewrite `episode_id` to `LEGACY_BP4_EP_<hash>` | `ok:false`, `episode:0:episode_id_mismatch` |
| World-event body tamper | Drop `world_event_no_update`; rewrite `summary` | `ok:false`, `world_event:0:body_hash_mismatch` |
| Cold reopen | Close and reopen `C12Store`; recompute chain and derived id | `ok:true`; hash, id and chain digest preserved |
| Injected world event | Raw insert a next-seq row whose body/hash are self-consistent | `ok:true`; injection accepted |
| Raw episode deletion | Drop `episode_no_delete`; delete the real episode | `ok:true`, `counts.episode == 0`; only unkeyed `chain_digest` changes |
| Fully rehashed episode forgery | Rewrite body, recompute body hash and derived id, update row hash | `ok:true`; forgery accepted |

The first four results confirm the intended narrow repair. The last three are residual HOLDs: content hashing verifies whatever preimage the writer supplied; it does not authenticate the writer or prove completeness.

### Injected world event

A fresh product was created, a SAY and `wait(30)` were executed, and a raw row was inserted at the next `world_event` seq with:

```json
{"event_id":"INJECTED_F2I_WORLD","clock":31,"summary":"raw injected world event","hash":"<digest of the preceding fields>"}
```

`verify_branch_chain(root)` returned `ok:true`, errors `[]`. The verifier checks body/column hash agreement and sequence contiguity only. It has no producer signature, world-event anchor or externally witnessed event set.

### Raw deletion

After a valid SAY, the append-only delete trigger was dropped and the episode row deleted. The verifier returned `ok:true` with `counts.episode == 0`; the episode count changed from 1 to 0. The unkeyed `chain_digest` changed from `72854b1f…` to `4d3e9452…`, but the verifier itself does not compare that digest to a trusted external copy. This is the author-acknowledged raw-SQLite/anchor HOLD, independently reproduced.

### Fully rehashed episode forgery

A valid episode was rewritten with a new `body.event_id`; the body hash, `episode_id` (`TEST_ONLY_BP4_EP_<new hash>`) and row hash were coherently recomputed. The verifier returned `ok:true`, errors `[]`; `chain_digest` changed from `fb7ea681…` to `a5d11db0…`. A simple id-only forgery is refused, but a fully self-consistent rewrite is not distinguishable from a legitimate row without an authenticated anchor.

### Upstream BP4

`bp4.store.C12Store.verify` was not repaired. On the valid episode it remains `ok:false` while the independent add-on is `ok:true`; `upstream_verify_defect(...).agrees == false`. This is the original BP4 self-referential defect, preserved as an owner HOLD.

## 3. Same-assertion source severance

The seven primary and three supplementary cuts were executed independently through `run_all_severances`. Every trial used `bp2p4.assertion.joined_downstream_a0_a2_assertion`:

| Edge | Baseline | Cut | Restored |
|---|---|---|---|
| BP2_C8_PROOF | red=false | red=true | red=false |
| BP2_ACTOR_HISTORY | red=false | red=true | red=false |
| BP2_RULE_A | red=false | red=true | red=false |
| BP2_RULE_T | red=false | red=true | red=false |
| BP2_TARGET_HASH | red=false | red=true | red=false |
| BP2_E2 | red=false | red=true | red=false |
| BP4_C10_M6_ACCESS | red=false | red=true | red=false |
| BP2_OTHER_HISTORY_ALIASED (supp.) | red=false | red=true | red=false |
| BP2_E2_NOT_PERFORMED (supp.) | red=false | red=true | red=false |
| BP2_PRACTICE_NOT_MATERIALIZED (supp.) | red=false | red=true | red=false |

`receipt.all_primary_proved == true` and `all_supplementary_proved == true`. The same consumer assertion is preserved; no assertion was substituted.

## 4. Preserved original negatives

- Original BP2P4JI `REVISE` remains the source review; this replay confirms the repair rather than erasing the review.
- The 33 original tests remain byte-identical and pass on the original tree; the focused test is the only intentionally added test.
- Episode body, episode id, world-event body and cold-reopen checks all remain red/green as claimed.
- The raw deletion, injection and fully rehashed forgery paths remain HOLD, not accepted as secure.
- No original test was disabled; the repaired JUnit has 0 skips, 0 errors, 0 failures.
- No native practice acquisition, original actor source, Rule A/T, C11/C12, production or external signer is established.

## 5. FINDING / INTERPRETATION / HQ ACTION / OWNER

**FINDING:** The F2 two-blob repair independently turns the exact valid-SAY RED into a same-assertion GREEN and preserves 33 baseline, 38 repaired, tamper, cold-reopen and 10/10 severance results. Content-only verifier limits remain: self-consistent world-event injection, fully rehashed episode forgery and raw deletion are accepted by `verify_branch_chain`; only an unkeyed chain digest flags the latter two as changed.

**INTERPRETATION:** The candidate is a correct minimal fix for episode hashing order. It is not an authenticated C12 custody system. The residual failures are outside the candidate's claimed preimage repair but material to any adoption claim.

**HQ ACTION:** Accept the engineering cut only as scoped sourcefree replay. Require original BP4/C12 owner decisions on upstream BP4 verification and the external anchor; require BP2P4J owner decision on the sole lawful episode-id derivation and legacy-writer support. Do not adopt on this return.

**OWNER:** Original BP2P4J verifier owner; BP4 C12 store owner; independent key/anchor custodian; Sorok HQ intake and separate post-return reviewer.

## 6. Limits and NOT_RUN

- No original survey/respondent data, native actor, CAN/ADP/SCI05, C11/C12, production deployment or external signed anchor.
- No original BP2 50-case or BP4 15-case suite rerun by this reviewer; the required 33+1+38 and independent probes were run.
- No owner adoption or merge.
- The author’s JUnit and logs were not used as this reviewer’s evidence; the embedded JUnit in `01_...json` is from this replay.
