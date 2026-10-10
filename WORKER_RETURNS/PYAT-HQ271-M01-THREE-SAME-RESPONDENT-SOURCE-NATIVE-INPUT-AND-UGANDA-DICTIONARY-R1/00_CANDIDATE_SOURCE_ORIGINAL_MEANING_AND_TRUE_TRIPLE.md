# PYAT HQ271 M01 — Same-respondent three-variable source-native candidate selection

**Commission:** `PYAT-HQ271-M01-THREE-SAME-RESPONDENT-SOURCE-NATIVE-INPUT-AND-UGANDA-DICTIONARY-R1`
**Commission file:** `WORKER_COMMISSIONS/PYAT-HQ271-M01-THREE-SAME-RESPONDENT-SOURCE-NATIVE-INPUT-AND-UGANDA-DICTIONARY-R1/00_COMMISSION.md`
**Commission tip:** `3332c2a3a85cb7e42a11c554fa2503fd472d406e` (= exact working HEAD used)
**Frozen control base:** `8b02d85a2fcd8acb6fe266543821434ef63ccb07`
**Branch:** `agent/rabochii-pyat-hq271-m01-exact-three-respondent-role-and-dictionary-court-r1`
**Repository:** `maidiu/rawlsing`

## 0. Execution provenance (no invented model/machine)

| Field | Value |
|---|---|
| Exact worktree | `/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/hq271/m01` (git worktree of `/Users/matthewsmith/Desktop/as2b-lits1-DiSDJn/repository`) |
| Worktree HEAD at start and end | `3332c2a3a85cb7e42a11c554fa2503fd472d406e` (clean; zero uncommitted changes before work) |
| Host | MacBookPro15,1 (Intel Core i9-9880H), macOS 13.2.1 build 22D68, Darwin arm64-independent |
| Execution surface | opencode CLI, local, single-threaded; no network fetch of survey data |
| Interpreter | CPython 3.11.3 (`/usr/local/bin/python3`), `pyreadstat` 1.3.2 |
| Model | **Launch-declared: MiMo V2.6-Flash.** The executing harness self-identifies as `opencode-go/step-5-preview-free`. This discrepancy is reported rather than resolved: **no model-identity claim in this return is independently certified from repository state.** Model provenance must not be quoted from this document as a certified fact. |
| Physical source census performed | `data/Data/` contains **exactly 44** `.sav`/`.dta` originals, including `LiTS_I.dta`. The launch's machine claim is verified. |
| Commissioned work performed | documentary source selection + bounded metadata dictionary gate only. |

**Sealed HQ271 resolved on start:** worktree detached HEAD `3332c2a3a` == the exact commission tip; frozen control base `8b02d85a2` present as HEAD~1; `origin/integration/staging-pyat-hq271-intake-r1` (`e3a2e7c5a`) read as the sealed HQ271 adjudication `HQD-2026-10-09-271`. That adjudication **refused** the existing LiTS S1 triple and **issued** this M01 court. No post-checkpoint movement was performed by this worker.

---

## 1. Comparative court — option (b) LiTS is REFUSED (independently corroborated)

### 1.1 Retained-authority ground truth (unchanged, not re-derived)

HQ270 L01 `edd95a71c279e6c4fd164f287bada73985220ee7` established, from the retained 3.4 GB I05 checkpoint `/Users/matthewsmith/Desktop/Rawlsing/LOCAL_CUSTODY/.../current_i05_materialization_checkpoint_v3.json`:

* AS2A projection authority `urn:rawlsing:pre553:as2a:lits1-projection-authority:sha256:9dd1e6b7…` admits **exactly two** `RespondentEvent` slots: `q301_2` and `q301_7`, both at `EXACT_SAME_RESPONDENT_ONLY`.
* `q310` and `q311` appear **only** as `SURVEY_RESPONSE_EVENT` condition leaves in `EmpiricalPredicate` ASTs, sourced from a **different release lineage** (`urn:rawlsing:prev3:f02:lits1-q310-question:sha256:c4b0f76b…`, release `LITS1-F02-C11-7cac43e2ca5b31cb-bf305bf3f169d669`).
* Every stratum query that adds `q310` carries the binding token `EXACT_MIXED_RESPONDENT_REFINEMENT__3ef0317887f6910838636d3816237a81d5a56b38e07595c8cc1f7c5e7f1fae74` — i.e. the third item is joined at a **mixed-respondent grain**, not co-travelled on the same `RespondentEvent` respondent as `q301_2`/`q301_7`.

### 1.2 New independent corroboration from the original instrument (this worker)

The local original `data/original codebook pdfs/LiTSI_Questionnaire.pdf` (36 pp.) was read as **document text only** — no DTA was opened, decoded or hashed. Findings:

