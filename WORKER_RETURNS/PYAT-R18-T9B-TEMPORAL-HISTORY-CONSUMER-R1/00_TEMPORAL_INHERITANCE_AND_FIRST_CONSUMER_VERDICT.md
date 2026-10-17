# PYAT R18 T9B — TEMPORAL INHERITANCE AND FIRST CONSUMER VERDICT

## Verdict

# `TEMPORAL_INHERITANCE_REUSE_WITH_MANDATORY_CLOCK_QUESTION_DISTINCTION__T9B_CANDIDATE_REQUIRES_INDEPENDENT_SCIENTIFIC_COURT`

The inherited V553 temporal machinery is **reusable and should be preserved, not
replaced**. But executing it against a real historical clock exposed a defect in
how the inherited model is normally framed, and fixing that framing is the actual
scientific contribution of this commission.

**28/28** frozen temporal tests pass. **8/8** pinned V553 consumer-contract tests
pass. Native closure **1259/1259** blob-verified.

---

## 1. A custody incident that could have invalidated every result

Before any experiment: this host contains an **ambient** `/Users/matthewsmith/Desktop/Rawlsing/`
with a `pytest.ini` and an unverified `data/ddm_build_copy/`. Plain pytest rootdir
discovery inserts that ambient directory into `sys.path`, so

```
pytest data/ddm_build_copy/tests/test_postg5_v552j_v553_consumer_contract.py
```

**silently imports unverified bytes from a different tree** while appearing to import
the pinned one. The symptom is an `ImportError` that looks like a broken harness.

`run_pinned_v553_suite.py` pins `sys.path` and asserts the resolved
`data.ddm_build_copy.__file__` lies inside this return **before collection**. With
the guard: **8 passed**. Without it: unresolved imports of bytes nobody verified.

**Any other worker that ran V553 code on this machine without that guard has
evidence of unknown provenance.** This is worth a separate custody note.

## 2. What the inherited V553 code already does well

Verified present in blob `5304b70f9f`, and **reused verbatim by identity**
(`T._interp is V553._interp` is asserted in the suite):

| Inherited capability | Why it is worth keeping |
|---|---|
| `_interp` | exact linear interpolation, no invented resolution |
| `_pressure_band` / `_bounded_score` | bounded 0–1; cannot emit a fake magnitude |
| `AUTHORIZED_/PROBE_ONLY_/BLOCKED_TEMPORAL_KEY` | **three-state**, not a boolean |
| `ALLOWED_MULTI_WAVE_GRAINS` | grain must be declared, not inferred |
| `_build_source_wave_anchor_manifest` | wave-anchor / known-at bookkeeping |
| `_build_interpolation_manifest(allow_interpolation=…)` | explicit gate, not a default |
| `_build_rupture_event_slot_ledger`, `_rupture_block_audit` | discontinuity is a first-class object |
| `_build_cohort_window_requirement_index` | cohort comparability |
| `_build_absence_noncomparability_register` | absence is recorded, not imputed |
| `_build_downstream_v554_handoff_index` | affordance-consumer handoff |

**Recommendation: REUSE.** Nothing here is improved by replacement.

## 3. The real finding: "the historical clock" is two different questions

The single most important result of this commission:

**Under strict known-at discipline, two-sided interpolation at a historical clock is
structurally impossible.** A right-hand anchor is *observed* later, therefore it is
*published* later, therefore it cannot be admissible at the earlier query clock.

Measured on TC1 (anchors 1990 = 0.20, 2000 = 0.60, query 1995):

| Clock question | M0 hold | M1 interpolation | M2 backoff |
|---|---|---|---|
| **AS_OF** (what was knowable in 1995) | 0.20 | 0.20 `TERMINAL_NO_RIGHT_ANCHOR` | 0.20 |
| **RETROSPECTIVE** (what today's archive says about 1995) | 0.20 | **0.40** `INTERPOLATED_NOT_OBSERVED` | 0.20 |

These are **not the same question** and must never be silently interchanged. The
engine now makes the clock question explicit in every value, and any wave published
after the clock is carried as a `PUBLICATION_LAG` flag so a retrospective value can
never be presented as knowable at that time.

**This is the scientific reuse/adapt decision: REUSE the inherited machinery, ADAPT
the clock framing to be an explicit as-of-vs-retrospective choice.**

## 4. The five frozen cases, as executed

| Case | Result | Prediction |
|---|---|---|
| TC1 trend | M1 interior 0.40; M0/M2 hold 0.20 | TP1 **HELD** |
| TC2 null stability | M0 = M1 = 0.50 exactly | TP2 **HELD** |
| TC3 discontinuity | M1 `RUPTURE_BRACKET_REFUSED`; M0 still 0.30 | TP3 **HELD** |
| TC4 incompatible geography | `NON_HARMONIZABLE_GEOMETRY`, **not pooled** | TP4 **HELD** |
| TC5 future leak | AS_OF `NO_TEMPORAL_SUPPORT`; RETRO 0.90 + `PUBLICATION_LAG` | TP5 **HELD** |

Plus TP6–TP8 all held. **No prediction was falsified, and none was edited.**

## 5. The two-time selected-world consumer

Same actor, same permission-valid structural/access world, two historical clocks:

| Query clock | Pressure band | Open opportunities |
|---|---|---|
| **1990** | low | `ROUTE_DEFERRED_REVIEW` |
| **2000** | medium | `ROUTE_PARTICIPATION`, `ROUTE_DEFERRED_REVIEW` |

**Materially different.** And `structurally_identical()` **proves** the structural
world, access grants, institution and grain are byte-identical between the two reads —
so the movement is attributable to the temporal channel alone, not to a silently
changed world.

Crucially, the 1990 read is `PROBE_ONLY_TEMPORAL_KEY`, not an authorized product
value: an interpolated interior point never masquerades as a measurement.

## 6. Honest correction made during execution

The frozen oracle initially under-specified the fixture: it did not say whether the
bracketing wave is published before or after the query clock. The first run produced
`TERMINAL_NO_RIGHT_ANCHOR` everywhere, which *looked* like an interpolation failure
and was actually correct known-at behaviour. I resolved it by making the clock
question explicit rather than by loosening the fixture — **the oracle was not edited**.

Two genuine defects were found and fixed in my own engine during the hostile pass:

1. **Revoked sources leaked through in retrospective mode** — `known_at()` was only
   consulted in the AS_OF branch. Fixed so revocation and archival non-renewal
   exclude a wave in *both* clock modes. This was a real bug, not a test artefact.
2. A wrong test expectation about probe-only vs blocked for a pre-first-observation
   query. Corrected in the test, not in the engine.

## 7. What is explicitly NOT claimed

- **No real observed temporal calibration.** Every series is synthetic and
  self-declared `synthetic: true`, `observed_temporal_calibration: false`.
- **No real EE12/EE14 source.** No source issuance, no OC05 installation, no N12, no V3.
- **No pooling** of unknown respondents into fictitious longitudinal individuals.
- **No modification** of any canonical or accepted module.
- **T8F3's source-claim assignment (`8079f697…`) is preserved, not duplicated,
  not modified, not re-run.**
- **Independent scientific court required before any new method adoption.** This
  worker cannot accept its own method.

See `04_COMPETENT_EE12_SOURCE_AND_N9_OWNER_GATE.md` for what a real source issuer
must supply before any of this becomes source-qualified product behaviour.