# PYAT C1-03R — ASTRA OPTION-A GENERIC LIFECYCLE OWNER EXTENSION — R1

Status: `PASS_C1_03R_ASTRA_A_OWNER_EXTENSION__INDEPENDENT_REVIEW_REQUIRED`

Branch: `agent/opencode-pyat-hq151-c1-03r-astra-a-owner-extension-r1`
Commission tip: `9705742b3466e764d310f73b9bc3115073991e9f`
Base: `b346bd9f7f18b582173a47ca337d468816270c84`
Corrected implementation underneath: `1f270880f7e3353003ef6199d76d7ff28303301d`

## Court

| Suite | Tests |
|---|---|
| `test_pre553_authority_maintenance.py` | 42 |
| `test_pre553_replay_audit.py` | 54 |
| `test_pre553_analytical_replay_dependency.py` | 35 |
| `test_pre553_analytical_composition.py` | 13 |
| **total** | **144 passed, 0 failed, 0 errors, 0 skipped** |

Runtime 37.88 s, exit status 0. Python 3.12.14, pytest 9.1.1, darwin.
Baseline on the same four suites before this work: **109 passed**. 35 new courts.
**Only these four commissioned suites were executed — no broader sweep is claimed.**

## A. Generic owner-level noncurrent outcome

The accepted owner now owns the negative lifecycle meaning. One fixed typed
disposition, `NO_CURRENT_NO_LAWFUL_REPLACEMENT`, and nothing else:

| field | value |
|---|---|
| `old_ref` | exact |
| `disposition` | the single fixed type |
| `reason_code` | bounded, selector-free |
| `supporting_refs` | exact evidence/policy refs, **required non-empty** |
| `replacement_ref` | always `null` |

No C1-specific product vocabulary. No `DEFERRED` / `UNAVAILABLE` / `DELETED`
classes — Astra did not authorize them, and a court proves each is refused. A row
may not carry a replacement ref. The owner alone computes affected/unaffected,
validates the outcome set, and commits the release; the adapter supplies only a
recomposition path or an explicit grounded absence.

**Error law preserved exactly.** Missing callback, callback exception,
unchanged-ref return, absent cache/object bytes and arbitrary adapter refusal all
remain **errors**. Only an explicitly supplied, grounded row records absence. The
owner never converts an error into noncurrent.

## B. Receipt, serialization, compatibility

`AuthorityInvalidationReceipt` gained `noncurrent_dependents` alongside
`recompilation_pairs`, under an explicit new schema
`PRE553_AUTH40_SEMANTIC_AUTHORITY_INVALIDATION_NONCURRENT@1.0.0`.

**Historical hashes are preserved byte for byte.** A positive-only receipt
projects the *original* field set exactly, so no historical receipt is silently
reinterpreted. I verified this the hard way — by loading the pre-change module from
git and comparing:

```
pre-change  receipt ref : 26facb7634719e66049c39547cf7f85ed04869e80d5da120affb6cd17d31fa82
post-change receipt ref : 26facb7634719e66049c39547cf7f85ed04869e80d5da120affb6cd17d31fa82
as_dict byte-identical  : True
```

`from_dict(as_dict(x))` and checkpoint export/import reproduce the negative rows,
the release/event identities and current availability exactly. A **separate OS
process** rebuilds the owner from the exported checkpoint and reproduces both
outcome classes. Promotion and rollback share one outcome law, atomically: an
invalid outcome set commits no release, no current change, no partial state.

## C. Current-vs-historical visibility

`executor.dependent_lifecycle_status()` is the owner-owned mechanism;
`resolve_current_analytical_product()` is the analytical entry point. A dependent
the owner recorded noncurrent raises `ExplicitNoncurrentDependent` — stale
historical use cannot be served as current. Historical exact lookup still works,
and noncurrent does **not** withdraw the governing authority. No artifact
repository was built, and currentness never comes from object presence.

## D. Astra's sealed-successor defect — reproduced, then repaired

