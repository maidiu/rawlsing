# Rawlsing J-Family Authority Project
## Full Explainer, Current State, Package Map, and Resume Guide

## 1. What we are doing

Rawlsing is ultimately a personality-generation system built from large, heterogeneous public-opinion surveys. Before Rawlsing can use those surveys coherently, it needs a governed answer to a deceptively difficult question:

> When do different survey variables, from different surveys and different years, count as implementations of the same underlying question-family proposition—and when must they remain separate, become explicit variants, form a hierarchy, or be rejected from combination?

This is the **J-family authority** problem.

The current work is not yet generating personalities, estimating respondents, or harmonizing arbitrary response values. It is building the semantic and evidentiary authority layer that later Rawlsing stages must rely on. That layer decides:

- which source-local question lineages belong to one canonical family;
- what proposition that family actually asks;
- which response forms are merely variants of the same proposition;
- which apparent similarities are false collapses;
- where direct, derived, hierarchical, conditional, or context-bearing items must remain distinct;
- what exact evidence permits each decision;
- how every decision is persisted, versioned, reconstructed, tested, and traced back to source wording.

The governing principle is fail-closed: similarity is never enough by itself, and no family identity may be created merely because it would be convenient downstream.

---

## 2. The three number systems that must not be confused

This project uses several kinds of version numbers at once.

### Package or handoff versions

Examples: `v35`, `v40`, `v41 RECOVERY`.

These identify cumulative delivery packages. The current split download is:

`Rawlsing_J_Family_Authority_Strategy_Handoff_v41_RECOVERY_20260802.zip`

The `v41` label means “recovery wrapper version 41.” It does **not** mean that P3C authority release R41 is the current state.

### P3A implementation version

The complete executable base in the recovery package is **P3A v40**, sections 00–62.

That is the last source-complete, independently executable engineering state physically preserved after the sandbox reset.

### P3C authority releases

Examples: `R41`, `R42`, through `R52`, with `R53` tested separately.

These are append-only authority releases inside PostgreSQL. The last recorded persistent P3C authority release was **R52**. R53 was tested on a disposable clone but was never promoted or committed.

---

## 3. The data universe

The project covers nine survey sources across 35 active waves:

- GSS;
- World Values Survey;
- European Values Study;
- Arab Barometer;
- Afrobarometer;
- Asian Barometer;
- Latinobarómetro;
- South Asia survey material;
- Life in Transition Survey.

The frozen P2 universe contains:

- **18,276 question implementations**: specific survey variables in specific waves;
- **13,526 source-local lineages**: implementations connected through governed within-source continuity;
- **19,175 effective governing pair authorities** in the P3 input surface;
- **141 P3A candidate revisions** generated for adjudication.

These levels are deliberately distinct.

A question implementation is a particular variable in one wave. A lineage groups implementations that are already governed as one source-local continuity. A candidate groups lineages for P3C review. A canonical family exists only after adjudication.

---

## 4. Core terms

### Implementation

One concrete survey variable in one survey wave, with wording, response contract, provenance, and source identity.

### Source-local lineage

A governed continuity across implementations within one survey source. A lineage does not automatically authorize cross-source equivalence.

### Pair authority

A P2 ruling about the relationship between two lineages. It may support proposition identity, response compatibility, collision, hierarchy, redirect, unresolved status, or another typed relation.

### Proposition signature

A structured account of what an item asks: subject, operator, target, outcome, modality, timeframe, condition, population, geographic scope, polarity, direct or derived status, and parent context.

### Candidate

A non-authoritative P3A object assembled from rule-derived topology and complete evidence. A candidate is a question submitted to adjudication, not a family declaration.

### Closure obligation

A specific pair or boundary that P3C must resolve before a candidate can close. P3C may accept, reject, split, preserve hierarchy, or remain blocked, but it may not silently ignore the obligation.

### Variant

A governed implementation or response-form difference that does not change proposition identity. Variants preserve exact source form. They do not imply that response values are portable across surveys.

### Canonical family

An append-only, release-scoped authority object created by P3C. It has a canonical proposition, exact memberships, evidence, variants, exclusions, history, and immutable revisions.

### Confirming revision

A later candidate may contain only members already governed by a family. It can create an evidence-confirming family revision with zero new membership, rather than re-accepting or duplicating the members.

---

## 5. The overall pipeline

## Phase P2: discover and govern the source evidence

