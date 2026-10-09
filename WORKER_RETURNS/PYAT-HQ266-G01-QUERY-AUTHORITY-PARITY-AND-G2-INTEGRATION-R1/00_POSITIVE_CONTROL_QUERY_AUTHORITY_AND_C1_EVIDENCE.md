# HQ266 G01 — positive control: exact HQ253 query authority and real C1 evidence

**DISPOSITION:** `COMMITTED_CORRECTION` (see `03_DISPOSITION.json`)
**FINAL COMMITTED SHA:** `3829fc4e63fc9fb0d802e8af237dfab2febc3d23`
**Commission tip:** `dfab8607177e02872a2da6cfa65a6d97bed8bdda` (verified = remote HEAD at launch)
**Branch:** `agent/space-bunny-pyat-hq266-g01-query-authority-parity-repair-r1`
**Terminal:** `HQ266_G01_RETURNED_FOR_HQ__NO_SELF_ADOPTION`

---

## 0. Sealed HQ266 resolved through origin, not a branch-local pointer

Live authority read from `origin/integration/pre-main-reconciliation-r1`:

| field | value |
|---|---|
| checkpoint | `20261009-PYAT-HQ266-G01-XOR-VERIFIED-QUERY-AUTHORITY-G2-PARITY-REPAIR-R1` |
| decision | `HQD-2026-10-09-266` |
| `next_action` | `LAUNCH_HQ266_G01_GENUINE_C1_QUERY_AUTHORITY_POSITIVE_THEN_G2_REPAIR_TIP_dfab8607177e__SOURCE_CUSTODY_RESTORE_SEPARATE` |
| active worker row | my branch, `commission_tip = dfab8607177e…`, `observed_head_at_checkpoint = dfab8607177e…`, `status = ISSUED_NEEDS_HUMAN_LAUNCH` |
| grain | `MATCH_EXACT_HQ253_QUERY_AUTHORITY_C1_POSITIVE_CONTROL_FIRST_THEN_REPAIR_ONLY_TWO_G01_FILES_REAL_G2_AND_NEGATIVES` |
| hold `g1` | `…AUTHORITY_QUERY_SNAPSHOT_NOT_HQ253_GRAMMAR_AUTHORITY__HQ266_PARITY_REPAIR_ISSUED_UNLAUNCHED` |
| hold `g0b` | `EE14_OPERATIVE_MODEL_USE_AND_SELECTED_SERVICE_GRANT_UNISSUED` — untouched by this lane |

The active row matched my branch and commission tip exactly, and direct origin HEAD matched
the commission tip, so no STOP condition triggered.

## 1. The exact historical witness, read by pinned blob — never reconstructed

| artefact | pinned value | verified |
|---|---|---|
| HQ253 T01 return commit | `e609be4f68c51182c5acb3a99c671949f1b71d34` | present, subject `HQ253: T0 rich C1 to authenticated F8 existing-API discriminator` |
| witness test blob | `17300a405d78820cd663618918e64bb0323f532e` | **`git rev-parse` of that path at that commit equals the pinned blob exactly** |
| original XOR fixture blob | `0393cc8c17a313b7944b2a5287d0406d6cbe3849` | `git hash-object` of the in-tree file equals it exactly |

The witness test is **not** in canonical control; it was retrieved by pinned Git blob as a
read-only reference, exactly as the commission directs. It was never re-derived from prose.

The witness's construction, read literally from that blob:

```python
from rawlsing_next.tests.test_pre553_empirical_query import _query_authority, _registry

source  = fx.xor_fixture()
qauth   = _query_authority("c1-at09-xor")
registry = _registry(source, qauth)

composition, consumer_query, witness, producer_query, predicate = \
    fx.direct_condition_composition(
        source=source, qauth=qauth, registry=registry,
        conditions=..., target_question="C", tag="hq253-qA" / "hq253-qAB")
```

`_query_snapshot()` appears **nowhere** in this lane's positive control, in the ingress, or
in the court.

## 2. STEP A — the complete positive control, run BEFORE any edit

Standalone script `/tmp/hq266/step_a_positive_control.py`, executed against the pristine
commission tip before either authorized file was touched.

**Result: `STEP A RESULT: ALL CHECKS PASSED`, exit 0, 34 PASS / 0 FAIL.**

Re-run unchanged at the final committed SHA: **exit 0, ALL CHECKS PASSED.**

### 2.1 The true query authority ref/key

```
type            : AuthoritySnapshot
authority_kind  : PREDICATE_GRAMMAR
authority_ref   : AuthorityRef(authority_id='I03-AUTH-c1-at09-xor',
                               authority_version='1.0.0',
                               authority_content_hash='7fbd015d4d45c533fdb2b9e48082544f284167a7dff5713e897a112b3bc94257')
object_id       : urn:rawlsing:pre553:AuthoritySnapshot:sha256:8082957627c5f2a53c51d92dabcdd1b87f75c5975bfc117c2fbd97179941fc69
typed_state     : ALLOW
governed_operations    : ('I03-OP-c1-at09-xor',)
governed_object_families : (EmpiricalFact@1.0.0, EmpiricalPredicate@1.0.0, EmpiricalQuerySpec@1.0.0)
```

The source of `_query_authority`, read at execution time:

