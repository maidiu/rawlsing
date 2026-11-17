# COLD BUILDER HANDOFF — exact artifact, cold reconstruction, limits

**Artifact:** `REPAIRED_PACKAGE.zip` (this return root). It expands to `ANVIL_R7/`, the corrected instrument over the original supplied ZIP bytes. **Authority:** preparation artifact only; not native science, not independent C, not protected H1, not an architecture selection.

## Required inputs and exact pins

- Original supplied ZIP: `/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip`, SHA-256 `526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332`, 280 entries.
- Shared Git object store: `/Users/matthewsmith/s2b-work/rawlsing` (worktree `.git` common store; no clone/install).
- Protected currentness witness: `31291d08179890852246c8742700e055168e9933`; K3 source cut `7fc00289dd801d2d0a8ce159986c7595fc27a4d9`.
- Authored local fixture: `EVIDENCE/FRAME.json`, `DECISION.json`, `C.json`, `SOURCE_IDENTITY_INVENTORY.json`, `RELEASE_REGISTER.json`, `SOURCE_118/`. This fixture is a test input, **not a real decision**.
- Six projections: `BUILT/` with `MANIFEST.json`.

## Cold reconstruct

```bash
rm -rf /tmp/anvil-cold-XXXX && mkdir /tmp/anvil-cold-XXXX
unzip REPAIRED_PACKAGE.zip -d /tmp/anvil-cold-XXXX
cd /tmp/anvil-cold-XXXX/ANVIL_R7/tools
python3 r7_inventory.py verify \
  --source-root ../tests/fixtures/source_118 \
  --repo /Users/matthewsmith/s2b-work/rawlsing \
  --zip /Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip \
  --inventory ../tests/fixtures/source_118/SOURCE_IDENTITY_INVENTORY.json
python3 test_r7_integrated.py -q          # inherited 29 sourcefree tests
python3 test_integrated_strict.py         # integrated 13 positive/mutation/restore tests
```

For the full authored packet, use the return-root `EVIDENCE/` and `BUILT/` paths; the commands are in `TEST_TRANSCRIPT.json`. Expected local statuses: `PASS_SOURCE_IDENTITY_INVENTORY_S1_DOCUMENTARY`, `PASS_LOCAL_COMMON_REQUIREMENTS_SOURCE_IDENTITY_NOT_NATIVE_AUTHENTICATED`, `PASS_LOCAL_INTEGRATED_DECISION_PENDING_C`, `PASS_LOCAL_C_PACKET_ONLY_INDEPENDENCE_UNVERIFIED`, `PASS_SIX_PROJECTIONS_BYTE_IDENTICAL`.

## Sabotage / restore

The integrated 13-test suite mutates exact bytes and requires RED, then restores exact bytes and requires PASS: K3 row text, missing requirement row, revoked release, actor-firewall flag, fabricated H1, missing identity disposition, prospective adoption, missing T4 negative, non-existent builder command, forged ZIP member. `r7_build.py verify` refuses a changed projection and passes after byte-identical regeneration.

## Honest limits

- No native SAV/DTA source read, no 600–1,300-slot dense 100k, no process-tree ≤6 GiB, no 1/10/100 distinct-operation benchmark. All `NOT_RUN`; the ~3,034s / 3.245 events-per-respondent sourcefree example is not representative.
- No source/actor/science right; no actual first reader executed; no independent C; no H1. `C_HOLD_EXACT` is the honest grade.
- A malicious author who controls the whole evidence root can still forge a local raw log and human summaries. The gate closes exact-byte/identity/topology paths, not issuer identity; only external runner/reviewer custody closes that.
- F26 exact caller/invalidation remains the existing K3/P4R owner hold; no invented body.
- The 16 terminal IDs are scope/held identities, not implemented readers. T1–T7 are interrogations, not seven stages.
- Do not run this handoff as an architecture launch or as independent C.
