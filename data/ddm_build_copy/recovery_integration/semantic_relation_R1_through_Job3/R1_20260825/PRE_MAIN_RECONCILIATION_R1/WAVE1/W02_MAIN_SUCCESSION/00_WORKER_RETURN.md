# RABOCHII 2 — PRE-MAIN RECONCILIATION WAVE 1
## MAIN / PR / PROJECT-SOVEREIGNTY SUCCESSION ARCHAEOLOGY R1

Repository: `maidiu/rawlsing`  
Worker branch: `agent/rabochii-premain-w1-main-succession-r1`  
Exact starting HEAD: `0777a34e50221bde6801dbaca26c058a7350c9e8`  
Mode: forensic / read-only with respect to all pre-existing branches  
Sibling discipline: PRE_MAIN_RECONCILIATION_R1 sibling returns were not inspected or consumed.

## Terminal verdict

Rawlsing did not undergo one clean `main -> replacement-main` handoff. It underwent a **progressive loss of single-trunk sovereignty**, followed by several operational reconstitutions of project authority on control/HQ/integration branches.

The earliest hard repository evidence that `main` had ceased to be the **unique cumulative trunk** is **2026-08-17T02:33:55Z**, when PR #28 (`W06-A: hostile source-wave identity acceptance harness`) merged into `agent/source-wave-identity-repair-integration`, not `main`. The enclosing campaign PR #27 (`Source/wave identity repair campaign`) was and remains an **open draft** against `main`; it never merged. PR #28's merge commit `7350f118395f677c62e4bc66ced579bcf8e7480d` is not an ancestor of current `main`: comparing that commit to `main` is `diverged`, with merge base `25a63e08b0fcf7ef3dfc9de0c7b03325d26d918a`, `main` 443 commits ahead and the PR #28 line 7 commits behind from that comparison direction. This makes the Aug. 17 split materially different from the earlier V550–V552J repair integration, which was explicitly merged back to `main` through PR #23.

`main` nevertheless remained an active and important sovereign stream for another ~40 hours. It continued receiving architecture and authority work, including PR #79, whose body explicitly recognized the dual-lineage state: `SWID G8/final merge remains an external production gate for V553 only; independent authority work can proceed in parallel.` The last commit ever added to `main` is PR #125 at **2026-08-18T18:52:29Z**, merge SHA `0777a34e50221bde6801dbaca26c058a7350c9e8`. As of this forensic run on 2026-08-30, the repository's `main` ref is still exactly that SHA. Thus:

- **functional cumulative-trunk break:** 2026-08-17T02:33:55Z, first proved accepted return merged into an off-main campaign trunk that never subsequently re-entered `main` as a lineage;
- **hard main freeze:** 2026-08-18T18:52:29Z at PR #125 / `0777a34e...`.

After the hard freeze, canonical work did not stop. It moved into a succession of direct descendants, forks, HQ/control surfaces, and later explicit documentary/semantic re-inheritance courts.

## Evidence law used in this report

This report distinguishes six relations and does not collapse them:

1. **ACTUAL_GIT_MERGE** — a PR/merge commit joins the worker/integration line into the target branch.
2. **DIRECT_DOWNSTREAM_INHERITANCE** — Git compare proves target is ahead of source with `behind_by=0` and the source/head is the merge base.
3. **SELECTIVE_OR_DIRECT_ADOPTION** — repository evidence says accepted payload was copied/integrated without merging the source branch or PR.
4. **OPERATIONAL_SUCCESSION / RE-INHERITANCE** — a later sovereign branch explicitly declares a prior branch/result inherited, even though Git ancestry is divergent.
5. **NAMED_INTEGRATION_ONLY / STALE_LABEL** — branch naming implies finality/integration but DAG evidence does not support trunk succession.
6. **STRANDED_OR_NONCURRENT_CAPITAL** — useful or executable work is explicitly outside the current control tree, or a return's payload is not proved admitted into the current HQ lineage.

A branch name, PR state, or recency is never treated by itself as sovereignty evidence.

## Reconstructed sovereignty history

### 1. Before the permanent break: `main` was still recoverably cumulative

The repository already used temporary integration branches. The important fact is that these earlier branches still had an explicit return path to `main`.

