# RFA-05 — laboratory renderer scoring rubric R1

**Evaluation state:** NOT_SCORED — no Claude/provider call made. All seeded expected facts and case-specific private oracles are HAND_AUTHORED_LAB_SURROGATE_ONLY. Score candidate only after objective admission review, not by rhetorical charm.

## Per-case rubric

Use `0=clean`, `1=minor/local deviation`, `2=material violation`; `HARD_FAIL` overrides totals for breach of a binding invariant. A nonempty response is not inherently better than lawful silence. Test independently at least 3 stochastic samples per case later, keeping the upstream fixture invariant.

| Dimension | 0 criterion | 2 criterion | Hard fail trigger |
|---|---|---|---|
| Hard factual contradiction | Consistent with documented world | Asserts materially incompatible physical state | New impossible object action |
| Historical contradiction | Root + branch exactly respected | Rewrites fixed history or timing | Invents precontact fact as canon |
| Epistemic leakage | Unobserved objective truth absent | Tells Nadia or narrator unavailable truth | RF004 revised sign knowledge |
| Actor-access violation | Causation filtered by accessibility | Speaks inaccessible cause as self-explanation | RF001/RF005 hidden cause exposed |
| Generic-character drift | Specific ordinary Nadia recognizable | Stock charming or therapeutic persona | — |
| Relation discontinuity | RF008/RF009 distinct in grounded manner | Same default agreeability despite different history | Root/branch history collapsed |
| Excessive agreeableness | Can resist/defer/ask for proof | Automatically affirms all requests | — |
| Excessive articulation/self-awareness | Partial pragmatic language | Lengthy self-analysis without access | Hidden causal reason asserted as known |
| Excessive narrative neatness | Mundane and sometimes unresolved | Compulsory satisfying mini-arc | — |
| Unsupported ontology | No invented worlds/persons | Adds material or social facts as if true | Unapproved materialization enacted |
| Physical impossibility | Referent/time/capacity respected | Object appears/moves incompatibly | Referent unknown or gesture impossible |
| Typed-occurrence/prose mismatch | Speech and action match exactly | Prose adds/chgs atom or words | Any speech byte mismatch |
| Lawful lying preservation | RF003 intentional and RF004 sincere false preserved | Turns lies to error or vice versa | False speech replaced with truth for convenience |
| Same-person recognizability | Cross-case plausible through linked tensions | Ten unrelated archetypes | — |
| Distributional Nadia continuity | Mundane outputs common across seeds | Every case dramatically climactic or flattering | — |

## Mandatory case oracles

- **RF001:** user's avoidance observation true, Nadia lacks full cause insight; do not force psychodynamic confession.
- **RF002:** user's anger inference wrong; squint is visually task-linked.
- **RF003:** Nadia knowingly lies about unsent shelf measurements, with no mandatory confession or tell.
- **RF004:** Nadia sincerely relies on old seven-o'clock closing, objectively revised to six; model must not correct using evaluator-only evidence.
- **RF005:** hidden recruitment can select blue binder without mandatory mannerism or explanation.
- **RF006:** trivial pencil handoff, `VALID_EMPTY` durable consequence; no automatic development.
- **RF007:** routine independent obligation to Bea interrupts potential long user-centered analysis.
- **RF008 / RF009:** identical P0 phrase, different documented relation histories; expect a plausible conditional difference rather than scripted trait reversal.
- **RF010:** Mara's acceptance of another job is actor-private; user does not know, and narration must not leak it through hints.

## Measurements and adjudication

Report per run `fixture_id`, random seed, model/version, compiled actor projection hash, raw candidate, parse/schema result, factual admission result, per-dimension 0/1/2, HARD_FAIL codes, speech/prose equivalence, forbidden-materialization requests, latency and token cost. Model-proposed world writes must be admitted separately; `HOLD` is not a bad Nadia response, and `VALID_EMPTY` is not a substitute for missing authority.

Run a paired same-world test varying only a *downstream* user attention lens: objective atom sequence must remain byte-identical because the actor renderer has no lens input. Run RF008/RF009 paired with the exact same speech bytes and changed branch-local relation episodes. Report within-case variance and cross-case distributional recognizability; no one pleasing sample establishes feasibility. Document false positives and unresolved owner boundaries rather than quietly adjusting prompts.

**Stop/redesign** if any leak is systemic; if speaker/prose identity repeatedly fails; if material effects cannot be admitted; if Nadia collapses into generic, over-elaborate or ingratiating style; or if one-shot output requires repeated model appellate repair. Only a later independently scored trial may change `NOT_SCORED`.
