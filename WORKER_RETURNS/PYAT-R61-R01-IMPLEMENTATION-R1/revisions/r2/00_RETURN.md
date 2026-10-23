# R61-R01 R2 author repair return — typed identity, axes and native semantic binding

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. The author does not adopt this
result, does not qualify it, and does not touch the V1 or reviewer returns.
R03 remains NOT_STARTED.

## Exact identity

- Branch: `agent/opencode-pyat-r61-r01-generic-grammar-r1`
- R2 resume/startup: `fcf9fe9f8662c9e98801e670d0d4357072d8d453`
- R2 code commit: `d56e53301aaa0203e83fc1b60a0bcafb86b17892`
- HQ review driving this repair: `b310c5469bb628a583d6e106946cddd08025ddc1`
- Repair commission: `0ad99eadaf7aa2edd96e5a50f7b61f84c893ff70`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01`

## Plain-English function delivered

R01 no longer treats a symbolic operation as a label-and-count shell. Every
operation identity now carries the exact source/dataset/wave/edition/digest,
instrument/policy/grade, full measure/estimand/weight/design/uncertainty
identity, typed clocks and current selection. Condition values are typed
bool/int/string/null/absent values with semantic order; int `1`, string `"1"`,
explicit null, and absent are distinct identities.

Eligibility, execution and result are separate axes. A method-gated scientific
shape stays in the eligible/prohibited/held/unknown universe; native
unsupported/error/pending/completed execution states do not rewrite eligibility.
The prospective frontier remains value-independent and complete, while the
lowerer supplies a sound pre-execution `LoweringRecord` for R03 with lowering
version, exact predicate/query/DiscoveryAuthority refs, Batch-unit bindings,
typed refusal and evidence-grade ceiling.

Native receipt anti-join now binds exact candidate IDs, candidate hashes,
family, rule, winning predicate, query-role predicate refs, query refs, ordered
typed validation material and ancestry. A changed condition atom that preserves
the old rule id is refused by the same actual I05 consumer assertion. Target
cells are preserved as typed values or mapped through an explicit injective
catalog codec; a non-injective codec is a typed refusal, never `1`/`"1"`
collision.

## Defect disposition D1–D16

| Defect | R2 result | Proof |
|---|---|---|
| D1 bool/null domains | bool, int, string, explicit `None`, and `ABSENT` are accepted as typed domain values; floats/opaque values refuse | `test_typed_bool_int_string_null_and_absent_identity_and_cells`; reviewer D1 probes replay |
| D2 source identity | wave/edition/digest/dataset/instrument/source id bind operation identity | `test_operation_identity_binds_source_measure_clocks_and_selection`; reviewer D2 replay |
| D3 measure identity | estimand/weight/design/variance bind operation identity | same test; reviewer D3 replay |
| D4 clocks/currentness | exact clock and current-selection fields exist and bind identity | same test; reviewer D4 replay |
| D5 three axes | `ELIGIBILITY_STATES`, `EXECUTION_STATES`, `RESULT_STATES`; `DISPOSITIONS` is eligibility only; runtime/deferred no longer overwrite eligibility | `test_axes_and_lowering_record_contract_fields_are_complete`; reviewer D5 replay |
| D6 semantic receipt anti-join | exact expected candidate identity/query-role binding; changed condition fails actual I05 receipt anti-join | `test_native_mapping_uses_current_i05_contract_and_real_receipts`; reviewer D6 replay |
| D7 LoweringRecord | lowering version, DiscoveryAuthority ref, Batch units, grade ceiling, typed refusal, exact predicate/query/query-role/candidate keys | field/introspection test and native plan records; reviewer D7 replay |
| D8 typed native cells | typed target cells preserved by default; explicit injective codec allowed; non-injective codec refused | typed cell test; reviewer D8 replay |
| D9 topology pre-gate | frontier keeps the scientific operation; lowering asks catalog capability and can promote declared support | catalog topology promotion test |
| D10 forged direction | lowering revalidates inventory/policy/roles/risk/unit/form/topology/scope/administration and exact direction grant | forged direction refusal test |
| D11 empty risk sets | explicit policy: `UNKNOWN` (default) or `UNCONSTRAINED`; no invented source semantics | structured held/unknown risk test |
| D12 held reasons | `HeldRecord(occurrence_id, reason, authority_ref)`; free text is only an unstructured claim, not exclusion authority | structured held test |
| D13 recursion/baseline | explicit `recursion_depth`, `baseline_ref`, policy recursion relation; D bound remains separate from conditioner depth | axes test |
| D14 cold restore | deterministic cold recomputation is proved; serialized custody restore is NOT_REACHED and left to R04 | cold subprocess recomputation test |
| D15 valid empty grammar | zero supported rules declares `allow_empty_frontier=True`, with complete-empty E_pre root | valid empty native grammar test |
| D16 all-missing | vacuous local-tuple proof removed; current synthetic I03 gives a typed integrity refusal before I05, frontier conserved; positive all-missing native result remains NOT_REACHED | all-missing boundary test |

## Native consumer proof

The committed suite executes the real imported
`rawlsing_next.pre553_discovery_exact.execute_exact_bounded_discovery` against
synthetic TEST_ONLY C11/I03 objects. It then compares every actual
`DiscoveryResultReceipt` to precompiled expected candidate identities from the
current I05 owner compiler. Proven mutations:

1. Drop one supported I05 rule: anti-join reports the missing rule.
2. Change a condition atom predicate `q_beta=0 -> q_beta=1` while preserving
   the old rule id: exact candidate ID/query-role anti-join fails; the original
   receipt set restores `no_drop_ok=true`.
3. Forge a direction ref on an otherwise eligible operation: typed refusal.
4. Declare catalog MR support: lowering succeeds instead of a hardcoded
   frontier refusal.
5. Non-injective native cell codec: typed `NATIVE_CELL_CODEC_NOT_INJECTIVE`.

This remains mapping/native-boundary evidence only. It does not issue R03
workloads, U43 admission, Batch proof, original science or source permission.

## Tests, commands and evidence

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_grammar.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/revisions/r2/junit.xml -o addopts=''
```

