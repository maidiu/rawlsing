# PYAT HQ188-B — Return: current C4 consolidated claims and external decision packet

Lane: **PYAT HQ188-B — Current C4 consolidated claims and external decision packet — R1**
Role: **RABOCHII / documentary forensics — Space Bunny**
Repository: `maidiu/rawlsing`
Worker branch: `agent/rabochii-pyat-hq188-b-c4-current-consolidation-r1`
Commissioned startup SHA: `9001be646305036e493eea3dbce427f62f91c9ae`
Commission base: `6820160533859cf8dd283d10c043947dfe1dd5d4`
Subject artifact: C4 executable freeze `8ff40d37de69db2d8a6053a7c2242f481677f1a4`

## Final disposition

`CONSOLIDATION_READY_FOR_HQ_REVIEW`

Not `MATERIAL_CONTRADICTION_FOUND`. Eighteen crosschecks were run; every
tension resolved against the inspected artifact. Two prior positions were
*refined* rather than overturned, and neither refinement changes a stage
count, an authority basis, or a hold. Four items remain open and are recorded
as HQ calls.

## Return identity

| Field | Value |
|---|---|
| Branch | `agent/rabochii-pyat-hq188-b-c4-current-consolidation-r1` |
| Commissioned startup SHA | `9001be646305036e493eea3dbce427f62f91c9ae` |
| **Sealed candidate commit (all commissioned work)** | **`e9bc84b2eed39e0023f856ae1351db3b24b535b6`** |
| Final remote SHA (verified `local HEAD == origin/<branch>`) | `e9bc84b2eed39e0023f856ae1351db3b24b535b6` |
| Final disposition | `CONSOLIDATION_READY_FOR_HQ_REVIEW` |
| Terminal | `HQ188_B_C4_CURRENT_CONSOLIDATION_RETURNED__HQ_REVIEW_REQUIRED` |
| Terminal addition | `HQ188-B_REMOTE_BRANCH_RETURN_VERIFIED` |

**Return verification performed:** the worker branch was pushed to `origin`,
re-fetched, and `local HEAD` was confirmed equal to
`origin/agent/rabochii-pyat-hq188-b-c4-current-consolidation-r1` at the single
exact full 40-hex SHA `e9bc84b2eed39e0023f856ae1351db3b24b535b6`.

A commit cannot contain its own SHA. The seal commit — this document's
successor, which is the branch tip — records the sealed candidate SHA above,
which is the commit carrying all ten commissioned artifacts. Verify either at
any time with:

```
git rev-parse origin/agent/rabochii-pyat-hq188-b-c4-current-consolidation-r1
git log --oneline -2 origin/agent/rabochii-pyat-hq188-b-c4-current-consolidation-r1
```

---

## 1. What was commissioned and what was produced

The commission asked for the **single current C4 technical consolidation**,
superseding the historical OPS-04 `00`/`01` packets as an operational summary
**without modifying their bytes**, plus a machine-readable claim/evidence map
and a narrow external packet for the one reserved C4 decision.

| Deliverable | Path |
|---|---|
| Current consolidated claims | `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/OPS-04/02_CURRENT_CONSOLIDATED_DECISION_CLAIMS.md` |
| Claim/evidence map (33 claims) | `…/OPS-04/03_CURRENT_CLAIM_EVIDENCE_MAP.json` |
| External Astra packet (md) | `…/OPS-04/04_EXTERNAL_ASTRA_C4_DECISION_PACKET.md` |
| External Astra packet (json) | `…/OPS-04/05_EXTERNAL_ASTRA_C4_DECISION_PACKET.json` |
| This return | `WORKER_RETURNS/PYAT-HQ188-B-C4-CURRENT-CONSOLIDATION-R1/00_RETURN.md` |
| Input/supersession map | `…/01_INPUT_AND_SUPERSESSION_MAP.json` |
| Claim crosscheck (18) | `…/02_CLAIM_CROSSCHECK.json` |
| Stage register | `…/03_STAGE_REGISTER.json` |
| External packet self-audit (29 checks) | `…/04_EXTERNAL_PACKET_SELF_AUDIT.json` |
| Final disposition | `…/05_FINAL_DISPOSITION.json` |

Ten files written. Zero writes outside the commissioned terrain. OPS-04 `00`
and `01` are byte-untouched; `HQ_HANDOFF/**` is untouched; no historical worker
return was altered; production is untouched.

## 2. Startup compliance

- Explicit `git fetch origin` — no blind `git pull`.
- `origin/agent/rabochii-pyat-hq188-b-c4-current-consolidation-r1` resolved to
  **`9001be646305036e493eea3dbce427f62f91c9ae`**, matching the commissioned
  startup SHA exactly. No mismatch, so no stop-before-editing was required.
- Isolated worktree created at exactly that tip; local `HEAD` and the remote
  branch both verified equal to it; zero unrelated uncommitted changes.
