"""RFA-06C2 exact speech-to-prose quotation invariant (post-generation only).

RFA-05 demands identical utterance content in corresponding prose quotation and
atom order. The surrounding quotation glyphs are typography, not utterance.
Do not accept paraphrases, unquoted utterances, reordering, or added quotations.
"""
from __future__ import annotations

PAIRS = {'"': '"', '\u201c': '\u201d', "'": "'", '\u2018': '\u2019'}

def _inner_apostrophe(s, pos):
    return (s[pos] in ("'", "\u2019") and 0 < pos < len(s)-1
            and s[pos-1].isalnum() and s[pos+1].isalnum())

def quoted_contents(prose):
    """Return quote bodies in order, or None on an unclosed quotation.

    A single quote following a letter is not an opening delimiter (workers'
    rights); an apostrophe between letters is not a closing delimiter (I'm,
    don't, corner's, I’m). Double and curly quotes retain exact body bytes.
    """
    if not isinstance(prose, str):
        return None
    values = []
    i = 0
    while i < len(prose):
        opener = prose[i]
        if opener not in PAIRS:
            i += 1
            continue
        if opener in ("'", "\u2018") and i and prose[i-1].isalnum():
            i += 1
            continue
        closer = PAIRS[opener]
        start = i + 1
        j = start
        while j < len(prose):
            if prose[j] == closer and not _inner_apostrophe(prose, j):
                values.append(prose[start:j])
                i = j + 1
                break
            j += 1
        else:
            return None
    return values

def speech_quotation_matches(candidate):
    if not isinstance(candidate, dict):
        return False
    atoms = candidate.get("atoms")
    if not isinstance(atoms, list):
        return False
    speech = []
    for atom in atoms:
        if not isinstance(atom, dict):
            return False
        if atom.get("kind") == "SPEECH":
            content = atom.get("content")
            if not isinstance(content, str):
                return False
            speech.append(content)
    observed = quoted_contents(candidate.get("realization_prose"))
    # Exact sequence rejects missing/changed punctuation, reversed utterances,
    # paraphrase, duplicated quotations, and unsupported extra spoken lines.
    return observed is not None and observed == speech
