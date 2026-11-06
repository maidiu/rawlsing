# P3 activation/opacity implementation — bounded return

**Startup commit:** `34f4313859a9c9ef7262991dbcf805ce32ea5f96`
**Branch:** `agent/sorok-p3-activation-opacity-20261106-r1`
**Status:** AUTHOR_QUALIFIED_TEST_ONLY — not self-accepted, not final P3 runtime acceptance.

## Scope

Implemented only:

- `p3/projections.py`
- `tests/test_projections.py`
- `evidence/projections/`

No accepted #704/P2, sourcepack, PROGRAMMA, production registry, storage, compression or other worker file was edited. The S1 input review `7466d37bf5e3147efa84adb907c5f8ea28fcd1cf` is preserved unchanged.

## Frozen API

```text
activate(records, *, identity, context, registry) -> dict
project_views(*, identity, actor_experience, experience_binding,
              public_view, public_binding, standpoint) -> dict
```

Both are pure reads. They return detached documents and never persist activation
flags, lifecycle fields, memory, claims, or prose.

## Activation behavior

- Validates identity, context, registry and every source/record/rule/hash.
- Accepts only `SOURCEFREE_TEST_ONLY`, exact root/actor/branch/clock, exact
  project/counterpart and exact source hashes.
- Keeps records indexed-store-compatible; does not require a record clock field.
- Emits `ELIGIBLE` / `INHIBITED` / `UNKNOWN` per stream.
- Reports `material_eligible` independently; material ineligibility does not
  erase psychological eligibility or create resources.
- Preserves two contradictory commitments as separate entries and emits
  `CONTRADICTION` only for registry-declared incompatible modes in the same
  project/counterpart/relation/obligation scope.
- No scalar winner, score, lifecycle transition or write.
- Rejects demographic selectors and mismatched source/rule/version/hash.

## Opacity behavior

- Actor projection uses only the supplied actual `actor_experience`; it never
  substitutes the user's public view. Held actor receipts remain held even when
  the public view contains events.
- User projection is a strict subset of supplied `visible_events`,
  `visible_actions`, `visible_speech`, location and clock, filtered by
  `OBSERVE_PUBLIC_ACTION` / `READ_PUBLIC_DIALOGUE`.
- Public/actor events pass the accepted S45 public allowlists and recursive
  private/explanation-field removal. No event absent from `public_view` is added.
- No raw source/owner/hash/readset, psyche ledger, private motive, causal
  explanation or actor-private field is emitted.
- Actor and user projections carry `memory_formation=MISSING_RULE`; claims stay
  `DEFER_MISSING_AUTHORITY`. No `ActorAccessibleRenderEnvelope` is constructed.
- Bindings require exact identity + digest for actor experience and public view;
  standpoint permissions only narrow, never widen.

## Tests

Command:

```sh
S=WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1
PYTHONPATH="$PWD:$PWD/$S:$PWD/WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1" \
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -B -m pytest -q -p no:cacheprovider "$S/tests/test_projections.py" \
  --junitxml="$S/evidence/projections/test_junit.xml"
```

Observed: **8 passed in 0.09s**.

Covered: actual P2-shaped compact documents; pure/no mutation; role/relation/
obligation/access selectors; unknown/unmet selectors; material independence;
contradictions and scope; wrong root/actor/branch/clock/source/rule/hash/version;
demographic-selector rejection; permission surfaces; absent actor with visible
user; recursive private-field removal; no prose memory; no event added outside
`public_view`.

## Explicit limitations

- No P2-root integrated proof, two-batch #704 replay, storage, compression,
  P3Owner, test_rules or rendering engine in this bounded unit.
- No native CAN/ADP psychological, memory, claim, actor or human evidence.
- No `ActorAccessibleRenderEnvelope`, first-person claim, formed memory or
  positive claim entries.
- The accepted S45 public projector is preferred when importable; an exact
  allowlist fallback exists for isolated P3 import. No alternate renderer is
  introduced.
- HQ must perform final integrated runtime review with a nonauthor reviewer.

## Evidence

- `RECEIPT.json`: API, source hashes, tests, scope limits.
- `MANIFEST.json`: exact file hashes.
- `PASSPORT.json`: sanitized runtime metadata.
- `test.log`, `test_junit.xml`: executed test evidence.
- `COMMANDS.md`: exact reproduction command.

No self-acceptance or merge.
