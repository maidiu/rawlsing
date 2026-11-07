# Final selective receiving PR draft — publication held

**Status:** CANDIDATE ASSEMBLED ON ISOLATED BRANCH. No PR was created, no protected ref changed, no merge performed. Additive residual-proof qualification remains PENDING; HQ owns final publication and any required PROGRAMMA/current-progress updates.

## Title

`SOROK P3: receive scoped sourcefree developmental state and actual P2-root proof`

## Body

```text
Selective receiving candidate for the P3 sourcefree developmental-state line.

Base: integration/pre-main-reconciliation-r1 @ c852d7516e23fcb6cf2215e9be7c5fa268503516
Isolated candidate branch: codex/sorok-p3-selective-receiving-20261107-r1
Runtime/evidence cut: 16275d03fc4724a694c48ed9d447c4eeadbe25f2
Implementation cut: 486d42a4aa5dcd449564b95567ae93b59c4679a4
Goal audit: 140b585f9b7321984725cf6f38ae95c2cb2bf89c
Additive residual proof: 036787c1f0c227cdc47828ba521a62b76c57a903

Source-ref custody note: at assembly the source branch head had moved to 687dc0cfc0d1f32942bec1e07eff68a811b8f0df, a descendant of 9abb3eee/16275d03. Runtime/test SHA-256 values at 687dc0c are identical to 16275d03; the observed head adds evidence/coordination/PROGRAMMA records only. This candidate uses the frozen 16275d03 runtime/test bytes and excludes the added coordination/PROGRAMMA; HQ must reconcile that source-ref movement before publication.

This is a selective checkout of 186 paths, not a bulk merge. It contains the 170-path prepared package plus 15 focused-review artifacts and 1 HQ focused-recheck disposition. Runtime/tests remain byte-identical to the accepted source; no runtime/test/authority edits were made.

Focused review:
- e85b6f6a733ef5bbd664679bdf9613c04003e3de is ACCEPT_SCOPED_TEST_ONLY for exact runtime 16275d03; M1/M2/M3 are closed.
- Independently executed: 61P/1 inapplicable skip store/owner, 37P units, 3P M1/M2, PRIMARY, cold reopen, identity/denial/cross-root, real-process crash and resource. No full 13-case matrix rerun by the reviewer.
- Prior REVISE negative evidence remains preserved.

Provenance correction:
- 16275d03 also updates three PROGRAMMA_SOROK records (08, 09, 10); this was not a pure evidence/checkpoint commit. No runtime, source hash or authority changed.
- HQ FOCUSED_RECHECK_DISPOSITION.json records the correction. This candidate excludes the PROGRAMMA changes; HQ will integrate required concise PROGRAMMA/current-progress updates before publication.

Evidence retained:
- 13/13 author/HQ combined PRIMARY/A-H/resource matrix at implementation 486d42a4.
- 71/71 inherited engine tests plus cold-process compatibility.
- Store/owner and unit evidence; goal audit; additive residual-proof author tests 3 passed in 27.14s.
- Residual author proofs are pending nonauthor qualification: matched source/history/later-objective-world formation-vs-stability, genuinely distinct seeded P2 roots with foreign-source denial, and actual-chain B1 missing/altered/exact-restore replay.
- Same-history limit retained: equal objective world/P2 identity/clock/source/history/later proposal, but independently initialized deterministic P2 fixtures have different full state_hash; no exact P2 root snapshot/fork/remap API is claimed or invented.
- Resource: DB 4,096 B + WAL 1,536,792 B = 1,540,888 B; per-record 741,600 B, per-event 247,200 B; no universal performance claim.

Remaining before publication:
- Nonauthor qualification of additive 140b585f/036787c1 residual proofs.
- HQ reconciliation of source-ref movement 16275d03 -> 687dc0c (runtime/test hashes unchanged; evidence/coordination/PROGRAMMA only).
- HQ final PR publication, protected receiving and merge. No one merges from this author assembly.

Holds:
- Sourcefree TEST_ONLY engineering only.
- No native CAN/ADP science, original human validity, independent B, ADP016/017 memory or claim issuance, production positive rule, source grant, protected CAS or merge authority.
```

## Branch construction

See `COMMANDS.md`. The candidate branch is already assembled locally from the protected base; no PR was created.
