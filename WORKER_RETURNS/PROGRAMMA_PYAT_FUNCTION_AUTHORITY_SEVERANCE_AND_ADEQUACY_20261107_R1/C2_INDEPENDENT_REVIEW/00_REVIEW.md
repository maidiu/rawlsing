# Independent nonauthor review — issue #777 C2 joint consumer

**Review worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-independent-review`  
**Review branch:** `review/pyat777-joint-consumer-20261107-r1`  
**Reviewed author cut:** `751fb3fab88ab0faef4b20afeb57a89801f7cce8`  
**Author session:** `ses_1b9742b6c02745d8a69d062011` (distinct from this reviewer)  
**Verdict:** **ACCEPT_WITH_REPORTING_CORRECTIONS**

This review covers only the C2_JOINT_CONSUMER sourcefree joint-composition case
and the exact current owners it invokes. It does not accept historical J
equivalence, native/science/actor authority, structural admission, or any
protected merge.

## Independently reproduced

- The author probe replay is **byte-identical** to
  `C2_JOINT_CONSUMER/logs/probe_joint.json` (`09_PROBE_DIFF.txt`).
- The four named sourcefree tests pass: **4 passed in 1.52s**
  (`02_FOCUSED_TEST_LOG.txt`). The actual owners are the current N10E provider,
  C1 composition, and plain F8 evaluator over the 58-row synthetic
  nonrespondent fixture; `real_subject=False`.
- Additional focused checks pass: production/consumption distinct-call test,
  real provider-state-vocabulary test, and cross-sample refusal test
  (`05_EXTRA_FOCUSED_TESTS.log`, 3 passed).
- Independent fixture arithmetic reproduces the claimed exact values:
  **32 / 18 / 9/16**, **16 / 10 / 5/8**, **8 / 6 / 3/4**
  (`08_FIXTURE_ARITHMETIC.txt`).
- Source hashes match the author receipt:
  provider `99d71605…`, composition `2358cd26…`, consumer `9c041cb1…`,
  candidate/fixture `78f85aea…` (`07_SOURCE_HASHES.txt`).
- Actual provider vocabulary is `EXACT_SUPPORTED_SLICE_PRODUCED`; composition
  state `SUPPORTED`; consumer state `EXACT_SUPPORTED`. The actual F8
  consumption is a distinct invocation from production; the focused
  production/consumption test passes.
- Actual refusals observed: wrong conditioner order and false pairing via
  `ConditionValueRelationMismatch`; wrong source universe via
  `PositionedSubjectPossibilityError`; missing registry via
  `EmpiricalQueryExecutionError` (`06_ACTUAL_PROVIDER_AND_MISSING_AUTH.txt`).
  The four named tests assert wrong-order and false-pairing; wrong-source and
  missing-registry are additionally observed, not all asserted in those four.
- The fixture declares all non-grant effects false and no real current; the
  no-rights/no-real-current test passes.
- F13 is excluded as a marginal/aggregate ancestor; no aggregate reconstruction
  is claimed.

## Required reporting corrections

### C2-R1 — Probe `provider_state` is hardcoded/mislabeled

`C2_JOINT_CONSUMER/probes/probe_joint.py:166` emits
`"provider_state": "EXACT_SUPPORTED"`. The real provider state is
`pre553_empirical_possibility_provider.py:53`
`EXACT_SUPPORTED_SLICE_PRODUCED`, as asserted by
`test_single_conditioner_step_uses_real_provider_state_vocabulary:413`.
`EXACT_SUPPORTED` is the consumer result state, not the provider state. The
positive function behavior is independently proven; the probe field must be
derived/renamed rather than stated as provider evidence.

### C2-R2 — “Cold restore” is a same-process deterministic rebuild

`probe_joint.py:147-155` calls `pc.build_synthetic_world()` a second time in the
**same process** and compares step IDs, denominators, cells, evidence refs and
consumer states. This proves deterministic rebuild/replay only. It does not
prove a cross-process persisted restore, serialization, cache cold start, or
durable world reconstruction. The author return/test receipt should say
“same-process deterministic rebuild”; cross-process persisted restore remains
`NOT_RUN`.

### C2-R3 — Broad Exception capture leaves two negatives observational

`probe_joint.py:58-63` catches any `Exception`. The four named tests cover full
positive chain, unordered conditioner order, false pairing, and no-rights/no-real
current; they do not assert wrong-source-universe or missing-registry types. The
probe records the actual observed types, but a broad catch is not a typed
assertion. Either add explicit `pytest.raises`/probe type assertions for those
two cases or label them “observed, not asserted”; no behavior failure was found.

### C2-R4 — J demand label is stronger than the witness evidence

`04_MINIMAL_OWNER_ACTIONS.tsv:3` labels J-02
`HISTORICAL_ONLY_OR_NO_JUSTIFIED_CURRENT_CONSUMER__AT_O11`. The actual evidence is
that **no selected original J issuer/row/version is present at this O11
witness**; `01_CASES.jsonl` C2-J02 has `first_consumer=None`; `C2-J01` has
`selected_issuer=UNKNOWN`, `selected_document=None`, `historical_j_equivalent=UNPROVED`
and `proven_severance=False`. This does not establish historical absence, a
whole-pipeline equivalence/severance verdict, or an absence of future demand.
Retain the bounded wording: historical F17/F19/F20/F21 unmatched at O11;
selected-issuer/demand not established. The J-01 HOLD action correctly asks for
the actual selected non-test demand or an explicit no-demand decision.

### C2-R5 — Keep shadow/old-version/revocation visible in the summary

`01_CASES.jsonl` C2-J01 already records
`old_version_shadow_revoked: NOT_RUN__NO_SELECTED_J_ISSUER_OR_VERSION`. That
explicit NOT_RUN should also appear in the concise return/limits; no new
original issuer or authority requirement is justified merely by the existence
of old J documents.

## Bounded J / F17 scope

`F17_J_REGISTRY`, `F19_J_PATTERN`, `F20_J_PACKET` and `F21_J_STRUCT` are, at
this named O11 consumer, **unmatched historical candidates / no selected original
J issuer**. This is bounded witness evidence, not proof of historical absence,
not a whole-pipeline severance/equivalence verdict, and not a finding that old J
documents are unneeded everywhere. The current generic C1/N10E/F8 composition
accepts caller-supplied exact determinants and synthetic test authorities; that
is not an original J issuer trace. `F13_V550_BRIDGE` remains excluded as a
marginal/aggregate ancestor. No J installation, private cache restore, new J
compiler, or new original issuer is authorized or inferred.

## Proof limits

- Synthetic nonrespondent fixture only: 58 rows, `real_subject=False`; no
  respondent/SAV/DTA/DB bytes were read.
- Sourcefree composition only; no native/science/actor/current grant, no
  structural admission, no FF/post-FF/world effect.
- The four named tests are current-owner evidence, not historical J parity or
  original-source provenance.
- Same-process deterministic rebuild is not a persisted cold restore.
- No full test suite was repeated; the author's four named tests were run, plus
  three minimal related checks.
- No original J issuer/version/shadow/revocation authority was selected or
  created. C2-J01 explicitly keeps those `NOT_RUN`.

## Minimal indispensable next action

Author/owner reporting correction only: derive/rename the provider state, label
the same-process rebuild honestly, add typed assertions (or observational labels)
for wrong-source/missing-registry, and relabel the J-02 demand disposition to
“no selected J issuer at O11 / demand not established.” Preserve the verified
sourcefree positive/refusal results and the bounded unmatched-J disposition. No
new engine, production patch, issuer, science/native/actor grant, or protected
merge is warranted.

## Artifacts

`00_REVIEW.md`, `01_FINDINGS.jsonl`, `02_COMMANDS_AND_EVIDENCE.md`,
`02_FOCUSED_TEST_LOG.txt`, `03_PROBE_REPLAY.json`, `04_PROBE_REPLAY.err`,
`05_EXTRA_FOCUSED_TESTS.log`, `06_ACTUAL_PROVIDER_AND_MISSING_AUTH.txt`,
`07_SOURCE_HASHES.txt`, `08_FIXTURE_ARITHMETIC.txt`, `09_PROBE_DIFF.txt`.

All writes were confined to this review lease. No author/production/test/HQ/
peer/protected writes; quota UNKNOWN; STOP after commit/push.
