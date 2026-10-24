# Language mediation R1 (TEST_ONLY)

Bounded multilingual mediation over the unchanged same-person JOIN-E
`JoinedSession`. All fixtures are invented. This slice makes no native,
source, human-rights, general-translation or scientific-validity claim, and it
makes zero product-model/provider calls.

## What it adds

- `index.py` — derived actor+branch relation index over real C12 speech events,
  perception rows and explicit access receipts. Relations name exact source
  event hashes; contradictions and counterexamples are preserved, not averaged.
- `plan.py` — finite authorized expression plan compiled before wording. A
  source-dependent unit is usable only when a valid relation for the same
  concept/milieu/sense, language and semantic atoms exists.
- `artifacts.py` / `equivalence.py` — native speech and labeled English
  artifacts bound to one plan, checked by a deterministic finite equivalence
  court. Matching artifacts cannot strengthen an unauthorized meaning.
- `session.py` — adapter on the real `JoinedSession`; writes the admitted native
  speech event through the existing C12/world writer and stores the English view
  as a derived projection. The baseline R31E template path is unchanged when
  mediation is not bound.
- `cli.py` — demo and inspection commands.

## Run

From the worker root:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=LANGUAGE_MEDIATION_R1 \
  python3 -m language_mediation.cli demo
```

Tests:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=LANGUAGE_MEDIATION_R1 \
  python3 -m pytest -q LANGUAGE_MEDIATION_R1/tests
```

## Covered behavior

The suite exercises the actual `JoinedSession` consumer, not a stand-in:

- contradictory family/work histories reach the planner and admission readset;
- authorized plan, native speech and labeled English view share plan/artifact
  hashes and finite atoms;
- cold reopen preserves the exact admitted speech event and valid readset;
- severing a source/access receipt refuses dependent use, invalidates the
  relation, allows a lawful greeting, and restoration restores the dependent
  use;
- wrong source/access hashes and foreign branches are refused;
- stronger or substituted meanings are rejected even when both artifacts agree;
- resealed artifacts cannot drop plan source bindings;
- optional translation failure leaves the admitted native event unchanged;
- locale and attention changes affect presentation only;
- forged/tampered translation projections resolve to translation unavailable
  with the source preserved;
- the unbound R31E template baseline still works.

## Limits

The phrase/atom table is deliberately finite and TEST_ONLY; unknown language,
phrase or atom resolves unavailable/unresolved rather than being guessed. A
translation projection is re-bound to its admission and equivalence receipt on
read. Mediated encounters are branch-local; using a copied encounter on another
branch is refused as a foreign source rather than silently re-attributed.
