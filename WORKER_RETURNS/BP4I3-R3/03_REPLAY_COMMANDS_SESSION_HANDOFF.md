# Replay commands and session handoff

**ENGINEERING_REVISE__AUTHENTICITY_COMPLETENESS_HOLD__NO_ADOPTION.** The exact as-executed scripts, command arguments, working directories, environment, stdout, exits and JUnit XML are embedded in `01_FORK_SCHEMA_ANCHOR_TESTS.json`. Scratch files are retained locally under this return's `.scratch/`; they are not adoption artifacts. Only the five contracted return files are published.

## Custody and source extraction

Sealed startup `187fdd11963163dab03c7b061e20067ea1f99134` is an ancestor of the actual commission head `15b1434b7f537fad02aa3b0c07a4c4a7741a8b8c`. The former does not contain the commission path. The exact latter prompt was read before execution; the user-specified review branch was created there in this chat's clean, previously detached checkout. No other worker worktree was changed. The two required live namespace files match blobs `74d9701cdc7dabccf61eb5089498db290c1efd9c` and `e0528d65215cb431196570c38bac4eae94217a1b`.

Read-only preflight included `git status --short`, exact branch/worktree occupancy, ancestor check, source-object reads, `scutil --get ComputerName`, and the app's thread-list API. No current-head claim is inferred for the original author from its frozen SHA. Device was observed as `oldMac`; historical author device remains UNKNOWN.

The following is the corrected source-extraction procedure used after the initial Python archive API rejected its unsupported `filter` argument. Use an isolated, authorized replay return tree with no preexisting `.scratch/base`, `.scratch/c9` or `.scratch/c12`; do not overwrite this completed review's retained evidence. This recipe reads Git objects, checks archive members and extracts only the named sourcefree returns under the review tree. It does not rerun survey sources.

```python
from pathlib import Path
import subprocess, tarfile, io, re, hashlib
root = Path('WORKER_RETURNS/BP4I3-R3/.scratch')
root.mkdir(parents=True, exist_ok=True)
sources = [
 ('base', '5b3e6577400ea1d88971ae6b48e41a118b8059ae',
  'WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1'),
 ('c9', '1e99681f58086f2784834df1186cfba71a2c50b9',
  'SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_R2_REVIEW/R3/C9_SQL'),
 ('c12', '68b058656254234f0af02df2a592aa6f8c6a8bd2',
  'WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1'),
]
for name, sha, prefix in sources:
    target = root / name
    target.mkdir()  # refuse an existing replay, never silently overwrite
    data = subprocess.check_output(['git', 'archive', sha, prefix])
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        assert all(not m.issym() and not m.islnk()
                   and not Path(m.name).is_absolute()
                   and '..' not in Path(m.name).parts
                   for m in archive.getmembers())
        archive.extractall(target)
path = ('WORKER_RETURNS/SOROK-BP4-C12-CHAIN-AUTHENTICITY-OWNER-COURT-R1/'
        '03_BOUNDED_SOURCEFREE_CODE_OR_EXACT_OWNER_HOLD.md')
doc = subprocess.check_output([
    'git', 'show', '790f793ea85c8aba914970b7d9c3c25f81bf8a01:' + path
]).decode()
blocks = re.findall(r'```diff\n(.*?)```', doc, re.S)
expected = {
 'bp2p4/c12_guard.py':
  '7fd5dd55912e5d8a16ece9eb47909728fc69ca5031064c809b6d2673232a8021',
 'tests/test_c12_guard.py':
  'fa4b6d8e347be254a40bdf9e0aaa8ee077c8a4ea3fdd11fb8bf5422df91ca82a',
}
for relative, sha in expected.items():
    block = blocks[1].split('diff --git a/' + relative + ' b/' + relative + '\n')[1]
    block = block.split('diff --git ')[0]
    code = ''.join(line[1:] for line in block.splitlines(keepends=True)
                   if line.startswith('+') and not line.startswith('+++'))
    assert hashlib.sha256(code.encode()).hexdigest() == sha
    destination = root / 'guard' / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(code)
```

