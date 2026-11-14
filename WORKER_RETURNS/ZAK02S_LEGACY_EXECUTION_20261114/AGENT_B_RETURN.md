# ZAK-02S Agent B — independent follow-upper and execution-bound return

**Terminal status: `ZAK02S_PARTIAL_WITH_EXACT_RUNTIME_BLOCKERS`.** This is a materially strengthened executable *candidate*, not completed S2 witness. Neither author-side claims nor passing source inspection substitute for historical function execution.

## 1. Exact provenance and reconstructed commission

- Protected, read-only: `integration/pre-main-reconciliation-r1@6a5c12f04323d74001f9632063ec907f4fc4468e` (verified).
- Independently read **before** Agent A: ZAK-00 owner/flight matrix at `e725ec39d021f4f7d8080298a95ea519ada2de01` and ZAK-02 S0–S1 return at `2030007c96cf2681f4aee6f3cb609d2648ec518b`. The original nine task/output identities, evidence, and six noninverse cases remain in PR #904 and were not modified.
- Historical code identity: `9253064bc9423a0f0ccda4fbdea43c2f54f800c6`; six Git blob expectations are unchanged from Agent A's harness and independently compared against pinned GitHub file identities.
- Agent A frozen artifact: PR #1041 at `c31f3ffa77cee92c51a72fe635d89cc9b170ce38`.
- Agent B is a **separate** branch, `agent/zak02s-followupper-20261114`, forked from exactly Agent A's frozen HEAD. No updates to Agent A's branch, PR #904, protected PRE-MAIN, or historical code.
- Required outcome: *actual* F08, V550J, V551J, V552, V552J, and V549b pinned historical calls with evidence of positive, negative, restore, named callers, and honest first-reader boundaries. MCR-lite governs this continuation without downgrading the inherited nine-task MCR-C contract.

## 2. Independently verified predecessor strengths

1. Agent A's runner requires an exact historical checkout SHA, six expected blob SHA-1 identities, and historical import file paths. It does not copy/reimplement historical functions.
2. F08 fixtures separate different matching override identities from duplicate rows, and wrong-wave changes both wave fields.
3. V551J fixtures preserve at least two relation components while adding an unresolved component, avoiding a confounded insufficient-relations test.
4. V552 correctly distinguishes overcount *coverage* from score permission; a diagnostic block cannot automatically be turned into score `DENY`.
5. V552J tests deterministic exact-score ordering and reverses input order rather than mistaking the selection for semantic uniqueness.
6. The reported GitHub Actions attempts did not run steps, and Agent A correctly declined to fabricate machine evidence or production/native authority.

## 3. Established defects, exact source implications, productive repairs

| Defect in Agent A artifact | Exact evidence | Agent B repair |
|---|---|---|
| One module import failure suppresses the other five families | Original `main()` imports **all six** using one loop before any `observe()` case; one `importlib.import_module` raises to global fatal handler | Per-family `load_module(family,short)` checks its historical blob/import path, emits `NOT_RUN_IMPORT_BLOCKER` for that family, then continues others. Source checkout SHA remains a global invariant. |
| V550J denominator comparison insufficiently discriminating | Original `invoke_550j` has only R1=YES and R2=NO, both answering: baseline context and answered subset have the same size | Add unanswered R3 to the sourcefree input; assert input-context 3 versus answered-variable 2, historical baseline answered n=2 and in-pattern answered n=1. Preserve *two separate* refusals: unjoined R4 versus in-context unanswered R3. |
| V552J tie test observes winner but not permission | Pinned `_packet_structural_dimension_resolution` sorts by descending score and fact ID; `build_v552j_join` consumes first matched fact and can produce `ALLOW` | Both original-order and permuted twin cases now require FACT_Z, two matches, downstream `join_permissions == ["ALLOW"]`, and `join_audit == ["MATCHED_EXACT_SCOPE"]`. This tests the *historical* permissive tie behavior; does not silently repair it. |
| Duplicated F08 negative could pass on an unrelated RuntimeError | Agent A's duplicate check only tested exception class, even though historical `_select_override` has a particular same-basis cardinality refusal | Require the actual `source_wave_var_code: 2 rows` refusal text. |
| Restore checks were only individual property assertions | Five restore phases matched a chosen ID/status/count, not equality of captured before/restore outputs; V549b used 49-candidate positive and 50-candidate restoration | Add `restoration_equivalence` comparing complete **harness-captured result maps** for all six families. V549b now has a matched 50-candidate/no-reporter control, 50-candidate/reporter negative, and 50-candidate/no-reporter restore; 49 candidates remains an independent below-threshold control. |

**Self-review correction:** Return-map equality is equality of the fields captured by the harness, **not** proof of byte-identical complete historical DataFrames. The status is accordingly `PASS_CAPTURED_RESULT_EQUAL`, not an unqualified “exact historical return” claim.

## 4. Source-level operation → effect → first reader

