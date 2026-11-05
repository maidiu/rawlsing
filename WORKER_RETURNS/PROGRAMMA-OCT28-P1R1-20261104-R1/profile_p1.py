"""Run the pinned E1 joined harness and record P1-specific resource counters."""
from collections import Counter
from contextlib import ExitStack, redirect_stdout
from functools import wraps
from importlib.util import module_from_spec, spec_from_file_location
from io import StringIO
import json
import os
from pathlib import Path
import sys
from time import perf_counter_ns
from unittest.mock import patch

profile_path, fixture = sys.argv[1:]
spec = spec_from_file_location("pinned_profile_oct28", profile_path)
profile = module_from_spec(spec)
spec.loader.exec_module(profile)

from rawlsing_next import pre553_c11_repository as repository
from rawlsing_next import pre553_physical_decoder as decoder
from rawlsing_next.pre553_empirical_objects import RespondentEvent

try:
    from rawlsing_next import _pre553_c11_execution_view as view
except ImportError:
    view = None

counts = Counter()
maxima = Counter()


def observe(module, name, observer):
    original = getattr(module, name)

    @wraps(original)
    def wrapped(*args, **kwargs):
        start = perf_counter_ns()
        output = original(*args, **kwargs)
        observer(args, output, perf_counter_ns() - start)
        return output

    return patch.object(module, name, wrapped)


def snapshot(_args, snapshot, _elapsed):
    counts["source_snapshot_opens"] += 1
    counts["source_snapshot_bytes_total"] += snapshot.size
    maxima["source_snapshot_bytes"] = max(maxima["source_snapshot_bytes"], snapshot.size)


def commit(args, _output, _elapsed):
    release = args[1]
    public = release.public_objects
    counts["repository_commits"] += 1
    maxima["public_object_count"] = max(maxima["public_object_count"], len(public))
    maxima["internal_record_count"] = max(maxima["internal_record_count"], len(release.internal_records))
    if view and isinstance(public, view._CompactPublicObjects):
        maxima["compact_event_count"] = max(maxima["compact_event_count"], len(public.lane.selectors))
        maxima["compact_event_body_arrow_bytes"] = max(
            maxima["compact_event_body_arrow_bytes"], public.lane.bodies.nbytes,
        )
    else:
        retained = sum(isinstance(obj, RespondentEvent) for obj in public)
        maxima["eager_event_count"] = max(maxima["eager_event_count"], retained)


def read(_args, result, elapsed):
    outcome = "miss" if result is None else "hit"
    counts[f"cache_{outcome}"] += 1
    counts[f"cache_{outcome}_ns"] += elapsed


def built(_args, _result, elapsed):
    counts["compact_view_builds"] += 1
    counts["compact_view_build_ns"] += elapsed


def materialized(_args, _result, _elapsed):
    counts["exact_event_reconstructions"] += 1


def observe_publication(original):
    @wraps(original)
    def wrapped(source, target, *args, **kwargs):
        if Path(source).name.startswith(".c11-events-"):
            active, staged = Path(target), Path(source)
            size = staged.stat().st_size
            existing = sum(member.stat().st_size for member in active.parent.glob("c11-events-*.parquet"))
            maxima["cache_temp_bytes"] = max(maxima["cache_temp_bytes"], size)
            maxima["cache_active_plus_temp_bytes"] = max(
                maxima["cache_active_plus_temp_bytes"], existing + size,
            )
            counts["cache_publications"] += 1
        return original(source, target, *args, **kwargs)

    return wrapped


stdout = StringIO()
with ExitStack() as stack:
    stack.enter_context(observe(decoder, "_acquire_source_snapshot", snapshot))
    stack.enter_context(observe(repository.C11Repository, "_commit_validated", commit))
    if view:
        stack.enter_context(observe(view, "_read_bodies", read))
        # The facade holds the actual imported function binding.
        stack.enter_context(observe(profile.facade, "_compact_public_objects", built))
        stack.enter_context(observe(view._EventLane, "materialize", materialized))
        stack.enter_context(patch.object(os, "replace", observe_publication(os.replace)))
    stack.enter_context(redirect_stdout(stdout))
    sys.argv[:] = [sys.argv[0], "joined", fixture, "--instrument"]
    profile.main()

record = json.loads(stdout.getvalue())
configured = os.environ.get("RAWLSING_C11_ACCELERATOR_DIR")
if configured:
    members = tuple(Path(configured).glob("c11-events-*.parquet"))
    maxima["cache_active_bytes"] = sum(member.stat().st_size for member in members)
    maxima["cache_active_members"] = len(members)
record["p1"] = {"counts": counts, "maxima": maxima}
print(json.dumps(record, sort_keys=True))
