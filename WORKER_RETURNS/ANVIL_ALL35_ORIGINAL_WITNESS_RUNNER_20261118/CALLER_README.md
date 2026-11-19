# Actual SRC04 witness caller

This is SRC04-specific. The reusable machinery is the producer/supervisor/fresh-reader pattern; the q217 hold, 177/3 scope and accepted historical accounting are SRC04 witness checks. Do not describe it as a generic all-wave acceptance.

## Gate

The `run` command cannot start without `--authorized-source-launch`; do not use it before independent construction G5 and the existing source permission. Preflight and synthetic refusal need no source.

## Exact command

```bash
python3 witness_caller.py \
  --mode run \
  --candidate-tree /path/to/exact-aee954-plus-ffa4520f-final-tree \
  --candidate-patch /path/to/candidate.patch \
  --config /path/to/SRC04/source.config.repaired.v2.json \
  --runtime-config /path/to/exact-accepted-ba886d-runtime-config.json \
  --binding-dir /path/to/ANVIL_ALL35_EXISTING_GRANT_ADMISSION_20261118 \
  --work-root /path/to/private-work \
  --authorized-source-launch
```

The candidate tree must hash as `pre553_source_i02_handoff.py = 6ab7cb50…` and the final patch as `ffa4520f…` before import.

## Behavior

1. Supervisor verifies candidate/patch hashes and opens a unique private root.
2. Producer verifies exact grant/request, q217 hold and 177/3 scoped config before source decode.
3. Producer uses localized `single_pass_handoff.py`: one admitted decode, exact projected sections, and the existing `write_direct_estate` directly. It removes the duplicate replay body journal and explicit first I02 pass; it does not change the core writer.
4. Supervisor reaps producer, checks 6 GiB process-tree RSS and live free-space floor, then starts a fresh reader.
5. If the exact `ba886d877…` runtime overlay is absent, the caller refuses before source with `RUNTIME_OVERLAY_REQUIRED_FOR_RUN`; base v2 stops at slot 176 q716withoutmorocco.
6. Reader checks producer is gone, opens exact held roots/manifest with a real grant-scope callback (not allow-all), records family counts, identity/routing digests, release-ref comparison and precise differences from the accepted historical receipt.
7. No wall clock cutoff; abort only on RSS/free-space caps or failure.

Resource floor: completed 512x600 `3.08 GiB` + 1 GiB Q2/routing spool + 8 GiB retained free = **12,970,801,234 B**. RAM cap 6 GiB.
