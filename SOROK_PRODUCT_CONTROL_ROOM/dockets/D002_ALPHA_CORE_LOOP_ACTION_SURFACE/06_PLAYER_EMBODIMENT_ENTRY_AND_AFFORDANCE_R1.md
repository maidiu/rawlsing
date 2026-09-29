# D002 — Player Embodiment, Entry and Affordance R1

Status: `PROVISIONAL_PRODUCT_LAW_INPUT__OPEN_ARCHITECTURE_QUESTIONS`

## 1. Missing object exposed by R3

The user is not an omniscient cursor floating over another person's life.

If the user can:
- enter a bathroom;
- sit beside a child;
- look at a refrigerator;
- wash dishes;
- offer a ride;
- handle an object;

then the simulation requires some representation of the user's **diegetic presence**.

“No avatar” does not mean “no embodied user-state.”

## 2. Player presence must have world position

At minimum, a live physical scene may need to know:
- current location;
- orientation / line of sight;
- reach;
- what the user is holding;
- what the user can hear;
- whether a barrier/door separates them from another space;
- current engagement with objects/tasks;
- movement required to acquire new perceptual access.

The user cannot ATTEND through walls, locked doors or arbitrary distance merely by asking the narrator.

## 3. ATTEND does not silently perform DO

If the user asks:

> What does the bill say?

while too far away to read it, lawful outcomes include:
- partial text;
- illegibility;
- “you can't make that out from here.”

The system should not silently move the user closer.

If closer access is required, the user may choose:

> I step closer and read it.

That is DO + ATTEND.

Likewise:
- looking inside a closed drawer requires opening it;
- reading the back of a magnet requires handling/turning it;
- inspecting a medicine bottle label may require picking it up or moving closer.

Perceptual requests cannot smuggle in unspoken physical actions.

## 4. Player inventory / capability authority

User prose does not automatically instantiate capabilities or possessions.

Examples:

> I drive Nadia to work.

requires some lawful transport capability.

> I give her $500.

requires some lawful resource/account/inventory representation if money is semantically real.

> I fix the toilet.

is an attempted action whose success may depend on tools, access, knowledge and physical conditions.

The exact player-resource model is open.

Product law:
**DO describes an attempted world action; it does not grant the user whatever means are necessary to make the action possible.**

## 5. Encounter / access must be causally justified

Randomly presenting an unchosen person does not imply randomly teleporting a stranger into their private home.

Every scene needs some lawful **encounter/access relation** explaining:
- why these people are in perceptual/contact range;
- why the user is permitted or able to be present;
- what each person currently understands the relationship to be;
- what spaces/actions are socially or physically available.

Possible future encounter forms might include:
- neighbor;
- coworker;
- friend-of-friend;
- volunteer/helper;
- classmate;
- online contact;
- travel encounter;
- existing acquaintance developed through earlier scenes.

No specific mechanism is yet adopted.

## 6. Random person ≠ random social access

The spiritual/product requirement is that the user did not select the person for desirability.

That does not require implausible access.

Rawlsing should distinguish:
- **person assignment / encounter non-selection**;
- **causal route by which contact occurs**;
- **current relational permission**.

This distinction becomes especially important for:
- homes;
- children;
- workplaces;
- medical settings;
- religious settings;
- private possessions;
- later invitations.

## 7. What is the player socially?

Nadia must perceive some user-facing social reality.

Potentially relevant:
- age;
- apparent gender;
- language/accent;
- clothing/presentation;
- cultural familiarity;
- name;
- relationship role;
- known occupation;
- prior behavior;
- resources/capabilities.

It remains open whether these come from:
- the real user;
- user-authored self-description;
- a minimal generated player-presence shell;
- mixed modes.

This is a major privacy/product decision and must not be solved casually.

## 8. Cross-cultural communication

If Rawlsing's purpose includes encounters across cultures, language cannot remain an invisible assumption.

Open questions include:
- does the user need to know the persona's language?
- is translation diegetic, UI-level or absent?
- do misunderstandings survive translation?
- what happens to dialect, register, honorifics, indirectness and code-switching?
- can assisted modes translate literal meaning while preserving pragmatic opacity?

This is registered as a future product/interaction question, not decided here.

## 9. Access is relationally dynamic

Access can change over time.

A user may eventually be:
- invited into a home;
- trusted with a child;
- given a key;
- asked to leave;
- excluded from a room/event;
- introduced to family;
- allowed to handle something previously private.

This makes access itself one way relational change becomes materially visible without a meter.

## 10. Alpha implication

Before implementing an embodied alpha, Sorok must specify the **player-presence contract** sufficiently to answer:
- where the user is;
- why they are there;
- what they can physically attempt;
- what resources they actually possess;
- what they can immediately perceive;
- what Nadia can perceive about them.

Otherwise DO/ATTEND cannot be causally governed.