P2 builds the question universe and governs source-local and cross-source relations. It does not create final J-families.

P2 work included:

- complete 35-wave question-node population;
- source-local deep passes for all nine surveys;
- continuity edges and anti-continuity guards;
- source structures and battery context;
- response-authority gaps;
- cross-source proposition seed refreshes;
- eight bounded global pair-adjudication tranches;
- final effective authority reconciliation.

The result is the frozen evidence surface from which P3 must work.

## Phase P3A: construct candidates without authoring families

P3A turns the P2 evidence into deterministic candidate objects. Its job is engineering and evidence closure, not semantic fiat.

P3A v40 established this path:

`P2 authority → endpoint resolution → pair projections → components and attachments → complete candidate evidence bundle → non-authoritative staging → atomic immutable promotion → packet and draft projection`

P3A v40 was rebuilt from an empty PostgreSQL database. The recorded successful execution included:

- 13,526 lineage objects;
- 18,276 implementation objects and memberships;
- 19,175 pair facts;
- 38,350 resolved endpoints;
- 119 candidate components;
- 141 candidate revisions;
- 141 immutable evidence snapshots;
- complete lifecycle events;
- 141/141 family-identity continuity checks;
- four pilot packets convergent with PostgreSQL;
- nineteen executable lifecycle and adversarial fixture cases;
- 56 live validation labels with no applicable failures;
- only the intentionally future-phase gates remaining.

The central P3A repair was to make candidate evidence complete and reconstructive. The staged payload, immutable PostgreSQL snapshot, database reconstruction, packet, and draft must all represent the same canonical evidence surface and hash.

## Phase P3C: make semantic authority decisions

P3C performs the substantive adjudication. It decides whether each candidate should:

- become a canonical family;
- become a family with explicit variants;
- converge with another candidate into one family;
- extend an existing family through a later immutable revision;
- confirm an existing family without adding membership;
- split into successor candidates;
- preserve a hierarchy;
- reject a collision or false collapse;
- remain blocked because authority is insufficient.

P3C is where wording, battery context, direct versus derived status, time index, rank position, target scope, and collision evidence become binding semantic decisions.

---

## 6. What the lost P3C execution had accomplished

Sections 63–79 describe a long sequence of actual work that was completed and tested before the sandbox reset. The records are useful as a roadmap, but the generated source, decision JSON, Git objects, manifests, verifier returns, and PostgreSQL database are no longer present.

### Sections 63–66: initial admissions and semantic boundaries

The execution:

- built evidence digests for all 141 candidates;
- admitted deterministic exact-proposition families;
- preserved response-form variants;
- converged proposition-identical candidates into shared families;
- kept genuinely distinct propositions apart with named exclusions;
- recovered missing parent context for temporal and ranked battery items.

Examples of distinctions preserved:

- the last national election versus elections in general;
- categorical religious identity versus graded religiosity;
- present democracy placement versus placement ten years earlier;
- first-ranked national aim versus second-ranked national aim.

### Sections 67–69: direct versus constructed prayer

A mixed prayer candidate was split because direct prayer frequency and a constructed WVS recode do not have the same derived status.

The execution then:

- materialized exact singleton split successors;
- extended the direct-prayer canonical family append-only;
- created a separate derived family for the constructed recode;
- installed reciprocal exclusions so direct and constructed prayer could not be collapsed later.

The recorded family identities were:

- `JFAM-000203`: direct prayer frequency;
- `JFAM-000425`: constructed WVS prayer recode.

### Sections 70–75: overlapping and redundant candidates

Later candidates often overlapped families already admitted. P3C added a truthful `ALREADY_CANONICAL` disposition:

- new lineages are accepted;
- predecessor members are marked already canonical;
- inherited members are not re-accepted or excluded;
- canonical revisions equal predecessor membership plus the exact disjoint set of new accepted members.

This allowed:

- append-only family extensions;
- evidence-only confirming revisions;
- closure of missing pair obligations without duplicating family membership;
- nested strict candidates to confirm larger families.

### Sections 73–77: attachment families, trust families, and remaining direct propositions

The execution admitted complete cross-source families for such surfaces as:

- generalized interpersonal trust;
- institutional trust in election commissions, churches, armed forces, police, parliaments, courts, and local government;
- unwanted-neighbour batteries;
- democratic-system evaluations;
- happiness;
- political attitudes and social norms;
- direct access, participation, moral-justifiability, and membership items.

