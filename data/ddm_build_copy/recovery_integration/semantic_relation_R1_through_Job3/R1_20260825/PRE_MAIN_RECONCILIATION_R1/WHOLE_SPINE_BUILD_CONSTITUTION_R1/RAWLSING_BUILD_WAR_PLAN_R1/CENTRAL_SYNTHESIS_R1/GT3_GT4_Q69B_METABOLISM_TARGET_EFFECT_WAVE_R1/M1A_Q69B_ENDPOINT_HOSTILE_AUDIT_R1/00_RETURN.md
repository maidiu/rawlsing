# GT3/GT4 M1A — Q69B ENDPOINT HOSTILE AUDIT R1 — RETURN

## Terminal

`FAIL__GT34_M1A_Q69B_ENDPOINT_HOSTILE_AUDIT__EXACT_DEFECT`

Exact defect:

`COORDINATE_SEMANTICS_AUTHORITY_OVERGRANTS_EMPIRICALPREDICATE_OUTSIDE_COORDINATE_JURISDICTION`

The Q69B source semantics and the guarded relation to ADP-010 `ENCOUNTER` survive hostile review. The L1A authority package does not survive unchanged because its `COORDINATE_SEMANTICS` candidate names `EmpiricalPredicate@1.0.0` as a governed object family even though current PRE553 law reserves predicate/operator/query grammar to `PREDICATE_GRAMMAR`, and K1 already proved that D08 predicate grammar exists.

This is an adoption-blocking authority-scope overgrant, not a source-semantic failure.

---

## Scope and ancestry

Repository:

`maidiu/rawlsing`

Worker branch:

`agent/rabochii-gt34-m1a-q69b-endpoint-hostile-audit-r1`

Exact required working start:

`913f2274bfb5a2b204a8666b34aa1b658eb86966`

Immutable instruction evidence ref:

`8e81c1d2e6351a7363494a1aa1ea16a8395519d5`

Executed only:

`WORKER M1A — Q69B ENDPOINT HOSTILE AUDIT R1`

Profile:

`HOSTILE_AUDIT`

No implementation.
No adoption.
No source-row execution.
No PSEPF.
No actor mutation.

---

# Audit target

L1A return:

`.../GT3_GT4_ENDPOINT_METABOLISM_RESPONSE_WAVE_R1/L1A_R5_ENDPOINT_FOR_OWNED_ACTOR_FACT_R1/00_RETURN.md`

L1A return blob:

`61bc38779198980c9941abe7d8e174285ef94010`

L1A candidate endpoint:

`Afrobarometer R5 Q69B -> PUBLIC_CLINIC_EXPERIENCE_STATUS`

L1A candidate authority:

`R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY@1.0.0`

claimed authority-content hash:

`3484a855a4726ffb1e13776bf57e17fa226a41e237b92f2e89f8fe443a90453a`

actor-side owner:

`ADP-010 / V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0`

actor-side candidate state:

`ENCOUNTER / OEE_ENCOUNTER_OCCURRED`

---

# Holding

The endpoint's **source-semantic core is valid**:

- Q69B is the cited local public clinic-or-hospital past-12-month problem item.
- Its source-native code `7` explicitly means no experience with public clinics in the last 12 months.
- The B-F interviewer rule makes code `7` an all-or-none clinic-experience applicability state across those items.
- Therefore Q69B codes `0-3` are lawfully on the clinic-experience-present branch even when code `0` means the named problem itself occurred zero times.
- Collapsing `0-3` to a boolean experience-present conditioner while discarding their frequency ordering is semantically narrower than the source and does not invent the named shortage problem in generated actor history.
- `9`, `998`, and `-1` remain nonpositive typed states.
- `DATEINTR` is an exact source-native interview-date field and is a lawful anchor for the source's "past 12 months" window.
- ADP-010 `ENCOUNTER` is the narrowest actor-side positive fact that can match this source applicability state; `EXPOSURE` would be stronger than the source requires.
- The actor guard correctly requires an independently authoritative `subject_ref` resolving to public-clinic-or-hospital contact/use.
- Silence in generated actor history is correctly forbidden as evidence of empirical absence.
- No portability, pooling, source mixing, weighted estimand, or population-rate authority is claimed.
- The old Q86 release remains immutable and a new bounded C11 release is required.

