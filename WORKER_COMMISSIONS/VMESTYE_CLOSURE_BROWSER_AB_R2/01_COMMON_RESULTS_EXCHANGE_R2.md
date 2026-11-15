# COMMON RESULTS / MUTUALLY ENHANCING A/B STORAGE — R2

**One shared exchange, one canonical VMESTYE atlas, distinct author/reviewer branches.** This applies to all Browser A/B roles on existing #814/#815/#816/#817. It extends, rather than replaces, [last campaign's **Unified Functional Reconnaissance Logging R1**](https://github.com/maidiu/rawlsing/blob/e4aa144ce69fd943910accb923159e576e4db06e/WORKER_COMMISSIONS/ZAKONCHILOS_CODEX_HQ_RECON_CAMPAIGN_R1/REFERENCES/VMESTYE_ZAKONCHILOS_UNIFIED_RECONNAISSANCE_LOGGING_USER_SUPPLIED_R1.md): identical nine VMESTYE-facing core file names and four source/shape/mechanism/reverse-consumer supplemental register headers, case-by-case source provenance, negative and branch status, five separate quality/completeness judgments where applicable.

## A. Exact repository locations
**Shared exchange/intake namespace (one HQ documentary writer):**
`UNIFIED_LOG_R1/VMESTYE_CLOSURE_AB_R2/SHARED/`
on the nonprotected campaign branch `docs/vmestye-zakonchilos-browser-duels-r2-20261115` (or its explicitly designated successor). This namespace contains immutable frozen-author **pointers**, material source/claim disagreements, C1–C5 gate state and next stage dependencies. It is **NOT** the normalized VMESTYE function atlas and cannot accept any product/owner claims.

**Per-flight, per-side, per-phase documentary returns (one agent = one writer):**
`UNIFIED_LOG_R1/VMESTYE_CLOSURE_AB_R2/FLIGHTS/ZL15/<A|B>/<P0|P1|P2>/`
`UNIFIED_LOG_R1/VMESTYE_CLOSURE_AB_R2/FLIGHTS/ZL16/<A|B>/<P0|P1|P2>/`
`UNIFIED_LOG_R1/VMESTYE_CLOSURE_AB_R2/FLIGHTS/ZL17/<A|B>/<P0|P1|P2>/`
`UNIFIED_LOG_R1/VMESTYE_CLOSURE_AB_R2/FLIGHTS/P4R/<A|B>/<P0|P1|P2>/`
Each author/reviewer uses its **own isolated branch/draft PR**; the location strings are stable and joinable but **must not be concurrently written on the shared HQ branch**. In B's later stage, reference A's original `PR@40hex::path#blob:line` and claim IDs rather than copy the whole corpus.

**Only accepted canonical VMESTYE integration writer:** existing #814 ZL-15 A on draft [PR #864](https://github.com/maidiu/rawlsing/pull/864) or a clearly named noncolliding handoff branch after an explicit verified lease; full normalized `VMESTYE/DATA/{FUNCTION_ATLAS,OPERATION_TRACES,RELATIONS,EVIDENCE,AUTHORITY_APPLICATIONS,DECISION_EVENTS,IMPLEMENTATIONS,CONSUMER_EDGES}.tsv` remains the *sole authoritative candidate atlas*. The SHARED exchange has no right to mirror or overwrite the canonical atlas.

