# AS3R3 Node5A-R2 — Corrected Cardinality Replay / Seal

## Terminal

`AS3R3_NODE5A_R2_CORRECTED_CARDINALITY_REPLAY_SEAL_COMPLETE__READY_FOR_NODE4B`

## Scope and ancestry

Executed only Node5A-R2 on `agent/verkhovod-as3r3-node5a-r2-replay-seal` from the existing command-only tip `127fda6e3275d9dd563903e6827d195db50bdade`. The command ancestry is `16098c57883fde512e933eb1a220ea59b6c526a8`; HQ reactivation disposition `a1cafae3859bd76b98372602e687a7c511880ae7` was consumed prospectively without rebasing or rewriting the worker command. No central, PRE-MAIN, main, or Sub-Vozhd branch was moved.

## Exact execution result

- Frozen Node4A inputs validated: **19/19**. Every reconstructed frozen input canonical serialization reproduced the exact per-role SHA-256 values in the accepted Node4A `PREDICATE_INPUT_HASHES.json`.
- Accepted predicate constructor invocations: **19** — one per frozen source/role input.
- Role/source-to-successor-ref mappings: **19**.
- Distinct canonical `EmpiricalPredicate@1.0.0` refs: **18**.
- Sole alias class: **`{A000,A1RAPP}`**.
- `A000` and `A1RAPP` remain independently addressable role keys and both resolve to canonical content hash `ac3fcb4e32a41f9972004b2c31da61e9b32ba69568a795d2c1e584c9bed21be0`. Role aliasing did not erase either source/provenance row.
- Canonical predicate representations serialized: **18 exactly once each**; role/source crosswalk rows preserved: **19**.
- Query inputs frozen: **0**; successor queries minted: **0**.

## Fresh-process deterministic replay

Three independent fresh Python process executions reproduced byte-identical replay output (minimum required: two).

- Fresh-process output SHA-256: `302c5636e1547f40ceaaceaf7eb20db42339932ace6d1596e053f55ddd0fb5f9` on runs 1, 2, and 3.
- Corrected replay package identity: `3b2324ff217b627b4b079695f141099ca09741e420c0e1e9fa9ccc363798ceaa` on all runs.
- 19-row mapping payload SHA-256: `081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e`.
- 18-object canonical manifest payload SHA-256: `ef5cd10a5af7fcaad82b7dca39f2035ff829c59fe6f45ec681f872810276ac27`.
- Sole-alias payload SHA-256: `5f3763afced573d70fc72233d3c28d6f2d4d2f3ce8585d050a48a43ef8b00f5d`.

The replay agrees with the prior fail-closed Node5A observation at `34caf24a79a0b49eae4cd0937e7b13f56bb38c2e` (19 mappings, 18 canonical refs, deterministic A000/A1RAPP collision) and applies the subsequently adopted court/Authority-34 disposition that this is the **lawful sole alias**, not a defect requiring manufactured identity.

## Governing court / authority

- Node4A accepted freeze: `4d66bc34c256f6bf3f9f707dda80d963881f3510`.
- Original Node5A fail-closed return: `34caf24a79a0b49eae4cd0937e7b13f56bb38c2e`.
- Identity/cardinality court: `dc597c5293ec62864617ff77a5e928d5edb36171` — `COMPLETE__DISPOSITION_A__19_ROLES_18_CANONICAL_PREDICATES`.
- Authority 34 / mandated ancestry: `16098c57883fde512e933eb1a220ea59b6c526a8` — adopts the 19-role / 19-mapping / 18-object law and authorizes this replay/seal.
- Frozen successor producer: `cfc240aa3a64c59509eab97450a7d3603af813cc`; file SHA-256 `ad7434186e5e72886333f438ed9726cec01a2d2cf740353175da938708a5ef6d`.

No production code or schema was changed. No source ID, role wrapper, derivation wrapper, or historical AS3R2 hash was injected into canonical identity.

## Hard-stop audit

Node4A was not altered; Node4B was not entered; no query minting, DiscoveryAuthority/frontier creation, LiTS-I/I05/C05R2B execution, candidate-terrain change, A/B/C fairness change, V3 work, or historical AS3R2 preimage recovery was performed.

Return owner: **SUB-VOZHD B — ARCHITECTURE / COMPILER / DVA / CHETIRI**.
