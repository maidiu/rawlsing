"""Residual hostile finding: header-preserving selector omission.

The attacker post-processes a genuine direct certificate, removes one real event
and its selector/closure/occurrence rows, preserves the historical identity
headers, and recomputes both physical and logical roots. This is a self-asserted
root, not an externally held root; it therefore tests the direct installer's
additional sealed-release anchor, which currently checks only respondent census
and the self-asserted header.

Observed: cold verification accepts with the recomputed roots, the direct
installer accepts against the exact sealed release, and the native selector
returns 1 event where the sealed release requires 2.
"""

from dataclasses import replace
from pathlib import Path
import sqlite3
import tempfile

from rawlsing_next.tests.test_pre553_direct_i02_sourcefree import (
    _candidate, _build_direct,
)
from rawlsing_next.pre553_c11_ingest import ingest_c11_source_release
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next._pre553_external_i02_certificate import (
    DIRECT_SCHEMA, VerifiedExternalI02, _digest_file, _logical_root,
    install_direct_sourcefree_i02_i03,
)
from rawlsing_next._pre553_query_predicate import (
    _build_release_index, _select_respondent_events,
)
from rawlsing_next.pre553_empirical_objects import exact_ref


def main() -> None:
    candidate = _candidate("g5-selector-omission")
    universe = candidate.empirical_universes[0].ref
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        path = root / "direct.sqlite"
        roots = _build_direct(candidate, path, chunk_size=1)
        repo = C11Repository()
        admission = ingest_c11_source_release(candidate, repo)
        assert admission.accepted
        release = repo.resolve_release_exact(admission.release_ref)
        native = _build_release_index(release, universe)
        respondent = exact_ref(candidate.respondent_events[0].scoped_respondent_ref).key
        target = exact_ref(candidate.respondent_events[0].native_question_ref)
        native_refs = [
            event.ref.key
            for event in _select_respondent_events(
                native, respondent, target, native_only=True,
            )
        ]
        with sqlite3.connect(path) as db:
            rows = db.execute(
                "SELECT ref,respondent FROM main.objects "
                "WHERE family='RespondentEvent' ORDER BY ref"
            ).fetchall()
            victim_ref, victim_respondent = rows[0]
            assert sum(1 for row in rows if row[1] == victim_respondent) >= 2
            db.execute("DELETE FROM main.selectors WHERE event_ref=?", (victim_ref,))
            db.execute("DELETE FROM main.objects WHERE ref=?", (victim_ref,))
            db.execute("DELETE FROM main.closure WHERE ref=?", (victim_ref,))
            db.execute(
                "DELETE FROM main.event_occurrences WHERE event_ref=?", (victim_ref,)
            )
            db.commit()
            forged_logical = _logical_root(db, schema=DIRECT_SCHEMA)
        forged = replace(
            roots,
            logical=forged_logical,
            physical=_digest_file(path),
        )
        print("native_selected", len(native_refs), native_refs)
        with VerifiedExternalI02(path, roots=forged) as certificate:
            print("cold_verify", "ACCEPTED")
            install_direct_sourcefree_i02_i03(
                repo, admission.release_ref, universe, certificate,
            )
            print("direct_install", "ACCEPTED")
            installed = repo._i03_release_indices[(admission.release_ref, universe)]
            installed_refs = [
                event.ref.key
                for event in _select_respondent_events(
                    installed, respondent, target, native_only=True,
                )
            ]
            print("installed_selected", len(installed_refs), installed_refs)
            print("diverged", installed_refs != native_refs)


if __name__ == "__main__":
    main()
