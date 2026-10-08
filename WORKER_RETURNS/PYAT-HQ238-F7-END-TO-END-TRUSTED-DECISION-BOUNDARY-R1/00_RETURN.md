# PYAT HQ238 — F7 END-TO-END TRUSTED DECISION-BOUNDARY DESIGN — R1

**DISPOSITION:** `F7_TRUSTED_DECISION_BOUNDARY_DESIGN_COMPLETE__READY_FOR_HQ_ARCHITECTURE_ADJUDICATION`  
**STATUS:** **PROPOSED DESIGN — NOT AN ADOPTED ARCHITECTURE, IMPLEMENTATION, AUTHORITY CHANGE, OR THREAT-MODEL CHANGE.**

**Repository:** `maidiu/rawlsing`  
**Branch:** `agent/rabochii-pyat-hq238-f7-end-to-end-trusted-decision-boundary-r1`  
**Commission tip:** `16ee0054622077c84f815c71c04468bc39411d61`  
**Exact governed startup/code base:** `ae5e140a378406888c94d099b7dd8e98dfeb1459`  
**Current code blobs:** P07 `8053d30d306a3654ebf563043088311ff390bb2b`; F7 `6f6b462b1cdef54d7989f15452473383c1661594`; F7 court `8a82bd5905d266c1d500b1bf2bdcb01ea948efd6`. All three independently verified identical at startup base and commission tip.

## 1. New decisive evidence, and the previous review's precise limit

The independent governed local proof (HQ236 coordinated-hostile-evidence R1, candidate `c86ae335eaf70e82b5764c46754b16ca7e1587ce`, governed CPython 3.11.3) established:

| Attempt | Actual victim result |
| --- | --- |
| Original HQ234: source payload + source anchor fields, rebind ledger cell | **REFUSED** under HQ235 repair |
| HQ235: replace victim's two visible live containers, then rebind ledger | **FALSE POSITIVE** P07 AUTHORIZED, F7 `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED` |
| HQ236: keep victim's live containers completely untouched, use source payload + victim anchor fields, rebind **only** ledger cell | **FALSE POSITIVE** |
| HQ236: same one-cell rebind but transplant **only** `by_ref` payload, retain victim's empty `by_key` | **FALSE POSITIVE** |

Controls: original source is truly positive, empty victim is truly negative, and restoring ledger restores both. Attack 3/4 demonstrate that HQ235's "all single reflection primitives closed" claim was false. No callable/code monkeypatch, authority forgery or native primitive was required. The status `F7-RR-04G__LEXICAL_CUSTODY_LEDGER_CELL_IS_CALLER_REBINDABLE` remains **OPEN**. The 228 green targeted tests and unchanged broad normalized failure set are regression evidence, **not provenance closure**. The witness asserting a successful forgery is a **red security gate**, regardless of pytest pass count.

Root cause: `pre553_source_relations.py:587-625` compares **self-declared sealed anchor fields** with `resolver._by_ref/_by_key` and recomputes a public fingerprint of live `_by_ref`. Decision code at :629-936 consumes independent `state.by_ref`, `state.by_key`, authority snapshots, hashes, and `custody_hash`. Neither those payloads nor the full custody hash is proven to come from the victim's sealed constructor. The existing F7 :1110-1150 subsequently accepts the positive P07 decision. A hash of attacker-selected material is integrity syntax, **not an ownership proof**.

The independent HQ236 browser review correctly rejected (a) generalizing this specific exploit into a universal pure-Python impossibility theorem and (b) claiming a C custody capsule alone secures F7 if trusted Python entrypoints or terminal outputs may be overwritten. The newer local proof makes the first claim **narrower and stronger as fact about this candidate**, and leaves both broader architecture distinctions intact.

## 2. Threat model freeze as a PROPOSAL, not silent authority

