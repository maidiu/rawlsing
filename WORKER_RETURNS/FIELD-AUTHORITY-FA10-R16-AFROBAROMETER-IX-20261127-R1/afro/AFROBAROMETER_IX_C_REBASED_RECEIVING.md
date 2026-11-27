# Afrobarometer IX — C-arm targeted repair and receiving

**Scope:** Afrobarometer Round 9 only. This continuation did not run or assign WVS7 work.

## Candidate and exact-head disposition

- Original arm-C stage-C packet SHA-256: `37ba49a5b34bcca1a9b2842112ce94df83cd5bf1f9c12a368734287dc49664c3`.
- Frozen source context includes the actual source-native SAV metadata for Q106C/D/E, Q48A/B, and Q53C. No respondent rows or claimed co-occurrence counts were supplied to workers.
- The initial C-arm review identified an addressee overclaim, unsupported threat-item relationship, Q48A typo/code distinctions, and omitted Q53C context.
- Sequential OpenCode repair sessions: `ses_de1139480ffeQnqEVkY2RlwD2a`, `ses_de110da7effeH3AWkRnzpP0IfM`, and the one-sentence wording repair `ses_de10ce4f1ffeEBzJw26vVcRMoe`.
- Fresh ancestry-bound stage chain is preserved in `afro-C-repaired-v2/C/`. Incumbent validator accepted O/D/C/R/I/S; the projection is `STRUCTURALLY_VALID_NOT_SEMANTICALLY_ADJUDICATED`.
- Independent reviewer first returned `CORRECTION_REQUIRED` on candidate v1 (`ses_de10dbae9ffetLJYiUc3r1eGkC`), because “co-occurrence is unobserved” could imply measured absence. That return is retained in `afro-C-repaired-v1/C/independent-receiving/`.
- Candidate v2 replaces 20 claims across O/C/R/I/S, leaves the literal “you” addressee unresolved for Q106C/D/E, removes directional threat claims, removes the “compartiot” typo, preserves Q48A's five substantive options and exact 93/94 special-code distinction, and adds a Q53C hold/exclusion rather than infer a relation.
- Exact candidate digest sent to independent receiving: `689e93f36acd42fd227bc0702751491d29eb9cea3c2d1a9029e2f477a215dd80`.
- Independent source-bound review returned `PASS_SCOPED` in session `ses_de10bdc3cffez1xtPitu60UCnd`; verdict covers the 20 listed claim repairs and Q53C hold only.

## Limits

No scientific or native acceptance, no observed respondent-level relationship, no interviewer-level linkage, no protected receiving, and no whole-factorial result are claimed. The C-arm's existing Q109F, Q28/Q29B, Q63B, Q97/Q98A, routing, and other evidence holds remain unresolved.

## Economy

Four sequential OpenCode Go calls used 17,958 input and 2,162 output tokens, with zero reported reasoning and 256 cache-read tokens; rate-equivalent estimate `$0.0038409`. Actual billed subscription usage and Codex-token cost are `UNOBSERVED`. Per-call receipts are in `AFRO_C_REPAIR_ECONOMICS.json`.
