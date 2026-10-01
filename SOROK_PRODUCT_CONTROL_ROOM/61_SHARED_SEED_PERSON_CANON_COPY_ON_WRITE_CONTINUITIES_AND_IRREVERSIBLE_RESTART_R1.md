# Sorok — Shared Seed-Person Canon, Copy-on-Write User Continuities, and Irreversible Restart R1

Status: `PROVISIONAL_PRODUCT_ARCHITECTURE_DIRECTION__ALPHA_ECONOMY_AND_CONTINUITY_REFINEMENT`

Date: 2026-10-01

## 0. Core proposal

Early Rawlsing may economically begin from a small set of deeply pre-generated introductory people rather than generating a new full V3 person for every first-time user.

Example:
- 5 richly generated introductory people;
- each has one pre-contact person/world canon;
- each user receives an independent continuity fork when first encountering one of them;
- relationship/person state then diverges irreversibly by user history.

This does not make the persona a reusable chatbot template.

It makes the persona a **shared pre-contact historical root with copy-on-write post-contact lives**.

## 1. Noncollapse

`SEED-PERSON ROOT CANON`
!= `USER CONTINUITY FORK`
!= `USER-PERSON RELATION HISTORY`
!= `USER ATTENTION / PERCEPTUAL TRAJECTORY`
!= `POST-FORK PERSON DEVELOPMENT`.

A Nadia may have one shared pre-user past and many mutually inaccessible post-contact continuities.

## 2. Shared root canon

The root may contain pre-contact facts such as:
- V3 developmental/person structure;
- biography/life history;
- family/network history;
- current pre-contact projects/obligations;
- home/world structure;
- object ownership and material ecology;
- pre-contact memories;
- pre-contact object significance;
- stable routines and constraints;
- pre-contact social network;
- current starting-date state.

Everything here must be independent of any specific future user.

## 3. Fork moment

At first causally meaningful user contact:

`ROOT NADIA @ T0`
→ `NADIA × USER-A CONTINUITY`
→ `NADIA × USER-B CONTINUITY`
→ `NADIA × USER-C CONTINUITY`.

After T0:
- user-specific event history differs;
- Nadia's models of each user differ;
- relation-specific expectations differ;
- current attention/recruitment differs;
- downstream schedules, choices, memories and development may diverge;
- no later branch is entitled to overwrite another.

These are no longer one continuing person in the strict causal sense.

They are counterfactual descendants of one pre-contact person.

## 4. Why this can save compute

Deep V3 person-generation can be amortized across many users.

Shared root costs:
- initial person generation;
- initial life/world generation;
- pre-contact material ecology;
- high-likelihood L0-L4 detail generation;
- pre-contact network generation.

Per-user costs begin primarily at:
- player embedding;
- perception;
- dyadic history;
- user-specific actor modeling;
- event-time response;
- post-contact developmental divergence.

This is especially useful when many first-time users leave after only a few turns.

## 5. Rich precomputation for alpha

Because the introductory set is small, Rawlsing can afford to generate them **much more deeply** than a just-in-time one-off persona.

For each seed person, precompute:
- dense V3 developmental specificity;
- major life domains;
- home topology;
- material/object ecology;
- many visible and inspectable particulars;
- major object provenance anchors;
- family/network anchors;
- recurring routines;
- tensions/projects/obligations;
- a large bank of pre-contact memories and causal dependencies.

The LLM should be intensely constrained by the person's existing V3 specificity, material history and world state at every step.

It should not generate decorative detail independently of person/history.

## 6. Root-world generation principle

Every material particular should be treated as a plausible consequence of the already-generated life.

For example, the old Birkenstocks should arise from some combination of:
- finances;
- replacement habits;
- consumption style;
- bodily use;
- travel history;
- gifts;
- attachment to continuity;
- practical wear;
- current alternatives.

Not:
> "Nadia is bohemian, therefore Birkenstocks."

The material world is sedimented person/world history, not aesthetic theming.

## 7. Shared lazy back-data

Some pre-contact back-data can remain unresolved until approached.

But one user's curiosity must not author a shared past for all branches.

Therefore shared pre-fork lazy completion must satisfy:

> **The user may choose the locus of resolution; no user may condition the content of shared pre-contact truth.**

Preferred implementations:
- precompute deeper than normal because seed set is small;
- where still lazy, resolve by root-person state + canonical target + governed seed/randomness;
- exclude user wording/preferences/relationship state from substantive truth generation;
- cache the resolved pre-contact fact for reuse only if it is valid for all forks.

## 8. Deterministic keyed backfill

A strong implementation direction:

`ROOT PERSON SEED`
+ `CANONICAL TARGET KEY`
+ `PRE-CONTACT STATE`
→ `PRE-CONTACT DETAIL`.

Examples:
- `home.living_room.rug.provenance`;
- `object.birkenstocks.acquisition`;
- `library.nabokov.editions`;
- `laundry.current_contents@T0`.

The query may trigger resolution of the target key.

