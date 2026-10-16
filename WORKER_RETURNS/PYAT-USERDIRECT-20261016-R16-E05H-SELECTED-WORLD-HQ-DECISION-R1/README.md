# E05H return

Start with `00_DECISION_OR_PENDING.md`. Exact proposal: `COMPETENT_HQ_DECISION_RECORD_CANDIDATE.json`; issuer/reviewer/signature remain NULL. `AUTHORITY_MATRIX.json` and 03/04 distinguish local accession from prospective installation/issuer gates.

From this return directory on the same private repository's exact returned branch:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 repro/stage_sources.py
PYTHONDONTWRITEBYTECODE=1 python3 repro/execute_preview.py
PYTHONDONTWRITEBYTECODE=1 python3 repro/run_tests.py
PYTHONDONTWRITEBYTECODE=1 python3 repro/build_packet.py
PYTHONDONTWRITEBYTECODE=1 python3 repro/verify_return.py
```

`stage_sources.py` reads the exact 401 sourcefree Git blobs into ignored `inherited_e05a/runtime/`, verifying their NUL-header Git preimages and SHA256s. It needs those private repository objects; it never downloads original data. The inherited E05A wrapper and provenance objects remain byte-identical and independently checked by `source_manifest.json`. Its copied historical repro scripts are evidence; use the commands above for this return. The completed 403-case acceptance is retained under `inherited_e05a/frozen_E05S/junit/`, never rerun by these commands.

Fresh executed consumer evidence is `02_ACTUAL_OPT_IN_SOURCEFREE_CONSUMER_PREVIEW.json`; trace, stdout, JUnit and declared terminal are under `observations/`. Both actual consumers are original unmodified E04 clients, not operative OC05 or an actor. The preview requires literal `enabled=True` for each read. The CLI repro explicitly opts in only to test fixtures. Nothing installs, schedules, starts later work or changes canonical state. Reset by omitting opt-in; archive evidence grants no fresh use.

All authored files and ignored runtime staging stay inside this commissioned return. `artifact_sha256.json` binds the submitted evidence cut; `publication_receipt.json` binds its pushed commit by direct remote readback. The final receipt commit is reported after independent direct readback outside its own content to avoid a recursive SHA.
