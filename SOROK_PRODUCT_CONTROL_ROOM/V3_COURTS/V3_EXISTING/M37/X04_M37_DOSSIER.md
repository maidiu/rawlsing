# X04 M37 — structural placeholder scene / non-LLM years

**Court grade:** `HISTORICAL_SOURCE_AUDITED` + `HISTORICAL_RUN`; current integration `UNTRACED`.
**Coverage:** `PARTIAL_WRONG_MEANING / CONFLICTING` — no-scene markers are partly quarantined, but annotations can still enter memory/previous-scene.
**Authority:** historical server/display code only.

## 1. Direct source map

| Symbol | File:lines | Input → output | Actual role |
|---|---|---|---|
| `render_year` | `v3/render/phenomenology.py:55-160` | state/derived, optional packet/callback → rendered_output | No packet = no narrative snapshot; parse fallback marker |
| server loop | `server/generation/simulation.py:538-575` | run_one_year, band/non-band → annotations | Non-LLM year `structural_placeholder_used=True`; annotation scene |
| `_trajectory_backstory_from_snapshots` | `v3/io/persona_sheet.py:470-575` | per-year snapshots → trajectory text | Ruptures/gifts/events; no scene field usage |
| scene collection | `persona_sheet.py:869-896` | rendered scenes → backstory | `real_scenes` exclude markers; `elif scene` fallback includes marker/annotation |
| `_previous_scene` | `server/generation/simulation.py:716-720` | rendered scene → continuity | Excludes only no-scene/structural markers |
| `distill_memory` | `v3/tools/distill_memory.py:57-104` | backstory → cleaned | Filters `[Structural year]`/no-scene; not "Age X: health declined" |

## 2. Actual behavior

- `render_year` without packet sets no `narrative_snapshot`; it is a structural/no-scene year.
- Server non-LLM years set `structural_placeholder_used=True`; if significant state deltas, it writes `rendered_output.narrative_snapshot.scene = "Age X: health declined."` etc. (`server...:554-575`). This text has **no `[Structural year]` marker**.
- `persona_sheet.real_scenes` excludes strings containing `[This year had no recorded scene` or `[Structural year`; the annotation passes and is collected as a "MEMORIES" line (`persona_sheet.py:877-892`).
- If `real_scenes` is empty, the `elif scene` branch (`:893-894`) writes the current scene as "Most recent memory" **even when it is a marker**; our probe confirmed `[This year had no recorded scene.]` and `[Structural year: no LLM scene rendered]` can appear as "Most recent memory" if no real scene.
- Server `_previous_scene` only filters markers, so an annotation "Age X: health declined." can be passed as previous scene into the next Pass 2.
- `distill_memory` filters `[Structural year]`/no-scene artifacts but not the annotation text.
- Tests: `test_architecture_invariants.py` render nonmutation; no test of annotation quarantine/previous-scene/backstory. **Reviewer probe** used `build_persona_sheet` with one snapshot and three scene forms; both markers and annotation entered the backstory.

## 3. N06/N09 differential

N06 needs interstitial routines/support/missed actions and materially changed conditions; N09 needs fallible, actor-owned memory distinct from objective history. M37 provides:
- an honest structural-year/degraded annotation idea;
- partial quarantine of no-scene markers in `real_scenes`/distill;
- but the annotation is a **state-delta summary**, not a lived scene, and can be misclassified as a memory/previous scene.

**Coverage:** `CONFLICTING` / `PARTIAL_WRONG_MEANING`; do not claim full quarantine.

## 4. Disposition / first consumer / owner

**Retain:** structural-year annotation as explicit non-memory metadata, degradation flags, `rendered_output` separation.
**Adapt:** tag every non-LLM/structural scene (including server annotations) with a marker/kind; exclude from memory/previous_scene/distillation; or keep annotation only in a non-scene field.
**Create:** interstitial activity/time record that is not narrativized as experienced memory; retrospective memory source is realized trajectory, not state summary.

First consumer: server persona sheet/backstory and next Pass2 `previous_scene`; no current C9/C12.

**Owner:** server/persona/ADP016/C9 owner; no native grant.

**Negative/fault:** if a structural annotation enters "MEMORIES" or `previous_scene`, the old code is not quarantined at the claimed grain. The reviewer probe is a sourcefree demonstration; no human memory claim.
