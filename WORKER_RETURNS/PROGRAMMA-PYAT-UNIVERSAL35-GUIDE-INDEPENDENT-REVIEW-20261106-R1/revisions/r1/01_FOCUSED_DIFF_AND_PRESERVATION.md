# 01 — Focused r1 diff and preservation notes

## Diff

`git diff 6a5f1ab3e..6c243ffee` changes only:

- master recovery `00`, function priority `02`, existing work agenda;
- `COMPONENT_STATUS.jsonl`, `CURRENT_SEAM_STATES.jsonl`;
- author guide-currentness return.

Eight added lines in each of three documents (the four corrections), four changed
JSON overlay rows in each of the two status files, and author return text. No
other path changed.

## C verification

- Existing commit is `30bd02a10feb1b5b97bcbe70e3981f482d2a412c` (parent
  `d119045f…`), not `0bd02a10…` from the prior review transcript.
- Its production view blob is `986f327aa18053edc61bd837cdded02bbf8388d9`.
- Protected `4df35cba8` view is `de5613301eb54aefaccb002e3c8dc4c657885479`; the
  C blob is donor-identical to accepted compressed code but not protected there.
- F `ebd20c165bb275f66e4b3e2210535e96eecaf2ac` is the independent scoped
  sourcefree acceptance.

## B/C/D/ABI details

- B `dd0249a0` actual planned F2/F3/F4 payload not consumed by
  `compile_governed_frontier`; B/AB/ABC joined seams REVISE.
- D reuses original B author ownership for live binding repair/original execution
  in `pre553_original35_operations.py` / `pre553_original35_execution.py`; actual
  native I03/I05/Batch and original N10E/FF first-reader proof pending.
- `SourceConfigLibrary.select(...)` is compact metadata, not validated
  `SourceConfig` or B config input; `SourceConfigLibrary.load_original(sid).document`
  is the full validated caller path.

## Preservation

- Five #705 dossier bodies: no missing original lines; binding `03` body
  untouched.
- 62 components / 82 seams: IDs equal; stripping only
  `nov06_universal35_candidate_currentness` yields 0 non-overlay diffs. 13/11
  overlays remain; four rows each receive the corrections.
- Graph 51/82/88/13 unchanged; FIABC 144/3, routing 676/4,705/249, old E negative
  `e714`, candidate/authority/native grades retained.
- No product, `CURRENT_PROGRESS`, controller, Sorok product, frozen graph, or
  binding-03 edit.
- Pinned frontdoor validator passes; S2/S3 NOT_RUN.
