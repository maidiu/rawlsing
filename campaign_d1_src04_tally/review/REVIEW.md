# D1 SRC04 observed-sample tally — independent review

**Verdict: `REVISE`.**

The tally product itself is real and independently reproduced from the accepted
local C11 event bundle: all 42 fields, 7,337 source records, state/value
partitions and global totals match. D1 is not yet accepted because the grant-required
held-authority negative is missing, the D1 primary/replay commands are not
portable in a clean checkout, and the source/ref mutation boundary is not guarded.
These are bounded adapter/evidence repairs; the observed-sample aggregate
`87e297bb…` remains valid at its stated descriptive grade.

## Exact identity

- Candidate: `b8f34be3b37bbc648e20b129d8f533c091206c32`
- Author branch: `agent/pyat-d1-src04-observed-tally`
- Review branch: `agent/pyat-d1-src04-observed-tally-review`
- Artifact/code commit: `adf1e81c6719132f1d889e96cf1a222a5f74fff1`
- TRUE-HQ D1/D2 grant: `f51de87818f8fd1365d347da3aee73005fe9ab8ae0c8d2a607487395016d48ae`
- Control commit: `3b703e878946a442b5c880f318b929365865ed00`
- A1 program: `9e292a10df7052afb6db503a96c4b1721472d9030ab33094f8681b6bc8e49b50`
- Accepted release: `fc111cfa78d0fc23b5c72c1dc4b45c39d35c66c394662d7b901f5422df3370ec`
- Source: SRC04, `2a48ba4b…`, 7,337 records, 181 columns, 42 accepted fields.

No original SAV was reread. The accepted local C11 bundle was consumed only for
independent aggregate verification; no respondent cells are in the product,
review files or Git.

## Independent result — product PASS at descriptive grade

The independent probe used the existing `materialize_public_object` carrier and
`R5TypedValueCodec.decode` value owners directly, not the author's `build_tally`
as an oracle. It read all 630,990 public objects and recomputed every selected
field:

| Check | Result |
|---|---|
| fields | 42 |
| held fields | 0 |
| event presence | 308,154 = 7,337 × 42 |
| observed response | 298,819 |
| substantive answered | 277,582 |
| DK | 14,784 |
| source-specific special | 6,453 |
| missing | 9,335 |
| refusal / invalid unresolved | 0 / 0 |
| observed + missing | 308,154 |
| per-field event/state/value/state-value partitions | all exact |
| product vs replay product | identical `d9d7f43b…` |
| tally ref | `87e297bb8795ae3628603a730c83ca0b90107556236c9e1cb7dba27858722022` |
| replay ref | `8c7205dc775fd9123ab09985e61b91671f38127e0ae22a6ae3d58e39dfd41b4f` |

The product does not treat event presence as an answered question:
`event_presence_count` (308,154), observed response (298,819) and substantive
answered (277,582) are distinct. DK and source-specific special are in observed
response; missing is excluded and separately counted. All fields are scalar
single-component response events, so no component/repeat identity was flattened.
`ROUTING_UNKNOWN`, `WITHHELD_DEFER_NO_SCIENTIFIC_ALLOW`, zero canonical values and
zero weight facts are preserved. The schema is
`PYAT_D1_SRC04_OBSERVED_SAMPLE_TALLY@1.0.0`, not an issued I03 EmpiricalFact.

## Demonstrated gaps — REVISE

### D1-D01 — held-authority negative missing

The D1 grant requires **wrong-release and held-authority refusals**. The return
has wrong-release and `UNKNOWN_RESPONSE_STATE`; the latter is a response-state
classifier refusal, not a held-authority refusal. No held-authority negative or
test exists in `campaign_d1_src04_tally/evidence` or `tests/`.

Minimal owner/repair: Campaign D1 adapter/evidence. Add a narrowly additive
negative through the existing authority owner for a DEFER/canonical/directional
or authority-gated request over the same exact release, recording the existing
refusal without changing `_risk_membership`, validators, predicates or
manufacturing an `EmpiricalFact`. Do not require a separate I03 issuance for the
typed D1 tally.

### D1-D02 — clean-checkout primary/replay fails

`run.py`/`adapter.py` hardcode:

```text
.r61/d1_src04_observed_sample_tally/TRUE_HQ_GRANT.txt
.r61/d1_src04_observed_sample_tally/PROGRAM.txt
```

That author-private path is absent in the review checkout, which has the exact
grant at `.r61/d1-review/TRUE_HQ_GRANT.txt`. Exact command:

```sh
PYTHONPATH=. python3 campaign_d1_src04_tally/run.py --mode primary
```

returned `RuntimeError: D1 TRUE_HQ_GRANT is absent`. The five focused tests pass
(0.13 s here; 0.27 s HQ; 0.11 s author receipt) because they only read the
committed product, but the claimed primary/cold-replay commands cannot run in a
clean checkout.

Minimal repair: use a committed pinned D1 grant/program evidence copy or an
explicit portable path; rerun primary/replay and update receipts. The product need
not be rebuilt if only path evidence changes.

### D1-D03 — source-mutated override is accepted

A private probe supplied `receipt_override` with `source_sha256 = 0*64`; the
adapter returned **ACCEPTED** with the unchanged tally ref and the constant
original source hash. The wrong-release hook checks only release identity, not
source/source-manifest override fields. Normal `build_tally()` uses the actual
receipt and remains correct, but the claimed malformed source/ref boundary is not
demonstrated.

Minimal owner/repair: Campaign D1 adapter negative hook. Verify source and
source-release-manifest override fields, or remove/narrow the override API; rerun
the wrong-source/ref negative and restoration. Do not change the native engine or
validators.

## Integrity, custody and limits

- 13/13 current `RETURN.json` artifact hashes match; `RETURN.json` SHA
  `08065806…`.
- Local bundle hashes: public `a47957a1…`, internal `2d9ea42a…`, replay
  `f13d893f…`, receipt `b1333a02…`; A receipt `4b18f500…`.
- Product/replay product byte-identical `d9d7f43b…`; replay receipt `1c4a048d…`.
- Only aggregate counts and exact refs are committed; respondent-level records
  remain local; no row cells in reports/Git.
- No original SAV reread, I03/I05 execution, canonical/directional/weighted/
  population/causal claim, M2/M3, F1–F4 or broader program completion is claimed.
  A properly issued I03 positive remains a subsequent separate obligation, not a
  requirement for this typed D1 tally.

## Next actual consumer

Existing descriptive aggregate consumer / independent reviewer. The product can
be consumed at the observed-sample descriptive grade after the three bounded
repairs; an I03 EmpiricalFact remains separately issued downstream and is not
claimed here.
