# ZAK-02S — pinned historical operational execution candidate / adversarial handoff

**Return grade:** `ZAK02S_PARTIAL_WITH_EXACT_RUNTIME_BLOCKERS` — executable harness and GitHub Actions workflow published, but **NO S2 test steps have run**. Neither an unstarted job nor source-predicted output is a passed execution. This is NOT `ZAK02S_EXECUTED_AT_SCOPED_GRADE`.

## 1. Exact artifact, source cuts, reproducibility

- Source branch: `agent/zak02s-legacy-execution-20261114`, independently forked from the protected `integration/pre-main-reconciliation-r1@6a5c12f04323d74001f9632063ec907f4fc4468e`.
- Source-only historical implementation cut: `9253064bc9423a0f0ccda4fbdea43c2f54f800c6`, with six individually pinned Git blob SHA-1 identities embedded in `run_historical.py`.
- Prior ZAK-02 S0–S1 candidate is **unchanged** at PR #904 / `2030007c96cf2681f4aee6f3cb609d2648ec518b`. Original nine MCR-C IDs and documentary artifacts remain there; this PR does not rewrite them.
- Executable: `WORKER_RETURNS/ZAK02S_LEGACY_EXECUTION_20261114/run_historical.py`.
- Automation: `.github/workflows/zak02s-pinned-historical-execution.yml`.
- Machine-readable receipt of actual orchestration and blockers: `RUNTIME_RECEIPT.json`. **It is not a synthetic PASS fabricated to fill the missing execution results.**

Local reproduction, on an authorized GitHub checkout with Python 3.11 and network to obtain dependencies:

```bash
git clone <authorized-repo-url> zak02s-candidate
cd zak02s-candidate
git checkout agent/zak02s-legacy-execution-20261114
git clone <authorized-repo-url> /tmp/zak02s-legacy
git -C /tmp/zak02s-legacy checkout --detach 9253064bc9423a0f0ccda4fbdea43c2f54f800c6
python -m pip install pandas==2.2.3 numpy==2.2.6 scipy==1.14.1 pyarrow==18.1.0 duckdb==1.1.3 PyYAML python-dotenv psycopg2-binary
python -u WORKER_RETURNS/ZAK02S_LEGACY_EXECUTION_20261114/run_historical.py --legacy /tmp/zak02s-legacy --out /tmp/zak02s-results.json
```

The runner checks the historical commit SHA, every source blob SHA, and every imported module's `__file__` before exercising the function. It writes JSON **even if individual assertions fail** and exits nonzero for a failed assertion. GitHub Actions additionally attempts to upload that exact output as an artifact. An operation's positive/negative/restore trace is not achieved until this command actually completes.

## 2. Governing contract and preserved jurisdiction

ZAK-00 owner map `WORKER_RETURNS/VMESTYE_ZAK00_V2_MCR_AUTHOR_EXECUTION_20261110_R1/03_FULL_FLIGHT_DEPENDENCY_AND_OWNER_MAP.md` at `e725ec39d021f4f7d8080298a95ea519ada2de01` assigns ZAK-02 historical V549b–V552J operation and first-reader succession, not the whole ZAK mission. ZAK-02 return `WORKER_RETURNS/VMESTYE_ZAK02_MCR_R1/00_RETURN.md` at `2030007c96cf2681f4aee6f3cb609d2648ec518b` preserves nine original obligation identities: `ZAK02-TASK-01` through `ZAK02-TASK-04`, `ZAK02-HOSTILE`, and `ZAK02-OUTPUT-01` through `ZAK02-OUTPUT-04`. Their original independent MCR-C receiving has not been discharged by this narrower MCR-lite continuation.

The six inherited noninverse exceptions are **not overwritten or recast as operational PASS**: `T1-ZL03-ZL03-T11`, `T1-ZL07-TR-041`, `T1-ZL03-UNTRACED-ZL03-F16`, `T1-ZL05-ZL05-OP-003`, `T1-ZL08-ZL08-T-CODE-LMX-016`, `T1-ZL02-ZL02-T-F09_ROUTING`. F03 existing ZAK-01 synthetic witness is not rerun here.

## 3. Operation → effect → actual first-reader qualification

| Operation / pinned symbol | Positive / negative / restore to execute | Historical caller established from actual source | Non-test production first reader |
|---|---|---|---|
| F08 `ddm_v550_question_use._select_override` | source/wave/variable row; different matching identity and duplicate refusal; replay | `_apply_manual_override` at historical source line 1394 | **NOT_OBSERVED**; contract builder further downstream |
| V550J `_association_candidate_trace_rows_fast` | respondent-ID match, disjoint respondent refusal, replay; baseline versus answered denominator | `_association_candidate_trace_rows` source line 4065; V550J to V551J compiler path in prior return | **NOT_OBSERVED** |
| V551J `_v2_packet_status` | two qualified components; ambiguity/conflict/unexplained/underqualified/measurement refusals; replay | `build_v551j_joint_outputs_v2` source line 1544; `compile_v551j_joint_evidence_packets.py` named prior callsite | **NOT_OBSERVED** |
| V552 `_surface` plus `build_v552_pressure_observation_index` | selected n=[1,1] / denominator 2, overcount n=[2,2], independent score ALLOW, replay | observation builder source line 163; structural compiler feed | **NOT_OBSERVED** |
| V552J `_packet_structural_dimension_resolution` plus `build_v552j_join` | single exact fact, two different equal-score exact-scope facts, order permutation, wrong-run refusal, replay | `build_v552j_join` source line 135; `compile_v552j_structural_handoff.py` named prior callsite | **NOT_OBSERVED** |
| V549b `build_answer_presence_anchors` | 49 candidate control, 50th reporter path expected unbound-name exception, identical 50 without reporter restores | historical `main` line 941 | **NOT_OBSERVED** |