The endpoint route therefore remains repairable.

The exact defect is confined to the **authority envelope**.

---

# Source-semantic evidence

Accepted source identity:

`Data/Afro Barometer Round 5.sav`

SHA-256:

`c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`

accepted row count:

`51,587`

accepted respondent carrier:

`FFP014_R5_CURRENT_RESPONDENT_CARRIER@1`

respondent-carrier SHA-256:

`6c2277e8832c8f070d1213f8f68adf54f115e4978f59702d150ab69fffd4a6d5`

accepted source structure:

`cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4`

source-structure SHA-256:

`ea9614b69e63a8e5bc87e65c944d67445082639fe45262da626bd6aa1a4d9e99`

Accepted/recovered codebook:

`merged_r5_codebook_2.pdf`

accepted SHA-256:

`7e02c649c8ae69c61f88c116fdad92353b7f06cba9e160d9ae4be18e72276735`

The exact accepted/recovered codebook bytes were available to this audit. No source-row execution was performed.

## Q69B exact source text

Question number:

`Q69B`

Question:

> Have you encountered any of these problems with your local public clinic or hospital during the past 12 months: Lack of medicines or other supplies?

Variable label:

`Problems with public clinic: lack of medicine/supplies`

Source-native values:

`0-3, 7, 9, 998, -1`

Source-native labels:

- `0 = Never`
- `1 = Once or twice`
- `2 = A few times`
- `3 = Often`
- `7 = No experience with public clinics in last 12 months`
- `9 = Don't know/Haven't heard enough`
- `998 = Refused to answer`
- `-1 = Missing`

Source:

`Afrobarometer Round 5`

Interviewer rule:

> For parts B-F, either ALL parts of the question should be coded as 7=No experience with clinics, or NONE of the parts should be coded as 7.

This rule is decisive for the `0-3 -> PRESENT` reduction. It prevents code `0` from being misread as "no clinic experience." Code `0` is "never encountered this named problem" inside the experienced-clinic branch.

Q69A immediately preceding Q69B carries the same public-clinic-or-hospital stem. Q69C-F repeat the same stem and B-F applicability rule. The source block therefore supports an applicability interpretation and not merely a variable-name inference.

---

# DATEINTR evidence

Exact source field:

`DATEINTR`

Question:

`Date of interview`

Variable label:

`Date of interview`

Source values:

`20.10.11 – 04.06.13`

Source note:

`Answered by interviewer. Entered in day, month, and year format`

Therefore the L1A time rule is source-grounded:

`R5_Q69B_SOURCE_NATIVE_PAST_12_MONTHS_AT_DATEINTR@1.0.0`

The source does not provide an explicit inclusive/exclusive mathematical edge convention for "past 12 months." L1A correctly refuses to invent one and classifies an actor event exactly on a disputed boundary as noncomparable until separate calendar-boundary authority exists.

That is fail-closed and lawful.

---

# ADP-010 evidence

Accepted authority artifact:

`data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W1_CRITICAL_AUTHORITY_EXPANSION/ADP_010_V3_ENCOUNTER_EXPOSURE/AUTHORITY.json`

blob:

`0eac41d081b112255dcfc6dd42a6afab15a2928b`

Accepted authority:

`V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0`

Registry:

`V3_OEE_REALIZATION_RULE_REGISTRY@1.0.0`

Owner:

`V3_ACTOR_DEVELOPMENTAL_CAUSALITY_ENGINE`

Relevant accepted state semantics:

