import os
import sys
import tempfile
import threading
import time
import tracemalloc
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, os.environ.get("RAWLSING_ROOT", "."))

from rawlsing_next.tests.test_pre553_direct_i02_sourcefree import _direct
from rawlsing_next._pre553_direct_i02_sourcefree import build_sourcefree_direct_i02
from rawlsing_next._pre553_external_i02_certificate import VerifiedExternalI02
from rawlsing_next.pre553_empirical_objects import RespondentEvent, exact_ref

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
candidate, _, base_source = _direct("s2b-scale-%d" % N)
base = candidate.respondent_events[0]
counts = dict(candidate.source_release_manifest.declared_record_counts_by_logical_family)
counts["RespondentEvent"] = N
manifest = replace(candidate.source_release_manifest,
                   declared_record_counts_by_logical_family=counts)

def events():
    for i in range(N):
        yield RespondentEvent(
            typed_state=base.typed_state,
            authority_snapshot_refs=base.authority_snapshot_refs,
            dependency_refs=base.dependency_refs,
            producer_replay_locator_or_reference_root=base.producer_replay_locator_or_reference_root,
            **{**dict(base.semantic_fields),
               "response_event_id_or_deterministic_index": "scale-%08d" % i},
        )

sections = dict(base_source.sections)
sections["RespondentEvent"] = events()
source = replace(base_source, manifest=manifest, sections=sections)
universe = candidate.empirical_universes[0].ref
work = Path(tempfile.mkdtemp(prefix="s2b-scale-"))
scratch = work / "scratch"
scratch.mkdir()
os.environ["SQLITE_TMPDIR"] = str(scratch)
target = work / "cert.sqlite"

def tree_bytes(path):
    total = 0
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat(follow_symlinks=False).st_size
            except OSError:
                pass
    except OSError:
        pass
    return total

peak = {"scratch": 0, "stage": 0}
stop = threading.Event()
def sampler():
    while not stop.is_set():
        s = tree_bytes(scratch)
        t = sum(tree_bytes(p) for p in (work, Path("/tmp")) if p.is_dir())
        peak["scratch"] = max(peak["scratch"], s)
        peak["stage"] = max(peak["stage"], t)
        time.sleep(0.05)
thread = threading.Thread(target=sampler, daemon=True)
thread.start()

tracemalloc.start()
started = time.monotonic()
roots = build_sourcefree_direct_i02(source, universe, target, chunk_size=2048)
build_s = time.monotonic() - started
live, peak_python = tracemalloc.get_traced_memory()
tracemalloc.stop()
stop.set(); thread.join()

started = time.monotonic()
with VerifiedExternalI02(target, roots=roots) as certified:
    respondent = exact_ref(base.scoped_respondent_ref).key
    question = exact_ref(base.native_question_ref)
    selected = sum(1 for _ in certified.selector_refs(respondent, question, native_only=True))
    respondents = sum(1 for _ in certified.respondent_refs())
cold_s = time.monotonic() - started

print({
    "n_events_decoded": N,
    "respondents": respondents,
    "selected_postings": selected,
    "retained_sqlite_bytes": target.stat().st_size,
    "retained_workdir_bytes": sum(tree_bytes(p) for p in (work, Path("/tmp")) if p.is_dir()),
    "max_scratch_tree_bytes_sampled": peak["scratch"],
    "max_tmp_plus_workdir_bytes_sampled": peak["stage"],
    "build_s": round(build_s, 3),
    "cold_verify_plus_select_s": round(cold_s, 3),
    "python_builder_peak_bytes": peak_python,
    "process_maxrss_kb": __import__("resource").getrusage(
        __import__("resource").RUSAGE_SELF).ru_maxrss,
    "workdir": str(work),
})