## B. Exactly how agents share without conflicts
1. HQ/commissioning custodian freezes the protected SHA and one **P0** source cut for each duel, lists it in `SHARED/FROZEN_RETURNS.tsv`, and verifies writer/branch exclusivity. A and B start **blind** from same source cut; no premature exposure of unpublished conclusions.
2. Each side publishes its individual source-graded `P0` return to its isolated PR, with immutable HEAD and exact paths, and posts the receipt to existing campaign issue. Until published, branch status remains **UNKNOWN** to unrelated agents.
3. Single HQ writer records **both** frozen P0 refs in `SHARED/FROZEN_RETURNS.tsv` and intake links/claim IDs in `SHARED/CLAIM_EXCHANGE.tsv`. Agents **read only** the pinned SHARED HEAD and opponent's immutable author HEAD; never commit to shared HQ branch or to opponent.
4. Each posts a **P1** adversarial `CONTESTS.tsv` and source-graded proof; HQ appends qualifying disputes to `SHARED/CONTESTED_CLAIMS.tsv`, distinguishing false positive, correction, acceptance at scope and held fact. Exact contradictory evidence remains preserved.
5. Each submits **P2** bounded rebuttal/correction; HQ updates disputes with `RESOLVED|PARTIAL|CONTESTED|HELD`, never silently deletes a negative. One routine exchange suffices; new material source/callsite evidence may justify a *named* scoped addendum but not default new A/B run.
6. HQ maintains `SHARED/C1_C5_GATE_STATUS.tsv`, `SHARED/SOURCE_RECOVERY.tsv` and `SHARED/FINITE_WORK_QUEUE.tsv` as **pointers to source-grade evidence**, never inventing a passed gate or verified running session. Real formal independent review/receiving occurs only in the existing #815/#816/#817 jurisdictions at the appropriate exact candidate head.
7. If HQ is unavailable, **individual PRs and issue comments are complete durable returns**. A side stops at `AWAIT_FROZEN_OPPONENT_RETURN` or `AWAIT_INTEGRATOR_HEAD`; it must NOT claim automatic synchronization or make the user retype finished evidence. The user (or actual connected HQ) may forward only the two immutable PR links to trigger exchange. Do not simulate a daemon.

## C. Common document/core package per side
For any substantive new original T or edge, use unchanged original R1 `FINDINGS.tsv`, `OPERATION_TRACES.tsv`, `AUTHORITY_USE.tsv`, `EVIDENCE.tsv`, `COVERAGE.tsv`, `UNJOINS.tsv`, `MECHANISM_RECONCILIATION.tsv`, `DATA_SHAPES.tsv`, `SOURCE_SEARCH_LOG.tsv`, `REVERSE_CONSUMERS.tsv`, `00_RETURN.md`, `HUMAN_STORY.md`, `SCOPE_CONTRACT.md`, `CHANGED_FILES.txt` and standalone `CASES/` **for genuine newly material T**. Literal columns/header/type per the linked R1; no per-agent novel schema. New refs/fields belong in R1 `EXTENSIONS.tsv`; never change 13 inherited headers to fit one user.
For a **review-only** Browser side, do not duplicate every existing T table or generate fake zero-coverage T rows. Return a `00_RETURN.md`, `SCOPE_CONTRACT.md`, `EVIDENCE.tsv` (R1 literal header), `SOURCE_SEARCH_LOG.tsv` (R1 literal header), `REVIEW_CASES.md`, `CONTESTS.tsv` (header below), `CHANGED_FILES.txt`, plus only materially relevant R1 delta files. This is a role-specific minimal compatible package; it does not relax any original issue output requirement. For #817 final court, also return its original five required documents in addition to the shared pointers.

## D. Stable ID and reference grammar
- Agent scope `ZL15:A`, `ZL15:B`, `ZL16:A`, `ZL16:B`, `ZL17:A`, `ZL17:B`, `P4R:A`, `P4R:B`; phase `P0|P1|P2`; each claim `VMCR2:ZL15:A:CLAIM:0001`, evidence `VMCR2:ZL15:A:EV:0001`, contest `VMCR2:ZL15:B:CONTEST:0001`. Source historic IDs must never be replaced with newly coined IDs or double-counted; stable prior T source ID remains referenced.
- Source tuple `<40hex commit>::<exact repo path>#<git blob SHA>:<line/row>`. A PR URL or `main` alone is not evidence. Include branch/protected/candidate grade as its own column or linked R1 evidence row.
- SHARED `FROZEN_RETURNS.tsv` has one row per **actually published** immutable P0/P1/P2 return. Do NOT seed with fictional sessions. Comparisons specify `target_return_id,comparison_basis_head`.
- A dispute must state *original proposition, exact conflicting source/evidence/negative, difference in semantic grain, decision impact, cheapest discriminator, owner and disposition*. If no material change to any functional/closure decision is possible, label `NON_DECISION_CHANGING` and do not commission another search.
- Original role reviews at #815/#816 may conclude `REVISE` without new T, without being counted as new historical functions. Reviewer B is an adversarial participant, not automatic credentialed independence or acceptance.

