# SRC04 Lane C V3 — authenticated native issuer/executor

The human empirical grant is now pinned and authenticated:

- `USER_EMPIRICAL_GRANT.json`
- SHA-256: `757ee9e0eddd933b9d23d9cb84450e0dafabd8b1b6a1ad7e737d433b32c0130f`
- Operation: `PRE553_OBSERVED_RESPONSE_EMPIRICAL_OPERATIONS@1.0.0`
- Scope: observed/co-observed SRC04 response operations over all actually source-qualified fields, with source-local statistic use.

The previous unconditional execute refusal is gone. The execute CLI now:

1. authenticates the exact grant bytes and scope;
2. loads the exact full native C11 release when supplied;
3. constructs positive `PREDICATE_GRAMMAR`, source-literal
   `PHYSICAL_NATIVE_REPRESENTATION_BINDING`, per-target
   `SOURCE_SEMANTICS_TOPOLOGY`, and `TARGET_USE_PERMISSION` snapshots in the
   existing `AuthorityRegistry`;
4. derives an authorized `ObservedResponseContract` over the actual release’s
   source-qualified targets (not a fixed 163/175 target list);
5. executes the existing native workload builder and I03 owner;
6. optionally invokes the accepted Lane D consumer as a read-only dependency.

## Source-literal boundary

The original/repaired source preparations carry historical authority refs that
may be preparation/DEFER refs. The human grant authorizes source-local observed
use, not canonical semantic adoption. The issuer therefore creates a positive
source-literal authority that:

- names the exact historical event authority refs;
- authorizes only `RespondentEvent`/`EmpiricalUniverse` source-literal use;
- explicitly records `canonical_adoption: DENY`;
- never promotes a fixture authority or invents canonical ALLOW.

Topology is issued only for targets validated as one-event-per-respondent scalar
carriers with the exact source-native topology ref/kind. Multiple-event,
ambiguous, non-scalar or canonical-bearing targets remain held in the exact
`held_targets` ledger. No rank/multiplicity loss is forced.

## Exact execute command

```sh
PYTHONPATH=. python3 campaign_src04_completion/empirical/run_native_workload.py \
  --mode execute \
  --parquet-root <exact-ParquetC11Carrier-root> \
  --release-id <exact-C11LogicalRelease-id> \
  --semantic-hash <exact-semantic-release-hash> \
  --source-sha 2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18 \
  --consumer
```

The release input is deliberately pending because the actual A full-source
product is still being constructed and its candidate/replay format is not final.
Lane C does not poll, duplicate the source read, or claim completion.

Without a release input, the CLI writes
`NATIVE_WORKLOAD_PREFLIGHT.json` with status:

`AUTHENTICATED_GRANT_ISSUER_READY__RELEASE_INPUT_PENDING`

and the exact pending fields. It does not emit a permission-refusal record.

## Consumer path

When the accepted Lane D consumer module is joined read-only, `--consumer` calls
`consume_native_producer` with an exact `ProducerBundle` and a bounded
`DiscoveryConsumer` over a supported unary baseline and a supported conditional
predicate. If the dependency is not joined, the bridge reports
`D_CONSUMER_DEPENDENCY_NOT_JOINED`; it does not copy or modify Lane D code.

## Limits

- No original SAV stat/hash/open/decode/read by Lane C.
- No original workload issuance or execution has occurred yet; the full release
  input is absent.
- No canonical value, weight, population, eligibility, structural, causal or
  actor/V3/V2 claim.
- `ser` remains identity-only; `country` and `q701` roles remain unadopted.
- Missing observations are excluded and counted; DK, refusal and source-specific
  special states remain distinct observed states.