- `OPPORTUNITY` = actor-specific possibility of contact/access; no occurrence.
- `ENCOUNTER` = admitted contact occurrence under opportunity; no exposure/downstream effect.
- `EXPOSURE` = admitted objective presentation/impingement through encounter.

Relevant positive event effect:

`OEE_ENCOUNTER_OCCURRED`

Relevant core rule:

`OEE_CORE_ENCOUNTER_FROM_EXPLICIT_CONTACT_WITNESS_V1`

ADP-010 requires an exact contact witness and explicitly rejects co-location, co-presence, same institution/category, and narrative plausibility as sufficient encounter evidence.

Its hostile fixture `HF-010-22` also rejects a mere meeting label without a witness rule.

Therefore L1A is correct not to derive an actor encounter from Q69B or from a label. Its future positive comparator may consume only an encounter that has already been lawfully admitted by ADP-010 and whose subject semantics are independently owned.

This preserves the cross-ontology boundary.

---

# PRE553 authority-law defect

Current PRE553 authority law:

`rawlsing_next/pre553_empirical_authority.py`

blob:

`6714340facfe186c6cc521884cc85ab6340ad989`

defines distinct authority kinds:

- `COORDINATE_SEMANTICS`
- `PREDICATE_GRAMMAR`
- `TARGET_USE_PERMISSION`

and gives their ceilings separately:

`COORDINATE_SEMANTICS`

> empirical coordinate identity/value/unit/taxonomy

`PREDICATE_GRAMMAR`

> empirical predicate/operator/query grammar

`TARGET_USE_PERMISSION`

> exact target-use permission

Exact authority resolution is fail-closed and does not infer adjacent semantic jurisdiction.

Current PRE553 predicate law:

`rawlsing_next/pre553_empirical_objects.py`

requires `EmpiricalPredicate@1.0.0` to carry a separate `grammar_authority_ref` and exact operator/coordinate references.

Current query evaluation:

`rawlsing_next/_pre553_query_predicate.py`

accepts an `EMPIRICAL_POSITION_COORDINATE` predicate leaf with an exact `coordinate_authority_ref` binding the coordinate fact. It does not require the coordinate authority itself to become the predicate-grammar owner.

K1 independently banked:

> The blocker is also not D08 predicate grammar. That exists.

K1's exact prerequisite was one accepted source-specific coordinate plus explicit D08 conditioner-use authorization, not a new predicate-grammar owner.

## L1A overgrant

The L1A candidate authority material says:

`kind = COORDINATE_SEMANTICS`

but its governed families are:

- `EmpiricalCoordinateFact@1.0.0`
- `EmpiricalPredicate@1.0.0`

That second family is outside the coordinate-semantics ceiling.

The candidate therefore does more than add the missing Q69B coordinate semantics and D08 conditioner-use ceiling. It also claims authority over the public predicate family whose grammar is separately owned.

That is semantic authority widening.

It is not cured by the fact that the content hash recomputes correctly.

---

# Existing Q86 precedent confirms the boundary

Current accepted R5 country coordinate authority:

`GT12-A-R5-COUNTRY-ALPHA3@1.0.0`

kind:

`COORDINATE_SEMANTICS`

governed family:

`EmpiricalCoordinateFact@1.0.0`

only.

Its operation/use ceiling is routing-specific:

`R5_COUNTRY_ALPHA3_SOURCE_NATIVE_ROUTING_IDENTITY`

`ROUTING_SOURCE_IDENTITY_ONLY`

K1 correctly held that this authority could not be silently widened into D08 conditioner use.

The lawful repair pattern for Q69B is therefore:

1. create/accept a Q69B coordinate-semantics authority;
2. make its coordinate-use ceiling explicitly permit the exact D08 conditioner role;
3. keep its governed public family at `EmpiricalCoordinateFact@1.0.0`;
4. reuse the already-existing D08 predicate grammar for any later comparator-produced `EmpiricalPredicate`;
5. do not make the Q69B coordinate authority a predicate-grammar authority by listing `EmpiricalPredicate@1.0.0`.

