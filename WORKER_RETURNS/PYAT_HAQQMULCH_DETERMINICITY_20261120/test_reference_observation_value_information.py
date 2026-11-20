"""Bounded sourcefree falsifiers for one proposed PYAT diagnostic extension.

Run:
  python -m unittest discover -s WORKER_RETURNS/PYAT_HAQQMULCH_DETERMINICITY_20261120 -p 'test_*.py' -v
No original-source read, I03-issued claim or protected test authorization.
"""

import math
import sys
import unittest
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reference_observation_value_information import (
    _mi_from_cells,
    decompose_observation_value_information,
)


class SourcefreeObservationValueFalsifiers(unittest.TestCase):
    def test_missingness_is_not_predictor_value_power(self):
        # Historical wrong subtraction: H(Y) = 1, H(Y|X observed) = 0.
        result = decompose_observation_value_information({
            ("A", "OBSERVED", "only-one-X"): 50,
            ("B", "NOT_ASKED", None): 50,
        })
        self.assertAlmostEqual(result.domain_target_entropy_bits, 1.0)
        self.assertEqual(result.observed_value_categories, 1)
        self.assertAlmostEqual(result.observed_value_information_bits, 0.0)
        self.assertAlmostEqual(result.observation_pattern_information_bits, 1.0)
        self.assertAlmostEqual(result.combined_available_information_bits, 1.0)
        self.assertEqual(result.observed_share, 0.5)

    def test_country_pooling_generates_fake_within_country_importance(self):
        # Within both fixed countries X and Y are independent. Pooling is not.
        country_a = {("1", "1"): 81, ("1", "0"): 9, ("0", "1"): 9, ("0", "0"): 1}
        country_b = {("1", "1"): 1, ("1", "0"): 9, ("0", "1"): 9, ("0", "0"): 81}
        pooled = {key: country_a[key] + country_b[key] for key in country_a}
        self.assertAlmostEqual(_mi_from_cells(country_a), 0.0, places=12)
        self.assertAlmostEqual(_mi_from_cells(country_b), 0.0, places=12)
        self.assertAlmostEqual(_mi_from_cells(pooled), 0.3199229542717201, places=10)

    def test_observed_values_have_separate_predictive_information(self):
        result = decompose_observation_value_information({
            ("A", "OBSERVED", "x1"): 25,
            ("B", "OBSERVED", "x2"): 25,
            ("A", "NOT_ASKED", None): 25,
            ("B", "NOT_ASKED", None): 25,
        })
        self.assertAlmostEqual(result.observation_pattern_information_bits, 0.0)
        self.assertAlmostEqual(result.observed_value_information_bits, 1.0)
        self.assertAlmostEqual(result.domain_weighted_observed_value_information_bits, 0.5)
        self.assertAlmostEqual(result.combined_available_information_bits, 0.5)

    def test_multiple_source_nonanswer_statuses_remain_distinct(self):
        result = decompose_observation_value_information({
            ("A", "OBSERVED", "yes"): 8,
            ("B", "OBSERVED", "no"): 7,
            ("A", "REFUSED", None): 4,
            ("B", "NOT_ASKED", None): 3,
            ("A", "DONT_KNOW", None): 2,
        })
        self.assertEqual(result.observation_states,
                         ("DONT_KNOW", "NOT_ASKED", "OBSERVED", "REFUSED"))
        self.assertTrue(result.combined_available_information_bits >= 0)
        self.assertAlmostEqual(
            result.combined_available_information_bits,
            result.observation_pattern_information_bits +
            result.domain_weighted_observed_value_information_bits,
        )

    def test_rare_support_is_retained_not_truncated_to_majority(self):
        result = decompose_observation_value_information({
            ("main", "OBSERVED", "high"): 98,
            ("minority", "OBSERVED", "rare"): 1,
            ("main", "OBSERVED", "rare"): 1,
        })
        self.assertEqual(result.observed_mass, Fraction(100))
        self.assertEqual(result.observed_value_categories, 2)
        self.assertGreater(result.observed_value_information_bits, 0.0)

    def test_exact_weighted_fractions_and_scale_invariance(self):
        rows = {("A", "OBSERVED", "x"): Fraction(3, 2),
                ("B", "OBSERVED", "y"): Fraction(1, 2),
                ("A", "MISSING", None): Fraction(1, 3),
                ("B", "MISSING", None): Fraction(2, 3)}
        first = decompose_observation_value_information(rows)
        second = decompose_observation_value_information({k: v*37 for k, v in rows.items()})
        self.assertEqual(first.domain_mass, Fraction(3, 1))
        self.assertAlmostEqual(first.observed_value_information_bits,
                               second.observed_value_information_bits)
        self.assertAlmostEqual(first.observation_pattern_information_bits,
                               second.observation_pattern_information_bits)

    def test_nonobserved_value_is_not_invented(self):
        with self.assertRaisesRegex(ValueError, "NONOBSERVED"):
            decompose_observation_value_information({("A", "NOT_ASKED", "yes"): 1})

    def test_observed_value_cannot_be_empty(self):
        with self.assertRaisesRegex(ValueError, "OBSERVED_X"):
            decompose_observation_value_information({("A", "OBSERVED", None): 1})

    def test_rounded_weight_not_silently_called_exact(self):
        with self.assertRaises(TypeError):
            decompose_observation_value_information({("A", "OBSERVED", "x"): 0.3})

    def test_empty_and_negative_masses_are_refused(self):
        with self.assertRaisesRegex(ValueError, "EMPTY_DOMAIN"):
            decompose_observation_value_information({})
        with self.assertRaisesRegex(ValueError, "NEGATIVE_CELL_MASS"):
            decompose_observation_value_information({("A", "OBSERVED", "x"): -1})
        with self.assertRaisesRegex(ValueError, "EMPTY_DOMAIN"):
            decompose_observation_value_information({("A", "OBSERVED", "x"): 0})


if __name__ == "__main__":
    unittest.main()
