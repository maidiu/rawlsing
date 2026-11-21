import copy
import tempfile
from pathlib import Path
import unittest
from check_live_receiving import audit, BASE_SHA, verify_readable_status, sha_blob


def fixture():
    row = dict(pr=1234, head_sha='a'*40, pr_state='open', merged=False,
               originating_owner_lane='SORACLE builder', next_receiving_owner='SOROK HQ',
               smallest_next_action='Prove first reader', disposition='UNRECEIVED',
               test=dict(executed_sha='a'*40, applied_to_head=True),
               review=dict(sha=None, applied_to_head=False),
               authorities=dict(science='NOT_ISSUED', actor='NOT_ISSUED', source='NOT_ISSUED', human='NOT_ISSUED'))
    ledger = dict(schema='SOROK_O_INDEX_LIVE_RECEIVING@1', protected_baseline=dict(sha=BASE_SHA),
                  records=[row], event_history=[])
    snap = dict(protected_sha=BASE_SHA, scope_complete=True,
                prs=[dict(pr=1234, head_sha='a'*40, title='SORACLE organism', state='open', merged=False)])
    return ledger, snap


class ReceivingCheckerAdversaries(unittest.TestCase):
    def test_positive_scoped(self):
        d, s = fixture()
        self.assertEqual(audit(d, s)[0], [])

    def test_changed_head_detected(self):
        d, s = fixture()
        s['prs'][0]['head_sha'] = 'b'*40
        self.assertIn('MOVED_HEAD_STALE_LEDGER:1234', audit(d, s)[0])

    def test_stale_test_detected(self):
        d, s = fixture()
        d['records'][0]['test']['executed_sha'] = 'b'*40
        self.assertIn('FALSE_GREEN_STALE_TEST:1234', audit(d, s)[0])

    def test_new_pr_unrecorded(self):
        d, s = fixture()
        s['prs'].append(dict(pr=1249, head_sha='c'*40, title='SOROK new body', state='open', merged=False))
        self.assertIn('UNRECORDED_NEW_RELEVANT_PR:1249', audit(d, s)[0])

    def test_closed_unreceived(self):
        d, s = fixture()
        d['records'][0]['pr_state'] = s['prs'][0]['state'] = 'closed'
        self.assertIn('UNRECEIVED_CLOSED_PR:1234', audit(d, s)[0])

    def test_missing_owner(self):
        d, s = fixture()
        d['records'][0]['next_receiving_owner'] = ''
        self.assertIn('MISSING_OWNER_OR_NEXT_ACTION:1234', audit(d, s)[0])

    def test_false_native_promotion(self):
        d, s = fixture()
        d['records'][0]['authorities']['science'] = 'NATIVE_ISSUED'
        self.assertIn('FALSE_NATIVE_OR_SCIENCE_PROMOTION:1234:science', audit(d, s)[0])

    def test_md_json_revision_divergence(self):
        d, s = fixture()
        e, _ = audit(d, s, '# SOROK current progress revision39', dict(owner='Sorok', revision=40))
        self.assertIn('MD_JSON_REVISION_CONTRADICTION', e)

    def test_missing_live_scope(self):
        d, s = fixture()
        s['scope_complete'] = False
        self.assertIn('DISCOVERY_SCOPE_INCOMPLETE_OR_UNAUTHENTICATED', audit(d, s)[0])

    def test_fake_independent_review_claim(self):
        d, s = fixture()
        d['records'][0]['disposition'] = 'INDEPENDENTLY_REVIEWED_SCOPED'
        self.assertIn('UNSUPPORTED_INDEPENDENT_REVIEW_CLAIM:1234', audit(d, s)[0])

    def test_readable_markdown_digest_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            raw = b'{"schema":"sample"}\n'
            (folder / 'LIVE_RECEIVING_LEDGER.json').write_bytes(raw)
            (folder / 'READABLE_CANDIDATE_STATUS_20261121.md').write_text(
                'exact Git **blob `' + sha_blob(raw) + '`**')
            self.assertEqual(verify_readable_status(folder), [])
            (folder / 'LIVE_RECEIVING_LEDGER.json').write_bytes(raw + b' ')
            self.assertIn('READABLE_LEDGER_VIEW_STALE', verify_readable_status(folder))

    def test_superseded_without_function_conservation(self):
        d, s = fixture()
        row = d['records'][0]
        row['pr_state'] = s['prs'][0]['state'] = 'closed'
        row['disposition'] = 'SUPERSEDED'
        row['successor_pr'] = 1240
        e, _ = audit(d, s)
        self.assertIn('SUPERSEDED_WITHOUT_FUNCTION_CONSERVATION:1234', e)
        self.assertIn('SUPERSEDED_WITHOUT_TRACKED_SUCCESSOR:1234', e)


if __name__ == '__main__':
    unittest.main()
