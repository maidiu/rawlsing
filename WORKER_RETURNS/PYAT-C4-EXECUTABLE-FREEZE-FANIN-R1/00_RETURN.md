# PYAT C4 — Executable freeze fan-in — R1

**Disposition: `PASS_C4_EXECUTABLE_FREEZE_FANIN__READY_FOR_INDEPENDENT_REVIEW`**

Terminal: `C4_EXECUTABLE_FREEZE_FANIN_RETURNED__INDEPENDENT_REVIEW_REQUIRED`

Branch `agent/opencode-pyat-hq179-c4-executable-freeze-fanin-r1`, commissioned tip `012569770c551aca60c16eb20482c3435399c5d1`, C4A base `8f7efe690`. No self-adoption.

## Result

| Condition | Status |
|---|---|
| **O1-C01** combined tree | `CLOSED_BOUND` — 13/13 pinned blobs exact |
| **O1-C02** workload | `CLOSED_BOUND` — 8 sources, 0 substitutions |
| **O1-C03** oracle custody | `CLOSED_BOUND` — D2P closed C4B's sole blocker |
| **O1-C04** D02 | `CLOSED_BOUND` — subclass observed, not inferred |
| **O1-C05** runtime | `CLOSED_BOUND` — reader-lane law mandatory |
| **O1-C06** warrant | `CANDIDATE ONLY — NOT ISSUED` |
| O1-C07 / C1-C08 | Frozen before warrant |
| O1-C09 / O1-C10 | Preserved, 280 cells verified |

**16/16 source-free checks pass. 34/34 imported evidence blobs exact. Zero production blobs changed. Zero raw-source access.**

## Integration: two different lawful methods

The commission offered two, and the inputs genuinely differed — so I used both and recorded why.

**C4C3 merged (method 1).** It is a clean descendant of `8f7efe690` with merge-base *exactly* `8f7efe690`, so a merge was lawful and added only its return directory.

**C4B and D2P imported by exact path/blob (method 2).** Neither is a descendant of the combined tree — C4B forks from `149c3d263`, D2P from `dc94857de`. Merging either would have dragged in unrelated ancestry. I verified **every one of the 34 imported files is byte-identical to its blob at the pinned source commit** before committing.

`rawlsing_next` tree hash is `b0c1ab472cde033e21f1c2f63fbcbea2f0cccef0` at C4A and at head — **identical**. Zero production blobs changed at any point.

## The precondition C4B left open is now closed

C4B froze on the **C1-only base** and recorded `g01_owner: ABSENT`, with stale decoder/codec blobs. It stated a precondition: the execution head must carry the accepted C3 blobs. I verified all three are now **present and exact**:

```
g01_owner        31a9afd7…  ✓
physical_decoder d3d828c1…  ✓   (C4B saw d2a074a4… on its own base)
r5_codec         6000a170…  ✓   (C4B saw 72f8f3c0…)
```

That is not drift — it is a stale-base observation superseded by the C4A tree.

## Three judgement calls worth flagging

**The O1-C07 accounting warning.** The freeze binds "exactly one governed fresh full Route-B pass" for SRC27. That is a **workload** constraint, not an access constraint. The run will need at minimum an existence check, a full hash pass, a metadata read, and a full compatibility read. I recorded that explicitly, because reading "one pass" as "one file open" is precisely the accounting error Omega-1 forbids. I also set every per-source retry budget to **0** — C4B froze immediate-stop-on-mismatch, so no permitted variation remains that a retry could legitimately explore. I did not invent a more permissive budget.

**The Route-B producer is fan-in-observed, not C4B-frozen.** C4B's authority freeze names the facade, composition, provider, consumer, lifecycle and replay owners — but **no Route-B producer**. I bound `pre553_route_b_production.py@2385cd32…` and flagged it for HQ confirmation rather than presenting it as a C4B binding.

**An authoring error I fixed rather than shipped.** In artifact 06 I mistyped the historical C3 freeze hash and then "corrected" it inline with a note. That is exactly the pattern I criticised in others, so I replaced it with the correct value and verified it against the C4C3 source of truth. All 11 inherited reader defaults in my freeze were then checked one-by-one against C4C3 — **11/11 agree**.

## O1-C04: observed, not inferred

C4B required `observed_native_subclass: null` until real execution. C4C3 then measured it on the qualified anchor using a **synthetic** SAV date variable: arrival is built-in `datetime.date`, carrier `python.datetime.date@1`, pandas dtype `object`.

The decisive control is `dates_as_pandas_datetime=False` — never passed by the repo, and now frozen. Had it been `True`, the `date@1` carrier would not have held. And the retained rendering `1582-10-13` is **not** used to infer the subclass anywhere. What SRC14's real `v372` produces remains a warrant-time observation.

## O1-C06: the warrant is emitted, not issued

Status is `CANDIDATE_ONLY__NOT_ISSUED__NO_RAW_ACCESS_AUTHORIZED`, signed false, authorises nothing, SHA `d57420f80…`.

All seven access-locator slots are **`SOURCE_LOCATOR_FILL_REQUIRED_BEFORE_WARRANT_ISSUANCE`**. C4B's template carried the placeholder `<TO_BE_SUPPLIED_ON_AUTHORIZED_EXECUTION_SURFACE>` for every source. I did **not** search raw storage to fill them — commission line 470 forbids exactly that, and it would have meant touching raw source before any warrant exists. Per line 502, a typed fill-in does not invalidate the source-free freeze.

I **did** resolve the other placeholder: C4B's `<HQ_TO_BIND_EXACT_RUNTIME_AND_C3_EQUIVALENT_HEAD>` is now bound to the real execution-surface identifier.

## Carried forward unchanged

`C2-EPCLASS-PAYLOAD-001` = `UNRESOLVED__NOT_MISSING_PROVED`. The C1 single-fresh-process bridge limitation stays `OPEN__NONBLOCKING`, and I recorded the **forbidden** single provider→consumer→lifecycle bridge rather than gluing it. C7 stays `HELD` — the EVS pair is physical-only and WVS is retained, so C4 completion alone does not unlock it.

The two recorded-but-unverified identity labels (`3fab15f3…`, `f264dd8f…`) stay **labels**. The checkpoint **document** SHA plus the accepted packet are the real custody binding.

## Honest limits

I did **not** verify the 3.4 GB checkpoint SHA — the document is not on this estate. Nor the 120 giant EmpiricalFact deferred digests, nor byte-reproducibility of the D2P extraction. Those remain checkpoint-side and are listed as open items rather than glossed.

Also open for HQ: no dependency lock exists in the repository, and the framework `python3.11` launcher is a zero-byte file — any future surface identity check must verify an actually-executing interpreter, not a PATH entry.

## Next step

One consolidated independent integration review of this exact freeze, **before** any source warrant is sought. This PASS authorises no raw execution, no fresh decode, no warrant issuance, no C7, and no adoption.

**0 raw-source operations · 0 production blobs changed · C4 not executed · 0 live readers rerun · no self-adoption.**
