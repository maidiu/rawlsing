# R138 focused confirmation — repaired production binding

**Verdict: `REVISE` for query-authority scope completeness.** The actual
repeated-event native positive, changed-value/restore, foreign source snapshot,
foreign query source/universe/risk, descriptor binding, and explicit
test-only regression repairs are independently demonstrated. One exact
query-authority scope block remains: foreign target-use, measure, as-of,
grammar and frontier fields are accepted. The two banked open contracts remain
OPEN and are not counted as successes.

## Exact identity

- R138 commission: `5b86ea7979edeac7d917f3c4f6a67ade100f8f27`.
- Candidate: `98612c6d511d54acdf304ab4086547192573f403` versus rejected
  `bda89324a85ce06d44a19e6b19994e5543c065de`.
- R137 return/decisions under
  `WORKER_RETURNS/PYAT-R135-REAL-SOURCE-PRODUCTION-BINDING-R1/revisions/r2/`.
- R136 review/oracle `28b29b5c7919f85989b03b40654ebb7caa0bc9c5`; R135
  commission `52b5a43ed9c71d29ad3745aef227212202b4d9b8`; R134 task `7c9952a71`.
- Reviewer branch:
  `agent/opencode-pyat-r138-production-repair-review-r1`; writes only
  `WORKER_RETURNS/PYAT-R138-PRODUCTION-REPAIR-REVIEW-R1/`. Private probes are
  under `.r61/r138/` with basetemp there; no `/tmp` or external directory.
- Oracle frozen at `68ece3afe` before candidate code inspection.
- Candidate code blobs verified:
  `pre553_native_workload_binding.py` `b60f72668d99cd7c9f4583457be5a4d32b3168d8`;
  `pre553_production_binding.py` `6656e657c9a113f66dd7002706fbe876fcbc4bad`;
  `pre553_source_native_preimage_adapter.py` `79f9131366574a9c7bc787f71722dbbdda09814c`;
  `tests/test_pre553_production_binding.py` `a49a88dafc5f667838626e15395692098cdee0b8`.

## Independent results

| Suite | Result | Evidence |
|---|---|---|
| Author focused | 10 passed | `replay/author_focused_junit.xml`, `.log` |
| Author affected regression | 4 passed (correctly reported now) | `replay/author_regression_junit.xml`, `.log` |
| R136 frozen probes | 2 passed, 3 errors (original RED preserved) | `replay/r136_frozen_junit.xml`, `.log` |
| R138 focused probes | 4 passed, 1 failed | `replay/independent_probes_junit.xml`, `.log` |
| Cold stable-source replay | 2/2 identical SUPPORTED refs | `replay/cold_stable.log` |
| Native positive | SUPPORTED, denominator 2, numerator 2, six cells | `replay/native_positive.log` |

## Repairs verified

1. **Actual repeated-event positive and restoration.** The harness now emits an
   actual `SUPPORTED` fact with `raw_denominator_support=2`,
   `raw_numerator_support=2`, six repeated-event cells and
   `execution_detail=exact governed target distribution resolved`. Response 0
   and 1 produce different facts; restore reproduces exact refs and manifest.
   The prior UNAVAILABLE/MISSING result is removed.
2. **Source/source-authority binding.** Foreign query source SHA and foreign
   source-authority snapshots now refuse; mixed snapshot identity is checked by
   source SHA and role. The seven-role source set is validated before
   materialization.
3. **Query source/universe/risk/role binding.** Foreign query source SHA,
   universe set, risk set and wrong role refuse. The supplied authority refs
   are preserved.
4. **Descriptor binding.** Descriptor source edition, items, release,
   routing/risk, carrier, country/population, weight/design/estimand,
   missing/occurrence topology and target/conditioner/measure are compared with
   the actual bundle/projection; foreign source/country/population metadata
   refuses.
5. **Discovery honesty.** `build_production_workload` now refuses
   discovery-only input with
   `PRODUCTION_DISCOVERY_ISSUANCE_CONTRACT_MISSING`; it does not count unused
   discovery refs as a path.
6. **Explicit test-only regression** remains green: 4/4 listed source
   projection/custody nodes. No skip counted as pass.

## Remaining blocking finding — query authority scope is still incomplete

`_exact_external_query_authority` checks source SHA, universe set, risk set,
authority kind and one nonempty operation. It does not compare the authority's
`target_use_refs`, measure, as-of/currentness, grammar or frontier scope with
the actual operation. R138 probes show all of these foreign scope values are
accepted and a production catalog is built:

- `target_use_refs=[]` or `FOREIGN_TARGET_USE`;
- `measure=GOVERNED_WEIGHTED`;
- `as_of=1999-01-01`;
- `grammar=FOREIGN_GRAMMAR`;
- `frontier=FOREIGN_FRONTIER`.

Minimal same-owner fix: extend the exact query-authority check to validate
target-use, measure/arithmetic, effective/as-of currentness, grammar/frontier
scope (and the operation's actual required identity) against the request,
query, descriptor and bundle; refuse before production catalog/execution. No
new engine or science authority.

## Explicit OPEN contracts (not scored as pass)

- **Permission before physical decode.** The R137 decision is evidenced at the
  codepath: `IssuedWorkloadRecord`/`NativeWorkload` require a materialized
  projection, `materialize_native_preimages` consumes an already-decoded
  incidence, and the harness calls `decode_sav` before admission. No external
  metadata-only source-read grant exists. The author correctly refuses to
  fabricate one; this remains OPEN for HQ.
- **Bounded production discovery/frontier.** No external production discovery
  authority/frontier ingress exists; the current path is TEST_ONLY. The author
  correctly refuses discovery submission; this remains OPEN for HQ. Honest
  refusal is not a successful discovery qualification.

## Scope/limits

Sourcefree synthetic harness only; `ORIGINAL_SOURCE_GRANTED` is a code-path
label, not source/scientific issuance. No real source/respondent read, original
35/1890/F1–F8/global F6/F7/F8, learned/FF/V553, actor/person/dyad/V3,
M1-for-all, R09/CI/prod, N11/N12, Sorok/J52/W52 or production adoption is
claimed. The synthetic source/projection country/population is explicitly
SYNTHETIC and is not real production metadata. No candidate code edit,
self-adoption, source permission or new engine was performed. The branch is
pushed nonforce and directly read back; final SHA is reported separately.
