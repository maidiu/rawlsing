# STATUS SEMANTICS — HOW RAWLSING AUTHORITY WORDS ACTUALLY BEHAVE

Status: `FORENSIC_SEMANTIC_MAP__NOT_A_NEW_AUTHORITY_COURT`

This file maps observed Rawlsing status vocabulary to the authority transitions actually evidenced in the repository. It is deliberately hostile to literal filename/status-token inference.

## 1. The governing principle

Rawlsing status is relational:

`STATUS_WORD + ACTOR + JURISDICTION + EXACT_OBJECT + CLAIM_GRAIN + ACCEPTING_PARENT + LIFECYCLE_STATE`.

Removing those operands makes the word unsafe.

Thus:

- `FINAL` does not mean project-final;
- `PASS` does not mean banked;
- `FROZEN` does not mean accepted;
- `CURRENT` does not mean globally current;
- `CANONICAL` does not mean globally sovereign;
- `CLOSURE` does not mean the task-name maximum is closed;
- `PRODUCTION` does not itself prove semantic authority;
- and physical installation does not prove admission.

## 2. Actor / layer model

### Layer W — worker / bounded court

Typical products: `RETURN`, `RESULT`, `RETURN_POINTER`, receipts, PASS tokens, frozen carriers.

Authority effect: evidence-producing. A worker may prove the burden assigned to it but cannot generally self-promote its result into parent/HQ authority.

Default classification before parent action: `UNADJUDICATED`.

### Layer C — subordinate campaign control / Sub-Vozhd

Typical products: campaign contract, worker authorization, exact sibling admission into a bounded campaign, campaign freezes.

Authority effect: binding **inside the delegated campaign jurisdiction**, but may be explicitly nonfinal relative to HQ. The current-joint campaign states this in constitutional form:

`CAMPAIGN ADOPTION != HQ ADOPTION`.

Default classification for an actually adopted campaign-local holding: `ACCEPTED_PARTIAL` unless the parent delegated final project jurisdiction for that exact claim.

### Layer H — HQ / central adjudicator

Typical products: `HQ BANK`, `HQ ACCEPTANCE`, `ADJUDICATION`, `BINDING` authority, exact disposition ledgers, next-DAG release.

Authority effect: strongest observed semantic/project-governance acceptance layer outside live executable merge. It normally pins exact child inputs and states exact holding/nonholding boundaries.

Classification: `ACCEPTED_PARTIAL` if the adopted grain is theorem/intermediate/property/historical only; `ACCEPTED_CURRENT` if the file constitutes current binding project law at that jurisdiction and has not been superseded.

### Layer M — main / live runtime

Typical products: merged PR, actual loader/reference change, runtime validation, installed authority packages.

Authority effect: strongest evidence of current **executable** project acceptance when the merge actually makes the claimed authority govern runtime behavior.

Classification: normally `ACCEPTED_CURRENT` for the exact merged/runtime grain, subject to later supersession.

Important: Layer M is not proven to be the exclusive carrier of project governance. The repository contains binding central HQ law off-main. Do not collapse semantic sovereignty into Git branch topology.

## 3. Vocabulary dictionary

### `RETURN`

Observed meaning: a child/worker has produced a result for a parent court.

Not sufficient for acceptance. Authority 47 states the rule directly:

`RETURN_EXISTS != RETURN_PROVES_TASK-NAME MAXIMUM`.

A return can be PASS, BLOCKED, or partial. Its presence says nothing by itself about parent banking.

### `PASS`

Observed meaning: the producing court claims its commanded proof burden passed.

Not sufficient for project acceptance.

Counterexamples:

- P1 return is court-complete while waiting for HQ acceptance.
- C06 R2 returns `PASS` and a success token; subordinate campaign consumption is observed, but central HQ adoption is not thereby automatic.
- tests can PASS while a court is BLOCKED (C06 R1).

Use PASS as proof evidence, then look for acceptance/banking.

### `ACCEPTED`

Observed meaning: strong when uttered by an authorized parent/HQ and attached to an exact child object/grain.

But `ACCEPTED` is not necessarily `CURRENT` or `COMPLETE`:

- P1 is accepted as identity/property law, not implementation proof;
- P8 is accepted at exact-entailment/property level, no live architecture choice;
- P10 is accepted as nonterminal while G1A remains blocked.

Therefore every accepted claim requires a **scope clause**.

### `ADOPTED`

Observed meaning: parent court incorporates a holding as governing law/input at a stated grain.

Authority 47 uses `Adopt:` followed by exact propositions and then immediately states prohibited promotions. That pattern is reliable: adoption is real, but only at the proposition actually adopted.

### `HQ_BANK` / `BANKED`

Observed meaning: a central parent has admitted a return into the governing campaign record after required verification. This is among the strongest semantic acceptance signals.