| Family | Pinned symbol and source-grounded effect | Historical callsite / receiving boundary |
|---|---|---|
| F08 | `ddm_v550_question_use._select_override`: distinct selected override, same-basis ambiguity, cross-basis conflicting identity | `_apply_manual_override`; original production compiler execution **UNOBSERVED** |
| V550J | `_association_candidate_trace_rows_fast`: `respondent_id_norm` inner join; answered-variable denominators conditional on members | `_association_candidate_trace_rows`; V551J compiler is a named source callsite, **not executed here** |
| V551J | `_v2_packet_status`: component certification, conflict, ambiguity, underqualification, authority and measurement gates | `build_v551j_joint_outputs_v2`; historical non-test reader **UNOBSERVED** |
| V552 | `_surface` + `build_v552_pressure_observation_index`: overcount diagnostic separate from scoring `ALLOW` | V552J handoff compiler is named, **not executed here** |
| V552J | `_packet_structural_dimension_resolution` + `build_v552j_join`: descending score/ID tie, selected fact potentially `ALLOW` despite duplicate exact-scope facts | `compile_v552j_structural_handoff.py` source callsite, **not executed here** |
| V549b | `build_answer_presence_anchors`: on a reporter-enabled 50th nested candidate, format string references `answer_type` and `cand_item_id` before assignment | historical `main` invokes builder; real downstream first reader **UNOBSERVED** |

The same two applicable boundaries remain: sourcefree fixture execution would be synthetic S2, **not** an observed historic production run; even a joined output is not automatically a production first-consumer receipt.

## 5. Improvement evidence and actual run attempts

**Directly confirmed:** The separate branch contains changed fixture predicates, family-isolated historical imports with fixed source checks, six capture-level restoration comparisons, branch-specific workflow trigger, and a pre-dependency `python -m py_compile` step. No historical implementation blob was changed.

**Not confirmed:** No GitHub Actions job executed a recorded step and there are no actual historical positive/negative/restore outcomes. After enabling the Agent B trigger the following push runs all completed as `failure` with job `steps=null`:

- `43633871982` (`928f4188...`)
- `43634144706` (`69b5ae62...`)
- `43634190440` (`6e5e90f1...`)
- `43634301755` (`1f8f5a64...`)

The authenticated GitHub job-log endpoint also returned `404 BlobNotFound` for the earlier comparable attempt; no Python traceback, syntax-failure evidence, dependency-install failure, or historical test result can be inferred. Local `git ls-remote` against GitHub fails name resolution. Neither the precise root cause of Action scheduling nor a working authorized checkout has been established.

The reproducible run remains:

```bash
python -u WORKER_RETURNS/ZAK02S_LEGACY_EXECUTION_20261114/run_historical.py \
  --legacy /path/to/9253064bc9423a0f0ccda4fbdea43c2f54f800c6-checkout \
  --out /path/to/zak02s-results.json
```

The candidate must be executed against **the actual original modules**; attempts on a rewritten approximation would not close ZAK-02S.

## 6. Challenges refuted or withheld

- **False: overcount requires score DENY.** The pinned V552 branch can report blocked coverage while separately scoring `ALLOW`. Do not rewrite that result to fit expectations.
- **False: deterministic V552J winner proves uniqueness.** The tie selection is observed in pinned *source*, not an independently authorized uniqueness decision.
- **False: V549b every invocation fails.** The unbound-name path is conditional on an enabled progress reporter and reaching the relevant 50th loop iteration; the 49-candidate control and reporter-disabled equivalent should succeed if their fixtures are valid.
- **Not established: original ZAK-02 engineering is broken because CI has no steps.** The failure is before logged test execution. Do not blame Python or historical code without job evidence.

## 7. New attack surfaces, unresolved disagreements and challenge to Agent A

- New family isolation can expose interactions among partial imports and module global initialization. Demand real imported-path traces, not inferred independence.
- V550J sourcefree R3 is represented as an unanswered row. Challenge the distinction between all context inputs, genuinely eligible response rows, and a published association (which may still be below the historical support floor).
- Captured return-map restoration equality does not cover extra historical output columns, timestamps, side effects, or an actual compiler's written artifacts.
- V552J permissive tie is source-grounded and must be actually observed, then forwarded to the legitimate current-rule/authority owner; this agent cannot impose a new rule in the legacy implementation.
- Historical `_v2_packet_status` helper execution is not packet compiler execution; named callsites are not production first readers.
- Native original35, competent source-science decisions, long-memory closure, and the nine original MCR-C independent receiving obligations remain separate.

**Agent A's strongest next challenge:** Find a qualified execution host, run the exact pinned modules, report all six families' actual observed exceptions/returns, demonstrate a true compiler/bridge first-reader case (or precise remaining blocker), prove or falsify the nonresponse and tie-permission fixtures, and attack the six captured-result restoration comparisons with a concrete mismatch. If the revised harness is wrong, produce the counterexample and correct it rather than asserting a general failure.

## 8. Graded disposition

- **ENGINEERING:** Source-grounded improvements committed; historical operational S2 **NOT_RUN**; first non-test readers **UNOBSERVED**.
- **SCIENTIFIC:** No source/causal/psychological inference, native original35, or production empirical claim issued.
- **AUTHORITY:** Independent branch/draft PR only; no inherited MCR-C closure, protected merge, or independent review credential.

**Terminal:** `ZAK02S_PARTIAL_WITH_EXACT_RUNTIME_BLOCKERS`.
