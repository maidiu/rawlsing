# UM-SOROK: Constitutive Computational Organism R1

**Status:** Implemented, runnable, **sourcefree provisional research software**. Not the protected SOROK product, native CAN/ADP developmental science, a validated human developmental model, or an authorized GitHub merge.

**Purpose:** Put the complete **iceberg → historically shaped recruitment → situated psychological composition → actor attempt/tip → independently resolved world consequence → actor-specific experience → psychic reconstitution → future recruitment** circuit into one *continuing* computational life. This is not a single-form experiment and not a replacement for the existing Rawlsing authorities.

## Run it

Requires Python 3.11+ and only Python standard library. No model key, external services, or network are needed for the offline demo.

```bash
cd UM_SOROK_ORGANISM_R1
python -m unittest discover -s tests -v
python -m um_sorok_organism.cli demo --db organism_demo.sqlite3 > result.json
python -m um_sorok_organism.cli inspect --db organism_demo.sqlite3 --actor nadia
python -m um_sorok_organism.cli situated --db organism_demo.sqlite3 --actor nadia
python -m um_sorok_organism.cli see --db organism_demo.sqlite3 --actor nadia
python -m um_sorok_organism.cli chain --db organism_demo.sqlite3
```

The archive includes a sample `demo.sqlite3`, `demo_output.json`, and a test receipt. Run `demo` with a new DB path if you want to preserve the shipped state.

## What now materially exists

- **One stored life:** SQLite `ResearchLedger` atomically commits the objective world, independently indexed actors, their fictional acquired changes, and an append-only world/actor-digest event chain. A genesis receipt records the original world and actors. State reopens in a new process; witness receipts are replay-verifiable as a hash chain.
- **Three differentiated persons:** Fictional, independently initialized mother and father with separate sampled-configuration *fixtures*; Nadia starts with a materially dependent sensory/motor organism and **no inherited adult ideology or psychological list**. Both entrances use the same continuing actor model.
- **Variable iceberg:** Acquired forms, ties among forms, ongoing projects, traces, memory, actor-specific models of Others, self-model, and changes to recruitment scope and project purpose. Content is sparse and historically bound, not a universal personality vector. A situated constitution is derived, not independently persisted.
- **Recruitment and composition:** Multiple streams: exact accessible cues, ongoing projects, admitted form-to-form links, inhibition, dormant forms, nondeclarative traces, simultaneous currents and qualified action possibilities. No single mandatory winning motive. A composition helper can derive multistep activities from present acquired means.
- **Embodied developmental beginnings:** Abstract nutrition, rest, discomfort, sensorimotor capacity and maturation actually change eligible conduct and attention. These are *functional engineering approximations*, **not measured hormones or validated neonatal physiology**.
- **Independent material world:** Places, stocks, food, work, repair, institutional access, other actors' independent attempted conduct, care, unilateral imposition, refusals, public cues, and continuing world-owned relational histories. Objective consequences do not require subjective recognition or consent; **voluntary coactivity does require an Other-originating research policy decision**.
- **Actual provisional developmental effects:** Structured semantic proposals may produce new forms, connections, differentiated operations, new projects, changed project objects/means, altered context applicability, changed strength/lifecycle, traces and fallible other-models. These are recorded with actor/event/experience identity and consumed later. `NO_CHANGE` and rejected proposals are supported. The research owner is intentionally NOT CAN-011.
- **Humanlike time is compressed:** An aggregate ordinary-life interval moves the same clock, changes the body, records known/modeled recurring processes, and can support bounded practical development **without inventing unperformed microevents**.
- **Psychological tip is partial:** The output is an actor-restricted public expression, not an omniscient biography or a full iceberg dump.
- **Model integration interface:** The offline heuristic provider supplies coarse psychology; a separate OpenAI-compatible JSON adapter can supply LLM-generated candidates via explicit credentials. **No live LLM call was executed in this return.** The runtime validates tasks, rights and allowed effects; an LLM cannot issue objective world facts or other actors' actions.
- **P2/P3/P6 adapters:** A concrete *read-only* P3 record adapter and owner-boundary contract clarify the direct future junctions. These do **not** yet use a running protected P2/P3/P6 worktree.

