"""SORACLE builder-owned R3+REMONT R18 functional convergence court.

Tests explicitly RETEST the bugs found and repaired by REMONT, as applied
to the *newer* SORACLE actor/constitution, plus a new author-local atomicity
issue. These tests are not a claim of actual Python execution.
"""
import copy
import tempfile
import unittest
from pathlib import Path

from um_sorok_organism.activity import record_activity_afterlife
from um_sorok_organism.constitution import compose,materialize,actor_access
from um_sorok_organism.storage import ResearchLedger,Conflict
from um_sorok_organism.types import adult,blank_world
from um_sorok_organism.world import add_cue


def actor_and_site():
    actor=adult("nadias_father","Father")
    for name,action in (("a","SING"),("b","WORK"),("c","REPAIR")):
        actor["forms"][name]={
            "id":name,"actor":actor["id"],"kind":"PRACTICE",
            "cues":["encounter"],"enables":[action],
            "strength":.65,"body_min":0,"lifecycle":"ACTIVE","scope":{}
        }
    world=blank_world()
    world["positions"]={actor["id"]:"home"}
    add_cue(world,"bell",["encounter"],location="home")
    return actor,world


class JoinedPsychicRecruitmentR15(unittest.TestCase):
    def test_stratified_inhibition_not_conservative_false_negative(self):
        a,w=actor_and_site()
        a["links"]=[
            {"source":"a","target":"b","relation":"INHIBITS","contexts":[]},
            {"source":"b","target":"c","relation":"INHIBITS","contexts":[]},
        ]
        first=compose(materialize(a,w),actor_access(a,w))
        self.assertEqual({form["id"] for form in first.recruited},
                         {"a","c"})
        self.assertNotIn("c",first.inhibited)
        a["links"].reverse()
        second=compose(materialize(a,w),actor_access(a,w))
        self.assertEqual({form["id"] for form in second.recruited},
                         {"a","c"})

    def test_r3_new_suppresses_relation_still_obeys_r15_truth(self):
        a,w=actor_and_site()
        a["links"]=[
            {"source":"a","target":"b","relation":"SUPPRESSES","contexts":[]},
            {"source":"b","target":"c","relation":"SUPPRESSES","contexts":[]},
        ]
        result=compose(materialize(a,w),actor_access(a,w))
        self.assertEqual({form["id"] for form in result.recruited},
                         {"a","c"})
        self.assertIn("b",result.inhibited)
        self.assertNotIn("c",result.inhibited)

    def test_conflicting_cyclic_inhibition_remains_unresolved(self):
        a,w=actor_and_site()
        a["links"]=[
            {"source":"a","target":"b","relation":"INHIBITS","contexts":[]},
            {"source":"b","target":"a","relation":"INHIBITS","contexts":[]},
        ]
        result=compose(materialize(a,w),actor_access(a,w))
        self.assertFalse({"a","b"} & {x["id"] for x in result.recruited})


