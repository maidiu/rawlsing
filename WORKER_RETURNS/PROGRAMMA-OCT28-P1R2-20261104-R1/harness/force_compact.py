"""Test-only adapter: exercise existing semantic courts on compact sealed releases."""
from dataclasses import replace
import os


def pytest_configure(config):
    from rawlsing_next.pre553_c11_repository import C11Repository
    from rawlsing_next._pre553_c11_execution_view import _compact_public_objects, _CompactPublicObjects
    original = C11Repository._commit_validated
    os.environ.pop("RAWLSING_C11_ACCELERATOR_DIR", None)
    def commit(self, release):
        if not isinstance(release.public_objects, _CompactPublicObjects):
            public = _compact_public_objects(release, physical_binding=lambda: None,
                                             projection_binding="independent-semantic-court")
            if public is not None:
                release = replace(release, public_objects=public)
        return original(self, release)
    C11Repository._commit_validated = commit