- **T0 input hostility:** hostile relations/ref/snapshots and mutable caller-held data through legitimate APIs, but owner implementation, issuer and relying consumer trusted. Authenticated means exact lawful constructor-admitted relation plus exact pinned authority snapshot and decision/replay cross-binding; forged means an empty owner becomes positive from caller data alone. Grounded in adopted P07 and F7 semantics, HQ219 (stub/wrong kind/denied/wrong pair), HQ225 and HQ227 exact snapshot/caller-state tests.
- **T1 commissioned reflection hostility:** additionally in-process `__closure__` reading, `cell.cell_contents` writes, `_AuthenticatedResolverState` construction, visible field replacement, `object.__setattr__` where applicable, recovered helper invocation, and the explicit HQ227 nested instance/class/method monkeypatch probes. **The final trusted F7 implementation and terminal consumer executable path are not under arbitrary rewrite**; their module-global attested entrypoint alias is in the TCB, not a free replacement seam. If HQ instead includes arbitrary replacement of that alias in T1, T1 cannot use trusted Python F7 and must be advanced to T2 or have a separately trusted consumer. A reflected callable or presented `RelationDecision` is not independently authoritative without native owner execution. Grounded in HQ227, HQ231, HQ234, HQ235 commissions and governed HQ236 witness.
- **T2 arbitrary same-interpreter code/output substitution:** includes `__code__`, globals including `_authenticated_source_relation_decide`, the F7 comparison function, replay validation and the Python final receipt/consumer. The **untrusted Python process cannot be the trusted terminal observer or accepting effect sink**. No semantics contract originally grants protection under these powers; HQ236 architecture review classifies them as a stronger independent attacker. Genuine T2 protection must move P07 decision + F7 calculation + the actual accepting consumer across an independently protected execution boundary. Merely returning an authenticated IPC packet to untrusted Python does not meet this.

**Not claimed by T0–T2:** adversary can alter sealed macOS service binary, dedicated-account permissions, server process memory, native C internals, kernel, trusted external acceptor, or stored accepted authority roots. Such powers require separate threat/architecture adjudication, and ordinary same-user service isolation alone may be insufficient to exclude them.

Detailed per-tier TCB and positive-forgery definitions are frozen **as candidate design** in `01_T0_T1_T2_THREAT_AND_TCB_CROSSWALK.json`.

## 3. Verified existing call graph and semantic bounds

**P07 live:** `SourceRelationResolver.__init__` (`pre553_source_relations.py:1004-1086`) calls constructor validation and seals a `NamedTuple` into a writable closure-cell ledger (:937-982). `_authenticated` (:1203-1226) loads state then evaluates `_decide_from_owner_state` (:812-936), which checks exact P07 relation kind, source pair, scope, target use, effective scope, versioned authority and replay identity. `validate_relation_decision_replay_identity` (:767-810) validates the returned decision's semantic hash, **not independent owner provenance**.

**F7 live:** `compare_temporal_anchors(request, registry)` (`pre553_temporal_comparability.py:836-1493`) creates no extra source equivalence; at :1099-1145 it calls the captured P07 function `_authenticated_source_relation_decide` (alias :247-251), then `_relation_decision_defect` (:433-499). The request's actual fields are at :686-739. The output `TemporalRelationReceipt` (:742-795) is **module-local**, content-addressed and **not** `CanonicalSemanticObject`; it has `receipt_hash` but **no unforgeable issuer authentication** and no claimed current public object registration. Cross-universe F7 must independently prove real P07 SOURCE_SEMANTIC_EQUIVALENCE, operation `SEMANTIC_EQUIVALENCE_ADMISSION`, exact `EXACT_BOUND_UNIVERSE_PAIR` scope/effective scope and actual `governed_use_id.object_id`. F7 separately proves TEMPORAL_COMPARABILITY and all other required authorities and derives exact signed delta.

