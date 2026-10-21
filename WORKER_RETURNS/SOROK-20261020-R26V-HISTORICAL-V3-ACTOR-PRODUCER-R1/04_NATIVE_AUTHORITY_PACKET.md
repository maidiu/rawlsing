# R26V native authority packet

`candidate/native_ports.NativeHistoricalActorPorts` fails closed with `NATIVE_AUTHORITY_UNISSUED` for every port. No actual native actor, source, encounter, E1, rule, target/grant, memory, E2, C8 trust, Pyat or C11 is issued.

| Port | Exact competent owner | Required artifact |
|---|---|---|
| ADP007 actor genesis | ADP007 owner | real actor genesis/initialization record |
| ADP010 opportunity/encounter | ADP010 owner | AVAILABLE + actual OPPORTUNITY/ENCOUNTER provenance |
| ADP015 independent relation/genealogy | ADP015 owner | separate relation/parent issuance; no inferred parent |
| ADP016 memory / ADP017 knowability | ADP016/017 owner | memory and knowability decisions |
| ADP019 E1 | External Admission Court | real E1 admission receipt and source-owner provenance |
| CAN008 Rule A | CAN008 rule issuer | exact rule body/hash/currentness |
| CAN011 T/grant | separate CAN011 target owner | exact target rule and separate grant |
| C8 D1/D2/D3 | protected trust custodian | writer custody, external anchor/key, signer/antirollback |
| Pyat N11/N12 | Pyat HQ | R53 STOP; original-world use unresolved |
| C11 weld | C11 authority | native weld decision |
| Original source/host/purpose | original source custodian | current tranche; no synthetic substitution |

Native intake must remain closed until these exact documents/IDs are supplied. No self-issuance; no M2/MP parent claim without actual parent.
