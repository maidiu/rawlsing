# PYAT HQ217 — V556 INDEPENDENT RUNTIME EVIDENCE — R1

**Disposition: `V556_INDEPENDENT_RUNTIME_EVIDENCE_COMPLETE__READY_FOR_HQ215_ACCEPTANCE_CLOSURE`**

- Startup tip: `cdfa47b0b040a18bfd1c0d3049c8dfc24fb3613a`
- Candidate under evidence: `9129bd54adbe73fdc09f8a3c02e4b91902d56661`
- Unblocked rereview: `747271cc1726c8fc7e40f2de21f5047a32abeaeb`
  (`V556_FINAL_REREVIEW_BLOCKED_BY_MISSING_EXACT_EVIDENCE`)

This lane is execution/qualification only. I made **zero semantic code edits**,
committed no mutated ontology or authority, and did not redesign V556.

## What HQ215 said was missing, and what I actually ran

HQ215 refused on **evidentiary** grounds, not semantic ones. It could not execute.
So the four things it demanded:

| HQ215 gap | Result |
|---|---|
| Independent `118 passed` certification | **118 collected, 118 passed**, twice, on two interpreters |
| The claimed `4 → 0` defect-sensitive slice | **Confirmed exactly**, with the same four IDs |
| An *independently executed* scratch coherence probe | **Executed**; the shared decision is reachable at runtime |
| Proof the environment exercises the candidate | **Stale-import tripwire** clean |

## 1. The 118-item surface

Collection matches HQ215's source-level reconstruction precisely:

```
61  test_pre553_v556_positive_substrate_court.py
29  test_m3_v556_higher_order_structural.py
28  test_m2_v555_atomic_route.py
    118 total
```

**118 passed, 0 failed / errored / skipped / xfailed**, 0.43 s.

I ran it on a *second, deliberately different* interpreter as well and got 118
passed again. That is worth something beyond decoration: it shows the result is
not an artifact of one interpreter.

## 2. Defect-sensitive before/after — the claim holds

I swapped the unrepaired repair-base module in (`e4d7e6f73`, sha256
`ade55043…`), cleared `__pycache__`, ran the same slice, restored, and compared
sorted failure-ID sets.

- **Before:** `4 failed, 114 passed` — the four IDs are exactly
  `test_d1_coherence_decision_refuses_genuine_mismatches`,
  `test_d1_registry_build_is_wired_to_the_coherence_decision`,
  `test_d1_unmapped_class_is_refused_by_the_coherence_decision`,
  `test_payload_participant_helper_classification_is_machine_readable`.
- **After:** `118 passed`.
- **New failures introduced: 0.**

The four IDs match HQ214's recorded list item for item. Restoration was verified
by sha256, not assumed.

## 3. The dynamic coherence probe — this was the real gap

HQ215 could trace the coherence gate at source level but could not *reach* it,
because every ordinary mismatch is refused earlier by the authorable-family
ceiling. That is a genuine evidence hole, so I closed it with an in-memory
scratch mutation of `TRANCHE_LOCAL_ADMITTED_SCHEMA_CLASS_FAMILY_MAP` only:

1. **Lawful positive path first.** Genuine `V556_TOPOLOGY` rules author and
   register as `GOVERNED_RULES_PRESENT` for all three admitted classes. This is
   the HQD-216 check: the gate cannot be satisfied by blanket refusal.
2. **Ordinary mismatch path, honestly labelled.** All six genuine mismatch pairs
   refuse — but they refuse at the **family ceiling**, before the coherence
   decision. I recorded this as `evidence_for_coherence_gate: false` rather than
   letting it masquerade as proof.
3. **Scratch remap.** Remap `OBJECTIVE_WORLD_STATUS` →
   `V556_INTERACTION_RELATION` in memory only. `V556RuleMaterialRegistry.build`
   still **PASSES** upstream (family/role checks, contract validation, body and
   dataclass family agreement), and only then does the shared decision fire:

   > `registry material rule 'R-OBJECTIVE_WORLD_STATUS' is incoherent: semantic_class
   > 'OBJECTIVE_WORLD_STATUS' is authorized by 'V556_INTERACTION_RELATION' but the
   > rule declares 'V556_TOPOLOGY'; class and family must agree`

Ontology restored immediately, module file byte-unchanged after the probe, and
the positive path still works afterwards.

**The shared coherence decision is independently reachable at runtime.**

## Environment truth, stated exactly

Primary: `LOCAL_COURTS/qualification/r7-c4-source-free-venv` — CPython **3.11.3**,
pytest 9.1.1, numpy 2.4.6, pandas 2.3.3, pyarrow 25.0.1, pyreadstat 1.3.6. Its
`pyvenv.cfg` records the pinned `cpython-3.11.3-macos-x86_64-none` home and the
exact creating command, so its provenance is documented rather than assumed.

**I do not claim it is a governed project environment.** It is a qualification
interpreter with reproducible pinned provenance.

Two honest discrepancies against HQ214's recorded environment, both reported
rather than papered over:

- HQ214 ran with `PYTEST_DISABLE_PLUGIN_AUTOLOAD` disabled. This lane ran with
  plugin autoload at its environment's default. I did not artificially reproduce
  the other configuration to make the reports match.
- The secondary cross-check interpreter is 3.12.14 with no pyarrow. That is why
  it is labelled reconstructed-equivalent, not qualification.

Neither difference blocks HQ215 closure: the blocker was *independent execution*,
which this lane supplies.

## Stale-import tripwire

The executed module resolved to the working-tree file path, its sha256 matched,
the coherence decision was present, and `TRANCHE_LOCAL_AUTHORABLE_FAMILIES` was
exactly `('V556_TOPOLOGY',)`. The environment is exercising the candidate.

## One bookkeeping note

HQ214's prose "55 → 61" is intermediate bookkeeping. The authoritative base
surface is 54 + 29 + 28 = **111**, which is what HQ214's own qualification JSON
records and what I measured. No semantic conflict; recording it so the counts are
not over-read.

## Scope

Writes confined to `WORKER_RETURNS/PYAT-HQ217-V556-INDEPENDENT-RUNTIME-EVIDENCE-R1/**`.
The coherence probe was a local scratch harness, run and **deleted**; nothing was
committed from it. No semantic edits, no mutated ontology, no authority changes,
no self-adoption, no source access. Single authorized sparse worktree; no clone.

Terminal: `PYAT_HQ217_V556_INDEPENDENT_RUNTIME_EVIDENCE_RETURNED__HQ215_ACCEPTANCE_CLOSURE_AVAILABLE`