The author guard/test are recovered from committed Markdown, not the author's mutable temporary directory. F2 overlay and its exact focused test are extracted by the banked `run_counts.py` from `0636d257f588f8874e65b2cb183d1d47c7f53327:WORKER_RETURNS/SOROK-HR1-F2-BP2P4J-EPISODE-VERIFY-REPAIR-R1/candidate/`. The original 150-file vendor manifest is verified against Git by the frozen source-closure tests; no source regeneration is needed.

## Commands actually run

Environment for tests/probes: `PYTHONHASHSEED=0`, `PYTHONDONTWRITEBYTECODE=1`, `BP2P4J_ORIGIN_RUNTIME=off`. Every pytest call disables its cache and uses an explicit `--basetemp` and `--junitxml` beneath the own return tree. The optional literal-origin case is intentionally not exercised. Do not report its generic ABSENT message as verified filesystem absence or alter historical 33/38 claims.

The JSON `replay_programs` includes exact executed source and SHA-256 for `run_counts.py`, `run_remaining.py`, `hostile.py`. To materialize those already-banked bytes in a fresh replay tree:

```python
from pathlib import Path
import json, hashlib
target = Path('WORKER_RETURNS/BP4I3-R3')
receipt = json.loads((target / '01_FORK_SCHEMA_ANCHOR_TESTS.json').read_text())
for name, program in receipt['replay_programs'].items():
    data = program['source'].encode()
    assert hashlib.sha256(data).hexdigest() == program['sha256']
    path = target / '.scratch' / name
    assert not path.exists()
    path.write_bytes(data)
```

