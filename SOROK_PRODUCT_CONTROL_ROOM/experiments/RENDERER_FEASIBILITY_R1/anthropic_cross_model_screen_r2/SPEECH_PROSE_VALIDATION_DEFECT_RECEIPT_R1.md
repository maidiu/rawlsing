# SPEECH_PROSE_VALIDATION_DEFECT_RECEIPT_R1

**Source-level disposition: CONFIRMED.** Startup `b4fd4855c1b7608d06481b5ac55f577af1476e06`; inherited `anthropic_court_r2/court_common_r2.py::deterministic_candidate`.

The inherited checker computes `speech = [a.get("content") for a in atoms if a.get("kind") == "SPEECH"]` then extracts only `“...”` and `"..." ` through `re.findall(r"\u201c([^\u201d]*)\u201d|\\"([^\\"]*)\\"", prose)`, finally comparing `quoted != speech` and emitting `SPEECH_PROSE_EXACT_QUOTATION_MISMATCH`. Ordinary/curly single quotation delimiters are absent from the pattern.

**Minimal exact reproduction:** atom `I'm finishing the blue one first. Ask me after we lock up.`; prose `'I'm finishing the blue one first. Ask me after we lock up.'`. Inherited extraction returns `[]`; the true atom list contains that string. Hence false rejection is unavoidable despite exact character identity. This is a source-level counterexample; the *owner-local actual Haiku receipt is not in this GitHub branch*.

**Authority:** `lab_fixture/CLAUDE_ACTOR_REALIZATION_CONTRACT_R1.md` binding invariant 7 and `OBJECTIVE_OCCURRENCE_OUTPUT_SCHEMA_R1.json` SPEECH content description require byte-identical speech in corresponding quotation and order. Neither prescribes a particular quotation delimiter. The word *quotation* still requires enclosure, so unquoted narration is not granted automatic eligibility.

**Successor post-generation check:** `quote_invariant.py` scans straight/curly double and straight/curly single enclosures, skips apostrophes between alphanumeric letters, disallows single-quote openers immediately following a letter (e.g. workers'), and compares the entire extracted quotation sequence to the speech-atom contents. Same order, exact punctuation/case, no omission, no extra quoted line. Nested exotic quotations remain a known narrow syntax edge; they are not silently normalized to approximate matches.

**Historical evidence:** `original_r2_issues` retains inherited code unchanged; `corrected_issues` removes its speech mismatch only after successor check independently passes. Given the reported exact shape, corrected result is `SCHEMA_VALID` *if and only if* no other corrected issue exists. Actual result is conditioned on authentic private receipt inspection. No prior raw response or candidate is rewritten.

**Tests:** `test_quote_and_smoke_r2.py` includes all four delimiter styles, literal Haiku shape, contractions, multi-atom order, changed word/punctuation, omitted/reversed atoms, extra utterance, paraphrase, repeated unsupported quotation, no-speech and malformed quotation controls.