PR #23 (`Integrate V550–V552J repair: G5 PASS`) merged `agent/v550-v552j-repair-integration` into `main` on 2026-08-16. That event demonstrates the earlier operating constitution: workers accumulated on an integration branch, then the integration branch itself returned to `main`.

The S00 case shows an even more discriminating form of re-anchoring. PR #45 (`Integrate S00 schematic returns`) was closed unmerged, but its body states that it was superseded by **direct integration of the four accepted S00 RESULT blobs onto current main at commit `7db3dfbab6d2497da50c496cb2de76a5d7cee083`**, specifically to avoid stale control-room conflicts. Therefore a closed/unmerged integration PR is not automatically stranded; the payload may have been selectively adopted.

### 2. 2026-08-17: dual sovereignty appears

PR #27 established `agent/source-wave-identity-repair-integration` as an integration surface against a `main` planning base `25a63e08...`, but the PR never merged. PR #28 then merged an accepted hostile acceptance harness into that integration branch at 02:33:55Z. Many subsequent SWID worker/repair PRs also targeted that branch.

Current DAG comparison makes the permanent separation unmistakable:

`main` -> `agent/source-wave-identity-repair-integration` = `diverged`, with the SWID branch **135 commits ahead** and **443 behind** current `main`, merge base `25a63e08b0fcf7ef3dfc9de0c7b03325d26d918a`.

At the same time `main` continued to acquire architecture/authority material. PR #79 makes the parallelism explicit rather than accidental: SWID finalization remained an external production gate while independent authority work proceeded on the other line.

This is the first constitutional ambiguity: **there was no longer one branch whose ancestry contained all accepted work**.

### 3. 2026-08-18: `main` freezes, successor campaigns branch directly from its final tip

PR #125 merged at `0777a34e...` on 2026-08-18T18:52:29Z. Current `main` remains exactly this commit.

Two proved downstream structures are important:

- `main` -> `agent/vozhd-trii-prechange-discovery-control`: direct descendant, **69 ahead / 0 behind**, merge base exactly `0777a34e...`.
- `agent/vozhd-trii-prechange-discovery-control` -> `agent/vozhd-trii-stage-close-hq`: direct descendant, **46 ahead / 0 behind**.

That is a genuine Git succession chain.

Separately:

- `main` -> `agent/vozhd-trii-pre553-substrate-reconstruction-control`: direct descendant, **444 ahead / 0 behind**, merge base exactly `0777a34e...`; current head observed at `04a0109aa170c6041b199e5c6130a39a8e0f6029`.

The PRE553 substrate-reconstruction control branch is therefore the strongest early post-main **de facto cumulative trunk**: it inherits final `main` exactly and then accumulates hundreds of commits across substrate reconstruction, control-room preservation, recovered corpus authority, compiler work, and successor launch material.

But `stage-close-hq` and the later PRE553 control surface are not one simple parent-child continuation. They diverge. This is the second constitutional ambiguity: multiple branches inherited the same frozen `main` legitimacy and then advanced different portions of the project.

### 4. Non-main governance becomes explicit, not accidental

PR #134 is decisive evidence. It merges accepted SR06 runtime/tests from `agent/vozhd-trii-sr06-c11-parquet-duckdb` into `agent/vozhd-trii-pre553-substrate-reconstruction-control` at merge SHA `def253c7f62b74d07c7297e6ca279642b7d13904`. Its body states:

> HQ integration of the accepted SR06 implementation ... into the substrate-reconstruction control branch; governance remains on the control branch.

That is an explicit constitutional transfer of operational governance away from `main`.

### 5. Late PRE553 sovereignty forks rather than moving linearly

Two major later surfaces branch from the PRE553 lineage but do not contain its entire final history:

- `agent/vozhd-trii-pre553-substrate-reconstruction-control` -> `agent/vozhd-trii-authority-revalidation-control` = `diverged`, authority-revalidation **212 ahead / 27 behind**, merge base `b824c7d2b618b8e0987f6774b302e875d90b8fdd`.
- PRE553 control -> `agent/rawlsing-conservation-hq-integration` = `diverged`, conservation HQ **39 ahead / 2 behind**, merge base `58a9347ae8b2b7561079c9d8cec79a8abd60b70a`.

So neither branch can be called a simple full successor by ancestry. They are **late PRE553 forks with different cumulative responsibilities**.

