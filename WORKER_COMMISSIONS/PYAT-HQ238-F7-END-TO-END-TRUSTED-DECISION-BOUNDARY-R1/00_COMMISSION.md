# PYAT HQ238 — F7 END-TO-END TRUSTED DECISION-BOUNDARY DESIGN — R1

**STATUS:** NEW — NEEDS LAUNCH  
**AGENT:** Browser/GitHub documentary architecture/semantic-authority design worker  
**MODEL / INTELLIGENCE:** **GPT-5.6 Sol High**  
**MACHINE:** Browser/GitHub; do not use the user's Mac  
**BRANCH:** `agent/rabochii-pyat-hq238-f7-end-to-end-trusted-decision-boundary-r1`  
**EXACT STARTUP BASE:** `ae5e140a378406888c94d099b7dd8e98dfeb1459`  
**PRODUCTION MUTATION:** FORBIDDEN  
**ARCHITECTURE / THREAT-MODEL ADOPTION:** FORBIDDEN  
**OWNER/AUTHORITY SEMANTIC MUTATION:** FORBIDDEN  
**SELF-ADOPTION:** FORBIDDEN

## Mandated context — read exact documents

1. `WORKER_RETURNS/PYAT-HQ236-F7-COORDINATED-HOSTILE-EVIDENCE-R1/00_RETURN.md`, `02_EXACT_ATTACK_AND_CONTROL_RECEIPTS.json`, `03_ANCHOR_IMPLEMENTATION_AND_REGRESSION_AUDIT.json`, `04_THREAT_MODEL_AND_PROOF_LIMITS.json`, `05_FINAL_DISPOSITION.json`, and the auditable `reproduction/` scripts and outputs.
2. `WORKER_RETURNS/PYAT-HQ236-F7-OWNER-BOUNDARY-ARCHITECTURE-R1/00_REVIEW.md`, `05_FINAL_DISPOSITION.json` at independent branch `agent/reviewer-pyat-hq236-f7-owner-boundary-architecture-r1 @ 7a9a0a5917b888c15b3ead051fb116b7549b37c9`; it is **not necessarily an ancestor of your branch**. Use exact cross-branch read only; no merge.
3. `WORKER_RETURNS/PYAT-HQ235-F7-NONFORGEABLE-CUSTODY-BINDING-REPAIR-R1/`; candidate `c86ae335eaf70e82b5764c46754b16ca7e1587ce`.
4. `WORKER_RETURNS/PYAT-HQ232-F7-SEALED-OWNER-STATE-FINAL-REREVIEW-R1/`, `WORKER_RETURNS/PYAT-HQ232-F7-RUNTIME-QUALIFICATION-R1/`.
5. Governing accepted F7 semantic contract and HQ219/HQ225/HQ227/HQ231/HQ234 hostile authority chain. `PYAT_CONTROL_ROOM/26_HQD216_PRODUCTIVE_ADEQUACY_AND_PREV3_EMPIRICAL_GATE_LAW.md`.
6. Live source/consumer call graph, notably `rawlsing_next/pre553_source_relations.py`, `rawlsing_next/pre553_temporal_comparability.py`, and every adopted F7 receipt consumer. Locate precise methods/paths at the exact base; do not invent source code or call sites.

## HQ-ratified evidence

- F7-RR-04G is STILL OPEN in HQ235 repaired candidate; a **lexical ledger-cell rebind alone** can mint positive custody if the constructed state carries the source's payload but anchors to the victim's untouched live `_by_ref` / `_by_key` fields.
- The first HQ235 claim "all individual reflection primitives closed" is falsified. The original HQ234 variant with source anchor fields was refused, but a materially equivalent, narrower one-cell rebind with victim anchors succeeds.
- Precise failure: gate validates **self-declared anchor fields**, not whether `state.by_ref`, `by_key`, `authority_snapshots`, semantic hash maps, and custody hash derive from constructor-sealed owner custody.
- Independent local governed CPython 3.11.3 controls/attacks/regression have returned in `ae5e140a...`; no production mutation. Green 228 targeted tests and unchanged broad failures do not close provenance forgery.
- A separate browser architectural hostile review rejects universal pure-Python impossibility as proven and rejects **native custody capsule only** as a sufficient end-to-end F7 security answer under attacker modification of trusted Python code.
- HQ has **not adopted** a narrowed adversary claim, native architecture, IPC architecture or full F7 acceptance.

## Mission: design a decision-ready *end-to-end* trust boundary, not another vague options list

The previous architecture review provided an option decision tree. Your job is to make that decision **implementable and bounded**. Do not simply repeat its prose.

### A — lock the distinct protection claims

Precisely distinguish:

- **T0 — ordinary source/caller-input hostility:** malicious/contradictory relation receipts, wrong exact refs, fake registry material, visible input mutation, and legitimate API use while trusted program logic executes unchanged.
- **T1 — explicit F7 provenance hostile reflection:** same-interpreter code that can read `__closure__`, write `cell.cell_contents`, construct state NamedTuples, replace caller-visible instance fields, recover helpers and invoke normal trusted P07/F7 decision paths; trusted production executable code and trusted terminal consumers remain unchanged unless particular accepted commission explicitly expands that.
- **T2 — arbitrary same-interpreter executable/result substitution:** hostile replacement of trusted `__code__`, module-global dispatch aliases, functions, verifiers and Python-observable final receipts. Under T2 no purely internal custody storage proves end-to-end authenticity without a trusted computation/consumer beyond the compromised process.

For EACH:
1. identify the exact accepted contract or commission that admits it or says no such thing;
2. define the TCB (trusted executable code, owner state, parent process, consumer);
3. state what "authenticated" actually means and what observable constitutes forgery;
4. avoid silently moving T1 capabilities into T0, or silently downgrading the binding later F7 reflection commissions.

### B — two concrete bounded designs, with real interfaces and gate placement

Produce **at least two** fully specified candidate designs:

**Design I — T1-hardened custody/decision route** with unchanged trusted code/consumer: show actual owner-instantiation, constructor custody storage, P07 provenance check, positive-result binding, F7 call path, replay and consuming gate. If an implementable pure-Python design cannot be justified against T1's admitted reflection, say explicitly where it fails, then specify minimal native/isolated state primitive; *do not* declare a C capsule sufficient if attacker can bypass Python code under T2.

**Design II — T2 end-to-end trusted decision/consumption route:** move the P07 authority decision, F7 comparison, receipt authentication, and relying consumer/verification operation into a protected boundary, or give an equally explicit arrangement proving that the untrusted Python process cannot issue a trusted positive by replay/fabrication. Define request format, sealed immutable authority snapshots, response identity, replay binding, versioning and negative states; explain why authenticating IPC bytes alone is NOT enough if the final consumer is attacker-controlled.

For both, specify:
- exact trust root and owner of the capability;
- boundary and API types;
- call graph before/after;
- source, authority, operation, target use, scope, and effective-time exact binding;
- allowed error/negative states and failure contract;
- repository/build/test dependencies and actual supported governed macOS Python/CI portability;
- migration relation to current `pre553_source_relations.py` and `pre553_temporal_comparability.py`;
- expected change terrain and compatibility risk;
- implementation work split for Space Bunny versus DeepSeek-Harness execution;
- acceptance courts that **fail on actual unauthorized positive**, never misleading success-forgery assertions;
- how all five HQD216 lawful positive paths remain productive.

### C — minimal post-HQ236 attack closure proof

Any proposed T1 design must defeat ALL exact reproduction variants:
1. original HQ234 source-anchor-ledger rebinding;
2. HQ235 coordinated live-anchor and ledger substitution;
3. HQ236 one-cell-only with victim live anchors;
4. HQ236 single `by_ref` payload transplant.

Propose at least one independent hostile proof for the payload-vs-anchor consistency invariant. Do not use only a public recomputable fingerprint or a self-declared source-to-owner reference. Do not rely on the caller's signature or "trusted" arbitrary registry label without issuer provenance.

### D — contract-level option recommendation

Recommend one of:
- T1 as the exact explicit bounded F7 provenance guarantee, **with** a justified non-forgeable T1 implementation path; T2 expressly outside the assertion;
- T2 protected end-to-end architecture warrant, with minimal trusted consumer boundary;
- fail-closed hold because the available evidence cannot support an enforceable architecture decision.

Give specific authority/compatibility costs and reasons. Do not authorize a choice yourself.

### E — deliver a deterministic implementation / review sequence

Write two paste-ready **proposed** successor commission skeletons corresponding to chosen option: implementation plus independent hostile/runtime qualification, clearly labeled `PROPOSED_NOT_AUTHORIZED`. They must pin concrete candidate base and invariants, and must not self-issue a production or architecture commission.

## Allowed dispositions

- `F7_TRUSTED_DECISION_BOUNDARY_DESIGN_COMPLETE__READY_FOR_HQ_ARCHITECTURE_ADJUDICATION`
- `F7_TRUSTED_DECISION_BOUNDARY_DESIGN_PARTIAL__NAMED_BLOCKER`
- `F7_TRUSTED_DECISION_BOUNDARY_CONTRACT_CONFLICT__COMPETENT_OWNER_REQUIRED`

## Return

Write under:
`WORKER_RETURNS/PYAT-HQ238-F7-END-TO-END-TRUSTED-DECISION-BOUNDARY-R1/`

- `00_RETURN.md`
- `01_T0_T1_T2_THREAT_AND_TCB_CROSSWALK.json`
- `02_T1_OWNER_PROVENANCE_IMPLEMENTABLE_DESIGN.json`
- `03_T2_END_TO_END_TRUSTED_GATE_DESIGN.json`
- `04_ACCEPTANCE_COURTS_PRODUCTIVITY_AND_TRANSITION.json`
- `05_DECISION_TRADEOFF_AND_PROPOSED_COMMISSIONS.md`
- `06_FINAL_DISPOSITION.json`

This is design only. No production changes, runtime tests, architecture adoption or HQ decision. Push only your commissioned branch and report exact remote SHA.