## E. SHARED TSV schemas — append only source-qualified rows
- `FROZEN_RETURNS.tsv`: `return_id,flight,side,phase,issue_number,author_pr_url,author_commit_sha,source_protected_sha,source_candidate_sha,return_root,grade,review_authorization,publication_status,submitted_at_utc,notes`
- `CLAIM_EXCHANGE.tsv`: `claim_id,return_id,primary_record_owner,prior_t_or_requirement_id,claim_kind,claim_short,evidence_ids,source_cut,source_grade,execution_grade,consumer_grade,authority_grade,other_side_reference,admission_status`
- `CONTESTED_CLAIMS.tsv`: `contest_id,target_claim_id,raised_by_return_id,challenge_type,contrary_evidence_ids,contradiction_or_missing_edge,material_closure_gate,alternative_outcomes,minimum_falsifier,competent_owner,status,response_return_id,decision_evidence_id`
- `C1_C5_GATE_STATUS.tsv`: `gate_id,canonical_integrator_head,source_estate_boundary,claimed_status,verified_supporting_claim_ids,independent_review_heads,typed_open_ids,possible_verdict,scope_limit,competent_reviewer,updated_at_utc`
- `SOURCE_RECOVERY.tsv`: `recovery_id,asserted_path,asserted_source_commit,lookup_failure,semantic_symbol_or_output,search_roots_and_branches,recovered_commit,recovered_path,recovered_blob,role_and_currentness,if_unfound_surrounding_clues,next_bounded_search,claim_evidence_id`
- `FINITE_WORK_QUEUE.tsv`: `task_id,closure_gate,underlying_t_or_authority_id,exact_unproved_edge,why_decision_changes,prior_search_scope,next_discriminating_check,competent_owner,required_permission,dependency,task_kind,priority,terminal_state`
- `WRITER_AND_EXCHANGE_STATE.tsv`: `flight,side,phase,branch,pr_url,claimed_session_id,session_verification,lease_owner,head_sha,exchange_head_seen,ready_for_peer,ready_for_receiving,notes`

These are **exchange metadata** only. Every accepted current semantic status remains exclusively in #814's canonical VMESTYE `DATA/` at its own source cut, with event sourcing and independent receiving.

## F. Finite economy, no artificial green
Prior accepted work is referenced, **not re-authored**. Historical search applies full broad path recovery to an actually material asserted source. No blind general 182/47/6125/2416/1314 recensus. A truthfully failed source lookup is a bounded negative and may trigger decision-changing recovery, never universal absence. A claim of `S2_PASS`, `ORIGINAL35` or `CURRENT_MACHINE_ZERO_LOSS` requires separate executed issuer-grade receipt; Browser reviewers cannot manufacture it.

**Output-quality checks:** links resolve at immutable SHA; selected rule content and negatives are distinct from role/hash; same-head reviews; overlap and aliases conserved; output/shape/consumer compare at exact grain; every C1–C5 hold has owner and next falsifier; no double-counted rows/unknown sessions; no editor sharing, forced merge or overwritten accepted negatives. The five R1 quality gates remain provenance, future utility, navigability, comprehensibility, comprehensiveness.

**If publication rights fail:** return full specified structured material in Browser chat and mark `NOT_COMMITTED`, naming intended path and exact blocked GitHub action. Do not fabricate a shared ledger update or sandbox artifact.
