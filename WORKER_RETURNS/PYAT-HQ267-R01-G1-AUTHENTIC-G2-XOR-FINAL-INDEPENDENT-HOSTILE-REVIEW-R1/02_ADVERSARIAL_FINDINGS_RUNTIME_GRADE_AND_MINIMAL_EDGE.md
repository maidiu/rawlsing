# HQ267 R01 — adversarial findings, runtime grade and the minimal edge

**Object:** HQ266 G01 @ `3829fc4e63fc9fb0d802e8af237dfab2febc3d23`, ingress blob
`4ec0038d218a20cc92f114e28fd6c1de4ebd71f5`, test blob `321e3e03415d1b980156f0ed4355216ca1f2273c`.

> **INDEPENDENCE.** This session also authored the code under review. Findings are
> objective and re-runnable; they are **not** an independent review. See
> `03_DISPOSITION.json`.

Independent probe: `/tmp/hq267/independent_probe.py`, **38 PASS / 6 FAIL / 44 TOTAL**,
written by this review (not the author's court) and run against a fresh clone of the
frozen SHA.

---

# PART A — DEFECTS WARRANTING CORRECTION

## D1 — F3 authentication can be silently vacuous (`if k in expected`)

**Severity: primary. Defect class: the same vacuity F3 was raised to close.**
**Location:** `pre553_ee14_c1_owner_authenticated_ingress.py:595-596`

```python
mismatches = tuple(
    sorted(k for k, v in observed.items() if k in expected and expected[k] != v))
```

`expected = self._owner_identity.get(req.cell)`. The `if k in expected` guard means any
key **absent** from the owner-held expectation is **never compared**. There is no check
that `expected` is complete.

**Independently demonstrated (probe P1, all three negative results are FAILs):**

| probe | configuration | observed |
|---|---|---|
| P1a | full `_expected_identity` | serves correctly (control) |
| **P1b** | `owner_identity={"q1": {}, "q2": {}}` | **`serve()` ACCEPTED** — no refusal |
| **P1c** | `owner_identity={"q1": {"raw_denominator_support": 2}, "q2": {}}` | **`serve()` ACCEPTED** — producer/evidence/provenance/release keys never compared |
| **P1d** | does `_authenticate` validate completeness? | **NO** — no `set(expected)` / required-key assertion anywhere in the method |

So the depth of F3 authentication is entirely **owner-supply-driven**, and the ingress
never complains when the root of trust is empty or one-key. With
`owner_identity={"q1": {}}`, the only surviving check is the truthiness test at
`ingress.py:604-608` (authority/provenance refs non-empty) — a *different* non-empty
provenance list passes.

**Why this is the same class as the original F3.** HQ263's F3 was *"check non-empty
authority/provenance refs"* — vacuous because non-emptiness does not authenticate. The
correction replaced it with field-by-field comparison, but made that comparison
conditional on a value the ingress never validates, so it can still be vacuous. The
substantive custody hostile *is* closed in the correctly-configured case (see
"Confirmed correct" below) — the defect is that the guard has no floor.

**Threat-model note (be precise).** `owner_identity` is supplied at TRUSTED HARNESS
setup, not through the public data-only surface, so an *external* DATA-ONLY client
cannot trigger this. It is an **owner-setup completeness** defect and a false
completeness claim, not an external bypass. It is still a defect against F3.

### D1 — minimal exact correction

Fix `_authenticate` to refuse when the owner-held expectation lacks required keys:

```python
REQUIRED_OWNER_IDENTITY_KEYS = frozenset(observed)          # or an explicit literal
missing = tuple(sorted(REQUIRED_OWNER_IDENTITY_KEYS - set(expected)))
if missing:
    raise SelectedIngressAuthenticationError(
        "owner-held expected C1 identity for cell %r is incomplete; missing keys: %s"
        % (req.cell, ", ".join(missing)),
        mismatched_fields=missing)
```

and compare over `REQUIRED_OWNER_IDENTITY_KEYS` (equivalently, over the union), so a
missing key can never silently skip a comparison. Add two tests: empty per-cell
identity → refused; one-key identity → refused; both at `f8_calls == 0`.

---

## D2 — the receipt does not bind the full G2 receipt it claims to bind

**Severity: secondary. Defect class: the "truncated G2 material" the commission named.**
**Location:** `pre553_ee14_c1_owner_authenticated_ingress.py:690-702`

`_build_receipt` hand-rolls a 6-key hash:

```python
g2_receipt_hash = semantic_hash({
    "service_request_set_identity": ..., "outcome": ..., "coverage": ...,
    "candidate_class_ref": ..., "service_id": ..., "decisions": [...],
})
```

The accepted owner's receipt carries **12** material fields. Independent enumeration
(probe P4):

```
receipt fields : receipt_id, service_request_set_identity, service_id,
                 candidate_class_ref, candidate_class_coverage, decisions, outcome,
                 no_applicable_source, candidate_class_binding, request_key,
                 canonical_replay_only_order, authorised_authority
hashed         : 6
NOT hashed     : receipt_id, no_applicable_source, candidate_class_binding,
                 request_key, canonical_replay_only_order, authorised_authority
```

Because `origin_receipt_hash = semantic_hash(origin_material)` only embeds
`g2_receipt_hash`, those six fields are **not transitively bound** by the returned
receipt.

This contradicts the shipped dataclass docstring (`ingress.py:238`), which states the
receipt binds *"the EXACT G2 request/**receipt**/replay identities"* — `receipt_id` is
literally the receipt's own identity and is omitted.

**The accepted owner already provides the correct primitive.**
`CandidateClassApplicabilityReceipt.replay_identity()` = `semantic_hash(self._material())`
(`pre553_service_source_applicability.py:631`) covers every one of those fields including
`receipt_id` and `authorised_authority`.

**Severity calibration (honest):** most omitted fields are weakly discriminating —
`authorised_authority` is a `__post_init__`-validated constant
(`ADMISSIBLE_SET_ONLY__RANKING_AND_SELECTION_NOT_AUTHORIZED`), `receipt_id` is
content-derived from the request, and `candidate_class_binding`/`request_key` are derived
from material the receipt already binds via `service_request_set_identity` and
`g2_binding_request_id`. The defect is an **overstated completeness claim and needless
hand-rolling**, not an externally reachable bypass.

### D2 — minimal exact correction

Replace the hand-rolled subset with the accepted owner's own identity:

```python
"receipt.replay_identity_or_receipt_hash": receipt.replay_identity(),
```

(or `semantic_hash(receipt.as_dict())`), and assert in the court that mutating
`receipt_id` / `no_applicable_source` / `authorised_authority` changes
`origin_receipt_hash`.

---

# PART B — RESIDUAL RISKS (recorded, not verdict-triggering)

## R1 — `_owner_identity` is self-referential, not an independent custody root

**Commission asked this explicitly.** `court._expected_identity` (`hq262.py:148-179`) is
computed by **re-executing the same `_compose(source, qauth, registry)`** that `serve()`
later runs:

```python
composition, _cq = _compose(source=source, qauth=qauth, registry=registry,
                            conditions=plan.conditions, ...)
```

**Answer: it is computed from equally mutable owner setup, not pinned to a
source-authorized preimage.** It is an **owner-controlled source-free internal
development invariant**, not an independent cryptographic custody root.

Two consequences, both independently confirmed:

- `source_universe_key_owner` / `release_key_owner` in `expected` were captured from
  `source` at setup, and `observed[..._owner]` is read from the live `self._source` at
  authenticate time (`ingress.py:592-593`) — **the same object**. They cannot diverge
  unless the object mutates between the two reads (probe P3b).
- An adversary who can influence `source`/`qauth`/`registry` **before** setup moves both
  `expected` and `observed` together; authentication still passes.

**This is correctly scoped in the shipped text** — the docstring says *"NOT A TRUST
ROOT"* and *"TRUSTED HARNESS SETUP ONLY -- never remote, never data-only"*. The module
does not overclaim a custody root here. Recorded so HQ does not later read
`owner_identity` as one.

**Post-construction mutation is nevertheless refused** (probe P2e: replacing
`source["release_ref"]` after `__init__` raises), because `expected` was captured earlier
and the frozen snapshot then diverges from the mutated live object. That path behaves
correctly.

## R2 — `_deep_freeze` covers only two of the live owner objects

Probe P2d, measured by attempting a real mutation:

| live attribute | type | mutation succeeded |
|---|---|---|
| `_source` | `dict` | **YES** |
| `_cells` | `dict` | **YES** |
| `_registry` | `AuthorityRegistry` | n/a (non-dict) |
| `_applicability` | `ApplicabilityMaterial` (frozen dataclass) | n/a |
| `_qauth` | `AuthoritySnapshot` | n/a |
| `_owner_identity` | deeply frozen | **NO** (P2c PASS) |
| `owner_scope_material()` return | deeply frozen | **NO** (P2a/P2b PASS) |

So `_deep_freeze` (`ingress.py:290`) is applied at `__init__` only to `owner_identity`
(`ingress.py:364`) and inside `owner_scope_material()` only to a **snapshot** it builds
(`ingress.py:413`). `self._source` and `self._cells` remain live mutable plain dicts.

Demonstrated consequence: inserting a key into `live _cells` makes
`owner_scope_material()` raise `AttributeError: 'int' object has no attribute 'cell'` at
`ingress.py:419`.

**Bounded:** the trust model is a trusted owner harness, `CellPlan` objects themselves
are frozen dataclasses, and post-construction `_source` mutation *is* refused (P2e).
This is an F5 **completeness** gap relative to "deeply immutable owner material", not an
external exploit. Minimal hardening: `_deep_freeze`-the-source's containers (or store
`MappingProxyType`/copied tuples) for `_source` and `_cells` at `__init__`.

