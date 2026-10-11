# 01 — Trust root, reachable caller graph, and the actual enforcement surface

**Method:** independent `grep` over the candidate worktree at `14ec16e2e`, plus 38 executed
runtime cases (§`03_BYPASS_AND_NEGATIVE_OWNER_INVOCATIONS.json`). No claim here rests on a docstring.

## 1. The accepted owners (unmodified by C02)

| module | blob | role | C02 change |
|---|---|---|---|
| `rawlsing_next/pre553_learned_product_lifecycle.py` (B5) | `a11c9eb73abab9be118ef4f0b6e325e676059f27` | lifecycle state owner; well-formedness gate over an opaque subject | none |
| `rawlsing_next/pre553_learned_product_release.py` (M2) | `f76c390665f06ef126968ccf1a6b2d816f43ae92` | ReleaseCore/closure owner; content-addressed resolution | none |
| `rawlsing_next/pre553_empirical_objects.py` | `a61365b994e5c3c50de0f598fcf40e90abf757b6` | `ExactRef`/`AuthorityRef`/`semantic_hash` | none |

B5's own module contract states it "deliberately does not own producer semantics, M2 release-core
semantics, AuthoritySnapshot maintenance, consumer permission…". C02 correctly declines to mutate
it. The consequence is the whole finding: **a correct owner-internal well-formedness gate is not a
producer-authenticity gate, and adding a perimeter beside it does not change what the owner does.**

## 2. Complete reachable-caller audit for B5 publication

`grep -rnE "\.(stage_release|publish_product|register_product)\(" rawlsing_next/ --include=*.py`
excluding tests yields exactly four call sites:

| # | call site | gated by C02 perimeter? | reachability |
|---|---|---|---|
| 1 | `pre553_learned_product_lifecycle.py:1499` (`stage_protocol` → `stage_release`) | **no** | public accepted-owner method; any protocol object accepted |
| 2 | `pre553_learned_product_lifecycle.py:2717` (`stage_release` inside `from_checkpoint`) | **no** | public classmethod; caller supplies the checkpoint mapping |
| 3 | `pre553_learned_world_composition.py:1203/1206/1219` | **no** | production composition module; imports `LearnedProductLifecycleExecutor` at line 36 and **never imports the C02 module** |
| 4 | `pre553_authenticated_b5_ingress_candidate.py:900/901/906` | **yes (it is the perimeter)** | new candidate module |

Therefore: **three of the four reachable B5 publication paths bypass the perimeter, including one
non-test production module.** The perimeter's public surface `publish(PublicationRequest)` is the
*only* gated entry, and nothing in the repository is required to use it.

### 2.1 The production composition path in detail

`compose_learned_world(contract, *, m2_repository, lifecycle_executor, …)`:

- builds the B5 subject as `LearnedProductLifecycleSubject.from_protocol(protocol)` (line 1201) from
  M2 artifacts it produced itself;
- stages/registers/publishes **only if** `contract.lifecycle_actions` contains
  `REGISTER`/`PUBLISH`/`SELECT_CURRENT` (lines 1201–1224).

`LearnedWorldProductContractBinding` is a plain caller-supplied dataclass. Two of its fields flow
straight into the B5 subject with no validation beyond exactness:

```python
# pre553_learned_world_composition.py, adapt_m2_release_to_b5 (line ~936)
producer_permission_ceiling_ref=_exact(
    contract.producer_permission_ceiling_ref, "producer_permission_ceiling_ref"),
...
selection_scope_ref=_exact(contract.selection_scope_ref, "selection_scope_ref"),
producer_owner_ref=_exact(contract.producer_owner_ref, "producer_owner_ref"),
```

So the caller-declared **permission ceiling**, product family, producer owner and selection scope
reach B5 publication through the composition path — the exact F8F K5 class — with no perimeter
consulted. This is the same defect C02's H04 test refuses *at the perimeter*, still live one module
over.

## 3. What C02's "trust root" actually is

C02 names the accepted M2 owner as the trust edge. Runtime probe results:

```
D1  caller-minted M2 release published by the perimeter        published=true
D2  ref with wrong content_hash refused by M2                  RELEASE_UNAVAILABLE
H3  modules performing signature/credential verification       0
H3  M2 lines mentioning issuer|credential|signature|authoriz   0
```

