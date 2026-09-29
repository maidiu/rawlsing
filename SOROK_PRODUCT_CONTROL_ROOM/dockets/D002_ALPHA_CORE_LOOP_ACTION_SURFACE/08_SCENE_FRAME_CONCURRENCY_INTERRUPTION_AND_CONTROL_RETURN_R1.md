# D002 — Scene Frame, Concurrency, Interruption and Control Return R1

Status: `PROVISIONAL_PRODUCT_LAW_INPUT__OPEN_UX_QUESTIONS`

## 1. Initial scene problem

A hard show-not-tell narrator cannot solve opacity by making the user manually ask for every obvious fact.

When entering a scene, the user needs a **baseline phenomenal frame** sufficient to orient and act.

Candidate initial frame should surface what a normally situated person would immediately register at coarse resolution:
- where they are;
- obvious people present;
- obvious ongoing actions;
- major spatial affordances/barriers;
- conspicuous sounds/conditions;
- immediately salient time pressure where perceptible.

It should not automatically surface:
- hidden importance;
- private meaning;
- detailed documents;
- subtle emotional interpretation;
- every visible object.

## 2. Ambient perception versus focused ATTEND

Distinguish:

### Ambient perception
Low-cost, coarse, ongoing surface information available without a special investigation act.

### Focused ATTEND
Deliberate allocation of attention to acquire more resolution.

Example:
Ambient:
> Nadia is at the stove. A child is working at the table. Papers and magnets cover part of the refrigerator.

Focused ATTEND:
> What's on the refrigerator?

Further focus:
> What does the bill say?

This avoids both extremes:
- omniscient information dump;
- tedious blindness requiring a query for every chair.

## 3. Compound actions may be concurrent

Not every multi-verb input is sequential.

Example:

> While asking Nadia about the Rome magnet, I sneak a quick glance at the bill.

This is overlapping:
- SAY;
- ATTEND;
- presentation/concealment.

The runtime needs to represent:
- temporal overlap;
- divided attention;
- shared duration;
- interference;
- actor observation of the combined performance.

Do not serialize all such actions into:
`finish speech → then glance`
if the user explicitly attempts them simultaneously.

## 4. Concurrency does not mean infinite parallelism

A user cannot perform arbitrarily many full-attention acts at once.

Overlapping operations compete for:
- attention;
- hands;
- gaze;
- posture;
- speech;
- physical position;
- time.

The engine may reduce performance/perceptual resolution or reject incompatible simultaneity.

## 5. ATTEND itself is interruptible

A long observation is not atomic.

While reading a document:
- Nadia may speak;
- the child may interrupt;
- a pot may boil over;
- someone may enter;
- the target object may move;
- the user may choose to stop.

The system may return partial information corresponding to what was acquired before interruption.

## 6. User may abort or redirect

When new information arrives during a multi-step plan, control should return before the system blindly completes later planned steps where the new event would reasonably permit reconsideration.

Example:
User:
> I walk toward the bathroom, open the cabinet and search every bottle.

If Nadia calls after the user as they reach the hallway, the system should not necessarily continue through the entire search before returning control.

The player submitted an intended plan, not irrevocable automation.

## 7. Control-return principle

A turn should end / control should return when one of the following occurs:
- the attempted action completes;
- a materially new observation changes the decision surface;
- another actor meaningfully intervenes;
- feasibility fails;
- an interruption occurs;
- the user requested only a bounded observation and its result is available;
- continuing would require assuming a new user decision.

Exact granularity remains a UX/prototype question.

## 8. No forced drama threshold

“Materially new observation” should not mean “narratively dramatic.”

Ordinary facts can justify control return if they change what action is feasible.

Example:
- bathroom door is locked;
- child is already sitting in the intended chair;
- bill is too far away to read.

The engine should not force through a user's original plan merely because the obstacle is mundane.

## 9. Scene continuity

The returned narration should preserve enough scene state that the user can reason about:
- what moved;
- what is still happening;
- what is unfinished;
- who is present;
- what time pressure continues.

The narrator should not reset the room composition each turn.

## 10. Alpha implication

A prototype must test not just natural-language action interpretation but:
- baseline scene framing;
- ambient vs focused perception;
- simultaneous SAY+ATTEND;
- incompatible simultaneity;
- partial observation under interruption;
- abort/replan;
- control-return cadence.
