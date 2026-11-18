# R3 FALSIFIERS AND COST — minimal decision-changing witnesses

**Status:** analytical/documentary. No native/100k/6 GiB run, no new benchmark.
Existing sourcefree tests are cited only where already executed; no new test was
needed in this pass.

## 1. Finite design falsifiers

### F1 — Same pairwise marginals, different true k≥3 joint

Input: same universe/risk/weights; two synthetic/sourcefree respondent sets
with identical univariate and pairwise marginals but disjoint true triple
support (even parity `000,011,101,110` vs odd `001,010,100,111`; equal counts).
Expected: native F4/`AnalyticalCompositionResult` returns different joint
support/P(111); a pairwise substitute returns the same result and must be
refused.
Counterexample/negative: pairwise product accepted as F4; exact restore must
reproduce the true joint.
Grade: sourcefree executable specification; no native claim.
Affected: F1–F4, K1-CAP-11, T2, S-01.

### F2 — Forward vs reverse conditional risk bases

Input: same condition/target question pair, forward `P(Y|D)` and reverse
`P(D|Y)` with different eligible/asked/observed/routing bases; include a
NOT_ASKED case and a routing-unknown case.
Expected: two different exact denominators; NOT_ASKED is not zero; one
denominator reused for both must refuse.
Negative: reverse denominator computed as algebraic inverse of forward.
Affected: F2, K1-CAP-05, T2, S-02, L-03/L-06.

### F3 — Minority/recursive/ranked occurrence

Input: ordered k≥3 pattern with a minority branch, repeated/ranked events, a
recursive parent/child branch, and typed missing/inapplicable.
Expected: minority/recursive result and occurrence topology preserved; no
first-value pivot; fixed I05 frontier not pruned by result diagnostics.
Negative: pairwise summary or first-value selection erases the minority/repeat.
Affected: F3/F4, I05, K1-CAP-03/06/11, S-02.

### F4 — Observed respondent category vs unreleased design stratum

Input: a source frame with religious/sect/ancestry sample strata but no
released respondent-level field; a party/religion/geography proxy; an external
group estimate.
Expected: `SAMPLE_DESIGN_ONLY`/`EXTERNAL_GROUP_CONTEXT`/`PROXY_OBSERVED` remain
distinct; no individual sect/ancestry assignment; F4 only over observed same
respondent fields.
Negative: stratum or external group estimate becomes respondent identity;
unreleased field becomes observed; proxy becomes measured identity.
Affected: L-01/L-04/L-08, S-06, T1/T3, K1-CAP-08.

### F5 — Different waves/universes and non-comparability

Input: two valid releases with different question wording/options/routing/time
and a same-name variable; one overlapping and one non-overlapping population.
Expected: separate C11 universes; F7 comparison only under exact authority;
numeric uncovered mass and nonpooling refusal for non-comparable inputs; no
individual longitudinal row.
Negative: same-name variable treated as measured trajectory; cross-sections
joined into a pseudo-person; pooling without authority.
Affected: F6/F7, L-05/L-08, S-06, K1-CAP-17.

### F6 — Independent material power changed, survey answers fixed

Input: identical survey answers/FF01 configuration; change only independently
evidenced institutional/legal/economic control (FF02/N9 material).
Expected: FF01 remains unchanged; only the qualified FF02/world option changes,
and only if the owner actually consumes it.
Negative: survey opinion frequency becomes institutional power; FF01 relabeled
FF02; group majority becomes coercion.
Affected: FF01/FF02, N9, K1-CAP-08/23, S-04, T4.

### F7 — Other positions changed, encounter data absent

Input: same selected person's joint configuration; different qualified
distribution of other positions/configurations; no observed encounter/contact
data.
Expected: potential Other configurations may change; actual relationship/
encounter remains an exact hold; actor private knowledge does not change.
Negative: position marginals treated as evidence people meet/marry/dominate;
encounter probability invented; offscreen event becomes actor knowledge.
Affected: S-03, SEAM/SOROK, N10W, T5/T6, K1-CAP-23.

