# WG0O — historical compatibility, source-artifact revocation, and capability classification

Role: independent WG0N reviewer continuation. Not WG0P6 author, not HQ, not a
source/semantic issuer. No inherited expectation file was edited.

## 1. Historical compatibility preserved (NOT retroactively green)

### 1.1 The two historical characterisation failures (reproduced UNMODIFIED)

`staged_candidate/court/tests/phase_b/test_additional_descriptor_binding_red.py`
is executed byte-identical and still gives **1 PASS / 2 FAILED**:

- `test_bound_descriptor_cannot_change_served_provenance[source_edition]`
- `test_bound_descriptor_cannot_change_served_provenance[native_item_ids]`

Both fail with `IdentityError: COMPLETE_BOUND_SOURCE_DESCRIPTOR_CHANGED` raised
from `_check_plan`. Their assertion shape calls `execute(altered)` and then
asserts `actual == expected`, i.e. it encodes "the forgery was SILENTLY IGNORED
and the unmutated provenance was served". Under WG0P6 the altered plan is
REFUSED before service, so the assertion is unreachable. The third test in the
same file (`test_copied_release_descriptor_refused_before_native_query`) has the
explicit early-refusal transport and passes.

Assessment (unchanged from the parent, restated on real bytes):

- The security property is STRONGER under WG0P6 — a forged bound descriptor is
  refused outright, before any native call, rather than silently ignored. My
  own fresh controls B1/B2/B3 and A1/A5/C3 confirm refusal independently with
  zero I03 calls on the refusing paths.
- The two tests are UNINFORMATIVE against a refusing implementation: "refused"
  and "forgery served unmutated" both fail them. Their only green path is the
  weaker behaviour.

**Recommendation to HQ (explicitly versioned, not acceptance by changing
assertions):** adopt a versioned safety-correct early-refusal transport for
exactly these two cases — the same shape the third test already uses: expect a
typed `IdentityError` at `_check_plan` with `new_I03_calls == 0`, and keep the
historical files byte-identical as compatibility evidence. I did not edit them
and I do not count them as green.

### 1.2 The five WG0N unconstructible controls (preserved as NOT green)

Executed in `inherited_wg0n_court/` with byte-identical copies of the parent
oracle, adapter, test and Phase A receipt. The parent's exact split reproduces:
**12 executed controls PASS / 5 not-constructible NOT GREEN / 0 RED**:

| Control | Observed | Why unconstructible (unchanged) |
|---|---|---|
| `C3_source_artifact_revocation` | not green | `FixtureOwner.revoke()` accepts only release tags |
| `D3_truncated_or_empty_snapshot` | not green | `ExactRef` refuses empty `content_hash` at construction (`Pre553IntegrityError`) |
| `E1_release_issuer_not_registrar` | not green | `IngestedRelease` has no `issuer_id` field (`TypeError` at `dataclasses.replace`) |
| `E2_unregistered_issuer` | not green | same |
| `E3_issuer_epoch_mismatch` | not green | `IngestedRelease` has no `issuer_epoch` field |

These are the parent's preregistration limits, not candidate defects, and they
are **not** rewritten, re-targeted or re-graded here. Fresh real-API
successors are separate NEW controls (A2 for epoch/currentness, C1 for
source-artifact revocation), never retroactive greens of E1–E3 or C3.

## 2. Source-artifact revocation (C3) expressibility — decided on the real owner surface

Fresh control `C1_source_artifact_revocation_not_release_tag` calls the REAL
owner interface with a source-artifact object id (distinct from a release tag):

```
p.fixture_owner.revoke(rel1.source_artifact_ref.object_id)
-> RevocationError('UNKNOWN_RELEASE_NO_REVOCATION')
```

Finding: **independent source-artifact revocation is NOT EXPRESSIBLE on this
owner surface.** `FixtureOwner.state()['grants']` is keyed by release tag only;
`revoke(tag)` refuses any non-tag key. A release and its source artifact can
therefore not be revoked independently: revoking `REL-A-W1` withdraws the
release grant, while there is no way to withdraw an artifact that other releases
or re-ingests may still reference.

Classification: **genuinely missing owner capability / source-owner design
decision.** Expressing it needs a new owner-surface capability (an
artifact-scoped revocation registry and a check at `_release_material`/
`assert_native_sources` time). A worker must not invent an issuer or patch the
accepted owner. The honest present ceiling is the typed
`RevocationError('UNKNOWN_RELEASE_NO_REVOCATION')` — an explicit refusal, never
a silent pass. WG0N's C3 stays not-green.

## 3. Missing independent issuer — typed HOLD

Fresh control `C2_missing_independent_issuer` (two flavors):
`REL-A-W1.qauth := None` and `REL-A-W1.authorities := ()`. Both are refused
typed: `IdentityError('RELEASE_VIEW_SOURCE_BINDING_UNRESOLVABLE')` (and
`SOURCE_C11_READSET_CHANGED` where the material is recomputed first).

