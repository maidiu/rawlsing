# Universal35 D r10 — refused-artifact ordering closure

**VERDICT: ACCEPT_SCOPED_ENGINEERING** at frozen D head `70c9ae198948d5ede69064eecbf8db2643317518`.

- Code: `0b38f3c7ebc2f90ae0d716f249cd9ac6b0008267`
- Prior reviewed head: `0d48fc73292277a403ca70e0d304450f62b5444b`
- Prior G review: `e693359b44802755453f1052d340f9ead29275ab`
- Review branch: `codex/pyat-universal35-d-r10-order-review-20261106-r1`
- Published review head: the commit containing this directory; exact SHA reported in final delivery.

## FINDING

The former ordering defect is closed in the actual production wrapper, not only
at helper/static level:

- `A,A,B` from a new state root: refused
  `SOURCE_READ_DECISION_CHANGED_AFTER_CONSUMER`; no envelope artifact.
- `A,A,B` with an existing valid artifact at the same path: refused and the
  existing artifact bytes remain unchanged; no `.staged-tmp` remains.
- Valid positive run: 30 facts / 30 envelopes / 15 operations / 18 candidates;
  all 30 envelopes retain the explicit
  `("FIELD_FORGE_RELATION_PRODUCTION",)` caller ceiling.
- The helper validates permission/query before staging, writes a sibling staged
  file, and atomically replaces only after full validation. Missing query,
  missing permission, and a forced `os.replace` failure leave the prior valid
  artifact unchanged and no staged temp. Missing replay remains a typed E
  ingress failure; no new artifact is accepted as a profile.
- Reused unchanged proofs: 30 one-target facts -> 30 typed
  `FIELD_FORGE_TWO_TARGET_RELATION_REQUIRED` refusals, 0 support profiles,
  `structural_grant=false`; changed controlled source input changes actual
  fact/envelope identity; E codec blob is exactly
  `6acba005…` matching accepted `f708b468…`.

## AXES

- **Transport permission: PASS_SCOPED.** No state-root-only envelopes; explicit
  ceiling unchanged; empty/invalid permission fails before artifact.
- **No-drop: PASS_SCOPED.** 30 facts / 30 envelopes accounted; no staged or
  partial new output on refusal.
- **Positive support: NOT_RUN/MISSING.** All 30 facts are 1-target; 30 typed E
  arity refusals, 0 profiles, structural grant false. Two-target joint producer
  remains missing; no forced positive profile.
- **Artifact ordering: PASS_SCOPED.** Publish occurs after the final exact
  decision check; prior valid artifact is preserved on refusal/failure.

## PRESERVED / LIMITS

Current 35-source plan/frontier/route floors remain 18,276/18,413/18,467;
7/694/683/11; 676/4,705/249; historical 20/991 retained. Actual original facts,
authentic E handshake, A/C scale, full estate and 650 s remain **NOT_RUN/HOLD**.
No original source read, code repair, A/C/E edit, native/science/protected
promotion, or self-review.
