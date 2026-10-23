# R61-R08 R8 bounded correction return

**Verdict: PASS for the single identified R7 correction; full J42/P41/E04 remains NOT_REACHED.** The explicit legacy-binding-pin migration code now survives a primary resolve cache hit, while native positives and all prior R61AF/R7 productive capabilities remain.

## Custody

- Startup: `ea39bd324d297a93bb9e87ede9b9da75dfa8750a`
- Correction contract commit (before code): `3f45fc9bc6bb5abb35427f752ef25abd4de8e79e`
- Final code commit: `80bb8c18241ebcd7ddbe559b76c6b39a72025b89`
- Branch: `agent/codex-pyat-r61-r08-r7-canonical-cache-repair-r1` (historical name; actual executor OpenCode DeepSeek V4.1-Flash MAX/Global, same author)
- R7 review read/preserved: `fc4597fb8398b8012367d8d9d1fa36502b3d798e`
- Writes only the two allowlisted code/test paths plus this `revisions/r8/` root.

## Correction

`EvidenceResolver._replay_cache` previously collapsed every
`EvidenceCacheIntegrityError` to `STALE_OR_UNAUTHENTICATED_CACHE`. It now
preserves the existing explicit codes:

- `LEGACY_BINDING_PINS_REQUIRE_MIGRATION`
- `CACHE_OWNER_DESCRIPTOR_NOT_PINNED`
- `NO_CONFIGURED_TRUST_ROOT`

Other cache-integrity/stale states retain `STALE_OR_UNAUTHENTICATED_CACHE`.
No schema, owner descriptor, envelope, native-owner, admission, live-producer or
positive-path behavior changed. Import/export limits remain explicit.

## Qualification

- Live first resolve under nonempty legacy binding pins: `SUPPORTED`, denominator
  60. Identical second resolve (cache hit): `UNKNOWN` with exact
  `LEGACY_BINDING_PINS_REQUIRE_MIGRATION`.
- Wrong descriptor pin on a live cache hit: `UNKNOWN` with exact
  `CACHE_OWNER_DESCRIPTOR_NOT_PINNED`; no support served, pin enforcement remains.
- Independent R7 review probe
  `test_legacy_binding_pin_cache_replay_has_explicit_migration_code`: **PASS**.
- Actual native positives unchanged: AT07 54/6/60 and changed 54/16/70; descriptor
  13-owner-class inventory, verifier-only replay/re-export, cold replay,
  observed-zero/ZERO_SUPPORT/valid-product/Z UNRESOLVED16 controls unchanged.

Author command (exit 0):

```text
/usr/local/bin/python3 -m pytest -q \
  rawlsing_next/tests/test_universal_evidence_binding.py \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  --junitxml=WORKER_RETURNS/PYAT-R61-R08-IMPLEMENTATION-R1/revisions/r8/junit.xml
```

**126 passed, 0 failed, 0 errors, 0 skipped, 24.90 s** (113 R08 + 13 unchanged
C1 regressions). This is author regression/qualification, not independent
acceptance.

## Mutations / restoration

- legacy pin configuration: live first SUPPORTED -> cache-hit explicit migration
  refusal; no values served, restore with a normal resolver -> SUPPORTED 60.
- descriptor pin configuration: live first SUPPORTED -> cache-hit explicit
  descriptor-pin refusal; normal verifier-only resolver restores positive.
- No setup exception/import crash counted as refusal; all assertions are typed
  result/refusal checks.

## Reach and limits

Full live J42/P41/E04 integration remains NOT_REACHED; archived returns/native
owners unedited. No original data/source/science, production/CI, N11/N12,
F6/F7/F8, actor, Sorok, J52/W52 or protected-capture authority is issued.
Same-UID host/key compromise, ptrace/root and dishonest issuer remain outside
scope. Author qualification only; a distinct reviewer follows; no self-adoption.
