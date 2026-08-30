# PRE-MAIN RECONCILIATION R1 — W01 GLOBAL DAG

## FORENSIC CHECKPOINT — IN PROGRESS

**Jurisdiction:** topology only.  
**Authority adjudication:** forbidden here.  
**Worker branch:** `agent/rabochii-premain-w1-global-dag-r1`  
**Mandated starting HEAD:** `0777a34e50221bde6801dbaca26c058a7350c9e8`

This checkpoint is intentionally banked before the exhaustive ancestry reduction is complete. It must not be read as the final maximal-head court.

## Frozen census invariant

The immutable branch-ref observation captured for this court contains:

- **638 branch refs**
- **581 unique tip SHAs**
- therefore **57 refs of exact-tip alias surplus** before any strict-ancestry collapse.

The frozen observation, not later live branch tips, is the census authority for this R1 court. During continuation, several Wave-1 worker refs were observed to have advanced after the snapshot. Those later movements are contamination for census purposes and are not substituted into the frozen ref→SHA mapping.

## API-proved topology already closed

| base | head / comparison | Git relation | merge base | unique counts |
|---|---|---|---|---|
| `daffee545fc60a8cd635aee9aafbe77a920f4c19` | `163a562e7bef187d1b417c9c3130bf65deaa86b1` | strict ancestor → descendant | `daffee545...` | head +44, base +0 |
| `daffee545fc60a8cd635aee9aafbe77a920f4c19` | `66295cb4b07d1dce63d55a4fd5df080cf8c5e0a5` | strict ancestor → descendant | `daffee545...` | head +20, base +0 |
| `daffee545fc60a8cd635aee9aafbe77a920f4c19` | `44e97e420d38b6a2b0c44034929b5994a352d8b6` | strict ancestor → descendant | `daffee545...` | head +5, base +0 |
| `66295cb4b07d1dce63d55a4fd5df080cf8c5e0a5` | `44e97e420d38b6a2b0c44034929b5994a352d8b6` | **diverged / incomparable** | `daffee545...` | C06 side 20; J01-A side 5 |
| `46a9d35d0edecc7dc9182038baeb0d0748c50fdc` | `163a562e7bef187d1b417c9c3130bf65deaa86b1` | **diverged / incomparable** | `ab19862b9485741228dfa84f4c976c6110171065` | R5 side 9; later HQ/Field-Forge side 352 |

These are Git reachability facts only. In particular, the fact that `163a562e...` is +44 beyond `daffee545...` does **not** establish that it is a superior canonical base; canonicality is outside W01 jurisdiction.

## Reduction pipeline still open

The court is continuing exactly:

```text
638 refs
→ 581 unique tips
→ exact-tip collapse
→ strict ancestry collapse
→ maximal independent tip set
→ containment map
→ unresolved topology
```

Pending before this worker can return FINAL:

1. materialize the complete frozen 638-row branch census with frozen tip SHA and requested annotations;
2. enumerate every exact-tip alias class;
3. perform exhaustive strict-ancestry collapse across the 581 unique tips;
4. emit the exact topologically maximal independent tip set;
5. emit complete proved containment edges;
6. isolate the residual incomparable / ambiguous topology set.

## Non-conclusions

This checkpoint does not identify a pre-main base, does not classify living project capital, does not supersede `daffee545...`, does not dismiss the R5 shadow, and does not authorize Wave 2. Those are later courts.
