# Prong Spaces

Prongs are bounded shared workspaces for one coherent execution concern. They are broader than a single Rabochii assignment but narrower than the whole Vozhd Dva control room.

## Context-envelope rule

Vozhd Dva is responsible for deciding what each prong and each worker needs to know.

No Rabochii is expected to reconstruct project architecture from repository archaeology, neighboring worker cells, old handoffs, or chat history. Before launch, Vozhd Dva must provide a deliberate context envelope containing the minimum sufficient external knowledge for correct work.

A good context envelope includes:

1. **Why this work exists** — the end-to-end capability or gate it serves.
2. **Canonical inputs** — exact current-main artifacts/interfaces the worker may rely on.
3. **Downstream consumer needs** — what must survive or be produced for later stages.
4. **Frozen architectural decisions** — decisions the worker must not reopen.
5. **Known defects/hazards** — active issue IDs and previously observed failure modes relevant to the lane.
6. **Neighbor interfaces** — only the contracts with adjacent prongs/workers that constrain local choices.
7. **Write jurisdiction** — exact files/domains/IDs the worker may change.
8. **Forbidden scope** — adjacent work that belongs to Vozhd Dva or another Rabochii.
9. **Acceptance evidence** — tests, artifacts, or invariants required for Vozhd Dva review.
10. **Escalation rule** — cross-cutting discoveries are reported, not silently solved outside jurisdiction.

The context envelope must be sufficient for intelligent local judgment. It must not become a dump of the entire project.

## Isolation principle

Workers should be isolated from irrelevant complexity but not from relevant consequences.

A V555 worker, for example, may need to understand what V556 and V3 require from mediation semantics even if they cannot edit V556 or V3. Conversely, they do not need unrelated source-ingestion history unless it constrains the V555 contract they consume.

## Vozhd Dva responsibility

If a worker makes a locally reasonable decision that is globally wrong because necessary downstream or upstream context was omitted from the assignment, that is a control-room failure first, not merely a worker failure.

Vozhd Dva therefore owns:

- context selection;
- boundary definition;
- dependency disclosure;
- synchronization between concurrent prongs;
- adjudication when one worker discovers a requirement that affects another lane;
- updating subsequent worker packets when accepted work changes the shared system.
