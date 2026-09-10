# M5_CONTEXT_POSITION_PARTICIPATION_COURT_R1

STATUS: `COURT_COMPLETE`

SOURCE BASIS: Dreier, *Psychotherapy in Everyday Life*, especially Ch. 2 pp. 21–46 and Chs. 4–5, 9–11.

## 1. Court question

Can Dreier’s `context`, `position` and `participation` be normalized without creating a generic CONTEXT box or collapsing structured possibility into actor action?

**VERDICT:** `YES__WITH_STRICT_TYPED_SEPARATIONS`.

## 2. Context decomposition

Dreier’s context of social practice is a local, historically and materially arranged configuration. It must not be normalized as any one of the following:

| Term | Dreier-compatible normalized meaning | Not equivalent to |
|---|---|---|
| `LOCATION` | concrete sociomaterial situatedness / place of participation | social position, institution, activity |
| `INSTITUTION` | wider organized practice/rules/trajectory arrangements that may span contexts | one local context |
| `ACTIVITY` | what participants actually or possibly do | location, context, position |
| `POSITION` | structured relation/place carrying differentiated scope, rights, obligations and counterparts | location, identity, action |
| `RELATION` | directed social connection among positions/persons/institutions | context as whole |
| `RULE/ARRANGEMENT` | norm, schedule, entitlement, obligation, division or gate structuring possibilities | actual action/compliance |
| `SOCIAL PRACTICE` | wider ongoing organized activity reproduced/changed by participants | isolated place or event |
| `CONTEXT OF SOCIAL PRACTICE` | local configuration in which locations, positions, relations, arrangements, objects, participants and activities are linked | generic environment/container |

A Rawlsing representation does not need a metaphysically thick `CONTEXT_OBJECT` if existing world/context binding can preserve the required references and links. It does need to avoid semantic loss among the typed components above.

## 3. LOCATION != POSITION court

### Dreier finding

The text repeatedly treats persons as both **located** and **positioned**. Location is concrete situatedness; position is a structured social place in a context and relation. The distinction matters because participants can share a place while having radically unequal scopes, obligations and influence.

Examples include:

- therapist/client/family members co-present in a session but occupying distinct positions;
- parent/child family members sharing a home but holding different authority, dependency and obligation relations;
- persons moving physically into a new place without thereby acquiring every position or entitlement available there;
- the same formal person-position taking on different practical scope in different contexts.

### Binding negative ceiling

```text
LOCATION != POSITION
COPRESENCE != SHARED_POSITION
POSITION != IDENTITY
POSITION != PARTICIPATION
POSITION != STANCE
POSITION != ACTION
```

### Rawlsing consequence

D1 already requires `POSITION_BINDING` and `WORLD/CONTEXT`; M5 recommends that implementation preserve a distinct `LOCATION/PLACE` reference when location has causal relevance (transport, access, co-presence, material arrangement) rather than overloading `POSITION_REF`.

This is a **typing/negative-ceiling refinement**, not D4.

## 4. Position court

### What position changes

Dreier directly supports D1 derivation of position-specific:

```text
SCOPE_OF_POSSIBLE_PARTICIPATION
ACCESS / EXCLUSION
RIGHT / ENTITLEMENT
OBLIGATION
AUTHORITY / CONTROL APPLICABILITY
DEPENDENCY
COUNTERPART_RELATIONS
INFLUENCE_CHANNELS
LINKS_TO_OTHER_CONTEXTS
INFORMATION/PERSPECTIVAL ACCESS
SANCTION EXPOSURE
```

These are not psychological properties. They are actor-relative social-ecology facts produced by the structured arrangement and the actor’s exact position.

### Power decomposition

Dreier’s generic power language should be normalized only through concrete mechanisms:

```text
unequal scope
+ authority/control
+ access/exclusion
+ dependency/resource asymmetry
+ rights/obligations
+ sanctions
+ capacity to affect arrangements/counterparts
+ cross-context reach
```

No generic scalar `POWER` is needed.

### D1 verdict

`D1__STRONGLY_SUPPORTED`.

The frozen D1 grammar can express Dreier’s position-specific scopes and obligations **provided** position binding is exact and the output remains typed. A nominal category such as `parent`, `child`, `client`, `worker`, `student` is insufficient unless the actual relation/rule/context gives it a concrete consequence.

## 5. Participation court

Dreier requires the following ladder to remain non-collapsed:

```text
MEMBERSHIP / FORMAL AFFILIATION
        !=
PRESENCE / LOCATION
        !=
CONTEXTUAL POSSIBILITY
        !=
PERSONALLY USABLE POSSIBILITY
        !=
ACTUAL PARTICIPATION
        !=
MODE / DEGREE OF PARTICIPATION
        !=
RECURRENT PARTICIPATION
        !=
CHANGED PARTICIPATION
        !=
DURABLE PERSONAL CHANGE
```

