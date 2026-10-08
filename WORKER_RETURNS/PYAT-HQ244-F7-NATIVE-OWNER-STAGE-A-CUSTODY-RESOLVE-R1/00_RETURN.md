# HQ244 — F7 NATIVE P07 OWNER STAGE A: CONSTRUCTOR CUSTODY + EXACT RESOLVE — RETURN

**DISPOSITION: `F7_NATIVE_STAGE_A_CUSTODY_AND_RESOLVE_READY__NONAUTHORIZING_FOR_STAGE_B`**

Agent: Space Bunny / OpenCode. Model: Space Bunny Max.
**This is NOT a security pass, NOT production adoption, and it does NOT close F7-RR-04G.**

## What was actually built

A real compiled CPython 3.11.3 C extension in the quarantined namespace
`rawlsing_next._p07_native_owner_stage_a`, providing a genuine non-subclassable
native type with:

- **one-shot constructor custody** — `Py_TPFLAGS_BASETYPE` deliberately absent; a `sealed`
  flag refuses every re-`__init__`, reseal and re-admission;
- **deep, immutable, owner-local custody** — relation identity (`ref.key`, `content_hash`)
  is copied into C memory at admission. No Python-visible mutable handle, no capsule,
  no state loader, no copier, no reconstructor; `__setattr__` refuses every name;
- **exact-key-only `resolve_exact`** — three accepted input shapes normalised to one
  canonical `kind|object_id|content_hash` key, with no label/ID/latest/default inference;
- **identity re-verification on every lookup** — live `ref.key` *and* `content_hash` are
  re-read and compared against the sealed C copies, so a post-seal substitute, ref swap or
  hash mutation is caught rather than trusted.

**Stage A court: 39 passed.** Production is untouched: P07 24 passed, F7 163 passed.

## Fail capability actually demonstrated

The court is not vacuously green. A deliberately broken build
(`-DSTAGE_A_FAULT_INJECT`, which skips all identity re-verification) turns it
**red — 2 failed** — and restoring the real build returns it to 39 passed. The fault hook
lives inside `#ifdef STAGE_A_FAULT_INJECT`, which the shipped recipe never defines.

## Non-authorizing by construction

`decide` and `require` are unconditional failures carrying
`NOT_IMPLEMENTED_NONAUTHORIZING_STAGE_A`. There is no silent delegation to Python and no
`AUTHORIZED`, `RelationDecision`, `authorize` or `issue` symbol anywhere on the native
surface. Stage A **cannot** issue positive authority or an F7 receipt.

## Quarantine held

Production P07 and F7 are byte-identical to the commission tip. The court greps both
production modules for any reference to the native module. This coexistence is temporary
and exists only as a **non-authorizing prototype**; Stage B must eliminate the duplicate
positive Python owner at cutover. A custody-only capsule is explicitly *not* an acceptable
end state.

## Honest caveats — read these

1. **I did not reproduce the HQ242 baseline digest.** Broad regression matched the baseline
   *exactly* on counts (2691 passed, 45 failed) but gave **16 errors vs HQ242's 7**, and my
   normalized digest `72d0a5ca…` does **not** equal the required `278854ee…`. The extra
   errors are collection-time failures from genuinely absent optional dependencies
   (`pandas` ABSENT, `pyarrow` ABSENT, `d07_bounded_loss_harness`). I proved Stage A adds
   zero collection errors: collection yields 9 errors both with and without my files, and the
   test count rises exactly 2743 → 2782 (+39). **No digest match is claimed.**
2. `resolve_exact` does **not** re-hash `semantic_projection()`. It re-verifies `ref.key`
   and `content_hash` only. Full parity re-hashing is an explicit Stage B item.
3. The exposed `custody_hash` is a native FNV-1a provenance walk. It is **not** the accepted
   P07 custody hash and must never be compared against it.
4. The `by_key` index key is derived from the exact ref key, not the true relation object
   key. That removes a Python callback from the admission path, but it is a deliberate
   simplification Stage B must replace.
5. Identity re-verification is defence in depth: the accepted production relation is already
   frozen, so the substitute-object tests use a purpose-built mutable stand-in.
6. **Two real memory-safety defects were found and fixed during Stage A** — a NULL key read
   and a malformed `Py_BuildValue` format (7 keys, 6 specs). Both segfaulted before the fix.
   Recorded rather than hidden.

## Source / victim isolation

A genuinely adjudicated source relation was admitted alongside a genuinely independent,
genuinely empty victim sharing the same registry. The victim stays absent across hostile
visible-container edits, registry `_by_ref`/`_by_key` clearing, and registry rebinding, with
the custody hash unchanged. The HQ234–HQ236 `by_ref`-only transplantation shape has **no
surface to attack at Stage A** because no secondary `by_key` authority index exists yet —
a structural argument, **not** a recovery of the full F7 forgery court.

## Not claimed

No adjudicator, no precedence ladder, no replay decision, no canonical/semantic-hash
parity. No four-forgery court, no five lawful positives (Stage D gate), no V2–V4
re-measurement, no HQ231 alias re-measurement. **F7-RR-04G remains OPEN.**

## Next gates

- **Stage B** — full native `decide`/`require`, all 12 states, `CONFLICTING_AUTHORITY`
  precedence, replay identity, real custody hash, canonicalise/semantic_hash trusted seam,
  and an exact parity oracle (full decomposition in `04_STAGE_B_FULL_P07_PORT_DEPENDENCIES_AND_PARITY_PLAN.json`).
- **Stage C** — test adaptation, retiring the introspection-coupled Python seam.
- **Stage D** — independent hostile validation plus the real five lawful positives.
- Independent inspection of native source and binary before any Stage B adoption.

The environment is **not** the obstacle. Native build capability is proven end-to-end,
including the `-undefined dynamic_lookup` requirement HQ242 documented.