1. **Section 3 is a re-selected-respondent module.** Page 9 header, verbatim:
   > *"Section 3. Attitudes and Values — INTERVIEWER: THANK THIS RESPONDENT AND ASK TO SPEAK TO THE PERSON WHO LAST HAD A BIRTHDAY IN THE HOUSEHOLD/ YOU HAVE SELECTED USING THE KISH GRID. IF THIS PERSON IS THE SAME RESPONDENT YOU ARE INTERVIEWING NOW, CONTINUE WITH THE INTERVIEW. IF DIFFERENT RESPONDENT REPEAT THE INTRODUCTION IF NECESSARY."*

   So the `q301_*` block is administered to a **Kish-grid / last-birthday selected person who is explicitly permitted to differ** from the household respondent of Sections 1–2 and 5. Same-respondent identity for items inside Section 3 is therefore a *proved per-item property*, not a structural given — which is exactly why the retained authority had to type `q301_2`/`q301_7` as proved and `q310`/`q311` as mixed.

2. **`q310` and `q311` are identified as `Q.3.10` and `Q.3.11`** (pdf pp. 12–13), both inside that same re-selected module:
   * `Q.3.10` — *"With which one of the following statements do you agree most … A market economy is preferable to any other form of economic system / Under some circumstances, a planned economy may be preferable / For people like me, it does not matter"* (1/2/3).
   * `Q.3.11` — *"With which one of the following statements do you agree most … Democracy is preferable … / authoritarian government may be preferable / it does not matter"* (1/2/3).

3. LiTS `D02_P3_CONDITIONAL_REVERSAL` remains `VALID_EMPTY` (never an observed reversal); `D02_P1` joint and 25 nonmodal candidates remain supported **at raw, unweighted, mixed-grain scope**. Quoting any of these as an S1 three-variable positive is falsified.

**Verdict: `LITS_I_THREE_WAY_SAME_RESPONDENT_REFUSED`.** A genuine LiTS three-variable same-respondent input would require *new respondent-identity proof on the retained checkpoint itself* (a different court). It cannot be produced by naming a third question.

---

## 2. Comparative court — option (a) Afrobarometer R5 Q86A/Q86B/Q86C is the QUALIFIED CANDIDATE

### 2.1 Why this option survives the court

| Court requirement | R5 Q86A/Q86B/Q86C |
|---|---|
| Three **distinct** bona fide respondent events | Yes — three separate scalar questions (`Q86A`, `Q86B`, `Q86C`), three separate `QUESTION_IMPLEMENTATION` identities, three separate `RespondentEvent` slots. Not three columns of one item. |
| **Same persons** | Yes — all three sit in one `Q86` block under **one shared stem**, in one release, on one respondent carrier (`RESPNO`), with **no re-selection and no household swap** anywhere in the block. |
| No cross-person join | Yes — every slot is projected from the same `RowRespondentBinding` on the same C11 release. |
| Existing two-variable precedent | Yes — SRC02 GT1 `GT1_R5_Q86A_RAW_UNARY_EXACT_RISK_SET@1` and GT2 `GT2_R5_Q86A_X_Q86B_RAW_JOINT_EXACT_RISK_SET@1` already exist at raw unweighted scope with a frozen risk set. |
| Third variable already physically present | Yes — verified in the physical dictionary (§3). Q86C is not an aspiration; it is already in the file with the identical native domain. |
| Release-bound source authorization | Yes — `Data/Afro Barometer Round 5.sav` @ SHA256 `c9200ba3…` (verified this run) and `merged_r5_codebook_2.pdf` @ SHA256 `7e02c649…` (verified present and hash-matching the frozen authority). |

### 2.2 Exact true question stems (governed R5 codebook, printed p. 53)

The stems below are transcribed from `data/Afrobarometer/merged_r5_codebook_2.txt` (= `Afro Bar r5_codebook.pdf`, SHA256 `7e02c649c8ae69c61f88c116fdad92353b7f06cba9e160d9ae4be18e72276735`, verified). Q86A/Q86B/Q86C fall on printed page 53 (footer *"Copyright Afrobarometer 53"* immediately precedes `Q86A`), corroborating the frozen authority's `"page": 53`.

Shared stem (all three items):

> *"In your opinion, which of the following people have a right to be a citizen of the country? A citizen would have the right to get a passport and to vote in national elections if they are at least 18 years old:"*

| Item | Item-specific completion | Codebook variable label | Codebook `Values:` line | Codebook value labels |
|---|---|---|---|---|
| `Q86A` | *"A person born in the country with one national and one non-national parent?"* | *Right to be citizen: born in country with one non-citizen parent* | `0, 1, 9, 998, -1` | `0=No, 1=Yes, 9=Don't know, 997=Not asked, 998=Refused to answer, -1=Missing` |
| `Q86B` | *"A person born in the country with two non-national parents?"* | *Right to be citizen: born in country with two non-citizen parents* | `0, 1, 9, 998, -1` | identical |
| `Q86C` | *"The wife of a national man, even if she was born outside of the country?"* | *Right to be citizen: wife of citizen husband* | `0, 1, 9, 998, -1` | identical |