---

# Hash hostile audit

All six L1A claimed semantic hashes were independently recomputed under the current PRE553 canonical semantic JSON law.

## Crosswalk

ID:

`R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_STATUS_CROSSWALK@1.0.0`

claimed:

`fde63966f0d8204d698047eb38d64faa2230543dff62928cdc513cdf56aae095`

recomputed:

`fde63966f0d8204d698047eb38d64faa2230543dff62928cdc513cdf56aae095`

Result:

`EXACT_MATCH`

## Time rule

ID:

`R5_Q69B_SOURCE_NATIVE_PAST_12_MONTHS_AT_DATEINTR@1.0.0`

claimed:

`4a771c6a27703bde285cedfe7b97da8bc29e953ef068ba22354e8af3f1fe6cf2`

recomputed:

`4a771c6a27703bde285cedfe7b97da8bc29e953ef068ba22354e8af3f1fe6cf2`

Result:

`EXACT_MATCH`

## Measure basis

ID:

`R5_Q69B_RAW_CONDITIONER_MEMBERSHIP_BASIS@1.0.0`

claimed:

`f2a33c3674e924cb535038e96554f838616c034141e265aa391c864f53f2c1c3`

recomputed:

`f2a33c3674e924cb535038e96554f838616c034141e265aa391c864f53f2c1c3`

Result:

`EXACT_MATCH`

## Coordinate

ID:

`Afrobarometer/R5:Q69B:PUBLIC_CLINIC_EXPERIENCE_STATUS`

claimed:

`7a9910beead34e2617f5fdbacdd762fdde89b3614b90444c2e30f61a1a601937`

recomputed:

`7a9910beead34e2617f5fdbacdd762fdde89b3614b90444c2e30f61a1a601937`

Result:

`EXACT_MATCH`

## Candidate authority

ID/version:

`R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY@1.0.0`

claimed:

`3484a855a4726ffb1e13776bf57e17fa226a41e237b92f2e89f8fe443a90453a`

recomputed:

`3484a855a4726ffb1e13776bf57e17fa226a41e237b92f2e89f8fe443a90453a`

Result:

`EXACT_MATCH__BUT_HASHED_MATERIAL_IS_OVERBROAD`

## Actor relation proof

ID:

`GT34_L1A_Q69B_TO_ADP010_ENCOUNTER_RELATION_PROOF@1.0.0`

claimed:

`7eaa5197a26c3e5ddc65b631453007f2a5ed9ba9310da6c9c233eaef6fb12aa9`

recomputed:

`7eaa5197a26c3e5ddc65b631453007f2a5ed9ba9310da6c9c233eaef6fb12aa9`

Result:

`EXACT_MATCH`

Thus audit item 13 passes mechanically.

The failure is jurisdictional, not cryptographic.

---

# Smallest exact repair

Change only the candidate authority's governed-family set from:

`["EmpiricalCoordinateFact@1.0.0", "EmpiricalPredicate@1.0.0"]`

to:

`["EmpiricalCoordinateFact@1.0.0"]`

while preserving:

- Q69B source identity;
- native domain;
- crosswalk;
- DATEINTR time rule;
- raw measure basis;
- coordinate identity;
- D08 conditioner-use scope;
- no-portability ceiling;
- predecessor-release immutability;
- ADP-010 relation proof and guards.

With that one semantic-field repair, the mechanically recomputed candidate authority-content hash is:

`cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c`

This audit does **not** create, adopt, or authorize that repaired candidate.

It is reported only as the deterministic consequence of removing the exact overgrant.

The old claimed authority hash:

`3484a855a4726ffb1e13776bf57e17fa226a41e237b92f2e89f8fe443a90453a`

must not be adopted as-is.

---

# Fifteen-point hostile court