## What the current software demonstrates and does not

| Positive, executed | Honest limitation |
| --- | --- |
| Same persistent actor across scenes and cold reopening | Independent native P2 world/owner was **not actually connected**; ResearchLedger is a separate sourcefree *research simulation*, not a rival proposed canonical store |
| Formation can change recruitment scopes/links/projects; later actor proposals consume them | The formation heuristics do not establish a scientific theory of acquisition or transfer |
| Bodily eligibility, actual material effects, institutions and another actor's separate policy matter | Objective world is small and stylized; actor policy is simple, not a fully expressive individual agent |
| Coactors may refuse; imposed consequences do not imply consent | The Python in-process boundary is not a security sandbox against hostile injected code; no real service identity attestation |
| Sourcefree adult construction is internally differentiated, and child construction is from a sparse body | Pseudo-respondent examples are synthetic fixtures; the offline interview reads answer-keyed forms, **not independent whole-survey correspondence** |
| Aggregate life changes clock and some capabilities | No deep historical causal distribution, multigenerational institutions, real socioeconomic world generator or validated physiology |
| Real-LLM adapter is included | It has not been connected, invoked, evaluated or given production permissions |
| 24 integration tests pass; 9-event example ledger verifies | This is author-side engineering evidence, not independent reviewing, human-validation or protected receiving |

## Architecture

`types.py`: typed outward interfaces, body and world births, stable identifiers.
`storage.py`: world+actor+event transactional research persistence and evidence chain.
`organism.py`: bounded bodily dynamics and developmental eligibility.
`constitution.py`: read-only whole-actor constitution, accessible world projection, situated recruiter.
`semantics.py`: semantic model role boundary with deterministic offline fallback and schema validation.
`model_provider.py`: **optional, untested** HTTP JSON model transport.
`development.py`: provisional, actor/event-grounded iceberg and recruitment-pathway transformations.
`ordinary_life.py`: aggregate time/recurrence without fabricated individual events.
`parents.py`: separate adult inverse-constitution and plainly unverified interview pathway.
`plans.py`: compose novel multi-operation activity from acquired means.
`world.py`: independently resolved world activities, other-policy requests, shared relations, institutions and resources.
`runtime.py`: the one joined causal circuit and cold-reopen API.
`adapters.py`: P3 scoped-record read contract and P2/P3/P6 ownership boundaries.
`cli.py`: runnable sourcefree continuing life and inspection interface.

## Governing architectural decisions

1. **A person is not a solitary giant state class.** Their enduring constitution can be reconstructed from competent owners; the current situational composition is derived. The actor/world/relationship distinction remains real.
2. **Two entrances, one ongoing psychology.** Source-conditioned fictional parents enter through abductive initialization; Nadia begins from an immature organism and forward encounters. Initial questionnaire statements may constrain the fictional adult but cannot predetermine their later life.
3. **Content and recruitment pathways both develop.** A form can remain possessed while dormant or out of scope; acquired links and projects can be revised without rewriting its historical origin.
4. **Shared fields are not fused minds.** Joint activity has an objective history; each actor may acquire a different afterlife. A caregiver's bid, a child's contribution, another's refusal and an institutional imposition are different causal facts.
5. **Scientific grade != fictional computational consequence.** The program can provisionally make a fictional actor acquire a capacity while admitting it has no human-learning law or source calibration.
6. **Hypercompression is a product decision, not a justification for fabricated details.** Aggregate periods are explicitly distinguished from objective episode receipts.
7. **Native authority is separate.** No protected source is changed, no official actor/world events are issued, no new canonical CAN/ADP writer is claimed.

Read `IMPLEMENTATION_MAP.md`, `KNOWN_LIMITATIONS.md`, `SOURCE_GROUNDING.md`, and `HANDOFF.md` for exact next integration work and why this is an R1 rather than a completed whole person.
