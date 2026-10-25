Exact S47 narrow reader repair1, same original session/branch/candidate d58c4e9e6a8fefe8fabed4269a77db0ab6237cd8. Independent review43 d1c54ace4fc2f25c56312021c034679e64bc7d46 confirms actual C9 conditioning edge/sourceclass/actor firewall/Bprovenance/targetless behavior. One defect: read_c9_conditioning ignores event_ref and uses latest binding/current source, losing historical truth after new interval or revoke. Select/validate supplied event identity via existing canonical binding; preserve documented default latest only when omitted. Read exact historical source identity/content from that event canonical C9 record, separately report present revocation/currentness without rewriting prior truth. No new ledger/duplicated shadow history. Add warm/cold two-event distinct sources and historical read after cut regression. Fix only this defect, use existing APIs, no new psychology/sourcegrants. Run preserved review reproducers and focused tests, commit/push same branch and return. Use only in-worktree output paths; avoid /tmp or /dev/null output redirection. No new agents/broad acceptedcomponent tests. Review full text below; exact reproducers read-only under reviewer SOROK_REVIEW/S47/evidence.

# S47 interval-to-C9 conditioning — REVISE

Decision: **REVISE**.

## Exact cut

- Candidate: `d58c4e9e6a8fefe8fabed4269a77db0ab6237cd8`.
- Branch: `codex/sorok-s47-interval-c9-conditioning`; remote matches.
- Base: accepted S46 `f0ef39b92ce2e4add5c0a699389e12f1d7ae434e`.
- Reviewed in a clean fixture with stale bytecode removed. No product edits,
  provider/model calls, extra agents, native/science/source grants, or `/dev`
  operations.

## Executed checks

```text
PYTHONPATH=<S47 return> python3 -B -m pytest -q \
  <S47 return>/tests -p no:cacheprovider
13 passed in 32.96s
```

`run_s47.py` exits 0. The actual C9 readset contains the qualified interval
source; ACTUAL material is `objective_material_eligible: false`, scheduled-only
is `true`; both remain targetless `NO_CHANGE`/`NO_PROPOSAL`; source cut/restore
and cold reopen work. The source class is the existing
`ResolvedStructuralContext` material class; its `access` field is objective
material availability, while `actor_access_granted` is false, so no actor
knowledge is inferred. The C9 readset still carries B event/access provenance
alongside the S47 source.

## Remaining defect

The S47 C9 reader is not event-keyed. `read_c9_conditioning(event_ref)` always
reads `binding_episodes(self)[-1]` and uses the **current** interval source; it
never selects the binding/source belonging to `event_ref`. After a second
interval and admission, reading the first event returns the second event’s C9
response and source:

```json
{
  "first_e1": "TEST_ONLY_BP2_E1_OCC-0002",
  "second_e1": "TEST_ONLY_BP2_E1_OCC-0003",
  "first_source_ref": "TEST_ONLY_S47_INTERVAL_S46_STATE_E22149E8875BE71309CFEB56",
  "second_source_ref": "TEST_ONLY_S47_INTERVAL_S46_STATE_735BCB2CBB4332C863DD1977",
  "first_read_after_event_ref": "aa7008f1516e1a085d72fc9aa15f5099f58bce48ec3dd5ecec5a367abb94a481",
  "first_read_after_source_ref": "TEST_ONLY_S47_INTERVAL_S46_STATE_735BCB2CBB4332C863DD1977",
  "first_read_matches_first": false,
  "cold_first_matches_first": false
}
```

The same reader loses the historical source after a condition cut: the C9
readset still contains the old S47 source ref, but `read_c9_conditioning`
returns `s47_source_ref: ""` and `s47_source_in_readset: false`. This violates
event-keyed/cold exactness and the requirement to retain historical interval
truth while distinguishing current revocation.

## Required repair

- Select the C9 binding by the supplied `event_ref` (and validate it) instead
  of always using the latest binding.
- Read the interval source identity/readset from that event’s canonical C9
  record; report historical source separately from current revocation/restore.
- Add warm/cold regressions for two events with different interval sources and
  for reading the earlier event after a condition cut.

## Receipt

- 13-test output: `evidence/s47-tests-13.out` SHA-256
  `a26db3401e46edde50980de74e1070cde0681cea6555c2364dbc45d014227637`.
- Entrypoint: `evidence/s47-entrypoint.json` SHA-256
  `323e033027f4350c69f6891b1a6e50af8cf0d0de334909287621088cd3352723`.
- Event-key reproducer: `evidence/repro_reader_event_ref.py` SHA-256
  `8622272e466f893a26ba849f5d483ed2679a0c83329052d1d9a71ab405b29b79`;
  output `evidence/s47-reader-event-ref.json` SHA-256
  `3850405154df8ef909a4e9599dd4598bfc372591a4456b50c7c045137d7cc255`.
- Condition-cut reader reproducer: `evidence/repro_reader_cut.py` SHA-256
  `a562379fa387a91bc470cb4f865e7f5c7a2f1e415db1112b846f9ee9e481ac52`;
  output `evidence/s47-reader-cut.json` SHA-256
  `37d995ea696cf07caf201e993322837626cf84defaabebee8776e9a9dfc840e5`.
- Source hashes are in `FROZEN.json`.
- No live provider/domain/native/production action was performed.
