import os
import sys
import tempfile
import pathlib
from dataclasses import replace

ROOT = os.environ.get("RAWLSING_ROOT", ".")
sys.path.insert(0, ROOT)

from rawlsing_next.tests.test_pre553_direct_i02_sourcefree import _direct
from rawlsing_next.pre553_empirical_objects import AuthorityRef, RespondentEvent
from rawlsing_next._pre553_direct_i02_sourcefree import build_sourcefree_direct_i02

candidate, _, source = _direct("probe-wrong-authority")
event = candidate.respondent_events[0]
fake = AuthorityRef("FAKE-AUTH", "1.0.0", "0" * 64)
changed = RespondentEvent(
    typed_state=event.typed_state,
    authority_snapshot_refs=(fake,),
    dependency_refs=event.dependency_refs,
    producer_replay_locator_or_reference_root=event.producer_replay_locator_or_reference_root,
    **dict(event.semantic_fields),
)
sections = dict(source.sections)
sections["RespondentEvent"] = iter((changed, *candidate.respondent_events[1:]))
try:
    build_sourcefree_direct_i02(
        replace(source, sections=sections),
        candidate.empirical_universes[0].ref,
        pathlib.Path(tempfile.mkdtemp(prefix="probe-wrong-auth-")) / "c.sqlite",
    )
except Exception as exc:
    print(type(exc).__module__ + "." + type(exc).__name__, str(exc)[:200])
else:
    print("ACCEPTED")
