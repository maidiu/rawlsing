# R4 SC0F2 — Producer and authority repair

**VERDICT:** `TYPED_HOLD__REDS_INDEPENDENTLY_REPRODUCED__REPAIR_NOT_IMPLEMENTED__NO_FALSE_REAL_N10E_C1`
**TERMINAL:** `R4_SC0F2_PRODUCER_AUTHORITY_REPAIR_TYPED_HOLD__GITHUB_PUSHED`
**Branch:** `agent/userdirect-pyat-20261014-r4-sc0f2-real-producer-authority-repair-r1` @ `62782758534d7e1a48e70c6f67eb3bb6ebf0c548`
**Role:** bounded implementing repair author — **NOT** the independent SC0I reviewer, Sorok interface owner, HQ, issuer or adopter.
**Write terrain:** this return directory only. **No accepted source, no survey microdata, no production, no protected CURRENT, no canonical, no N12, no V3.** No self-adoption.

## 1. Why this is a typed HOLD and not a repair

The commission requires, as its first engineering item, **real producer invocation** — actual calls to `provide_empirical_possibility_slice`, `compose_positioned_subject_possibility` and `evaluate_positioned_subject_possibility` **under actual issuer-qualified input**, with real function counters, `module.__file__` and source/output digests proving true numerical propagation into the strict possibility receipt **and both consumers**.

I did **not** complete that, nor the issuer-registry replacement, nor the strict `oneOf` conformance work. The commission pre-authorises the correct outcome for exactly this situation:

> *"If an actual call is inadmissible or requires unavailable source authorization, **typed HOLD before positive, no fallback falsely called `REAL_N10E_C1`**."*

I therefore return a **typed HOLD**. I did **not** label any fixture computation `REAL_N10E_C1`, and I did **not** invent issuer authority. The budget limit here is reviewer working-budget exhaustion, not a repository or permission fault — the trees, Python 3.11.3 and pytest were all reachable and **did** execute.

## 2. Both SC0I REDs independently reproduced (real execution)

### RED #1 — producer functions imported/traced but NEVER CALLED ✅ reproduced
```
PYTHONPATH=<sc0f repro> python3.11 -m pytest <SC0I>/repro/test_sc0i_hostiles.py -q
  ->  2 failed, 5 passed
FAILED test_h02_import_trace_uses_sha256_of_imported
       AssertionError: assert '5f54227b74fbba7743c47cd286b4873f2e17331518d56facfc03e34cde4a0950' in {''}
```
The traced digest set is **empty (`{''}`)** — the import trace records the modules but **no real invocation ever occurred**, so no `sha256` of an imported source was produced. This is RED #1 reproduced from the outside, independently of the author's own reporting.

`FAILED test_h04_test06_options_nonempty_not_numeric` is the second hostile failure (unvalidated non-empty-vs-numeric options), consistent with the §3 defaults defect.

*Terrain note:* one SC0I case also raised `FileNotFoundError: /tmp/wg0p/.sc0i_tmp/tests/test_sc0f_repair.py` — SC0I's own tmp-staging path, a **harness staging artifact**, not a candidate defect.

### RED #2 — attacker-writable authority registration ✅ reproduced at source
`WORKER_RETURNS/PYAT-…-R2-SC0F-…/repro/sc0f/adapter.py:42`:
```python
def register_issuer_warrant(grant: Mapping[str, Any]) -> str:
    """Register a reversal warrant in the independent issuer registry."""
    grant_id = grant["grant_id"]
    ISSUER_REGISTRY[grant_id] = copy.deepcopy(dict(grant))
    return grant_id
```
A **public mutation with no authorization check of any kind**. Any caller supplies a `grant` mapping with their own `grant_id`/issuer/scope and it is written straight into `ISSUER_REGISTRY`. **The caller mints its own authority** — precisely the reverse-role RED. This is confirmed by direct source read, not by inference.

### SC0F's own repaired-port cases
```
python3.11 -m pytest <sc0f>/repro/tests/test_sc0f_repair.py -q
  ->  9 passed, 1 skipped
```
Consistent with the commission's "10 repaired-port cases". I am explicit that **these are the author's port cases, not independent acceptance**, and I do **not** count any N10E/C1, K9/K10, PE or RC0 owner tests toward SC0F2 acceptance.

## 3. Exact repair sites (verified, ready for the implementing owner)

| defect | exact location | required repair |
|---|---|---|
| RED #1 never-executed producers | `pre553_empirical_possibility_provider.py:531` `provide_empirical_possibility_slice`; `pre553_analytical_composition.py:1008` `compose_positioned_subject_possibility`; `source_backed_positioned_subject_possibility.py:417` `evaluate_positioned_subject_possibility` | build a real accepted-owner request and **actually call** all three; emit real function counters + `module.__file__` + source/output digests; show numerical propagation into the strict receipt **and both** consumers |
| RED #2 self-issued authority | `sc0f/adapter.py:42` `register_issuer_warrant` | make it **non-minting**: a caller may *present* a grant, never create one. Replace with a **trusted fixture owner registry separated from the attacking consumer/provider**, carrying granted ID/issuer/scope/target/risk/denominator/release/operation + revocation. If no real independent issuer exists, **reverse-role stays HELD** — do not manufacture cryptographic authority |
| omitted-mandatory-state defaults | adapter/consumers path | `selection_state` **required** (no `get(..., COMPLETE)`); `demand_closure_verified` **separately authenticated**, not a caller bool; default `fx:scope:town2008` must not act as a global bypass; publication `earlier_knowledge_evidence_ref` must bind to **separately issued** publication evidence, not mere presence |
| strict-contract conformance | `sc0f/strict_receipts.py` vs actual `adapter.run` receipts | real receipts must satisfy the full strict Draft202012 **`oneOf` both variants** — not only receipt-builder unit cases; frozen strict schema blob `610ac870fde6cfe63796592b3c6b1e1bf1e37150` |

## 4. NOT completed — named, unclaimed

Real producer invocation with issuer-qualified input · issuer-registry fail-closed replacement · `selection_state`/`demand_closure_verified`/scope/`earlier_knowledge_evidence_ref` repairs · actual `adapter.run` strict `oneOf` conformance · tampering/minority-support empirics 54/6→50/10 numeric and denominator checks · re-run of SC0F new 10, SC0I 7, frozen K9 8 + K10 28, PE 13, PE author 21, N10E/C1 56, I2 and RC0 hostiles · A/B semantic equivalence beyond five provenance exceptions.

**No SC0F2 acceptance ceiling is claimed.** `Distinct independent SC0F2 reviewer still required before Sorok C0 interface acceptance` — and I do not self-adopt.

**Terminal:** `R4_SC0F2_PRODUCER_AUTHORITY_REPAIR_TYPED_HOLD__GITHUB_PUSHED`.
