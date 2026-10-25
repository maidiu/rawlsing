S46 exact repair1, same original session/branch. HQ reproduced BLOCKED performing repair/material depletion and rehashed zero domain hash accepted with verify true. Independent review41 exact 9f6486799322e2254ab645f173e6eaed9d1e5d2b is REVISE. Repair only its four demonstrated blockers below. Preserve original commission scope and actual full goal. No new psychological law, arbitrary probabilities/learning, native authority, T/targets, adult-workshop-as-childhood, daily spam or years multipliers. Implement the missing actual consumer edge, not a parallel evidence reader. Use existing owner-qualified TEST_ONLY bounded-period world mechanism with explicit lawful coarse activity semantics; do not claim instantaneous repair covers a span merely by moving clock. If indispensable semantics cannot be implemented within settled finite material/time domain, return the exact limitation rather than invent psychology. Minimal S42/S45 seam edits already authorized by original commission. Keep same person/root/branch/canonical ledger/cold/native English. Add focused regressions for these defects and same normal consumer source/currentness cut/restore. Run preserved review reproducers, focused suite. Commit/push same author branch and return exact cut/scope/results. No unrelated improvements, no external writes or new agents. Read-only reviewer evidence available at /Users/matthewsmith/repos/rawlsing-controller/.worktrees/sorok-incumbent-review/SOROK_REVIEW/S46

# S46 interval participation — REVISE

Decision: **REVISE**.

## Exact cut

- Candidate: `fb9e72e0fc53682ac52245058872ce9f820ad5a4`.
- Branch: `codex/sorok-s46-interval-participation-consumer`; remote matches.
- Base: accepted S45 `f26a138e20d53c809d611cf8d834ec647b0804bf`.
- Reviewed in a disposable fixture using the existing warm S45/S44 dependencies.
  No product edits, provider/model calls, extra agents, launcher/notifier
  changes, native science/source/human grants, or `/dev` redirection.

## Executed checks

```text
PYTHONPATH=<S46 return> python3 -B -m pytest -q \
  <S46 return>/tests -p no:cacheprovider
10 passed in 21.19s
```

`run_s46.py` exits 0 with the S45 root/person, two bounded segments, a real
repair-derived material change, subsequent S45 SAY/DO_HELP/ATTEND, cold reopen,
targetless `NO_CHANGE`, and verify true. The focused tests cover ACTUAL,
SCHEDULED_ONLY, CONSTRAINED, DECLINED, UNKNOWN, supersession, some owner/model
forgeries, and S45 compatibility.

## Blocking findings

### 1. `BLOCKED` is not implemented; it performs the activity

`make_domain(mode="BLOCKED")` produces an `ATTEMPT` (the fallback branch in
`s46/producer.py:_attempt_receipt`), executes `product.repair`, consumes
material, and returns `PARTIAL`/`CONFIRMED`:

```json
{
  "mode": "BLOCKED",
  "attempts": ["ATTEMPT", "ATTEMPT"],
  "world_statuses": ["CONFIRMED", "NOT_PERFORMED"],
  "material_before": 1,
  "material_after": 0,
  "status": "PARTIAL",
  "verify_ok": true
}
```

BLOCKED must remain a qualified prospective/obstructed input and must not
become an actual actor attempt or world success.

### 2. The interval receipt is disconnected from the S42 consumer

`S46Session.world_prerequisites` only wraps the accepted S41 function, and
`S42Session.admit_event` calls `s41.event.world_prerequisites` directly. The
interval state, currentness, source and owner receipts are never supplied to
that path. The positive S42 readset is explained by ordinary
`product.repair` material depletion, not by validating the interval receipt.
Revoking/forging the interval state therefore cannot change the claimed
conditioning path; the focused test only observes the resource side effect.

### 3. A forged domain hash is accepted by the actual interval reader

A real state was copied, its `domain_hash` changed to 64 zeroes, and its state
and receipt hashes recomputed. `validate_interval_state` accepted it and
`read_interval_states` returned it with `verify_ok: true`:

```json
{
  "validated_domain_hash": "0000000000000000000000000000000000000000000000000000000000000000",
  "read_domain_hash": "0000000000000000000000000000000000000000000000000000000000000000",
  "read_status": "PARTIAL",
  "verify_ok": true
}
```

`validate_domain` checks model/owner strings but not the domain hash or an
independent domain/source issuance record; `validate_interval_state` does not
revalidate the domain. Matching owner/model strings alone are not issuing
authority.

### 4. One instantaneous action is marked as full-span coverage

For an ACTUAL domain `[222,226]`, one repair event at the first segment start
is used to produce coverage `[[222,224]]`; the producer then advances the clock
to 224 and marks the whole segment REALIZED. The model declares a coarse
`resolution` label but no action-to-span coverage rule or actual span evidence.
This is a relabeled instantaneous event rather than demonstrated bounded-period
coverage; no daily/yearly events are added, but the coverage claim is not
independently established.

## Required repair

- Implement BLOCKED as a typed obstructed/nonperformance mode with no repair
  attempt or material mutation.
- Add an explicit validated interval/currentness seam that feeds the actual
  S42 `world_prerequisites`/`ContinuationProducer` path, with source/access
  revocation and restoration at that same consumer.
- Bind state validation to the actual domain/source issuance record and reject
  rehashed forged domain/span/status/coverage/owner/action evidence.
- Declare and enforce the coarse action-to-coverage semantics, or stop claiming
  full-span coverage from one instantaneous repair.

Preserve the already demonstrated S45 root, actor/branch, material state,
native/English, cold, unsupported/denied, and ATTEND behavior.

## Receipt

- 10-test output: `evidence/s46-tests-10.out` SHA-256
  `b0c70b7e812eb271809960c4b3ddce1420e30b7b593ac8f82eb91c3d8877a5b5`.
- Entrypoint: `evidence/s46-entrypoint.json` SHA-256
  `29d4326f60d19aded339968322f3fd0771387415a20d4b2d8f29a6d235aac425`.
- BLOCKED-mode reproducer: `evidence/repro_blocked_mode.py` SHA-256
  `80a0a0d858907e901107d65525c4ba5a0a5b9280e2addb259b519f525cc8a638`;
  output `evidence/s46-blocked-mode.json` SHA-256
  `68d2a3dbcd5236640a0ba98af2afa1cb596667e31cca0cae3dbe63038d7ce499`.
- Domain-forgery reproducer: `evidence/repro_domain_forgery.py` SHA-256
  `19f1f35e987253d942d01be1b0d82f94e4b0c7466fa364499d862159c243c3f9`;
  output `evidence/s46-domain-forgery.json` SHA-256
  `39abfbc84861f46a99e9ddba85e0d93f61d503836b03157c7f67dd2fd6ef9540`.
- Source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed.
