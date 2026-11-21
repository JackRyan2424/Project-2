import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

import streamlit as st
from streamlit.testing.v1 import AppTest

from portfolio import (
    CORRELATIONS, SLEEVES, benchmark_weights, covariance_matrix,
    expected_return, portfolio_volatility, validate_inputs,
)
from rates import read_vintage


class PortfolioTests(unittest.TestCase):
    def test_benchmark_known_answer(self):
        validate_inputs(SLEEVES, CORRELATIONS, 0.065)
        weights = benchmark_weights(SLEEVES)
        covariance = covariance_matrix(SLEEVES, CORRELATIONS)
        self.assertEqual(weights, [0, 0, 0.40, 0.60])
        self.assertAlmostEqual(expected_return(weights, SLEEVES), 0.068)
        self.assertAlmostEqual(portfolio_volatility(weights, covariance) ** 2, 0.010944)


class VintageTests(unittest.TestCase):
    vintage = date(2026, 10, 4)
    header = "observation_date,DGS10_20261004\n"

    def test_latest_valid_observation(self):
        rows = "2026-09-30,5.11\n2026-10-01,5.24\n2026-10-02,.\n"
        self.assertEqual(read_vintage(self.header + rows, self.vintage), (date(2026, 10, 1), 5.24))

    def test_ineligible_data(self):
        cases = (
            ("wrong vintage", "observation_date,DGS10\n2026-10-01,5.24\n"),
            ("future observation", self.header + "2026-10-05,5.24\n"),
            ("stale observation", self.header + "2026-09-26,5.24\n"),
            ("duplicate observation", self.header + "2026-10-01,5.24\n2026-10-01,5.25\n"),
        )
        for reason, csv_text in cases:
            with self.subTest(reason=reason), self.assertRaises(ValueError):
                read_vintage(csv_text, self.vintage)


class AppTests(unittest.TestCase):
    def setUp(self):
        st.cache_data.clear()
        self.app = AppTest.from_file(str(Path(__file__).with_name("app.py")), default_timeout=30)

    def test_unavailable_vintage_keeps_live_hold(self):
        with patch("rates.fetch_signal", side_effect=OSError("offline test")):
            self.app.run()
            self.app.checkbox[0].check().run()
        self.assertFalse(self.app.exception)
        self.assertTrue(any("historical vintage could not be admitted" in w.value for w in self.app.warning))
        self.assertTrue(any("0% of the reserve" in w.value for w in self.app.warning))

    def test_recorded_allocation_and_stress_stops(self):
        signal = (date(2026, 10, 4), date(2026, 10, 1), 5.24, "fixture", "https://example.invalid")
        with patch("rates.fetch_signal", return_value=signal):
            self.app.run()
            self.app.checkbox[0].check().run()
        self.assertFalse(self.app.exception)
        comparison = self.app.dataframe[0].value.set_index("Portfolio")
        self.assertEqual(len(comparison), 4)
        selected = comparison.loc["Constrained"]
        self.assertEqual(selected["Global equity index fund"], "65.00%")
        self.assertEqual(selected["Investment-grade bond fund"], "32.00%")
        self.assertEqual(selected["Bills"], "3.00%")
        self.assertEqual(selected["Projected 5-year annualized net return"], "6.90%")
        self.assertEqual(selected["Volatility"], "11.04%")
        self.assertEqual(selected["Mandate verdict"], "Pass")
        stress = self.app.dataframe[1].value
        self.assertEqual(list(stress["Net window return"]), ["-11.04%", "-9.72%"])
        self.assertEqual(list(stress["Stop reason"]), ["loss of 10% or more", "volatility cap, bills floor"])
        self.assertTrue(any("0% of the reserve" in w.value for w in self.app.warning))


if __name__ == "__main__":
    unittest.main()