- All three commission files read from that exact fetched tip.
- Control branch was **not** merged in. Evidence outside the worker ancestry
  was read by exact ref only, as `02_STARTUP_GIT_PROTOCOL.md` permits.

Startup terminal: `HQ188-B_GITHUB_STARTUP_VERIFIED`

## 3. The findings that matter

### 3.1 The distinction the whole record turns on

**M01 named-file identity is real.** All four named producer/carrier/test pairs
are byte-identical between the qualified candidate `46f3bec82` and the freeze.
The final court binding at `74a06774` names that candidate.

**M01 transitive-closure identity is not established — and is demonstrably
false for exactly two modules.** I computed the transitive import closure of
the two bounded-court suites myself:

| | At `46f3bec82` | At freeze `8ff40d37d` |
|---|---|---|
| Closure size | **23 modules** | **23 modules** |
| Membership | *identical set* | *identical set* |
| Byte-identical | — | **21 of 23** |
| Differing | — | **2** |

The two: `pre553_physical_decoder.py` (`d2a074a4…` → `d3d828c1…`) and
`pre553_r5_codec.py` (`72f8f3c0…` → `6000a170…`). I verified the pre-C3 pair
is present at `903c262e4`, `a1545aee`, `46f3bec82` **and the final rebind
`74a06774`**; the C3 pair arrives with `30686b185`.

> **The M01 61/61 does not qualify the freeze's exact 23-module closure.**

### 3.2 A refinement to HQ187 that strengthens its own conclusion

HQ187 records the chain as "`pre553_physical_decoder.py` L21 imports
`pre553_r5_codec`". That is correct **at the freeze**. It is not the edge that
placed the codec in the M01-time closure — the pre-C3 decoder has **zero**
`r5_codec` references. The codec enters via
`test_…route_b_production.py` L30 → `pre553_source_backed_c11_facade.py` L38
→ `pre553_r5_codec`, and the facade blob is identical at both states. The
decoder → codec edge was **added by the accepted C3 repair**.

Conclusion unchanged, and firmer: both modules are inside the closure at both
states, and the codec never depended on the changed decoder. No stage effect.

### 3.3 The corrected authority basis — different scope, not weaker

- Accepted C3 six-file court: **55 passed**, denominator `9+8+13+9+6+10`
  asserted by `--collect-only` *before* the timed run, executed **twice**,
  identical.
- C4C3's **55/55 executed twice on the freeze/combined-tree bytes** —
  explicitly a fresh execution, "not an inheritance".
- Decoder and codec are **two of the six pinned accepted C3 blobs**, so they sit
  inside the authoritative C3 denominator directly. All **11** pinned blobs
  verified **EXACT** at the freeze, zero drift.
- `rawlsing_next` is `b0c1ab47` at C4A, at C4C3's head **and** at the freeze,
  so C4C3's Darwin qualification covered the freeze's exact decoder/codec
  bytes.

Defect location: **the record, not the evidence.** Zero freeze-acceptance
blockers.

### 3.4 21 → 23, tightened, with both overreaches refused

Three root sets, computed separately at the freeze: C4C3's five layers = **21**
(reproducing C4C3 exactly); producer+carrier = **19**; union = **23**, overlap
17. So the producer-inclusive closure is **exactly 23**, not "at least 23".

Both forbidden claims are **false** and were not made:

- ❌ "M01 61/61 qualified the 23-module closure."
- ❌ "All 23 producer-inclusive modules were freshly rerun on Darwin" —
  producer and carrier sit **above** C4C3's five layers and are outside its 21.

### 3.5 The rest, at its ceiling

- **M01's 32** = 30 functions + one `@pytest.mark.parametrize` at line 1388 over
  three refusal states. `11+4+14+32 = 61`. Source-derived. The *run* result
  stays inherited; the Actions log was **not** retrieved.
- **R7 is BOTH.** The record says "from **this path** alone", not "from the
  repository". The recipe pins **13** packages; the resolved environment has
  **14** — `narwhals` is present at 2.26.0 and **absent and unpinned** from the
  recipe. Off-path and bounded, but **not absent**: it would change the freeze
  hash.
- **R9 is six of eight**, not eight of eight. SRC27 has one governed full
  Route-B pass, max one, zero retries, and **four separate access accounts** that
  may not be collapsed into one open. SRC35 has a zero-fresh-read law. The
  warrant candidate carries **zero of seven**. SRC27 and SRC35 are heavily
  constrained, **not unconstrained**.
- **Hash census** 32/29, 6, 2, 3, plus 9 raw-text 32-hex of which **3 are
  prose**. The two 40-hex values are **complete Git SHA-1 tree identities**,
  **not** truncated SHA-256.
- **R10** digest recovered by exact field read; the only truncated identity in
  the 12-file packet.
- **Cross-lane T3 attribution** recorded at actual severity: record-level, not a
  blocker, not a counterexample, R10 recovery unaffected, left open for HQ.