The conservation branch became especially important because it froze the Rawlsing Long Memory / zero-loss functional baseline. Its head is `669062e6c319f31214f403939dded91300639bde`.

### 6. Later HQ sovereignty is reconstituted on `vozhd-to-vozhdy-inheritance-integration-r1`

`agent/vozhd-to-vozhdy-inheritance-integration-r1` is not a Git descendant of the entire conservation-HQ branch. Comparing conservation HQ -> inheritance integration is `diverged`: inheritance integration is **110 ahead / 39 behind**, with the same late-PRE553 merge base `58a9347...`.

However, this is not mere branch-name theater. Repository authority documents on the inheritance branch explicitly perform the missing constitutional work:

- Authority 39 names `agent/rawlsing-conservation-hq-integration` and terminal HEAD `669062e6...` as the **authoritative prior conservation branch**, declares that its 44 normalized obligations **must be inherited rather than rediscovered**, and requires a living succession ledger on the current HQ control surface.
- Authority 40 states that Authority 39 **permanently inherits Rawlsing Long Memory at `669062e6...`**, accepts seven exact delta-audit returns, distinguishes evidence from production promotion, and continues bounded zero-loss repair from the coordination branch.

This is therefore an **OPERATIONAL_SUCCESSION / RE-INHERITANCE** edge rather than an actual Git merge edge. The later HQ line deliberately reconstituted prior sovereign capital through explicit authority and succession accounting.

The observed head of this HQ branch is:

`daffee545fc60a8cd635aee9aafbe77a920f4c19`

with commit message `[HQ][Authority-47] join C01-C10 returns and release C06 court` (2026-08-29).

This is the strongest repository-supported answer to “what branch is the current de facto HQ trunk?”

### 7. Current Joint Authority is a direct child campaign, not a new global sovereign

`agent/vozhd-to-vozhdy-inheritance-integration-r1` -> `agent/subvozhd-current-joint-authority-r1-control` is a clean direct inheritance edge: **2 ahead / 0 behind**, merge base exactly `daffee545...`. The current joint-control head observed is `97250b26ec847f8f4598e49bd9e99f8eed58be9f`.

But its own campaign authority is constitutionally explicit:

- Parent HQ branch: `agent/vozhd-to-vozhdy-inheritance-integration-r1`
- Exact parent HQ HEAD: `daffee545...`
- Campaign control: `agent/subvozhd-current-joint-authority-r1-control`
- `This campaign does not supersede HQ.`
- findings/artifacts return to HQ for adoption.

Therefore the current joint-control branch is a **subordinate active successor campaign**, not the replacement global trunk. The global HQ sovereignty remains anchored in the parent HQ lineage unless and until HQ adopts a returned successor.

## Branch names that must not be mistaken for sovereignty

Several branch names are actively misleading if read without DAG evidence:

- `agent/rawlsing-conservation-hq-integration-postp10` is **17 commits behind** `agent/rawlsing-conservation-hq-integration`; the later-sounding name is a stale ancestor snapshot.
- `agent/vozhd-final-rawlsing-inheritance-r3-install` is **107 commits behind** `agent/vozhd-to-vozhdy-inheritance-integration-r1`; “final” does not mean current.
- `agent/verkhovod-fracturemap-fulljoin-r1` is **17 commits behind** the current inheritance-integration HQ head.
- `agent/verkhovod-z02-fracturemap-integration-r1` is a side fork: relative to the inheritance HQ head it is **7 ahead / 13 behind**, merge base `c649d57c14ca6c0f84571beab4610c007c2484f2`.
- `agent/vozhd-verkhovod-hq-continuity-r1` is also a side lineage, not the ancestor of current joint control: current HQ and that branch diverge; current joint control directly descends from `daffee545...`, not from the continuity branch's six unique commits.

## Constitutional succession: explicit versus merely operational

### Explicit transitions

1. V550–V552J repair integration -> `main` through PR #23.
2. S00 accepted blobs -> `main` through direct selective adoption documented in closed PR #45.
3. Accepted SR06 -> PRE553 substrate-control through PR #134, with explicit statement that governance remains on the control branch.
4. Conservation Long Memory -> inheritance HQ through Authority 39/40 explicit inheritance and succession law.
5. Inheritance HQ -> Current Joint campaign through direct Git descent plus an explicit parent-HQ declaration; importantly, this is an explicit **subordinate campaign cut**, not HQ supersession.

