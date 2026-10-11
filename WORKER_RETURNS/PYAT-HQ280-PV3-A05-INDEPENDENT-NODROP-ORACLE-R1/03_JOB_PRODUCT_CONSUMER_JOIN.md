# HQ280 PV3 A05 — job / product / consumer join

## 1. The five-set reconciliation

```
E  independently expected operations   (external frozen; the ORACLE's own set)
J  constructed jobs                    (producer-submitted)
R  typed results                       (per attempt)
A  released products                   (per job)
C  required consumers satisfied        (per product)
```
plus three always-visible non-runnable classes: `H` held, `D` denied, `NA` source-intrinsic non-applicable.

## 2. Join law (what must hold for PASS)

For every `e ∈ E`:

1. exactly one job with `expected_work_key == e` exists in `J` (**no omission, no multiplicity**);
2. **no** job exists in `J` whose key is not in `E` (**no unauthorized work**);
3. that job yields exactly one typed result in `R`, and the type is honest: a null is admissible **only** when genuinely measured, and `PARTIAL`/`UNVISITED`/`UNAVAILABLE` can never be reported as success;
4. that job yields a released product in `A`;
5. that product has its **required consumer** satisfied in `C`, matched on `(expected_work_key, consumer)` — a product with a missing consumer is a **failure**, not a partial success.

Separately, for every row in `H ∪ D ∪ NA`: it must appear in the manifest's visible documentary-item list, and its `expected_work_key` must **never** appear in `J`.

## 3. Why an outer join is mandatory

An inner join (`E ⋈ J`) silently discards exactly the cases the commission cares about. The oracle therefore performs the **outer** reconciliation explicitly:

- `E \ J` → `EXPECTED_OPERATION_OMITTED` (T1, T2, T4 — this is the "local tests still PASS after a valid expected B or J2 was excluded upstream" case);
- `J \ E` → `UNAUTHORIZED_EXTRA_JOB` (T3, and the extra half of T5);
- `A` present but `(key, consumer) ∉ C` → `REQUIRED_CONSUMER_OMITTED` (**T10** — the decisive consumer-side case: job counts, result types and products are all correct, and the run still fails);
- `H ∪ D ∪ NA` excluded from the manifest → `HELD_OR_DENIED_WORK_NOT_VISIBLE` (T11b — a holder schedule that omits held work cannot report no-drop).

## 4. Same-count / different-key substitution

T5 replaces the four expected keys with four fabricated keys of an identical total count and gives every one a positive typed result and a product. Job count, result count and product count all match the honest run; the oracle still fails on both `E \ J` and `J \ E`. **Count equality is not set equality**, and no completion ratio computed from counts alone can detect this class — it requires the frozen key set.

## 5. Consumer obligations are first-class

`C` is a set of `(expected_work_key, consumer)` pairs derived from `E` itself, never from the manifest. This is what makes T10 detectable: the producer can report every product as released and still be caught on a single missing consumer. Consumer satisfaction is therefore **not** inferable from job or product counts, which is precisely why the commission asks for it separately.

## 6. Order invariance

T13 reverses `J`, `A` and `C` and must still PASS. The oracle compares **sets**, so a stable reordering of an otherwise correct run is not a failure — this guards against a spurious "no-drop" that depends on emission order, and against the opposite error of flagging a legitimate reorder as an omission.
