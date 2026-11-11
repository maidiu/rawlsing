# R0-05 — Vertical Fixture and Continuity Test Harness — Result

- **Worker:** `R0-05`
- **Branch:** `agent/vozhd-dva-r0-05-vertical-harness`
- **Base SHA:** `958983139b8f75dc5cda65d5bf71b376d17820df`
- **Target base:** `agent/vozhd-dva-wave0-integration`
- **Draft PR:** `#37`
- **Implementation head at PR creation:** `5e3fcf41c17261b65b28eace121b066aded5592f`
- **Worker status:** `COMPLETE_WITH_FINDINGS`

The assignment is complete within its authorized test-only domain. The harness is green as a reference-contract court while current production semantic continuity remains deliberately non-green: five strict XFAILs encode the five Wave-0 cross-stage gaps instead of inventing V553–V558 semantics.

## 1. Fixture design

The fixture is deterministic and synthetic: one reference source-country (`REFERENCE_SURVEY` / `ZZ`) with three ordered waves (`W1`, `W2`, `W3`) and stable typed identifiers. It is intentionally small enough for routine PR execution while carrying every fixed Wave-0 distinction:

- one persistent temporal relation;
- one drifting temporal relation;
- one rupture-like structural change, explicitly only a `RUPTURE_CANDIDATE` and with no external-event claim;
- two opposing structural pressures in the same conflict set;
- one mediation route containing a typed `BUFFER` condition and a typed `AMPLIFY` condition;
- two pressure-flow route candidates tied to those conditions;
- two attractor prerequisites that explicitly forbid finished personality-type assignment;
- explicit `UNCERTAIN`, `ABSENT`, and `NONCOMPARABLE` states, with absence/noncomparability represented by `None`, never zero/neutral;
- stable authority/provenance IDs;
- one adversarial direct structural-to-persona/biography inference request that must fail closed.

Reference packets for V553 through V558 are marked `REFERENCE_CONTRACT_FIXTURE_NOT_PRODUCTION_OUTPUT`, set `production_semantic_readiness_claim=False`, and carry an explicit future-producer obligation for the stage they stand in for. They are a reference consumer contract, not a claim that current production stages already emit the represented semantics.

## 2. Test inventory

Focused command:

```bash
python -m pytest -q data/ddm_build_copy/tests/vozhd_dva_wave0/test_vertical_continuity.py
```

Result:

```text
12 passed, 5 xfailed in 0.11s
```

The passing guard/reference tests cover:

1. deterministic fixture construction and stable-ID uniqueness;
2. explicit future-producer obligations on every reference packet;
3. temporal persistence / drift / rupture-candidate continuity;
4. preservation of contradictory pressure identity and sign;
5. buffering vs amplification mediation continuity;
6. pressure-flow route and attractor-prerequisite continuity;
7. uncertainty / absence / noncomparability preservation;
8. artifact-shape success separated from semantic-preservation success;
9. information-loss detection when a required buffer condition disappears;
10. direct persona/biography/Enneagram-like inference rejected fail-closed;
11. stage-output persona leakage rejected fail-closed;
12. the complete reference V553→V558 consumer contract passes while explicitly making no production-readiness claim.

The five strict XFAILs correspond one-for-one to the five fixed vertical slices. Each XFAIL asserts the desired future `PASS` condition against an explicit `CURRENT_GAP`; an unexpected green therefore means a gap declaration must be reviewed rather than silently disappearing.

## 3. Current pass/fail/gap matrix by vertical slice

| Slice | Reference contract | Current production continuity | First surfaced gap | Wave-0 disposition |
|---|---|---|---|---|
| VS1 temporal persistence / drift / rupture | PASS | GAP | `V554→V555` | strict XFAIL |
| VS2 contradictory inter-strata pressure | PASS | GAP | `V554→V555` | strict XFAIL |
| VS3 mediation with buffering / amplification | PASS | GAP | `V555` | strict XFAIL |
| VS4 pressure-flow / attractor prerequisites | PASS | GAP | `V556→V557` | strict XFAIL |
| VS5 uncertainty / absence / noncomparability / forbidden inference | PASS | GAP | `V554→V558` | strict XFAIL |

There are no unexpected focused-test failures. The five XFAILs are intentional current-gap accounting, not test weakening.

### Semantic-readiness vs artifact-shape readiness

