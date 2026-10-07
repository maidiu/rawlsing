# PYAT HQ236 — F7 OWNER-BOUNDARY / THREAT-MODEL ARCHITECTURE HOSTILE ADJUDICATION — R1

**DISPOSITION:** `F7_OWNER_BOUNDARY_ARCHITECTURE_DECISION_READY__EXACT_CONTRACT_AND_OPTION_RULING`  
**REVIEW BRANCH / COMMISSION:** `agent/reviewer-pyat-hq236-f7-owner-boundary-architecture-r1` / `44581009b053147fc4e1498b247735fa463717d4`  
**DECLARED COMMISSION BASE:** `c86ae335eaf70e82b5764c46754b16ca7e1587ce`  
**MODE:** independent browser/GitHub documentary hostile analysis. No production execution, code mutation, architecture adoption, semantic mutation or self-adoption.

## Dispositive ruling

The HQ235 coordinated-substitution witness is a **real local P07/F7 owner-boundary defeat** at the committed source and court grain. Its adversary starts with a genuinely authorized SOURCE resolver and an EMPTY victim resolver, sharing a legitimate exact registry. It rebinds the lexical custody ledger *and* the victim's live `_by_ref/_by_key` anchors, using a constructed `_AuthenticatedResolverState` with the victim owner ref but genuine source relations/authority snapshots. The normal P07 authenticated decision becomes positive and the normal F7 request reaches `TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED`. This does not forge source authority content; it forges the **owner-to-valid-custody association**. The test intentionally asserts success, not refusal.

The HQ235 statement that a native C-held capability automatically makes custody nonforgeable against an adversary able to rebind **every Python object and function** is **false as an end-to-end F7 claim**. Even with a protected C ledger, the F7 producer presently makes its owner decision through a Python module-global alias, `_authenticated_source_relation_decide` (`pre553_temporal_comparability.py:247-251,1110`). Its subsequent check is a Python function (`_relation_decision_defect` at :440-500) and the enclosing `compare_temporal_anchors` function is Python. An attacker authorized to rewrite those functions or the caller-visible result can bypass, replace or simulate the decision after/before the native check. Native custody protection is not Python callsite integrity and not end-to-end trusted receipt verification.

Conversely, HQ235 has not established a **universal theorem** that *every possible Python-level container* is always caller-reachable/reassignable. It examined a significant set of CPython 3.11.3 reflection primitives and defeated the actual design. That is sufficient to falsify this candidate; no universal quantifier is needed. Under truly arbitrary same-interpreter code execution, impossibility of **enforcing an authentic Python-observable F7 decision** follows from the attacker being able to replace the computation/observable result, independently of whether a particular custody store is secret.

## A. Exact accepted threat-model archaeology

The original F7 contract accepted at `c57a96897788108db7b194e4e51691d1ca8ab729` governs two-anchor temporal comparability, exact authority/source-relation closure, 12-state precedence, exact-zero differences, and negative ceilings. It does not state a general security guarantee against all arbitrary hostile same-interpreter Python execution.

Later commissions **explicitly expand the hostile owner-provenance surface**, and their terms must not be retroactively minimized:
- HQ219 F7-RR-04: caller-controlled stub/denied/wrong-pair relation is not enough; a genuine positive P07 owner decision is necessary.
- HQ227 F7-RR-04D/E: exact resolver instance mutation; relation/registry injection, subclass shadowing, method/validation monkeypatch probes and exact nested authority provenance; demands a non-forgeable owner path.
- HQ231 F7-RR-04F: live state exposure, `object.__setattr__`, closure/lexical stores, inspector exposure, resolver-field replacement and constructor custody.
- HQ234 lead + HQ232 hostile review F7-RR-04G: `__closure__` access and writable `cell.cell_contents`, actual source→victim custody rebind.
- HQ235 repair commission: requires resistance to enumerated in-process reflection, visible field/registry mutation, helper recovery, state construction and owner-binding transplant. Its worker also locally probed `__code__`, `__defaults__`, class/module rebinding.

**Classification:** ordinary hostile input/forged relation material is not the same attacker as arbitrary runtime code mutation. Later *commissioned* hostile powers are binding review demands for the active F7 closure attempt, but they are not proof that the original temporal semantic authority made the whole Python interpreter an untrusted execution environment. HQ must explicitly rule the trusted computing base and claim rather than assuming either direction.

## B. Concrete attack audit

Relevant source at `c86ae335eaf70e82b5764c46754b16ca7e1587ce`:
- `rawlsing_next/pre553_source_relations.py:535-625,937-1102`: tuple-backed state, live-container identity checks, fingerprint, ledger lookup, state sealer.
- `rawlsing_next/tests/test_pre553_temporal_comparability.py:2394-2664`: fixtures, precise reflection seam, single-primitive refusals and coordinated truth witness; specifically :2608-2659.
- `rawlsing_next/pre553_temporal_comparability.py:1099-1135`: actual F7 authenticated owner path.

