# R95-R06V R4 independent expectations — frozen before R4 code/probe inspection

Status: successor oracle for the R06V R4 exact four-boundary review. Sourcefree
TEST_ONLY, trusted-host only. Existing distinct R06V reviewer, not author/HQ.

## Exact target and scope

- R4 commission: `f3698cf286e4659ba451304175c29cda8041787f`
  `WORKER_COMMISSIONS/PYAT-R95-R06-WORLD-CONSUMER-INTEGRATION-R1/R06V/revisions/r4/00_COMMISSION.md`.
- Exact candidate/startup: `b2cfe93cee854b7aff2081a7a223ada75295332a`.
- R4 contract/code: `3382aa85f3f88f9f58d54bf3f3d1b3064aa50d07` /
  `80a85827a0f5a840566290abf449a89873f59fbc`.
- Prior full review commission/oracle:
  `e2776897af673f14237178daf7ae35c2331d48af` /
  `0153d1f9b88ede3f76e5b1658a7441cb2e9a1713`; latest R3 review
  `05f54b961712695b4836c6160586510dff60986a`.
- Author R3 contract/code: `033efe2b4a636d909fe4def2056aa5c68762e182` /
  `d0690af0c85fca962a4ac1e08012e869e94cb404`; repair commission
  `e57ad4993ceaa6a7f41203c98c28ead5cd1a0167`.
- R95 grant: `1315aff53c3eb063a65088fcb5bd8398852668fa`; original R06
  commission `bd712a4aed1c57bd9ac6ebd158ea05f48842bc54`; R2 commission
  `fe92f83348201cad5b9e41d5bd0ab1b68b5847d2`.
- Reviewer branch: `agent/opencode-pyat-r95-r06v-r4-world-consumer-review-r1`.
- Reviewer writes ONLY
  `WORKER_RETURNS/PYAT-R95-R06V-INDEPENDENT-WORLD-CONSUMER-REVIEW-R1/revisions/r4/`.
  Candidate/R03/R04/R05/R08/native/FF/temporal/service/evaluator/test-helper
  bodies untouched; no candidate repair.
- Two authorized R06 code paths only:
  `rawlsing_next/pre553_universal_world_binding.py`,
  `rawlsing_next/tests/test_universal_world_binding.py`.

## Exact R4 boundaries to qualify

1. **Pinned actual P41 owner.** The wrapper must derive the fixed Git packet
   `f27d1101048638bba395143a48efb7ef00bfcda4` / P41 runtime, materialize a
   private pinned copy, compare a deterministic tree SHA256 (excluding
   bytecode), purge conflicting preloaded modules, and import/check the actual
   owner files under the pinned root. A caller-supplied fake runtime or
   preloaded fake `bootstrap`/`p41_service`/`product` must not mint receipts;
   path/class name alone is not authority. Verify actual owner invocation and
   value dependence, not only a hash/name check. No new signer/R09.
2. **Trusted execution context.** `configure_trusted_execution_context` must
   execute the actual accepted R05 coordinator, verify returned original/
   learned/step against captured inputs, and register a module-private opaque
   handle. Public request must not select its own runtime/verifier/original;
   forged/missing handle, original, learned, step, runtime, or same-context
   input substitution must refuse. Genuine configured handle positive must
   survive hostile attempt and restore. The trusted-host context factory itself
   is private infrastructure, not the public subject boundary; a request-level
   attempt to replace it must fail.
3. **CONTEXT authority honestly HELD.** No competent FF issuer is configured;
   any CONTEXT field in `select_world_view`, `select_joined_world_view`, and
   `select_r05_world_view` must return typed HELD/UNAVAILABLE, never issue
   structural science from an arbitrary ref or forged real-type dataclass.
   Direct synthetic STRUCTURAL positive remains. No F5/F6/F7 issuance.
4. **Temporal actual payload dependence.** Actual normalized consumer
   routes/values/N10W/structural dependency change is required; clock/hash/
   provenance-only changes must not claim `temporal_changed=True`. Actual
   synthetic pair positive, equal-payload refusal, cold current/as-of,
   revocation, severance and restore retained.
5. **Two real fields same actual assertion.** Both fields must affect the same
   actual consumer assertion, not a wrapper rules/label mapping or returned
   hash alone.
6. **Cross-unit.** A relation/transport label plus authorized boolean without
   actual indexed linkage remains typed UNAVAILABLE across ALL public wrappers;
   no hidden easier bypass or invented link/query method. Honest absent
   linked-query scope limit retained.
7. **Trusted-host boundary.** Trusted-host private code/root/deliberate
   trusted new grant excluded; no new R09. Sourcefree TEST_ONLY; original
   35/1890/global F6/F7/F8/source/science/CI/prod/N11/N12/Sorok/J52/W52 held.

## Independent successor plan

- Replay author R4 17 tests and 11 prior independent probes (5 R06V + 6 R3
  successor) and add proportionate exact R4 controls only:
  - same configured trusted entry positive -> forged runtime/original/learned/
    step/handle -> restore;
  - caller-supplied preloaded fake modules and runtime path; verify imported
    owner file path/content under pinned root;
  - public request with own verifier/original/runtime refuses;
  - all CONTEXT wrappers HELD with arbitrary/forged real-type admission;
  - equal-payload temporal refusal and actual change positive/cold/restore;
  - cross-unit label-only UNAVAILABLE in all wrappers;
  - two fields same actual consumer assertion.
- No broad sweep; preserve accepted bodies and the two-path scope. Verdict
  `ACCEPT_SCOPED_LOCAL` only if all four repairs and the genuine positive are
  demonstrated; otherwise exact productive `REVISE`.

## Artifacts and stop

`EXPECTATIONS.md`, `00_RETURN.md`, `defects_and_limits.md`,
`independent_probes/`, `replay/`, `evidence/`, `proof_witness.json`,
`manifest.json` self-excluding, `RESUME.md`; commit/push own branch non-force
and direct remote verify. Bank 45; stop 90.
