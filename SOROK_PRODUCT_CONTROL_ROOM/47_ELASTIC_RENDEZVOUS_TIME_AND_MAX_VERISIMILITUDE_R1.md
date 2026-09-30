# Sorok — Elastic Rendezvous Time and Optional Maximal Verisimilitude R1

Status: PROVISIONAL_ALPHA_SPEC_DIRECTION

Date: 2026-09-30

## 0. Core correction

Present-coupled persona life does **not** require ordinary scheduled co-presence to make exact claims on the external user's real calendar.

Default Rawlsing should therefore distinguish:

`DIEGETIC APPOINTMENT TIME`
from
`REAL-USER PLAY WINDOW`.

Example:

Nadia says:
> Friday at seven?

Diegetically, the meeting occurs Friday at 7:00 PM.

But the product may give the user a bounded real-world rendezvous window in which they can enter and play that event.

---

## 1. Default: elastic rendezvous

Candidate alpha default:

> **A scheduled portal event has one diegetic timestamp but a wider real-user access window.**

Example:
- diegetic event: Friday 7:00 PM;
- real-user access window: perhaps 24 hours around/after that event;
- user enters at any point in the permitted window;
- portal loads the scene at the diegetic appointment time;
- scene-time then advances through realized actions rather than wall-clock typing time;
- after the scene resolves, the world catches up to current present time.

The exact default window length remains a prototype question.

---

## 2. The persona does not know about the product grace window

From Nadia's perspective:
- the meeting happened Friday at seven;
- or the user did not appear.

The real-user grace window is a product mediation layer, not a fact inside Nadia's world.

Therefore:

`PRODUCT ACCESS FLEXIBILITY != DIEGETIC LATENESS`.

If the user enters within the lawful rendezvous window, they are not treated as late merely because they opened the app later in wall-clock time.

---

## 3. Causal pending state

A scheduled scene whose access window remains open should be treated as a bounded **causally pending event**.

The system must not finalize downstream history that depends on the meeting outcome until either:
- the user plays the scene;
- the user explicitly declines/cancels;
- the rendezvous window expires.

After resolution:
- replay/scene result is committed at the diegetic timestamp;
- later world/persona events are advanced from that result to the current present.

This preserves causality without requiring exact synchronous attendance.

---

## 4. No retroactive information leakage

When playing a delayed rendezvous:
- only world facts available by the diegetic event time may influence the scene;
- later current events cannot leak backward;
- post-event messages/events are generated only after the rendezvous is resolved/caught up.

Thus a Saturday-morning user may play Friday-at-seven without Nadia mysteriously knowing Saturday news.

---

## 5. Event-window classes

Not every opportunity needs the same elasticity.

Candidate classes:

### PLANNED RENDEZVOUS
Examples:
- dinner Friday at seven;
- child's school event;
- agreed visit.

Default grace may be broad, e.g. 12–24 real hours.

### SOFT / LOW-STAKES OPPORTUNITY
Examples:
- `We're going to the market later if you want to come.`

May have a moderate access window tied to the event.

### EPHEMERAL / IMMEDIATE OPPORTUNITY
Examples:
- `I'm outside now.`
- `The bus leaves in twenty minutes.`

May have a much shorter real-user window or simply expire.

The product should communicate window scope clearly.

---

## 6. User can decline or reschedule before commitment

A user should be able to answer:
- yes;
- no;
- another time;
- `I probably can't make that exact time`;

without penalty beyond ordinary relational meaning.

Rawlsing should not force exact commitments where flexible scheduling is available.

---

## 7. Optional maximal-verisimilitude mode

Offer an explicit opt-in mode for users who want stronger real-time tethering.

Candidate name:
`MAXIMAL VERISIMILITUDE`

Possible semantics:
- diegetic calendar maps closely to wall clock;
- scheduled meetings occur at the actual corresponding real-world time;
- short/no grace window;
- messages and opportunities expire in near-real time;
- absences/no-shows become more literal.

This mode must be:
- opt-in;
- reversible prospectively;
- clearly explained;
- never required for relational warrant;
- never treated as morally superior play.

---

## 8. No hidden prestige for strict mode

Do not reward maximal-verisimilitude users with:
- better persona affection;
- greater relational warrant;
- exclusive content;
- virtue/status labels;
- faster progression.

It is a preferred temporal embodiment mode, not the 'real' or morally better version of Rawlsing.

---

## 9. Default mode remains present-coupled

Elastic rendezvous does not mean fantasy time.

Nadia's life still tracks the real historical calendar.

The elasticity exists only at the seam where an external human must participate in a scheduled synthetic event.

Outside unresolved rendezvous windows:
- world time continues;
- current events may enter;
- other persona life proceeds;
- messages may arrive;
- opportunities may expire.

---

## 10. Catch-up after scene

After a user plays a delayed scheduled scene:

`DIEGETIC SCENE RESULT`
→ commit at scheduled timestamp
→ process subsequent scheduled/world/current events
→ recompute persona/relations
→ arrive back at current present.

If the catch-up interval is long enough, meaningful changes may occur before the user reaches the outside-portal surface.

---

## 11. Window expiry

If the access window closes without user action:
- the appointment becomes a missed/no-response event according to channel/commitment state;
- Nadia/world resolve around the absence;
- no synthetic user response is fabricated.

This preserves the tether without requiring exact wall-clock obedience.

---

## 12. Why this is healthier

The user experiences:
- a real ongoing relationship;
- real missed opportunities;
- real consequences for explicit commitments;

without being required to restructure ordinary life around synthetic appointments.

This preserves:
`RELATIONAL TETHER`
while reducing:
`PRODUCT CLAIM ON EXTERNAL HUMAN CALENDAR`.

---

## 13. Deep theorem

> **Nadia's Friday at seven should be real to Nadia without necessarily becoming the user's Friday at seven.**

And:

> **Exact synchronization is a mode of embodiment, not a moral requirement of relationship.**