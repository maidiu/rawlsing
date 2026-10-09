# HQ270 R02 — accepted SA `canonical_replay_only_order`: semantic disposition

**Return:** `WORKER_RETURNS/PYAT-HQ270-R02-G1-INDEPENDENT-QUALIFIED-RUNTIME-AND-SA-ORDER-COURT-R1/`
**Accepted owner under review (READ-ONLY):**
`rawlsing_next/pre553_service_source_applicability.py` @ blob
`3e40caca29e8c96ee1f412f919cfc7dba63f96c4` at candidate `46a95a8e`.
**No edit of any kind was made to this owner, or to any accepted owner.**

---

## 1. The question the commission poses

> Determine whether `canonical_replay_only_order` is **semantically derived** from other
> identity-bearing fields of the accepted SA owner's receipt, or is an **externally
> supplied opaque order**. If it is derived, test the resolver derivation and classify the
> owner's omission of the field from `replay_identity()` as either
> `INTENTIONAL_NONSEMANTIC_DERIVED` or `CONTRACT_DEFECT_REQUIRES_OWNER_NATIVE_COURT`,
> with exact evidence.

## 2. Verdict

**`INTENTIONAL_NONSEMANTIC_DERIVED`.**

The owner's omission of `canonical_replay_only_order` from `_material()` — and therefore
from `replay_identity()` — is **not** a contract defect. The order is a pure, deterministic
function of `receipt.decisions`, which the owner already includes in its identity
material. Admitting the order to `_material()` would be redundant with information the
identity already covers. The owner's own law declares the field's semantics to be
**zero**. One residual exists and is named in §6; it is an **advisory**, not a defect.

---

## 3. The accepted SA original law (SOURCE_STATIC, read at the pinned blob)

| Fact | Location |
|---|---|
| The receipt is a frozen dataclass with **12** fields; `canonical_replay_only_order` is field 11, defaulting to `()`. | `CandidateClassApplicabilityReceipt`, line ~570 |
| `_material()` returns **exactly 11** keys and **excludes** the order. | line 614 |
| `replay_identity() == semantic_hash(self._material())`. | line 629 |
| `as_dict()` publishes the order **and** its semantics. | line 641 |
| `ORDERING_SEMANTICS = "REPLAY_ONLY_DETERMINISTIC_SERIALIZATION__ZERO_RANKING_PRIORITY_PREFERENCE_WEIGHT_OR_FALLBACK_SEMANTICS"`. | line 215 |
| `as_dict()` also publishes `canonical_order_grants_no_rank_priority_preference_weight_or_fallback: True`. | line 643 |
| `_sorted_replay_only(refs) = tuple(sorted(canonical_json(r.as_dict()) for r in refs))`. | line 261 |
| The **only** production assignment of the field is inside the resolver, as the last statement before return. | line 804: `object.__setattr__(receipt, "canonical_replay_only_order", _sorted_replay_only(receipt.admissible_source_universe_refs()))` |
| `admissible_source_universe_refs()` = the `source_universe_ref` of every decision whose `applicability_decision == POSITIVE_DECISION` ("ADMITTED"). | line 597 |
| `decisions` **is** one of the 11 `_material()` keys. | line 614 |
| `AUTHORISED_AUTHORITY = "ADMISSIBLE_SET_ONLY__RANKING_AND_SELECTION_NOT_AUTHORIZED"`; `SOURCE_RANKING` and `SOURCE_PRIORITY` are in `FORBIDDEN_AUTHORIZED_PURPOSES`. | lines 87, 166–178 |
| No owner state field anywhere in the receipt, decision, candidate-class or request dataclasses is named for rank, priority, weight, preference or selection. | measured, see §4 |

**Consequence, stated as a function.** For every receipt the SA owner itself produces:

```
canonical_replay_only_order
  = tuple(sorted(canonical_json(ref) for ref in admissible_source_universe_refs()))
  = g(decisions)
  = g(material["decisions"])
```

i.e. the order is a function of a field the identity already covers. It is **derived**,
not externally supplied.

---

## 4. Measured discrimination (D2 court, 41/41 checks, exit 0)

