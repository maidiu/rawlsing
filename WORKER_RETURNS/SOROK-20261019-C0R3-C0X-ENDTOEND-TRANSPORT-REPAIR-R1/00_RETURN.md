# SOROK C0R3 — corrected two-owner N9/N10 transport and C10 read-only receiver

**DISPOSITION: `C0R3_SOURCEFREE_TWO_OWNER_TRANSPORT_REPAIR_PENDING_I2`.**

This is one coherent bounded sourcefree implementation return, not an independent acceptance, not a Pyat producer change, not an actor/CAN/ADP grant and not a C11 weld. The prior HQ adjudication at `401a14f54624f8a7f627154d2f2f57d7316a1fe0` correctly found the C0X transport RED and the vacuous C0R2 relocation test; this return closes the transport at the exact owner-object grain and supplies a new falsifiable test.

## 1. Exact identity and preflight

| Item | Value |
|---|---|
| Sealed startup | `0a0f8e99d9117a88a51d67b3b2b51f4f618cbaab` |
| Startup parent | `401a14f54624f8a7f627154d2f2f57d7316a1fe0` (sole changed path: this commission) |
| Branch | `agent/rabochii-sorok-20261019-c0r3-c0x-endtoend-transport-repair-r1` |
| C0R2 | `55d2daa4bab41c5ff4ffdc196c8d36d300c3d60f` |
| C0X | `b02deee1bac9393921845caa657841c40408eaf6` |
| Environment | local full Git checkout, CPython 3.11.3, pytest 9.1.1, Git 2.39.1, Darwin x86_64 |
| Authored write | only `WORKER_RETURNS/SOROK-20261019-C0R3-C0X-ENDTOEND-TRANSPORT-REPAIR-R1/` |

The remote branch was exactly the sealed commission tip before work; no prior return subtree and no running C0R3 worker were found. The 29-module native closure was staged directly from the actual local Git object store, not from an ambient Python install.

## 2. Inherited defect reproduced exactly

Against the unmodified repaired C0P facade (`855bb72f…`) and original C0X receiver (`8d80b5a…`):

- `ordered_steps[0].parent_receipt_ref` is a **Python function object** `TwoContractPort._possibility_receipt.<locals>.er0` (the source line is the `er0 if i == 0` branch), not an ExactRef value.
- `json.dumps(possibility_receipt)` → `TypeError: Object of type function is not JSON serializable`.
- C0X receiver transport → `NON_TRANSPORTABLE_OWNER_FIELD`, path `possibility_receipt.ordered_steps[0].parent_receipt_ref`, world fields 17 / possibility fields 20 but transport HOLD.
- Pre-publication clock → `TypeError: 'NoneType' object is not subscriptable` at the facade source-ref mapping, not a typed owner refusal.

Full receipt: `evidence/original_defect_reproduction.json`. This is a real inherited defect, not a test artifact.

## 3. Corrections in the isolated candidate

Corrected facade `candidate/upstream/c0p_two_contract_port.py` (`sha256 6e828fd8…`, parent blob `855bb72f…`, patch `candidate/patches/facade_c0r3.patch`):

1. The declared TEST_ONLY root parent ref is **materialized as the same exact value** `{kind:"OrderedConditionStep", id:"urn:test:c0p:step:root", hash:semantic_hash("root")}`. No new identity, no dummy hash, no change to the semantic lineage: the original `er0()` body is now actually returned.
2. A native `values_read` entry without a `source_ref` under an unavailable clock no longer causes a `TypeError`. The Sorok facade raises `TemporalSourceRefUnavailable("TEMPORAL_SOURCE_REF_UNAVAILABLE_AT_ASOF", consumer, fields)`, naming every unavailable structural/empirical field. This is a Sorok receiving-facade typed refusal, not a Pyat semantic repair.
3. The root/child parent refs remain exact dicts; child refs still hash the previous native empirical step (`new_binding.hash`).

Corrected C0X receiver `candidate/c0x_world_receiver.py` (`sha256 54fd2f35…`, parent blob `8d80b5a…`, patch `candidate/patches/receiver_c0r3.patch`):

- validates every `ordered_steps[i].parent_receipt_ref` as an exact `{kind,id,hash}` dict and refuses `PARENT_RECEIPT_REF_NOT_EXACT`;
- returns `UPSTREAM_TYPED_TEMPORAL_SOURCE_REFUSAL` with `upstream_refusal_code` and every field for the pre-publication case; no receipt, no positive, no fabricated reference;
- refuses a non-transportable owner object as `NON_TRANSPORTABLE_OWNER_FIELD`;
- records lossless JSON round-trip and the owner-receipts payload SHA-256 in the transport block;
- carries the versioned `C0R3_LOSSLESS_TRANSPORT_AND_TYPED_SOURCE_REFUSAL@1` revision while leaving the N9/N10 owner contracts and field counts unchanged.

