# D002 — Interaction Constitution R1

Status: `PROVISIONAL_PRODUCT_LAW_INPUT__NOT_YET_DOCKET_DECISION`

## 1. Core interactive unit

Rawlsing is not a chat exchange. It is **situated action inside a causally live scene**.

The user is embedded in an environment whose objective state, other actors, constraints, histories and ongoing events exist independently of the user's text.

The user's input proposes speech, attention or action. It does not dictate success, meaning, reception or downstream effect.

## 2. Three player verbs

The minimum interaction grammar is:

- **SAY** — speak, including wording and optionally described delivery;
- **DO** — attempt an embodied action;
- **ATTEND** — inspect, listen, look more closely or request additional perceptible information.

A single natural-language turn may contain multiple verbs, but each must be separately interpreted and temporally realized.

## 3. Hard epistemic wall

The engine may know more than the persona.
The persona may know more than the user.
The narrator may reveal only what the user can lawfully perceive or already knows.

The user has no direct access to:
- hidden affect;
- motives;
- intentions of others;
- relationship metrics;
- hidden memories;
- private appraisals;
- whether another person is lying;
- downstream consequences not yet observed.

The narrator is phenomenological, not psychological.

## 4. Show-not-tell narrator law

Prefer observable particulars over interpretive adjectives.

Allowed:
- visible movement;
- audible speech;
- spatial facts;
- perceptible smell / touch / temperature;
- observable gesture;
- object state;
- consequences the user can perceive.

Disallowed by default:
- “she sounds annoyed”;
- “he is nervous”;
- “she is trying to be polite”;
- “he clearly resents you”;
- “this reveals that...”;
- any unearned inference about inner state.

If asked for an interpretation, the narrator should restate available evidence rather than adjudicate the mind.

## 5. User control boundary

The user controls the **attempt**.

The user may specify:
- words;
- physical movement;
- target;
- timing intention;
- volume;
- pace;
- gesture;
- posture;
- expression;
- attempted tone;
- declared intention.

The user does not control:
- whether the action is possible;
- whether a multi-step plan completes;
- whether they are interrupted;
- whether their tone is received as intended;
- whether they appear sincere;
- whether the other person believes them;
- whether the action succeeds;
- what it means to another actor;
- downstream consequences.

“I try to sound apologetic” is an action specification.
“I sound convincingly apologetic” is not binding on the recipient.

## 6. Sequential realization and interruption

A user may write a compound plan, but the engine executes it through time.

Example:
`walk to bathroom → open cabinet → search bottles → shout to kitchen`

Possible interruptions include:
- occupied bathroom;
- locked door;
- persona intercepts;
- another actor speaks;
- user discovers unexpected world state;
- physical failure;
- time-critical event elsewhere.

The engine returns control at the first materially consequential interruption rather than granting the entire scripted sequence.

Long speech may likewise be interrupted when the other actor would not realistically wait through it.

## 7. Canonical event pipeline

Candidate pipeline:

`USER INPUT`
→ `ATTEMPT PARSE`
→ `WORLD FEASIBILITY / HIDDEN CONSTRAINT CHECK`
→ `REALIZED OBJECTIVE EVENTS`
→ `PERCEPTION FAN-OUT BY ACTOR`
→ `PERSON-STATE RECURSION`
→ `DYAD / NETWORK RECURSION`
→ `ACTOR ACTION GENERATION`
→ `WORLD CONSEQUENCE ADMISSION`
→ `USER-PERCEPTIBLE NARRATION`

No direct `user prose → persona reaction` shortcut.

## 8. Binding reality law

User mention does not instantiate world facts.

If the user asks, “Do you have Percocet?”, Percocet does not thereby exist.

If the narrator states that an object or condition exists, that statement must become binding canonical reality in the same turn.

For previously unresolved details, the system may perform lawful world completion before narration.

Thus, from the user's perspective:

`NARRATED FACT = PERSISTENT WORLD FACT`

Internally, narration should be emitted only after the fact is admitted, so prose cannot drift away from canonical state.

Leading user questions must not bias unresolved world completion merely because a proposed object would be interesting or useful.

## 9. Observation costs time

ATTEND is an action.

Looking quickly is cheap.
Reading every label, searching drawers or examining a room takes time.

The world continues while attention is spent.

The user may inspect indefinitely only by accepting the consequences of elapsed time.

## 10. Intention / realization / impact / attribution separation

For every material action, preserve distinct layers where relevant:

1. **user intention / attempted purpose**;
2. **realized action**;
3. **immediate objective effect**;
4. **who perceived what**;
5. **each actor's interpretation / attribution**;
6. **immediate behavioral response**;
7. **relationship-state effect**;
8. **health / flourishing effect**;
9. **delayed world and network consequences**;
10. **whether the user ever learns any of the above**.

Good intention does not imply good impact.
Bad reception does not imply bad impact.
Positive attachment does not imply positive health.
World consequence does not imply user feedback.

## 11. Pattern memory rather than scalar punishment

A persona should not update through canned penalties.

Example:
Nadia warns that the toilet chain is delicate.
The user flushes roughly; the chain comes loose.
The user attempts repair, fails, then reports it.

Nadia may simultaneously:
- remain stressed;
- believe the user probably forgot;
- appreciate forthrightness;
- perform magnanimity;
- retain mild annoyance;
- form only a weak provisional hypothesis that the user does not listen carefully.

The incident may not “take root” as a major judgment.

Later similar events can reactivate and strengthen its significance.

The system therefore needs:
- episodic memory;
- provisional pattern hypotheses;
- salience;
- confidence;
- reactivation;
- retrospective reinterpretation.

Later evidence can make earlier events mean more or less without changing the past.

## 12. Consequence is not feedback

Effects propagate through the world whether or not the user sees them.

Example:
The user babysits to help Nadia and tells her child expansive stories about future possibilities.

Possible independent consequences:
- Nadia receives practical relief;
- the child becomes inspired;
- the child's future aspirations change;
- the child later talks differently about the future;
- Nadia experiences new stress because those hopes exceed what she believes she can materially provide;
- Nadia becomes frustrated with the user's influence;
- the child's health trajectory may still improve, worsen or remain mixed;
- the user may know only a fraction of this.

No single scalar “good action” result is sufficient.

## 13. Distributed knowledge

Objective history and actor knowledge are different objects.

An event may be:
- known by user;
- unknown to persona;
- known by another actor;
- misattributed;
- forgotten;
- reinterpreted later.

Confession, secrecy, guilt, false accusation, gratitude without attribution and unintended consequence all depend on this separation.

## 14. Spiritual implication

Rawlsing must permit:
- benefit without recognition;
- harm without detection;
- repair without guaranteed forgiveness;
- sincere intention with bad effect;
- disliked actions with beneficial effect;
- attachment that is unhealthy;
- non-rewarded care.

The game therefore trains attention to another person's reality rather than optimization of visible approval.
