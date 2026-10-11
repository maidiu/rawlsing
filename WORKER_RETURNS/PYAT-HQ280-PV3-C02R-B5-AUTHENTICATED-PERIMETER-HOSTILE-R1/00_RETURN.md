# PYAT HQ280 PV3 C02R — Independent C02 source-free authenticated B5 perimeter and bypass review

**TERMINAL:** `HQ280_PV3_C02R_B5_AUTHENTICATED_PERIMETER_HOSTILE_REVIEW_RETURNED__NONISSUING__GITHUB_PUSHED`

**Role:** Independent code/runtime hostile reviewer (not the C02 implementer, not an adopter).
**Repository:** `maidiu/rawlsing`
**Assigned branch:** `agent/reviewer-pyat-hq280-pv3-c02r-b5-authenticated-perimeter-hostile-r1`
**EXACT SEALED STARTUP (verified remote tip, not rebased):** `d4f50aff32e255935118b4a1d13a5e5a16c6f1e3`
**Inherited exact C02 candidate:** `agent/rabochii-pyat-hq280-pv3-c02-authenticated-b5-boundary-r1 @ 14ec16e2ef07716ab958aa7f514167821807d11c`
**Primary adversary:** F8F `aecc3273615ef158ae8428819d82d86d4cc64462`; F8E `2a4a90ec76d3400f98ba6fd3fd306f6ff977d042`
**Authority:** HQD-2026-10-10-280 · canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f` · semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390`

No operative G0b. No CURRENT adoption. No canonical mutation. No self-adoption. No ZIP relay.

---

## 0. Verdict in one paragraph

C02's **evidence is honest and faithfully reproducible**: all 37 candidate tests pass, all 525
adjacent accepted-owner tests pass, and C02's own F8F re-reproduction (4/5 caller-constructed
subjects reaching `PUBLISHED` and `CURRENT_SELECTED`) replays exactly. The candidate is **not**
overclaiming in its residual section, and its data-only request surface does genuinely eliminate
subject-forgery *at that surface*. **But the candidate does not close the F8F gap it is named for,
and it cannot be certified as an authenticated perimeter.** Independently reproduced here:

1. The **raw accepted B5 executor remains fully reachable and unmodified**, and the production
   module `rawlsing_next/pre553_learned_world_composition.py` is an **in-repo caller that invokes
   `stage_release`/`register_product`/`publish_product` directly**, importing no perimeter. A
   caller-side subject forgery still reaches `PUBLISHED` **and `CURRENT_SELECTED`** with the
   candidate installed.
2. `LearnedProductLifecycleExecutor.from_checkpoint` **rehydrates caller-authored state** and
   bypasses the perimeter entirely (`perimeter_consulted=False` confirmed at runtime); its
   integrity check is self-referential (`checkpoint_hash == semantic_hash(payload)`).
3. The perimeter's asserted trust anchor ("the accepted M2 owner already content-verifies its own
   releases") is **not a producer-authenticity edge**. `M2.register_producer_subject` /
   `constitute_release` are unauthenticated; a release minted end-to-end by the *caller* through
   the public M2 API is admitted and published by the perimeter as "producer-issued".
4. `EXPECTATION_KEY_TYPES` is a **module-level mutable dict**: the "fail-closed" exact-builtin-type
   gate can be weakened at runtime by an in-process caller.

Disposition: **bounded technical candidate — ACCEPTED as honest development-grade work; NOT
certified as an authenticated perimeter; F8F B5 trust hold remains OPEN.** No adoption, no G0b,
no CURRENT, no trust root.

---

## 1. What was actually executed (nothing here is a restatement)

Worktrees: reviewer branch at the sealed startup; a separate real Git worktree at the C02
candidate; a `git archive` export of the sealed tree for cross-checking blob identity.

| run | exact command | actual result |
|---|---|---|
| C02 candidate suite | `python3 -m pytest rawlsing_next/tests/test_pre553_authenticated_b5_ingress_candidate.py -q` @ `14ec16e2e` | **37 passed, 0 failed** (0.46s) |
| 13 adjacent accepted owners | `python3 -m pytest <13 files> -q` @ `14ec16e2e` | **525 passed, 0 failed** (34.79s) |
| C02's own F8F repro | `python3 repro/repro_f8f_k4_k5_boundary.py` @ `14ec16e2e` | **4/5 PUBLISHED, 4/5 CURRENT_SELECTED** — matches C02 exactly |
| reviewer hostile suite | `python3 repro/hostile_c02r.py <worktree>` | **38 cases, 0 exceptions, EXIT 0** |

