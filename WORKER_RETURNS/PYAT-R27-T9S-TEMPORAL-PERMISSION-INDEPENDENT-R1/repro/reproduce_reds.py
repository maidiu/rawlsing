"""T9S Phase A — physically reproduce the T9R REDs on the pinned T9C adapter.

Writes the raw counterexample observations so the preregistered REDs are backed
by actual adapter outputs, not documentary restatement.
"""
import json
import sys
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
PINCAND = (RET.parent / "PYAT-R26-T9R-INDEPENDENT-TEMPORAL-DELTA-R1"
           / "phase_b" / "pinned_candidate")
sys.path.insert(0, str(PINCAND))

import t9b_temporal as T  # noqa: E402


def wave(name, year, value, **kw):
    f = dict(wave_id=name, source_family='ACTUAL_SOURCE', country='SYNTH_COUNTRY_A',
             instrument='SYNTH_INSTRUMENT', edition='E1', cohort='COHORT_ALL',
             observation_year=year, published_year=year, value=value)
    f.update(kw)
    return T.Wave(**f)


def case(waves, **kw):
    return T.TemporalCase(case_id='T9S', country='SYNTH_COUNTRY_A',
                          waves=tuple(waves), target_year=1995, **kw)


WORLD = T.StructuralWorld('SAME_WORLD', ('ROUTE_PARTICIPATION', 'ROUTE_DEFERRED_REVIEW'),
                          (), 'INSTITUTION')
GRANTED = T.StructuralWorld('SAME_WORLD', ('ROUTE_PARTICIPATION', 'ROUTE_DEFERRED_REVIEW'),
                            ('GRANT_YOUNG_PERSON_ACCESS',), 'INSTITUTION')

reds = {}

# F1 unused future upgrade
reds['F1_unused_future_upgrade'] = {}
for m in (T.METHOD_M0_HOLD, T.METHOD_M2_BACKOFF):
    before = T.read_selected_world(GRANTED, case([wave('W0', 1990, .2)]), m, 1995, retrospective=True)
    after = T.read_selected_world(GRANTED, case([wave('W0', 1990, .2), wave('W1', 2000, .6)]),
                                  m, 1995, retrospective=True)
    reds['F1_unused_future_upgrade'][m] = dict(
        before=before.as_dict(), after=after.as_dict(),
        value_before=before.basis_wave_ids, value_after=after.basis_wave_ids)

# F2 empty actor grants
reds['F2_empty_actor_grants'] = {}
for m in (T.METHOD_M0_HOLD, T.METHOD_M1_INTERP, T.METHOD_M2_BACKOFF):
    x = T.read_selected_world(WORLD, case([wave('OLD', 1980, .2), wave('RECENT', 1990, .6)]), m, 1995)
    reds['F2_empty_actor_grants'][m] = x.as_dict()

# F3 lag parser
c = case([wave('DELAYED', 1990, .8, published_year=2000)], ruptures=(1995,))
x = T.evaluate(c, T.METHOD_M0_HOLD, clock_year=1997, retrospective=True)
reds['F3_lag_pipe_rupture_suffix'] = dict(result=x.as_dict(), pub_lag_of=list(T.pub_lag_of(x)))

# F4 duplicate id
c = case([wave('DUPLICATE', 1990, .6),
          wave('DUPLICATE', 1980, .1, country='OTHER', source_family='WRONG_SOURCE',
               edition='WRONG_EDITION')])
x = T.read_selected_world(WORLD, c, T.METHOD_M0_HOLD, 1995)
reds['F4_duplicate_wave_id'] = x.as_dict()

(RET / "observations" / "phase_a_reproduced_reds.json").write_text(
    json.dumps(reds, indent=1, sort_keys=True) + "\n")
print("reproduced", len(reds), "RED groups on the pinned T9C adapter")
print("F2 authorized_opportunity:", {m: reds['F2_empty_actor_grants'][m]['authorized_opportunity']
                                      for m in reds['F2_empty_actor_grants']})
print("F3 pub_lag_of:", reds['F3_lag_pipe_rupture_suffix']['pub_lag_of'])
print("F4 source_family:", reds['F4_duplicate_wave_id']['provenance']['source_family'])
