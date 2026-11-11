## Early construction findings — REVISE (not final completion)

Snapshot `de373b08ecc950541ce2f6264be85668354c0137`; review test artifact committed separately at `d33e58d5b4b8b841227f7e2356a970d44171508d`. No implementation or existing tracked source was modified.

### Executed tests
```text
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  -m pytest -q -p no:cacheprovider --basetemp "$PWD/.mii-review-state" \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_mii.py

# 4 passed in 224.26s
```

```text
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  -m pytest -q -p no:cacheprovider --basetemp "$PWD/.mii-review-state" \
  WORKER_REVIEWS/SOROK-MII-CONSTRUCTION-PROGRESS-R1/test_early_adverse.py

# 3 passed in 77.77s
```

The new tests intentionally assert the current defective behavior; passing confirms the defects, not conformance.

### Concrete findings

1. **Viewer-specific source identity is not enforced.**
   - `house.py:92-105` writes one global `presentation_conditions` object, including an `observer` field.
   - `mii.py:129-163` checks light, sightline and legibility but ignores `observer`; `run_p6.py:137-164` uses those details for the current user.
   - Test `test_viewer_observer_identity_is_not_enforced` set `observer="B"` while the current user remained `U`; `new` still returned non-null optional detail.
   - Consequence: room/global fixture access can be promoted to another viewer’s presentation, contrary to E2/MII viewer-source requirements.

2. **Forged recognition provenance is accepted as committed inspection.**
   - `mii.py:110-115` loads arbitrary `recognized` data from the profile.
   - `mii.py:230-250` trusts any existing row as `EARNED`, and `recognized_for` labels it `COMMITTED_INSPECTION`; `mii.py:244-250` explicitly does this without rechecking the event.
   - Test `test_forged_profile_recognition_is_accepted_as_committed` injected a `coaster` identity with an invented event; `view` returned that identity and `recognition_source == "COMMITTED_INSPECTION"`.
   - Consequence: E4/E8 provenance is forgeable through persisted user state; an uncommitted label becomes earned recognition.

3. **Adaptive evidence cannot distinguish independent user selection from exposed/offered selection.**
   - `mii.py:156-163` places every in-room object in `offered`, not just the optional selected item.
   - `mii.py:263-280` sets `independent = target not in offered`; since any lawful `look(target)` target is in `offered`, the `+2` independent branch is unreachable for valid actions.
   - Test `test_unselected_available_look_gets_only_offered_weight` looked at an omitted available object and observed weight `1`, uncertainty `HIGH`.
   - Consequence: E5/G01/G07 cannot distinguish a user’s unprompted target from a system-offered selection, so adaptive evidence is systematically miscoded.

### Scope gaps

- **E1 source denial/restore:** the existing occlusion test mutates `run_p6.establish`; it does not mutate a committed public source, observe a typed refusal, and restore it.
- **E2 per-viewer/feature source:** one global fixture controls all room/object presentation; `offered_details` filters only by room (`mii.py:156-163`).
- **E3/E8 exposure and replay:** the four MII tests cover one cold profile reopen and scope mismatch, but there is no branch-fork, interrupted exposure, immutable-entry tamper, or duplicate-exposure integration proof.
- **E5:** no decay, conflicting-evidence resolution, or correction-linked hypothesis behavior beyond explicit weight setting; see `mii.py:263-280`.
- **E9:** no measurement implementation for latency distributions, storage growth, memory, provider calls/tokens, or replay-failure accounting.
- **E10 / original 44:** `test_mii.py` contains only four tests and no O01–O06/P01–P09/G01–G08/M01–M06/N01–N10/T01–T05 mapping; no README, versioned ABI documentation, PROGRAMMA delta, or complete integrated example.
- **E4 controls:** `mii-learn-label`/`mii-correct-label` operate on arbitrary target strings without exposure or target-existence provenance; this compounds finding 2.

### Positive evidence

- The four author MII tests pass for neutral exposure, cold profile reopen, earned recognition after a committed inspection, basic occlusion, explicit adaptive controls, and scope reset.
- Real consumers are used through `run_p6.experience`, `house.scene`, `house.perform`, and `read_house`; MII profile writes remain separate from world/actor state, and no extra model call is introduced on this path.
- The snapshot is explicitly `IN_PROGRESS_NOT_AUTHOR_HANDOFF`; no native, human, production, or protected authority is claimed.