The P8 chain shows that a semantically persuasive return may still be **not banked** until durable evidence is sealed and cold-reopened.

`RETURN_RECEIVED != BANKED`.

### `FINAL`

Observed meaning: terminal relative to some artifact, worker sequence, or release family.

It is not self-authenticating project-finality.

The starting-main authority file contains `FINAL_APPLIED` in its filename, but its `ACCEPTED_CURRENT` status derives from PR #125 being merged and runtime loaders actually consuming/policing it—not from the string `FINAL`.

Rule: strip `FINAL` mentally, then reconstruct actor/grain/consumer.

### `FROZEN`

Observed meanings include:

- immutable input denominator;
- exact child tips frozen for a join;
- artifact/carrier freeze;
- terminal worker output freeze;
- historical semantic state freeze.

Freeze primarily means **do not mutate / do not drift the referenced object**. It does not necessarily mean a higher court has accepted the object's semantic claim.

J01-A R4 can be `PASS__FROZEN` while still requiring parent adoption.

### `CURRENT`

Observed meaning: must be explicitly governed and scoped.

Accepted P2 law is categorical:

- `CURRENTNESS_IS_EXPLICIT`;
- `LATEST` is not current-selection authority;
- timestamp/commit/filesystem/version ordering is not current-selection authority;
- absence of a newer row is not current-selection authority;
- `RECERTIFIES != CURRENT_SELECT`.

A `CURRENT.json` may identify the current release **inside one authority family**. It does not necessarily select global Rawlsing current truth.

### `CANONICAL`

Observed meaning: selected canonical representation/authority within a stated jurisdiction.

The semantic-relation recovery subtree calls itself a noncompeting companion authority and is canonical within recovery scope while explicitly not replacing full question-relation authority or gaining automatic live promotion.

Therefore:

`CANONICAL_IN_SCOPE != GLOBALLY_SOVEREIGN`.

### `PRODUCTION`

Observed risk: production/runtime terminology can tempt promotion from implementation fact to semantic authority.

Rawlsing's governing law repeatedly rejects this shortcut:

- `IMPLEMENTED != ADMITTED`;
- `RECOVERED CARRIER != EXECUTABLE AUTHORITY`;
- exact-byte installation is not semantic finding;
- a compiler may validate but may not invent source authority.

For reconciliation, treat `PRODUCTION` as a consumer/runtime-location clue. Require separate evidence that the semantics it executes were lawfully admitted.

### `CLOSURE`

Observed meaning: closure of the **named bounded court burden**, not necessarily the semantic maximum suggested by the branch/task name.

Examples:

- portability delta closes a forward portability blocker while explicitly not closing G1A;
- P10 is accepted nonterminal and opens more closure lanes;
- C01 repair can PASS while fresh full admission remains pending.

Rule:

`CLOSURE(COURT_GRAIN) != CLOSURE(PARENT_TASK_MAXIMUM)`.

### `BLOCKED`

Observed meaning: unresolved authority/proof state.

Accepted law freezes:

`BLOCKED != FALSE`.

`REOPENS_BLOCKED != ACCEPT`.

A blocked claim should normally be classified `UNADJUDICATED`, not `REJECTED`, unless a separate court explicitly rejects the proposition.

### `REJECTED` / `REJECT`

Observed meaning: exact proposed object/relation failed its adjudication.

Accepted law freezes:

`REJECT != PROVEN_NEGATIVE`.

Therefore rejection must not be silently transformed into truth-bearing negative authority.

### `SUPERSEDED`

Observed meaning: a later **explicit governing lifecycle/corrective disposition** replaces the current authority/function at the same grain.

Not equivalent to “newer file exists.”

Authority 46 is the model: it names the prior Authority-45 wording, explains why its semantic promotion was invalid, explicitly supersedes it, and preserves the old deployment as historical evidence.

Accepted lifecycle law also keeps history immutable. A predecessor may become `ACCEPTED_HISTORICAL` rather than disappear.

### `EXPLORATORY`, `NON-BINDING`, `PROVISIONAL`

Observed meaning: information can be useful, even exact, without being admitted as governing truth.

Examples include G0-G4 discovery/council work, recovery/materialization surfaces, historical reservoir material, and provisional denominators.

Do not promote these via richness, recency, exact bytes, or later convenience.

### `AUTHORIZED`

Observed meaning: permission to execute the next court, not evidence that the court's result already exists or will pass.

P9 may be deferred/not authorized while P10 is authorized. J01-A authorization predates its worker PASS. Authorization is dependency state, not acceptance of a future result.

## 4. Evidence that distinguishes the user's A-G categories

### A. Worker self-assertion

Look for:

- worker branch / role-native return;
- `RETURN_POINTER.json`, `RESULT.md`, success token;
- no later parent bank/adoption yet;
- return itself says “return to HQ” or children remain blocked until acceptance.

