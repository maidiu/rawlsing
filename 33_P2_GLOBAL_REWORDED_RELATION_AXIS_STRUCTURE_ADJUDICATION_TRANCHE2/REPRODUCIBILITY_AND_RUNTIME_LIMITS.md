# Reproducibility and runtime limits

`rebuild_tranche2_authority_surfaces_in_place.py` regenerates the tranche-2 CSV/JSON authority surfaces from the delivered section-32 inputs and the section-33 `SOURCE_*` files. It deliberately leaves DOCX files, restart controls, manifests, and hashes untouched; regenerate those only after reviewing the rebuilt surfaces.

The historical full-package builder is retained as an exact task return. Its outer copy/build paths reflect the original execution environment. The in-place rebuild wrapper removes that dependency for the authority surfaces.

The V552→V552J sidecar adapter is synthetically tested only. This handoff lacks the live V552 `question_semantic_hierarchy` and V552J run artifacts needed to install and execute the retrofit. Runtime repair therefore remains open and must fail closed on duplicate join keys or conflicting non-empty values.
