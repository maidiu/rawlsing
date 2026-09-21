# FIABC-LM2-R1J-A — Authority Usability Boundary

## Purpose

This packet establishes **upstream representation mechanics** only. It is deliberately not a Rawlsing authority issuance and deliberately does not fill R1I's missing WVS physical→native relation by itself.

## Positive propositions available to fan-in

The following upstream law may be consumed by HQ together with independently accepted premises:

1. In the SAV format as parsed by the exact ReadStat revisions bundled by pyreadstat 1.3.2 and 1.3.6, a variable declared numeric is represented to the client as `READSTAT_TYPE_DOUBLE`; a string variable is represented as string.
2. Every ordinary cell of such a SAV numeric variable, including a numerically integral cell, traverses the ReadStat `double_value` lane rather than being retyped as an integer because of its magnitude.
3. Numeric SAV user-defined missing declarations are themselves double-valued missing definitions.
4. With `user_missing=True`, pyreadstat preserves a ReadStat-defined SAV numeric user-missing value through the same numeric conversion path; system missing remains separate.
5. With `apply_value_formats=False`, pyreadstat does not substitute display/value-label text for the underlying numeric value.
6. pyreadstat maps the relevant ReadStat DOUBLE lane to `np.float64`/Python floating representation. In the accepted Rawlsing physical decoder, NumPy scalar `.item()` conversion yields the corresponding ordinary Python float without turning it into an integer.
7. These mechanics are materially identical for the relevant lane between exact pyreadstat 1.3.2 and 1.3.6, notwithstanding the different bundled ReadStat revisions.

The exact parity disposition is:

`REPRESENTATION_STACK_PARITY_PROVED__1_3_2_AND_1_3_6_EQUIVALENT_FOR_RELEVANT_SAV_NUMERIC_LANE`

## Conditional fan-in use

A lawful fan-in may instantiate this upstream law for Q291G5/Q291P5 **only if an independent accepted premise establishes that those exact source variables are SAV numeric variables under the governed source identity/decoder contract**.

Conceptually:

`exact source + exact variable proven SAV-numeric`
+
`exact pyreadstat/ReadStat representation law from R1J-A`
→
`that variable's SAV numeric cells are decoded through the DOUBLE/float lane`

This is a representation conclusion. It remains separate from source semantics.

If separate accepted source-semantic evidence states that a source-native response code is a numeric SAV code, HQ may use that evidence together with the exact representation law to construct a narrowly scoped representation binding. R1J-A does not perform that fan-in, choose its Rawlsing authority kind, or mint its authority reference.

## Hard negative limits

This packet does **not** prove or authorize any of the following:

- that Q291G5 or Q291P5 is numeric; R1J-A did not inspect WVS source metadata;
- that physical `float64 1.0` means WVS native response code `1`;
- that physical `float64 -1.0` means WVS native state `DK`, or any analogous special-state pairing;
- any global equivalence between Python `int 1` and `float 1.0`;
- any weakening of R5 typed physical equality or `physical_value_binding_key`;
- any coercion inside C11;
- any response semantics inferred from labels, frequencies, ordering, numeric resemblance, or downstream expectations;
- any canonical question mapping or native→canonical/program mapping;
- any cross-source semantic relation;
- any candidate A/B/C parentage or candidate-specific authority;
- any authority for system missing to enter a source-native representation binding.

System missing remains the separate ReadStat/pyreadstat system-missing path.

## Evidence-quality ledger

### Official/project documentation

- pyreadstat exact tagged `read_sav` docstrings define `user_missing` and `apply_value_formats` behavior for 1.3.2 and 1.3.6.
- pyreadstat exact tagged changelog establishes the bundled ReadStat lineage.
- IBM SPSS documentation independently corroborates the numeric-versus-string distinction and double-precision numeric storage.

### Exact implementation source

- ReadStat `src/spss/readstat_sav_read.c`: SAV variable classification, numeric row decoding, numeric missing-declaration reading.
- ReadStat `src/spss/readstat_spss.c`: numeric missing boxing/type and missingness construction.
- ReadStat `src/readstat_value.c`: numeric defined-missing comparison and double extraction.
- pyreadstat `_readstat_parser.pyx`: DOUBLE→`np.float64`, DOUBLE→Python float conversion, user-missing preservation, emitted metadata type.
- pyreadstat public reader/chunk wrapper: flag semantics and forwarding.

### Inference from implementation

The following are explicit implementation inferences, not quoted API promises:

- integral-valued numeric cells do not become integer-typed values because the SAV variable type controls the decoding branch;
- the endpoint ReadStat change set cannot alter this lane because the files/functions carrying its value/missing behavior are either byte-identical or unchanged in the relevant blocks, while the sole `readstat_sav_read.c` endpoint change is in multiple-response-name parsing;
- the pyreadstat 1.3.4 public-wrapper refactor and later typing changes do not alter the critical parser's DOUBLE/user-missing behavior.

## U09 change-boundary detail

The exact upstream ReadStat revisions differ:

- pyreadstat 1.3.2 stack: ReadStat `b2d5407d62caf3c33caadc0495c9f7684b6a0df7`;
- pyreadstat 1.3.6 stack: ReadStat `634f40a80d27221848ba57e9fb633b41146bac36`.

The upstream compare spans 21 commits. Within the relevant SAV representation path:

- `src/spss/readstat_spss.c` has identical endpoint blob `4bc7cde0813d379d59526e488b07135eeb99bb58`;
- `src/readstat_value.c` has identical endpoint blob `62aac39820184626df90451f0d999887d77ea884`;
- `src/spss/readstat_sav_read.c` differs at one endpoint line, changing only the `parse_mr_string` call to pass `ctx`; the numeric variable classification, double cell decoding, and numeric missing-value code blocks are unchanged.

Accordingly U09 is closed for the scoped lane. This is not a claim that all ReadStat behavior is identical across those revisions.

## Earliest lawful HQ use

R1J-A can be admitted as the upstream-decoder parent in the R1J fan-in court. It becomes sufficient to instantiate an exact WVS Q291 representation conclusion only when paired with the independently recovered exact-variable premise owned by R1J-B and whatever already-governed source-native semantic premise HQ lawfully selects.

Until that happens, R1I's prohibition remains intact:

`NO_RAW_VALUE_INFERENCE__NO_R15_RETRY_FROM_R1J_A_ALONE`
