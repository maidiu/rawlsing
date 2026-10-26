# R142 combined independent confirmation — production ingress

**Scoped verdict: `ACCEPT_SCOPED_SOURCEFREE_PRODUCTION_INGRESS`.** The exact
R138 query-scope witness now fails closed; the repaired repeated-event query is
actually `SUPPORTED` (2/2, six cells) with value change/exact restore; foreign
source/descriptor controls remain; predecode source-read transport demonstrates
zero I/O on refusal, order, and post-decode revocation; and the bounded full
native I05 discovery emits actual supported/valid-empty facts with complete
no-drop and restoration.

No actual source read, real issuer competence or production metadata is
certified. The R136 original RED is preserved; R140 source binding and issuer
deployment remain external; R139/R140 metadata has the known erratum.

## Exact identity

- R142 commission: `3a2fccbeedc4a0f47a62c9a779fa0cc3c43c9eac`.
- Candidate: `44e7ace44d9e1b023a15d14ee1ead9b176d0e522`; R140
  `ccf97c89d276e3b1460b9bc65d380ff79d8fd97b`; R141 scope successor.
- R135 commission `52b5a43ed9c71d29ad3745aef227212202b4d9b8`; R136 review/oracle
  `28b29b5c7919f85989b03b40654ebb7caa0bc9c5`; R138 review
  `3f35210eadd9891100b6aae2ac01bb9b05d3406a`; R139 contract/R140 commission
  `8a6760daeccfc09eade88fa4365d06a86509af1a`; R141 commission
  `f67b4f2a5aae4da8869b7994f468f53d69ceb658`.
- Reviewer branch:
  `agent/opencode-pyat-r142-production-repair-review-r1`; writes only
  `WORKER_RETURNS/PYAT-R142-PRODUCTION-REPAIR-REVIEW-R1/`; private probes and
  basetemp under `.r61/r142/`; no `/tmp`/external directory.
- Oracle frozen at `d8748198b` before candidate inspection.
- Code blobs verified:
  `pre553_source_read_admission.py` `652ea3cdf0f53cd9ce14c4419486f6c1a81f3584`;
  `pre553_production_binding.py` `ad5abfe7d71b76eb421f729c1b88e4ac56a59591`;
  `pre553_native_workload_binding.py` `94ef81792ad2db7895b33dbbdaddc7e3b6b9306b`;
  `pre553_universal_workload.py` `95d19e9fa7a8d222e8b429578a8fd3efdc79f8bd`;
  tests `b0309b51b6ae23581b74af8fc0819e230636bca1` and
  `b48641813eea1fc78778c65379505d7c46d641b3`.

## Independent results

| Suite | Result | Evidence |
|---|---|---|
| Author focused production + source-read | 19 passed | `replay/author_focused_junit.xml`, `.log` |
| Listed repeated/test-only regression | 4 passed | `replay/author_regression_junit.xml`, `.log` |
| R138 six-field query-scope successor | 5 passed | `replay/r138_successor_junit.xml`, `.log` |
| R136 frozen original RED | 2 passed, 3 exception-fail | `replay/r136_frozen_junit.xml`, `.log` |
| Private predecode trust controls | 2 passed | `replay/trust_probes_junit.xml`, `.log` |
| Native query values | SUPPORTED, 2/2, six cells | `replay/native_query_positive.log` |
| Native full discovery | 150/150 candidates, 150 receipts, 330 facts, 314 supported + 16 zero, no-drop | `replay/discovery_values.log` |
| Stable-source cold replay | 2/2 identical SUPPORTED refs | `replay/cold_stable.log` |

## Repairs verified

1. **R141 query-authority scope.** The R138 witness `target_use_refs=[]`,
   foreign target use, `measure=GOVERNED_WEIGHTED`, `as_of=1999-01-01`, foreign
   grammar and foreign frontier all refuse before catalog construction. Supplied
   scope fields are checked against the actual operation; grammar/frontier are
   unsupported and refuse rather than silently accepted.
2. **Genuine repeated positive.** The production query returns
   `SUPPORTED` with numerator/denominator 2, six repeated-event cells and
   `exact governed target distribution resolved`. Response 0/1 produces
   different facts and exact restore reproduces refs/manifest. Foreign source
   authority, foreign query universe/risk/role and foreign descriptor metadata
   refuse; prior controls remain.
3. **Predecode source-read transport.** A metadata-only request contains no
   decoded capability. The exact external decision is resolved before the
   source path is touched; a valid synthetic whole file uses unchanged R04
   decoder/custody and expected SHA; selected-column extents/foreign/stale/
   revoked decisions refuse with zero decoder/open/stat/read attempts; a
   post-decode revocation closes the incidence and returns nothing. Fixture
   resolver is not deployment competence.
4. **Full native discovery.** `prepare_production_discovery` accepts the
   existing external query/discovery authorities and full frontier; execution
   uses the existing Batch/C11/I05 owners, not a second loop or scalar
   substitute. The synthetic run emits 150 expected/covered candidates, 150
   native receipts (98 supported, 52 valid-empty), 330 facts (314 supported,
   16 zero-support), exact complete no-drop, and restored receipt/fact/frontier
   identities. Foreign authority/descriptor/currentness refusals remain.

## Metadata and open boundaries

- R140's original manifest cites the R137 commission in its `commission` field;
  R141's erratum correctly identifies the actual R139/R140 seal
  `8a6760daeccfc09eade88fa4365d06a86509af1a`. The original R140 return is
  unchanged and its result/code evidence is unaffected. This is a metadata
  erratum, not a repaired code failure.
- R136's original 3 failures (old assertion forms) remain 2 passed/3
  exception-fail; they are not counted as passes.
- Actual deployment still requires a real source package/access decision and
  trusted issuer/resolver; the synthetic fixture proves code mechanics only.
  This is separate from the demonstrated sourcefree transport scope.

## Limits

Synthetic fixtures and test-harness authorities/resolvers only.
`ORIGINAL_SOURCE_GRANTED` is a transport label, not actual source/scientific
issuance. No real source/respondent read, original 35/1890/F1–F8/global
F6/F7/F8, learned/FF/V553, actor/person/dyad/V3, M1-for-all, R09/CI/prod,
N11/N12, Sorok/J52/W52 or production adoption is claimed. No candidate code
edit, self-adoption, new engine/worker/provider or broader court. The branch is
pushed nonforce and directly read back; final SHA is reported separately.
