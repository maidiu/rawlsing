# HQ264 G01 — repair status, call graph and source grain

**STOP: `HQ264_G01_RETURNED_FOR_HQ__NO_SELF_ADOPTION`**
**Disposition: `HOLD__HQ253_T01_XOR_FIXTURE_ARTIFACT_MISSING`**

**No code was modified.** The two permitted unadopted candidate files are unchanged from
their commissioned blobs (`e1c09957519f10b29ae2635f3277b4f3af0912c9` and
`f71c0ce87d4005acc6806cac9afe5bbbb76ad9bc`). A half-corrected candidate is not a
deliverable, so I did not ship one.

## Model declaration

The launch line reads "MODEL: GPT-6 Sol High". The actual configured model in this worker is
**Space Bunny Max** (`space-bunny-free`), not GPT-6 Sol High. Per the commission's own
instruction — "if different, declare actual model" — I declare the actual model and have
not relabelled.

## All six commissioned blobs verified exact at HEAD `8377eee256175d1ad1a4d02494150e8f95af61f1`

| blob | file | match |
|---|---|---|
| `604c8d591d4c` | C1 `pre553_analytical_composition.py` | yes |
| `62e5eced47b6` | F8 `source_backed_positioned_subject_possibility.py` | yes |
| `3e40caca29e8` | service applicability | yes |
| `848d2d0eedb0` | G2 `pre553_service_f8_source_scope_binding.py` | yes |
| `e1c09957519f` | unadopted ingress | yes |
| `f71c0ce87d40` | unadopted ingress test | yes |

## F1 — the decisive determination: real G2 is available, and it needs NO operative G0b

This is the finding that changes the blocker, and it is the most valuable thing in this
return.

The adopted G2 path is fully present and does **not** require an issued G0b permission:

- `resolve_service_source_applicability(request, candidate_class, authority_records)`
  returns a `CandidateClassApplicabilityReceipt`;
- `bind_service_applicability_to_f8_scope(...)` returns a `ServiceApplicabilityF8SourceScopeBinding`;
- `evaluate_bound_positioned_subject_possibility(binding, request, receipt, query, rule, evidence)`
  hands query/rule/**evidence UNCHANGED** to F8 — which is exactly what F1 demands.

Two facts establish that no G0b is needed:

1. **`AUTHORISED_AUTHORITY = "ADMISSIBLE_SET_ONLY__RANKING_AND_SELECTION_NOT_AUTHORIZED"`**
   (applicability module line 87). Applicability asserts only an **admissible set** and
   explicitly does **not** authorise ranking or selection. It is therefore not a model-use
   grant and does not need G0b.
2. `ApplicabilityAuthorityRecord` (line 401) takes a plain `admission_authority_ref`, which
   is constructible source-free as a TEST_ONLY_UNISSUED authority.

**Critically, the G2 binder is not a self-hash.** Its own docstring states that a
self-consistent hash or `__post_init__` shape check "proves nothing, because a caller can
fabricate a self-consistent binding", and `_authenticate_binding_against_authority`
**re-derives** the binding from the exact request, receipt and rule, returning the re-derived
object. That is precisely the property my HQ262 scope-hash substitute lacked and precisely
what F1 asks for.

**Therefore `G0B_OWNER_PERMISSION_REQUIRES_ADOPTION` is NOT the correct blocker**, and no
existing-owner edit is required for F1. The commission's STOP condition for F1 does not
fire.

## F2 — genuine blocker: the approved XOR fixture is not in the repository

F2 requires reusing the **approved HQ253 T01 four-respondent source-free XOR fixture** —
four synthetic respondents in one exact release, with two distinct C1 producer
queries/predicates/witnesses/conditioner grains giving q1 = q(C|A=1) at 1/2 and 1/2 with
**native joint denominator 2**, and q2 = q(C|A=1,B=0) at 0 and 1 with **native joint
denominator 1**, preserving same-original-respondent lineage.

**That fixture is not present in the tree.** Searching the repository finds no
`q(C|A=1)` fixture material and no approved four-respondent same-respondent XOR fixture
module. The only in-tree C1 source-free fixture I can actually execute is the accepted
AT07 fixture, which I used at HQ262 — and that fixture does **not** produce the specified
1/2,1/2 and 0,1 marginals with denominators 2 and 1.

The commission is explicit: *"If the fixture's exact identity/authority is unavailable,
identify the missing artifact and STOP rather than silently substitute."* The exact
four-respondent identities, their release, their risk-set and denominator membership, and
their C1 producer/predicate/witness identities would all have to be **invented** by me.
Inventing them would produce numbers that look like the commissioned figures while being
my own construction — precisely the silent substitution the commission forbids, and
precisely the "multiply marginals / swap in new F8-only evidence" failure it names.

## F3–F6 — not attempted, because the candidate they would repair is blocked

F3 (in-flight provenance/authority integrity), F5 (exact data-only request shape and
owner-scope custody) and F6 (real hostile court) are repairable. But all three are
repairs *to* the candidate, and shipping F3/F5/F6 without F1 and F2 would leave a
candidate that still substitutes a local scope hash for real G2 and still lacks the
commissioned XOR grain — i.e. a **half-corrected** candidate that looks repaired and is not.
I declined to ship that.

F4 (typed negative preservation, distinguishing applicability non-admission from an admitted
source with missing internal evidence) likewise cannot be honestly exercised without an
authenticated G2 receipt to classify against.

## Requested terrain or authorization

To proceed, HQ needs one of:

1. **the HQ253 T01 four-respondent XOR fixture** landed in-tree with its exact respondent,
   release, risk-set, denominator, C1 producer, predicate and witness identities — then F2
   becomes executable; or
2. **explicit authorization** to construct the four-respondent XOR fixture source-free
   myself, with HQ accepting that the identities are newly constructed rather than the
   approved HQ253 ones — which would materially change what F2 means.

No edit to C1, F8, applicability, G2, B5 or G3 is requested. F1 needs none.