`test_artifact_shape_success_does_not_imply_semantic_readiness` deliberately deletes the noncomparability distinction from a V557 reference packet while leaving its packet envelope/artifact-shape status intact. The shape report remains `PASS`; the semantic report fails. This prevents process success, packet existence, or a nominal readiness label from standing in for preservation of required meaning.

### Information-loss detector

`test_information_loss_detector_fails_when_buffer_condition_is_dropped` removes the `BUFFER` condition at V556. Artifact shape remains valid, but the semantic court raises `SemanticContinuityError`. This is the minimum concrete proof that a required distinction can make an otherwise successful-looking chain fail.

### Forbidden-inference detector

The fixture includes a direct request for `enneagram_type` plus invented biography from structural/temporal evidence. `reject_direct_persona_inference` rejects it. A second test injects `persona_fact` into V558 generated output and verifies the entire chain fails closed.

## 4. Producer-consumer obligations surfaced by current gaps

### R0-05-H001 — V554/V555 temporal identity handoff

V553 currently has typed temporal keys, observations, deltas, gaps, and rupture candidates. V554 can retain bounded seed provenance, but V555 does not guarantee preservation of the temporal relation/key identity needed by later mediation and pressure-flow consumers. Wave 1 needs an explicit temporal-identity carry-through contract rather than a reconstructed generic slot.

### R0-05-H002 — V554/V555 contradictory pressure identity handoff

V554 can carry source contradiction identifiers. V555 currently reduces mediation to seed IDs and unresolved slot topology. V556 therefore cannot rely on two distinct competing pressures, their signs, and their shared conflict set surviving mediation. Wave 1 needs pressure identity and conflict-set provenance on the mediation handoff.

### R0-05-H003 — V555 typed mediation effects

Current V555 provides mediation topology but does not express a typed condition/effect relation equivalent to `BUFFER` and `AMPLIFY` against named source pressures. V556 must not invent those effects from generic household/family/carrier slots. Wave 1 needs a bounded typed mediation-condition contract with provenance and uncertainty.

### R0-05-H004 — V556 pressure-flow / attractor prerequisite identity

Current V556 exposes generic route axes and attractor requirements but does not guarantee stable route identity tied to mediated competing pressures and conditions. V557 then carries renderer boundaries rather than the full semantic prerequisite graph. Wave 1 needs stable route/prerequisite IDs and source mediation/pressure IDs retained through the renderer boundary.

### R0-05-H005 — epistemic/provenance survival to V558

Absence and prohibition are explicitly represented upstream and runtime leakage is blocked downstream, but the chain does not yet guarantee that uncertainty, noncomparability, absence, and authority provenance all survive as distinct runtime-input metadata. V558 must receive these as typed states, not infer neutral/zero or reconstruct missing authority.

None of these hooks blocks integration of this Wave-0 harness. They block promotion of the corresponding production slice from `CURRENT_GAP` to semantic `PASS`.

## 5. Recommendations for Wave 1 CI placement

1. Add the focused test file to the ordinary downstream PR test lane; runtime is ~0.1 s in isolation.
2. Keep all five production-gap tests `strict=True` XFAIL until the owning producer/consumer hook lands. Do not convert them to loose XFAIL or delete them to obtain green CI.
3. When a hook lands, change only the corresponding `CURRENT_PRODUCTION_COVERAGE` entry after adding a production adapter test that demonstrates the real stage output satisfies the reference-consumer assertion.
4. Preserve the artifact-shape-vs-semantic-readiness negative test permanently. It should remain a regression court even after all five slices become green.
5. Preserve the information-loss and forbidden-inference tests permanently; they police distinct failure modes that normal happy-path build tests do not catch.
6. Do not wire the reference packets into runtime or production builders. They are test authority for required distinctions and future-producer obligations only.

## Files changed

- `data/ddm_build_copy/tests/vozhd_dva_wave0/__init__.py`
- `data/ddm_build_copy/tests/vozhd_dva_wave0/vertical_continuity.py`
- `data/ddm_build_copy/tests/vozhd_dva_wave0/test_vertical_continuity.py`
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/rabochii/WAVE_0/R0_05_VERTICAL_HARNESS/RESULT.md`
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/rabochii/WAVE_0/R0_05_VERTICAL_HARNESS/RESULT.json`

No V553–V558 production semantics, V550–V552J code, full-data qualification, V3/V2 implementation, or runtime/persona generation was modified.