- Exit `0`; `18 passed`, `0 failed/errors/skips`; final run `9.19s`.
- JUnit: `junit.xml`; log: `pytest.log`.
- Reviewer blocking-defect replay (D1–D8, excluding the superseded D9
  pre-classification assertion): `9 passed`, exit `0`, in
  `reviewer_d1_d8_replay.log`.
- Full old reviewer suite: 16 passed / 4 failed, and all four failures are
  explained rather than hidden: three probes assert the pre-repair behavior that
  R2 intentionally repairs (frontier topology pre-classification, forged
  direction accepted, D9 old disposition assertion), and the copied cold probe
  has a path-derived module import artifact; the committed cold recomputation
  test passes in-process and in a subprocess.
- Python `3.11.3`, pytest `9.0.2`, pyreadstat `1.3.2` verified.
- Imported current owner blobs:
  - `rawlsing_next/pre553_empirical_objects.py` = `a61365b994e5c3c50de0f598fcf40e90abf757b6`
  - `rawlsing_next/pre553_discovery_exact.py` = `905f24d114419dbdd93879ad2bee5b59dd2f23af`
  - `rawlsing_next/tests/test_pre553_discovery_exact.py` = `b53039aeb95e012993c5233a7575c1dad5a14929`
  - `rawlsing_next/tests/test_pre553_empirical_query.py` = `cc7d93db1f87d9c311170c229dbe3506937b404a`

## Capacity

- Tiny fixture: 22 operations, 8 eligible, 1 partition, `0.0195s`.
- Main synthetic fixture: 1,852 operations, 536 eligible, 29 partitions,
  `0.9929s`, peak RSS about 36 MB.
- No original data, credentials, external home reads, new provider/model/
  account/session/subagent, or unrelated branch was used.

## Exact changed paths and blobs

| Path | Blob |
|---|---|
| `rawlsing_next/universal_grammar/types.py` | `04b1d7608cdbf3bb79c849a8e2c529cab05be25b` |
| `rawlsing_next/universal_grammar/enumerate.py` | `2f038cae64ed6b7d1ecbde8e73b7897821218a94` |
| `rawlsing_next/universal_grammar/native_map.py` | `c8ef2cbc8bb18ed3ce09121b3a89d0fc457adcff` |
| `rawlsing_next/tests/test_universal_grammar.py` | `078122dc620a117da8e6f59fe6ab8053ecf97f0e` |

Report artifacts are SHA256-listed in `manifest.json`, which explicitly excludes
itself and claims no hash for any future file/commit. V1 reports and the
independent review tree are immutable and were not edited.

## Remaining boundary

- A fresh distinct reviewer must re-qualify this exact pushed candidate.
- R03 remains blocked until R01 is independently qualified and R02 accepted.
- Serialized cold restore, complete all-missing native result, R03 total native
  issuance/Batch proof, original U/E_pre, F6/F7/F8, N11/N12, production/CI and
  J52/W52 remain NOT_REACHED.