Routing exception for all six items `Q86A`–`Q86F`, printed on each: *"Not asked in ALG, EGY, MRC, SUD, TUN"*. Crucially, `Q86A`, `Q86B` and `Q86C` carry the **identical** exception list and the **identical** value domain — so their eligibility regimes coincide exactly, which is what makes the minimal extension possible (see §5).

**Codebook internal inconsistency, recorded not repaired:** each item's `Values:` line lists `0, 1, 9, 998, -1` and **omits `997`**, while the same item's `Value Labels` line includes `997=Not asked`. The physical SAV dictionary confirms `997` is a real, stored, labelled state (§3.3). The frozen `Q86_NATIVE_STATES` tuple is therefore correct to include `997`, and the printed `Values:` range line must not be used as the authoritative domain.

### 2.3 Physical dictionary confirmation (this run, metadata only)

All three variables are present in `Afro Barometer Round 5.sav` with these exact source-native labels:

| Variable | Physical label | Physical value labels (verbatim) |
|---|---|---|
| `Q86A` | `Q86a. Right to be citizen: born in country with one non-citizen parent` | `0=No`, `1=Yes`, `9=Don't know`, `997=Not asked`, `998=Refused`, `-1=Missing` |
| `Q86B` | `Q86b. Right to be citizen: born in country with two non-citizen parents` | identical |
| `Q86C` | `Q86c. Right to be citizen: wife of citizen husband` | identical |

Reconciliation note for HQ: the physical label for `998` is **`Refused`**, whereas the frozen `Q86_NATIVE_STATES` and the codebook say **`Refused to answer`**. The *codes and response-state typing* match the frozen authority exactly; only the label string differs. This is a label-string reconciliation item, not a domain defect, and must not be silently harmonised.

### 2.4 Item identity, respondent unit, routing

* **Item identity:** `question_impl.phase0.67f036c0efb7fb98ff4a` (Q86A, identity sha `67f036c0…`), `question_impl.phase0.2fb3a62609dad4c1306d` (Q86B, identity sha `2fb3a626…`). Q86C has **no frozen qimpl identity** — obtaining one is part of the adoption ask (§5).
* **Respondent unit:** one admitted interview, keyed `(COUNTRY, RESPNO)` on carrier `FFP014_R5_CURRENT_RESPONDENT_CARRIER@1`. Unique-one-to-one uniqueness is already enforced by the frozen producer (`wave1_r5_q86_c11_projection.py:387`).
* **Routing / common risk set:** `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`, member-set SHA256 `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`, **19,210 members**, exact country scope `{BFO, BOT, CVE, KEN, LES, MAU, MLW, MOZ, NAM, SAF, UGA}` — a scope *proved by FFP017 evidence to equal* the 12-measurement common-coexposure set for the admitted respondents, not merely asserted.
* **Release:** `Data/Afro Barometer Round 5.sav`, 51,587 rows, 348 columns, SHA256 `c9200ba3…`; governed codebook `merged_r5_codebook_2.pdf` @ `7e02c649…`; measure basis `AS3_QUERY_MEASURE_BASIS` **RAW**, unweighted, `weighted_support_authorized: false`.

### 2.5 Can an authenticated producer build both q(Y|A) and q(Y|A,B) without cross-person join?

**Yes.** The existing producer `rawlsing_next/wave1_gt12_i03_positive_facts.py` already carries a two-way `EmpiricalQuerySpec` whose `target_refs` are `(q86b, q86a)` with `target_arity_and_topology.arity = 2` and `joint_order_semantics = "SEMANTIC_ORDERED"`, over the same frozen predicate `_predicate_for_members` (`same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT"`, operator `DERIVED_BRANCH_COHORT`). Adding a third target is a *same-codepath* arity change to `(q86b, q86a, q86c)` over the **identical** predicate and the **identical** risk-set member set. No numerator/denominator is built from independent marginals; both operations resolve over the same 19,210 exact member refs.

### 2.6 Scientific reading, and its honest limitation

**Construct.** The three items measure one thing at three nested distances: `Q86A` is *partial jus soli* inclusion (born in-country, one national parent), `Q86B` is the strict *descent-only* boundary (born in-country of two non-nationals), `Q86C` is *kinship-based* inclusion of a foreign-born wife of a national man. A respondent can hold a coherently liberal position on `Q86A`, a restrictive one on `Q86B`, and either position on `Q86C`.