Astra was right, and the defect was worse than a wrong-version bug. The old filter
selected by the consumed `(authority_id, authority_version)` tuple, so in a
v1→v2 promotion it selected the **prior consumed ref** and passed it to
recomposition as the successor. Measured:

```
consumed prior (v1) hash : 4d565f1b40adb2bd
sealed successor    hash : 0a5ebefa7023e816
callback received after repair : 0a5ebefa7023e816   <- the sealed successor
old buggy filter would have passed : 4d565f1b40adb2bd <- the prior
```

Resolution is now by exact identity: find the consumed ref present in the owner's
changed set, then take the one *other* changed ref sharing that authority
identity — never by tuple position, never by version label. The successor must be
an authority the owner actually knows, which is what forbids future pre-binding.

## E. The fixture identity proof — the decoy

`build_model_authority_transition` exposed two non-interchangeable refs, and courts
used them interchangeably. The separately synthesized `revised_model` **shares the
consumed prior's `authority_content_hash`** (`4d565f1b`) and differs only in version
label and fingerprint, because `revised_model_authority_snapshot` copies the base
content hash. So the decoy was a v2-labelled ref carrying v1 content: choosing it
would recompute the product under the authority it already consumed, and no identity
change would ever be observable.

The fixture now exposes `unsealed_decoy_model_ref` and `sealed_successor_ref` as
distinct named values, **six existing court references** that passed the decoy as
the successor were corrected, and the consumer model rule is built from the exact
governed successor whose hash it provably commits to. Numerical geometry is
unchanged; identity moved (`feec9fc7...`) because the governing authority moved.
`AuthorityCandidate` hashing and identity semantics are untouched.

## F. Required mixed-outcome witness

In **one** governed source-free release: 4 registered dependents, 3 affected,
1 unaffected — one real lawful replacement, two explicit noncurrent rows
(`NO_LAWFUL_REPLACEMENT_SOURCE` and `REQUIRED_INPUT_NONCURRENT`), and an unaffected
sibling that stays current with identical identity. R and N disjoint, R ∪ N = A.
Also proven: missing cross-owner edge fails the independent closure witness even
with cached objects present; stale noncurrent cannot be served as current;
historical exact evidence stays retrievable; the downstream dependent gets **no**
replacement built from its noncurrent required input.

## G. Hostile matrix

23 hostiles, all proven, promotion **and** rollback exercised. Full matrix in
`05_HOSTILE_MATRIX.json`.

## AT18 intact

Replay grades are not collapsed: historical explanation, serialization replay,
fresh-process product replay and fresh empirical recomputation remain distinct, and
the runner-input/oracle separation is preserved. The fresh-process owner replay here
proves **serialization replay of lifecycle state** — explicitly *not* fresh
analytical recomputation, and a court asserts those grades differ.

## Changed files

- `rawlsing_next/pre553_authority_maintenance.py`
- `rawlsing_next/pre553_analytical_replay_dependency.py`
- `rawlsing_next/tests/test_pre553_authority_maintenance.py`
- `rawlsing_next/tests/test_pre553_analytical_replay_dependency.py`
- `rawlsing_next/tests/c1_at18_at19_fixture.py`
- `WORKER_RETURNS/PYAT-C1-03R-ASTRA-A-OWNER-EXTENSION-R1/**`

`pre553_replay_audit.py`, `pre553_analytical_composition.py`, C1-03A, N10E/AT17 and
C5/C7 terrain all verified unchanged. No existing-owner binding obstruction was
found, so no counterexample is returned.

## Non-claims

No raw survey access. No new survey/model/comparability authority. No
AuthorityCandidate identity change. No C1-specific sentinel product. No fabricated
replacement. No future authority pre-binding. No inferred dependency. No
adapter-owned lifecycle. No automatic error→noncurrent conversion. No C4/C7. No
live-occupancy, real-source, AT33 or multi-conditioner closure claim. Not merged,
not self-adopted.

## Terminal

`C1_03R_ASTRA_A_OWNER_EXTENSION_RETURNED__HQ_ADJUDICATION_REQUIRED`
