# C3: current physical repair acceptance and integration

[Start](README.md) · [Prior draft](https://github.com/maidiu/rawlsing/blob/b3b2fa13049513078c301a1f6574b661fcf390c5/PYAT_CONTROL_ROOM/ASTRA_PYAT_PHASE1_COMMISSION_BINDINGS_R1/C3.md) · [Exact inputs](https://github.com/maidiu/rawlsing/blob/b3b2fa13049513078c301a1f6574b661fcf390c5/PYAT_CONTROL_ROOM/ASTRA_PYAT_PHASE1_COMMISSION_BINDINGS_R1/C3.json) · [Review](08_REVIEW_AND_INTEGRATION.md)

Default owner: browser Sol High physical-path worker plus independent reviewer; one integration owner for shared decoder files. C3 is initially source-free. A different execution environment may be needed for native libraries; that is a capability routing issue, not automatically an Astra issue.

## Pinned starting evidence

| Item | Commit | Blob |
|---|---|---|
| Candidate decoder | `3cefb4ebf61ccdb6a8c5a03815438bdcda021292` | `37013eb52efb8b61ef202b0d686f729f459d79c5` |
| Current audited decoder | H125 `1585b3edf1014544dfce90bbeb758a5024d69855`; unchanged at planning baseline | `d2a074a41fb556a1cd5928a5fe1421ef3672a4e5` |
| Current facade | Same current baseline | `8a761119e4a8d68eb291fc4edfadb52e027f8284` |
| Qualified fan-in return | `9bf2fd3641136c58c9e54f050864eb9f29c1a6c4` | `4365bc346e7615382d0b909d09209260bbe8908d` |

Paths: `rawlsing_next/pre553_physical_decoder.py`, `rawlsing_next/pre553_source_backed_c11_facade.py`, and `WORKER_RETURNS/PREMAIN-CLOSED35-REPRESENTATION-IMPLEMENTATION-FANIN-R1/00_RETURN.md`. Reverify exact current blobs before applying any patch.

## C3-01 — accept/reject each repair independently

Recover constituent patch, test and authority identities from the fan-in; freeze the complete helper/codec/manifest closure. A reported historical 20-test protocol result and 42-test interaction result are evidence about that candidate, not current-run results.

- G01: exact nine-surface SAV native-int → float64 physical representation rule; reject global numeric coercion or widened applicability.
- D01: exact-source-SHA declared BIG5/WINDOWS-1252 decoder admission; reject guessed encoding, wrong SHA, absent declaration and text-semantic inference.
- D02: preserve an explicit opaque decoder-native date/time carrier; reject bare R5 date/time and timezone-aware values where authority remains absent.

Use an independent oracle derived from the accepted bounded law. Reviewer checks positive and hostile fixtures before acceptance; do not let the candidate's observed output define correctness. Dispose G01/D01/D02 separately; a failure in one does not prove the others invalid.

## C3-02 — integrate accepted changes into current code

HQ records the exact file allowlist and accepted dispositions. Apply the smallest current-compatible patch, preserving intervening current behavior. Never replace the full current decoder with the historical candidate snapshot. D01 and D02 share a file and must be reconciled by one owner. Any changed physical/semantic boundary triggers E02 rather than broadening coercion to make tests pass.

Run relevant existing source-free regression, each accepted repair's hostile cases, D01×D02 interaction, exact-SHA mismatch, unsupported encoding/date/time behavior, and current facade compatibility. Freeze platform/runtime/native-library identities from the applicable qualification contract. If dependencies cannot be provided in browser/CI, prepare the bounded Codex handoff; source files remain forbidden.

## Return and implications

Return candidate/current diff manifest, separate repair decisions, allowlist, integrated implementation identities, executed qualification receipt and remaining live obligations. Independent review must target the final integrated commit. A source-free accepted repair unlocks only affected future proof obligations; it does not rerun CLOSED35, certify survey semantics or close full horizontal F1 coverage.
