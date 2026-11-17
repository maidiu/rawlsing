# GROK_PROOF — D3A independent pre-grok

**Agent:** D3A (ANVIL corrective rabochiy, role A for the D3 pair question). **Not** HQ, **not** final independent C, **not** architecture selector.
**Custody:** worktree `/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/D3A`, branch `agent/anvil-d3a-rabochii-20261117-r1`, base `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`.
**Currentness cut used:** live protected `31291d08179890852246c8742700e055168e9933` (paired PYAT progress revision 10) plus frozen source cuts `596f1230`, `796452b8`, `3cc09bba`; supplied ZIP `526d835d…2332` (280 files, verified).
**Evidence grades used in this file:** (1) source bytes / Git blob, (2) documentary classification, (3) code observed, (4) executed local test, (5) original native/source permission, (6) independent review, (7) competent owner/protected receiving. Nothing here crosses 1→5, 4→6 or 4→7.

> Every probe below states its own **falsifier**: the observation that would defeat the answer. A probe whose falsifier has already fired is marked **FIRED** and the answer is withdrawn.

---

## 1. Why `118 = 29+26+14+10+8+8+7+16`, and why this is not 118 accepted functions

**Answer.** The total is a *mixed identity census*, summed across eight registers of different kinds:

| Register | n | Kind of identity | Source bytes |
|---|---:|---|---|
| K1-CAP-01..29 | 29 | historical capability / conservation rows | `…/K3_HQ_POST_AB_OWNER_DECISIONS_20261116_R1/K3_CONSERVATION_VS_IMPLEMENTATION_29.tsv` blob `a91214b9fd89ab97897ec1c3cd48cb5285b7029c`, 30 lines (1 header + 29 rows), file sha256 `0dfe6539f1a1f7f028c5968c0e85078cbf5f80a847d0c94ea1929f57d20c052d` |
| PYAT-PC-R9/R11/R15 … | 26 | R15 **NOT_ADOPTED** proposals | `K3_R15_26_OWNER_DECISIONS.tsv` blob `1f5a3ae8a40593dccf34753c9fa9577155ebf163`, 27 lines, sha256 `6d0766ecc6…e0dfa2` |
| P4R-R01..14 | 14 | **HELD** unproved proof routes | `K3_P4R_14_OBLIGATION_ROUTES.tsv` blob `5a84ca8cb0a2b16d4a68b2200fa426fd9451b343`, 15 lines, sha256 `8adf74cfbf…eb0e9d3` |
| B-01..B-10 | 10 | SEAM **boundary questions** | SEAM/25 blob `181ab1aaee26d71524dd7401a59c2ca550b4a81c` |
| S-01..S-08 | 8 | SEAM **science-grade contracts** | SEAM/26 blob `a05c21dd0b7b1d404fc500c0ef36c81aee67c96e` |
| L-01..L-08 | 8 | **irreversible-loss risk rows** | ANVIL/15 blob `6253a632d10f201e0bf446f055f96c82fb4a479f` |
| T1..T7 | 7 | **architectural interrogations** | `ANVIL_R7/02_BOUNDARY_CONTRACTS.json`, schema `ANVIL_BOUNDARIES_R3` |
| F1–F8, N9, N10E, N10W, N11, N12, PRE-V3, SEAM, SOROK | 16 | downstream terminal/loss identities | `ANVIL_R7/03_FROZEN_SOURCE_CUTS.json` → `mandatory.TERMINAL` |

**69 exact K3 TSV rows** = 29 K1-CAP + 26 PYAT-PC + 14 P4R. These are the only rows whose bytes are literal TSV records reachable by `git show 31291d0:…`. I re-derived each of the three files from the live protected commit: the recomputed **Git blob ids equal the frozen blob ids exactly**, and my row hashes (`sha256` of the exact raw TSV line, no trailing newline) reproduce deterministically (see `PACKAGE/D3A_INVENTORY_SAMPLE.json`, 118 rows, `PASS_LOCAL_SOURCE_BYTES_ONLY`).