### F8 — Exact fact/membership sharing, revocation and root change

Input: same sourcefree fact membership under identical release/condition/
measure/routing vs changed forward/reverse, weighted/unweighted, missing/
routing or wave; then revoke a member or change the root.
Expected: identical identity may share a content-addressed set ref; any changed
identity gets a separate set; replay re-executes and matches exact fact refs;
revocation/changed root refuses.
Negative: shared ref across F2 directions/weights/waves; cached fact served
after revocation; journal-derived Q2 accepted as independent proof.
Affected: H/S/Q/O, T2, REQ-EVIDENCE-OUTPUT-EXACT-IDENTITY, REQ-SOURCE-I02-
REVOCATION.

### F9 — Cold 1/10/100 and high-width output (future qualification)

Input: one authorized real-width workload; 1/10/100 distinct issued operations
same-process and 10 fresh-process opens; high-width F4/FF and I05 multi-role.
Expected: report H, S, Q, O separately; process-tree RSS, retained, scratch,
output; exact facts/replay; no fabricated PASS.
Negative: 1.69–1.70× four-op author report extrapolated to 100; sparse canary
called dense 100k; 20/118 structural guard called science.
Status: **NOT RUN**; owner `#1006` + S04/I03.

## 2. H/S/Q/O cost model

Let `N` = distinct operations; `H` = cold admission (manifest/I02/member/
current); `S` = session index build; `Q` = per-operation native counting;
`O` = evidence/replay output; `I` = durable index validation.

| Pattern | Formula | Consequence |
|---|---|---|
| one-shot per operation | `H + N(S+Q+O)` | S paid per operation; Batch per-unit current path |
| prepared same-process | `H + S + N(Q+O)` | removes repeated S only; neutral at N=1 |
| truly fresh per operation | `N(H+S+Q+O)` | prepared session does not help |
| durable index | `H + I + N(Q+O)` | only route to remove fresh S; needs binding/invalidation |
| typed/columnar pushdown | `H + I + N(q+O)`, `q<Q` | only if Q measured dominant; exact candidate streams |

**Cited sourcefree witness:** writer 3033.723 s; retained 310.16 MB; staging
5.26 GB; temporary I02 4.39 GB; session index 1.30 GB; selected query 562.362 s.
These are cite-specific and not RSS or native 100k. A 3.245-event/respondent
canary is sparse, not dense 600–1,300-slot width.

**Evidence output:** 2×100,000 refs at 150–250 bytes = 30–50 MB per fact before
provenance; 100 facts = 3–5 GB. Actual cardinality/serialization is unmeasured.
Exact set-ref sharing is required only under identical population/condition/
routing/measure/wave; replay re-executes; cached facts are never authoritative.

**Durable index:** 1.30 GB SQLite witness is ≈4.19× the 310.16 MB estate. It
must pass a retained-size gate and invalidation/rebuild economics; not selected
now.

## 3. What would reverse the design choice

1. A bounded proof that the 13-family body loses a required native/occurrence/
   routing/time/weight distinction not recoverable from source/C11.
2. A measured `S ≫ Q+O` on a real-width workload with a compact exact index
   that beats the 1.30 GB witness and passes binding/invalidation.
3. A measured `Q` dominance requiring exact typed pushdown into the native
   evaluator; then a separate S04/I03-qualified accelerator, not a second
   evaluator.
4. A measured `O` dominance requiring owner-approved versioned set-ref
   compression while preserving v1 facts/replay.
5. Failure of source-derived Q2/full physical proof; then keep the second
   certificate and withdraw the one-certificate claim.
6. Any demonstrated source→actor, opinion→power, fictional→observed or
   pairwise→joint promotion; then refuse and correct the affected route.

## 4. Non-claims

No native original35/100k/6 GiB/1–10–100 pass; no new execution; no
source/science/actor authorization; no protected adoption; no whole-future
guarantee.
