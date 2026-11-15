# Strategy, economy, review and monitoring — ZAKONCHILOS research HQ

## Strategic diagnosis
The prior Browser/chat loop had three failures: the human was the scheduler; each small return induced a new prompt/review; and progress was inferred from expanding T×domain counts rather than a finite research deliverable. More agents and more PRs can magnify those failures. PR #1054 already establishes a sensible three-way ownership split and a 14-row *initial* seam registry. Reuse it. **Do not build another full controller, new architecture or 10th-format review process for this documentary phase.**

## The unit of work is a finite stratum, not the whole universe
A **stratum** = one specified historical source/version/branch family + related output/data-semantic family + relevant current recipient/consumer boundary (a finite enumerated search list). E.g. V550 indicator-distribution family→V551 bridge; V553 signed sparse temporal output→V554 actual reader; one current C11/I03 selected rule and separate Batch importing reader.

Before worker begins, write a one-paragraph finite scope and prior-evidence pointers. Define material expected answers and a bounded countersearch. At finish:
- what source files/commits and output records were inspected, including alternate paths and 404 recovery;
- what old T/S/M functions were identified or legitimately ruled out **within that stratum** and why the meaning matters;
- exact input→transform→output→positive/refusal→first reader (old and applicable modern), or clear `NOT_PROVED`;
- source/alias/owner collision, new evidence and actual obsolete/missing hypotheses challenged;
- what cells are FOUND / bounded NOT_FOUND / unresolved / uninspected / excluded;
- a peer omission challenge at independent source-reading level for the **stratum**;
- what remains outside the finite tract; queue a separate tract if newly discovered.
Mark `DONE_AT_SCOPED_SOURCE_SEARCH`, `HELD_EXACT_EVIDENCE`, or `NEEDS_INDEPENDENT_SEMANTIC_REVIEW`. Global `OPEN_DISCOVERY` can coexist with a properly finished tranche.

## Prioritize research value, not row volume
HQ uses a qualitative queue ordered by:
1. source/result that could change actual source→world→actor inference or accepted conservation (first-reader/actual output);
2. discovered contradiction that would misclassify a historical function as lost/superseded;
3. uninspected source stratum likely to hide an independent original T (branch/output/consumer-driven omitted-T search);
4. essential cross-agent alias/permission/denominator joins that unlock existing work;
5. inherited high-confidence source/reader mapping ready for bounded documentary closure;
6. routine format cleanup **only if broken references block use**.
Never award productivity for more TSV rows, report length, name changes, new review cycles, or intentionally increasing the provisional denominator. A new T is valuable only if a genuinely different knowledge-producing capability is supported.

## Economy: constrained concurrency and model routing
- Use **at most three OpenCode workers** in separate documents-only worktrees, one primary jurisdiction each. If two workers would do the same archaeology, reassign or temporarily idle one. HQ is the source-based integrator; no fourth full-time documentation agent.
- New independent reviewer **only at a substantively complete tranche / contested high-impact claim**, separate session/context from author, and legally independent credential where required. Author-side QA is not independent acceptance.
- Local source grep/git/log/registry join before expensive model analysis. Import existing #1046/#1048/#1045–#1054 receipts by immutable SHA. Reuse stable same-blob findings; verify only claim-specific disagreement.
- OpenCode is the requested **harness**, not a model or automatic paid account. Apply actual current user routing/availability law, including Browser suitability and DeepSeek V4.1-Flash MAX suitability if verified, GPT-6.1 High only when necessary, otherwise user-selected middle. Do not assert a model/provider/reasoning setting without runtime checks. Never silently substitute provider or consume unknown paid-overflow budget. If runtime model or financial grant is unavailable, pause only affected worker and ask the user ONCE for a material choice.
- **Budget:** record observed per-worker model, token/$ usage if actually exposed, retry count, source/privacy basis, queue. Require explicit financial ceiling prior to unattended paid runs. No hardcoded dollar amount, unlimited-quota assumption or speculative price/speed comparison.
- No CI, test harness, code execution, scientific run, production edit or new orchestration daemon. Non-scientific structural TSV/link/hash checks are documentary QA, not native proof.