**Why not 118 accepted functions.**
- All 26 PYAT-PC rows carry `HQ_five_test_owner_disposition` = `…NOT_ADOPTED__…` and `new_BUILD = NONE__NO_K4`; the TSV itself says `NOT_ADOPTED__INDIVIDUAL_R15_OWNER_SELECTION_ONLY`.
- All 14 P4R rows carry `HQ_route = HISTORICAL_NAMED_ALIAS_ONLY` / `HOLD_CONDITIONAL` and `protected_receiving = HELD__…NOT_DONE`.
- The 10 B rows are explicitly "requests for the two UMs to locate and adjudicate existing owners, NOT new tasks or proposed components" (SEAM/25 §2).
- The 7 T rows are "seven architectural interrogations, not seven new pipeline stages" (`02_BOUNDARY_CONTRACTS.json` → `meaning`).
- `03_FROZEN_SOURCE_CUTS.json` → `warning`: "118 identifiers form coverage inventory, NOT 118 adopted requirements or semantic proof."

**Falsifier.** Falsified if any one of the 118 identities can be shown to carry a competent adoption/receiving decision at its own grain that I claim it lacks. Concrete check: `grep` for `ADOPTED` in `K3_R15_26_OWNER_DECISIONS.tsv` returns only `NOT_ADOPTED` and `NO_AUTOMATIC_HISTORICAL_PORT`; a single counter-row would defeat the claim. Status: **not fired**.

---

## 2. Why a *source-qualified 118 identity inventory* is lawful at S1, but a final 118→design/hold disposition is only required at the decision

**Answer.** S1 is the *common requirement boundary before architecture selection* (`29_R7_INTEGRATED_MISSION_AND_GATES.md` §S1; `00_R7_READ_FIRST.md` item 1). At S1 the only lawful question about the 118 is: **does each identity still exist, with its original negative, consumer/hold and evidence locator, and can I prove that from bytes?** That is identity accounting, not adjudication. No candidate exists yet, so no per-identity disposition can honestly exist yet.

At S3 a *single proposed strategy* exists (`29` §S3), so each of the 118 must receive one of exactly four non-vacuous dispositions: `PRESENT_PRESERVED`, `FUTURE_NONPRECLUDED`, `EXACT_OWNER_HOLD`, `BLOCKING_LOSS`, "with actual physical consequence and evidence" (`00_R7_READ_FIRST.md` item 3; `01_DECISION_CONSTITUTION.md` line 35).