No Pyat producer source, original C0R2/C0X test, native producer blob or accepted semantic registry was edited.

## 4. Complete two-owner transport

The corrected object carries both complete owner contracts through the actual nonparent/scenario consumers, the C0X receiver, JSON encode/decode and cold processes:

| Property | N9 `GENERIC_WORLD_SELECTION@1.0.0` | N10E_N10W `GENERIC_ORDERED_POSSIBILITY@1.0.0` |
|---|---:|---:|
| Fields | **17/17** | **20/20** |
| Selection/payloads | 5 / 5 | — |
| Ordered steps | — | 3 |
| Root parent ref | exact materialized dict | exact materialized dict |
| Child parent refs | — | previous `new_binding.hash`, exact chain |
| JSON serializable | **true** | **true** |
| Receiver transport | `LOSSLESS_TWO_CONTRACT_OBJECT` | `LOSSLESS_TWO_CONTRACT_OBJECT` |
| Owner receipt hash | `52e10a2f…` nonparent | `33251a74…` conception |
| Source identity | actual `product/nonparent.py` blob | actual `product/scenario.py` blob in lineage |

No field was dropped, sanitized, defaulted or replaced by a dummy. Both receipts retain `values_read`/`values_read_refs`, native unit, minority/unknown cells, generated-criteria echo (held empty), same-respondent joint (null), composition mode `REFUSED`, route probability null and selection weight null.

## 5. Clocks and temporal/source limits

Four clock roles are preserved: `observation_effective`, `publication_knowledge`, `actor_event`, `request_currentness`, mode `KNOWLEDGE_AS_OF`; `actor_event.caller_owns_time = true`. The actor clock is caller-owned; no historical entitlement is reconstructed and no archival known-at upper bound is invented. The pre-publication unavailable clock is a typed refusal, never a blank/unknown positive. A post-publication clock remains a supported receipt. Full details are asserted in the new court and recorded in `03_SOURCE_AND_CLOCK_LIMITS.json`.

## 6. Execution results

| Court | Tests | PASS | RED |
|---|---:|---:|---:|
| Original C0P author court | 49 | 49 | 0 |
| Original C0I frozen court on original facade | 50 | 47 | **3** |
| C0I frozen court on repaired author facade | 50 | 50 | 0 |
| C0I frozen court on corrected candidate | 50 | 50 | 0 |
| C0R2 author court on repaired facade | 23 | 23 | 0 |
| C0R2 author court on corrected candidate | 23 | 23 | 0 |
| Original C0X receiver court | 15 | 15 | 0 (inherited transport HOLD preserved) |
| K9/K10 sourcefree fixture port | 36 | 36 | 0 |
| **New C0R3 end-to-end court** | **13** | **13** | **0** |
| **Total selected test events** | **309** | **306** | **3 expected historical** |

Zero errors and zero skips. The three C0I REDs are the preserved original-facade runtime/two-contract/17-field failures:

- `test_port_runtime_binding_uses_actual_imported_native_module_tree`
- `test_facade_exposes_two_distinct_owner_contract_receipts_not_two_N9_clients`
- `test_facade_receipt_roundtrips_frozen_SC0_envelope_not_only_a_consumer_hash`

The original C0X 15/15 is green *because* it asserts the inherited transport HOLD; it is not evidence for the corrected transport. The corrected transport is proved by the new court and the 13/13 result.

## 7. Nonvacuous relocation/source-consumer proof

The inherited C0R2 test `test_r1_relocation_changes_no_consumer_value` still ends with literal `or True` at line 72. It is preserved byte-exact:

- commit `55d2daa4…`
- blob `89a0f119…`
- SHA-256 `f4c3968e…`
- line text recorded in `01_SOURCE_AND_IMPORT_CUSTODY.json`

It is not counted as proof. The new test `test_relocated_candidate_preserves_both_owner_sources_and_json_values`:

- imports a real relocated copy of the corrected facade from a temporary directory;
- verifies the relocated `module.__file__` and the actual native `RUNTIME`;
- verifies both owner producer source identities from the actual staged native bytes;
- verifies exact owner hashes, complete values and byte-identical JSON payloads;
- verifies deterministic repeat/no-change.

The shared proof gate ran three claim-specific severances. Every baseline passed; every target assertion failed through the intended edge, and the facade was restored to `6e828fd8…`:

