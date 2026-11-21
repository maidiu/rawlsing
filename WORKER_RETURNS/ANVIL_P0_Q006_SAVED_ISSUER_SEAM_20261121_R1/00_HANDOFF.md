# Q006 saved-stream typed issuance seam — candidate

## Status

`TYPED_ISSUANCE_SEAM_IMPLEMENTED__SOURCEFREE_POSITIVE_NONANSWER_NEGATIVES_GREEN__Q103_SOURCE_DECISION_HELD`

Isolated candidate only. No q103 original-wave issuance or scientific authority
is claimed.

## Candidate code

`rawlsing_next/pre553_anvil_stream_issuance.py`

`HeldStreamIssuanceDecision` is externally supplied and held. It carries the
exact stream source/release/universe/replay roots, question ref, authorized
operation, typed authority snapshots, existing `EmpiricalPredicate` and
`EmpiricalQuerySpec`, and approved raw/nonanswer domains.

`issue_and_execute_stream_i03`:

1. requires a verified `VerifiedAnvilStreamEstate`;
2. checks the held source identity and all four roots against the estate;
3. requires exactly one matching saved `QuestionVariableBinding`;
4. requires the query condition to be the exact predicate and the query target
   to be exactly the held question/universe;
5. requires exact held authorities and an exact authorized operation;
6. reuses the existing `RuntimeObjectCatalog` constructor;
7. calls the existing `execute_anvil_stream_i03` native I03 path;
8. checks approved raw cells and approved nonanswer states;
9. checks effective live authority before and after execution and rechecks
   unchanged stream members.

No alternate evaluator, issuer, new permanent ref, TEST_ONLY promotion, or
caller-selected unscoped admission is introduced.

## Sourcefree executed proof

`proof_typed_issuance.py` / `TYPED_ISSUANCE.out`:

- positive: `SUPPORTED`, raw denominator 2, cells `0`/`1`, exact
  `PRE553_I03_QUERY_REPLAY`, stream release retained, roots unchanged;
- nonanswer fixture: native `UNRESOLVED`, approved as `UNRESOLVED`, replay
  retained;
- wrong source root: refused;
- wrong release root: refused;
- wrong universe root: refused;
- wrong replay root: refused;
- wrong question ref: refused;
- wrong authorized operation: refused by exact authority;
- missing authority: refused;
- raw outcome outside approved domain: refused;
- denied current authority: refused;
- revoked during execution: refused.

## q103 constraint

The q103 source return `4a35990659f40130f4579a3929d61238dde4b84d` still lacks
independent decisions for 97/98/99 and asked/eligible routing. This candidate
does not remap those codes or risk; q103 is not executed. The generic
`approved_raw_domain`/`approved_nonanswer_states` fields preserve those as
explicit externally supplied constraints.

## Reused / pinned

- P0 issuer handoff: `refs/anvil-p0/issuer` @ `357a0fbf...` (#1084)
- asked-eligible: `refs/anvil-p0/asked-eligible` @ `c5efdbdf...` (#1205)
- 1185 bridge: `3eee662d...`
- q103 return: `4a3599065...`
- existing 997/998 contracts were not reissued or merged.

## Owner

- **R03 / saved-release issuer owner**: accept or amend the held-decision
  issuance seam and runtime catalog construction.
- **SRC04 QSM/source/risk owner**: issue q103 97/98/99, system missingness,
  and asked/eligible decision (or narrower recorded-responses-only scope).

No original source, saved-estate rebuild/write, private custody file, protected
ref, G5 claim, or original-wave I03 was used.