The query text does not enter the substantive generator except to identify the target/operation.

This makes first-user discovery cacheable without granting that user authorship over everyone else's Nadia.

## 9. Cross-branch compatibility law

A pre-contact fact may become globally shared after forks exist only if it is compatible with every already-admitted branch fact that depends on the same pre-contact history.

If compatibility cannot be proven:
- do not mutate the shared root;
- preserve the branch-local admitted fact;
- treat the unresolved root region as requiring adjudication/rebuild rather than silent global backfill.

In practice, deep precomputation + keyed deterministic completion should minimize this case.

## 10. L0-L5 ownership under the shared-root model

### L0 — structural space
Usually shared pre-contact root.

### L1 — visible material ecology
Usually shared pre-contact root.

### L2 — inspectable physical particularity
Prefer shared root or deterministic root completion.

### L3 — objective provenance/history
Shared if wholly pre-contact.

### L4 — Nadia's own pre-contact relation to object/history
Shared if it belongs to her pre-contact V3/memory organization.

### L5 — present relational recruitment
Always branch-specific once the current event involves a particular user.

After T0, even L0-L4 can acquire branch-specific changes:
- user breaks the mug;
- Nadia moves;
- shoes wear further;
- an object is given away;
- user repairs the mandolin.

Then later state is branch-local.

## 11. Phenomenal divergence over a shared root

Two users can encounter identical root Nadia and still see materially different initial surfaces due to:
- attention regime;
- recognition repertoire;
- current task;
- viewpoint;
- time spent;
- explicit ATTEND.

Thus:
`SAME ROOT WORLD`
+ `DIFFERENT USER PERCEPTION`
→ `DIFFERENT EXPERIENCED NADIA`.

Then:
`DIFFERENT INTERACTION HISTORY`
→ `DIFFERENT POST-FORK NADIAS`.

Both differences are lawful, but they arise at different layers.

## 12. Restart is abandonment, not reroll-backtracking

If a user abandons a continuity:
- they do not rewind Nadia;
- they do not return to T0;
- they do not recover the "other Nadia they could have met";
- they do not inspect alternate branches of the same relationship.

They leave the only Nadia-who-met-them that exists in that continuity.

A new start may assign another introductory seed person according to product law.

If product law permits the same root person to be allocated again to another fresh user, that is a different branch, not recovery of the abandoned one.

For the same user, default product law should not allow a restart to re-enter that person's root and try again.

## 13. No starting over inside a relation

This is stronger than no save-scumming.

At any time `T > T0`:

`CURRENT RELATION HISTORY`
cannot return to
`T0`.

If the user:
- made a bad first impression;
- ignored something;
- lied;
- offended Nadia;
- failed to notice something;
- was generous;
- became trusted;
- became distrusted;

that history is now part of the relation.

Repair may occur.
Reinterpretation may occur.
Forgiveness may occur.
Forgetting may occur.

Undo does not.

## 14. Restart-warning consequence

A restart warning can truthfully disclose:

- the user has not seen all of this person;
- their phenomenal surface was shaped partly by their own attention;
- another observer could have known a strikingly different Nadia;
- returning to this continuity will not restore the Nadia they might have met before their existing history;
- abandoning the continuity forfeits any future relation with this branch.

Critically:

> **Going back is not going back to the beginning.**

If the user cancels restart and returns:
- time/history remain;
- impressions remain;
- current Nadia remains;
- the user can only act from now.

## 15. Developmental force

This creates a powerful relational law:

> **You do not get to meet people again for the first time.**

The user may come to understand:
- first impressions were partial;
- attention was selective;
- their conduct changed what became possible;
- the person always exceeded what they knew;
- discovering that incompleteness does not restore lost possibilities.

Rawlsing cannot claim this causes moral growth.

But it can make irreversible relational time experientially real.

## 16. Five-person introductory alpha pool

A small introductory pool has additional alpha advantages:
- consistent benchmark persons across testers;
- easier regression testing;
- stronger pre-generation quality;
- lower first-session compute;
- comparable reports across users;
- direct testing of perceptual divergence;
- direct testing of relationship divergence;
- easier forensic reproduction of bugs.

Care is required to prevent:
- users shopping among the five;
- public tier lists / optimization guides;
- cross-user spoilers turning root facts into walkthrough content.

Assignment should remain unchosen/opaque enough to preserve encounter law.

## 17. Research opportunity

With informed research consent, identical-root forks can support unusually clean study of:
- attentional divergence;
- interpretation divergence;
- relational behavior divergence;
- effect of different user histories on the same starting person.

This is stronger evidence than comparing wholly different generated personas because initial person/world variance is controlled.

But each post-contact branch must remain isolated in live operation.

## 18. Compact laws

> **One past can seed many possible meetings; every actual meeting creates its own irreversible history.**

> **Shared pre-contact personhood may be amortized. Relationship history may not be.**

> **You can repair a relationship. You cannot reload it.**

> **You never meet the person you could have met; you meet the person who has now met you.**
