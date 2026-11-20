# R4 — CONSTITUTIVE ORGANISM: RELATIONAL METABOLISM IN ACTUAL CODE

**November 20, 2026 · sourcefree provisional R4, stacked on SOROK REMONTATHON #1171 R5 at immutable \`52fcbe5f36952fe671e9c941c85896e5f6149078\`.** Separate isolated branch; does not alter #1167/#1171 author branches, native P2–P6/CAN/ADP, protected SOROK PROGRAMMA or CURRENT_PROGRESS.

## Why this is construction, not another ontology

The SORACLE/UM-SOROK/Astra Constitutive Organism R3 recast ([#1161](https://github.com/maidiu/rawlsing/pull/1161)) changes the causal center: the historical relation of activity, embodiment, independent Others, material institutions and other psychic forms *constitutes what a form means and how it may operate*.

The old R3 program implemented actor-owned forms, scoped RECRUITS/SUPPORTS/INHIBITS, actor-authored action under a separate objective world, action-level APPROACH/WITHHOLD conflicts, qualified LLM developmental proposals, and actual atomic history. It did not yet make relation-of-relation configurations causal in action generation, retain an inhibited form's *indirect* current, or permit event-qualified historical revaluation of a relation. This R4 **writes those functions and wires them into that functioning organism**, without appointing an independent psychic owner.

## Connected implementation

### 1. Actor-owned relational motifs

The new \`um_sorok_organism/relational_metabolism.py\` implements a bounded read-only present operation over existing actor forms, directed relations and acquired \`relational_motifs\`. Each motif has 2–4 prior acquired **same-actor forms**, bounded context terms and locations, and qualified consequences:

- \`RELATION_MEDIATION\` reports a source/target functional relation (e.g. care *SUBORDINATES* under acquired authority). It is **not** the actor's explicitly held belief, the world's truth, or a deterministic clinical diagnosis.
- \`ACTION_CURRENT\` adds an acquired, context-conditioned \`APPROACH\` or \`WITHHOLD\` current **only** to already bodily and materially available options. It does not create a new physical action or commandeer an Other's consent.
- A motif can operate when one of its historical sources is presently **inhibited** and another is active; the inhibited form is **not** thereby restored to direct action. Its *existing relation* is consequential.
- Existing form links can now recognize \`ACTIVATES\`/\`REINFORCES\` in recruitment and \`SUPPRESSES\` in inhibition alongside the R3 positive and negative relations. Inherited contexts and form scopes still apply.
- Every operative relation/motif is included in a bounded situated readset with form refs, relation ref, possible inhibited ancestry, current grading and no assertion of actor self-knowledge.

**No universal polarity physics**: the only action polarities are the already inherited R3 \`APPROACH\`/\`WITHHOLD\` in sourcefree practical consideration. Other affective and relational semantics are typed, structural and provisional. These affect action feasibility without a global motivational arithmetic vote.

### 2. Historical modification of the relation itself

\`development.admit\` now accepts three additional *atomic and actor-local* kinds:

- \`ACQUIRE_RELATIONAL_MOTIF\`: after an accessible actor-specific encounter, a model may propose a 2–4 source-form local configuration, validated against **existing actor-owned acquired history**, with event/experience parentage, bounded effects and grading.
- \`REVALUE_RELATION\`: modifies the *current meaning/function of an existing relation*, retaining the prior relation, context, event and origin in \`relational_history\`. Its stable relation ID survives revaluation. Earlier admiration need not be retrospectively falsified when current trust changes.
- \`REORGANIZE_RELATIONAL_MOTIF\`: revises current activation contexts, effects or active/dormant status of an acquired configuration; the previous complete settings remain as a \`motif_history\` entry.

All use the inherited **copy-on-write staged \`admit\`**. If a late candidate is invalid, earlier candidate modifications are rolled back together. No one changes another actor's world facts or objective history.

### 3. Unified parent and Nadia paths

\`types.Constitution\`, \`types.newborn\`, \`constitution.materialize\`, \`semantics.HeuristicSemanticProvider\` and \`parents.construct_parent\` now carry optional \`relational_motifs\`.

A fictional adult can start from an **explicit fictional backfill** of previously acquired forms and the relations among them. The example authority/care motif is *not* automatically inferred from the parent's religion, class, questionnaire answer or demographic group. Without supplied construction, the motif is absent. Parent-abduction outputs are overwritten with explicit fictional-source grades and \`not_respondent_unconscious_truth=True\`.

Nadia starts with **no adult motifs**, no default id/ego/superego, no predetermined religious obedience or compulsory personality type. Event-qualified developmental proposals may build relational organizations across her actual life. The one engine works for both.

### 4. Event first; semantic flesh follows

\`constitution.compose\` now includes the relational projection when it calculates available actions. \`psychodynamics.enact_currents\` receives new motif action currents alongside existing acquired currents, keeps antagonisms unresolved and never infers motive satisfaction from technical success.

\`runtime.step\` saves an actor-private **pre-world-outcome psychodynamic snapshot**, then the world resolves action and other agents independently; it separately stores an actor-private **post-world/pre-development snapshot**. Development admission follows; the outward LLM \`expression\` packet remains limited to actual public sign and the focal actor's accessible lived receipt. The renderer never receives the private snapshots as self-knowledge or authorization to rewrite world history.

This constitutes a real causal route from historical relational motif → action eligibility/current → actual world attempt → actor-specific experience → possible relational reconstitution → different future recruitment. It is a real *programmatic step*, not a proof of a full person.

### 5. Sourcefree typed psychological power, not metaphysical energy

Inhibition of an active candidate does not automatically destroy it. An inhibited form can continue to condition a present motific process via **qualified relation history**. The program does not create an arbitrary compensating current merely because a form is blocked, does not conserve a mythical scalar of psychic energy, and does not require every encounter to change an actor.

Competing motifs can recruit differing currents on the same operation. Where \`APPROACH\` and \`WITHHOLD\` coexist, R3's \`UNRESOLVED_CONTRADICTION\` is preserved; the engine does not silently make every mixed condition into deferral or a single stronger pole.

**Materialist and epistemic safeguards**: the pastor's authority, the victim's injury, scarcity and institutional force remain world-owned facts; a believer's righteous identification is an actor-owned learned relational interpretation, **not** proof of the pastor's righteousness. Actual coercion can occur; supposed voluntary cooperation still requires independently authored co-activity.

## Tests authored versus evidence actually executed

New sourcefree tests: \`tests/test_relational_metabolism_r4.py\` (11 pytest tests). They cover context-bounded moralized care/authority, suppressed care as still indirectly operative, unresolved opposing currents, nonmagical ritual cue, read-only projection, acquisition in an actor-owned staged transaction, relation revaluation preserving previous meaning, motif reorganization, total rollback on a late invalid model proposal, explicit-source fictional parent formation rather than survey psyche inference, and actual runtime ledger pre/post-private receipts.

**Tests have been authored and committed, but NOT actually executed on a checked-out full repository at the exact R4 HEAD.** The available tool session can inspect and write GitHub but cannot run that remote branch as a Python checkout. GitHub content readbacks confirm exact stored text, not importability, syntactic compilation, or runtime correctness. No green status is asserted. The prior #1171 report of 111 passing normal/optimized tests belongs **only** to the earlier R5 HEAD, not this R4 candidate.

Local full research execution in a clean exact-HEAD checkout:

\`\`\`sh
cd SEAM/ORACLE/UM_SOROK_ORGANISM_R3
python -m pip install -e .
python -m pytest -q -o addopts='' tests/test_relational_metabolism_r4.py
python -m unittest discover -s tests -v
python -m um_sorok_organism demo --db /tmp/um_sorok_r4.sqlite3
\`\`\`

For optimized interpreter and regression tests on exact R4 head, run the existing R5 REMONTATHON suites and R3 suite as their original source/test ownership allows. A test run at an earlier R3/R5 HEAD does **not** carry forward automatically. No original respondent wave, native psychology science or actor authority is issued.

## Critique, open construction and handoff

- Current R4 motifs are **simple bounded conjunctions** of two to four prior forms, not a full dynamic graph of nested relational transformations, social institution and bodily affect. Extend functionally via PRE-A0 §14 and competent PFF/CAN/ADP owners; don't install another psychology database.
- Current context salience is tag/encounter grounded. More complex graded perception and misrecognition need actor-specific encounter semantics, without making the person an iceberg manager.
- \`RELATION_MEDIATION\` is presently an operative private current and actor-LMM-relevant historical meaning; practical action changes occur through explicit acquired \`ACTION_CURRENT\` outcomes. A more general relational means/ends and affect transformation remains future R4+ work, not already accomplished.
- R3's candidate action heuristic may still choose WAIT on first unresolved conflict. That is an explicit heuristic placeholder, **not** a universal psychology of repression or conflict bearing.
- \`REVALUE_RELATION\` and motif acquisition are fictional abductions after actual received encounters, not scientifically identified inevitabilities; no fixed growth, diagnosis, trauma or compulsory “integration” follows.
- Rich biological, non-declarative, class/family relation coupling; rare analogies and slow C5 motifs; general field/institution legitimacy; LLM developmental semantic context; PYAT full empirical world entry; sustainable memory and ordinary-life compression; and product-facing independent person remain incomplete.
- This implementation is **not** a live P3/CAN/ADP owner replacement. It reuses research R3 read/store conventions and inherits the #1171 REMONT concrete-world fixes. Native protected receiving would require its actual competent owner and independent review.
- The existing older R3 \`SOURCE_SHA256.json\` is a historical R3 manifest and must not be cited as a verification of these R4 changed files. GitHub readback SHA is the present file custody; independent SHA-256 manifest and executed proof remain outstanding.
- Do not silently carry this as a resolved SOROK PROGRAMMA obligation. It is a new **sourcefree research candidate** to be reconciled with the paired current-progress documents by an authorized receiving agent; this isolated writer has not altered protected state.

**Next constructor:** Advance the *full* actor/world/person loop with the richer psychodynamic relational operations, including real independent institutions, actor-specific perception, nonconscious mediation, acquired defenses, changed motifs and future recruitment—without relapsing into tiny stand-alone tests as the main deliverable. Preserve the REMONT physical/material fixes and don't declare the organism scientifically calibrated.
