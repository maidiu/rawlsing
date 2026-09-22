# Required hostile tests — Asian Barometer runtime admission

These are required tests for a future Asian PRE553 runtime-package court. They are specified here only; this worker did not execute them.

## Cross-wave generic hostile tests

1. **typed numeric nonintersection**
   - Construct a governed response rule with an integer typed key and a physical cell with numerically equal float representation.
   - Require nonintersection unless an explicit representation successor authorizes a transform.
   - Repeat inverse direction.
   - This test is mandatory for all three waves and priority-critical for W1.

2. **representation form ignored by consumer**
   - Give two physically/substantively similar values different governed representation forms.
   - Require the consumer to honor the form-specific authority and reject fallback by apparent equality.

3. **dynamic query ref absent from static catalog**
   - Mint a derived query from an admitted template/predicate.
   - Remove the derived preimage while retaining the ref.
   - Require fail-closed; static template catalog resolution must not reconstruct it.

4. **I05 fact ref retained but fact preimage dropped**
   - Retain receipt refs/states but delete one exact fact object required by constituent packaging.
   - Require postconsumer failure before candidate or terminal qualification.

5. **historical authority replaced by ambient current file**
   - Change the current path target while preserving the historical dependency ref.
   - Require dependency identity failure rather than ambient-current substitution.

6. **runtime catalog successor outside frozen scope**
   - Introduce a valid-looking successor object not admitted by the package's frozen catalog scope.
   - Require rejection.

7. **source-specific terminal state replaced by generic field**
   - Replace bounded UNKNOWN / user-missing / ordinary storage / MR-specific state with a generic missing/N/A field.
   - Require terminal/postconsumer rejection.

8. **shape-only truth claim**
   - Supply a structurally valid source-module/runtime package with no qualified source receipt.
   - Require failure of any claim asserting real-source equivalence, certification, or substantive closure.

## Wave 1 hostile tests

9. **BIG-5 reader identity drift**
   - Package W1 under any reader identity other than the exact authorized source-declared BIG-5 successor.
   - Require fail-closed.

10. **compatibility override invention**
    - Attempt to replace W1 source-declared decoding with an explicit compatibility encoding override.
    - Require rejection unless separately authorized by an exact successor.

11. **decoded text promoted to semantic authority**
    - Feed readable decoded labels into response/routing construction without documentary authority.
    - Require rejection.

12. **user-missing -> observed response collapse**
    - Use q001 stored 98 with its declared user-missing state.
    - Attempt to bind it as an ordinary observed substantive value because 98 is positive/numeric.
    - Require rejection.

13. **system/user missing collapse**
    - Make q018_1 system missing and q001 user missing share one generic missing key/state.
    - Require rejection.

14. **native ID replay substitution**
    - Replace source SHA + row ordinal with idnumber or country+idnumber.
    - Require rejection even where a packet-level pair happens to be injective.

15. **nine-weight default invention**
    - Preserve all nine carriers, then select any one (including w_all) as default based only on name/existence.
    - Require rejection.

16. **q097 ranked flattening**
    - Reorder, deduplicate, or scalarize q097_1/q097_2/q097_3.
    - Require rejection.

17. **W1 routing inferred from missingness/country/text**
    - Attempt to create row applicability from physical missingness, decoded text, or country support.
    - Require authority-blocked result.

## Wave 4 hostile tests

18. **ordinary -1 -> missing coercion**
    - Bind raw -1 as SYSTEM_MISSING or USER_MISSING.
    - Require rejection.

19. **global -1 semantics**
    - Assign one semantic state to -1 across all W4 variables.
    - Require rejection.

20. **merged/instrument geography collapse**
    - Treat merged `country` codes as if they were `SE1` documentary codes.
    - Require rejection.

21. **q172 exact membership fabricated from ASEAN scope**
    - Convert the documentary phrase `ASEAN_COUNTRIES_ONLY` into exact row membership without an admitted membership preimage.
    - Require rejection.

22. **q172 routing inferred from -1 incidence**
    - Use ordinary -1 as not-asked/inapplicable evidence.
    - Require rejection.

23. **ranked families flattened**
    - Reorder/scalarize q20/q21/q22 or q99/q99a/q99b.
    - Require rejection.

24. **w/w_cross alias**
    - Treat w and w_cross as one carrier because vectors, names, or values look related.
    - Require rejection.

25. **default W4 weight invented**
    - Select w or w_cross without exact estimand/default authority.
    - Require rejection.

## Wave 5 hostile tests

26. **native ID collision replay test**
    - Construct duplicate COUNTRY+IDnumber rows with different row ordinals.
    - Require distinct replay identities.

27. **MR set flattening**
    - Remove a set, member, or counted-value declaration from IR3a/Q112/SE15.
    - Require rejection.

28. **Q112/SE15 collapse by overlap**
    - Merge Q112 and SE15 because SE15A..SE15M overlap.
    - Require rejection.

29. **native MR Q112 -> questionnaire Q112 name inference**
    - Assert same semantics from string equality.
    - Require rejection.

30. **India module routing inferred from country**
    - Use COUNTRY alone to mint exact Q106c/d/e applicability.
    - Require authority-blocked result.

31. **q186 exact membership fabricated from ASEAN scope**
    - Build exact row membership without an admitted risk-set preimage.
    - Require rejection.

32. **q186/India routing inferred from ordinary -1**
    - Use -1 incidence as routing authority.
    - Require rejection.

33. **geography harmonization invention**
    - Map raw COUNTRY to generic instrument/cross-wave geography without exact reconciliation authority.
    - Require rejection.

34. **default W5 weight invented**
    - Select w as analytical default based only on presence/name.
    - Require rejection.

## Whole-source hostile tests

35. **declared R35 dimensions but missing receipt**
    - Provide the source-specific R35 hook declarations without a qualified whole-source physical-equivalence receipt.
    - Require any whole-source equivalence claim to fail.

36. **missing physical dimension**
    - For each wave, remove one required declared physical dimension from the candidate whole-source realization.
    - Require equivalence failure.

37. **candidate semantics diverge**
    - Keep physical source root constant but mutate candidate C's source-specific realization identity.
    - Require common semantic-law failure.

38. **bounded UNKNOWN promoted**
    - Replace any authority-blocked field with a guessed semantic value while preserving shape.
    - Require rejection.

## Test boundary

Passing these synthetic tests would prove implementation discipline only.

It would not prove:

- real-source decoder representation;
- whole-source physical equivalence;
- exact authority-blocked routing/risk sets;
- source certification;
- ABC execution parity;
- I05 PASS;
- measured P2X.

