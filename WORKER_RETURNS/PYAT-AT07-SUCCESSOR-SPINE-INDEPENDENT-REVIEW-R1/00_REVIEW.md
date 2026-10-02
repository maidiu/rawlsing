# AT07 SUCCESSOR SPINE — INDEPENDENT ORACLE REVIEW — R1

Disposition: `APPROVE_AT_DECLARED_GRAIN`

Reviewed object: the AT07 successor-spine oracle package only.
Oracle return head: `92ddee2241a78b46394665d325e5ebf0e75adf40`

The oracle is independently derivable from pinned law and frozen inputs. No blocking
counterexample remains.

## 1. Provenance and terrain

Every commissioned fact verified:

- the oracle return head is `92ddee` (this review branch's HEAD is the HQ165 commission
  bind `d6cfce73`, whose parent is `92ddee`);
- movement confined to
  `WORKER_RETURNS/PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1/**`;
- **zero `rawlsing_next/**` files changed** by either oracle commit;
- `79a3b7e5` carries the core artifacts and `92ddee` differs by exactly
  `09_EXECUTION_RECEIPT.json`.

**All 24 pinned INPUTS verified independently** — I compared `git rev-parse <ref>:<path>`
against each stated blob and recomputed SHA-256 myself. **24/24 match, 0 mismatches.**
I did not rely on the worker's table.

## 2. Independence — the contamination attack

| contamination path | present |
|---|---|
| imports/executes production composition | **No** — imports only `argparse, ast, copy, hashlib, json, fractions, pathlib` |
| calls `identity_material()` | **No** — the two textual hits are `ast.parse` of *pinned source text* to enumerate field names |
| calls provider/consumer production path | **No** — zero occurrences of the three entry points |
| copies the disclosed forward digest | **No** — zero occurrences |
| reads a precomputed reverse digest | **No** — zero occurrences |
| derives truth from candidate output | **No** — successor = historical(38) + six **owner-default** values |

**The strongest evidence is the reverse direction.** The commission disclosed only the
forward candidate observation. The reverse successor
`a3bd7e85ae14babb5ac5a12b0bcc57a8cdf3eccf8f43394895903dc43aca40ca` was **never
disclosed to me**, and I reproduced it blind. Agreement on an unannounced value cannot
be explained by fitting to candidate output.

## 3. Field law — reconstructed by me, not trusted

From the two owner blobs directly:

```
historical direct fields : 38
current   direct fields : 44
removed                : 0
added                  : exactly the six commissioned
```

A naive AST walk first gave 41/47 because it descends into nested dicts, and a
parent-based heuristic gave 47 current because the adopted owner binds the nested
`producer_result_envelope` via an intermediate variable. I enumerated only the direct
returned/assigned dict — the correct notion of a *direct* composed field.

Nested witness evolution is preserved as nested: the 16-field
condition-binding-witness preimage evolves and feeds `consumer_binding_fingerprint`
without becoming a new top-level field.

The six lawful AT07 values come from the **adopted owner's own dataclass defaults**
(blob lines 376–381) plus the AT07 law that a single direct composition has no
discovery, no recursive handoff, no joint component. The package agrees.

## 4. Hash reconstruction — the core

Using my own canonicalizer (stdlib JSON, `sort_keys`, compact separators,
`ensure_ascii=False`, `allow_nan=False`, sha256/utf-8):

**Step 1 — anchor.** The R8 summary spine carries only 10 keys, not the 38-field
preimage, so I anchored the package's historical preimage against the independently
frozen R8 digests. Both reproduce exactly (forward `03610f9d…`, reverse `1202822c…`).
**The base is therefore anchored to a prior independent commission in both directions.**

**Step 2 — derive.** historical(38) + the six owner-default values:

```
forward  mine = 01c381d3f3c386cfc22fd2f57b8e2c244771ddf1529d4f8ab8c7b1cf41bd50dd  MATCH
reverse  mine = a3bd7e85ae14babb5ac5a12b0bcc57a8cdf3eccf8f43394895903dc43aca40ca  MATCH
```

Both distinct from their historical digests. Content verified too: denominators 60/62
match the AT07 source law, per-direction consumer queries and witness refs differ, and
the 16-field witness preimage is present with custody.

**No missing or ambiguous field.** The expected preimage is fully determined from
frozen inputs and law, so a matching hash here is a derivation, not a blessing.

## 5. Procedure rerun — my environment, not the producer's

Run in a **scratch copy** so the committed artifacts were never executed in place:

| mode | exit | seconds |
|---|---|---|
| generate | 0 | 0.249 |
| verify | 0 | 0.205 |
| hostiles | 0 | 0.467 |

All **41 package artifacts reproduced byte-exactly**; **0 frozen inputs mutated**; R8
evidence untouched. My interpreter is **3.12.14**; the producer's was **3.11.3** — a
different environment producing identical bytes.

## 6. Hostiles — substantively reviewed, not accepted on count

44/44 rejected, 0 false accepts, confirmed by my own rerun. Verified by enumerating case
ids per category and per field:

- **OMIT** for each of the six, both directions (12)
- **WRONG_VALUE** for each of the six, both directions (12)
- release, source-universe, witness, authority, serialization, key-order, array-order
  mutations; `OLD_OWNER_AS_CURRENT`; five frozen-input blob mutations

The mechanism is sound: content hashes are **re-derived** from mutated material, and
the hostile wrapper raises `HOSTILE_FALSE_ACCEPT` if a mutation fails to raise.

**My three review-only probes:**
1. changing any one of the six moves the digest in both directions — all load-bearing;
2. omitting any one moves the digest — no silent default;
3. tampering `joint_component_count` to 99 while leaving the expected SHA unchanged
   re-hashes to `c86cb726…` and the bytes differ — a stale checksum cannot pass.

## 7. Historical conservation

- R8 pinned copy is **blob-identical** to the R8 artifact at its origin commit
  `9e2655818` (`462bb282…`), and both historical digests reproduce.
- 38 shared fields **canonically equal in each direction; not one value changed**.
- Successors are **distinct versioned identities, never aliases**.
- No adoption claim: status is `PASS_…__INDEPENDENT_REVIEW_REQUIRED`, `self_adopted`
  is `false`, and downstream AT17 identities are explicitly "Not computed".

## 8. Execution provenance

Producer receipt fully reconciles: artifact commit `79a3b7e5`, clean tree before and
after, Python 3.11.3, three commands exit 0, 44 rejected / 0 false accepts, final head
one receipt-only commit later.

## Two informational residuals (non-blocking)

**R-1.** The R8 package is absent from this lineage's working tree, so "R8 unmodified"
could not be tested by diffing live R8 files. I proved conservation positively instead
— pinned copy blob-identical to origin, and both historical digests reproduce.

**R-2.** My first automated "already current" keyword scan flagged `adopted`. Inspection
showed the only occurrence is the `adopted_owner_blob` identifier, not an adoption claim.

## Scope

No implementation, AT17/N10E, or C1-03 join modification. No production candidate
comparison used as acceptance evidence. No raw sources. No model/comparability
authority broadened. No self-adoption. No new review layer.

## Terminal

`AT07_SUCCESSOR_SPINE_INDEPENDENT_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`
