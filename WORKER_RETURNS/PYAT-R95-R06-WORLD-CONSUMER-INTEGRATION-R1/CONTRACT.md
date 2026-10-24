# R95 R06 pre-code contract — source-separated world selected-view binding

Status: frozen before the R06 code commit; later actual-joined extension is recorded in ADDENDUM_J42_INTEGRATION.md. Sourcefree TEST_ONLY local trusted
host. Reuses accepted R05 fixture/products and the unchanged N10E positioned-
subject consumer via `compose_positioned_subject_possibility`; no new world,
possibility, FF/F6/F7, evaluator or evidence engine.

## API

`pre553_universal_world_binding.py`:

- `WorldFieldBinding`: exact empirical coordinate/field ref, typed value, exact
  subject fact ref, source universe/release, unit, role STRUCTURAL/CONTEXT,
  optional clock and relation ref.
- `WorldSelectionRequest`: fields, actual repository/empirical query/predicate/
  authority registry, release refs, consumer query, model rule, witness,
  currentness/as-of, optional relation transport, FF structural authority,
  temporal pair/observed-pair refs.
- `WorldSelectedView`: state/reason, exact field/source/release refs, actual
  unchanged consumer result object, consumer values-read and canonical view
  hash.
- `select_world_view(request)`.

## Validation

Require >=2 unique fields, currentness CURRENT, same source/release as the
consumer query and admitted release set. Different units require an authorized
exact relation/transport ref on every field; otherwise refuse
UNLINKED_UNIT_POOLING_UNAUTHORIZED. CONTEXT fields require explicit FF structural
authority. Different clocks require an explicitly observed temporal pair ref;
otherwise refuse. Consumer conditioner bindings must exactly match the field
coordinate/subject-fact set. Any mismatch refuses before consumer release.
Native owner refusal is surfaced as typed REFUSED, never converted to evidence.

## Positive / hostile

Positive uses actual two-field N10E composition: two distinct fields change the
same consumer result/view hash; cold subprocess recomputation reproduces it.
Hostile controls: wrong source/release, unlinked person/household pooling,
context-as-structural, unobserved temporal pair, revoked currentness. No all-
refuse success.

## Limits

No original source/science/F5/FF/F6/F7 issuance, R04/R05 replacement, CI/prod/
N11/N12/Sorok/J52/W52. Synthetic engineer evidence only; independent reviewer
must qualify. Cross-unit transport authorization is validated but does not by
itself create a linked indexed query.