| Claim | Positive node | Fault | Result |
|---|---|---|---|
| N9 selection drives receiver | new relocation/source-consumer test | `selection` → `[]` | `TARGET_ASSERTION_FAILED` |
| N10 ordered steps drive receiver | new relocation/source-consumer test | `ordered_steps` → `[]` | `TARGET_ASSERTION_FAILED` |
| Root parent is materialized | new exact-parent test | root parent → `None` | `TARGET_ASSERTION_FAILED` |

Receipt: `evidence/proof_witness_receipt.json`; gate log: `evidence/proof_witness.log`.

## 8. Adversarial consumer results

The new court exercises, on the actual candidate:

- provider swap → `PARTIAL`, training `BLOCKED_BY_MODELED_RULE`, civil `ELIGIBLE`;
- `training_access` revocation → `PARTIAL`, training `UNAVAILABLE_AUTHORITY_OR_CLOCK`, civil preserved;
- owner substitution → `OWNER_SUBSTITUTION`;
- invalid/missing parent → `PARENT_RECEIPT_REF_NOT_EXACT` at the exact ordered-step path;
- original callable parent ref → `TypeError` on JSON and `PARENT_RECEIPT_REF_NOT_EXACT` at the receiver; corrected ref is an exact dict and JSON transports;
- pre-publication source ref → typed `TEMPORAL_SOURCE_REF_UNAVAILABLE_AT_ASOF` with no positive;
- identical input twice → same owner hashes/JSON, no mutation (C0 has no psychological `NO_CHANGE` state; this is exact no-change/replay identity);
- two fresh child processes → equal complete receipts, transport and JSON SHA-256.

## 9. Source/import and historical custody

- **29/29 native modules, 859,712 bytes, every Git blob match**, closure resolves; see `01_SOURCE_AND_IMPORT_CUSTODY.json`.
- **11 actual imported modules** recorded with return-relative `module.__file__` and SHA-256 (product five, M4, M5, possibility provider, analytical composition, positioned-subject possibility, progressive candidate).
- Corrected facade `6e828fd8…`; corrected receiver `54fd2f35…`. Original repaired facade `fa08d5f5…`; original first-author facade `0409e327…`; original C0X receiver `a49dae62…`. No native runtime bytes are committed; the runtime is staged from pinned Git blobs and is gitignored.
- K9/K10 are the inherited **sourcefree fixture port** grade `SOURCEFREE_FIXTURE_PORT__NOT_OPERATIVE_N9`, not operative N9 installation.

## 10. Authority and scientific ceiling

1. This is a sourcefree TEST_ONLY two-owner receiving object. It is not real survey data, a Pyat native source grant, N9/N10W/OC05 installation, K9/K10 operative acceptance or a production C10 service.
2. The corrected parent ref preserves the declared synthetic root identity; it is not a new issuer/owner fact. The fixed facade `RULE_HASH` is not external rule authentication.
3. No route probability, selection weight, person, parent, family, conception, generated actor, psychological adoption, CAN008/CAN011 grant or source entitlement is created.
4. C0R2/C0X are author/earlier-worker candidates; this return is not independent I2 acceptance. No self-adoption. A separate independent I2 may be commissioned by HQ after this source is frozen.
5. C11 is **not welded**. Full C10 production readiness, real native source values, K9/K10 operative installation and actor/world-person semantics remain held for competent owners.

## 11. Terminal grid and remaining holds

`08_TERMINAL_C0_C10_GRID.json` records 22 stages and 7 explicit holds: independent I2 pending; C11 not welded; no operative N9/N10W/OC05; no Pyat producer edit; no old-schema migration/actor/person/conception/source inference; C0R2 vacuous test preserved and untrusted; inherited C0I/C0X historical REDs preserved.

## 12. Reproduce

```bash
cd WORKER_RETURNS/SOROK-20261019-C0R3-C0X-ENDTOEND-TRANSPORT-REPAIR-R1
PYTHONDONTWRITEBYTECODE=1 python3 runner/prepare_historical.py
PYTHONDONTWRITEBYTECODE=1 python3 runner/build_manifest.py
PYTHONDONTWRITEBYTECODE=1 python3 runner/run_all.py
python3 -B candidate/tools/proof_integrity_gate_r1.py witness \
  tests/test_c0r3_endtoend.py.proof.json --root "$PWD" \
  --receipt evidence/proof_witness_receipt.json
```

The runtime and historical courts are materialized from exact Git commits; they are not committed as ambient native bytes. The final remote SHA and direct remote readback are reported in the final chat return and in `publication_verification.json`.

**No self-acceptance, no Pyat producer edit, no actor or probability invention, no C11 physical weld.**
