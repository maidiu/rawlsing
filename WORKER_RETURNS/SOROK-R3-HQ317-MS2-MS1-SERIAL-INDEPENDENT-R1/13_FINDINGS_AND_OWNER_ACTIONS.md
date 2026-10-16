# MS2 findings requiring revision

Source: MS1 d40cc32ecec8f681dcced6a482b6438a86080899, `runtime/ms1_serial.py`. These are review findings, not author repairs or issued semantics. All failures remain in the original frozen reviewer suite and first-run JUnit.

| Finding | Source location | First-run evidence | Required owner action |
|---|---|---|---|
| Formation ancestry is not validated | `_verify_memory_provenance`, lines137–165 | `evidence/new/observations/coherent_forgery_*.json`, four REDs | Verify exact native memory and transition congruence, nonempty event/source-feature refs and actual authorized predecessor; reject contradictions before ADP017 application. Current self-hash and ID presence are insufficient. |
| Contradictory stale permit overrides terminal native state | `consume`, lines255–284 | `evidence/new/observations/stale_permission_*.json`, three REDs, each REROUTE | Bind permission to verified selected canonical claim, exact terminal stance/access snapshot and native transition ancestry; recompute/verify the native permission value. A matching hash pointer is insufficient. |
| Unknown claim is promoted to valid absence | `consume`, absent-state branch | `evidence/new/observations/unknown_selected_claim.json`, one RED | Validate canonical selected-claim identity/source binding first; distinguish lawful bound absence from unknown selector. Preserve genuine C5/C6 EMPTY. |
| Accepted-law quote attributed to candidate comment | Original F7 and return legal-footing paragraph | `10_AUTHORITY_AND_DAG_LIMITS.json`; candidate `owner_transitions.py`163–164 | Correct attribution. Use accepted ADP017 belief gate and memory-interaction law without treating a candidate comment as an issued content rule. |
| Claimed response journal commit is absent | Prereg consumer description versus `consume` response return | All eleven per-cell responses have `committed=False`; no journal object/commit in consumer | Correct the claim or separately commission an actual transaction/journal implementation. Do not relabel a constructed response receipt as a commit. |

The first four memory attacks retain contradiction with the original native formation post-hash. Changed uncertainty alone and jointly changed feature content/uncertainty turn honest UNCERTAIN→DEFER into forged CERTAIN→REROUTE. The two other variants still create an epistemic transition despite invalid formation/source custody. The three stale-permit attacks retain the latest native withdrawal/supersession transition and its snapshot but overwrite permission; all produce an unearned REROUTE. They do not establish external signing, institutional custody or protected-store vulnerabilities; they show this fixture's exposed restorable owner state is insufficiently validated by the two hypothetical rule boundaries.

No claim that these failures arose during an honest native trajectory is made. Honest controls pass. The hostile question is whether a resealed but internally contradictory checkpoint can be consumed as though it were a native trajectory. The answer is yes in these cases. Either close that boundary or explicitly narrow the authority contract to separately trusted native store custody; this review cannot infer or grant that missing trust.

Preserve P3b and F_B exactly. The original global top gate is unsatisfied even after any implementation repair, because an honest UNKNOWN active/withdrawn pair still has no stance-only identifying contrast. Do not amend old predictions, hide the two original law-map failures, count DEFER as productive, or claim the hostile fixture findings invalidate all positive constructibility evidence.

The competent owner must separately specify a lawful serial rule contract:

1. Define exact source-memory classes, authorized source-bound content, native formation/transition ancestry and actor/world/effective-time scope. Keep hidden causal origin nonclaimable.
2. Specify a content→epistemic map and its uncertainty/accessibility policy, with owning rule ID/version/hash and issuer/destination authority. The current CERTAIN→ACCESSIBLE map is hypothetical; accepted generic interfaces do not supply it.
3. Bind exact actor-facing causal/acquisition evidence, canonical claim and private BELIEF ceiling. Memory references alone neither create a stance nor authorize KNOWLEDGE/public standing.
4. Validate actual predecessor and terminal native records across ADD, exact supersession, withdrawal and re-add; preserve valid UNKNOWN holds, bound NONE and lawful replay.
5. Define response-time selection, permission verification, response decision estimand and any productive commit/rollback/journal requirements. Owner-state nonmutation and receipt construction do not establish transaction durability.
6. Keep sourcefree finite constructibility, arm-specific causal effects, protected operational authority, empirical psychology and production feasibility separate. Independent review is an input to owner adjudication; no adoption is issued here.