```python
def _query_authority(tag: str = "query") -> AuthoritySnapshot:
    return _auth(
        tag,
        "PREDICATE_GRAMMAR",
        families=("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"),
    )
```

### 2.2 Non-null original C1 evidence for both q1 and q2

| | q1 | q2 |
|---|---|---|
| `analytical_state` | `SUPPORTED` | `SUPPORTED` |
| `producer_fact_state` | `SUPPORTED` | `SUPPORTED` |
| `possibility_slice_evidence_or_null` | **NON-NULL** | **NON-NULL** |
| `consumer_result_or_null` | **NON-NULL** (`EXACT_SUPPORTED`) | **NON-NULL** (`EXACT_SUPPORTED`) |
| `retained_conditioner_ids` | `('c0',)` | `('c0', 'c1')` |
| producer predicate ref | `sha256:9bdff5e3d9b93b4…` | `sha256:a8b05e75b088822…` (distinct) |
| composed identity | `e7a358b587bf6c0d…` | `0556d4abe02e650e…` (distinct) |

### 2.3 The exact original XOR figures, preserved byte-for-byte

```
q1 cells: {'0': 1, '1': 1}  denominator = 2     -> C=0 1/2, C=1 1/2
q2 cells: {'0': 0, '1': 1}  denominator = 1     -> C=0 0/1, C=1 1/1
```

Frozen assertions all passed: `q1 C=0 == 1/2`, `q1 C=1 == 1/2`, `q2 C=0 == 0/1`,
`q2 C=1 == 1/1`, and `q1 and q2 producer identity distinct`. No value was derived from a
candidate run — the expectations are the fixture's own `XOR_ORACLE` literal.

### 2.4 Authentic source-applicability receipt

```
receipt.outcome               : ADMISSIBLE_SOURCE_INDEXED_SET   (= SA.OUTCOME_ADMISSIBLE_SET)
receipt.candidate_class_cover : COMPLETE
receipt.service_request_set_identity : d960858b45a30525cf065ec8877331a9fba66e849e417595abd00ac6108a2270
any POSITIVE_DECISION         : True
source universe admitted      : True
```

Built by the real `SA.resolve_service_source_applicability` with a real
`CandidateClassBinding`, a real `ServiceApplicabilityRequest.build(...)` and a real
`ApplicabilityAuthorityRecord(universe, "ADMITTED", authority)`. No scope dictionary, no
hash stand-in.

### 2.5 Adopted G2 binding and bound F8 evaluation with full parity

For **both** q1 and q2:

| assertion | q1 | q2 |
|---|---|---|
| `out.result_state` | `EXACT_SUPPORTED` | `EXACT_SUPPORTED` |
| `out.exact_disposition` | `SUPPORTED` | `SUPPORTED` |
| `out.exact_reason` | `EXACT_POSITIONED_STRATUM_SUPPORTED` | `EXACT_POSITIONED_STRATUM_SUPPORTED` |
| `out.material() == direct.material()` | **True** | **True** |
| `out.result_hash == direct.result_hash` | **True** | **True** |
| `out.exact_evidence_ref == evidence.evidence_ref` | **True** | **True** |
| `request.requested_currentness_claim` | `None` | `None` |
| `binding_mode` | `SINGLE_SOURCE_VALIDATION` | `SINGLE_SOURCE_VALIDATION` |

The exercised path is the historical first-edge path exactly:
`SA.resolve_service_source_applicability` → `B.bind_service_applicability_to_f8_scope`
→ `B.evaluate_bound_positioned_subject_possibility`.

**Because STEP A passed completely, STEP B was authorised and performed.** No STOP was
required: no typed failure occurred, and no speculative rewrite was attempted.

## 3. Reproducible commands and exits (final committed SHA)

Runtime: macOS, **CPython 3.11.3**, **pytest 9.1.1**, stdlib only. No `pyarrow`, `pandas`,
`pyreadstat` or `numpy`. Worktree clean (0 non-pycache dirty entries) at run time.

```bash
# STEP A positive control
PYTHONPATH=. /private/tmp/hq210venv/bin/python /tmp/hq266/step_a_positive_control.py
#   -> exit 0, ALL CHECKS PASSED (34 PASS / 0 FAIL)

# A) new G01 court
PYTHONPATH=. /private/tmp/hq210venv/bin/python -m pytest \
  rawlsing_next/tests/test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py \
  -q -p no:cacheprovider
#   -> 75 passed, exit 0

# B) four accepted G2 / applicability baseline courts
PYTHONPATH=. /private/tmp/hq210venv/bin/python -m pytest \
  rawlsing_next/tests/test_pre553_service_f8_source_scope_binding_court.py \
  rawlsing_next/tests/test_pre553_service_f8_binding_authentication_court.py \
  rawlsing_next/tests/test_pre553_service_f8_source_scope_binding_repair_court.py \
  rawlsing_next/tests/test_pre553_service_source_applicability_court.py \
  -q -p no:cacheprovider
#   -> 199 passed, exit 0

# C) C1 + query-authority + higher-order regression
PYTHONPATH=. /private/tmp/hq210venv/bin/python -m pytest \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_analytical_composition_higher_order.py \
  -q -p no:cacheprovider
#   -> 80 passed, exit 0

# D) COMBINED
#   -> 354 passed, exit 0
```

See `01_CLEAN_COMMITTED_RUN_AND_HOSTILES.json` for the machine-readable record.
