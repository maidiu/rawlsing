# SOROK C0X — dual-owner world receiver and K9/K10 campaign

**Verdict: BOUNDED C0/C10 READ-ONLY TWO-OWNER RECEIVER IMPLEMENTED AND
EXECUTED. C0R2 REMAINS AN AUTHOR CANDIDATE PENDING I2. FULL C10 TRANSPORT IS
HOLD ON ONE NON-TRANSPORTABLE OWNER FIELD. C11 IS NOT WELDED.**

**Role:** one bounded Sorok C0 semantic receiving-facade/consumer implementation
worker. Not Pyat owner, Pyat original-source issuer, F1–F8 estimator, N11/N12
issuer, independent acceptance reviewer, production C11 welder or HQ.

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Branch | `agent/rabochii-sorok-20261019-c0x-dual-owner-receiver-completion-r1` |
| Sealed startup | `6925ece4a2e5ccd647ac909904c2db40b55260a7` |
| Inherited C0R2 | `55d2daa4bab41c5ff4ffdc196c8d36d300c3d60f` |
| Repaired C0P facade | blob `855bb72f494d64083cee706e12f4f3d58c47dec3` |
| Native closure | 29/29 modules, 859,712 bytes, all blob/SHA/bytes match |
| C0X receiver | `SOROK_C0X_WORLD_RECEIVER@1`, version `1.0.0` |

## 1. Source and actual consumer custody — PASS

The 29-module E03/E04T native closure was staged from exact Git blobs with an
all-match ledger (`evidence/_c0p_runtime_ledger.json`,
`evidence/native29_verification.json`) and resolves. The C0X receiver stages the
same closure from Git on demand through `tools/c0p_stage_runtime.py`; no native
bytes are duplicated into the changed tree, and no ambient module is used. Actual
imported `__file__` paths are recorded in
`evidence/source_import_custody.json`.

The repaired C0P facade is vendored at exact blob `855bb72f…`, SHA-256
`fa08d5f5…`; `upstream/c0p_two_contract_port.py` is the actual upstream under
test, not a fixture.

## 2. Inherited + full K9/K10 execution

| Court | Result |
|---|---:|
| C0P original author court | **49 / 49 PASS** |
| C0I frozen court on **unrepaired** facade | **47 PASS / 3 RED** — R1 runtime portability, R2 two distinct contracts, R3 17-field SC0 envelope |
| C0I frozen court on repaired facade | **50 / 50 PASS** at author-candidate grain |
| C0R2 adversarial court | **23 / 23 PASS**, with one inherited vacuous assertion disclosed |
| K9 provider-swap | **8 / 8 PASS** |
| K10 structural conservation | **28 / 28 PASS** |
| K9+K10 full corpus | **36 / 36 PASS** |

The K9/K10 corpus is the inherited **sourcefree fixture port**, not the operative
native N9 installation. Its exact grade is
`SOURCEFREE_FIXTURE_PORT__NOT_OPERATIVE_N9`, recorded in
`evidence/k9k10_manifest.json`; it is not upgraded to native acceptance here.

The C0R2 test `test_r1_relocation_changes_no_consumer_value` ends with
`... or True` (line 72). Its green is not treated as proof. The C0I 3 REDs are
preserved in `evidence/c0i50_unrepaired.xml`.

## 3. Versioned C0X receiver — actual two-owner consumption

`c0x_world_receiver.py` consumes the **actual repaired C0P receipt object** and
exposes:

* the literal 17-field `GENERIC_WORLD_SELECTION@1.0.0` N9 receipt and the
  literal 20-field `GENERIC_ORDERED_POSSIBILITY@1.0.0` N10E/N10W receipt, with
  distinct contract versions and distinct owner outputs;
* native unit `SYNTHETIC_INDIVIDUAL_RESPONDENT`, native geography, release,
  risk set and field-time refs;
* source permission atoms limited to `TEST_ONLY_CONTEXT`; null `model_use_ref`;
* the consumer's actual `values_read` and receipt `values_read_refs`;
* four clock roles (`observation_effective`, `publication_knowledge`,
  `actor_event`, `request_currentness`) with `mode = KNOWLEDGE_AS_OF`;
* the nonparent structural/empirical material opportunity and the conception
  scenario output without person or parent generation;
* minority/unknown records and empirical cells without pruning or
  renormalization;
* `same_respondent_joint_ref = null`, `composition_mode = REFUSED`,
  `route_probability = null`, `selection_weight = null`.

Positive C0X court: **15 / 15 native**, and **15 / 15** in two cold replay seeds.
The actual receiver outputs are in `evidence/c0x_readings.json`.

### Positive and hostile states