| # | Audit question | Ruling | Evidence / reason |
|---|---|---|---|
| 1 | Exact Q69B question? | PASS | Codebook Q69B is the cited local public clinic-or-hospital past-12-month lack-of-medicines/supplies item. |
| 2 | Do 0-3 imply clinic/hospital experience? | PASS | B-F code-7 all-or-none applicability rule makes 0-3 the experienced-clinic branch. |
| 3 | Does 7 exactly mean no experience? | PASS | Source label explicitly says no experience with public clinics in last 12 months. |
| 4 | 9/998/-1 typed/nonpromotable? | PASS | Unknown/refusal/missing preserved; no positive promotion. |
| 5 | Collapse 0-3 to PRESENT lawful? | PASS | It discards problem-frequency ordering and retains only applicability membership. |
| 6 | No named shortage problem promoted into actor history? | PASS | Crosswalk expressly does not assert problem occurrence or actor exposure. |
| 7 | DATEINTR window exact enough? | PASS | DATEINTR is source-native interview date; disputed exact boundary is fail-closed NONCOMPARABLE. |
| 8 | ADP-010 ENCOUNTER narrowest legitimate actor fact? | PASS | ENCOUNTER is admitted contact occurrence; EXPOSURE is stronger and unnecessary. |
| 9 | Independent actor subject ref required? | PASS | L1A requires separately owned public-clinic-or-hospital subject semantics. |
| 10 | Silence forbidden as ABSENT? | PASS | Absence requires separately authoritative full-window nonoccurrence; missing actor record is not negative evidence. |
| 11 | No portability/pooling/source mixing? | PASS | RAW, weights N/A, pooling NONE, portability NONE, one R5 source/release. |
| 12 | Only new conditioner-use authority, no unrelated widening? | **FAIL** | Candidate `COORDINATE_SEMANTICS` authority additionally governs `EmpiricalPredicate@1.0.0`, crossing into separately owned predicate-grammar jurisdiction. |
| 13 | Candidate hashes recompute? | PASS | All six claimed hashes independently recomputed exactly. |
| 14 | New immutable C11 release required? | PASS | L1A explicitly preserves `R5_GT12_Q86A_Q86B_FROZEN` and requires a new bounded release. |
| 15 | Hidden applicability-vs-ENCOUNTER mismatch fatal to route? | PASS WITH GUARDS | Positive comparison is lawful only for an already-admitted ADP-010 contact event with exact independent subject/time authority; negative comparison remains asymmetric/fail-closed. |

One failed mandatory audit question is sufficient to deny the required PASS terminal.

---

# What remains valid after this audit

This audit does **not** invalidate:

`Q69B -> PUBLIC_CLINIC_EXPERIENCE_STATUS`

as a bounded source-specific empirical coordinate candidate.

It does **not** invalidate:

`ADP-010 ENCOUNTER`

as the narrowest positive actor-side family.

It does **not** require fallback to L1B age at this stage.

It does block adoption of the exact L1A authority hash as written.

A corrected endpoint authority can return for a bounded re-audit without reopening the Q69B source-semantic question unless new materialization evidence contradicts the codebook.

M1B remains independently responsible for source-byte materialization and source-row verification. This audit makes no claim about observed Q69B row distributions or undocumented physical source values.

---

# Final disposition

`FAIL__GT34_M1A_Q69B_ENDPOINT_HOSTILE_AUDIT__EXACT_DEFECT`

Exact defect:

`COORDINATE_SEMANTICS_AUTHORITY_OVERGRANTS_EMPIRICALPREDICATE_OUTSIDE_COORDINATE_JURISDICTION`

Smallest repair:

remove `EmpiricalPredicate@1.0.0` from the governed object-family set of the Q69B `COORDINATE_SEMANTICS` candidate; retain the existing D08 predicate grammar as its own authority; recompute the coordinate-authority hash.

Mechanical repaired candidate hash if and only if that single family-list change is made:

`cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c`

No authority adopted.
No implementation.
No source-row execution.
No PSEPF.
No actor mutation.
