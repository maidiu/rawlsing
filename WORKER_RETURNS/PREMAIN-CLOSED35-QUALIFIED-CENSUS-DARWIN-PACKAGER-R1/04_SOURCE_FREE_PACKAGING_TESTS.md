# PREMAIN CLOSED35 Qualified Census Darwin Packager — Source-Free Packaging Qualification

Status: **GREEN**

Qualification method: `EXACT_GITHUB_BLOB_HOSTILE_REPLAY`.

This court did not open or decode any survey source. The qualification replay inspected the exact committed packager blobs together with the already-qualified frozen census harness and proved that every commissioned hostile condition reaches a fail-closed branch before an unauthorized measurement or commit can occur.

Exact blobs qualified:

- one-command wrapper: `803400b34fb9c611200c63601cc91953b741979c`
- estate-to-path-manifest bridge: `80c3e8dd10aff7ba5e6ce451c7f83e0b221e48ef`
- post-run receipt commit helper: `b4e9a53dcbfc6f6a70665c6f8b3eb3e8db7013c9`
- frozen census harness implementation: `b667f7198349486cec32d8168ddc2de1ed0427a8`

## Hostile matrix

| hostile condition | result | fail-closed witness |
|---|---|---|
| wrong `surveys.zip` carrier SHA | PASS | bridge recomputes full SHA-256 before opening archive |
| missing accepted archive member | PASS | exact member map requires count exactly 1 |
| altered extracted member | PASS | streamed extracted byte count + SHA-256 must equal canonical source identity |
| wrong LiTS-I alias bytes | PASS | carrier SHA/size gate plus staged `LiTS_I.dta` SHA/size gate |
| wrong WVS7 archive/member | PASS | archive root SHA/size gate plus exact member-name and staged SHA/size gate |
| incomplete 35-source staging | PASS | staged filename set must equal the exact 35-name canonical set |
| malformed/incomplete path manifest | PASS | generator requires exact IDs `01..35`; immutable existing manifest must byte-match regenerated canonical JSON |
| wrong harness branch | PASS | shell and Python guards both require the frozen harness branch |
| wrong harness head | PASS | shell and Python guards both require `efe8de2b032c93d1820fd3f8c82fe2f1acabbf87` |
| wrong qualified-code ancestry | PASS | `merge-base --is-ancestor 11704fb... HEAD` is mandatory |
| wrong OS | PASS | wrapper requires `Darwin` |
| wrong machine | PASS | wrapper requires `x86_64` |
| wrong CPython | PASS | runtime dictionary must equal CPython `3.11.3` exactly |
| wrong pyreadstat | PASS | runtime dictionary must equal pyreadstat `1.3.6` exactly |
| wrong pyarrow | PASS | runtime dictionary must equal pyarrow `25.0.1` exactly |
| existing conflicting immutable packaging state | PASS | manifest/binding immutable writes reject non-identical pre-existing bytes |
| existing conflicting immutable source receipt | PASS | frozen harness rejects receipt input drift before resume |
| output-root reuse with changed source identity | PASS | packager binding freezes 35 SHA/size identities; harness additionally binds receipt manifest hash |
| accidental raw `.sav`/`.dta`/archive inclusion in results commit | PASS | verifier and commit helper reject raw suffixes before Git staging |
| candidate / measured-P2X output inclusion | PASS | output-root allowlist plus explicit post-run filename rejection |
| Candidate A/B/C or measured-P2X import/dispatch in packager | PASS | exact blob replay found no candidate/measured execution import path |
| stock macOS Bash dependency trap | PASS | helper contains neither `mapfile` nor `seq`; Bash 3.2-compatible arithmetic/read loops are used |
| incomplete authoritative receipt tree | PASS | result verifier requires exactly 35 source receipts regardless of PASS/BLOCKED source status |
| result commit path spill | PASS | result helper allows exactly 35 receipt paths + six aggregate paths = 41 files |

Replay summary: **24/24 hostile obligations green; 0 failed**. The automated replay used 21 grouped assertions because the three independent runtime-version obligations share one exact runtime-dictionary equality gate.

The qualification is source-free. It proves packaging/rejection behavior and does **not** claim the authoritative 35-source representation census has already run.

No Candidate A/B/C, measured P2X, P3, or architecture-selection execution occurred.