Interpreter: Python 3.11.3, pytest 9.1.1 (matches C02's own `repro/interpreter.txt`).

Blob identity, verified independently by `git hash-object`:

| artifact | expected | observed |
|---|---|---|
| `rawlsing_next/pre553_authenticated_b5_ingress_candidate.py` | `5c30b9a0739989827f6028ef7858f3a4c046f4b8` | **match** |
| `rawlsing_next/tests/test_pre553_authenticated_b5_ingress_candidate.py` | `00a6c039c4d17ce5cbabbb8e238611c02280b0c3` | **match** |

`git diff d4f50aff… 14ec16e2e…` is exactly **one file**: the C02R commission document itself. The
sealed startup is the commission commit; the candidate adds only the two new files. No accepted
owner was modified by C02.

One honest correction to my own earlier pass: in a plain `git archive` export (no object store),
the adjacent suite reports **524 passed, 1 skipped** — `test_pre553_f8_receipt_permission_identity_hq254.py:345`
skips with *"no git object store available"*. In a real Git worktree it is **525 passed**. That is a
harness artifact, not a C02 defect, and C02's 525 claim is **confirmed**.

---

## 2. Findings, by severity

### F1 — CRITICAL: the raw accepted B5 executor is still directly reachable; the perimeter is not on the enforcement path

`LearnedProductLifecycleExecutor` is imported and invoked **directly** by a production module:

```
rawlsing_next/pre553_learned_world_composition.py:36    from ... import LearnedProductLifecycleExecutor
rawlsing_next/pre553_learned_world_composition.py:1203  lifecycle_executor.stage_release(b5_subject)
rawlsing_next/pre553_learned_world_composition.py:1206  lifecycle_executor.register_product(...)
rawlsing_next/pre553_learned_world_composition.py:1219  lifecycle_executor.publish_product(...)
```

`pre553_learned_world_composition.py` contains **no reference to the C02 module** (`grep` = 0 hits).
Therefore an accepted, in-repo, non-test B5 publication path exists that **cannot** consult the
perimeter. Independently reproduced (cases B1/B2/B3): a caller-built subject with forged
`replay_state`, forged `producer_permission_ceiling_ref`, forged receipts and a forged
`replay_root_ref` reaches:

- `publication = "PUBLISHED"`, events `[PRODUCT_REGISTERED, PRODUCT_PUBLISHED]` (B1, B2)
- **`CURRENT_SELECTED`** reachable on a forged subject (B3), `perimeter_consulted=false`

The stored forged ceiling is preserved verbatim
(`ProducerPermissionCeiling|urn:c02r:PRODUCTION_GRANT|0715fabb…`). This is F8F K4/K5, unclosed.

**Why this is not merely the declared R4.** C02's residual R4 frames in-process attackers as out of
scope while claiming the perimeter answers F8F's bounded data-only caller. That framing is
incomplete in one decisive respect: the perimeter is an **optional, uninstrumented, parallel**
surface. Until the accepted B5 owner, the composition path, or rehydration *cannot* publish without
the perimeter, "the ingress refuses forgeries" is a statement about one code path, not about the
system. The commission's own instruction — "do not assume matching schema tokens constitute
interoperability" — applies here as: **do not assume a correct perimeter constitutes an enforced
boundary.**

### F2 — CRITICAL: checkpoint rehydration publishes without the perimeter, with a self-referential hash

`LearnedProductLifecycleExecutor.from_checkpoint` (lifecycle module line ~2717) stages subjects
straight from `LearnedProductLifecycleSubject.from_dict(row)` and restores ledgers/events directly.
Its only integrity check is:

```python
supplied_hash = checkpoint.get("checkpoint_hash")
if supplied_hash != semantic_hash(payload):   # caller computes both sides
    raise LearnedProductLifecycleConflict(...)
```

Reproduced (H1, H2): a caller computes `checkpoint_hash` over its own payload, rehydration
succeeds (`n_subjects=1`), and the executor comes back with `publication="PUBLISHED"` **and a
`CURRENT_SELECTED` event present**, with `perimeter_consulted=false`. This is the simplest complete
bypass of the candidate: no subject construction, no B5 call sequence, no perimeter — a JSON dict
and one hash.

### F3 — HIGH: the "trust edge" is not a producer-authenticity edge; "producer-issued" is not established

C02 §"THE TRUST EDGE" asserts the accepted M2 owner "already content-verifies its own releases" and
is therefore the authority for `release_ref`, contract, anatomy, replay root and closures. Runtime
facts (D1/D2/H3):

- `M2.register_producer_subject(...)` and `M2.constitute_release(...)` take **only data** and perform
  **no credential, issuer, signature or authorization check** (module grep for
  `issuer|credential|signature|authoriz` = **0 lines**).
- A release minted entirely by the reviewer through the public M2 API is **published by the
  perimeter** (D1, `published=true`).
- M2 *does* bind a ref to its stored content: a ref with a wrong `content_hash` is refused
  (`RELEASE_UNAVAILABLE`, D2). That is **content-addressing / graph well-formedness**, not
  producer authenticity.
- No signature scheme, key registry, or credential verification exists anywhere in
  `rawlsing_next/*.py` (`verification_modules = 0`).

So the perimeter proves **"this subject is consistent with a well-formed release that exists in the
owner's M2 repository"**, and nothing about who issued it. C02 *declares* residual R1 (owner-held
AuthoritySnapshot) honestly, but its own summary language — "a B5-published subject *corresponds to*
material the M2 owner actually issued" — overstates the guarantee: M2 did not *issue* it, it
*stored* it. This is the exact conflation the commission warned against.