- **Register carried unchanged**: 0 / 1 / 1 / 9 / 1, two sealed pointers
  agreeing.

## 4. The external packet

Scoped to the **one reserved C4 decision**. Six dispositions (A–F), each with
explicit *becomes available* and *remains held* lists. Lifting the hold would
**not** issue a warrant, cure R9, cure R7, authorize locator discovery,
authorize raw access, authorize live C4, authorize C7, or authorize
PRE-V3→V3 actor work. Net effect stated plainly: **lifting changes exactly one
thing** — the freeze is no longer withheld from the build.

The packet carries no model identity, benchmark timing, throughput, cost,
latency, or model-preference material in its technical proof. 29 self-audit
checks, 29 passed.

**HQ188-B has not contacted or invoked Astra. Routing the packet is HQ's act.**

## 5. Claims deliberately not made

Stated so the ceiling is auditable. Full list in `03_CURRENT_CLAIM_EVIDENCE_MAP.json`
and `05_FINAL_DISPOSITION.json`:

1. That M01 61/61 qualified the freeze's complete 23-module closure.
2. That all 23 producer-inclusive modules were freshly rerun on Darwin.
3. That the 40-hex values are truncated SHA-256.
4. That SRC27 or SRC35 carry no constraints.
5. That artifact 07 binds read counters for eight sources.
6. That "from the repository" appears in the environment record.
7. That the environment is exactly reconstructible from the 13-package recipe.
8. That R7 is fingerprint incompleteness only.
9. That the GitHub Actions execution log for run 36302391261 was retrieved.
10. That C4 is adopted, the hold is lifted, or any warrant, locator, raw access,
    live C4, C7 or actor work is authorized.

## 6. Hard holds — all observed

| Hold | State |
|---|---|
| Raw-source access | 0 |
| Locator discovery / fill | 0 / 0 |
| Warrant issued or altered | no |
| Live C4 executed | no |
| Production mutated | no |
| C7 implemented | no |
| Actor/person work implemented | no |
| C4 adopted | no |
| HQ182 hold lifted | **no — unlifted** |
| Astra contacted or invoked | no |
| Self-adopted | no |
| Merged into control | no |
| `HQ_HANDOFF/**` edited | no |
| OPS-04 `00`/`01` edited | no |
| Historical worker returns edited | 0 |

## 7. Verification discipline

`git` plumbing and `node` v18.14.2. `python3` was verified functional on this
host but **not relied upon** for any verification result.

**Non-equality law:** no verification rests on `null == null`, on an absent
field, or on comparing two missing values. Every identity resolves to a
nonempty exact 40-hex Git blob ID or a complete 64-hex digest. Two known
vacuous-pass disclosures in the evidence are preserved rather than dropped:
the R2 reviewer's self-caught `None == None` manifest comparison, and the
audit's reproduced vacuous OPS-03 Q08 acceptance.

Where a conclusion depended on it, the actual artifact was inspected.
Contradictions were not resolved by choosing the newest prose, by lane
agreement, or by model reputation.

## 8. Open items for HQ

1. **Cross-lane T3 attribution** — reconcile which lane the shared freeze
   digest belongs to, or record that one digest covers both. Advisory.
2. **Warrant issuance blocker 5** — decide whether the existing independent
   reviews (`fe6103cd`, `3a5b2cbc`) and the R2 re-check (`afb1eb49`) discharge
   "independent integration review of the freeze not yet completed". **Not
   decided here.**
3. **Lane A formal adjudication** — remains open; HQ182 held it and `LATEST`
   records `c4_final_review_adjudicated: false`. **Not closed here.**
4. **D2P's two identities** — `checkpoint_identity 3fab15f3…` and
   `canonical_closure_identity f264dd8f…` remain recorded-but-unverified by
   D2P's own ruling.
5. **Route or withhold the external packet** — the reserved C4 decision is not
   HQ188-B's to dispose.

## 9. Return protocol compliance

- Complete return packet written before commit.
- All and only authorized documentary/evidence changes committed.
- No uncommitted commissioned work remains.
- Worker branch pushed to `origin`.
- Remote branch re-fetched and resolved; local `HEAD` equals
  `origin/agent/rabochii-pyat-hq188-b-c4-current-consolidation-r1` at one exact
  full 40-hex SHA.
- Exact final remote SHA recorded in `00_RETURN.md` and `05_FINAL_DISPOSITION.json`
  via the seal commit.
- **Not** merged, fast-forwarded or rebased into
  `integration/pre-main-reconciliation-r1`.
- **No** force-push. If a correction is later required, a new commit is
  appended and its SHA reported.
- **No** self-adoption.

Terminal:
`HQ188_B_C4_CURRENT_CONSOLIDATION_RETURNED__HQ_REVIEW_REQUIRED`

Terminal addition:
`HQ188-B_REMOTE_BRANCH_RETURN_VERIFIED`