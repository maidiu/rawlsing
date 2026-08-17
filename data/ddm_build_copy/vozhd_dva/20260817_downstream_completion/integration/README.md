# Integration Space

Owned by Vozhd Dva.

This directory contains only cross-prong facts that must remain synchronized after workers are launched.

## What belongs here

- accepted interface changes;
- cross-prong dependencies discovered during execution;
- merge/integration ordering constraints;
- shared schema or semantic changes that alter later worker context;
- unresolved collisions between locally valid worker outputs;
- vertical continuity status across stages;
- decisions that must be propagated into future worker packets.

## What does not belong here

- raw worker scratch work;
- entire PR summaries;
- historical discussion with no current integration consequence;
- speculative architecture not attached to an active capability or gate.

## Synchronization law

When Vozhd Dva accepts a worker result that changes what another active or future worker needs to know, the integration state must be updated before the dependent work is launched or accepted.

Concurrent workers may proceed only where their frozen assumptions are compatible. If one worker changes a shared assumption, Vozhd Dva determines whether neighboring workers may continue, need a context update, or must rebase/rework.
