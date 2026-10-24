# R95 R06R3 author return — four public-boundary repairs

**Disposition:** CANDIDATE_FOR_INDEPENDENT_REVIEW. Not self-adopted.

## Identity

- Branch: `agent/opencode-pyat-r95-r06-world-consumer-integration-r1`
- Startup: `08fa9a2560ff5a37313434a3edb3d61e702926eb`
- R3 contract: `033efe2b4a636d909fe4def2056aa5c68762e182`
- R3 code: `d0690af0c85fca962a4ac1e08012e869e94cb404`
- Executor: existing OpenCode DeepSeek V4.1-Flash MAX/Global.

## Four defects repaired

### 1. Actual P41/E04 invocation, not a caller receipt

`select_r05_world_view` now constructs and invokes the actual pinned P41
service from host-retained actual inputs: actual R05 empirical objects, exact
learned/coordinator original, actual step and P41 runtime. It builds the actual
`SelectedWorldCatalog`, provider, structural service and `P41Service`, then
runs actual N10W/E04 `consume` for T0/T1. The old caller callback is rejected
without being called (`CALLER_CALLBACK_NOT_ACCEPTED`). Optional claimed receipts
are compared by content hash to the actual execution; a canned/tampered mapping
returns `R05_CLAIMED_RECEIPT_MISMATCH`. A canned callback alone can no longer
mint `R05_WORLD_SELECTED_VIEW`.

### 2. Actual temporal consumer dependence

`temporal_changed=True` now requires the normalized actual consumer payload to
differ: E04 routes, N10E target/conditioners/state/denominator/cells, and N10W
positioned consumptions/state. Clock labels, receipt hashes and incidental
provenance are excluded. Distinct clocks with identical actual payload return
`R05_TEMPORAL_PAIR_NOT_CONSUMED`. The positive T0/T1 pair changes actual routes
`ELIGIBLE/WITHIN_MODELED_BUDGET` ->
`BLOCKED_BY_MODELED_RULE/RESOURCE_CONSTRAINED`; a no-revision actual execution
refuses. This is declared synthetic modeled-rule evidence, not original F7.

### 3. Cross-unit transport is typed UNAVAILABLE

Every public wrapper (`select_world_view`, `select_joined_world_view`,
`select_r05_world_view`) now returns `CROSS_UNIT_LINKED_QUERY_UNAVAILABLE` for
different units. A relation/transport ref plus `authorized=True` is not a
linked indexed query and is not accepted. Same-unit two-field positive remains.

### 4. Context promotion requires actual FF admission

A CONTEXT field requires an exact `StructuralEmpiricalAdmission` object with
typed state `ADMITTED_FOR_EXACT_STRUCTURAL_USE`, target use
`STRUCTURAL_MEDIATION_INPUT`, matching source universe and structural field
refs. An arbitrary FF ref or absent admission refuses. The direct STRUCTURAL
synthetic positive remains; no F5/F6/F7 issuance is claimed.

## Preserved genuine positive

Actual accepted R05 learned product + retained-original coordinator result feeds
the same actual P41 N9/N10W/E04 consumer. Two real fields affect the same
assertion; E04 routes change; N10E values bind to the R05 consumer hash and
coordinator original; cold fresh-process replay matches. R1 J42/N10E positives
are preserved, with R1 cross-unit label positives now typed UNAVAILABLE.

## Evidence

```text
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_world_binding.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R95-R06-WORLD-CONSUMER-INTEGRATION-R1/revisions/r3/junit.xml -o addopts=''
```

`14 passed`, 0 failed/errors/skips, `170.142s`.

Independent R06V probes replayed against the repaired tree:

```text
PYTHONPATH=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01 \
  /usr/local/bin/python3 -m pytest <R06V independent_probes/test_r06v_world.py> -q \
  --junitxml=WORKER_RETURNS/PYAT-R95-R06-WORLD-CONSUMER-INTEGRATION-R1/revisions/r3/reviewer_probes_junit.xml -o addopts=''
```

`5 passed`, 0 failed/errors/skips, `7.302s`: actual positive, hash/clock-only
mutation refusal, transport-label refusal, bogus-FF refusal, canned-callback
refusal.

## Code blobs

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_universal_world_binding.py` | `f695d8974c1b5cf617213a9976620defc91fb270` |
| `rawlsing_next/tests/test_universal_world_binding.py` | `a0cdee8d481382a4fd1e6065206badd99398192f` |

Only these two code paths changed from startup. R03/R04/R05/R08/native/FF/
temporal/J42/P41/E04 bodies read-only.

## Import pins

- R05 candidate/review: `bc2b5465c8f0ec2ea4657c6206436cdfa9ca58d0` /
  `2f7faac6da620b7651c175ec074d7088d5a49343`
- R05 consumer/fixture blobs at startup:
  `pre553_learned_world_composition.py` `adbcc3316920c708580097dfe9f5aef4c9ca82fb`;
  `test_universal_learned_consumer.py` `b0114a82c8852faffc52686c69585a50ee89ba9f`;
  `pre553_analytical_composition.py` `ed2b1680006ac2b89ddd40499e0a6d1429327d7b`;
  `pre553_universal_empirical_extension.py` `37279fa82001d5853dadf4906efc904e8dc3b9bc`.
- Actual P41 packet: `f27d1101048638bba395143a48efb7ef00bfcda4`
- R1 J42 packet preserved: `f53cb0d2bce52640268c844c398bbd8007d28edc`

## Limits

- Sourcefree TEST_ONLY local trusted host only. No cryptographic/R09 isolation;
  actual execution inputs/runtime are host-retained, not subject-signed.
- Original F7 measured waves, original 35x54/F6/F8, source/science, F5/F6/F7
  issuance, CI/prod, N11/N12, Sorok and J52/W52 remain held/NOT_REACHED.
- The temporal pair is a declared synthetic modeled-rule pair, not original F7
  measured-wave comparison.
- No self-adoption; distinct independent reviewer required.
