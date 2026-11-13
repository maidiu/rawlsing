# PYAT1002 — native source hold, gates and next dependency

**Verdict:** `NATIVE_SOURCE_ISSUER_HOLD`  
**Receipt disposition:** `HOLD_EXTERNAL`  
**Evidence grade:** `PREFLIGHT_METADATA_RIGHTS_INVENTORY_ONLY`  
**Integration:** `UNMERGED`  
**Stop state:** `HOLD_EXTERNAL`

This is a completed authority disposition for the assigned finite issue1002
lane, not a scientific sourcefree green and not an engineering failure to be
"fixed" by more code.

## Why the hold is terminal for this scope

The commission permits source-native execution **only** under a genuine current
source right. The inventory found:

- 35/35 source identities and artifacts accounted for;
- 35/35 local artifact sizes matching the historical declared sizes;
- 0 current source-use grants;
- 0 authorized sources;
- 0 source opens / decodes / hashes / native facts.

Applying the commission's own rule:

> If none is authorized, stop with `NATIVE_SOURCE_ISSUER_HOLD` and the precise
> 35×right matrix, plus exact one highest-impact grant.

That condition is met. Continuing to inventory the same 35 sources, or writing
an engineering bridge that pretends to be permission, is out of scope.

## Gate states

| Gate | State | Exact basis |
|---|---|---|
| G1 exact contract / complete inventory | `PASS` | 35-row typed matrix, exact R157 refs, historical ledger, permission-proof search, one exact grant request |
| G2 real executable source-native positive | `NOT_RUN` | No current authorized source; no source read |
| G3 hostile source-native negative + conservation | `NOT_RUN` | No authorized source; nothing to poison or conserve at a native reader |
| G4 custody / resources / recovery | `NOT_APPLICABLE_PROVED` | Read-only metadata inventory; no persistent source-native artifact, no durability claim, no source bytes read |
| G5 independent nonauthor receiving | `NOT_RUN` | No source-native positive; this is an author return |

`G4=NOT_APPLICABLE_PROVED` is not a claim that future source-native custody is
unnecessary. It records that this exact return owns no persistent physical
artifact and makes no durability/resource claim. The eventual authorized source
positive must supply the applicable G4 evidence.

`G5=NOT_RUN` is not an acceptance. Reviewer 999 (or another qualified nonauthor)
must receive any future source-native positive at its exact SHA. No author or
model self-review can satisfy G5.

## Evidence ceiling

This return proves only:

- the exact 35-row metadata/rights inventory;
- the absence of a located current grant in the declared roots;
- the exact historical ledger and fixture/replay limits;
- one exact grant request.

It does **not** prove:

- original35 source availability in a legal sense;
- source-native correctness;
- U/Epre claim validity;
- I02 or first I03 behavior;
- population, temporal or causal claims;
- current-world or production CURRENT authority;
- protected merge or integration acceptance;
- independent receiving.

## No source-open / no-hash evidence

- Source files discovered: 35 exact declared artifacts (with duplicate local
  copies for some GSS/EVS artifacts).
- Source files `stat`-checked: 35.
- Source files opened/read/decoded: 0.
- Source bytes hashed by this commission: 0.
- Source-native execution attempts: 0.
- Source read decisions issued by this commission: 0.
- Source permission refs minted by this commission: 0.

The local `stat` check is metadata only. It is not a source read and not a
permission proof.

## Failure classification

| Item | Classification | Disposition |
|---|---|---|
| No current source-use grant for any source | `HOLD_EXTERNAL` | Competent source owner / data steward required |
| Host authentication not established | `HOLD_EXTERNAL` | Exact authenticated host binding required |
| Current source hash not re-verified | `NOT_RUN_PER_CONTRACT` | No re-hash allowed merely to inventory; eventual authorized read must bind exact SHA |
| Historical SRC04/SRC17 `PASS` is fixture-only | `EVIDENCE_CEILING` | Not promoted; see `03_HISTORICAL_SRC04_SRC17.md` |
| Bounded search may miss an external grant | `SCOPE_LIMIT` | Supply exact external grant if it exists; do not infer denial |
| No independent G5 | `NOT_RUN` | Future source positive must go to a distinct nonauthor |

No `SEV-0`, `SEV-1` or `SEV-2` source-native defect is reported because no
source-native execution occurred. This is not a clean native green; it is a
lawful no-execution hold.

## Next indispensable dependency

1. **Exact grant:** current authenticated `IssuedSourceReadDecision` for SRC04
   matching `04_ONE_HIGHEST_IMPACT_GRANT.md`, or an equivalent exact grant for
   another source. Without it, no source bytes may be opened.
2. **Authorized source positive:** only after (1), run the existing compatible
   selected-column native reader + U/Epre claim-graded operation with a
   changed/restored proof and typed negatives.
3. **Distinct nonauthor G5:** receive the exact positive SHA. No self-accept.

If (1) is impossible, the correct outcome remains this hold. The next work
should move to an independent lawful packet, not repeat the same inventory.

## Preserved holds / no-conflict

- Original35 source/science/host rights: **HOLD**.
- Production CURRENT: **HOLD**.
- Protected merge / protected receiving: **not performed**.
- W03/W04: **still paused/not restarted**.
- Accepted S2-C/D, math/science, Browser #997 and Codex #998 code: **read-only**.
- No replacement bridge, engine, issuer, licence or admin system.
- No model/provider/account/effort/region/harness/VM change.
- No source-native writes outside the return directory.
- No old evidence edited, no existing test weakened, no test added.

## What would change this verdict

Only exact external authority evidence can change the authority court:

- a current authenticated decision from the competent source owner;
- exact permission refs and retention/export/currentness/revocation terms;
- exact host/purpose/consumer-use/semantic-scope binding;
- exact source SHA and metadata freeze refs.

A new engineering test, a source-free fixture, a model answer, a filesystem
mount, a user "GO" to sourcefree work, or a prose assertion cannot change it.
