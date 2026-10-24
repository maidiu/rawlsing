# R91-R04V R3 independent expectations — frozen before candidate code inspection

Status: smallest successor oracle for the R04_JOINED R3 restored-native-identity
review. Sourcefree TEST_ONLY, trusted-host only. Reviewer is the existing
distinct R04V reviewer, not author/HQ.

## Exact target, startup and write scope

- Commission: `9bbc2b235a63882551580d364a4963324d36aeba`
  `WORKER_COMMISSIONS/PYAT-R91-R04-JOINED-R05-FLIGHT-R1/R04V/revisions/r3/00_COMMISSION.md`.
- Exact candidate/startup: `e6f7b04c49772e07c20ad36f65b9b270a28a49cf`.
- Reviewer branch: `agent/opencode-pyat-r91-r04v-r3-joined-review-r1`.
- Prior R04V R2 review:
  `239f492272bd72011f53570020a4b0cdc27dff27`
  (`WORKER_RETURNS/PYAT-R91-R04V-JOINED-INDEPENDENT-REVIEW-R1/revisions/r2/`).
- Author R3 commission:
  `fdd5ff5665e63fba62d635df74959bd487a767ab`
  `WORKER_COMMISSIONS/PYAT-R91-R04-JOINED-R05-FLIGHT-R1/R04_JOINED/revisions/r3/00_COMMISSION.md`.
- Original full R04V expectations remain inherited; no settled trust/native
  byte court reopening.
- Reviewer writes ONLY
  `WORKER_RETURNS/PYAT-R91-R04V-JOINED-INDEPENDENT-REVIEW-R1/revisions/r3/`.
  Candidate/R03/native/R05/other lanes untouched; no candidate repair.

## Sole remaining defect

The R2 completed cold-restored output was a mutable facts-only
`SimpleNamespace`; it lost the actual native output identity
(`QueryExecutionResult.query_ref`, and discovery owner output identity). R3 must
reconstruct actual native owner objects OR a checked immutable view preserving
every identity-bearing field and association:
- unary: query ref, source/release refs, output facts, receipt/result
  associations, coverage/typed state and any owner output fields;
- governed discovery: native result identity (evaluated frontier/replay/
  coverage/receipt/fact associations), not only `empirical_facts`.
- Nested objects mutable at restored view must not allow authority mutation;
  temporary mutation/control must refuse or be impossible.
- Validate output material against the original externally fixed checkpoint and
  native closure before releasing completed cached facts.
- The SAME native downstream consumer must work uninterrupted versus restored
  for both unary and governed discovery, with exact identities/associations
  and native facts. No field echo, no narrowed facts-only substitute.

## Retained positives to preserve

- Actual governed `NativeDiscoveryExecution` capture/restore with exact
  facts/manifest.
- External original checkpoint pin required; forged/rehashed checkpoint
  refuses.
- Real partial multi-unit prefix -> fresh-process -> pending units, exact
  uninterrupted operation/job/receipt/fact identity/multiplicity, no completed
  rerun/recharge.
- Original manifest retained; current grant/source rechecked before release/new
  native work.
- Fixed-pin/current-grant controls, U43/R03/native owners and R04.byte decoder
  unchanged; two authorized code paths only.
- No new stronger trust service, global exactly-once/R09/R05 requirement.

## Independent successor plan

- Read actual R3 return/code only after this freeze.
- Run relevant author 6 and retained R03 16 plus exact successor checks:
  - uninterrupted vs restored unary output object identity/fields/facts and
    same consumer;
  - uninterrupted vs restored governed discovery output identity/fields/facts
    and same consumer;
  - mutation/immutability control on restored output/nested objects must refuse
    or be impossible;
  - external pin genuine/missing/wrong/mutation;
  - retain partial multi-unit fresh-process/no-rerun positive.
- No broad census.

## Verdict rule

`ACCEPT_SCOPED_LOCAL` only if the restored output identity is actually qualified
at the commissioned unary+governed/same-consumer grain with external pin and
native closure. Otherwise `REVISE` with the precise reproducible gap. No
self-adoption or candidate repair.

## Artifacts and stop

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/`, `replay/`, `evidence/`, `proof_witness.json`,
`manifest.json` self-excluding, `RESUME.md`; commit/push own branch non-force
and direct remote verify.
