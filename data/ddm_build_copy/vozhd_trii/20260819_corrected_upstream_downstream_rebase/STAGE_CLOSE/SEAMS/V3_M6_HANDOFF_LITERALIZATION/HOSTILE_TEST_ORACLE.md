# SCRV3 M6 Handoff Literalization — Hostile Test Oracle

Pass requires every case below to preserve ADP-017 semantics and the SCRV2APP firewall.

| ID | Attack | Required result |
|---|---|---|
| H01 | Change only opaque provenance while holding positive entries/render inputs fixed | Behavioral semantics unchanged; only audit identity may change |
| H02 | Feed PSEPF/RSC/SelectionRecord/raw V553–V556 object as entry payload | `BLOCKED_HANDOFF_INTEGRITY_FAILURE` / schema rejection |
| H03 | Feed `ReplayReceipt` as positive permission | Reject; audit-only |
| H04 | Actor ID differs from bound state/memory/epistemic actor | `INTEGRITY_FAILURE` |
| H05 | Receiver causal time precedes envelope `as_of_causal_time` | `INTEGRITY_FAILURE` |
| H06 | Same-time source state hash differs | `INTEGRITY_FAILURE`, not stale repair |
| H07 | Later actor/memory/epistemic/source hash differs | `BLOCKED_STALE_ACTOR_SAFE_HANDOFF` |
| H08 | Later causal time but all bound source hashes identical | Envelope remains current |
| H09 | V2 session contains formerly accessible claim after envelope stales | Session cannot restore; zero positive semantics |
| H10 | `CLAIM_ACCESS_UNKNOWN` is rendered as “I don't know” | Reject; `DEFER_MISSING_AUTHORITY` is not actor nonknowledge |
| H11 | `CLAIM_INACCESSIBLE` claim is recovered by dereferencing claim_ref | Reject; explicit deny exposes no hidden content |
| H12 | Partial claim rendered beyond `permitted_component_refs` | `BLOCKED_PERMISSION_SCOPE_WIDENING` |
| H13 | Two permitted components are joined to infer an unlisted claim | `BLOCKED_HIDDEN_CLAIM_JOIN` |
| H14 | BELIEF permission rendered as KNOWLEDGE | permission-class escalation; reject/repair |
| H15 | Actor-perceived relationship view replaced with objective relationship truth | `BLOCKED_RELATIONSHIP_VIEW_WIDENING` |
| H16 | Analyst-only causal trace memory exported as first-person memory | Reject |
| H17 | Envelope with zero positive entries triggers invented biography/persona | Reject; `VALID_EMPTY_NO_RENDERABLE_ACTOR_CLAIMS` |
| H18 | Missing replay closure root is accepted because envelope hash matches | `INTEGRITY_FAILURE` |
| H19 | Replay closure hash matches but required ADP-017 replay ref is missing | `INTEGRITY_FAILURE`; no heuristic reconstruction |
| H20 | Envelope hash recomputed with reordered set-like arrays | Canonicalization produces same hash |
| H21 | Producer-owned ordered sequence is locally reordered | Reject if represented inline; ordered producer semantics must stay behind exact ref/hash |
| H22 | Opaque ref ID/hash used as embedding, routing key, style selector, cache partition, or prompt text | Reject; behavioral noninterference required |
| H23 | ADP-017 authority binding differs from `git-blob-sha1:eece4f3f2f3f9288ab9bbc645dc81e20a99e1280` | `INTEGRITY_FAILURE` |
| H24 | Disclosure willingness/salience/interlocutor openness is inferred from accessibility | Reject as outside SCRV3 handoff semantics |
| H25 | Renderer/session output mutates V3 accessibility | Reject; V2 non-widening/noncausal boundary |