Classification: usually `UNADJUDICATED` even when PASS.

### B. HQ/adjudicator acceptance

Look for:

- explicit `HQ accepts`, `adopt`, `bank`, `binding`;
- exact child return/hash/ref pinned;
- independent hostile review/cold verification where required;
- exact holding and nonholding list;
- next-DAG state changed because of the accepted result.

Classification: `ACCEPTED_PARTIAL` or `ACCEPTED_CURRENT` depending grain/currentness.

### C. Downstream consumption

Look for:

- later authorized authority names the upstream law as parent/binding/admitted;
- exact upstream ref/tip/hash is pinned;
- consumer uses result only within inherited jurisdiction.

This is strong inheritance evidence, but cannot expand the claim.

### D. Project-current authority

Look for:

- explicit current-selection law/pointer within jurisdiction;
- binding central HQ authority inherited by later project-control work; and/or
- merged main/runtime code actually consuming the authority.

Never use latest branch/timestamp as substitute.

### E. Provisional or partial closure

Look for phrases that combine acceptance/pass with explicit stop laws:

- `accepted as ... level`;
- `nonterminal`;
- `in principle, not implementation`;
- `do not promote to ...`;
- next dependency remains blocked.

Classification: `ACCEPTED_PARTIAL` if a parent has accepted the bounded claim; otherwise `UNADJUDICATED`.

### F. Explicit rejection

Look for:

- `REJECT`, `COMPOST`, `REVOKED`, explicit invalidation/correction;
- exact grain being rejected;
- whether historical/provenance utility is separately retained.

Classification: `REJECTED` for the rejected claim, not for every fact in the artifact.

### G. Semantic supersession

Require:

1. exact predecessor claim/jurisdiction;
2. explicit lifecycle/corrective relation (`CORRECTS`, `RECERTIFIES`, `WITHDRAWS`, `CURRENT_SELECT`, etc.);
3. exact successor/current holding;
4. no recency inference;
5. predecessor history preserved unless separately authorized for retirement.

## 5. Acceptance rule for the later court

A later pre-main court should implement the following test per claim, not per branch:

1. **Identify exact claim grain.** What proposition/function/authority does this branch actually assert?
2. **Pin exact object.** Ref, tip/hash, artifact path, carrier identity.
3. **Identify actor/jurisdiction.** Worker, campaign, HQ, main/runtime.
4. **Find parent disposition.** Was it accepted/adopted/banked, merely received, blocked, rejected, or never adjudicated?
5. **Find downstream consumers.** Who inherited it, at what exact grain?
6. **Check current selection.** Is there explicit current selection or live governed consumption? Never infer from recency.
7. **Check supersession.** Has a later binding authority corrected/revoked/reclassified this exact claim?
8. **Preserve ceilings.** Do not promote evidence, historical provenance, tests, exact-byte recovery, or implementation above their stated jurisdiction.
9. **Classify.** Use the seven provisional classes in `AUTHORITY_CLAIMS.tsv`.
10. **Only later construct merge decisions.** Acceptance classification is evidence for the merge court; it is not the merge court itself.

Formal rule:

`ACCEPTED(C,G,S,T) = EXACT(C) ∧ AUTHORIZED_ADOPTION(C,G,S) ∧ REQUIRED_EVIDENCE_SEALED(C) ∧ ¬SUPERSEDED_AT(C,G,S,T)`.

For currentness:

`ACCEPTED_CURRENT = ACCEPTED ∧ EXPLICIT_CURRENT_SELECT_OR_GOVERNED_LIVE_CONSUMPTION`.

Notably absent from the formula:

`FINAL`, `PASS`, `FROZEN`, newest commit, newest branch, biggest file, most tests, or most confident prose.

## 6. Classification notes

### `ACCEPTED_CURRENT`

Use sparingly. Requires current-selection/live-consumption evidence or current binding central law with downstream inheritance.

### `ACCEPTED_HISTORICAL`

Use for predecessor/provenance/fixture/replay truth explicitly retained after current supersession or retirement of live authority.

### `ACCEPTED_PARTIAL`

Use for banked theorem/property/campaign-local authority where the parent explicitly limits scope or says larger/live state remains unproved.

### `UNADJUDICATED`

Use for PASS/FROZEN/COMPLETE returns awaiting parent acceptance, and for BLOCKED state.

### `REJECTED`

Use only where a governing disposition rejects/revokes/composts the exact claim. Do not infer opposite truth.

### `EXPLORATORY_NONBINDING`

Use where the artifact explicitly exists for research/recovery/provenance/discovery and cannot promote itself.

### `AMBIGUOUS`

Use when actor/jurisdiction/current-selection/supersession cannot be reconstructed well enough to choose another class. Ambiguity must survive rather than be resolved by branch recency.