class JoinedPurposeP004(unittest.TestCase):
    def _actor(self):
        a=adult("parent","Parent")
        a["projects"]=[
            {"id":"care","object":"care for this child",
             "means":["CARE"],"operational_history":[]},
            {"id":"speak","object":"learn to speak together",
             "means":["SPEAK"],"operational_history":[]}
        ]
        return a

    def _purpose(self,ids):
        return {"status":(
            "ACTOR_POLICY_SELECTED_PROJECT_COURSE" if len(ids)==1 else
            "ACTOR_POLICY_SELECTED_MULTIPLE_PROJECT_COURSES"),
            "project_id":ids[0] if len(ids)==1 else None,
            "project_ids":ids}

    def test_actor_selected_incompatible_project_must_not_silently_disappear(self):
        a=self._actor();before=copy.deepcopy(a)
        with self.assertRaisesRegex(ValueError,
                                    "ACTIVITY_SELECTED_MEANS_CONTRADICTION"):
            record_activity_afterlife(
                a,"SPEAK","PERFORMED","SPEECH_PERFORMED",
                ["project:care"],"evt_wrong",
                purpose_selection=self._purpose(["care"]))
        self.assertEqual(a,before)

    def test_mixed_compatible_and_incompatible_selection_is_atomic(self):
        a=self._actor();before=copy.deepcopy(a)
        with self.assertRaisesRegex(ValueError,
                                    "ACTIVITY_SELECTED_MEANS_CONTRADICTION"):
            record_activity_afterlife(
                a,"SPEAK","PERFORMED","SPEECH_PERFORMED",
                ["project:care","project:speak"],"evt_mixed",
                purpose_selection=self._purpose(["care","speak"]))
        self.assertEqual(a,before)

    def test_missing_actor_selected_project_does_not_disappear(self):
        a=self._actor();before=copy.deepcopy(a)
        with self.assertRaisesRegex(ValueError,
                                    "ACTIVITY_SELECTED_MEANS_CONTRADICTION"):
            record_activity_afterlife(
                a,"SPEAK","PERFORMED","SPEECH_PERFORMED",
                ["project:ghost"],"evt_ghost",
                purpose_selection=self._purpose(["ghost"]))
        self.assertEqual(a,before)

    def test_project_history_collision_is_atomic_in_multi_project_selection(self):
        a=self._actor()
        a["projects"][0]["means"].append("SPEAK")
        a["projects"][1]["operational_history"].append({
            "event":"evt_same","operation":"SPEAK"})
        before=copy.deepcopy(a)
        with self.assertRaisesRegex(ValueError,
                                    "DUPLICATE_ACTIVITY_EVENT_FOR_PROJECT"):
            record_activity_afterlife(
                a,"SPEAK","PERFORMED","SPEECH_PERFORMED",
                ["project:care","project:speak"],"evt_same",
                purpose_selection=self._purpose(["care","speak"]))
        self.assertEqual(a,before)

    def test_actual_selected_project_retains_its_practical_object(self):
        a=self._actor()
        record_activity_afterlife(
            a,"SPEAK","PERFORMED","SPEECH_PERFORMED",
            ["project:speak"],"evt_ok",
            purpose_selection=self._purpose(["speak"]))
        self.assertEqual(len(a["projects"][1]["operational_history"]),1)
        self.assertEqual(a["projects"][1]["operational_history"][0][
            "practical_object"],"learn to speak together")
        self.assertEqual(a["projects"][0]["operational_history"],[])


class JoinedSourcePreflightP018(unittest.TestCase):
    def test_corrupt_history_blocks_all_existing_authority_paths(self):
        with tempfile.TemporaryDirectory() as folder:
            path=str(Path(folder)/"preflight.sqlite3")
            l=ResearchLedger(path)
            try:
                l.initialize(blank_world(),[adult("parent","Parent")],
                             source_seals=[("seed","FICTIONAL",{"person":"A"})])
                self.assertEqual(l.source("seed")["content"],{"person":"A"})
                l.conn.execute(
                    "UPDATE events SET payload='{}' WHERE seq=1")
                with self.assertRaisesRegex(Conflict,
                                            "SOURCE_HISTORY_INVALID"):
                    l.source("seed")
                with self.assertRaisesRegex(Conflict,
                                            "SOURCE_HISTORY_INVALID"):
                    l.seal_source("late","FICTIONAL",{"person":"B"})
                version,w=l.world()
                with self.assertRaisesRegex(Conflict,
                                            "SOURCE_HISTORY_INVALID"):
                    l.commit("w1",version,w,{},{},"OBJECTIVE_CUE",None,
                             {"no":"unsafe_append"})
                self.assertEqual(l.conn.execute(
                    "SELECT count(*) FROM events").fetchone()[0],1)
            finally:
                l.close()


if __name__=="__main__":
    unittest.main()