**Answer to the commission question: yes — a missing independent issuer is a
typed HOLD/refusal on this adapter, never synthetic authority.** The
`source_issuer_grant` field on the plan is explicitly
`{'grant': 'GRANTED_FIXTURE', 'scope': 'TEST_ONLY_HINT_CANNOT_ISSUE_PERMISSION'}`
and `_check_plan` refuses any mutation of it
(`RevocationError('CALLER_GRANT_HINT_MUTATED; NOT_AUTHORITY')`).

## 4. Classification of the three REAL REDs (same-identity authority-body substitution)

| Control | Mutation (identity triple preserved) | Observed |
|---|---|---|
| `A2_stale_issuer_epoch_same_identity` | `effective_time_or_interval='2019-01-01'`, non-empty `supersession_refs` | SERVED 42 supported cells, 4 I03 calls |
| `A3_same_hash_foreign_signed_body` | foreign `interpretation_semantics_fingerprint`, foreign producer replay root, foreign `parent_authority_refs` | SERVED 42 supported cells, 4 I03 calls |
| `A4_foreign_governed_operations_same_hash` | `governed_operations=('WG0P3-OP-FOREIGN-ONLY',)` + foreign fingerprint | SERVED 42 supported cells, 4 I03 calls |

Mechanism (from real imported code):

1. `_release_material(rel)` binds only
   `authority_refs=[a.authority_ref.as_dict() for a in (*rel.authorities, rel.qauth)]`.
   `AuthorityRef` is the triple `(authority_id, authority_version,
   authority_content_hash)`. `authority_content_hash` is a CALLER-CLAIMED field
   (this fixture sets it to `_h('wg0p3-authority:<tag>:1.0.0')`, a label hash);
   `CanonicalSemanticObject` computes a separate semantic projection hash into
   `content_hash` and the claimed field is never checked against it.
2. Therefore a same-triple body substitution leaves `_release_material`
   unchanged: `assert_native_sources` and the `SOURCE_C11_READSET_CHANGED` check
   both pass — unlike A1/A5/C3, which change the triple and are refused.
3. `require_positive_authority` (native I01/I03 boundary) checks
   `decision_state`, `authority_kind`, `operation`, `object_family` and
   `scope_envelope` — but **not** `effective_time_or_interval` and **not**
   `supersession_refs` (A2 seam), and nothing binds the body to the triple
   (A3 seam).
4. For A4 the I03 query operation is inferred from the resolved snapshots'
   `governed_operations`, so a body that renames its governed operation is
   treated as governing whatever it now claims.

### Classification per the commission question

- **Executable at the adapter seam (no new issuer, no accepted-native-owner
  edits):** bind each authority snapshot's immutable object `content_hash`
  (already computed at construction by `CanonicalSemanticObject`) into
  `_release_material`'s `authority_refs` beside the ref triple; then any body
  substitution changes the owner-registered material and is refused by the
  EXISTING `assert_native_sources` / `SOURCE_C11_READSET_CHANGED` machinery.
  Additionally the adapter's `_check_plan`/`check_current` can (a) pin the
  plan-bound query operation instead of following live inference and (b) enforce
  an epoch/currentness bound over `effective_time_or_interval`/`supersession_refs`.
  These are adapter-level repairs inside the productive module; the accepted
  PRE553 native owners stay untouched.
- **Source-owner design decision (deeper layer):** whether
  `require_positive_authority` should itself interpret
  `effective_time_or_interval`/`supersession_refs` (the FAIL_CLOSED_STATES
  vocabulary already contains `SUPERSEDED_NOT_REPLAYABLE`, but no check emits
  it), and whether `authority_content_hash` is defined as a semantic content
  binding rather than a label claim. The native owner modules are accepted and
  must not be edited by a worker; this is an HQ/owner question.
- **Genuinely missing capability:** independent source-artifact revocation
  (section 2).

## 5. Reproduction

```bash
cd WORKER_RETURNS/PYAT-R28-WG0O-SOURCE-ISSUER-RESIDUAL-R1
export PYTHONPATH="$PWD/staged_candidate/court/bootstrap_p6:$PWD/repro"
WG0O_RUN=phase_b_seam python3 -m pytest tests/test_authority_seam_court.py -q -p no:cacheprovider
python3 -m pytest staged_candidate/court/tests/phase_b/test_additional_descriptor_binding_red.py -q -p no:cacheprovider
WG0M_DESCRIPTOR_ADAPTER=descriptor_adapter_v1 python3 -m pytest staged_candidate/court/tests/test_descriptor_delta_frozen.py -q -p no:cacheprovider
WG0L_PHASE_B_ADAPTER=phase_b_adapter_v1 python3 -m pytest staged_candidate/court/tests/test_precommitted_phase_b.py -q -p no:cacheprovider
WG0N_RUN=wg0o_regression WG0N_PRESERVED_ROOT="$PWD/../PYAT-R26-WG0M-ORIGINAL-FRONTIER-INDEPENDENT-DELTA-R1" \
  python3 -m pytest inherited_wg0n_court/tests/test_hostile_source_view_court.py -q -p no:cacheprovider
```

All JUnit, raw receipts and per-case stimuli are under `observations/`.
