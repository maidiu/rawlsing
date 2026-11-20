# SOROK REMONTATHON R15 — independent hostile receiving

**Frozen author candidate:** PR #1220, `6075792420e1d87b30036ebe6f352815783e47c2`; direct parent R14 `f8c0d8dc901116d5fd1bfa7ec992dffa90a9aef0`. Draft, unmerged. **Overall verdict: `REVISE_EXACT_DEFECT`**. This is sourcefree software review, not credential-independent GitHub/G5, science, native protected, or human approval. No original implementation code altered.

## Independently executed (Python 3.13.5)

- Exact runnable Library archive `SOROK_REMONT_R15_P012_P018_276_TESTS.zip`: SHA-256 `cc044f0796a77fc8dfa0155dea13b87107ba83a784fd6ea4444901ad471c6664` verified by local sha256sum.
- Fresh extracted original 276: 276/276 normal PASS; 276/276 optimized `-O` PASS; pytest 276 PASS +22 subtests. Executable sourcefree `python -m um_sorok_organism demo` exited 0.
- All 46/46 original source/test Python files individually matched local size, SHA-256, Git blob hashes in exact R15 manifest. 46/46 Git blob IDs match exact GitHub source-tree descendants of frozen `6075792420e1d87b30036ebe6f352815783e47c2`. No source family substitution.
- Added **six new reviewer-designed tests** in the actual R15 `tests/` directory: **P012** all 64 distinct four-form acyclic inhibition graphs match a separate deterministic surviving-inhibitor oracle (**PASS**); **P018** five independent source-read/append challenges **RED** on both normal and optimized interpreters. Combined 282-suite: 277 PASS / 5 FAIL, normal and `-O` (282 executed). Pytest `--maxfail=5`: 5 reproduced failures, 46 passing tests +2 subtests before early stop; no misleading full-pytest claim.
- Python 3.11 is **NOT_RUN**: only CPython 3.13.5 installed. `UV_OFFLINE=1 uv python install 3.11` refused because the interpreter was not in cache and this environment has no network. Prior unrelated 3.11 R12 proof is not an R15 compatibility test.

## P012 — `ACCEPT_SCOPED_SOURCEFREE_FIRST_FAULT`

For fully cued, qualified forms and an acyclic inhibition graph, the new sourcefree deterministic stratification computes exactly the survivors from active inhibitors. The new reviewer cross-product explores all 64 directed DAG subsets of `a→b`, `a→c`, `a→d`, `b→c`, `b→d`, `c→d` and matches a separate oracle. The author's A inhibits B inhibits C correction, link-order independence, and conservative mutual-inhibition control passed. No broad psychological fidelity, general non-acyclic settlement, native CAN/ADP, or scientific recruitment law is accepted.

## P018 — `REVISE_EXACT_DEFECT`: audited-bad history still read and extended

The repair's `_verified_source_seals_locked` (`storage.py`, near lines 90–141) iterates only event kinds `INITIALIZATION` and `SOURCE_SEAL`, comparing source maps and sealed table contents. It does **not** verify the canonical bytes, event IDs and hashes of those historical issuer envelopes, nor does it reject source-seal maps in ordinary events. `source(sid)` calls this incomplete fast check; `commit()` checks source maps plus only the *last* event anchor. The full `verify_chain()` correctly rejects each hostile history below, while the actual preflight still grants read/append rights. This directly defeats the user-visible R15 promise of source integrity *before reads or further writes*.

**Five independently reproduced RED cases, all normal and `-O`:**

1. Initialize with a legitimate `seed` source and append a legitimate ordinary event. Update the sealed source row from `{'truth':'A'}` to `{'truth':'B'}`; also rewrite the historical **initialization** source-seal digest to match B without recomputing the immutable event ID/chain. Full `verify_chain()` rejects `BAD_EVENT_ID`. **`source('seed')` nevertheless returns the attacker-altered B.**
2. Same modified history: with a perfectly normal expected-version transaction, **`commit('OBJECTIVE_CUE',...)` succeeds and appends a new hash-consistent event to the already unauditable source ancestry**, instead of refusing atomically.
3. Initialize normally and append ordinary `OBJECTIVE_CUE`. Add an unauthorized `source_seal_digests={'ghost-source':'fictional-digest'}` to that **ordinary event**, recompute its event ID and chain hash to be internally valid. `verify_chain()` rejects `SOURCE_SEAL_EVENT_UNAUTHORIZED_ANCHOR`; **`source('seed')` still returns content**.
4. Same unauthorized ordinary-event anchor: **`commit('OBJECTIVE_CUE',...)` accepts and appends** instead of refusing, leaving history invalid.
5. Legitimately add a late `SOURCE_SEAL`, then append a single trailing whitespace character to its event payload. The history is `EVENT_ENVELOPE_NONCANONICAL_BYTES` under full audit; **`source('later')` accepts the invalid envelope and returns content**.

These negatives are against sourcefree local SQLite adversarial tampering and do not purport to prove external cryptographic signatures. The problem is not that external tampering becomes impossible to detect—the full audit already detects it—but that read and append methods do not enforce their own audit's source preconditions.

**Bounded repair target:** In the existing `storage.ResearchLedger` owner, make the source read and append preflight reject noncanonical or hash-invalid source issuer envelopes *and* unauthorized source maps in non-source events, and preserve ordinary event chain ancestry. Use a complete source/chain verification under lock or an explicitly proven equivalent; do not turn last-event checking into a false whole-history guarantee. Re-run the five RED cases, original 276, -O, pytest, and SQLite cold reopen on new exact commit. Avoid native source-disclosure claims.

## Ledger and authority conservation

- R15 carries 73 P IDs, 53 original independently reviewed first-fault scoped records, 8 OPEN, 8 PARTIAL and four P070–P073 author-repaired pending distinct receiving. T=0, E=6. R15 first 71 P identity and statuses match the existing #1171 ledger HEAD `30f9ce0208bad066fe89231f0e25d75f56857700`; P072 and P073 are the two additional identities.
- Comparing frozen R14 parent to R15, 71/73 P structured records are identical; P012 and P018 differ only by new `r15_repair` annotations, **statuses unchanged**. No defect status is author-promoted here.
- P009 native privacy/source-disclosure authority still held. SORACLE psychological construction, PYAT whole-survey, human rights, original P070/P071 reviewer independence and production entitlements remain separate.
- Protected `integration/pre-main-reconciliation-r1` was `5d387a9a8c72c68e6ef87a671d6d486bfd1fc43e` on accession, unmodified. OATH read from same cut and paired protected `CURRENT_PROGRESS.md`/`.json` checked. No authorized writer lease or protected receiving established; **`HQ_CURRENTNESS_HOLD`** for canonical PROGRAMMA paired updates; send durable exact-source handoff to current REMONT and PROGRAMMA candidates instead. This hold does not prohibit bounded owner repair.

**Disposition:** P012 `ACCEPT_SCOPED_FIRST_FAULT`, P018 `REVISE_EXACT_DEFECT`, PR #1220 `REVISE_EXACT_DEFECT` overall, 3.11 `NOT_RUN`.