### Operational / ambiguous transitions

1. `main` -> SWID integration as a parallel cumulative trunk: the campaign PR remained open; worker returns nevertheless merged into the branch.
2. final `main` -> multiple post-main control/HQ branches: several branches are direct descendants of the same final tip, but there is no single Git event choosing one constitutional successor.
3. late PRE553 -> authority-revalidation / conservation HQ: both are divergent forks with substantial unique work.
4. conservation HQ -> inheritance HQ: the later branch explicitly inherits the prior baseline but does not merge the prior branch history; semantic/constitutional adoption and Git ancestry separate.

## Where constitutional succession becomes ambiguous

The first ambiguity begins on **2026-08-17** when accepted SWID work and accepted `main` work proceed in parallel with neither history containing the other.

The deeper ambiguity begins after `main` freezes: direct-descendant control branches inherit `main`, but later HQ/control branches fork from different points. At that point “canonical” cannot be recovered by commit date, branch name, PR merge status, or simple ancestry alone.

The project partially repairs this defect later through explicit re-inheritance courts—especially Authority 39/40—but those courts themselves prove why a pre-main reconciliation is necessary: the later HQ had to distinguish `RECOVERED_ON_OLD_BRANCH != CURRENTLY_ADOPTED`, `ADOPTED_DOCTRINE != EXECUTABLE_SUCCESSOR`, and explicitly audit stranded capital.

## Contemporary heads inheriting large portions of the post-main project

### Primary current HQ trunk

`agent/vozhd-to-vozhdy-inheritance-integration-r1` @ `daffee545fc60a8cd635aee9aafbe77a920f4c19`

Why: late operational integration line; contains the recovery-integration campaign, explicit Long Memory re-inheritance, zero-loss succession courts, return joins, and Authority-47 HQ join. Current Joint authority names it as parent HQ.

### Active subordinate child campaign

`agent/subvozhd-current-joint-authority-r1-control` @ `97250b26ec847f8f4598e49bd9e99f8eed58be9f`

Why: exact direct descendant (+2 / -0) of `daffee545...`; explicitly subordinate to HQ and pending HQ adoption.

### Major retained/divergent capital lines

- `agent/rawlsing-conservation-hq-integration` @ `669062e6c319f31214f403939dded91300639bde` — authoritative prior Long Memory baseline, later explicitly inherited but not Git-merged into current HQ.
- `agent/vozhd-trii-authority-revalidation-control` @ `3fdb4d899923f5b7a326fbfbe15112c82b44716e` — 212 unique commits after its PRE553 fork point; not a full descendant of final PRE553 control.
- `agent/vozhd-trii-pre553-substrate-reconstruction-control` @ `04a0109aa170c6041b199e5c6130a39a8e0f6029` — 444 commits beyond final `main`; strongest early post-main cumulative trunk and explicit governance target for PR #134.
- `agent/source-wave-identity-repair-integration` @ observed PR #27 head `75aac98e0280289a717e2b49f8d2066ab1c926db` — old but large parallel runtime lineage, 135 unique commits relative to final main.

## Stranded / noncurrent return findings

There is **no responsible basis to claim that every unmerged PR or non-ancestor worker branch is globally stranded**. PR #45 proves why: its PR was unmerged but accepted payload was directly adopted elsewhere.

The strongest repository-supported stranded-capital findings come from Authority 40 itself. It explicitly records implementation/proof stranding as real and names known non-current executable capital:

- C4R2A seven-gap information-repair prototype `5ea5cd5a5e4f8cc6c5ef256a439f3f7bdfb27e5d` — explicitly non-bankable prototype.
- C5R2 maintenance owner/executor prototype `b4dae70ee524c7a3297f7b48bdfd0d0c927eac21` — explicitly non-bankable reference-identity prototype.
- Route-A R5/Audit69 runtime `d6206cd0e351100b64cdf3ace997733153c18eb7` — deeply implemented/tested candidate runtime **outside current control tree**; exact-file reuse allowed, branch-history merge not implied.

