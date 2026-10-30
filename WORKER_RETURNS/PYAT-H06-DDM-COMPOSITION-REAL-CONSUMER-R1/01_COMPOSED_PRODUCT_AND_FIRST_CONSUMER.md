# H06 composed product and first consumer

## 1. AT10 modal/minority/counterpattern product

### Call graph

```
C1-02 synthetic source fiction (c1-at10-minority)
  -> rawlsing_next.pre553_discovery_exact.execute_exact_bounded_discovery
  -> three DiscoveryResultReceipts (G=A, G=B, G=C)
  -> rawlsing_next.pre553_analytical_composition.compose_positioned_subject_possibility(
         discovery_result=discovery, discovery_receipt_ref=receipt.ref)
  -> rawlsing_next.source_backed_positioned_subject_possibility.evaluate_positioned_subject_possibility
  -> PositionedSubjectPossibilityResult EXACT_SUPPORTED per branch
```

### Exact product

| Branch | Denominator | Composed identity | Consumer result |
|---|---:|---|---|
| G=A modal | 10 | `c1285c3d980271aee0f030ab1c08de51c72080fbed9ceb9597227248d31a8c90` | `EXACT_SUPPORTED`; result `2d2c15a2…` |
| G=B minority | 8 | `4f0f83af8cc0819e07a4c501dc4700a3fb45292465261a373f1cf0a4da1e3abf` | `EXACT_SUPPORTED`; result `1772d757…` |
| G=C counterpattern | 2 | `51557675ec53b443f02d1a25c1eee7c1188eeac9dc8e637ff446c4fa8dd8364c` | `EXACT_SUPPORTED`; result `8c9e52bb…` |

- Three distinct composed identities; no branch collapsed into the modal one.
- Denominated member refs: 10 / 8 / 2.
- Discovery receipt refs: `28273426…` (A), `8a6b92db…` (B), `de1053b6…` (C).
- Product path: `I05_EXACT_BOUNDED_TO_POSITIONED_SUBJECT`.

## 2. AT11 recursive-handoff product

### Call graph

```
C1-02 synthetic source fixture (c1-at11; 6 respondents)
  -> rawlsing_next.pre553_recursive_handoff.execute_exact_bounded_discovery_with_handoffs
  -> RecursiveBranchHandoff / DiscoveryBranchReplayBinding 3900f7b2…
  -> rawlsing_next.pre553_analytical_composition.compose_positioned_subject_possibility(
         recursive_handoff=handoff)
  -> rawlsing_next.source_backed_positioned_subject_possibility.evaluate_positioned_subject_possibility
  -> PositionedSubjectPossibilityResult EXACT_SUPPORTED
```

### Exact product

- Parent branch predicate: `7db282703ba51df15f3698d38212690911517e0668a108f1d9823ae8e24804ec`.
- Discovery receipt state: `DISCOVERED_RESULT_SUPPORTED`.
- Child producer query: `d1dcceb21871deff3b9ce796ca59c63fff1778246bfed15d33054c776a272062`.
- Child predicate: `d13e6334e07e00c465e4725f3da1ace73d8811b1ad1ce9441a8ca9d2e6d1ea1d`.
- Consumer query: `6f439e21f394be883a9e98eb0e516548d6f496a3cb14fa4534a207d3e14ae25a`.
- Witness: `67856e870a87d10041a585f158144b1ec79239c38e350e9ae9a5d871df0dfca3`.
- Model rule hash: `cf18f929767fed3ea36f4b25b25d071b4146767d64fd37d7b209d3399073105c`.
- Composed identity: `2a3924a3b6eb632b012ad9780c639db68ca14f4ea316b37ce49a03bd38a9848d`.
- Denominator: 4; denominator member refs: 4; complete cell geometry: two observed cells, each `2/4`; uncertainty `UNCERTAINTY_UNQUANTIFIED`.
- Recursive handoff ref: `3900f7b2cbc87c56b617548e7573ceb9a79527d2ed0475200fd553e1b640d577`.
- Recursive lineage: handoff ref plus parent branch predicate `7db28270…`.
- Coverage state: `RECURSIVE_DEPTH_CONTINUATION`.
- Consumer result: `EXACT_SUPPORTED`, result hash `0d81dae82e1fc1da7cd75a285a97ff8295625aaa3528461ccc0cb345d6bd4fa4`.

## 3. First consumer

Both products are consumed by the actual in-repository positioned-subject consumer:

`rawlsing_next.source_backed_positioned_subject_possibility.evaluate_positioned_subject_possibility`

It returns the exact result state and geometry. The composer does not manufacture a second consumer, and the H06 harness does not call a fixture constructor as a substitute for consumption.

## 4. Preserved functions

- Exact source/universe/release/target refs.
- Conditioning direction (AT10 G→Y; AT11 child branch→Y).
- Exact denominators and denominator member refs.
- Modal, minority and counterpattern alternatives (AT10 10/8/2).
- Recursive ancestry and immediate parent branch (AT11).
- Exact authority, provenance, dependency and replay refs in the result identity.
- Fresh-process replay equality for the recursive product.

## 5. Grade

The product is a **source-free synthetic fixture capability**. It is not original survey execution, live 35-wave occupancy, a new semantic-relation authority, or an actor/person claim. No production engine was added.
