# RABOCHII 3 — PRE-MAIN RECONCILIATION WAVE 1 — PROJECT-ACCEPTANCE / AUTHORITY-SEMANTICS DISCOVERY R1

Status: `COMPLETE__FORENSIC__READ_ONLY_EXCEPT_REPORT__NO_MERGE_SET`

Repository: `maidiu/rawlsing`

Worker branch: `agent/rabochii-premain-w1-acceptance-semantics-r1`

Exact starting HEAD: `0777a34e50221bde6801dbaca26c058a7350c9e8`

Jurisdiction: acceptance / authority semantics only. No merge-set adjudication was attempted.

Sibling-blindness: preserved. No other `PRE_MAIN_RECONCILIATION_R1/WAVE1` worker artifact or result was inspected or consumed.

## 1. Mission holding

Rawlsing does **not** have a reliable project-wide acceptance vocabulary in which a filename or status token such as `FINAL`, `PASS`, `FROZEN`, `CURRENT`, `CANONICAL`, `PRODUCTION`, or `CLOSURE` can be read literally as project acceptance.

The repository instead exhibits a layered authority process. The same object can be:

- complete as a worker return;
- accepted as a bounded theorem by HQ;
- binding inside a subordinate campaign;
- historical/provenance authority but not current executable authority;
- current inside one authority family but not globally current;
- installed as bytes without gaining semantic authority;
- or superseded as current authority while remaining immutable historical evidence.

The decisive unit is therefore **claim + exact grain + jurisdiction + governing actor + exact object identity + lifecycle/current-selection state**, not the surface status word.

## 2. Evidence strategy

This was not a keyword-counting exercise. I reconstructed high-signal authority succession chains and compared what happened before and after claimed closure:

1. **main / PR / runtime baseline** — PR #125 and `main @ 0777a34e...`, where an R1 authority package was actually merged and wired into runtime/Postgres loading;
2. **worker-return -> HQ-bank chains** — G5/P1/P2-P4/P8/P10 under the central `agent/vozhd-to-vozhdy-inheritance-integration-r1` line;
3. **recovery-scope authority / supersession law** — `authority/semantic_relation_dag_recovery/`;
4. **current corrective HQ law** — Authorities 46 and 47 on the coordination line;
5. **subordinate campaign law** — `agent/subvozhd-current-joint-authority-r1-control`, whose own constitution explicitly distinguishes campaign adoption from HQ adoption;
6. **recent worker returns** — C06 R1 blocked, C06 R2 PASS, and J01-A R4 PASS/FROZEN, to test whether successful self-status alone produces project acceptance;
7. **portability / installation chain** — to test whether exact-byte recovery or installation itself constitutes semantic adoption.

Where no higher-layer banking/adoption was observed, I did not infer it from branch age, filename, branch naming, commit recency, or task-name success.

## 3. Core distinction: seven authority states

### A. Worker self-assertion

A worker can return `PASS`, `FROZEN`, `FINAL`, `CLOSURE_COMPLETE`, or a success token. This proves at most that the worker claims to have satisfied its commanded burden.

The P1 return is explicit: `P1_COURT_COMPLETE...` while P2-P4 remain blocked **until HQ accepts the return**. C06 R2 likewise returns a PASS token but is still a worker return. J01-A R4 returns `PASS__FROZEN` and says J01-B is releasable, but the worker itself does not execute or bank the successor court.

Rule: `WORKER_PASS != PROJECT_ACCEPTANCE`.

### B. HQ / adjudicator acceptance

Rawlsing's strongest acceptance act is an authorized higher-layer disposition that:

- identifies the exact submitted object (often by SHA/hash/ref);
- says `accepts`, `adopts`, `banks`, or equivalent;
- states the exact grain of the holding;
- states what is **not** thereby proved;
- and changes downstream authorization/dependency state.

Examples:

- `06_P1_HQ_ACCEPTANCE_AND_PARALLEL_CHILD_AUTHORIZATION.md` accepts P1 as post-G5 identity/property law, while denying implementation proof/live promotion.
- `07_P2_P3_P4_HQ_ACCEPTANCE_AND_NEXT_DAG.md` pins all three child returns, adopts their laws, and releases P5/P6/P7.
- `10_P8_HQ_ACCEPTANCE_P9_DISPOSITION_AND_P10_AUTHORIZATION.md` accepts P8 only after durable evidence sealing and independent cold verification.
- `11_P10_HQ_BANK_AND_G1A_TARGETED_CLOSURE_ROUTING.md` accepts P10 **as nonterminal** while explicitly refusing to pass G1A.

Rule: `HQ_ACCEPTANCE_IS_GRAINED`, not totalizing.