The independent D2 court (`d2_hostile.py`, digest in doc 00) measured, against the
accepted owner itself:

**4.1 What the owner's identity covers.**

* `_material()` has exactly **11** keys: `receipt_id`, `service_request_set_identity`,
  `service_id`, `candidate_class_ref`, `candidate_class_coverage`, `outcome`,
  `no_applicable_source`, `candidate_class_binding`, `request_key`, `decisions`,
  `authorised_authority`.
* `canonical_replay_only_order` is **absent** from that set.
* `replay_identity()` equals `semantic_hash(_material())` exactly.

**4.2 11 / 11 material-field discrimination.** Each of the eleven material fields was
flipped in turn on a clone of a resolver-produced receipt; **every** flip changed
`replay_identity()`. So the accepted primitive discriminates every field the owner
declares to be identity-bearing, including `authorised_authority`, `receipt_id`,
`request_key`, `no_applicable_source` and `candidate_class_binding`.

**4.3 The order is invisible to `replay_identity()` and visible to `as_dict()`.**

| Mutation | `replay_identity()` | `as_dict()["canonical_replay_only_order"]` |
|---|---|---|
| resolver receipt, unchanged | `90b5401f…60fec0` | `[canonical json]` |
| **only** `canonical_replay_only_order` replaced | **`90b5401f…60fec0` (unchanged)** | **changed** |

**4.4 The order re-derives from `_material()` alone, across five different outcomes.**
For each receipt below, the order was recomputed using nothing but
`material["decisions"]`, and compared with the owner's own field:

| Receipt | Derived | Actual | Equal |
|---|---|---|---|
| `single_admitted` | 1 entry | 1 entry | yes |
| `single_negative` (`NO_ADMITTED_SOURCE_IN_CANDIDATE_CLASS`) | `()` | `()` | yes |
| `no_authority_record` | `()` | `()` | yes |
| `two_members_one_admitted` (one `MISSING_APPLICABILITY_AUTHORITY`, coverage `INCOMPLETE`) | 1 entry | 1 entry | yes |
| `two_members_both_admitted` | 2 **sorted** entries | 2 **sorted** entries | yes |

**4.5 The order never ranks.** Every entry is a `canonical_json` serialisation of an
`ExactRef`; the two-member case is byte-sorted, not preference-ordered; and the empty
order is produced whenever nothing is admitted. There is no candidate selection anywhere
in the derivation — the member set is the positively bounded candidate class, fixed by the
request, not chosen.

**4.6 Static provenance.**

* `object.__setattr__(receipt, "canonical_replay_only_order", …)` occurs **exactly once**
  in the repository, inside `resolve_service_source_applicability`.
* The selected ingress obtains its receipt **only** from
  `SA.resolve_service_source_applicability` (line 862); it never constructs a
  `CandidateClassApplicabilityReceipt` itself.
* `pre553_service_f8_source_scope_binding.py` contains **no** reference to
  `canonical_replay_only_order`: the accepted G2 binder and the bound-F8 evaluator never
  read the field.
* No dataclass field of the receipt, decision, candidate-class binding or request is
  named for rank/priority/weight/preference/selection (measured over `dataclasses.fields`).

---

## 5. The selected ingress separately binds the order (MEASURED)

The commission's stated design — "selected ingress separately binds it into origin
hash" — was tested directly, and it is what makes the omission safe rather than merely
tolerable.

An order-only tamper was injected at the applicability boundary (the resolver's return
value was replaced by a clone whose `canonical_replay_only_order` was the constant
`("urn:attacker:order",)`, with `_material()` untouched), and `serve()` was re-run:

| Quantity | Baseline | Order-tampered | Result |
|---|---|---|---|
| `g2_receipt_hash` (accepted owner `replay_identity()`) | `90b5401f…60fec0` | `90b5401f…60fec0` | **unchanged** (as the owner's law requires) |
| `f8_result_hash` (bound F8) | `ebde2f9a…83390` | `ebde2f9a…83390` | **unchanged** |
| `origin_receipt_hash` (ingress) | `516256bf…0bc52` | `71892f72…a70f0` | **changed** |
| full chain still ran | — | compose 1 / applicability 1 / binder ≥1 / evaluate 1 | yes |

The mechanism is at ingress lines 952–957 and 1007: `origin_material` carries
`g2_canonical_replay_only_order` alongside `g2_receipt_hash`, and
`origin_receipt_hash = semantic_hash(origin_material)`. The ingress therefore **adds**
the binding; it never redefines or re-derives it, and the accepted SA owner is untouched.

This same measurement doubles as the decisive F6 proof: with the observable F8 number and
the G2 replay identity both held fixed, the origin hash moves — so the origin hash is not
a function of, and cannot be reconstructed from, the observable F8 number.

---

## 6. Residual, named exactly (ADVISORY, not a defect)

**Residual name:** `NON_RESOLVER_CONSTRUCTION_PATH`.

**Statement.** `CandidateClassApplicabilityReceipt` is a public frozen dataclass whose
`canonical_replay_only_order` defaults to `()` and is **never** re-derived or validated in
`__post_init__` (which validates coverage, the authority label and the
no-applicable-source/coverage consistency only). A receipt constructed directly — rather
than by the resolver — can therefore carry any order, or none, while `replay_identity()`
is unchanged.

**Measured.** A receipt built by hand from a resolver receipt's fields, with the order
left at its default, was confirmed to share the resolver receipt's `replay_identity()`
while carrying `()` instead of the canonical one-entry order.

**Why this is not a `CONTRACT_DEFECT_REQUIRES_OWNER_NATIVE_COURT`:**

1. The field is declared `REPLAY_ONLY` with **zero** ranking, priority, preference,
   weight, tie-break or fallback semantics by the owner's own law, and `SOURCE_RANKING` /
   `SOURCE_PRIORITY` are explicitly forbidden purposes.
2. The order is a pure function of `receipt.decisions`, which the owner already includes
   in its identity material, so admitting it to `_material()` would be redundant rather
   than corrective.
3. The only production producer of this receipt is the resolver, and it always assigns
   the derived order (single assignment, verified).
4. The selected ingress neither re-derives nor trusts the field: it binds whatever value
   it received into `origin_receipt_hash`, so a non-derived value is at worst a
   **distinguishable** origin, never a silent one — the §5 measurement is exactly this.
5. The accepted G2 binder and the bound-F8 evaluator never read the field, so no
   admission, binding or evaluation decision can be steered by it.
6. No accepted production caller mints a receipt outside the resolver: the only
   `CandidateClassApplicabilityReceipt(...)` construction in the repository outside the
   SA module is inside a committed *test* that copies the real receipt's order verbatim.

**Disposition of the residual:** recorded as **ADVISORY** for the owner's attention. It
is not a required correction, and this return makes **no** proposal to edit the accepted
SA owner.

---

## 7. Non-collapse of the two identities, stated plainly

| Identity | What it covers | Blind to the order? |
|---|---|---|
| Accepted SA `replay_identity()` — bound into the ingress as `g2_receipt_hash` | the 11 `_material()` fields | **yes** |
| Ingress `origin_receipt_hash` | C1 identity, evidence projection, authority/provenance custody, denominator, the real G2 receipt hash and binding hash, **and** `g2_canonical_replay_only_order` | **no** |

Neither is redundant with the other, and neither is a substitute for the other. A caller
who holds only the observable F8 number holds neither.

---

## 8. Classification (the exact required output)

```
canonical_replay_only_order  : SEMANTICALLY DERIVED (from receipt.decisions ⊆ _material())
owner omission from replay   : INTENTIONAL_NONSEMANTIC_DERIVED
rejected classification      : CONTRACT_DEFECT_REQUIRES_OWNER_NATIVE_COURT
accepted SA owner edited     : NO
residual                     : NON_RESOLVER_CONSTRUCTION_PATH  → ADVISORY
```

Evidence per case: §3 (the owner's own law), §4 (measured 11/11 discrimination, order
invisible to `replay_identity()`, order re-derived from `_material()` alone across five
outcomes, single production assignment, G2/F8 never read it), §5 (the ingress separately
binds it into `origin_receipt_hash`, measured), §6 (the residual, stated and bounded).
