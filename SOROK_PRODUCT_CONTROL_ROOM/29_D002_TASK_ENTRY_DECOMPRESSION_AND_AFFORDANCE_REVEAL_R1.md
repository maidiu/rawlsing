# Sorok D002 — Task-Entry Decompression and Concrete Affordance Reveal R1

Status: PROVISIONAL_CORE_INTERACTION_REFINEMENT__SUPERSEDES_NEUTRAL_AUTOEXECUTION_AS_DEFAULT_TASK_ENTRY

Date: 2026-09-29

## 0. Correction

For many ordinary tasks, broad goal language should not immediately authorize full neutral execution.

Instead:

> **A broad task statement may function as entry into a concrete task. Rawlsing reveals the actionable state of that task and returns control before choosing the user's method.**

Example:

User:
> I help with the groceries.

Rawlsing may realize approach/availability and then surface:
- how many bags remain;
- obvious size/weight variation;
- fragile/awkward items if perceptible;
- where Nadia/others are;
- stairs/distance;
- time pressure;
- what the user can physically see/reach.

Then control returns.

---

## 1. Task-entry theorem

`BROAD TASK INTENT`
→ `ENTER TASK`
→ `REVEAL CONCRETE AFFORDANCE STATE`
→ `USER CHOOSES METHOD / LEVEL OF DETAIL`
→ `WORLD RESOLVES ATTEMPT`.

This avoids both:
- tedious pre-task questioning;
- hidden engine assumptions about how the user performed the task.

---

## 2. Groceries worked example

User:
> I help with the groceries.

Possible surface:
> The trunk is still crowded: twelve plastic bags, two cases of water, a carton of eggs in one open bag, and a paper sack with a damp bottom. Nadia has two bags in each hand already. The apartment is up one flight.

Now the user may say:
- `I grab three bags and follow her.`
- `I take the two water cases.`
- `I grab all twelve bags.`
- `I take the eggs and paper sack first.`
- `I ask which ones she wants upstairs first.`
- `I take a normal load and keep making trips until we're done.`

Each gives the engine a different execution contract.

---

## 3. Probability / feasibility resolution

If the user attempts an aggressive or uncertain physical act, Rawlsing should resolve success from current world/body/task state.

Example:
> I grab all twelve bags.

Relevant factors may include:
- bag weights;
- handle strength;
- bulk/shape;
- player's represented body/carry capacity;
- hand availability;
- stairs;
- fatigue;
- surface conditions;
- randomness where lawful.

Possible outcomes:
- succeeds impressively but awkwardly;
- succeeds with visible strain;
- Nadia reacts to apparent competence or recklessness;
- one bag slips;
- handle tears;
- user cannot physically get secure purchase on all of them;
- user makes it a few steps and has to set some down.

Important:

`LLM NARRATIVE CHOICE != FEASIBILITY AUTHORITY`.

The LLM may help estimate/realize bounded probability, but outcome must be constrained by canonical physical state and governed stochastic law rather than dramatic preference.

---

## 4. Persona response is downstream

Nadia does not react to the text command.

She reacts to what she perceives of the realized attempt.

Examples:
- competent efficiency;
- showboating;
- recklessness;
- dropping groceries;
- asking before acting;
- choosing fragile bags first;
- quietly making repeated trips;
- stopping after one trip.

Her interpretation remains actor-local.

---

## 5. User-controlled granularity

After task entry, the user can choose their own granularity.

Detailed:
> I take the eggs and the paper sack first, then come back for the water.

Moderate:
> I take three bags at a time and keep making trips.

Delegated:
> I take a normal load and keep going until everything is inside.

The more the user specifies, the more method belongs to them.

The more they delegate explicitly, the more routine procedure the engine may compress.

Thus:

`DETAIL LEVEL -> EXECUTION AUTHORITY`

but not:

`DETAIL LEVEL -> MORAL QUALITY`.

---

## 6. Dinner worked example

User:
> I make dinner.

Rather than silently choosing the meal, Rawlsing first exposes the task state if no plan already exists:
- available ingredients;
- time;
- known dietary constraints;
- household members present;
- current kitchen state;
- prior plans if any.

Then return control.

User can choose:
- exact meal;
- broad goal (`something quick with the chicken and rice`);
- explicit delegation (`whatever is fastest and feeds everyone`).

Only after that should routine preparation compress.

---

## 7. Laundry worked example

User:
> I fold the laundry.

Rawlsing can surface:
- one basket / several loads;
- adult/child clothing mix if visible;
- delicate/unusual items if obvious;
- whether storage locations are known;
- time pressure.

Then user can choose:
- exact sorting method;
- broad ordinary method;
- explicit delegation (`I just fold it normally and leave stacks on the table`).

This prevents hidden assumptions about meticulousness or sloppiness.

---

## 8. When task-entry reveal is unnecessary

Do not interrupt every trivial act.

Task-entry decompression is most useful when:
- multiple plausible methods exist;
- scope/quantity is nontrivial;
- physical risk/effort varies;
- choices can become socially expressive;
- task-state itself is informative;
- another actor is jointly performing the task;
- resource/time tradeoffs matter.

Simple acts may still resolve directly.

---

## 9. Deep interaction law

> **Broad natural language should often buy the user access to the real situation, not a narrated completion of it.**

Rawlsing's job is to concretize the world enough that the user can make an actual choice.

This is especially powerful because the world can confront the user with details they did not know when they volunteered.

---

## 10. Relationship payoff

Repeated task-entry encounters create ordinary relational knowledge:
- how much Nadia usually carries;
- whether she asks for help;
- where groceries go;
- what the child can carry;
- how rushed evenings are;
- what counts as helpful versus intrusive in this household.

Over time, established routines allow more compression because the user genuinely knows the task/world better.

Compression is therefore learned through history rather than assumed at first contact.

---

## 11. Refined rule

At first encounter with a consequential ordinary task:

`ENTER -> REVEAL -> CHOOSE -> RESOLVE`.

After stable routine/history exists or the user explicitly delegates:

`ENTER -> COMPRESS UNTIL SALIENT FORK`.

This preserves both realism and usability.