# G1A portability Agent A installation report

Status: `G1A_PORTABILITY_AGENT_A_KNOWN_CORPUS_INSTALL_COMPLETE`

This is a deterministic installation and provenance return, not a finding of semantic authority, historical completeness, or G1A/P9/C1-C6/P10 closure.

## Branch control

- Starting branch: `agent/g1a-github-portability-install-r1`
- Starting commit: `9b65e0232916f660d9a0bc343b01e94e438e2cbb`
- Resulting branch: `agent/g1a-github-portability-install-r1`
- Resulting installation commit: `9f684ba8bedaf72da6bc74435d73d9670ef3280d`

The named coordination ref was checked before writes and currently resolved to `f805c6a0f79f00f66e1ecd7949a8bf05f707249c`; the mandated pinned commit remained fetchable and was used exactly. No files were written to the artifact workspace, `main`, live Trii, the coordination branch, or any C1-C5 execution branch.

## Carrier verification

| Carrier | Expected SHA-256 | Observed SHA-256 | ZIP integrity |
|---|---|---|---|
| `Rawlsing_G1A_GitHub_Portability_R1_CORE_20260826.zip` | `98326813914573a502f9b55b7c23418a181e31c8aed048380882f27649ee76a6` | `98326813914573a502f9b55b7c23418a181e31c8aed048380882f27649ee76a6` | PASS |
| `Rawlsing_G1A_GitHub_Portability_R1_C4_20260826.zip` | `9668ca0951662fd79a7678297d8f10ff463cf21860667d1d4331107b32eaf95e` | `9668ca0951662fd79a7678297d8f10ff463cf21860667d1d4331107b32eaf95e` | PASS |

All 13 manifest-supplied ready objects matched their top-level SHA identities before extraction or copy. All 10 nested ZIPs passed integrity testing. The four duplicated control files across carriers were verified byte-identical.

## Installed corpus

- Exact installed objects: 12
- Derived portability representations with exact provenance: 1
- Integrity/size blocked objects: 0
- Internal provenance or evidence-manifest member hashes validated: 428
- Exact GSS source reconstructed from nine header-repeated CSV parts: SHA-256 `43d3f835bc4137060ddc1a84f36c47a320c8d99cb9585b33e7fc1cc6d3289de3`
- Ordinary Git objects at or above 95 MiB: 0

The original V550 response-option archive is retained under C1 raw archives. Its exploded C1 inspection representation is separately marked derived and is not presented as a replacement authority object. All nested transfer archives, source members, roles, ceilings, and reconstructability notes are recorded in [SOURCE_PROVENANCE.tsv](99_PROVENANCE/SOURCE_PROVENANCE.tsv); the installation disposition is in [PORTABILITY_INSTALL_LEDGER.tsv](PORTABILITY_INSTALL_LEDGER.tsv).

## Deliberately referred to Agent B

The following manifest §4 historical SHA-located recovery targets were deliberately not searched by Agent A: the C1 nine-family archive; C2 SWID binding/code; C3 V525b driver/semantic and d62 carriers; C4 historical strategy/spec artifacts; and C5 R184 bundle/dump. Their absence from the two supplied transfer carriers is not a `NOT_FOUND` finding. The ledger preserves them as `BLOCKED_OTHER` solely to mark the jurisdiction boundary, not an integrity failure or adjudication.

Accordingly:

`G1A_GITHUB_PORTABILITY = PARTIAL__SHA_PINNED__CODEX_MIRROR_REQUIRED`

G1A_PORTABILITY_AGENT_A_COMPLETE__RETURN_FOR_CROSS_AGENT_ADJUDICATION__NO_G1A_CLOSURE
