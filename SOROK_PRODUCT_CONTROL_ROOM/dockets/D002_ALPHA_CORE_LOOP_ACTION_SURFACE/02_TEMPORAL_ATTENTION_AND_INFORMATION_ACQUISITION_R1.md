# D002 — Temporal Attention and Information Acquisition R1

Status: `PROVISIONAL_PRODUCT_LAW_INPUT__NOT_YET_DOCKET_DECISION`

## 1. Core theorem

**ATTEND is an embodied action inside continuous simulated time.**

The interface may be turn-based in the sense that control returns to the user at discrete boundaries.

The world itself must not be turn-based.

Every act of speaking, moving, inspecting, reading, searching, waiting, helping or performing another action consumes variable simulated time while the rest of the scene continues.

## 2. Variable duration

Different actions must consume different amounts of time.

Examples:
- “What is broadly on the fridge?” may be a glance.
- “What is written on that electricity bill?” requires orientation and reading.
- “Give me more detail about the fridge objects” requires additional observation.
- “Read every paper, inspect every magnet front and back and check handwriting/dates” may consume materially significant time.

Duration is not a fixed price attached to a UI command.

Candidate determinants include:
- action class;
- requested observational depth;
- physical distance;
- orientation / line of sight;
- lighting;
- clutter / obstruction;
- divided attention;
- user-character capability where modeled;
- familiarity;
- environmental friction;
- interruption;
- whether the object must be handled/moved.

## 3. Prospective temporal opacity

The system should ordinarily **not announce exact duration before the action**.

No default:
`READ BILL — COST 18.4 SECONDS`

The user should make ordinary human estimates and sometimes be wrong.

This preserves contingency and makes time a condition of judgment rather than a transparent resource meter.

Assisted modes may expose bounded temporal scaffolding, but the underlying world duration remains the same.

## 4. Retrospective temporal knowledge

The engine may know exact or sufficient causal timing.

The user should receive only temporally accessible information.

Examples:
- an explicitly visible clock may reveal exact time;
- the user may check a watch/phone if available;
- another actor may mention the time;
- narration may communicate rough passage through events;
- otherwise the user may have only an ordinary approximate sense.

Thus:

`SIMULATION KNOWS CAUSAL TIME`
does not imply
`USER KNOWS EXACT TIME`.

## 5. Attention resolution

Information yield should depend on how attention is allocated.

Candidate ATTEND dimensions:

### Target
What is the user trying to perceive?

### Depth
Glance / inspect / study / search / read closely.

### Presentation
Openly / incidentally / covertly / while performing another action.

### Allocation
Single-focus versus divided attention.

### Persistence
How long does the user stay with the target?

These dimensions need not be exposed as buttons; natural language can specify them.

## 6. Divided attention

Trying to acquire information while maintaining another presentation should reduce perceptual resolution where appropriate.

Example:

The user looks Nadia in the face and asks about a Rome magnet while attempting to read an electricity bill in peripheral vision.

Possible result:
- utility company name;
- a red `PAST DUE` marker;
- incomplete amount;
- no exact due date.

Want more information?

Look longer or reposition.

That increases temporal and social exposure.

## 7. The world continues

Observation does not pause:
- food keeps cooking;
- buses leave;
- phones ring;
- children finish or abandon homework;
- other actors move;
- scheduled commitments approach;
- someone may notice the user's absence;
- interruptions occur.

This prevents “pause the emergency and read every diary” ludonarrative exemption.

## 8. No exhaustive-observation guarantee

Rawlsing should never promise that a live situation can be fully inspected before action.

There is no “100% clues found” state.

The person and world always exceed the user's available attention.

Finite observation is not a failure state; it is the intended epistemic condition.

## 9. Attention as relational behavior

What the user chooses to inspect is itself behavior.

Across relationships Rawlsing may eventually distinguish:
- capacity for attention;
- allocation of attention;
- self-referential attention;
- practical attention;
- status attention;
- ideological/symbolic attention;
- boundary-respecting versus invasive curiosity;
- attention to children / third parties;
- willingness to act without complete information.

This belongs to the future player-praxis model only if validly inferable.

## 10. Inferential gameplay

Time pressure converts information gathering into judgment.

The player must repeatedly decide:

> What do I need to know before I act?

and

> What am I willing to leave unknown?

The intended loop is not:

`collect all information → compute correct response`

but:

`perceive incompletely → infer → act → observe → revise`.

This is central to both the game mechanic and the project's spiritual purpose.

## 11. Assisted epistemic modes

Candidate mode distinction:

### RAWlsing
Minimal scaffolding.
- no action-time preview;
- no psychological interpretation;
- no relationship meter;
- no consequence flagging;
- no “important clue” highlighting;
- no guaranteed reminder beyond what the user has lawfully externalized;
- user relies on memory, available tools, inference and contingency.

### Rawlsing
Same world/person simulation with humane agency scaffolding.
Potentially:
- visible approximate action classes such as glance / inspect / study;
- surfaced clock only where reasonably accessible;
- notebook;
- reminders for commitments the user explicitly made or recorded;
- resurfacing of facts the user already learned;
- coarse warning that an action is nontrivial where an ordinary person could foresee it.

Assistance must never disclose hidden psychology or future relational consequence.

The mode distinction is an open UX hypothesis, not settled branding.

## 12. Design principle

**Information has a situated acquisition price.**

That price may include:
- time;
- missed alternatives;
- social visibility;
- privacy transgression;
- interruption;
- physical risk;
- opportunity cost.

The player should ordinarily experience that price through the unfolding world, not a game-economy overlay.


## 13. Duration plausibility / no punitive time tax

Variable time must remain **commensurate with the actual act**.

The system must not inflate duration merely to make observation costly.

Examples:
- a glance at a refrigerator may take seconds;
- reading one visible heading may take seconds;
- reading a full bill may take longer;
- inspecting many objects carefully may accumulate meaningful time;
- searching drawers or moving through rooms may take substantially longer.

The scarcity mechanism is realistic accumulation and opportunity cost, not arbitrary punishment.

A user request for “more detail” should consume only the plausible additional attention required to acquire that detail.

## 14. Cumulative micro-time matters

Small observational acts can each be cheap while their aggregate becomes consequential.

Five glances do not each need to be expensive.

But:
- glance;
- re-read;
- move closer;
- inspect amount;
- examine menu;
- inspect magnets;
- turn one over;

can cumulatively consume enough time for the surrounding scene to change.

This preserves both realism and tension.

## 15. Query-invariant temporal semantics

Paraphrasing the same attentional act should not materially change its duration merely because one prompt is verbose.

Duration should follow the realized perceptual/action operation, not token count or rhetorical wording.

Similarly, a user should not gain extra world-time efficiency by packing many independent observations into one long prompt.

The parser must decompose the requested operations and realize their cumulative duration.
