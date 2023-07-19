"""Tests for differentiate."""
import unittest
from differentiate import differniate_expression, derivative_of_single_term


class TestDifferniateExpression(unittest.TestCase):
    def test(self):
        test_cases = [
            ("2x^2", "4x"),
            ("12x^3+4x", "36x^2+4"),
            ("36x^3*12x^2", "108x^2*12x^2+36x^3*24x"),
            ("3x^4/12x", "(12x^3*12x+3x^4*12)/(12x)^2")
        ]

        for case in test_cases:
            self.assertEqual(differniate_expression(case[0]), case[1])


class TestDerivativeOfSingleTerm(unittest.TestCase):
    def test(self):
        test_cases = [
            ("2x^2", "4x"),
            ("12x^3", "36x^2")
        ]

        for case in test_cases:
            self.assertEqual(derivative_of_single_term(case[0]), case[1])


if __name__ == '__main__':
    unittest.main()