The predicted twin-fact winner is lexicographically descending `FACT_Z`, not a validated semantic uniqueness constraint. The predicted V549b `NameError` has **NOT** been reproduced; it must not be asserted as an executed bug. A coverage overcount is **not automatically a score DENY**. Those are hypotheses until the pinned calls run.

## 4. Strongest achieved result and actual GitHub runtime blockers

1. The historical symbols, definitions and internal callsites above were fetched directly from pinned GitHub blobs, not inferred from test names. The runner and workflow are remotely committed, and draft PR is open.
2. GitHub accepted both push and pull-request events for the workflow, but **created jobs terminated `failure` with `steps=null`, `logs_url=null`, and no artifacts**. The log endpoint returned `404 BlobNotFound`. This does **not** demonstrate source import or a Python test failure, because there are no executed steps to inspect.
3. Independent canonical-tree CI on the same branch also terminated `failure` with `steps=null`. The proximal barrier is **GitHub Actions runner/job allocation or orchestration before any recorded step**; the ultimate cause is unknown. Do not assert billing, repository invalidity or a source-code error without actual job evidence.
4. The local container cannot clone GitHub: `git ls-remote https://github.com/maidiu/rawlsing.git HEAD` returned `Could not resolve host: github.com`. The authenticated GitHub connector permits source reading and PR/branch writes, but cannot hand off a complete Git checkout to this local runtime. No offline approximation was substituted for original module imports.

**Actual run references:** Push `43631412889`, PR `43631432512`; second head push `43631720658`, PR `43631725231`; canonical paired `43631432464` and `43631725135`. Each is an orchestration-failure record, **not a completed historical-run receipt**.

## 5. Own hostile findings and repairs

- Initial F08 distinct-match fixture also selected both rows by question ID and therefore tested duplicate matching rather than the intended cross-key conflict. **Repaired** by disjoint question/variable keys, requiring the exact distinct-row exception text.
- Initial F08 wrong-wave negative retained the original `canonical_wave`, allowing canonical-wave matching and invalidating the denial case. **Repaired** with both wave coordinates varied.
- Initial V551J unresolved-component fixture also had fewer than two relation components; the insufficient-relation blocker would mask the intended unresolved component. **Repaired** with two valid relations plus one unresolved component.
- The runner's negative for V552 is intentionally not a score DENY assertion. Assert overcount coverage separately from observed score permission, as the historical code requires.
- No source file at the 9253 pin was patched. No current authority/source science rule or actor behavior was created.

## 6. Remaining limitations and likely adversarial attack surfaces

The most important remaining test is to acquire a **working qualified runner**, rerun the exact command, and commit its real machine-readable trace, including failure evidence. After the first actual run, inspect fixture-schema and import compatibility, cross-check all six families against actual results, and amend **the harness fixture only** where its assumptions were wrong; never patch historical source to make the expectation pass.

Prioritize the V550J membership-frame field requirements and denominator/eligibility distinctions; V551J authority token/measurement statuses and conflicting ordered vectors; V552 complete versus overcount without conflating ALLOW; V552J second-ranked equal-score fact and whether the consumer ever notices it; V549b conditional log branch and reporter timing. Verify whether `legacy` checkout and dependencies actually import before claiming module-level execution. An independent reviewer must check actual first readers rather than simply believing these named source callsites.

## 7. Rejected alternatives

- **Do not rewrite legacy functions in a test double**: would manufacture parity, violating the historical-operation contract.
- **Do not count source assertions or YAML creation as S2 PASS**: jobs never produced a test step or output.
- **Do not force canonical score DENY on every overcount**: source distinguishes selected coverage from pressure computation.
- **Do not make twin-fact deterministic sorting proof of uniqueness**: lexical tie order is a behavior, not authority.
- **Do not rerun ZAK-01's 58 AR resources or expand into original35**: not ZAK-02S jurisdiction.

## 8. Proof boundary / courts

**ENGINEERING:** executable implementation + frozen source identities committed; **S2 NOT_RUN**; no first non-test reader executed.  
**SCIENTIFIC:** sourcefree fixtures only; empirical/causal/native original35 validity NOT_PROVED.  
**AUTHORITY:** isolated branch/draft PR only; source/actor/scientific issuer, independent receiving and protected merge NOT_GRANTED.

**Terminal:** `ZAK02S_PARTIAL_WITH_EXACT_RUNTIME_BLOCKERS`. No full original nine-obligation MCR-C completion claim.