The defect in the supplied active gate is that S1 demanded an **already-finished R5/R6 `SPINE.json`** (`tools/r7_integrated.py` `check_frame`: `historical_source_spine` schema must be `ANVIL_SPINE_R5|R6` and its `coverage` must equal the transfer's `coverage`). That artifact was the R5 campaign's **expected output**, and R5 records itself as `PREPARED / LOCALLY STRUCTURALLY TESTED / NOT DISPATCHED` (`20_RECOVERY_AND_TEST_PROVENANCE.md` §State). So S1 could only pass by presupposing its own result. That is a circular dependency, not a requirement boundary.

**Falsifier.** Falsified if a genuine, never-dispatched R5 `SPINE.json` with full 118 semantic coverage exists in the supplied evidence or in the pinned source cuts. Bounded search performed: no `SPINE.json` in the 280-file ZIP; none in `evidence/`; `ls` of the ZIP root shows no spine artifact; `20_RECOVERY_AND_TEST_PROVENANCE.md` states the runnable set was not independently recoverable. Status: **not fired**.

---

## 3. What goes wrong when a synthetic source-consistent `SPINE.json` passes a local transfer equality check, and how to source-authenticate

**Answer.** `tools/r7_transfer_conservation.py` checks only three things: the source is labelled `ANVIL_SPINE_R5|R6`, its `coverage` dict has exactly the 118 keys with the five required text fields, and the 26/14 flags are `adopted:false`/`closed:false`. `check_frame` then compares `original['coverage'] != history['coverage']`. **Both sides are attacker-authored JSON.** A fixture built by `test_r6.r6_fixture()` satisfies all of it and passes. Nothing compares any field to a real source byte. Result: a synthetic "original" is promoted to "inherited conservation", and the 118 map's *content* is whatever the fixture author wrote.

**How to source-authenticate (implemented in D3A).** Each row must carry an `origin` object that resolves to real bytes under the supplied `--source-root`:
- `kind` ∈ {`K3_TSV_ROW`, `DOC_ROW`, `JSON_MEMBER`, `TERMINAL_TABLE`};
- `path`, plus exactly one container pin: `commit` (40-hex Git commit) **or** `zip_sha256` (64-hex);
- `git_blob` (40-hex) recomputed locally as `sha1(b"blob <len>\0" + bytes)`;
- `file_sha256`, `row_selector`, `exact_excerpt`, and `row_sha256` (sha256 of the **exact located row bytes**).
The verifier re-opens the file, recomputes the Git blob id, recomputes the row hash and rejects on any mismatch (`SOURCE_FILE_ABSENT`, `GIT_BLOB_ID_DISAGREES`, `SOURCE_FILE_BYTES_CHANGED`, `ROW_NOT_IN_SOURCE`, `EXCERPT_NOT_IN_SOURCE`, `ROW_BYTES_CHANGED`). It then requires the row's `source_semantics` to share ≥2 distinctive tokens with the located row text (`SEMANTICS_NOT_GROUNDED_IN_ORIGIN`), so a row cannot be re-written while keeping an honest locator.

**Falsifier.** Falsified if a synthetic fixture can still obtain `PASS` from `FRAME`. Executed: `test_synthetic_spine_cannot_be_the_origin` and `test_historical_row_meaning_cannot_be_rewritten` in `tools/test_r7_integrated_d3a.py` (both RED as asserted). Status: **not fired**.

---

## 4. Which essential information from V549/V550/V550J/F26 survives irrespective of old Postgres layout, and which historic bugs do not

**Answer.** The surviving inheritance is *semantic function*, not carrier. Per `29_R7_INTEGRATED_MISSION_AND_GATES.md` §S1, the old DDM functions that remain real obligations are: **country preparation, respondent pivots, branch memoization, shared denominators, true same-person k-way joints, temporal / neutral / signed behaviour, and source-selection behaviour** — "treated as real inheritance, corrected for historic errors."

What does **not** survive:
- the old **Postgres/physical layout** — `01_DECISION_CONSTITUTION.md` "Candidate universe" forbids treating a historical persistent backend as universal semantic owner; `00_RAWLSING_GROUND.md` §12 anti-resurrection wall names "PostgreSQL or another persistent backend as universal semantic owner merely because historical code used it";
- the **empty V552 contradiction tensor** — `05_HISTORICAL_FUNCTION_SUCCESSION_AND_WORK_SELECTION_LAW_R1.md`: "Old V552 contradiction tensor is empty; it is not an F5 implementation";
- **V549b / V552 / MI as a current oracle** — `22_R6_VALUE_AND_FUNCTION_CONSERVATION.md` line 13: "no old broken V549b/V552/MI as current oracle";
- the **non-gating V550J FAIL** as a *pass* — it is preserved as a **negative** (`12_ORIGINAL_MANDATE_AND_DECISION_LEVERAGE.md`: "Preserve V550J non-gating FAIL");
- `V551J` certification conflated with `V552` coverage scoring — these stay separate functions (`12`, same row).

**Falsifier.** Falsified if the supplied package anywhere asserts that the historical physical schema is a current requirement, or that V550J FAIL is a success. Bounded search: `grep -n "V550J\|V549\|F26"` across the package resolves to the same five documents, all of which state the negative. Status: **not fired**.

---

## 5. Why matching survey marginals can conceal different true three-way respondent patterns; distinct F2 denominators and typed missing/routing

**Answer.** A triple joint `P(A,B,C)` is not identified by `P(A)`, `P(B)`, `P(C)` — many joint tables share the same marginals. So two populations with *identical* marginal distributions can have completely different three-way respondent configurations. SEAM/26 **S-01** names the exact counterfeit: *"Synthetic product of pairwise marginals declared a rare actual respondent pattern"*; ANVIL/15 **R1** says the same for "high-order same-person patterns that can coexist even when an outsider sees different ideological 'dimensions'".

**Distinct F2 denominators.** SEAM/26 **S-02** requires "F2 **both directions** with **own denominators**" — `P(D|Y) ≠ P(Y|D)` and neither is the transpose of the other; `P(D)` and `P(Y)` are different bases. ANVIL/15 **R2** adds "reverse P(D|Y), context/relative support". A single denominator reused in both directions is a defect (`T2` `must_preserve`: "conditioned risk set, weighted/unweighted denominators, **direction of reverse conditional**").

**Typed missing/routing.** ANVIL/15 **L-03** requires the disposition to distinguish `target eligible / asked / observed / refused / inapplicable / routing unknown`. These are not `0`. `T2` `veto`: "pairwise products, full-body replay per operation, **false zero or unproved negative**". SEAM/26 S-02: "Unobserved/routed minority called impossible or missing treated false" is the rejected outcome.

**Falsifier.** Falsified if the supplied sources anywhere license reconstructing a triple joint from marginals under a measured similarity claim. `01_DECISION_CONSTITUTION.md` "integrated cross-boundary epistemic falsifier" demands a "real 3-variable same-person joint distinction **with fixed marginals**" — i.e. the document itself asserts the insufficiency. Status: **not fired**.

---

## 6. Why a sampled design stratum may not imply measured respondent sect/ancestry; native source vs modelled possibility

**Answer.** A stratum variable describes how the **sample frame** was drawn. It is not a response to a question about the respondent, and it does not tell you that a *released individual field* exists. ANVIL/15 **L-03**: "no reconstructed respondent-level sect from sample stratum metadata"; **L-08**: "External Joshua Project ethnic/diaspora group estimates cannot provide individual Latinobarómetro ancestry … **Do NOT add phantom source respondent identity to C11**". SEAM/26 **S-06** names the same counterfeit: "Wave II 'Muslim' cast as measured sect; independent cross-sections used as longitudinal self". PR #1133's finding (supplied verbatim in `LIVE_GITHUB.json`) lists exactly these three blindspots: "AB II sample stratum vs released respondent sect, GSS religiosity semantics, Latinobarómetro Lebanese-ancestry blindspot".

**Native source vs modelled possibility.** Native source = an actual released question/option/code the respondent answered (grade: `OBSERVED`). Modelled possibility = a derived statement about a population or a generated position (grade: `DESCRIPTIVE_MODELED` / `STRUCTURAL_QUALIFIED`), which may not be written back as an observation. `T4` `veto` makes the collapse explicit: "survey opinion treated as institutional power or **modeled likelihood asserted as causal fact**".

**Falsifier.** Falsified if any supplied source authorizes inferring a respondent's sect from a design stratum. `14_AUTHORITY_TRANSITION_MATRIX` states (quoted in `01_DECISION_CONSTITUTION.md` line 62) that the instrument can distinguish `OBSERVED_SELF / OBSERVED_INTERVIEWER / ASKED_REFUSED / NOT_ASKED / NOT_RELEASED / NOT_ELIGIBLE / HOUSEHOLD_MEASURE / MODELED_PROXY / EXTERNAL_STRUCTURAL / FICTIONAL_ONLY` — a stratum is none of the observed states. Status: **not fired**.

---

## 7. FF01 descriptive, FF02 structural/causal owner, N9/N10W world, SOROK actor psychology — with a negative example

**Answer.**
- **FF01** = *descriptive* position/field description. `T3` producers "F1-F4 and qualified Field Forge **descriptive** machinery"; SEAM/25 §1 assigns "FF01 generic descriptive work **under #1009**".
- **FF02** = *structural/causal owner*, not a descriptive extension. `T4` owners are "PYAT **FF02** N9/N10E/N10W, **independent structural scientist**"; SEAM/25 §1 says FF02 causal power is "HELD unless evidenced" (SEAM/26 S-04).
- **N9 / N10W** = *world* pathway: N9 is the direct material/objective case; N10W is the *conditioned* world route; N10E is the direct empirical route that must remain available. `T4`/`T5`; SEAM/25 **B-03**: "Change authoritative material eligibility holding N10E source slice fixed; **if N10W selected, conditioned option actually changes, not joined-hash only**".
- **SOROK** = *actor psychology and continuing person*, owned elsewhere. `T6` producers are "SOROK admitted actor/world access and event, **not PYAT psyche**"; ANVIL/15 §I **R7** lists identification/alienation/Horizon as "**SOROK OWNER OPEN** … not a C11 semantic quantity".

**Negative example (one concrete).** A WVS/Arab-Barometer attitudinal joint shows that respondents in position X more often endorse a norm. Writing "position X **holds institutional power**" into the world because the norm prevalence is high is the exact T4 veto ("survey opinion treated as institutional power"). The lawful chain is: FF01 describes the prevalence → an **independently sourced** structural relation (control/resources/tenure/sanction) is admitted at its own grade → only then may N9/N10W change a world opportunity, and the survey facts must be unchanged by that change (`T4` `first_effect`).

**Falsifier.** Falsified if any source assigns actor psychology to C11/PYAT, or assigns descriptive FF01 products the power to create institutional relations. `12_ORIGINAL_MANDATE…` "Differentiate survey distributions from material power and actual interpersonal events" states the opposite. Status: **not fired**.

---

## 8. Why producer and verifier agreeing on a hash does not prove source truth; how to test cold revocation and the actor/world firewall

**Answer.** A hash agreement proves only that two parties hashed the *same bytes*. It cannot prove (a) that those bytes are the right source, (b) that the producer did not author both sides of the comparison, (c) that a real machine executed anything, or (d) that the semantic reading is correct. `01_DECISION_CONSTITUTION.md` line 75 says it directly: "Even fully populated numerical arrays are only **matched declared values**, not proof that a real machine executed them. C must read raw instrument/runner evidence." `00_R7_READ_FIRST.md` line 32 adds: "A validated local JSON statement and SHA-checked citation are not proof that its semantics are correct."

What a hash can do is *locate* a byte range inside a container whose identity is independently fixed (Git blob id / zip sha256). That is what D3A implements: the pin is not "we agree", it is "this exact row exists inside this exact container, and here is a reproducible locator".

**Cold revocation test.** Disable or remove the source object, or invalidate the release/permission, then require the downstream read to **refuse**, not to fall back to a cached or default value; then restore and require byte-identical results. Concretely: `T1` `first_effect` "actual source-selected response, weight, routing or permission changes **or refuses** a cold authenticated C11 first read"; `T2` "invalid body/fate denies; **exact restore matches**". D3A enforces this structurally by requiring a `positive`/`negative`/`restore` triple per boundary in `C`.

**Actor/world firewall test.** Change an actor-accessible event into an inaccessible one and require the actor's knowledge to differ; change a fictional performed act and require the real survey bytes to be unchanged; change a real survey answer and require no fictional world state to be written. `T6` `veto`: "survey answers cause mandatory private motives or world change automatically modifies actor state"; `T7` `veto`: "fictional effect edits empirical C11". D3A forbids the corresponding authority upgrades (`FICTIONAL_WORLD→OBSERVED`, `ACTOR_STATE→OBSERVED`, `DESCRIPTIVE_MODELED→STRUCTURAL_QUALIFIED` without an explicit external warrant).

**Falsifier.** Falsified if the supplied package offers any local check that converts a self-consistent hash agreement into an acceptance grade. It does the opposite everywhere (`r7_integrated.py` docstring: "All positives are LOCAL and do not authenticate source rights, independent reviews, runner results, or HQ"). Status: **not fired**.

---

## 9. The seven T1–T7 boundary questions, and why they are neither seven new pipeline stages nor independently accredited science

**Answer.** Verbatim from `02_BOUNDARY_CONTRACTS.json`:

| ID | Question (condensed from `name` + `must_preserve`) | Veto |
|---|---|---|
| T1 | original source → governed canonical evidence: native question/option/code, respondent and occurrence identity, routing, eligibility, missing/not-asked/unreleased, design, authority | irreversible observability loss, or a positive on a denied source |
| T2 | canonical evidence → respondent-coherent computation: true same-person ≥3 joint, conditioned risk set, weighted/unweighted denominators, direction of reverse conditional, minority/routing negatives, replay | pairwise products, full-body replay per op, false zero or unproved negative |
| T3 | empirical computation → differentiated social-field possibility | marginal-only field, impossible proxy identification, unqualified generalization |
| T4 | descriptive field + external structural evidence → objective-world relations | survey opinion as institutional power; modelled likelihood as causal fact |
| T5 | objective possibility → particular fictional world and encounter constraints | respondent becomes character; fabricated kinship; proposed event counted performed |
| T6 | situated encounter → independent developing person | survey answers cause private motives; world change auto-modifies actor state |
| T7 | performed activity → next historical situation | fictional effect edits C11; branch rewrites sealed past |

**Why not stages.** The file's own `meaning` field: "Seven architectural **interrogations**, not seven new pipeline stages, owners or mandatory implementations. Selected direct branches may bypass intermediate products only if their corresponding invariants survive." `29` §"Executable law" repeats: "Retain direct N9/N10E and composed N10W routes rather than imposing a universal T1–T7 runtime chain."

**Why not science.** Each T names a *producer*, *receiver*, *must-preserve*, *first effect*, *veto*, *time class* and *owner*; none of them issues a scientific claim. `status` is `FROZEN_REVIEW_INSTRUMENT_NOT_ADOPTED_PREV3_SCIENCE`.

**Falsifier.** Falsified if any supplied document treats T1–T7 as an execution order or as scientific accreditation. `02`'s `status` and `meaning` fields say otherwise, and `00_R7_READ_FIRST.md` line 12 places FRAME *before* architecture selection. Status: **not fired**.

---

## 10. The decisive acceptance difference: prepared/locally tested R5 tools, source-verified 118 inventory, integrated architecture decision, independent C, protected H1

**Answer.** These are five different *claims*, not five strengths of the same claim.

| Artifact | What it can establish | What it cannot | Evidence |
|---|---|---|---|
| **R5 tools, prepared / locally tested** | the tooling is structurally coherent and its own synthetic tests pass | that the campaign ran, that any source is authentic, that any architecture was selected | `20_RECOVERY_AND_TEST_PROVENANCE.md` §State: `PREPARED / LOCALLY STRUCTURALLY TESTED / NOT DISPATCHED` |
| **Source-verified 118 inventory** | every identity is located in exact bytes; the census is 118; the 26/14 negatives are intact | any semantic truth, any disposition, any science, any adoption | D3A `D3A_INVENTORY_SAMPLE.json` (118 rows, `PASS_LOCAL_SOURCE_BYTES_ONLY`) |
| **Integrated architecture decision** | one candidate maps all 118 to a specific preservation / nonpreclusion / hold / blocking loss, with a typed graph and a builder handoff | independent review, that the mapping is *correct*, that a first reader executed | `r7_integrated.py DECISION` returns `PASS_LOCAL_INTEGRATED_DECISION_PENDING_C` |
| **Independent C** | a distinct non-author inspected the same frame, ran the cold builder and reported positive/negative/restore per boundary | that C is truly independent (external fact), or that the science is true | D3A `C_INTEGRATED` returns `PASS_LOCAL_C_PACKET_ONLY_INDEPENDENCE_UNVERIFIED` |
| **Protected H1** | a competent owner received a specific scope into protected custody | engineering acceptance, native science, actor rights, production readiness | `29` §S5; `00_R7_READ_FIRST.md` item 5 |

The decisive difference is therefore **not** "stronger test suite". It is *which question the artifact answers*. A local PASS at any level never upgrades the claim of the level above it. `01_DECISION_CONSTITUTION.md` line 36 makes this a mandatory terminal separation: `COMMISSION_COMPLETE_YN`, `ARCHITECTURE_DECIDABLE_YN`, `ENGINEERING_ACCEPTED_YN`, `SCIENTIFIC_GRANTED_YN`, `SOURCE_RIGHTS_GRANTED_YN`, `ACTOR_GRANTED_YN`, `PROTECTED_RECEIVED_YN` — "One YES does not imply any other."

**Falsifier.** Falsified if any supplied gate returns a single global "accepted" that collapses these levels. The supplied `r7_integrated.py` is careful here (its PASS strings embed `PENDING_C` / `ONLY`); D3A preserves that property and adds `C:FALSE_PROTECTED_H1` as a hard RED. Status: **not fired**.

---

## Pre-grok result

**`READY_FOR_BOUNDED_COMMISSION`** — all ten answers are materially supported by byte-located sources, and no source or authority fiction was needed.

Limits recorded honestly:
1. I did **not** read the optional independent forensic `ANVIL_118_FORENSIC_AUDIT.md`; no bounded local search found it in the supplied evidence (`find evidence -iname '*FORENSIC*'` empty) and it is not in the 280-file ZIP. No audit finding is invented; the original sources were tested directly instead.
2. PR #1097's ZL-15 estate (52/24/21) is treated **only** as a separate, differently-grained historical register. It is not summed with the 118 and I did not re-mine it.
3. The `53`/`38` artifacts of unaccepted commit `4913b562…` were **not** used as a baseline and get no credit. The earlier frame is an unaccepted challenge fixture only.
4. Terminal F1–F8/N9–N12/PRE-V3/SEAM/SOROK semantics are bound in my instrument at **documentary token grade** via `D3A_TERMINAL_ORIGINS.json`; a deciding author must still supply their operative definitions.
5. All local PASS results are sourcefree/synthetic + documentary. **No native 100k run, no owner receiving, no science, no actor rights, no protected H1.**