| Demand / hostile | C0X result |
|---|---|
| Nonparent, actual N9+N10E | `SUPPORTED`; selection 5, payloads 5, native scope 1, route probability null |
| Conception proposals, actual N10E | `SUPPORTED`; two scenarios; `selection_weight = null`; no person/actor generation |
| Provider-state replacement (`structural_revision=True`) | `PARTIAL`; training `BLOCKED_BY_MODELED_RULE`; civil `ELIGIBLE`; not stale |
| Source revocation (`training_access`) | `PARTIAL`; training `UNAVAILABLE_AUTHORITY_OR_CLOCK`; civil preserved |
| Temporal pre-publication | `UNKNOWN`; no receipt fabricated; upstream refusal typed |
| Owner substitution (N9 receipt as N10, or reverse) | `OWNER_SUBSTITUTION` |
| Withheld owner contract | `MISSING_OWNER_CONTRACT` |
| Swapped / forged contract versions | `OWNER_CONTRACT_MISMATCH` |
| Reverse direction | `REVERSE_HELD` |
| Real-use request | `PROHIBITED_MODEL_USE` |
| Unknown demand | `NO_OWNER_CONSUMER_FOR_DEMAND` |

## 4. Dependency severance — mechanical witness

* Claim: `C0X_RECEIVER_DEPENDS_ON_ACTUAL_N9_SELECTED_WORLD_OUTPUT`
* Positive node:
  `tests/test_c0x_receiving_consumer.py::test_nonparent_receipt_reads_actual_upstream_selection`
* Fault: in the vendored actual facade, `"selection": selection,` →
  `"selection": [],`
* Baseline: **PASS**; fault probe: **`TARGET_ASSERTION_FAILED`**; grade:
  **`BOUNDED_MUTATION_DETECTED`**
* Restored facade blob: **`855bb72f…`**; post-restoration court green.

The shared proof-integrity checker is vendored at exact blob `461c8ac0…` under
`tools/`; the witness receipt is `evidence/proof_witness_receipt.json`.

## 5. Material findings / honest limits

1. **Non-transportable owner field (C10 transport HOLD).** In the repaired C0P
   `PossibilityReceipt`, every `ordered_steps[].parent_receipt_ref` is a
   **callable function**, not an `ExactRef`. The 20-field object is present and
   readable, but the literal envelope cannot round-trip through JSON transport.
   C0X records `transport.state = NON_TRANSPORTABLE_OWNER_FIELD`,
   `json_serializable = false`, and the exact paths. This is the smallest
   genuine owner edge; it is not silently normalized or fabricated.
2. **Temporal pre-publication upstream refusal.** The current facade raises a
   `TypeError` when a native `values_read` source ref is `None` under an
   unavailable clock. C0X catches and types that as `UNKNOWN` with no fabricated
   receipt, but the upstream owner should return a typed temporal refusal.
3. **Four clocks are graded, not complete.** All four roles are published and
   preserved; actor scene is caller-owned and actor/request values may coincide.
   No independent archival known-at upper bound or effective/discovered-at
   revocation timestamp is supplied by the adopted law.
4. **C0R2 is not self-accepted.** C0R2 is an author candidate pending I2. Its
   23-test court contains a vacuous `or True` assertion; that green is not proof.
5. **K9/K10 grade.** 36/36 on the sourcefree fixture port, not operative native
   N9; the native C0X receiver tests are the separate actual-N9/N10E reading.
6. **No C11 weld and no actor/person.** The campaign reaches a bounded read-only
   C0/C10 receiving seam; it does not issue a generated actor, parent,
   conception, route probability or route model.

## 6. C0/C10 terminal grid

See `evidence/terminal_matrix.json`. Summary:

* C0 source contract: **C0R2 author candidate pending I2**.
* Native 29/29, C0P 49/49, C0I 3 RED preserved and 50/50 repaired: **executed**.
* K9 8/8 and K10 28/28: **executed on the fixture port, not operative N9**.
* C0X two-owner receiving facade and actual demand consumers: **PASS** at
  object/read grain.
* Full literal C10 transport: **HOLD** on the callable parent receipt ref.
* C11 physical weld: **NOT RUN / NOT AUTHORIZED**.
* Positive actor input: **MISSING / HOLD**.
* Independent I2/C0 acceptance: **REQUIRED, NOT SELF-ACCEPTED**.

## 7. Authority and cost

No original source operation, raw SAV/DTA, original U/E_pre, model-use grant,
route probability, selection weight, actor/person generation, N11/N12, V3, C11
weld or production adoption is issued. Local warm Git/pytest execution; no paid
API call observed; incremental cash/quota **UNKNOWN**. Sanitized passport:
`environment_passport_delta.json`.

## 8. Return evidence

`00_RETURN.md` · `c0x_world_receiver.py` · `upstream/c0p_two_contract_port.py` ·
`tools/c0p_stage_runtime.py` · `tools/proof_integrity_gate_r1.py` ·
`tests/test_c0x_receiving_consumer.py` and `.proof.json` ·
`evidence/native29_verification.json` · `evidence/_c0p_runtime_ledger.json` ·
`evidence/k9k10_manifest.json` · `evidence/inherited_courts.json` ·
`evidence/c0x_readings.json` · `evidence/terminal_matrix.json` ·
`evidence/source_import_custody.json` · `evidence/proof_witness_receipt.json` ·
JUnit XMLs · `environment_passport_delta.json` · `PUBLICATION_RECEIPT.json`.

The final remote SHA is verified by direct `git ls-remote` readback and bound in
`PUBLICATION_RECEIPT.json`.
