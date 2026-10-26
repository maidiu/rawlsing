# R152 independent review — documentary native scientific binding

**Verdict: `REVISE`.** The documentary item/context/conservation and LiTS
partial-resolution grain is demonstrated, and the two WVS occurrences/incomplete
inventory are real native objects. One exact WVS binding defect remains:
`NativeSourceRule.administered=True` is fabricated while the same occurrence
says administration is `UNKNOWN`; WVS form/unit/topology are hardcoded rather
than read from the source-specific package/authority. This is a false typed
authority/default promotion under the R150/R151 contract.

## Exact identity

- R152 commission: `26d61f11d4213192b30c1842ae3772696dfc2560`.
- Candidate: `e3a95fef6eecfbac56341553cf3482ccd750a351`.
- R150 contract `5d68b349e2af147a58b05bba3b0818399226692f`; R151 defect
  contract `d6b235ca069ec3a128343f0ee80d5024f0672832`; R148 metadata
  `29982440dd3148552b23173af0c52288393023f5`; native engine
  `44e7ace44d9e1b023a15d14ee1ead9b176d0e522`.
- Reviewer branch:
  `agent/opencode-pyat-r152-native-scientific-binding-review-r1`; writes only
  `WORKER_RETURNS/PYAT-R152-NATIVE-SCIENTIFIC-BINDING-REVIEW-R1/`. Private
  probes under `.r61/r152/`; authorized staged inputs read under
  `.r61/r150-scientific-native-input/inputs` and
  `.r61/r151-grounded-native-occurrences/inputs`. No external/author-worktree or
  `/tmp` read.
- Oracle frozen at `98d48cdad` before R151 code inspection.

## Independent results

| Suite | Result | Evidence |
|---|---|---|
| Author R151 focused tests | 6 passed | `replay/author_junit.xml`, `.log` |
| R152 conservation/native-type probe | 1 passed | `replay/independent_probes_junit.xml`, `.log` |
| R152 WVS administration/default-form probe | 1 failed | same |
| Generated summary/evidence | conservation and WVS values inspected | `replay/summary_witness.log`, `replay/native_inspect.log` |

Verified:

- 4,460 B49 item records, 3,804 conditioner/context items retained, 26
  unmatched relation holds, all 35 source cells; 4,493 preparation items.
- 38/38 typed surfaces consumed; 18 exact typed domains, 17 raw codebook
  domains, 4 units, 2 topologies, 4 risk sets.
- Actual WVS7: 2 Occurrence objects, 2 NativeSourceRule objects, 1 incomplete
  SourceInventory; domain is exact `[1,2,3,4,5,-1,-2,-4,-5]`; risk set is the
  exact WVS7 package binding; inventory is `inventory_complete=false` with
  explicit gaps.
- LiTS-I `q301_2`/`q301_7`: typed domain, selected-respondent unit and D03 risk
  set resolve; topology stays unresolved; no fake Occurrence is constructed.
- Context items are not promoted to target measurement; no decoder/survey call;
  current source grant/U/Epre remains null; `native_execution_authorized=false`.
- No casefold joins, no collision substitution, no global absence claim.

## Blocking finding — WVS unknown administration promoted; source-specific defaults not bound

Generated SRC35 native objects show:

- each WVS Occurrence: `administration="UNKNOWN"`;
- each paired `NativeSourceRule`: `administered=true`;
- forms: `["DEFAULT_FORM"]`;
- unit/topology: hardcoded `SOURCE_ROW_IDENTITY__EXACT_SAME_WVS7_RECORD` /
  `SCALAR_SINGULAR` literals in `_wvs_package`, not read from the WVS package.

The R150/R151 contract says source-specific unit/topology/risk/domain must come
from the proper source authority, unknown administration must remain unknown,
and native constructor defaults must not silently promote unknowns. The typed
surface itself is representation-only (`documentary_unknowns="representation
only"`), and the WVS package contains no exact `administered` evidence for these
items. The constructed rule therefore asserts administration that the evidence
does not establish; the default form is also unbound.

Minimal fix at `runtime/grounded_occurrences.py`:

- Bind WVS unit/topology/forms/administration from the exact WVS package or
  source-specific authority fields; do not use literals/defaults.
- If exact administration is absent/unknown, do not construct a `NativeSourceRule`
  with `administered=true`; retain the occurrence as `UNKNOWN` and use a typed
  pending rule/no rule, updating the claimed counts honestly.
- Preserve the two Occurrence objects and incomplete inventory only with exact
  grounded fields; do not fabricate a default form.
- Re-run the same conservation, LiTS partial and no-decoder controls.

## Preserved limits

This is partial documentary typed-input qualification only. No source/respondent
read, current source identity/grant, U/Epre, scientific frontier, empirical/
learned/FF execution or current adoption. No full35/1890/F1–F8/global
F6/F7/F8/LongMemory/C5, R09/CI/prod, N11/N12, Sorok/J52/W52, actor or source/
science claim. No candidate edit, source fixture as original positive, new
worker/engine or broader court. The next actual product edge remains exact
source/current metadata and grounded native inputs, not this synthetic partial
grain.

The branch is pushed nonforce and directly read back; final SHA is reported
separately.