## HQ supervision: check enough, not continually
HQ maintains `CAMPAIGN_STATE.md` or equivalent in the HQ **docs-only** branch:
`campaign_id, protected_sha, issue_and_pr_refs, per_agent{session_id_or_NOT_LAUNCHED, host, worktree, branch, observed_model, budget_status, last_seen, next_stratum, status, last_checkpoint_sha}, priority_queue, decisions, contested_seams, review_queue, source_strata`.
Never infer RUNNING from the existence of a PR. A PID/session/host may be verified locally only; otherwise `UNKNOWN`.

**Inspect at each material stratum checkpoint and once per day when a real supervising Codex host is operating.** Check:
- actual process, last event, session continuity, duplicate-write and branch safety;
- source claims can be opened at exact SHA/blob/line;
- meaningful old vs modern input/output/negative and real first reader rather than a similarly named guard;
- progress of finite source/consumer work and whether inherited evidence was reused;
- new original T recorded with primary owner and no double count;
- source-location 404 followed by broad recovery or useful clues;
- new turns obey no-test/no-engineering/provider/budget limits.
If no material delta twice on the same narrow issue, force ONE smaller discriminating source search or transfer; then park it `HELD`. Do not commission recursive hostile reviews to prove an unobservable native behavior; make an explicit unproved edge and continue other research.

## Review and cumulative integration
Workers author individual PRs/worktrees. HQ may read all, but is sole writer of the **central source-qualified seam index**. Freeze each candidate at an exact HEAD and integrate only documentary IDs and claims. No protected VMESTYE atlas acceptance by this research campaign.

At **substantive tranche group** (not every commit):
- independent reviewer chooses counterexample cases by *actual source*, alternate implementation, negative condition, different grain and reverse reader; not just validate the manifest;
- verdict `ACCEPT_SCOPED_S1` / `REVISE_EXACT_DEFECT` / `HOLD_EXACT_EVIDENCE` for the documentary return only, never global scientific/authority/protected adoption;
- HQ banks intact accepted subset, commissions targeted bounded correction where material, then resumes unrelated items without human relay. Inherited MCR obligations stay separate and are not self-discharged by this S1 scope.
- Conflicts: exact source A and B + divergent propositions + competent owner + least-cost falsifier; source-supported contradiction is not resolved by overwriting the oldest row.

## One daily human report (not three)
Use the same short structure, and suppress ordinary no-change chatter:
```
ZAK RECON HQ DAILY  |  protected <sha>  |  actual host/runtime <verified|unknown>
02 [running|queued|held]  last <sha>  stratum <name>  real new source finding <one sentence>
03 [running|queued|held]  last <sha>  stratum <name>  real selected-reader finding <one sentence>
04 [running|queued|held]  last <sha>  stratum <name>  real FF/world/actor finding <one sentence>
FINISHED: bounded source strata [names]; accepted at S1 [identities], NOT global %
DISCOVERY: new true T/grains [ids]; corrected false equivalences/absence [ids]
FIRST READERS: actual source-only vs executed [honest split]
OPEN: top 3 material evidence/authority holds; next source strata
COST/CAPACITY: [observed; otherwise UNKNOWN]
USER ACTION NEEDED: NONE | exactly one unavoidable decision with alternatives
```
If there is no material delta, a daily tick need not interrupt the user; keep state updated.

## Stop conditions and guardrails
- Workers finish a **bounded stratum** when their exact search set is qualified/held, its T/S/M and modern consumer comparison is intelligible and source-backed, and omission countersearch is done. No infinite 'search until every historical function ever discovered' loop.
- HQ finishes **the commissioned campaign** only when all authorized ZAK-02/03/04 source territories have defensibly bounded coverage, all acquired functions have typed dispositions/owner/first-reader status, the shared seam/alias join is coherent, independent documentary review has challenged omissions, and remaining outside-source or unexecuted science/authority proof is an explicit **held future commission**. No fake complete current machine.
- Suspend/seek user for a material provider/privacy/cost/auth decision or genuine stop order, not for ordinary GitHub file paths, reviewer fixes, more row filling or unambiguous source recovery.