**Candidate estimand.** `q(Q86A = Yes | Q86B = 0 "No", Q86C = w)` — i.e. whether support for citizenship of the partially-insider child tracks the strict bloodline boundary **conditional on** the respondent's stance on gendered kinship transmission. The two-variable predecessor `q(Q86A | Q86B)` is already the authorised GT2 fact; the third variable asks whether the A–B relationship is stable across the C dimension or reorders within it.

**Limitation, stated rather than hidden.** Q86A/Q86B/Q86C is a **within-block, attitude-only battery**: three items of a single construct under one shared stem. The commission's stated preference was for heterogeneous combinations of material/social position, reported behaviour and attitude. That preference is *not satisfied* by this candidate, and HQ should not pretend otherwise. The trade-off is explicit: this is the **smallest possible positive authorization** (one item added to an already-frozen two-item projection over an already-frozen risk set), at the cost of construct heterogeneity.

**Superior heterogeneous alternative, and its exact price.** Within the same physical file, with no cross-person join, a genuinely heterogeneous triple is available:

* `Y = Q86A` (attitude: partial jus soli inclusion) — domain `{0,1,9,997,998,-1}`
* `A = Q8A` (reported experience: *"Over the past year, how often, if ever, have you or your family gone without: Enough food to eat?"*) — domain `{0,1,2,3,4,9,998,-1}`, **no `997`**
* `B = Q97` (social position: *"What is the highest level of education you have completed?"*) — domain `{0…9, 99, 998, -1}`, **no `997`**

This combines reported material experience, social position and attitude. Its price is that **none** of the three has any existing frozen domain, risk set, target-use permission or authority snapshot; and because `Q8A`/`Q97` carry no `997` "Not asked" state while `Q86A/B/C` do, the eligibility intersection is a **new, separately-adjudicated risk-set construction** with genuinely different not-asked regimes — not a free extension of the existing one. HQ should choose this only if it is willing to fund three fresh domain/routing adoptions.

**Recommended for the first executable court:** the Q86C extension. It is the smallest lawful step toward a real source-backed `q(Y|A) → q(Y|A,B)`, and it converts an existing two-variable authority into a three-variable one without inventing any new respondent identity, universe, coordinate or risk set.

### 2.7 No fabricated pressure indicator

No structural-pressure, personality, essentialist or latent-trait indicator is proposed or implied. The proposal uses only three source-native, separately-coded, interviewer-administered scalar questions whose native states are preserved verbatim (`0`, `1`, `9`, `997`, `998`, `-1`). No numeric code is granted order or metric authority, no state is collapsed, and no harmonisation is applied.

---

## 3. What this candidate does **not** authorise

* Not permission to read any respondent row, cell, or frequency. Nothing in this return implies any empirical execution.
* Not a grant of `withinwt` / `combinwt` (R5) or `withinwt_ea` / `withinwt_hh` / `Combinwt_new_hh` / `Combinwt_old_ea` (R9) use. Those variables merely exist by name (§4).
* Not a `TARGET_USE_PERMISSION` for a three-way operation. The existing GT1/GT2 target-use ceiling stops at arity 2. Extending it is an adoption HQ must make (§5).
* Not an EE12 / C7 temporal pair warrant, and not a Uganda trend or wave-difference.
* Not an R5 `Q86C` semantic adoption. Naming the question is not authorising it.
* Not a PRE-V3 / V3 / actor admission, and not an F02 or N9 field-forge relation.
* Not an answer to the Uganda national-vs-supplement record-selector question. See §4.

---

## 4. Preserved independently: LiTS S2

LiTS **S2 minority-context FF02** remains available **independently of** the S1 choice above: `ff02_executed=false`, `structural_admission_created=false`, `structural_admission_object_count=0`, `status=FF02_READY__NO_SOURCE_REOPEN_REQUIRED`. Selecting or refusing the R5 S1 triple neither advances nor blocks S2. S2's 50 discovery receipts (`D02_P1` joint, `D02_P3` `VALID_EMPTY`, 25 nonmodal, 23 bounded-k-way) remain at raw, unweighted, mixed-grain scope.

---

## 5. Summary verdict

`SOURCE_NATIVE_TRIPLE_QUALIFIED__AFRO_R5_Q86A_Q86B_Q86C__LITS_I_REFUSED__NO_SELF_ADOPTION`

Full permission analysis: `02_EXACT_PRODUCER_OPERATION_PERMISSION_AND_FIRST_EXECUTABLE_COURT.md`.
Full physical dictionary evidence: `01_FILE_SHA_DICTIONARY_AND_NATIONAL_SAMPLE_METADATA.json`.

**Terminal:** `HQ271_M01_RETURNED_FOR_HQ__NO_SELF_ADOPTION`
