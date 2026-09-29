# Sorok Operating Method — Green-Field Product Architecture Without Sprawl

Status: `ACTIVE_METHOD_R1`

## 1. The problem

Sorok is intentionally green-field. Prematurely forcing certainty would be as damaging as unstructured brainstorming.

The method therefore preserves:
- imagination before closure;
- explicit uncertainty;
- traceable decisions;
- bounded investigations;
- prototypes where prose cannot settle behavior;
- architecture ownership;
- reversibility;
- connection to the governed codebase.

## 2. Canonical lifecycle

Every material product idea should move through:

`CAPTURE → FRAME → INVESTIGATE → PROTOTYPE / MODEL → ADJUDICATE → RECORD → CROSSWALK → HANDOFF → VERIFY`

### CAPTURE
Add a question or hypothesis to `registers/QUESTIONS.jsonl`.

### FRAME
State:
- exact question;
- why it matters;
- what would change depending on the answer;
- dependencies;
- what evidence could answer it;
- what is explicitly out of scope.

### INVESTIGATE
Use the lightest method sufficient:
- conceptual analysis;
- existing repo archaeology;
- literature / product research;
- user research;
- paper prototype;
- interactive prototype;
- simulation;
- cost experiment;
- adversarial / abuse test.

### PROTOTYPE / MODEL
Prototype only the uncertainty that prose cannot resolve.

### ADJUDICATE
Choose:
- `ACCEPT_PROVISIONAL`
- `ACCEPT_REQUIREMENT`
- `REJECT`
- `DEFER`
- `NEEDS_MORE_EVIDENCE`

### RECORD
Write one decision record. Do not bury decisions in a docket narrative.

### CROSSWALK
Identify exactly which existing Rawlsing owners, seams or runtime layers are affected.

### HANDOFF
Only `ACCEPTED_PRODUCT_REQUIREMENT` items can be packaged for governed engineering.

### VERIFY
After implementation, test whether the actual experience satisfies the product requirement.

## 3. Question statuses

- `OPEN`
- `FRAMED`
- `RESEARCHING`
- `PROTOTYPING`
- `READY_FOR_DECISION`
- `DECIDED`
- `DEFERRED`
- `OBSOLETE`

## 4. Docket structure

When a question requires more than a short adjudication, create:

`dockets/D###_<slug>/`

Recommended contents:
- `00_DOCKET.md` — question, stakes, scope, dependencies;
- `01_CURRENT_KNOWLEDGE.md`;
- `02_OPTIONS.md`;
- `03_EVIDENCE.md`;
- `04_PROTOTYPE_OR_MODEL.md` where relevant;
- `05_ADVERSARIAL_FAILURES.md`;
- `06_RECOMMENDATION.md`;
- `07_DECISION_RETURN.md`.

A docket may omit files that do not help answer the question. Do not ritualize paperwork.

## 5. Decision record law

Every decision must state:
- decision ID;
- date;
- status;
- question(s) closed;
- exact decision;
- rationale;
- evidence;
- rejected alternatives;
- consequences;
- affected workstreams;
- architecture impact;
- reopen condition.

A decision is not immortal. Reopening must cite the exact new evidence or contradiction.

## 6. Evidence discipline

Distinguish:
- project vision;
- current repo fact;
- empirical research;
- design convention;
- user preference;
- prototype observation;
- inference;
- normative choice.

Do not smuggle a normative model of flourishing in as psychology.

Do not treat market convention as moral necessity.

Do not treat compelling UX copy as architecture evidence.

## 7. Prototype ladder

Prefer the cheapest falsifier:

1. state diagrams / scenario walkthroughs;
2. scripted conversation prototype;
3. LLM prompt prototype with fixed hidden state;
4. event-sourced dyad prototype;
5. persistent single-person alpha;
6. only then broader world / social / monetized experiments.

## 8. Weekly / session discipline

At the end of a substantive Sorok session:
1. update affected question records;
2. add decisions if any;
3. add risks if discovered;
4. update `state/CURRENT_STATE.md`;
5. identify the next 1–3 highest-leverage dockets;
6. do not rewrite stable charter/ontology files unless their governing content changed.

## 9. No-chat-canonicality law

Chat is an ideation surface, not the durable project state.

Anything we would regret forgetting must be serialized into Sorok before the session ends.