**Adopted downstream use:** the inspected F7 test courts call `compare_temporal_anchors` directly. Inspected M1/V554 tests are regression neighbors, **not evidence that M1 consumes F7's receipt**; the HQ210 contract expressly authorizes **no F8 consumption**. I did not obtain a repo-wide exhaustive import graph in this browser-only lane and therefore do not assert that no other consumer exists. Before a T2 architecture commission, HQ **must** inventory every terminal receiver/authorization effect of `TemporalRelationReceipt` and either move it into the trusted gate or forbid its use as a positive authorization sink. An unlocated terminal consumer is not an implicit newly authorized one.

## 4. Two actual candidate architecture paths

**Design I (recommended if HQ explicitly freezes T1, T2 out of scope):** a **native CPython 3.11.3 exact, non-subclassable, one-shot P07 owner object**, not merely a capsule attached to a Python resolver. Owner construction and complete P07 adjudication run in the native protected implementation; immutable validated relation and pinned snapshot bytes are copied into private native state keyed to the **same exact resolver instance** and cannot be mutated/resealed from Python. No exported state loader, constructor sealer or owner→payload reassignment function. Native P07 produces an exact bound `RelationDecision` for a given resolver and full request. Existing trusted Python F7 consumes that decision through one pinned native owner entrypoint and still runs its accepted F7 state/receipt semantics. A caller can replace visible `_by_ref/_by_key/_registry` diagnostic fields without altering native custody; legitimate `_registry` replacement immunity continues. A Python class wrapper whose sole private capability may be replaced by the caller **fails** this design. The design migrates P07 adjudication to one owner implementation rather than creating a competing P07 authority; conformance/differential courts are mandatory. This protects T1, **not T2**. Exact interface/provenance/state/control flow in `02_T1_OWNER_PROVENANCE_IMPLEMENTABLE_DESIGN.json`.

**Design II (T2):** move the **entire trusted P07→F7 comparison→receipt verification→relying decision/commit** into a protected owner service operating in a separately administered trust domain with immutable accepted authority bootstraps and server-side per-job resolver custody. The untrusted Python client submits typed *requests/candidates*, never registers a self-issued owner or authoritative snapshot. The service binds job/owner/source/scope/use/effective-time to trusted pre-provisioned material, runs the accepted algorithms server-side and commits a positive effect **only through an internal trusted sink**. Returned IPC receipt bytes are display/copy **only**, not acceptance; client fabrication/alias replacement cannot create an accepted event. OS/transport identity, exact requests, protocol/release/replay version, correlation, nonce/counter, body hash, client replay and result mutation are independently gated. Avoid requiring signing if a protected server journal and trusted same-side sink suffice; if asynchronously exported, provide an authenticated envelope with verification in the trusted recipient. Exact interface in `03_T2_END_TO_END_TRUSTED_GATE_DESIGN.json`.

The two paths have fundamentally different reliance boundaries. They are **not** interchangeable uses of a "native" or "IPC" label.

## 5. Recommendation and HQ decision required

Recommend **T1's exact bounded provenance guarantee** *conditionally on HQ formally constituting the T1 TCB and excluding arbitrary trusted F7 executable/alias/final-consumer replacement*. This is the smallest declared change that blocks **all four** verified 04G variants while preserving the existing F7 receipt contract and avoids inventing downstream F8/V3 consumers. The cost is a real CPython-native P07 migration, exact ABI/build/replay parity and source-level independent hostile qualification; **a storage-only C capsule fails the requirement**. If HQ wants T2, issue a separate explicit architecture warrant for Design II and first identify the authoritative downstream accepting consumer: that is larger and presently not proved to exist at production integration grain.

No refusal-only closure: courts must show all five lawful F7 positives, including authorized cross-universe comparability, after every attack family and after all protected replay/integrity checks. In T2 the final trusted accepting effect must match the lawful positive and reject a forged positive, independently of what hostile Python prints or returns.

**Design status:** COMPLETE FOR HQ ADJUDICATION, NOT ACCEPTED.  
**Permission:** NONE to mutate production, create native code, start IPC, narrow threat authority, or merge.
