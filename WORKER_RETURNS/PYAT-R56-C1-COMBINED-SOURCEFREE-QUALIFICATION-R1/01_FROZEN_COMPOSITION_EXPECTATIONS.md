# R56-C1 — frozen composition expectations

Written BEFORE the qualification run and before reading the C1 candidate's own
qualification outputs. Derived from the accepted R00/R02/R04 semantics, packet
25/26, the frozen policy, and the C1 test fixtures.

## 1. Synthetic source fixtures and exact tuples/domains

SAV repeated-row fixture: 4 respondents × 2 occasions, `PID`, `OCCASION`,
`SCORE`, value `(2*respondent + occasion) % 4`. Governed plan binds source
respondent tokens to `P0..P3`, occasion 0/1 to repeated-event order 0/1.

Expected exact event tuples (sorted): `("R56R02:P{r}", o,
"SUBSTANTIVE_RESPONSE", str((2*r+o)%4))` for r=0..3, o=0..1 (8 tuples).
Expected prospective I03 domain: one list per respondent in sorted respondent
order, each with the two events in occasion order, exact event ids derived from
the source sha + row + respondent + occasion + physical value binding, values
`"0"`/`"1"`/`"2"`/`"3"` per the formula.

DTA fixtures: same repeated fixture through `decode_dta` (source_format "DTA"),
plus a separate-unit DTA (household `HMEAS` + person `OUTCOME`) that must refuse
`CROSS_UNIT_POOLING_UNAUTHORIZED` before any C11.

Composition variation: reversed SAV row order must conserve tuples and the
respondent/occasion/value projection (event ids change with source sha);
5 respondents must conserve the exact denominator/cardinality shape.

## 2. Combined-path fact expectations

R04 decoder -> R02 `materialize_native_preimages` -> unchanged facade/C11 ->
unchanged I03 `execute_empirical_query`:

- `incidence.source_sha256 == sha256(file bytes) ==
  source_custody.snapshot_sha256`; `reader_access_mode == "O_RDONLY"`;
  pathname unlinked.
- `release.source_artifact_ref.content_hash == source sha`.
- `event_tuples == expected_tuples`; `domain_from_bundle == expected_domain`.
- Fact: `SUPPORTED`, denominator 4, numerator 4, 4 cells each support 1,
  repeat query same fact ref.
- DTA same expectations via `decode_dta`.
- Exact fact/release ids must remain deterministic for byte-identical inputs.

## 3. Custody/attack expectations on the combined path

- Original-path replacement after acquisition: rebuilt bundle/facts identical
  (bound source identity) for the same query.
- Foreign file at the old private snapshot pathname: not consumed; facts
  identical; `close()` leaves foreign content.
- Supplied-fd `write`/`pwrite`/`ftruncate`/shared-writable-`mmap`/`/dev/fd`
  `O_RDWR` reopen: denied before modification; digest unchanged; facts
  identical.
- Normalized respondent/source-key collisions: `NativePreimageRefusal` with
  `DUPLICATE_RESPONDENT_KEY_MAPPING` / `DUPLICATE_NORMALIZED_SOURCE_KEY`
  before any C11 release or fact.
- A permitted source value fault changes/refuses the same query/fact; exact
  original bytes restore the same fact id/payload, including a fresh process.
- Required producer dependency substitution: a source→fact assertion must fail
  by assertion-level RED and restore in a fresh process.

## 4. R00 policy/claim-ceiling expectations (separate claim)

On independently pinned policy objects (`6d95a78b`, variant CANONICAL_V1,
freeze blobs verified):

- Complete POLICY_ONLY claim: `ALLOW_LOCAL_POLICY_CONSISTENT`, ceiling
  `LOCAL_ONLY_POLICY_CONSISTENT`.
- Missing or altered frontier: `REFUSE_FRONTIER`, ceiling NONE.
- EXECUTED_NATIVE claim without R09 evidence: HOLD/refuse
  (`HOLD_TRUSTED_NATIVE` expected), ceiling local-only, never native-positive.
- GENERIC_SOURCEFREE: `HOLD_GENERIC_R09`.
- Supported status without native evidence: HOLD/refuse.
- `K_mutation` marker: `REFUSE_IDENTITY`; this is a policy conflict marker,
  NOT native association verification.
- Policy substitution (expected-operations/identity change): the same claim's
  GateDecision changes to `REFUSE_FRONTIER`; restore returns
  `ALLOW_LOCAL_POLICY_CONSISTENT`.
- No verified-evidence handle is created; no local log is treated as R09
  attestation; no native-positive gate verdict issued.

## 5. Claims separation and capability limits

- Claim (a): actual native projection/custody compatibility (decoder, adapter,
  facade/C11, I03 facts).
- Claim (b): R00 policy/claim-ceiling enforcement on the same combined tree.
- R08 serving association and R09 authenticated enforcement are
  NOT_IMPLEMENTED/NOT_REACHED; the gate remains a policy checker.
- Preserve known limits: POSIX `/dev/fd`; read-only capability trusted-runtime
  assumptions and fail-closed raw OS exceptions; DTA full-frame O(rows×cols);
  transformed R02 stream limited to the admitted facade path; DTA
  extended-missing writer skip; synthetic encoding-authority only. No
  original35/N11 scale claim.
