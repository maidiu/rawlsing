"""Review-only R4 adapter revocation/order witness on the sealed R2 estate."""
from __future__ import annotations
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117')
ADAPTER = ROOT / 'R4_LOCALITY_EXPERIMENT'
sys.path.insert(0, str(ADAPTER))
sys.path.insert(0, str(ROOT.parents[1]))
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate

def main(argv):
    if len(argv) != 2:
        raise SystemExit('usage: revocation_witness.py <proofroot>')
    proofroot = Path(argv[1]).resolve()
    contract = json.loads((ROOT/'R2_PILOT/fixture_contract_pilot.json').read_text())
    e = contract['estate']
    grant = {'ok': True}
    estate = VerifiedDirectEstate(
        e['root'], exact_path=e['exact_path'],
        independently_held_manifest_sha256=e['manifest_sha256'],
        independently_held_i02=ExternalI02Roots(**e['i02']),
        current_authorizer=lambda _roots: grant['ok'],
    )
    import locality_adapter
    original = locality_adapter.install()
    try:
        with DirectEstateI03Session(estate) as session:
            respondent = next(iter(session.respondents))
            gen = session._respondent_family('RoutingEligibilityFact', respondent)
            first = next(gen)
            first_ref = first.ref.key
            grant['ok'] = False
            try:
                second = next(gen)
                adapter_second_error = None
                second_ref = second.ref.key
            except Exception as exc:
                adapter_second_error = f'{type(exc).__name__}: {exc}'
                second_ref = None
    finally:
        locality_adapter.restore(original)
    # Original path must check current between yields and refuse.
    grant['ok'] = True
    estate2 = VerifiedDirectEstate(
        e['root'], exact_path=e['exact_path'],
        independently_held_manifest_sha256=e['manifest_sha256'],
        independently_held_i02=ExternalI02Roots(**e['i02']),
        current_authorizer=lambda _roots: grant['ok'],
    )
    with DirectEstateI03Session(estate2) as session2:
        respondent2 = next(iter(session2.respondents))
        gen2 = session2._respondent_family('RoutingEligibilityFact', respondent2)
        first2 = next(gen2)
        first2_ref = first2.ref.key
        grant['ok'] = False
        try:
            second2 = next(gen2)
            original_second_error = None
            second2_ref = second2.ref.key
        except Exception as exc:
            original_second_error = f'{type(exc).__name__}: {exc}'
            second2_ref = None
    out = {
        'schema': 'ANVIL_CUT2_LOCALITY_REVOCATION_WITNESS@1',
        'sealed_estate_manifest': e['manifest_sha256'],
        'family': 'RoutingEligibilityFact',
        'first_ref': first_ref,
        'adapter_second_ref': second_ref,
        'adapter_second_error': adapter_second_error,
        'adapter_bypassed_revocation_between_yields': adapter_second_error is None and second_ref is not None,
        'original_first_ref': first2_ref,
        'original_second_ref': second2_ref,
        'original_second_error': original_second_error,
        'original_refused': original_second_error is not None,
        'fixture_note': 'sealed R2 sourcefree estate; no product edits; target adapter read-only',
    }
    (proofroot/'locality_revocation_witness.json').write_text(json.dumps(out,indent=2,sort_keys=True),encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0

if __name__ == '__main__':
    raise SystemExit(main(__import__('sys').argv))
