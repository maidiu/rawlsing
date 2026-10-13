#!/usr/bin/env python3
"""Hostile RFA-06C2 no-provider speech and nonselective-smoke regressions."""
import re
import unittest
from unittest.mock import patch
from quote_invariant import quoted_contents, speech_quotation_matches
from run_cross_model_court import smoke_pass

def candidate(speech, prose):
    return {"atoms":[{"kind":"SPEECH","content":s} for s in speech],
            "realization_prose":prose}

class SpeechInvariant(unittest.TestCase):
    def assertSpeech(self, speech, prose, ok):
        self.assertEqual(speech_quotation_matches(candidate(speech,prose)),ok,
                         (speech,prose))
    def test_straight_double(self):
        self.assertSpeech(["The blue one first."], 'She said "The blue one first."', True)
    def test_curly_double(self):
        self.assertSpeech(["The blue one first."], 'She said “The blue one first.”', True)
    def test_straight_single(self):
        self.assertSpeech(["The blue one first."], "She said 'The blue one first.'", True)
    def test_curly_single(self):
        self.assertSpeech(["The blue one first."], "She said ‘The blue one first.’", True)
    def test_haiku_observed_shape(self):
        s="I'm finishing the blue one first. Ask me after we lock up."
        prose="'I'm finishing the blue one first. Ask me after we lock up.'"
        self.assertSpeech([s],prose,True)
        inherited_quoted=[a or b for a,b in re.findall(
            r'\u201c([^\u201d]*)\u201d|"([^"]*)"',prose)]
        self.assertEqual(inherited_quoted,[]) # the exact inherited false positive
    def test_internal_contractions(self):
        s="I'm not done; don't touch the corner's edge."
        self.assertSpeech([s],f"She said '{s}'",True)
        self.assertSpeech([s],f"She said “{s}”",True)
        curly="I’m not done; don’t touch the corner’s edge."
        self.assertSpeech([curly],f"She said ‘{curly}’",True)
    def test_two_exact_ordered(self):
        a,b="I'm here.","Don't move."
        self.assertSpeech([a,b],f"She said '{a}' and then “{b}”",True)
    def test_changed_word(self):
        self.assertSpeech(["The blue one."],"'The red one.'",False)
    def test_changed_punctuation(self):
        self.assertSpeech(["The blue one."],"'The blue one!'",False)
    def test_omitted(self):
        self.assertSpeech(["First.","Second."],"'First.'",False)
    def test_reversed(self):
        self.assertSpeech(["First.","Second."],"'Second.' then 'First.'",False)
    def test_extra_spoken_line(self):
        self.assertSpeech(["First."],"'First.' then 'Extra.'",False)
    def test_duplicate_unlicensed_speech(self):
        self.assertSpeech(["First."],"'First.' and 'First.'",False)
    def test_paraphrase(self):
        self.assertSpeech(["Ask me after we lock up."],"'Ask me later.'",False)
    def test_unquoted_speech(self):
        self.assertSpeech(["First."],"She said First.",False)
    def test_unclosed_quote(self):
        self.assertSpeech(["First."],"'First.",False)
    def test_possessive_nonquote(self):
        self.assertSpeech(["First."],"The workers' request was 'First.'",True)
    def test_no_speech_no_quotes(self):
        self.assertSpeech([],"She stood by the door.",True)
    def test_no_speech_extra_quote(self):
        self.assertSpeech([],"She whispered 'hello'.",False)

class SmokeContract(unittest.TestCase):
    def test_smoke_diagnostic_does_not_select_model(self):
        c={"model_smokes":[{"run_id":"CMHAIKU-SMOKE",
                             "model":"claude-haiku-5-5","case_id":"RF001"}]}
        rec={"status":"STRUCTURAL_INVALID","provider_message_id":"msg_test",
             "provider_returned_model":"claude-haiku-5-5",
             "requested_model":"claude-haiku-5-5",
             "schema_status":"EXACT_ORIGINAL_SCHEMA_VALID",
             "structured_candidate":{"fixture_id":"RF001"},
             "provider_schema_fixture_const":"RF001",
             "corrected_issues":["SPEECH_PROSE_EXACT_QUOTATION_MISMATCH"]}
        with patch("run_cross_model_court.latest",return_value=rec):
            self.assertTrue(smoke_pass(c,"claude-haiku-5-5"))
        rec["schema_status"]="EXACT_ORIGINAL_SCHEMA_INVALID"
        with patch("run_cross_model_court.latest",return_value=rec):
            with self.assertRaises(RuntimeError):smoke_pass(c,"claude-haiku-5-5")

if __name__ == "__main__":
    unittest.main()
