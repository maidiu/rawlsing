# PYAT HQ242 — F7 T1 NATIVE ACTUAL P07 OWNER IMPLEMENTATION — R1 RETURN

**DISPOSITION:** `F7_T1_NATIVE_P07_OWNER_PARTIAL__NAMED_API_OR_NATIVE_BLOCKER`
**BRANCH:** `agent/space-bunny-pyat-hq242-f7-t1-native-p07-owner-implementation-r1`
**COMMISSION TIP GIVEN:** `08f4c0a10a6095c81f40836a6426dd34bee55883`
**WORKED FROM:** `c4d46de7535359f0ebddc50ae5cad109124a4300`
**PRODUCTION MUTATION:** NONE · **SEMANTIC/AUTHORITY MUTATION:** NONE · **CONTROL MERGE:** NONE · **SELF-ADOPTION:** NONE

---

## 1. Bottom line — and why this is not an environment blocker

The commission said: *"Verify … compiler/build availability … before mutating. If native
build cannot be governed, RETURN BLOCKED rather than faking qualification or downgrading
requirements."*

**It can be governed, definitively.** I compiled and imported a real CPython C extension
under the governed interpreter. So `…BLOCKED__GOVERNED_ENVIRONMENT_OR_TCB_PROOF_MISSING`
would have been the dishonest call.

The real blocker is **scope/parity**, and I shipped no native module rather than ship a
forbidden shape.

---

## 2. Two tip facts, disclosed rather than assumed

**Tip discrepancy:** the commissioned `08f4c0a1…` is an **ancestor** of the branch tip.
One commit sits above it — `c4d46de7`, the **HQ243 routing correction** — which changes
exactly one line of the commission: it redirects the model identity to Space Bunny in
OpenCode and *forbids* relabelling as GPT-5.6 Sol High.

**I honour that correction.** The launch header's "GPT-5.6 Sol High" is superseded; I am
Space Bunny Max and did not relabel. I worked from the branch tip.

**Base witness blobs match exactly:**

| | observed | commission | match |
|---|---|---|---|
| F7 `pre553_temporal_comparability.py` | `6f6b462b1cde…` | `6f6b462b1cde…` | ✅ |
| P07 `pre553_source_relations.py` | `8053d30d306a…` | `8053d30d306a…` | ✅ |

No drift. Both F7 witness blobs verified.

---

## 3. Governed native build capability — verified, with receipts

| Item | Result |
|---|---|
| Python headers | present (`include/python3.11/Python.h`) |
| Compiler | Apple clang 14.0.3, `x86_64-apple-darwin22.6.0` |
| Extension suffix | `.cpython-311-darwin.so` |
| **Required macOS link flag** | `-undefined dynamic_lookup` |
| Probe source SHA | `217e3f31a50040f…` |
| Probe binary SHA | `4a4437065cc65e9f…` (49,536 bytes) |
| Import result | `native-ok` |

A naive link **fails** with undefined `_PyModule_Create2` / `_PyUnicode_FromString`; the
`dynamic_lookup` flag is required. Recorded because a future lane will hit it.

**No binary was shipped into the repo.** The probe lives only in the governed local
worktree.

---

## 4. The named blocker — `HQ242-NATIVE-BLOCKER-001`

**`FULL_P07_ADJUDICATOR_NATIVE_PORT_NOT_COMPLETED_OR_PARITY_VERIFIED`**
— engineering scope/parity risk, **not** an environment blocker.

A non-subclassable C owner with one-shot sealed custody is buildable here. But the
mandate is the **full** adjudicator over native-owned material: 12 decision states, the
`CONFLICTING_AUTHORITY` precedence ladder, exact-key relation-key derivation, authority
positivity adjudication, custody hash and replay identity — **~300 lines of Python to
port faithfully**.

Faithful parity requires either:
- reimplementing canonical-JSON + `semantic_hash` in C with byte-exact agreement, **or**
- calling trusted Python `canonicalize`/`semantic_hash` from native code at decision time.

The commission *permits* the latter ("Preserve only explicitly trusted canonical semantic
hash functions"). Neither route was completed **and verified** here.

### Why I did not ship a partial native module
Every partial shape is either forbidden or worthless:

- **Custody-only capsule** → explicitly forbidden ("must not be a Python wrapper holding a
  caller-replaceable capsule/handle").
- **Keep the Python owner as decider** → violates "no duplicate Python owner capable of
  positive decisions" and "no Python fallback that can authorize".

So a partial artifact would be **architecturally non-compliant, not merely incomplete** —
and shipping it would have consumed the honest PARTIAL disposition for a shape HQ would
have to reject.

---

## 5. Baseline evidence (real, not native-path results)

| Evidence | Result |
|---|---|
| targeted courts (F7 163 / P07 24 / M1 41) | **228 passed**, exit 0 |
| broad regression, 9 environmental exclusions | 45 failed / 2691 passed / 7 errors |
| **normalized FAILED/ERROR** | **54** |
| **normalized digest** | `278854ee94fadfd57284a572441522fb56105081f89af431b17ec2e556ace6a9` |
| required digest | identical — **verified** |

Pre-existing failures unchanged, neither hidden nor masked.

### Hostile status at the pinned base — baseline only
- **V0** empty victim → `TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT` (no mint)
- **V1** HQ234 one-cell ledger rebind → **refused** (the ledger cell seam was recovered
  and exercised; this is not a green from a missing helper)
- **V2–V4** not re-measured in this lane

**No native-path coverage exists.** I am not claiming any forgery fails on an actual
native path, because no such path exists. That would be exactly the no-coverage green the
commission forbids.

---

## 6. What a full completion requires

1. Non-subclassable heap type, one-shot C-memory custody sealed at construction.
2. Deep copy + validation of all relation/snapshot material into C-owned canonical bytes.
3. Native by-ref/by-key maps, exact-key-only lookup.
4. Faithful native port of the decision/validate/resolve/replay chain.
5. Documented trusted-Python TCB calls **or** byte-exact C reimplementation.
6. Adaptation of **3,577 lines** of introspection-coupled tests that reach `__closure__`,
   `cell.cell_contents` and resolver method monkeypatching — preserving adversarial intent
   without deleting hard tests.
7. Byte-exact parity vs the accepted Python owner on all 12 states + 5 productive paths.
8. Four hostile variants re-run on the **actual native** path.
9. Non-shippable native binding fail-capability + separate build manifest.

---

## 7. Recommendation

Re-dispatch with the adjudication-parity work split into sequenced sub-lanes:
**(a)** native custody + exact resolve → **(b)** native decision port with a parity
harness → **(c)** test adaptation → **(d)** hostile re-run and fail-capability.

The environment is proven capable and is not the obstacle. The obstacle is that the
mandate's *correctness bar* — byte-exact parity across 12 states plus hostile closure — is
materially larger than the "write a native capsule" framing, and shipping an unverified
parity claim would repeat the exact failure mode this entire F7 sequence exists to prevent.

`HQ242_F7_T1_NATIVE_P07_OWNER_PARTIAL__NAMED_API_OR_NATIVE_BLOCKER`