Exact source-response forms were kept as variants. Missing upstream pair authority was closed through named P3C adjudication rows rather than by rewriting P2 history.

### Sections 78–79: internet frequency

The complete internet-use-frequency surface was found to extend an existing family rather than create a duplicate family.

The last recorded persistent action was an evidence-only confirmation of the nested internet candidate.

---

## 7. The exact recorded state

## Last recorded persistent state: R52

The recovery record states:

- authority release: **R52**;
- Git commit: `68c3114acad3366380a5e83c0480802dfef6e511`;
- cumulative adjudication decisions: **139**;
- canonical families: **108**;
- canonical revisions: **134**;
- human-resolved pair obligations: **326**;
- original P3A candidates remaining: **2**;
- no applicable q01–q54 failures;
- only phase-aware future gates remained.

This was the last state recorded as applied to the persistent working database.

## Tested but never promoted: R53

Section 80 was tested on a disposable clone only. It would have added three decisions:

- household-income contribution;
- political-party trust;
- abortion justifiability.

The clone reportedly reached:

- 142 cumulative decisions;
- 111 canonical families;
- one original candidate remaining.

The special contract required stronger upstream collision or hierarchy evidence to receive exact P3C dispositions before an accepted decision could commit. Mutation tests reportedly proved that omitting those dispositions failed at deferred commit.

**R53 is not authority.** It was not committed or promoted, and its executable evidence was lost.

## Final unresolved original candidate

`P3CAND-000273` was the mixed direct/constructed prayer attachment.

Its intended disposition was:

- split the candidate exactly by direct versus constructed status;
- route the direct prayer members to `JFAM-000203`;
- route the constructed WVS recode to `JFAM-000425`;
- add zero new canonical memberships if all members are already governed;
- close the final mixed-status obligation;
- record a redundant split confirmation rather than create another family.

That final decision was not executed before the reset.

---

## 8. What was lost and why the current package is a recovery package

The execution sandbox reset after the P3C run. The following were lost:

- the Git worktree containing sections 63–80;
- the Git objects and local commits for those sections;
- the persistent R52 PostgreSQL database;
- the R53 disposable test databases;
- the 139 persistent P3C decision JSON objects and cumulative manifests;
- the three R53 tested-only decision objects;
- generated verifier, query, and mutation returns.

What survived:

- the source-complete v40 transfer, sections 00–62;
- the Linux PostgreSQL runtime kit;
- earlier cumulative Rawlsing archives;
- terminal-session evidence;
- transfer manifests and dependency records;
- the package-return record;
- the conversation record from which the section 63–80 execution ledger was reconstructed.

Therefore the current archive is classified as:

`COMPLETE_AVAILABLE_ARTIFACT_RECOVERY_HANDOFF_NOT_P3C_AUTHORITY_CHECKPOINT`

That phrase matters. The package is complete with respect to the artifacts physically available. It is **not** a complete P3C authority checkpoint.

The section 63–80 `RECORDED_STATE.json` and `README_RECOVERY.md` files are descriptions of the lost execution. They must never be imported as canonical decisions or treated as substitutes for executable evidence.

---

## 9. Where everything is in the recovery package

After combining and extracting the three ZIP parts, the package root is:

`Rawlsing_J_Family_Authority_Strategy_Handoff_v41_RECOVERY_20260802/`

## Start here—current recovery controls

`00_RECOVERY_START_HERE/`

This is the authoritative orientation layer for the recovery package.

Important files:

- `README_FIRST.md` — the truthful package classification and immediate warning;
- `CURRENT_STATE.json` — machine-readable R52/R53 state;
- `EXACT_RESUME_POINT.md` — preferred recovery and fallback paths;
- `RECOVERY_BOUNDARY.md` — what survived versus what vanished;
- `MISSING_ARTIFACTS.csv` — exact missing authority classes;
- `AVAILABLE_RECOVERY_INPUTS.csv` — surviving original archives and hashes;
- `P3C_EXECUTION_LEDGER.csv` and `.json` — section-by-section recorded trajectory;
- `NEXT_CHAT_OPENING_INSTRUCTION.txt` — safe instruction for a new agent;
- `verify_recovery_handoff.py` — recovery-package verifier.

**Important usability warning:** the root-level `README_FIRST.md` and `MASTER_HANDOFF.md`, and the files under `00_START_HERE/`, are inherited historical v35/v40-base controls. They are not the current recovery orientation. Always open `00_RECOVERY_START_HERE/README_FIRST.md` first.