Execution sequence was:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 WORKER_RETURNS/BP4I3-R3/.scratch/run_counts.py
PYTHONDONTWRITEBYTECODE=1 python3 WORKER_RETURNS/BP4I3-R3/.scratch/run_remaining.py
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 BP2P4J_ORIGIN_RUNTIME=off python3 WORKER_RETURNS/BP4I3-R3/.scratch/hostile.py
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 BP2P4J_ORIGIN_RUNTIME=off python3 -m pytest -p no:cacheprovider WORKER_RETURNS/BP4I3-R3/.scratch/c9/SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_R2_REVIEW/R3/C9_SQL/tests -q -rs --basetemp=WORKER_RETURNS/BP4I3-R3/.scratch/tmp-c9-exact --junitxml=WORKER_RETURNS/BP4I3-R3/.scratch/c9-exact.xml
```

The first count runner contains a disclosed mistyped focused selector (`test_valid_say_episode_verifies_green`): its exit 4 means zero tests ran and is not acceptance evidence. The remaining runner copies the exact F2 test into the baseline and uses the correct selector `test_valid_say_episode_is_green_and_preserves_the_post_hash_id`, yielding the required expected RED, exit 1. This procedure error is retained rather than silently edited out of the as-executed record. Individual counts and test identities, not the orchestration process's exit, determine the verdict.

`run_remaining.py` explicitly maps only the absent author mirror-schema pathname in `Path.exists/read_text` to the exact staged C9 schema. Candidate/test source bytes stay identical. Exact unmodified results are 10/1 and 47/2; mapped results are 11 and 48/1. They are different declared execution surfaces. No global `/private/tmp` artifact was created and no active author worktree was modified.

The full C9 suite intentionally runs its original hard-coded dependency paths. Before execution, all Python/SQL files under the original C12 dependency subtree (141) and S36 source subtree (23) were compared byte-for-byte to their exact commits. The complete file/digest readback is embedded in 01. Its 14 passes/1 failure include an actual S36 unchanged seven-table readset pass and the C12 repaired-writer conflict, not skipped dependencies. Sourcefree synthetic inputs are created only under this review's pytest temp tree.

## Bounded independent probes and receiving contract

`hostile.py` creates new sourcefree BP2 artifacts from the exact staged machinery and drives the actual joined product. Its guard store replacement is explicitly test-only. It proves the episode-bearing fork contradiction, metadata-unbound anchor, raw deletion/injection/rehash/perception substitution, stale/legacy IDs, direct schema negatives, independent SQLite-trigger rollback, inherited clock residual and unsupported C9 writer readiness. Its C9 actor/mirror/outbox replay uses the existing `MirrorStore.status`, not a fabricated receipt checker. Seventeen recorded diagnostic observations complete with exit 0; several demonstrate defects, so this exit is not an engineering PASS.

Author-script historical claims are not re-attested: original `/private/tmp/bp4c12-probe.py`, `-sev-probe.py`, `-c9-probe.py` and the generated combined patch are not committed artifacts. The two committed diff-fence source files reconstruct exactly. A hash of concatenated fences is not the unspecified original generated patch's hash; no byte-equivalence is claimed for that unavailable artifact.

NOT_RUN: real externally signed anchor/custody ledger, original issuer adoption, original survey/response sources, native CAN/ADP/Pyat/SCI05/C8/C11/C12, production writes, standalone original BP2/BP4 suites, broad adversarial concurrency proof of this guard, QF2, merge or autonomous dispatch. The `68b` test suite's own concurrency/savepoint cases were replayed as tests of that distinct source cut.

## Session and return custody

Actual reviewer: Codex, canonical task path `/root`, independent I3 security/source reviewer, Default mode. No separate provider agent ID is exposed. Actual session: **Review Commission 5 evidence**, app thread ID `01a188b1-d39d-77b1-b50f-855f9dadf149`, host `local`, worktree `/Users/matthewsmith/.codex/worktrees/ff52/Rawlsing`. No session URL was exposed or invented. Harness Codex is distinct from the user-confirmed `GPT-6 High` selection; requested High and confirmed selection are recorded separately from unavailable provider telemetry.

Original implementing lane: branch `agent/sorok-bp4-c12-chain-authenticity-writer-compatibility-r1`, return `790f793ea85c8aba914970b7d9c3c25f81bf8a01`, OpenCode with reported `opencode-go/deepseek-v4.1-flash`, requested MAX/unverified. Author return supplies worktree `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-bp4-c12-chain-auth-r1`. Central registry at sealed startup has `HISTORICAL-SOROK-BP4-R1`, revision 1, with device/title/ID/URL UNKNOWN: **SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION**. No operator hunt or invented link substitutes for this absence. This reviewer is not routed to that author session.

After push, resolve this return by direct remote branch readback and fetch the resulting full SHA; compare all five returned Git blobs against local committed bytes. The commit cannot contain its own future identity: `return_sha=null` is intentional. The exact final SHA/readback is reported externally to the user. The narrow worker publication adds only these five own-return files.

The custody law at `187fdd11963163dab03c7b061e20067ea1f99134:CROSS_HQ_CONTROL_ROOM/SESSION_LOCATOR_AND_RETURN_CUSTODY_LAW_R1.md` says: **“A worker may update its own return manifest only; PRE-MAIN owner updates canonical registry together with current flight/control intake via authorized CAS.”** Therefore central append-only registration after push is an explicit PRE-MAIN-owner handoff, not an omitted permission request or a worker registry mutation. Supply this manifest and externally read-back SHA at intake. Existing historical rows must remain intact.

FINDING → independent replay exposes exact candidate/consumer defects. INTERPRETATION → sourcefree content correctness and custody are separate gates. ACTION → original owners choose the contracts in 02, incumbent HQ and a separate reviewer assess the resulting cut; PRE-MAIN owner appends the locator through its own CAS. OWNER → original C12/BP4/BP2P4J, C9, independent anchor custodian and protected control owner, each within its domain.

DONE: five-file independent return and banked replay evidence. REMAINING: owner corrections/decisions and central intake. CRITICAL BLOCKERS: BP4I3-01/02, unissued anchor, original science and canonical CAS. LARGEST PRODUCTIVE MOVE: repair the named real consumer contracts using the existing implementations. FLIGHT: single reviewer, QF2 NOT_STARTED, active workers undisturbed. DELTA: prior narrow green now has exact compatibility RED and payload limitations. STOP: source-only return; no self-adoption.
