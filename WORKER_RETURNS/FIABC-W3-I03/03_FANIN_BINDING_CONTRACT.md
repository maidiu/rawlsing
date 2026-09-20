# FIABC-W3-I03 — Fan-in Binding Contract

## Ownership separation

Truth owner:

    exact source + governed projection + source-backed C11 + unchanged I03/I05 authorities

Physical policy/cost owner:

    Candidate C / SOURCE_BACKED_HYBRID_WITH_REGENERABLE_ACCELERATORS

Frozen Candidate-C identity:

    owner commit  0b96b8de9aac774566f872cf0630ebd4ddeb70e6
    owner path    rawlsing_next/pre553_route_c_accelerators.py
    owner blob    abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889
    candidate     a476e6e44c21b8029ae5d3e6d387428a5fa19549a2126d61aae7c71c50c64a3c

The new production-binding module is not a replacement semantic owner and must not be entered into any authority registry as one.

## Runner consumption

For a current Candidate-C cell the integrated runner should select:

    builder = candidate_c_repository_builder_for_source(source_name)
    builder_identity = candidate_c_builder_identity(source_name)

and pass the exact authorized source incidence plus the exact governed projection to that builder.

The source-specific builder returns:

    (C11Repository, validated_release, candidate_c_binding_receipt)

The common repository/I03/I05 seam may consume the first two values. The third is candidate-local physical/provenance evidence and should be retained for replay/accounting qualification.

## LiTS-I

Current F02:

    permitted CACC identities = CACC1, CACC2
    fully applicable to exact current projection = none
    realization = exact-source-backed fallback

The runner must not interpret accelerator presence as reachability. It must not ask the frozen CACC1 stream to fabricate q310/q311.

## WVS7

Current WVS7:

    permitted CACC identities = none
    realization = exact-source-backed zero-accelerator

The runner must not import a LiTS CACC, create a WVS CACC, or relabel the cell Candidate B.

## Historical P2X reducer

The historical continuation reducer's WVS-C preserved-failure/skip branch and the backend's LiTS-C q310/q311 hard stop are superseded at the exact Candidate-C portability grain by the Wave-2 adjudication. They remain historical evidence and should not be edited in place. The integrated Wave-3 current successor court must bind executable C cells to the new production entrypoints.

## Negative state

Failure to satisfy exact source/projection/authority/replay determinants remains a typed Candidate-C/current-source failure. Accelerator absence alone is not such a failure.
