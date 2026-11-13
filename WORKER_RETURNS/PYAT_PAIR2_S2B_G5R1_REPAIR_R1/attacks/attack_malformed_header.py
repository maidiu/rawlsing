"""Independent G5 attack: malformed direct-certificate header must refuse typed.

Threat model matches the accepted D3 test: the certificate bytes are modified and
the caller recomputes only the *physical* root; the externally held logical root
is unchanged. The cold verifier must reject the malformed certificate with
ExternalI02IntegrityError before any raw JSON/KeyError/TypeError escapes.
"""

from dataclasses import replace
from pathlib import Path
import shutil
import sqlite3
import tempfile

from rawlsing_next.tests.test_pre553_direct_i02_sourcefree import (
    _direct, _build_direct,
)
from rawlsing_next._pre553_external_i02_certificate import (
    ExternalI02IntegrityError, VerifiedExternalI02, _digest_file,
)


def main() -> None:
    candidate, _, _ = _direct("g5-malformed-header")
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        original = root / "original.sqlite"
        roots = _build_direct(candidate, original)
        cases = (
            ("invalid-json", "{not-json"),
            ("missing-key", None),
            ("json-null", "null"),
            ("json-number", "123"),
        )
        for label, value in cases:
            case = root / (label + ".sqlite")
            shutil.copyfile(original, case)
            with sqlite3.connect(case) as db:
                if value is None:
                    db.execute("DELETE FROM main.header WHERE name='coverage'")
                else:
                    db.execute(
                        "UPDATE main.header SET value=? WHERE name='coverage'",
                        (value,),
                    )
                db.commit()
            forged = replace(roots, physical=_digest_file(case))
            try:
                VerifiedExternalI02(case, roots=forged)
            except ExternalI02IntegrityError as exc:
                print(label, "TYPED_REFUSAL", type(exc).__name__, str(exc))
            except BaseException as exc:
                print(label, "UNTYPED_REFUSAL", type(exc).__name__, str(exc))
            else:
                print(label, "ACCEPTED")


if __name__ == "__main__":
    main()
