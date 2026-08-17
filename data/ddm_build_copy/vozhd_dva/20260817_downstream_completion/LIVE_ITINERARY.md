# Live Itinerary

**Status:** S00_READY_TO_LAUNCH  
**Canonical base:** `main`  
**Coordinator:** Vozhd Dva

## Wave 0

Closed. R0-01 through R0-05 have been reviewed and integrated back to canonical `main` through PR #40 (`1bbfb62791a583ab9ab7d21f5a0d76b4617b8f89`).

R0-01's returned fix is accepted: the V552J→V553 consumer boundary now fails closed on missing, unreadable/corrupt, schema-invalid, and integrity-invalid canonical publications while preserving valid-empty as distinct from failure.

## Immediate sequence

### 1. Launch S00 only

Session:
`S00 V552J → V553`

Workspace:
`schematics/sessions/S00_V552J_TO_V553/`

Run two independent breakout workers concurrently:
- **S00-F:** forward from V552J authority.
- **S00-B:** backward from V554 need.

Both workers:
- start from the same pinned S00 packet snapshot;
- make no production edits;
- do not read one another's results before submission;
- write only their assigned `RESULT.md` and `RESULT.json`;
- open draft PRs to `agent/vozhd-dva-s00-integration`.

### 2. Intake both S00 returns

Vozhd Dva reviews each report for:
- fidelity to actual upstream/downstream code;
- stage jurisdiction;
- explicit preserve/derive/drop/forbid/unresolved law;
- forward ceiling vs backward floor;
- object-grain disagreements;
- unsupported invention;
- concrete implementation consequences.

No worker-local schema becomes project law by merge.

### 3. Reconvene S00

Write the authoritative ruling to:
`schematics/synthesis/S00_V552J_TO_V553_RULING.md`

Freeze only:
- lawful V552J intake object(s)/grain;
- V553-authorized temporal operation;
- minimum V553 output grain;
- preservation/transformation ledger;
- current seam defects;
- implementation obligations/tests;
- exact V553 output contract for S01.

### 4. Promote S01 only after S00 is adjudicated

S01 remains blocked until the S00 ruling is `VOZHD_ADJUDICATED` and its accepted V553 output is inserted into the S01 context envelope as frozen upstream law.

### 5. Continue serially through S07

`S00 synthesis → S01 → synthesis → S02 → ... → S07 synthesis`

Within a seam, parallel independent thought is allowed. Across seams, speculative parallel architecture is prohibited.

### 6. Implementation only after schematic chain

After S07 synthesis:
- update `CAPABILITY_MATRIX.md`;
- generate finite non-overlapping implementation packets;
- implement against accepted seam contracts;
- use the Wave-0 vertical harness as standing semantic court;
- qualify horizontally only after representative vertical continuity works.

## Active risks

- Schematic sessions must terminate in implementable rulings, not ontology encyclopedias.
- Backward consumer need cannot authorize unsupported upstream invention.
- Forward evidence ceilings cannot be used as an excuse to discard distinctions downstream demonstrably needs when those distinctions already exist upstream.
- Aggregate convenience representations may not silently replace richer canonical identity.
- S01 and later sessions must remain blocked until their immediate upstream seam is frozen.

## Decision log

- 2026-08-17: adopted bounded verticalization rather than serial isolated stage completion.
- 2026-08-17: affirmed Enneagram-like attractor formation as intended design; V556 structural prerequisites/topology, V3 actor-specific realization.
- 2026-08-17: completed Wave-0 reconnaissance/harness work and integrated it to main.
- 2026-08-17: accepted R0-01 fail-closed V552J→V553 repair.
- 2026-08-17: established schematic transformation layer.
- 2026-08-17: changed schematic execution to one seam at a time, with parallel thought only inside the active seam.
- 2026-08-17: prepared S00 forward/backward breakout packets; later seams remain blocked.

## Next Vozhd Dva action

Launch S00-F and S00-B from their pinned branches. When both return, reconvene S00 before doing anything with S01.
