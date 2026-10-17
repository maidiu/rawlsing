# WG0Q Phase A — authority-body / temporal / cold-replay precommit

**Role:** independent WG0O scientific-review continuation (**WG0Q**). Not WG0P7
author, not HQ, not source/semantic issuer.

- Repository: `maidiu/rawlsing` (PRIVATE)
- Branch: `agent/reviewer-pyat-r29-wg0q-independent-authority-body-delta-court-r1`
- Sealed startup: `81075b2db946bda2623721c431c68bd0c6a95ad4`
- Review base: WG0O `3ee5d6a4e246fca89740d4d36ab26206230c83bf`
- Unrepaired candidate: WG0P6 `e7e429c3dfb649233e74e0e5106e51ff25024806`
- Write terrain: `WORKER_RETURNS/PYAT-R29-WG0Q-INDEPENDENT-AUTHORITY-BODY-DELTA-R1/`
- Future WG0P7 candidate: **UNKNOWN at freeze time; not inspected**.

## 1. Preserved WG0O inheritance

The exact WG0O 14-control oracle is copied byte-for-byte at
`01_WG0P6_STAGED/court/01_FROZEN_ACTUAL_AUTHORITY_API_CASES.json`:

- 11 negatives, 3 positives.
- The three physically RED controls A2 stale/superseded body, A3 foreign
  semantic body under the same triple, and A4 foreign governed operations under
  the same triple are preserved: each originally served 42 supported cells and
  four I03 calls.
- The 8 claimed prior typed refusals are not silently re-graded. On physical
  replay, 7 are typed (A1, A5, C1, C3, B1, B2, B3); **C2 missing-issuer is an
  untyped `AttributeError` with zero served facts and zero I03**, so the WG0O
  “8 typed refusals” claim does not strictly reproduce. It is a typed-refusal
  defect, not a served-authority RED.
- The five WG0N unconstructible controls and two historical characterisation
  failures remain NOT green and are not retroactively counted.

## 2. New finite precommitted matrix

`01_FROZEN_AUTHORITY_BODY_AND_EPOCH_ORACLE.json` adds **34 controls: 29
negatives + 5 positives** over the REAL `AuthoritySnapshot` fields, the REAL
`FixtureOwner` grant/clock surface, and the REAL `ColdCheckpoint` restore path.

### Body integrity (12 negatives)

B1 semantic fingerprint, B2 parent authority refs, B3 replay root, B4 governed
object-family removal, B5 false authority kind, B6 negative-limit addition, B7
DENY state, B8 false content-hash claim, B9 foreign scope, B10 no permitted
operation, B11 foreign governed operation, B12 foreign replay protocol ref —
each under the same `(authority_id, authority_version, authority_content_hash)`
identity triple unless the case explicitly alters the claimed hash.

### Temporal / currentness (7 negatives)

T1 expired interval, T2 missing epoch (`None`), T3 unknown epoch label, T4
plausible current interval on an unissued body, T5 supersession-only body, T6
stale single date, T7 owner knowledge clock earlier than an explicit authority
effective time. T1–T6 are adapter-body cases; T7 is the deeper owner-qualified
temporal case and is marked `deeper_semantics`.

### Source / item swaps (5 negatives)

S1 source-artifact-ref swap, S2 source-edition swap, S3 release/universe swap,
S4 same-cardinality native-item metadata swap, S5 question-ref swap.

### Owner grant / cold replay (5 negatives + 1 positive)

R1 source grant withdrawn after plan, R2 source-artifact revocation
inexpressible in the release-tag owner, R3 re-signed forged source edition,
R4 re-signed forged science/replay root, R5 cross-plan cold checkpoint.
R6 is the honest same-plan cold restore positive.

### Honest positives (4 serve + 1 cold)

P1 pristine body serves exactly 42 supported cells and four I03 calls;
P2 owner identity rebind serves; P3 replay is consumer- and receipt-identical;
P4 identical authority-body rebind serves; R6 valid cold restore succeeds.
The frozen pristine effects SHA-256 is
`4b9d03246167c93df6dde8d590fac33c24c51ef158d60abd8ee33601ca059550`.

## 3. Frozen law

- A negative must serve **no** supported original fact.
- A negative must call `execute_empirical_query` **zero** times before refusal.
- A negative must return a typed exception family or typed token. A late
  `KeyError`/`TypeError`/`AttributeError` after any I03 call is a RED, not a
  pass.
- A positive must have no exception and serve exactly 42 supported original
  cells with four I03 calls (P3 must be replay-identical).
- A source-artifact revocation that is not expressible must remain a typed
  `UNKNOWN_RELEASE_NO_REVOCATION`; it must not be declared green.
- A body that is simply mutated with a plausible current interval is still
  unissued; only an owner-qualified/current body may serve. No signing
  authority is inferred from Git hashes.

## 4. Freeze discipline

The oracle, adapter, tests and WG0P6 reproduction were committed and pushed
before any WG0P7 branch content was read. The exact freeze hashes and remote
commit are in `03_PHASE_A_FREEZE_RECEIPT.json`. Phase B will stage the finished
WG0P7 tree separately, verify Git blob and module `__file__`, and run the
original 14, this new matrix, inherited WG0M/WG0L/WG0N regressions, and the
genuine positive/cold original workload.