### Membership

Membership or institutional inclusion establishes only a possible or regulated relation to a practice. It does not prove presence or action.

### Presence

Physical/social presence can expose the actor to counterparts and local arrangements but does not establish participation in a particular activity or stance toward it.

### Possible participation

The context and position can make an activity available, required, risky or blocked. This is D1 ecology qualification.

### Actual participation

Requires realization: the activity/contact/action actually occurs. Where discrete, existing OEE/event mechanisms may suffice; where recurrent, D2 must preserve recurrence identity/duration rather than minting unrelated events.

### Stance toward participation

Actor-side evaluation/reason/orientation. This belongs to V3.

### Recurrent participation

A temporally patterned series or interval with a stable practice identity. This is a D2 concern plus realized practice history.

### Change through participation

No shortcut. Repeated participation can change abilities/understanding/practice, but durable personal change is downstream V3 and must be earned.

## 6. Same context, different persons

Dreier’s therapy case is especially useful because it holds place/session relatively constant while participants differ in position and wider life connection.

Thus:

```text
SAME SESSION
+ DIFFERENT POSITION
+ DIFFERENT PRIOR/WIDER CONTEXT LINKS
-> DIFFERENT SCOPE / STAKES / PERSPECTIVE / OBLIGATION
-> POSSIBLY DIFFERENT ACTUAL PARTICIPATION
```

This defeats any Rawlsing shortcut that treats context resolution as sufficient to establish a common actor state.

## 7. Same person, different contexts

Equally important:

```text
SAME PERSON
+ CONTEXT A / POSITION A
-> PARTICIPATION MODE A

SAME PERSON
+ CONTEXT B / POSITION B
-> PARTICIPATION MODE B
```

Dreier therefore rejects a person model in which one decontextualized trait/action rule fully determines behavior across social practices. Cross-context consistency, when present, may itself be an achievement of conduct and stable arrangements.

## 8. Position, perspective and stance

The court separates:

```text
POSITION
-> DIFFERENTIAL OBJECTIVE SCOPE / ACCESS / RELATIONS
-> DIFFERENTIAL SITUATED PERSPECTIVE POSSIBILITY

but

POSITION != SUBJECTIVE STANCE
```

A person’s stance is formed across a broader conducted life and may incorporate comparisons, conflicts and concerns from other contexts. Two persons in similar positions can therefore take different stances; one person can enact a broadly similar stance through different context-specific actions.

**Rawlsing owner:** D1 may publish the objective ecology; V3 owns stance/reason/interpretation/action selection.

## 9. Social possibility vs personal ability

Dreier also requires:

```text
CONTEXTUAL POSSIBILITY
+ POSITIONAL ACCESS
!=
ABILITY_TO_REALIZE POSSIBILITY
```

Abilities are developed through prior participation and matter for whether a possible activity can actually be used. But a person’s ability should not be silently imported into PRE-V3 social ecology.

Rawlsing therefore needs a lawful meeting point:

```text
D1 actor-relative social possibility
× existing V3 person capability/history
-> action/participation decision or realization path
```

The seam must not create the capability itself.

## 10. Context-changing participation

Persons are not passive occupants. Dreier treats participation as one way social practices are reproduced and changed. However:

```text
PERSON WANTS CHANGE
!=
PERSON ACTS
!=
OTHERS/INSTITUTION RESPOND
!=
ARRANGEMENT CHANGES
```

This is exactly the provenance firewall required by D3.

## 11. Court rulings

```text
R1  generic CONTEXT black box                       REJECT
R2  LOCATION == POSITION                            REJECT
R3  POSITION -> typed scope/obligation ecology      ADMIT under D1
R4  POSITION -> stance/action                       REJECT shortcut
R5  MEMBERSHIP -> participation                     REJECT shortcut
R6  POSSIBILITY -> realization                      REJECT shortcut
R7  recurrent participation as unrelated events    REJECT semantic loss
R8  actor participation can reproduce/change world ADMIT only through D3 external chain
R9  position-specific perspective                   ADMIT as situated access; subjective interpretation remains V3
R10 one person in several active contexts           REQUIRED REPRESENTATIONAL CAPABILITY
```

## 12. Smallest consequence

No fourth seam capability is proven. The smallest requirement is an implementation invariant on D1/D2:

> An actor may hold multiple simultaneous or overlapping `CONTEXT × POSITION × VALID_INTERVAL × PARTICIPATION_STATUS` bindings, with location separately represented when causally relevant, and each binding may yield different typed scopes, obligations, counterpart relations and constraints.

The actor’s practical coordination among those bindings is **not** precomputed by D1. It belongs to V3 conduct/action composition.