## R3 — threat model not enlarged

- The external DATA-ONLY boundary is respected: `SelectedRequest` admits only
  `cell` + `stratum_ids`, both exact builtins; there is no channel for evidence, a C1
  result, a hash, an authority, a registry, a callback or any object.
- The **same-process arbitrary-Python adversary remains UNPROVED**, exactly as the
  module docstring declares. Nothing in this review enlarges that claim.
- Built-in-type enforcement in-process is **not** remote schema or isolation proof; no
  remote boundary is claimed or established.
- R1/R2 are consequences of staying inside the declared trusted-owner model, not silent
  expansions of it.

---

# PART C — WHAT INDEPENDENTLY HOLDS ("confirmed correct")

The following were re-verified by this review and are **not** in dispute:

1. **Real call graph (F1).** `_applicability_scope` is absent (0 occurrences);
   `SA.resolve_service_source_applicability` (`:641`), `B.bind_service_applicability_to_f8_scope`
   (`:674`) and `B.evaluate_bound_positioned_subject_possibility` (`:465`) are all
   invoked; the raw low-level evaluator is absent from the module. Independent counters
   show applicability ≥ 1, binder ≥ 1, evaluate ≥ 1 on a single `serve()`; monkeypatching
   the binder to raise makes that exact refusal surface with F8 count 0, proving the
   chain is not bypassed.