PR #116 (`Restore active-35 authority surfaces`) is a separate **current-HQ stranding candidate**, not a proved globally-never-consumed return. It remains an open draft against `main` at head `3e2160834482caaf9ce9923b7bca5a20e53d60d4`. Comparing its head to current inheritance HQ is divergent, and at least two of its defining restored paths (`bindings/question_block_registry_35wave_active_v1.yaml` and `manifests/question_structural_mapping_live_35wave_active_v1.csv`) are absent from the inheritance-HQ branch. However, related authority surfaces exist on the old SWID integration lineage, so exact content-equivalence across every successor branch was not proven. It is therefore classified as **HQ-not-adopted / global-stranding-unresolved**, not falsely promoted to a certain global loss.

## Answers required by command

### When did `main` cease being the effective cumulative trunk?

Earliest hard permanent break: **2026-08-17T02:33:55Z**, PR #28 merged accepted work into the unmerged SWID integration branch. `main` then became one of multiple active authoritative streams. Hard freeze: **2026-08-18T18:52:29Z**, PR #125 / `0777a34e...`; `main` has not moved since.

### What branches subsequently served as de facto trunks?

In order of role rather than pretending one clean ancestry:

`agent/source-wave-identity-repair-integration` (parallel runtime trunk while main still moved)  
`agent/vozhd-trii-prechange-discovery-control` -> `agent/vozhd-trii-stage-close-hq` (clean post-main descendant chain)  
`agent/vozhd-trii-pre553-substrate-reconstruction-control` (major early post-main cumulative control trunk)  
late PRE553 forks including `agent/rawlsing-conservation-hq-integration` and `agent/vozhd-trii-authority-revalidation-control`  
`agent/vozhd-to-vozhdy-inheritance-integration-r1` (later reconstituted HQ coordination trunk)  
`agent/subvozhd-current-joint-authority-r1-control` (current direct child campaign, explicitly not HQ replacement).

### Which transitions were explicit and which merely happened operationally?

See the explicit/operational section above and `SUCCESSION_CHAIN.tsv`. The most important difference is that Long Memory -> current HQ is **explicit semantic/constitutional inheritance without Git merge**, while the earliest SWID split is **operational accumulation without constitutional global re-anchoring**.

### Where does constitutional succession become ambiguous?

First at the Aug. 17 SWID/main dual-lineage split; then structurally after final main when several direct-descendant and late-PRE553 forks simultaneously accumulated canonical-looking authority. The later inheritance HQ repairs some ambiguity through explicit inheritance courts but does not retroactively make the DAG linear.

### Which contemporary heads inherit large portions of the post-main project?

Primary: `agent/vozhd-to-vozhdy-inheritance-integration-r1` @ `daffee545...`.  
Active child: `agent/subvozhd-current-joint-authority-r1-control` @ `97250b26...`.  
Major retained divergent capital: PRE553 control `04a0109...`, conservation HQ `669062e6...`, authority revalidation `3fdb4d...`, and the older SWID runtime integration line `75aac98...`.

### Which accepted-looking returns appear never to have entered any successor trunk?

No blanket inference is safe. Authority 40 itself proves real noncurrent executable capital and names the C4R2A, C5R2, and Route-A R5/Audit69 refs above. PR #116 is proved absent from current HQ ancestry and missing defining paths there, but global never-consumption is unresolved because related surfaces exist on another divergent lineage. Closed PR #45 is explicitly **not stranded**; it was selectively adopted to `main`. PR #134 is explicitly **not stranded**; it was merged into the PRE553 control trunk rather than `main`.

## Reconciliation implication for VOZHD

The repository does support the fear that Rawlsing's accumulated project capital became **distributed across sovereign and quasi-sovereign branch lineages without a single continuously updated canonical root**. But a blind “merge every integration/final branch into pre-main” would be destructive: some later-sounding branches are stale ancestors, some are side forks, some carry prototypes explicitly rejected as current, and some later HQ documents re-inherit prior semantic capital without inheriting its branch history.

The safe PRE-MAIN operation therefore needs an **edge-by-edge admissibility court**:

`branch recency/name` must never imply adoption;  
`Git ancestry` must be combined with `explicit acceptance/re-inheritance evidence`;  
`payload equivalence` must be checked before treating unmerged returns as lost;  
`current HQ sovereignty` must be distinguished from subordinate campaign controls.

The strongest current constitutional anchor recovered by this worker is:

`agent/vozhd-to-vozhdy-inheritance-integration-r1 @ daffee545fc60a8cd635aee9aafbe77a920f4c19`

with current-joint work branching directly from it but explicitly returning to it for HQ adoption.
