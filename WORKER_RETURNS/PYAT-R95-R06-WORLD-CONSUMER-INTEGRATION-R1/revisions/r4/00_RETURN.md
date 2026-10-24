# R95 R06R4 author return — pinned actual owner, trusted original, held FF

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted.

## Identity

- Branch: `agent/opencode-pyat-r95-r06-world-consumer-integration-r1`
- Startup: `02800fcfd77abde178851031f877838bedb5e242`
- R4 contract: `3382aa85f3f88f9f58d54bf3f3d1b3064aa50d07`
- R4 code: `80a85827a0f5a840566290abf449a89873f59fbc`
- Executor: existing OpenCode DeepSeek V4.1-Flash MAX/Global.

## R4 repairs

### 1. Pinned actual P41 runtime; forged runtime refused

`_execute_p41_world` no longer imports from the caller's `p41_runtime` string.
It derives the workspace root from its own file, materializes the fixed Git
packet `f27d1101048638bba395143a48efb7ef00bfcda4` /
`WORKER_RETURNS/PYAT-R41-P41-GENERIC-PROGRESSIVE-N10E-N10W-SERVING-R1/runtime`
in a private host temp directory, and compares a deterministic tree SHA256
(excluding bytecode) with the caller path. Only the pinned copy is imported;
preloaded `bootstrap`/`p41_service`/`fixture`/`readthrough`/`product` modules are
purged and imported module files are checked under the pinned root. The S1 fake
runtime now refuses `UNTRUSTED_P41_RUNTIME` before any canned receipt can be
accepted. No new signer/R09 service.

### 2. Trusted R05 execution context; subject original refused

`configure_trusted_execution_context` verifies the P41 pin, executes the actual
accepted `TrustedNativeGraphCoordinator`, checks the returned original, learned
consumer result and step against the captured inputs, and registers a
module-private opaque handle. The public request carries `execution_handle` plus
view/field/learned claims; authority comes from the registered context, not from
request-supplied original/runtime/verifier. Optional actual-execution claims are
compared to the context. The S3 forged coordinator original refuses
`R05_COORDINATOR_ORIGINAL_MISMATCH`; a missing/invalid handle refuses.

### 3. CONTEXT-to-STRUCTURAL authority is honestly held

All public wrappers (`select_world_view`, `select_joined_world_view`,
`select_r05_world_view`) now return `CONTEXT_STRUCTURAL_AUTHORITY_HELD` for any
CONTEXT field. A real-type `StructuralEmpiricalAdmission`, arbitrary FF ref or
plausible fabricated object is not issuance; no competent retained FF
issuance/authority closure is configured here, so the edge stays HELD. No
F5/F6/F7 science is claimed. Directly declared synthetic STRUCTURAL fields
remain the positive path. S2 and S6 forged real-type FF probes refuse.

## Preserved genuine positives

- Actual accepted R05 learned/coordinator -> actual P41 N9/N10W/E04 consumer.
- Two real fields affect the same actual consumer assertion.
- Declared synthetic T0/T1 pair changes actual E04 routes
  (`ELIGIBLE/WITHIN_MODELED_BUDGET` ->
  `BLOCKED_BY_MODELED_RULE/RESOURCE_CONSTRAINED`), with equal-payload refusal.
- Cross-unit label-only pooling remains `CROSS_UNIT_LINKED_QUERY_UNAVAILABLE`.
- Learned/source/evidence/fact/step/receipt severance/restore, cold fresh-process
  replay, current/as-of/revocation and R1 J42/N10E genuine positives remain.

## Evidence

Author suite:

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_world_binding.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R95-R06-WORLD-CONSUMER-INTEGRATION-R1/revisions/r4/junit.xml -o addopts=''
```

`17 passed`, 0 failed/errors/skips, `180.674s`.

Independent R06V prior five probes + R3 successor six probes replayed against
this tree:

```text
PYTHONPATH=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01 \
  /usr/local/bin/python3 -m pytest <R06V prior> <R06V R3 successor> -q \
  --junitxml=WORKER_RETURNS/PYAT-R95-R06-WORLD-CONSUMER-INTEGRATION-R1/revisions/r4/reviewer_probes_junit.xml -o addopts=''
```

`11 passed`, 0 failed/errors/skips, `97.557s`. This includes S1 forged runtime,
S2/S6 forged real-type FF, S3 forged coordinator original, S4 equal-payload
temporal refusal, S5 genuine positive/restore.

## Code blobs

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_universal_world_binding.py` | `44ac11c9b7f5809e06b22fb9afee11ca8bc0dee5` |
| `rawlsing_next/tests/test_universal_world_binding.py` | `7095820c4ac1e263da3a9670d6d792f3a161ec0d` |

Only these two code paths changed from startup. R03/R04/R05/R08/native/FF/
temporal/J42/P41/E04 bodies read-only.

## Import pins

- P41 packet: `f27d1101048638bba395143a48efb7ef00bfcda4`
- R05 candidate/review: `bc2b5465c8f0ec2ea4657c6206436cdfa9ca58d0` /
  `2f7faac6da620b7651c175ec074d7088d5a49343`
- R06V R3 defects: `05f54b961712695b4836c6160586510dff60986a`
- R05 code blobs at startup:
  `pre553_learned_world_composition.py` `adbcc3316920c708580097dfe9f5aef4c9ca82fb`;
  `test_universal_learned_consumer.py` `b0114a82c8852faffc52686c69585a50ee89ba9f`;
  `pre553_analytical_composition.py` `ed2b1680006ac2b89ddd40499e0a6d1429327d7b`;
  `pre553_universal_empirical_extension.py` `37279fa82001d5853dadf4906efc904e8dc3b9bc`.
- R1 J42 packet preserved: `f53cb0d2bce52640268c844c398bbd8007d28edc`.

## Limits

- Sourcefree TEST_ONLY local trusted host; the context handle is a private local
  registration, not cryptographic/R09 isolation. A caller that can execute
  arbitrary host code can configure its own context; trusted-host boundary is
  explicit, not claimed as protection against that.
- CONTEXT structural authority is HELD pending competent FF issuance; no
  original F5/F6/F7 science is claimed.
- Original F7 measured waves, original 35x54/F6/F8, source/science, CI/prod,
  N11/N12, Sorok and J52/W52 remain held/NOT_REACHED.
- No self-adoption; distinct independent reviewer required.