2. **Unchanged evidence.** The very same C1 `possibility_slice_evidence_or_null` object
   is passed to bound F8; the parity gate requires `result_hash` and `material()` equality
   with the direct C1 result for both cells.
3. **Coherence (probe P8).** Release `REL-c1-at09-xor`, source universe, receipt
   identity, bound permission refs all match owner-held material; `requested_currentness_claim`
   is `None`; outcome `ADMISSIBLE_SOURCE_INDEXED_SET`; coverage `COMPLETE`.
4. **XOR (probe P5).** q1 denom 2 (1/2, 1/2), q2 denom 1 (0/1, 1/1); distinct producer
   predicates (`9bdff5e3` / `a8b05e75`), distinct composed identities (`e7a358b5` /
   `0556d4ab`), distinct denominator member refs; one shared release and one shared
   universe hash `318719f6…`; stratum swap refused.
5. **Custody false positive (probe P6).** The accepted chain produces an **identical** F8
   hash for genuine and provenance-forged evidence (`5f0fde451026c077…`) — the HQ253
   gap is real and reproducible — **and the ingress refuses it at `f8_calls = 0`** with
   `mismatched_fields = ('evidence_provenance_keys',)`. F3's core hostile is closed.
6. **Low-level F8 cannot mint a receipt (probe P7).** No overlap with any receipt field;
   lacks `origin_receipt_hash`, `authorizing`, `c1_identity_hash`, `g2_binding_hash`,
   `g2_receipt_hash`.
