# D02Y — acquisition record and exact implementation trace (no substituted runtime)

## Official original-document browsing

1. [Ghana Parliament first Act 591 index](https://repository.parliament.gh/handle/123456789/1773) and [second Act 591 index](https://repository.parliament.gh/items/46e276d1-1a5e-4bc5-8d34-7cd8bbcbe3c1): official issuance attribution and published PDFs indexed; actual direct page for second `https://ir.parliament.gh/bitstream/handle/123456789/1774/CITIZENSHIP%20ACT.pdf?isAllowed=y&sequence=1` was exposed in search and yielded **403 on direct web open**. No source bitstream hash.
2. [Ghana BRR government Act PDF](https://www.brr.gov.gh/acc/registry/docs/Citizenship%20Act%20-%20ACT%20591.pdf): web-extracted 7 pages, visually inspected pages index 1 and 2 at §7; printed Gazette notice checked at PDF index 6 from extracted source text. Source reproduction includes copyright of DataCenta Ltd; Gov BRR metadata [conflicting Gazetted date](https://www.brr.gov.gh/reg_details.php?id=NzM4).
3. [Ghana Immigration Service Legal Handbook 2016](https://www.gis.gov.gh/wp-content/uploads/2024/02/Legal-Handbook-2016.pdf): inspected indexed Section 7 at PDF page 36 and Gazette notice at index 46. Genuine separate .gov.gh corroboration of visible wording; not necessarily editorially independent typesetting or certified current text.
4. [OSP original 1992 constitutional scan](https://www.osp.gov.gh/media/Resources/constitutionofghana.pdf): screenshot index 17 shows Article 6(2), printed spread pp.5–6. [OSP hosted Constitution/Promulgation Law](https://osp.gov.gh/media/Resources/Ghana_Constitution.pdf): source-extracted promulgation law section 1 records Constitution commencement 1993-01-07 (distinct from Act).
5. [Refworld law entry](https://www.refworld.org/legal/legislation/natlegbod/2001/27300) and [GhaLII law entry](https://ghalii.org/akn/gh/act/2000/591/eng%402001-01-05): confirm 2001 publication metadata, but are non-issuer statutory-commencement interpretations.

**Bytes:** Attempt to retrieve BRR PDF via container download failed; independent Python HTTPS fetch failed on DNS resolution. This is a retrieval/custody negative, **not** proof PDF does not exist. `pdf_sha256 = null` for every reviewed original document, no invented hash. Browser PDF text rendering does not supply certified file bytes.

## Exact pinned owner source reading (seal `08b490b2832f8b1ab6622a22557fcacb37a59db6`)

| Original code path | Git blob SHA from pinned fetch_file | Inspected decisive behavior |
|---|---|---|
| `rawlsing_next/pre553_structural_admission.py` | `fe8f706afbb5739d026846952681081b2937e9a8` | P06 function signature and I01 empirical query/fact identity/registry checks, lines 529+ |
| `rawlsing_next/m1_admitted_field_forge_relation_v554_ingress.py` | `0aeacd9e66c7e4340b36e1b622bb5c9bf2865fd5` | Admitted FF relation only; no law-document producer |
| `rawlsing_next/m4_v557_v558_publication_repository.py` | `8ec5c8e1c1a3cb7e998bb6cf0972ac87f396e360` | StructuralObject fields and payload-hash validation lines 217–282; V557 exact V553–V556 root restriction lines 573–585; `govern_v557` producer ceiling lines 506–530; producer locator closure lines 641+ |
| `rawlsing_next/prev3_objective_position_v557_v558_publication.py` | `7d2a5dbb3e0979c599632645867aa48a336a8e79` | source-limited J04 BEN0002 Q73A, no legal text |
| `rawlsing_next/objective_consumer_bounded_evidence.py` | `f30fca20e7b56e00348e82765d95f974b4b6a195` | caller-declared PolicyInput; OC05 NOT_YET_APPLICABLE |
| `PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/report/N_OBJECTIVE_PRE_V3_MAP.md` | `244a63d7f83eef04bb06c1753e3237ffeddf726f` | ordered classes of objective function, conditional production |
| `PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/nodes/N5.md`, `N6.md`, `N9.md` | pinned read, SHAs not retained in this row | actual producer/demand/permission/as-of gates |

See inherited `WORKER_RETURNS/PYAT-HQ280-PV3-D02-OBJECTIVE-PRODUCT-CANDIDATE-R1/02_ACTUAL_N5N6_TO_N9_PRODUCT_OR_HOLD.md` for actual source-free 18/18 unittest receipt **from D02**, not claimed to have been rerun by D02Y.

## Integrity and work boundary

No source original bitstream fetched to local container; no code execution or pytest claimed; no change to source runtimes, owner acceptance, semantic law, canonical controls, selected current state or branch outside assigned return. All JSON files are self-describing *candidate scientific dockets*, not active machine schemas.
