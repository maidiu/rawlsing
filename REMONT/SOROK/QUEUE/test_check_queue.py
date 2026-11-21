"""Self-tests for the REMONT local-machine queue controller.

Run: python3 -m unittest discover -s REMONT/SOROK/QUEUE -p 'test_check_queue.py' -v
Does not contact GitHub or modify candidate source branches.
"""
from contextlib import redirect_stderr, redirect_stdout
import copy
import hashlib
import io
import json
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import check_queue as q


class QueueDisciplineTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.queue = q.validate_queue(q.load_json(q.DEFAULT_QUEUE))
        self.results = self.root / 'LOCAL_COURTS' / 'REMONT_QUEUE'

    def test_queue_eight_pinned_exact_shas_in_newest_first_order(self):
        self.assertEqual([x['pr'] for x in self.queue['candidates']],
                         [1234,1241,1230,1222,1220,1214,1210,1199])
        self.assertEqual(self.queue['candidates'][0]['sha'],
                         'dbfb35c18ed0ec061050acdd1a1e5000e0bacc6b')
        self.assertEqual(self.queue['candidates'][1]['sha'],
                         'a4a495bbb456bd211b4fbdbd29478c0f0052603f')
        self.assertEqual(self.queue['candidates'][0]['manifest'], 'PINNED_GIT_TREE')
        self.assertTrue(self.queue['candidates'][0]['joined_first_consumer'])
        self.assertEqual(self.queue['default_python'], 'python3.11')

    def test_joined_branch_requires_explicit_integrated_source_lane(self):
        bad = copy.deepcopy(self.queue)
        bad['candidates'][0]['joined_first_consumer'] = False
        with self.assertRaisesRegex(ValueError, 'INVALID_QUEUE_BRANCH'):
            q.validate_queue(bad)
        bad = copy.deepcopy(self.queue)
        bad['candidates'][1]['manifest'] = 'PINNED_GIT_TREE'
        with self.assertRaisesRegex(ValueError, 'UNAUTHORIZED_GIT_TREE_MODE'):
            q.validate_queue(bad)

    def test_pinned_git_tree_checks_every_joined_python_file_and_bytes(self):
        root = self.root / 'repo'
        src = root / 'SEAM' / 'ORACLE' / 'UM_SOROK_ORGANISM_R3'
        (src / 'tests').mkdir(parents=True)
        source = src / 'example.py'
        source.write_text('print("source")\n', encoding='utf-8')
        test = src / 'tests' / 'test_example.py'
        test.write_text('print("test")\n', encoding='utf-8')

        def git(*args):
            return subprocess.run(['git', '-C', str(root), *args],
                                  check=True, capture_output=True, text=True).stdout.strip()

        git('init', '-q')
        git('add', '.')
        git('-c', 'user.name=Queue-Test', '-c',
            'user.email=queue-test@example.invalid', 'commit', '-q', '-m', 'fixture')
        verified = q.pinned_git_tree_check(src)
        self.assertEqual(verified['verified_python_files'], 2)
        self.assertEqual(verified['manifest'], 'PINNED_GIT_TREE')
        self.assertFalse(verified['precommitted_independent_sha256_manifest'])
        source.write_text('print("tampered")\n', encoding='utf-8')
        with self.assertRaisesRegex(q.QueueFailure, 'PINNED_TREE_SOURCE_BLOB_MISMATCH'):
            q.pinned_git_tree_check(src)
        source.write_text('print("source")\n', encoding='utf-8')
        (src / 'rogue.py').write_text('print("untracked")\n', encoding='utf-8')
        with self.assertRaisesRegex(q.QueueFailure, 'PINNED_TREE_PYTHON_SET_MISMATCH'):
            q.pinned_git_tree_check(src)

    def test_duplicate_pr_refused(self):
        bad = copy.deepcopy(self.queue)
        bad['candidates'].append(copy.deepcopy(bad['candidates'][0]))
        with self.assertRaisesRegex(ValueError,'DUPLICATE'):
            q.validate_queue(bad)

    def test_bad_sha_refused(self):
        bad = copy.deepcopy(self.queue)
        bad['candidates'][0]['sha'] = 'newly-updated-fabricated-head'
        with self.assertRaisesRegex(ValueError,'INVALID_PINNED_SHA'):
            q.validate_queue(bad)

    def test_cross_repository_queue_refused(self):
        bad = copy.deepcopy(self.queue)
        bad['repository'] = 'stranger/forge'
        with self.assertRaisesRegex(ValueError,'UNEXPECTED_REPOSITORY'):
            q.validate_queue(bad)

    def test_moved_remote_branch_becomes_hold(self):
        with patch.object(q,'git',return_value='a'*40+'\trefs/heads/test'):
            with self.assertRaisesRegex(q.QueueFailure,'LIVE_BRANCH_HEAD_CHANGED_HOLD'):
                q.verify_source_ref(self.root,self.queue['candidates'][0])

    def test_manifest_exact_python_source_bytes(self):
        src = self.root/'candidate'
        (src/'tests').mkdir(parents=True)
        data = b'print("hello")\n'
        (src/'tests'/'hello.py').write_bytes(data)
        sha = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        m = {'python_file_count':1,'files':{'tests/hello.py':{'sha256':hashlib.sha256(data).hexdigest(),'git_blob_sha1':sha}}}
        q.atomic_json(src/'manifest.json',m)
        good = q.source_manifest_check(src,'manifest.json')
        self.assertEqual(good['verified_python_files'],1)
        (src/'tests'/'hello.py').write_bytes(b'print("tampered")\n')
        with self.assertRaisesRegex(q.QueueFailure,'SOURCE_SHA256_MISMATCH'):
            q.source_manifest_check(src,'manifest.json')

    def test_manifest_path_escape_refused(self):
        src = self.root/'candidate'
        src.mkdir()
        q.atomic_json(src/'manifest.json',{'files':{'../../secret.py':{'sha256':'a'*64}}})
        with self.assertRaisesRegex(q.QueueFailure,'SOURCE_MANIFEST_PATH_INVALID'):
            q.source_manifest_check(src,'manifest.json')

    def test_real_machine_version_mismatch_is_hold_not_green(self):
        if sys.version_info[:2] == (3,11):
            self.skipTest('This negative control needs a non-3.11 test machine')
        with self.assertRaisesRegex(q.QueueFailure,'PYTHON_3_11_REQUIRED'):
            q.ensure_machine_version(sys.executable,self.root)

    def test_no_result_is_not_accepted(self):
        s = q.load_state(self.results/'ledger.json')
        s['_results_path']=self.results
        self.assertTrue(q.needs_execution(s,'1241@'+self.queue['candidates'][0]['sha']))
        with redirect_stdout(io.StringIO()) as out:
            q.print_queue(self.queue['candidates'][:1],s)
        self.assertIn('COMPAT_NOT_RUN',out.getvalue())
        self.assertIn('HOSTILE_REVIEW_PENDING',out.getvalue())

    def test_receipt_atomically_written_and_skip_only_exact_green(self):
        i=self.queue['candidates'][0]
        k=q.state_key(i)
        receipt={'status':'COMPAT_PASS__HOSTILE_REVIEW_PENDING','sha':i['sha'],'independent_acceptance':False}
        file=q.record_receipt(self.results,k,receipt)
        self.assertTrue(file.is_file())
        s=q.load_state(self.results/'ledger.json')
        s['_results_path']=self.results
        self.assertFalse(q.needs_execution(s,k))
        self.assertTrue(q.needs_execution(s,k,force=True))
        self.assertTrue(q.needs_execution(s,'1241@'+'b'*40))
        self.assertEqual(q.load_json(file)['independent_acceptance'],False)

    def test_failed_execution_remains_pending(self):
        i=self.queue['candidates'][0];k=q.state_key(i)
        q.record_receipt(self.results,k,{'status':'TEST_COURT_FAILED_PYTEST','sha':i['sha']})
        s=q.load_state(self.results/'ledger.json');s['_results_path']=self.results
        self.assertTrue(q.needs_execution(s,k))

    def test_unsubstantiated_auto_acceptance_not_recorded(self):
        i=self.queue['candidates'][0]
        document=self.root/'fake_review.md'
        document.write_text('empty')
        args=['record-review','--pr',str(i['pr']),'--repo',str(self.root),
              '--results',str(self.results),'--reviewer','fake',
              '--independence-basis','I claim to be independent','--evidence',str(document),
              '--verdict','ACCEPT_SCOPED']
        with self.assertRaises(SystemExit):
            q.main(args)
        self.assertFalse((self.results/'reviews').exists())

    def test_unknown_pr_refused(self):
        class A: pr=[777777]
        with self.assertRaisesRegex(ValueError,'UNKNOWN_REQUESTED_PR'):
            q.pick(self.queue,A)

    def test_template_not_a_verdict(self):
        i=self.queue['candidates'][0]
        text=q.review_template(i,'runs/source.json')
        self.assertIn('Verdict: HOLD until a distinct reviewer',text)
        self.assertIn(i['sha'],text)
        self.assertIn('## New adversarial probes',text)

    def test_deferred_builder_is_not_a_green_receipt_or_default_queued_review(self):
        joined = self.queue['candidates'][0]
        self.assertTrue(joined['execution_deferred'])
        self.assertEqual(joined['sha'], 'dbfb35c18ed0ec061050acdd1a1e5000e0bacc6b')
        self.assertIn('BUILDER', joined['defer_reason'].upper())
        with redirect_stdout(io.StringIO()) as out:
            state = q.load_state(self.results/'ledger.json')
            state['_results_path'] = self.results
            q.print_queue([joined],state)
        self.assertIn('DEFERRED_TO_BUILDER__HISTORICAL_RED',out.getvalue())
        bad=copy.deepcopy(self.queue)
        bad['candidates'][1]['execution_deferred']=True
        with self.assertRaisesRegex(ValueError,'DEFER_ONLY_ACTIVE_BUILDER_LANE'):
            q.validate_queue(bad)
        bad=copy.deepcopy(self.queue)
        bad['candidates'][0]['execution_deferred']='yes'
        with self.assertRaisesRegex(ValueError,'INVALID_EXECUTION_DEFER_FLAG'):
            q.validate_queue(bad)

    def test_current_r17_review_pin_and_prior_pin_conserved(self):
        old = '6f2e98433822a4fb1246ff72c388b2e901c6ab7f'
        item = next(x for x in self.queue['candidates'] if x['pr']==1230)
        self.assertEqual(item['sha'],'bd023cccea8912913ace132600c69a97b0eb6a44')
        self.assertEqual(item['previous_pinned_shas'],[old])
        self.assertEqual(next(x for x in self.queue['candidates'] if x['pr']==1241)['sha'],
                         'a4a495bbb456bd211b4fbdbd29478c0f0052603f')


if __name__=='__main__': unittest.main()
