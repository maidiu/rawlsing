# SOROK P2 LOCAL ENCOUNTER LIFECYCLE — INDEPENDENT REVIEW

## VERDICT

**ACCEPT_SCOPED_TEST_ONLY** for `79b90e4a57cbd1b738a9b9484677736d1b6415ab`, parent `41bf45813fd0adeffd9b54e1306c2022abe96514`.

- Original accepted41bf scope is preserved unchanged.
- This accepts only the new local UI lifecycle boundary, not native authorization, security, absence/life simulation, world return, human validation or any science/Pyat/B grant.
- The shipping unit remains adjacent: lifecycle + accepted projection + shipped package closure.

## SCOPE

Reviewed implementation/tests in `WORKER_RETURNS/SOROK-P2-ENCOUNTER-LIFECYCLE-20261105-R1` against pinned WP19/S11/projection. The sidecar at `<state_root>/.sorok_p2_local/encounter_lifecycle.json` is local UI convenience only; it is not a tamperproof security boundary.

## EXACT COMMANDS AND RESULTS

```text
TMPDIR=$PWD/.local-logs/p2-lifecycle-review/pytest-tmp PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider   --junitxml=.local-logs/p2-lifecycle-review/focused_lifecycle.xml   WORKER_RETURNS/SOROK-P2-ENCOUNTER-LIFECYCLE-20261105-R1/tests
# 5 passed in 19.82s, exit 0

PYTHONDONTWRITEBYTECODE=1 python3 -B   .local-logs/p2-lifecycle-review/probe_lifecycle_boundary.py
# 5/5 independent probe groups passed, exit 0
```

Independent probe groups:

| Probe | Result |
|---|---|
| Fresh subprocess CLI: `new -> exit -> lifecycle/view/status OUTSIDE -> blocked SAY/DO_HELP/ATTEND -> local return -> PORTAL -> real SAY` | PASS |
| Canonical store hash, world hash, clock, event count and encounter count unchanged across exit/blocked/local-return | PASS |
| Outside block occurs before S45 projection calls (spy counts zero); local return does not call projection.return_ | PASS |
| Wrong-root sidecar `LOCAL_LIFECYCLE_ROOT_MISMATCH`; removal resets PORTAL; malformed/missing/invalid sidecar typed refusals | PASS |
| Actual importer origins; view/status outside equal accepted projection with `mode=OUTSIDE`; privacy walker clean | PASS |

Additional CLI checks: `view --text` outside reported `Mode: OUTSIDE`, `status.mode=OUTSIDE`, no `root_hash`/`root_id`/private markers. Cross-process store hashes stayed identical across exit, blocked actions and local return. Positive `SAY` after local return is a real `SOROK_WP19_INTERACTION_RESULT@1`.

## OBSERVED BOUNDARY

- `EXIT` persists `OUTSIDE`; fresh commands see it and `SAY`/`DO_HELP`/`ATTEND` are refused locally with `LOCAL_OUTSIDE_MODE_BLOCKED` before real S45 calls.
- `RETURN` while outside is `LOCAL_RETURN_ONLY`; it writes only the local sidecar and does not mutate canonical clock, world, events, encounters or store.
- `RETURN` while inside still returns the existing `RETURN_UNSUPPORTED_TYPED_HOLD`.
- Missing sidecar means default `PORTAL`; malformed/invalid/foreign sidecars fail honestly with typed `LifecycleRefusal` (CLI exit 2).
- `view`/`status` outside are exactly the accepted projection's view/status with `mode=OUTSIDE`; no fabricated absence activity.

## RESIDUAL LIMITS

- Outside view remains the pinned projection's portal-shaped view with `mode=OUTSIDE`; full S11 OUTSIDE contacts/thread surface and world-return/absence/delivery producers remain unimplemented and unclaimed.
- Local sidecar is not tamperproof and is not claimed as security/native authorization. No general concurrency infrastructure was demanded or tested.
- Blocked `SAY` returns empty `user_attempt.input`; the local refusal does not preserve the attempted utterance. This is a UX limitation, not an access-boundary failure.
- `status` retains local root/store path strings (inherited behavior) but no `root_hash`, `root_id` or projection private markers.
- No full inherited 55-test estate was rerun; no native/human/B/Pyat/science acceptance.

## NOT RUN

- Full inherited 55-test estate.
- Native C8/C9/C12, CAN008/CAN011, ADP, Pyat or human validation.
- Tamperproof sidecar/security architecture, general concurrency, or crash-consistency hardening.
- Absence/life-advance, external delivery or world-return producer.
- Full S11 OUTSIDE contacts/thread UI surface.
- Canonical-state corruption fuzzing beyond sidecar corrupt/missing semantics.

## EVIDENCE

- `READBACK.json` — exact head/source/evidence index.
- `PROGRAMMA_DELTA.json` / `.md` — compact owner-intake delta.
- `evidence/FOCUSED_5_TESTS.log` / `.xml` — independent 5-test run.
- `evidence/INDEPENDENT_PROBES.json` — five focused probe groups.
- `evidence/SOURCE_MANIFEST_AUDIT.json` — 10/10 lifecycle source hashes.
- `evidence/AUTHOR_EVIDENCE_AUDIT.json` — author evidence hashes checked, not trusted as labels.
- `evidence/CLI_TEXT_OUTSIDE_AUDIT.json` — outside text/status privacy scan.
- `evidence/REVIEW_SUMMARY.json` — compact verdict and limits.

## REMOTE READBACK

Review branch: `codex/sorok-p2-lifecycle-independent-review-20261105-r1`. Remote 40-hex head is reported in the final chat after push.
