import unittest
from inference_lab_rfa_attempts_r24 import reduce_attempts, TRANSIENT

E={'source_run_id':'CMRUN-0001','model':'claude-sonnet-5-5','case_id':'RF010','condition':'N','replicate':1}


def attempt(n, status, usage, start, end):
    return dict(run_id=E['source_run_id'], attempt_id=f"{E['source_run_id']}-A{n:04d}",
                requested_model=E['model'], case_id=E['case_id'], condition=E['condition'], replicate=1,
                request_identity_sha256='a'*64, status=status, usage=usage,
                started_at_utc=f'2026-10-13T04:00:{start:02d}+00:00',
                ended_at_utc=f'2026-10-13T04:00:{end:02d}+00:00', latency_seconds=end-start)


class RFAAttempts(unittest.TestCase):
    def test_missing_usage_and_wait(self):
        a=attempt(1,TRANSIENT,None,0,2)
        b=attempt(2,'SCHEMA_VALID',dict(input_tokens=3414,output_tokens=669,cache_creation_input_tokens=0,cache_read_input_tokens=0),5,12)
        x=reduce_attempts(E,[a,b])
        self.assertEqual(x['attempts'],2)
        self.assertEqual(x['known_usage']['output_tokens'],669)
        self.assertEqual(x['usage_observations']['output_tokens'],1)
        self.assertFalse(x['complete_observed_usage'])
        self.assertEqual(x['sum_attempt_seconds'],9)
        self.assertEqual(x['time_to_terminal_seconds'],12)
        self.assertIsNone(x['time_to_adequate_result_seconds'])
        self.assertIsNone(reduce_attempts(E,[])['observed_span_seconds'])
        self.assertIsNone(reduce_attempts(E,[a])['time_to_terminal_seconds'])

    def test_retry_integrity(self):
        a=attempt(1,TRANSIENT,None,0,2)
        b=attempt(2,'SCHEMA_VALID',None,5,12)
        for records in ([b],[a,dict(b,request_identity_sha256='b'*64)],
                        [dict(a,status='SCHEMA_VALID'),b],[a,dict(b,case_id='RF009')],
                        [a,dict(b,usage={'input_tokens':-1})],[a,dict(b,started_at_utc=a['started_at_utc'])]):
            with self.assertRaises(ValueError):
                reduce_attempts(E,records)


if __name__=='__main__':
    unittest.main()