The fixture is competent at the local source-free test grain: SOURCE carries a genuinely admitted `SOURCE_SEMANTIC_EQUIVALENCE` relation and pinned snapshot; VICTIM was constructed with no relation; the registry is shared so there is no new registry-authority minting. Both new live-anchor identities can be satisfied because the adversary changes the victim's live fields. The re-derived relation fingerprint matches the source-shaped inserted material. The new ledger entry binds victim identity to the source's custodied relation/snapshots/hash. `_state_or_refuse` now accepts the coordinated state and `_decide_from_owner_state` resolves source evidence from it. This defeats the actual P07/F7 positive path rather than only a cosmetic diagnostic.

Precision correction: although HQ235's code comment says `custody_hash` is re-derived at decision time, `_authenticate_owner_custody_anchor` directly re-derives **the relation fingerprint**; it does not independently recompute the entire constructor custody hash (including snapshots) from an unforgeable owner source at this seam. The transcribed source custody hash is then incorporated in the result. This is not a distinct new necessary exploit; it explains why the existing one remains possible.

The HQ235 worker reported targeted 228 passes and identical normalized broad regressions (54 failures/errors in both baseline and candidate). These are **worker-local reports**; this browser lane examined exact committed code/courts and did not independently execute CPython. The separate commissioned DeepSeek reproduction lane is independent evidence pending at this review grain and must not be represented as already consumed.

## C. Pure-Python and native security analysis

Three separate properties must be distinguished:
1. **custody confidentiality/integrity**: a caller cannot read/replace an owner→state mapping;
2. **decision authenticity**: the trusted authority check actually runs and cannot be skipped/substituted;
3. **end-to-end result authenticity**: an unauthorized positive F7 receipt cannot be returned and accepted downstream.

Against only data/limited reflection with the application code itself trusted, a carefully bounded Python owner can enforce many exact-fitness and provenance checks. HQ235's exact coordinated witness defeats the **present** Python architecture, so its present claim must not be greened.

A C-owned capsule without Python-visible state access could improve (1), assuming no hostile native memory/API access. But a Python-level entrypoint to that capsule can be rebound and the Python result path replaced; this does not prove (2) or (3). Even a genuine C decision can be ignored and a Python return forged. Requiring a native signed receipt only helps if a **trusted, non-bypassable verifier and consumer** rejects any unsigned forged result; a verifier callable wholly controlled by the same attacker is not such a boundary.

Separate-process IPC protects server-internal custody from Python-process reflection, but the compromised Python caller may still lie about the IPC result to Python downstream consumers. Genuine end-to-end authenticity requires an independently trusted consuming/verifying endpoint or moving the entire positive gate and reliance across the isolation boundary. An IPC socket or OS-backed handle alone is not a complete solution, and OS peer credentials/process permissions must be specified.

## D. Architecture disposition and decision tree

**Recommended immediate HQ decision:** do **not** adopt the HQ235 repair as full nonforgeability, and do **not** adopt its C-extension proposal as sufficient. First issue an explicit threat-boundary/TCB decision:

- **If HQ demands resistance to arbitrary hostile same-interpreter Python code mutation through final F7 output**, the trust boundary cannot end at a native custody capsule. Commission an architecture warrant for end-to-end protected decision plus trusted verification/consumption, preferably a separately isolated P07/F7 authority service with authenticated IPC and downstream verification outside the attacker-controlled Python interpreter. A native C component could instead hold the entire decision-and-use path, but must prove there is no remaining trusted Python-visible override. This is a materially broader redesign, not a one-file repair.
- **If HQ's binding adversary is narrowed to caller-owned data plus named reflection attacks while the trusted decision entrypoint/code and consumer are immutable**, either a small opaque native owner or further bounded Python hardening may be considered, with discriminating coordinated-attack tests. This must be an **explicit HQ limitation/authority decision**; it cannot silently weaken the HQ227–HQ235 commissioned nonforgeability claim.
- **If HQ accepts residual coordinated same-process compromise as out of scope**, freeze the exact weaker claim, mark current F7 as unqualified for full in-process nonforgeability, and test/qualify only the narrower property. Do not pass the existing intentionally successful attack as if it were a green custody court.

This adjudication makes the decision tree ready. **It does not adopt any option.** No native implementation, IPC design, or full threat-model change is authorized here.

## E. Productive adequacy and conservation

Whichever option HQ chooses must retain the lawful five: same-universe comparison, exact-zero/no authorized change, nonzero INCREASE, nonzero DECREASE, and genuinely authorized cross-universe comparison. Must preserve registry replacement immunity, constructor-pinned authority snapshots, actual P07 semantics, exact source universe/target use/operation/effective-scope binding, 12-state precedence, 19-kind prior ceiling, 3+ anchors refusal, no tolerance or interpolation, and no F8/causal/trajectory/currentness/pooling/actor power. The HQ235 reported local productive witnesses remain relevant but are not security closure.

## F. Final ruling

`F7_OWNER_BOUNDARY_ARCHITECTURE_DECISION_READY__EXACT_CONTRACT_AND_OPTION_RULING`

**Authority status:** NONE ADOPTED. **Implementation:** NONE. **Production mutation:** NONE. **Independent local execution:** NOT PERFORMED. **External DeepSeek lane:** NOT CLAIMED. HQ must choose threat boundary/TCB and issue an architecture decision before any F7 owner-boundary implementation or qualification.