### C. Downstream consumption

Downstream use is strong corroboration that an upstream holding has entered a governing chain, especially when the consumer pins an exact upstream authority/ref and is itself authorized to consume it.

Authority 47 is inherited as binding by the Sub-Vozhd current-joint campaign. That campaign may consume the exact joined/admitted routing ledger at its proved grain. But downstream consumption cannot widen the authority ceiling: the Sub-Vozhd charter says `CAMPAIGN ADOPTION != HQ ADOPTION` and `IMPLEMENTED != ADMITTED`.

Rule: `CONSUMPTION_INHERITS_GRAIN; IT_DOES_NOT ENLARGE IT`.

### D. Project-current authority

Currentness is not chronology. Accepted P2 law explicitly rejects `LATEST`, timestamps, commit order, filesystem order, version-string order, fuzzy/default resolution, and absence of a newer row as current-selection authority.

Project-current authority requires one of two observed strong patterns:

1. **explicit governed current selection / binding HQ current law** within the relevant jurisdiction; or
2. **actual main/runtime installation and consumption** where the project has merged an authority into the executable machine.

PR #125 is the clean main/runtime case: merged to `main`, points loaders to the immutable R1 authority surface, enforces exact counts/fields, and reports runtime/Postgres validation. That is stronger than the word `FINAL_APPLIED` in the authority filename.

Authority 46/47 are the clean off-main central-governance case: explicitly corrective/binding HQ law, inherited by later campaign control. This proves that `main` is **not the sole possible carrier of project-current governance**, even though main integration is exceptionally strong evidence for current executable authority.

Rule: `CURRENT != NEWEST`; `CURRENT = EXPLICIT_GOVERNED_SELECTION_OR_LIVE_GOVERNED_CONSUMPTION_AT_THE_RELEVANT_GRAIN`.

### E. Provisional or partial closure

Rawlsing frequently accepts a theorem while refusing its larger task-name implication.

Examples:

- P1 accepted as identity/property law, no implementation proof.
- P4 carrier sufficiency accepted in principle, not live implementation.
- P8 accepted at property/exact-entailment level, no live architecture selection or retirement.
- P10 accepted as successful nonterminal anti-omission court, G1A still blocked.
- Authority 47 adopts C01 selective invalidation PASS but explicitly refuses `FULL_FRACTURE_MAP_FRESH_ADMISSION = PASS`.
- Authority 47 adopts current-ID accounting for C02-C05 but refuses to call that all current routing semantic authority.

This is the dominant meaning of `ACCEPTED_PARTIAL`.

### F. Explicit rejection

Rejection is a governed disposition, not merely lack of promotion.

Examples:

- R15/C4 bulk-negative and revoked pair-completeness mechanisms are `COMPOST` and explicitly prohibited from returning as live semantic truth.
- Authority 46 revokes the PostgreSQL-specific current zero-loss blocker inherited from prior wording.
- `EXACT_CANDIDATE_REJECT` means the exact proposed relation failed adjudication.

Critically, rejection does not automatically assert the opposite proposition. Accepted law states `REJECT != PROVEN_NEGATIVE`.

### G. Semantic supersession

Supersession requires explicit lifecycle/corrective authority. It is not inferred from a later date or later branch.

Examples:

- Authority 46 explicitly supersedes Authority 45 Section 8's PostgreSQL-specific requirement while retaining PR #27/G8 as historical deployment evidence.
- the seven R16F T06 IDs are predecessor authority and are not duplicate current edges beside the later strict source-first recertifications;
- R15/C4 may remain provenance/fixture material while losing current semantic authority.

Accepted lifecycle law requires typed succession/current selection and freezes `HISTORY_IS_IMMUTABLE`.

Rule: `SUPERSEDED_CURRENT != DELETED_HISTORY`.

## 4. What counts as Rawlsing project acceptance?

### Defensible acceptance rule

> **A Rawlsing claim counts as project-accepted only at the exact grain and jurisdiction for which an authorized governing layer explicitly admits/adopts/banks the exact identified claim or artifact, with required evidence preserved, and no later binding authority has revoked or superseded that holding. `ACCEPTED_CURRENT` additionally requires explicit governed current-selection or actual governed live/runtime consumption at that grain. Worker status words, chronology, filenames, installation, hashes, tests, or branch tips are corroborating evidence only and cannot by themselves promote authority.**

Operationally:

`PROJECT_ACCEPTANCE(CLAIM, GRAIN, SCOPE, T)` requires:

1. **Exact object identity** — ref/path plus pinned commit/hash/version sufficient to know what was admitted;
2. **Jurisdictionally authorized disposition** — the accepting actor is empowered to adopt at that grain;
3. **Explicit acceptance semantics** — adopt/bank/accept/binding disposition, not mere worker self-report;
4. **Evidence sufficiency required by that court** — including durable sealing/cold replay where the governing law demands it;
5. **Scope/grain boundary** — explicit nonclaims/stop laws survive acceptance;
6. **Lifecycle check** — no later binding corrective/superseding authority has displaced the claim at the same grain;
7. **For currentness** — explicit governed current selection or governed executable/current-consumer binding. Recency is forbidden as a substitute.

### Evidence hierarchy

From weakest to strongest:

1. token/filename (`FINAL`, `PASS`, `FROZEN`, `CURRENT`, etc.);
2. worker proof/receipt/test result;
3. exact durable return sealed for review;
4. authorized campaign-level admission at exact grain;
5. HQ/adjudicator bank/adoption at exact grain;
6. authorized downstream inheritance/consumption of that exact admitted holding;
7. explicit current-selection or live/runtime integration for the exact governing jurisdiction.

Higher evidence never widens the grain beyond what the accepting court actually adopted.

## 5. Classification law used in this return

- `ACCEPTED_CURRENT` — explicitly governed current authority at the relevant project jurisdiction, with current selection/live consumption and no observed superseder.
- `ACCEPTED_HISTORICAL` — authority/evidence remains accepted as historical predecessor, provenance, fixture, or replay truth but is not current governing truth.
- `ACCEPTED_PARTIAL` — explicitly accepted/binding only at a bounded theorem, campaign, property, evidence, or intermediate-court grain; larger/live claim remains unproved or blocked.
- `UNADJUDICATED` — return/proof/claim exists, but required higher-layer acceptance/current-selection has not been observed; `BLOCKED` normally lands here, not in `REJECTED`.
- `REJECTED` — explicit governing rejection/revocation/composting of the claim at the specified grain.
- `EXPLORATORY_NONBINDING` — discovery, reservoir, worker packet, exact-byte recovery, installation/provenance, or other surface explicitly denied authority-promotion power.
- `AMBIGUOUS` — evidence cannot safely determine the governing layer/grain or conflicting acceptance evidence cannot be resolved without another authority source. It is not a license to choose by recency.

## 6. High-value forensic conclusions for the later court

1. **Do not select branches by status words.** A branch saying `PASS`, `FINAL`, or `FROZEN` may still be an unbanked worker return.
2. **Do not select by recency.** Accepted law explicitly forbids recency as semantic current-selection authority.
3. **Do not make `main` the only sovereignty test.** Main/runtime merge is strong current-executable evidence, but central HQ coordination law can be binding project governance while work remains off-main.
4. **Do not equate installation with admission.** Exact-byte recovery and installation can remain provenance-only/nonsemantic.
5. **Trace worker -> bank -> consumer.** The strongest branch genealogy is not branch-name genealogy but authority-flow genealogy.
6. **Preserve partial acceptance.** A theorem accepted at property grain must not be promoted to full task-name closure during reconciliation.
7. **Preserve old accepted history when superseded.** Supersession changes current selection; it does not justify deleting predecessor evidence.
8. **Treat `BLOCKED` as unresolved, not rejected.** Reopening a blocker does not imply acceptance either.
9. **A `CURRENT.json` is scoped.** A current pointer inside a bounded authority family is not evidence of global currentness without a governing cross-scope adoption.
10. **Downstream consumers must be audited for exact pins.** Authority 47's rule that no later branch movement is implicitly consumed is a model for pre-main reconciliation.

## 7. Limits / nonclaims

- This return does **not** determine the final merge set.
- This return does **not** claim that every one of the repository's branches was exhaustively classified.
- No absence of an observed HQ bank is converted into proof that no such bank can exist elsewhere; such cases stay `UNADJUDICATED`/`AMBIGUOUS` as appropriate.
- This return does not reopen already accepted semantic holdings; it classifies their authority state for later reconciliation.
- This return does not consume sibling PRE-MAIN Wave-1 work.

## 8. Produced artifacts

- `00_WORKER_RETURN.md`
- `AUTHORITY_CLAIMS.tsv`
- `ACCEPTANCE_EVIDENCE.tsv`
- `STATUS_SEMANTICS.md`
- `AMBIGUOUS_ACCEPTANCE.tsv`

Terminal marker:

`W03_ACCEPTANCE_SEMANTICS_DISCOVERY_COMPLETE__ACCEPTANCE_IS_EXACT_GRAINED_JURISDICTIONAL_ADOPTION_PLUS_CURRENT_SELECTION_WHERE_CURRENT__NO_MERGE_SET`