## P2 and historical architecture

- `01_MACHINE_PLAN/` — machine schemas, gates, ledgers, and work phases;
- `02_CORE_REFERENCE/` — frozen GSS controls, code, and core authority references;
- `03_SEMANTIC_REFERENCE/` — semantic registries and concept maps;
- `05_PHASE_HISTORY/` — earlier P1/P1.5 packages and reports;
- `06_CURRENT_ARCHITECTURE/` — accepted architecture controls;
- `07_P2_EXECUTION_CONTRACT/` — P2 execution contract;
- `08_P2_PHASE0/` — complete 35-wave node universe.

## Source-local P2 passes

- `09_...` through `27_...` — source-local deep passes and cross-source refreshes;
- `28_...` through `31_...` — all-source closure, calibre audit, and independent integrity review.

## Global P2 pair adjudication

- `32_...` through `42_...` — bounded global pair-adjudication tranches and final cross-tranche closure.

These sections contain the frozen evidence that P3 uses. They are not superseded by the missing P3C narrative.

## P3 architecture and implementation hardening

- `43_...` through `49_...` — the succession of implementation-readiness, falsification, and executable-closure audits;
- `50_...` through `62_...` — P3A v7 implementation, populated object closure, typed constraints, release-neutral identity, evidence convergence, staging, and atomic promotion.

Section 62 is the final source-complete P3A implementation in the package.

## P3C recovery records

- `63_...` through `80_...`

Each contains only:

- `README_RECOVERY.md`;
- `RECORDED_STATE.json`.

These are non-authoritative execution records. The actual section source, decisions, manifests, and database are missing.

## Original recovery inputs

`90_RECOVERY_INPUTS/`

Important subdirectories:

- `ORIGINAL_ARCHIVES/Rawlsing_P3A_V40_Direct_Engineering_Transfer.zip` — original source-complete v40 transfer;
- `ORIGINAL_ARCHIVES/Rawlsing_P3A_Linux_Runtime_Kit.zip` — PostgreSQL 15 and offline Python runtime kit;
- `SESSION_EVIDENCE/` — saved terminal and conversation evidence;
- `TRANSFER_METADATA/` — worktree manifest, dependencies, absolute paths, and execution entrypoints.

## Root integrity controls

- `PACKAGE_INDEX.csv` — every packaged path, byte size, hash, and classification;
- `SHA256SUMS.csv` — payload checksums;
- `VALIDATION.json` — inherited executable-base validation;
- `RECOVERY_PACKAGE_NOTE.md` — package-level warning.

---

## 10. How to reconstruct the three-part download

The three `.part` files are binary segments of one ZIP. They are not independently extractable archives.

Place all three in the same folder and run:

```bash
cat Rawlsing_J_Family_Authority_Strategy_Handoff_v41_RECOVERY_20260802.zip.part1 \
    Rawlsing_J_Family_Authority_Strategy_Handoff_v41_RECOVERY_20260802.zip.part2 \
    Rawlsing_J_Family_Authority_Strategy_Handoff_v41_RECOVERY_20260802.zip.part3 \
    > Rawlsing_J_Family_Authority_Strategy_Handoff_v41_RECOVERY_20260802.zip
```

Verify the reconstructed ZIP:

```bash
shasum -a 256 Rawlsing_J_Family_Authority_Strategy_Handoff_v41_RECOVERY_20260802.zip
```

Expected SHA-256:

`88313f76ca1d5af2abcd1e7092bc955946d2c16ec071b59f12135263c642f9b1`

Then test and extract:

```bash
unzip -t Rawlsing_J_Family_Authority_Strategy_Handoff_v41_RECOVERY_20260802.zip
unzip Rawlsing_J_Family_Authority_Strategy_Handoff_v41_RECOVERY_20260802.zip
```

The package-return record reports 3,169 manifested payload files, 3,170 ZIP regular files, and zero fresh-extraction mismatches.

---

## 11. The preferred next step: recover the actual R52 authority state

Before rerunning P3C, search for an external copy of the lost worktree or database.

The original local workspace was associated with:

`/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution`

Search the Mac, Codex workspaces, Downloads, Desktop, Trash, external storage, and any cloud-synced directories for:

- a worktree containing `63_P3C_ADJUDICATION_INVENTORY_AND_DETERMINISTIC_PASS/` through `79_P3C_INTERNET_FREQUENCY_SUBSET_CONFIRMATION/`;
- Git commit `68c3114acad3366380a5e83c0480802dfef6e511`;
- a Git bundle, repository copy, or archive created after that commit;
- PostgreSQL data or dumps containing database names such as `rawlsing_p3c_v41_working`;
- section 80 source retained separately;
- files named `P3C_V52_CUMULATIVE_DECISION_MANIFEST.json` or similar.

Useful macOS searches:

```bash
find /Users/matthewsmith -type d -name '63_P3C_ADJUDICATION_INVENTORY_AND_DETERMINISTIC_PASS' 2>/dev/null
find /Users/matthewsmith -type f \( -name '*P3C_V52*' -o -name '*P3C_V53*' -o -name '*.bundle' -o -name '*.dump' \) 2>/dev/null
find /Users/matthewsmith -type d -name '.git' -print 2>/dev/null
```

For every Git repository found:

```bash
git -C /path/to/repository cat-file -t 68c3114acad3366380a5e83c0480802dfef6e511
```

A recovered state is not accepted merely because its filenames look right. It must reconcile to the recorded R52 counts and pass the live validators.

---

## 12. Fallback next step: rerun P3C from the executable v40 base

If no external copy exists, rebuild rather than fabricate.

### Step 1: establish a persistent engineering workspace

- Extract the v40 direct-engineering transfer.
- Initialize or preserve a real Git repository outside a disposable session.
- Commit the untouched v40 baseline.
- Keep generated decisions and code in version control.

### Step 2: install the runtime

Use:

`90_RECOVERY_INPUTS/ORIGINAL_ARCHIVES/Rawlsing_P3A_Linux_Runtime_Kit.zip`

It contains the PostgreSQL 15 runtime and offline Psycopg wheels used in the prior execution.

### Step 3: rebuild P3A from empty PostgreSQL

Use the execution entrypoints under:

`90_RECOVERY_INPUTS/TRANSFER_METADATA/EXECUTION_ENTRYPOINTS.md`

Rebuild:

- contracts;
- lineage and implementation memberships;
- pair facts and endpoints;
- signatures and components;
- all 141 candidates;
- complete immutable candidate evidence snapshots;
- packets, reports, fixtures, live queries, and verifier outputs.

Do not begin P3C until the v40 P3A acceptance path passes from an empty database.

### Step 4: regenerate section 63 inventory

Rebuild all 141 evidence digests from PostgreSQL and the frozen source files. Do not copy the recorded ledger’s decisions into the new authority database.

### Step 5: independently reproduce P3C decisions

Use `P3C_EXECUTION_LEDGER.csv` as:

- an ordering guide;
- a list of previously encountered semantic traps;
- a regression and mutation checklist;
- a comparison target for cumulative counts.

It is not decision authority.

Every reconstructed decision must have:

- source wording and battery context;
- exact candidate membership;
- proposition signature;
- pair and boundary disposition;
- variant assignments where necessary;
- exclusions;
- immutable decision hash;
- append-only family revision logic;
- successful database reconstruction and validation.

### Step 6: reach and verify R52

A reconstructed R52 should independently reach the recorded state:

- 139 decisions;
- 108 families;
- 134 revisions;
- 326 human-resolved obligations;
- two original candidates remaining;
- no applicable validation failures.

Matching counts are necessary but not sufficient. The actual decisions and reconstructed evidence must pass.

### Step 7: independently reproduce R53

Rebuild and retest the three special decisions. Do not promote them merely because the ledger says the disposable clone passed.

The collision and hierarchy overrides must retain the stronger upstream evidence and supply exact dispositions. They may not erase or rewrite P2 rulings.

### Step 8: adjudicate candidate 273

Execute the mixed-prayer split confirmation:

- exact direct/constructed partition;
- direct members linked to `JFAM-000203`;
- constructed member linked to `JFAM-000425`;
- zero duplicate canonical memberships;
- closure of the final mixed-status obligation;
- complete lifecycle and evidence history.

### Step 9: close P3C

Run the complete validation suite. The final P3C closure gate requires no unadjudicated original candidates and no unresolved applicable obligations.

---

## 13. What happens after P3C

P3C closure is not the end of Rawlsing. It unlocks the downstream J-family pipeline.

The next major deliverable is the canonical non-GSS J-family authority in the existing GSS-compatible schema. That authority must include:

- stable canonical family identities;
- immutable family revisions;
- exact source-local lineage memberships;
- implementation mappings;
- proposition signatures;
- source-response variants;
- exclusions and collision boundaries;
- provenance and release history;
- downstream permission states.

Then the downstream J-family stages can run across all governed waves:

### V550J: prepared joint-response substrate

Construct the family-aware respondent-level substrate without flattening variants or violating response authority.

### V551J: joint evidence packets

Generate governed joint evidence, support/opposition states, component structures, conflicts, and certification status.

### V552J: runtime-safe structural handoff

Produce the validated runtime-safe authority used by later Rawlsing personality-generation layers.

The downstream chain must continue to preserve the distinction between:

- proposition identity;
- response-form compatibility;
- value harmonization authority;
- respondent-level joint evidence.

P3C may authorize the first. It does not automatically authorize the others.

---

## 14. What “finished” means

P3C is complete only when:

- every original P3A candidate has a final governed disposition;
- every split successor is materialized and adjudicated;
- all canonical memberships are non-overlapping unless an explicit governed structure permits otherwise;
- no duplicate canonical proposition remains;
- all variants and promotion mappings are complete;
- every accepted family has rule-based exclusions and named exclusions where actual near-neighbours exist;
- every open pair, collision, hierarchy, redirect, coordinate constraint, and unresolved boundary has a final status;
- all family and decision hashes reconstruct from PostgreSQL;
- lifecycle event order and release ancestry are valid;
- q01–q54 have no applicable failures;
- the P3C no-unadjudicated-candidate closure gate passes;
- a persistent Git commit and database dump are captured;
- a cumulative handoff is built from those actual artifacts.

For the next true checkpoint, the handoff should include both:

1. a Git bundle or complete repository containing the P3C worktree; and
2. a PostgreSQL custom-format dump of the authority database.

That dump is metadata authority, not the massive respondent-level survey database. Capturing it prevents this exact recovery problem from recurring.

---

## 15. Things the next agent must not do

- Do not start from the root-level historical `README_FIRST.md`; start from `00_RECOVERY_START_HERE/README_FIRST.md`.
- Do not call the recovery ledger an authority checkpoint.
- Do not import section 63–80 narrative records as decisions.
- Do not promote the recorded R53 state without reproducing its source and database proof.
- Do not treat a P3A candidate as a canonical family.
- Do not infer response-value portability from proposition identity.
- Do not flatten source response forms that were governed as variants.
- Do not mutate old canonical revisions; create append-only successor revisions.
- Do not re-accept predecessor members; mark them `ALREADY_CANONICAL` under the governed extension contract.
- Do not erase collisions or hierarchy evidence merely because P3C overrides their effect.
- Do not reopen the architecture abstractly. Change contracts only when a real candidate produces a failed invariant or an unrepresentable case.
- Do not claim closure from summary JSON. Rerun the database, queries, fixtures, reconstruction, and mutation tests.

---

## 16. The trajectory in one paragraph

The project has completed the full survey-question universe and pair-authority layer, built and independently exercised the P3A candidate-construction system, and recorded a nearly complete P3C adjudication run. The authoritative P3C artifacts were lost after R52, while R53 existed only in a disposable test clone. The immediate task is therefore recovery, not new architecture: first search for the R52 Git/database state; failing that, rebuild P3A from the preserved v40 base and rerun P3C using the recorded ledger only as a roadmap. Reproduce R52, independently retest and promote the three R53 special-boundary decisions, close candidate 273 as a redundant direct/constructed prayer split, pass final P3C closure, generate canonical non-GSS J-family authority files, and then run the V550J→V551J→V552J downstream chain.

---

## 17. Safe opening instruction for a new execution agent

Open `00_RECOVERY_START_HERE/README_FIRST.md`, `CURRENT_STATE.json`, `EXACT_RESUME_POINT.md`, and `P3C_EXECUTION_LEDGER.csv`. Treat sections 00–62 as the source-complete executable v40 base. Treat sections 63–80 as non-authoritative recovery records only. First search for an external copy of the R52 worktree at commit `68c3114acad3366380a5e83c0480802dfef6e511` and its PostgreSQL authority database. If neither exists, rebuild from empty PostgreSQL and independently rerun P3C from section 63. Never import the narrative ledger as authority, never promote the recorded R53 claims without executable reproduction, and capture both a Git bundle and a PostgreSQL dump at the next checkpoint.
