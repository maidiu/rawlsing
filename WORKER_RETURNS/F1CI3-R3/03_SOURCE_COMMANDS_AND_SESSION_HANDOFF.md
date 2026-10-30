# F1CI3 — exact source, commands and session handoff

**FINDING:** independent replay completed with three preserved full-history assertion failures and an existing targetless REFUSE regression pass. **INTERPRETATION:** a bounded sourcefree critic return; no native or canonical acceptance. **ACTION:** incumbent HQ reads back the immutable published return and routes the original-owner correction/reuse decision, then assigns a distinct reviewer. **OWNER:** incumbent HQ + separate reviewer; original B/world/CAN/ADP/Pyat/C8/C9/C10/C12/SCI05 owners retain grants; PRE-MAIN owner retains central registry/CAS writes.

## Repository and worktree custody

Repository identity directly read: `origin=https://github.com/maidiu/rawlsing.git`. The supplied Desktop Rawlsing directory is an artifact workspace, not a Git checkout. Verified shared store: `/Users/matthewsmith/Desktop/as2b-lits1-DiSDJn/repository`.

Owned isolated checkout: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/f1ci3-r3-independent-court`; branch `review/sorok-r3-f1c-b-world-causal-independent-court-20261030`. The assigned branch was absent from the store's worktree list; atomic `git worktree add -b` established this own local branch/worktree claim. No active worker's checkout or process was reused, reset or killed. This is a verified local exclusive claim, not an invented fleet/dispatcher lease. External lease service and provider quota were not supplied; no numeric quota floor was commissioned.

Sealed underlying startup **187fdd11963163dab03c7b061e20067ea1f99134**; direct remote commission head **e1b877f7dbc8da0ae85448fe367f301d7a639c1c**. Its five later commits change only:

- `WORKER_COMMISSIONS/F1CI3-R3/00_COMMISSION.md`
- `WORKER_COMMISSIONS/F1CI3-R3/01_COPY_PASTE_LAUNCH_PROMPT.md`
- `WORKER_COMMISSIONS/F1CI3-R3/SESSION_LOCATOR_DISPATCH.json`

The worktree began at the actual published commission head, retaining sealed ancestry. Its initial empty index after `--no-checkout` was populated using `git read-tree -mu HEAD` under the new sparse checkout. The resulting tracked state was clean before any return writes. No deletion of repository sources was staged/published.

All content writes and runtimes belong to `WORKER_RETURNS/F1CI3-R3/**`. Exact historical sources are staged under ignored `candidate/runtime` and `candidate/join_runtime`; they are not modified or republished as a replacement engine. Reproduction scripts/receipts and unchanged embedded F1C code are retained. No original survey/respondent/native source, PRE-MAIN/main, PR514/516/519/521, other worker, central session registry or semantic issuer source was mutated.

## Exact source identities

The five F1C artifacts were read at **bcea367e7dc0f2e069de71b0fe5e481de094dad5**; exact path prefix `WORKER_RETURNS/SOROK-F1C-NONRETROACTIVE-WORLD-B-SOURCEFREE-RECEIVER-R1/`. Their Git blobs/SHA256 are in artifact 01. The embedded executable was extracted without changes:

- Program Git blob: **104f5bd7826c8676192eac96753d980e35d8a80a**.
- Program SHA256: **7e3492a267acbc0fa11d8792158bdaa2acc9dfb6053f16141ed637dc1cd2881b**.
- Selected unchanged `r31j.assertion.p01`: **f53ad1bffb4dcd7fc0edc27ccbd3362d64ca1aa8**.
- F2 separately loaded verifier: **c1699c8da5e944ed079708e272c3af50d5a30a44**; no overlay/adoption.

All **27 supplied source pins** were independently resolved at their exact commits, Git blob preimages and SHA256s. Full paths are in `candidate/source_manifest.json`, including:

| Source | Exact commit | Read/run scope |
|---|---|---|
| F1 | `8aad22736c9f488c92ed007128c1875075142839` | All four artifacts; documentary rival/negative specifications, not execution totals. |
| F1I | `c48d3dff2b86e0da54ad3dbb09a34baf53d0273e` | All four artifacts; nine rival and twelve negative crosswalks preserved. |
| Original R31J | `64fec28c374d8f77fb0b412d0c934d798ede03e8` | Exact runtime archive; 217 files match tree blobs; historical producer and unchanged p01 executed. |
| JOIN | `7bf2da302996491ddf34b9a039fea47ac982d135` | Exact archive; 478 files match tree blobs; original targetless regression executed separately. |
| BP2P4J | `5b3e6577400ea1d88971ae6b48e41a118b8059ae` | Original assertion/verifier read; R31J inherited lineage executed. Distinct named `joined_downstream_a0_a2_assertion` and original full suites NOT_RUN. |
| PFF G1/G2 | `f4a61361ae9da371a0319594c297fbf93f0326ad` | Original §5 source semantics read; no new generic G1/G2 issued. |
| Pyat R95 | `b2cfe93cee854b7aff2081a7a223ada75295332a` | Exact R4 original return read; trusted bounded consumer preserved; CONTEXT→STRUCTURAL authority remains held. No R95 rerun. |

The inherited runtime imports repository namespace modules. The two declared live pins and five transitive dependencies were staged from the exact F1C commit **inside this owned return tree**, with manifest `candidate/live_namespace_manifest.json`. The first import attempt correctly failed because M6 also requires M5; staging the transitive exact closure resolved that setup defect. No runtime code was patched. Namespace file location differs from the original root; the original JOIN whole-suite `LIVE_ROOT` location assertion is not claimed run/passing. The independent F1C process records **69 physical Python imports**, paths and byte identities in `candidate/independent_probe_results.json`. The separate JOIN regression uses its own pinned J-first/E-second process and source archive.

## Reproduction commands and actual outcomes

Run from the owned checkout root, with the exact Git objects accessible. Paths below are repository-relative **inside these shell commands**. All generated paths remain within the own return tree.

```bash
F1CI3_CANDIDATE="$PWD/WORKER_RETURNS/F1CI3-R3/candidate"
PYTHONDONTWRITEBYTECODE=1 python3 "$F1CI3_CANDIDATE/prepare.py"
PYTHONDONTWRITEBYTECODE=1 python3 "$F1CI3_CANDIDATE/f1c.py" > "$F1CI3_CANDIDATE/replayed_results.json"
PYTHONDONTWRITEBYTECODE=1 python3 "$F1CI3_CANDIDATE/independent_probes.py"
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest "$F1CI3_CANDIDATE/test_full_history_binding.py" -q -p no:cacheprovider -o addopts='' --basetemp="$F1CI3_CANDIDATE/pytest_history_tmp" --junitxml="$F1CI3_CANDIDATE/history_binding_junit.xml"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$F1CI3_CANDIDATE:$F1CI3_CANDIDATE/join_runtime" python3 -m pytest "$F1CI3_CANDIDATE/join_runtime/tests/test_join.py::test_targetless_provenance_lineage_and_fork" -q -p no:cacheprovider -o addopts='' --basetemp="$F1CI3_CANDIDATE/pytest_targetless_tmp" --junitxml="$F1CI3_CANDIDATE/targetless_original_junit.xml"
```

| Actual operation | Exit / result | Retained evidence |
|---|---|---|
| Original F1C program, exact bytes | **0; 13/13 expected scenarios** | `replayed_results.json`, `replay.stderr` (empty after final successful replay) |
| Independent frozen/material/source/access comparison and six probe observations | **0; observations retained, including accepted invalid live history** | `independent_probe_results.json`, `independent_probes.log` |
| Independent full-live-history refusal properties | **1; 3 failed, 0 errors, 0 skips** | `history_binding_junit.xml`, `history_binding_pytest.log`; all fail `DID NOT RAISE f1c.Hold` |
| Unchanged original targetless provenance/lineage/fork test | **0; 1 passed, 0 errors, 0 skips** | `targetless_original_junit.xml`, `targetless_original_pytest.log` |
| Exact source preparation and byte verification | **0** | `prepare.log`, supplied-source/namespace/archive manifests |

Shell display wrappers sometimes end with `cat`/`tail` and therefore return the display command's status. The table reports the underlying Python/pytest statuses; the three failures are preserved in JUnit and are not converted into green by those wrappers. Original F1C main contains its own expected-outcome assertions; its 13 cases are **not 13 pytest passes**. Likewise six probe observations are not six independent accepted properties. Do not add historical 98/38/51/35 suites to these counts.

**NOT_RUN:** original full BP2/BP4/R31J/JOIN/F2/Pyat suites; native autonomous A/B/world or original survey/respondent data; original scientific Rule A/T, G1/G2, SCI05; native ADP/CAN/Pyat grants, N11/N12/C11; general actor claim/access semantics; native C10 targetless contract; F1C→JOIN targetless adapter and SILENCE cold continuation; helper attribution or acquired-practice/transfer court; production C12 completeness/authenticity; human A4/A5; QF2; independent post-return review; merge/adoption/CAS.

## Session custody and HQ intake

`scutil --get ComputerName` returned **mainMac**, separately from hostname **MacBook-Pro.lan** and architecture x86_64. Python **3.11.3**, SQLite **3.40.1**. `SESSION_LOCATOR.json` records AGENT_NAME=Codex, AGENT_ID=/root (exposed canonical agent path; provider ID unavailable), AGENT_ROLE/mode, harness=Codex and actual locally saved model/effort separately.

Current chat ID **01a18de3-25a9-7d42-b544-a5bd6936c6dc** is exposed by `CODEX_THREAD_ID` and verified in the read-only local thread database. Its exact **stored** title is retained in the manifest; direct UI title inspection was not available and no suggested title or URL was substituted. No invented deep link. The agent's optional custom profile nickname is null; it is not inferred from the harness or model. Local configuration verification is not provider-side model/effort/account attestation.

The central registry was read at exact commission head. Its exact F1C historical row resolves original return **bcea367e7dc0f2e069de71b0fe5e481de094dad5**, harness Codex, but device/title/ID/worktree UNKNOWN. The original return has no session manifest. A bounded local thread search for the exact original author branch in title/first-user-message found no match. Original author session therefore remains **HISTORICAL_SESSION_UNKNOWN**, not this critic's session and not an invented oldMac/mainMac attribution. The row is copied intact into the own manifest. Further author recovery is an HQ intake matter, not an operator app-window hunt.

Post-return reviewer: **NOT_ASSIGNED**, owned by incumbent HQ + a separate reviewer. This independent F1C critique is not its own acceptance. The PRE-MAIN owner must append the own manifest with the exact returned SHA to the central registry via its authorized control/CAS path; this worker has no write authorization for that registry. No Slack/email/other-chat message was sent.

## Publication and return identity

Publish only the own return tree with an ordinary non-force push to the assigned branch. Before pushing, require the remote still equal the recorded commission parent; if it changed, stop without overwriting it. After push, independently execute:

```bash
git rev-parse HEAD
git ls-remote origin refs/heads/review/sorok-r3-f1c-b-world-causal-independent-court-20261030
git diff-tree --no-commit-id --name-only -r HEAD
```

The exact immutable pushed SHA and direct readback are reported in the final chat after publication. A commit cannot embed its own SHA; `SESSION_LOCATOR.return_sha=null` is intentional and includes the resolution method. A subsequent HQ registry intake may name that SHA without changing this return. No self-referential manifest, central CAS or merge is performed.

**DONE:** exact source/replay, live-history negative court, recovered targetless regression, own manifest and finite handoff. **REMAINING/BLOCKERS:** three REDs and original-owner contracts/grants; separate review. **LARGEST MOVE:** original owner binds full live inputs and reuses existing targetless machinery under the bounded decisions. **FLIGHT:** one critic, own branch only, no workers disturbed. **DELTA:** executable independent evidence and a recovered receiver replace blanket absence/proof claims. **ENGINEERING:** REVISE plus scoped positives; **SCIENTIFIC/AUTHORITY:** HOLD. **STOP_QF2_ORIGINAL_OWNER_GRANTS_AND_REVIEWS_NOT_PRESENT** remains explicit.
