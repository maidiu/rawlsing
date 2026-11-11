# 00 — HQ211 V556 UNBOUNDED value-gate and valid-empty repair — R1

Lane: `PYAT-HQ211-V556-UNBOUNDED-GATE-REPAIR-R1`
Role: bounded implementation repair worker — Space Bunny High
Commission tip: `694b220cfbb14353c59eeec503f0ae0d9cab97bc`
Repair base: `3a2dcafe024b2556af1df909deb5452841e45b7c`
Hostile review: `agent/reviewer-pyat-hq210-v556-final-r1 @ 46bf1ac246f51d7499bccf56e41add78779e00ad`

**Disposition: `V556_BOUNDED_REPAIR_COMPLETE__READY_FOR_FINAL_HOSTILE_REREVIEW`**
**V556 remains unadopted.**

Change set: **2 files**, +560/−50. Zero seam edits.

---

## 1. I reproduced every defect before fixing anything

A repair that hasn't reproduced its defects is a guess. I built one probe harness and
ran it twice — against the unrepaired base and against the repair — driving
author → registry → the **unmodified** M3 seam and inspecting the emitted positive object.

| Probe | Hostile value | Before | After |
|---|---|---|---|
| P1 | `DOMINATION` on an UNBOUNDED string leaf | **SUPPORTED** `{"label":"DOMINATION"}` | refused |
| P2 | `HEGEMONY` on an UNBOUNDED ref-kind leaf | **SUPPORTED** | refused |
| P4 | `"0.87"` magnitude on a string leaf | **SUPPORTED** `{"magnitude":"0.87"}` | refused |
| HAND1/2 | same, via hand-authored mapping | **SUPPORTED** | refused |
| P7a/b | generic authoring of both families | **registered → `GOVERNED_RULES_PRESENT`** | refused |
| P5 | ten actor-semantic role labels | **10 accepted, 0 refused** | **0 accepted, 10 refused** |

## 2. The root cause was not a missing check

M3 was **correct**. At `m3:655-660` and `m3:667-669` it constrains a string/kind
*only when the declaration is closed*; at `m3:931` it copies the payload verbatim.
The substrate was handing it an `UNBOUNDED` declaration and then claiming closed
governance in prose. So the fix belongs in the substrate, and **the seam stays byte-identical**.

## 3. What each repair actually did

**Repair 1** — `UNBOUNDED` is no longer legal for a semantic *value* or *kind* leaf, at
both the constructors and `_validate_authored_schema_node`. The validator walks the node
*mapping*, so hand-authoring cannot evade it (HAND1/2 confirm). It runs in schema authoring
→ binding authoring → binding validation → rule authoring → registry build, i.e. before any
positive object exists. Structural cardinality `UNBOUNDED` is deliberately untouched, as instructed.

**Repair 2** — the valid-empty claim is now machinery, not an accident of the shipped
instance. Both families are refused at `author_governed_rule` **and** independently at
`V556RuleMaterialRegistry.build`, so a hand-built `GovernedRule` cannot slip through.

**Repair 4** — replaced the blacklist with a **positive per-family allowlist**
(`V556_TOPOLOGY → STRUCTURAL_ENDPOINT_A, STRUCTURAL_ENDPOINT_B`), derived only from the
roles the canary already used. No role invented. The discriminating witness is
`CIVIC_ASSOCIATION`: innocent-looking, names no blocked token, and a blacklist would have
accepted it. The token blacklist survives as defence in depth, but for participant roles the
allowlist subsumes it entirely — so the blacklist can no longer be what makes the claim true.

**Repair 6** — the illustrative/no-F2 labels stay documentary and are surfaced in the
registry snapshot where they're truthful; the court now asserts they are **absent** from
emitted rule/schema/contract material. `validate_payload_against_participants` is now
declared a court/helper utility, and the court asserts the seam never calls it. I did
**not** wire it in, because that needs a new seam and HQ211 forbids one.

**Repair 7** — `binding_ref.object_id` checked at authoring; the actor-named schema classes
`OBJECTIVE_ACTOR_POSITION`/`OBJECTIVE_ACTOR_OPPORTUNITY` **withdrawn** (they were incoherent
with the role ceiling) and every class now names the family that authorizes it; hand-built
bindings are deep-frozen at rule authoring instead of waiting for registry build.

## 4. Repair 3 — I made the claims true rather than narrowing them

Both disproved claims are now enforced as written:

- *"No numeric magnitude can be authored through any positive path"* — **now true** (numeric node types refused; `UNBOUNDED` value leaves refused; closed lists enforced by the seam).
- *"The whole actor/person-semantic class is blocked"* — **now true** (allowlist is total over its complement).

The superseded prose lives in HQ206's return directory. HQ211 forbids writing outside its
own return dir, so I did **not** edit those files — `05_FINAL_DISPOSITION.json` carries the
correction ledger of record.

## 5. The regression slice, and one thing worth flagging

I compared exact failure-ID sets by running the repaired court against the **unrepaired**
module, then the repaired one:

**15 failing IDs → 0. New failures introduced: 0.**

The discriminating set is those 15. But **five of my new witnesses also pass against the
unrepaired module** — `w3b`, `w7`, `w8`, `w9`, `w10`. Those are positive controls and an
anti-vacuity check, not proof the repair worked. I've said so in the return so nobody
over-counts them.

## 6. Two disclosures

- **No pytest existed here.** I installed it (9.1.1) into an isolated throwaway venv with
  `--break-system-packages`. HQ211 forbids claiming a historical governed environment that
  is absent, so I'm not pretending otherwise.
- **The full-suite baseline is not claimed.** Only **4 of 157** test files are materialized
  under the commissioned sparse scope, so a full-suite number would be meaningless. I supply
  the structural substitute instead: 2 changed files, **zero production importers** repo-wide,
  seam contains zero references to the substrate, seam byte-identical.

Also worth noting: at the repair base the three courts pass **92/92** with the *original*
court — matching HQ210 exactly. The old court was green and blind to all eight routes.

## 7. Preserved, not traded away

M3/M2 byte-identical (`736c17d8…` unchanged) · truthful dyadic maximum 2 · no mandatory
shared-channel field · `AUTHORIZED_INTERACTION_RELATION_KINDS = ()` · no fabricated relation
kind · no attractor population · deep-frozen material · frozen multiplicity vocabulary ·
exact M3 hash mirroring · the five previously fixed defects still fixed. All twelve reductions
HQ210 credited as sustained remain intact.

## 8. Residual — none blocking

Six named items, all disclosed rather than smoothed: full-suite baseline not reproducible ·
pytest environment disclosure · payload helper not on a production path (commission's
explicit second option) · allowlist deliberately narrow · structural `UNBOUNDED` retained by
instruction · five non-discriminating witnesses.

## 9. For the final hostile re-review

I'd attack: any route that bypasses all four authoring surfaces at once; any attempt to
widen the allowlist or family set without a governed rule authority; whether the labels are
really absent from emitted material; and an independent reproduction of 92 → 111.

**This lane does not adopt V556 and does not certify a full-suite baseline.**

`HQ211_V556_BOUNDED_REPAIR_RETURNED__FINAL_HOSTILE_REREVIEW_REQUIRED`