7. **F4 typing.** Native-state vocabulary enforced; out-of-vocabulary and the route
   family `UNDERPOWERED` refused rather than coerced; C1 negatives carry
   `SelectedIngressC1StateError` with `native_state` and never
   `SelectedIngressPermissionError`; `NO_ADMITTED_SOURCE` is a distinct G2 reason.
8. **F6 quality.** Non-vacuity control asserts `f8_calls == 1` on the positive path, so
   every `== 0` assertion means something. Zero `skip`/`xfail` markers in the court.
9. **Baseline preserved.** 14/14 original names, 22 collected, +53 new = 75.
10. **Reporting.** 75 / 199 / 80 / 354 all exit 0 in a fresh clone; 75+199+80 = 354
    exactly, so no double counting; the `99` in commit `bdc65ff89` is a prose typo and
    **199 was independently executed**, not accepted on the author's word.

---

# PART D — RUNTIME GRADE (separate axis, per commission)

| axis | grade |
|---|---|
| Did this review execute the frozen SHA itself? | **YES** |
| Method | fresh `git clone https://github.com/maidiu/rawlsing.git` → `git checkout 3829fc4e6…` |
| Checkout clean before run | **YES** (0 dirty) |
| Tracked files modified by the run | **0** (only `__pycache__/`) |
| Blobs unchanged after run | **YES** |
| Interpreter | CPython **3.11.3** (the approved version; not substituted) |
| pytest | **9.1.1** |
| Skips / xfails used to reach totals | **NONE** |
| Results | A 75 / B 199 / C 80 / D 354 / E ALL CHECKS PASSED — **all exit 0** |
| **Reused author's results** | **NO — independently re-executed** |
| Same host as author | **YES** |
| Same interpreter installation as author | **YES** |
| HQ-provisioned / HQ-verified runtime | **NO** — HQ recorded `QUALIFIED_INDEPENDENT_PYTHON_RUNTIME_NOT_VERIFIED_BY_HQ`, `worktree NOT_PROVISIONED_BY_HQ` |
| Governed Mac faked / fresh-checkout authority invented | **NO** |
| Raw survey / Library access | **NONE** |

**Runtime grade:** `INDEPENDENTLY_RE-EXECUTED_FRESH_CLONE_PINNED_SHA_CPY3113_PyTEST911__SAME_HOST_SAME_INTERPRETER_AS_AUTHOR__NOT_HQ_PROVISIONED`.

Interpretation, stated plainly: the numbers are **genuinely re-measured**, not accepted
from the author, and the code is therefore **not "runtime untested"**. But the runtime is
**not a separately HQ-qualified environment**, so it does not by itself satisfy a strict
"independently qualified runtime" requirement. If HQ requires strict runtime separation,
grade the runtime axis as `INDEPENDENT_QUALIFIED_RUNTIME_UNTESTED_HOLD` while keeping the
source-static verdict below — the two axes are reported separately as the commission
directs.

---

# PART E — MINIMAL EDGE AND THE FIRST MISSING CONNECTION TO T1

**First demonstrably missing connection to a selected source-free current/as-of T1,**
after source-free G1: **an actual selected T1 service join.** Nothing in this candidate
performs one. The control records `dependency_graph[T1_SELECTED_SOURCE_FREE].status =
G3_LOCAL_COURT_ADOPTED__G1_REAL_G2_XOR_CORRECTION_AUTHOR_COMMITTED_INDEPENDENT_FINAL_REVIEW_PENDING__G0B_UNISSUED`
and hold `g3 = …ACTUAL_SELECTED_T1_SERVICE_JOIN_NOT_PROVED`. That join requires, in order:

1. **EE14 G0b issuance** — still `UNISSUED` (hold `g0b`). This candidate grants no
   model-use or selected-service permission; `authorizing` is `False` throughout.
2. **A genuinely separate independent hostile review of the author's tests** — which
   this session cannot supply (see `03_DISPOSITION.json`).
3. **Correction of D1 and D2** (Part A).
4. **A HQ-provisioned, HQ-verified runtime** if strict runtime separation is required.
5. **A real selected-service join with a current/as-of claim** — `requested_currentness_claim`
   is `None` everywhere here by design, so no CURRENT/as-of result exists yet.

Only after those does a source-free current/as-of selected T1 become claimable. None of
`deployment`, `B5/G3 CURRENT join`, `T2 empirical field`, `native F7/AT07` or `V3` is
approached by this return.