Interpretation, stated precisely:

- M2 provides **content-addressing and graph well-formedness**: a `release_ref` resolves only if the
  stored object's own hash projection matches, and closure refs must be exactly the ones the release
  names. This is real and useful.
- M2 does **not** provide **issuance**: `register_producer_subject`/`constitute_release` accept plain
  data and check no identity, no credential, no authority.
- The perimeter adds **owner-custody consistency**: custody refs must match a closed 21-key
  expectation. Its own R3 admits the expectation is authored from the construction it authenticates;
  probe C2 makes that executable — after an injected determinant edge is added to the owner's M2
  closure, re-authoring the expectation admits it (`injected_edge_present=true`).

Net trust root: **the owner process's own custody state plus whatever is in its M2 repository.**
There is no cryptographic root and no issuer. C02 says so in R1/R4; the summary language
("material the M2 owner actually issued", "THE TRUST EDGE IS THE ACCEPTED M2 OWNER") is stronger
than what the runtime supports.

## 4. In-process enforcement state — audit of mutability

| state | mutability | runtime evidence |
|---|---|---|
| `AuthenticatedB5Ingress._custody` | `MappingProxyType` | L2: `pop` → `AttributeError`; no unmount surface |
| `AuthenticatedB5Ingress._expected` | `MappingProxyType` over deep-frozen values | constructor |
| `EXPECTATION_KEY_TYPES` | **plain module-level `dict`** | L1/L1b: weakening it admits a wrong-typed expectation past the type gate |
| `M2Repository` + `ExactRef`/`AuthorityRef` inside custody | **shared, unfrozen owner objects** | C3; declared by C02 residual |

C02's "FROZEN (deeply, at every level)" claim is therefore **not exactly true**: one module-level
dict used by the fail-closed type gate is freely mutable, and the shared ref/repository objects are
explicitly acknowledged as unfrozen. Both are in-process risks C02 partly declares; the module-level
dict is not declared.

## 5. Rehydration and cross-process paths

`LearnedProductLifecycleExecutor.from_checkpoint` (line 2699) is the only rehydration entry and it
**does not consult the perimeter** (only `stage_release` per subject, then direct ledger/event
restore). Its integrity check compares the caller-supplied `checkpoint_hash` against
`semantic_hash(caller-supplied payload)` — both sides caller-controlled (H1). Probe H2 rehydrates
`publication="PUBLISHED"` with a `CURRENT_SELECTED` event, `perimeter_consulted=false`.

Consequently the mandate item "cross-process rehydrate/replay" is answered: **rehydration is a
complete, unperimetered ingress to B5 state.**

## 6. Items the mandate asked for that are structurally *absent* (no defect)

- **In-process module/global registry mutation of a slot registry:** absent. C02 holds no global
  slot registry; custody is per-instance. No attack surface exists (L1).
- **Forged custodian object:** only `ProducerCustodyMaterial` is accepted, exact-type enforced, and
  `material.slot` must equal the mapping key. No gap found.
- **`replay_root_ref` / receipt / ceiling / AuthoritySnapshot substitution via the public
  surface:** structurally impossible (one `str` field). Refused with `REQUEST_SURFACE_VIOLATION`.
- **`CURRENT_SELECTED` spoof via the perimeter:** structurally impossible; the perimeter never calls
  `select_current`, and an `assert` over `FORBIDDEN_SELECTION_EVENT_KINDS` guards it. **Further:
  probe A1 confirms `current_selection_performed=false`.** Note this is a *facade* property only —
  `CURRENT_SELECTED` is trivially reachable via the raw executor (B3) and via rehydration (H2).

## 7. Trust-root conclusion

The candidate supplies a **correct, well-built facade** and an **incorrect security boundary**.
The missing artefact is not more candidate code; it is either (a) a mandatory, universal ingress
that the accepted B5 owner, the composition path and rehydration are all forced through — which
requires mutating accepted owners, out of this commission's scope — or (b) an honest rename of this
candidate to a caller-side facade plus a recorded hold that F8F's B5 trust gap remains open.