### F4 — MEDIUM: a module-level mutable dict lets a caller weaken the "fail-closed" type gate

`EXPECTATION_KEY_TYPES` is a plain module-level `dict` (candidate line 185). Reproduced (L1/L1a/L1b):
mutating `EXPECTATION_KEY_TYPES["release_key"] = bool` admits a wrong-typed expectation past the
construction-time type gate (`gate_bypassed=true`), directly contradicting the docstring claim that
"`type(v) is T` (never `isinstance`) so … no subclass slips through". The subsequent value comparison
still refused the mismatched expectation, so this is **gate weakening, not standalone forgery** — but
it is mutable enforcement state in a module whose stated design freezes everything that matters.

### Confirmed positives (no defect — recorded for symmetry and non-vacuity)

| behaviour | evidence |
|---|---|
| Data-only surface refuses caller subject / ceiling / currentness / subclass / string | G1–G5, all `REQUEST_SURFACE_VIOLATION`, all `b5_invoked=false` |
| Genuine perimeter publication works and is non-authorizing | A1: `published=true`, `authorizing=false`, `grant=g0b=g1_service=null`, `current_selection_performed=false` |
| Refusal precedes the first B5 call | every perimeter refusal carried `b5_invoked=false` |
| Exact revocation works (release / semantic / consumed) and ignores unrelated refs | E1–E4 |
| Replay grade mismatch refused | E5 `REPLAY_CLOSURE_REFUSED` |
| Expectation completeness/typing/exactness gate | J1–J4 refused; F2 cross-slot expectation refused on 6 fields |
| Deterministic re-publication across a fresh ingress | I1/I2 |

### Declaration check against C02's own claims

| C02 claim | reviewer result |
|---|---|
| 37 tests pass (7 positive / 30 hostile) | **confirmed** |
| 525 adjacent owner tests pass | **confirmed** (in a real Git worktree) |
| 6/6 mutants killed | **not independently re-run** — declared `NOT_REPRODUCED_BY_REVIEWER` |
| F8F boundary 4/5 PUBLISHED, 4/5 CURRENT_SELECTED | **confirmed** |
| R1 owner-held AuthoritySnapshot | **confirmed accurate** |
| R2 REPLAY_COMPLETE is an owner-held claim | **confirmed accurate** |
| R3 expectation authored from the construction it authenticates | **confirmed, and made executable** (C2: re-authoring after mutation admits an injected determinant edge) |
| R4 no arbitrary-Python/in-process defence | **confirmed, but materially understated** (see F1/F2: the bypass is reachable from repo production code and from a plain checkpoint dict, not only from "arbitrary Python") |

---

## 3. Is the candidate certifiable?

**No — not as an authenticated perimeter.** It is certifiable as: an honest, bounded,
non-authorizing **development candidate providing a data-only ingress facade** with genuine positive
and negative owner invocation behaviour and no accepted-owner mutation.

The gap between "the bounded data-only caller of F8F K4–K5 can no longer forge a subject" (true, at
this surface) and "the F8F B5 publication trust defect is closed" (false) is the whole finding.

## 4. Exact holds (nonissuing)

1. **PRODUCER-ISSUER HOLD (unchanged from F8F):** no accepted issuer/credential exists; M2
   registration is unauthenticated. Nothing here establishes that any release was producer-issued.
2. **ENFORCEMENT-SURFACE HOLD (new):** no accepted owner, production composition path, or
   rehydration path is required to pass the perimeter. F1 + F2 must be repaired or explicitly
   bounded before any "authenticated ingress" naming is honoured.
3. **REPLAY HOLD (R2, unchanged):** `REPLAY_COMPLETE` remains an owner-held claim.
4. **AUTHORITY HOLD (R1, unchanged):** semantic AuthoritySnapshot refs remain owner-held.
5. **No G0b / no operative CURRENT / no G1 selected service / no trust root.**

Successor requirement: an **honest successor contract** that either (a) makes the perimeter the
mandatory ingress for every publication against the accepted B5 owner, including rehydration, or
(b) is renamed and recorded as a *caller-side facade* that constrains only callers who choose it.
See `01_TRUST_ROOT_AND_REACHABLE_CALLERS.md` and `04_ADOPTION_AND_ISSUER_HOLDS.md`.

## 5. Return contents

- `01_TRUST_ROOT_AND_REACHABLE_CALLERS.md`
- `02_EXACT_RUNTIME_AND_INTEGRITY.json`
- `03_BYPASS_AND_NEGATIVE_OWNER_INVOCATIONS.json`
- `04_ADOPTION_AND_ISSUER_HOLDS.md`
- `05_MANIFEST.json`
- `repro/hostile_c02r.py` (reviewer-authored, 38 cases), `repro/c02_official_f8f_repro.py`,
  and the four captured logs.
