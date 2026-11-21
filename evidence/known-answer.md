# Twelve-line known-answer reconciliation

The worked example applies the course's Week 3 known-answer method to the saved October 5, 2026 portfolio scenario. Weights and rates are decimals in the arithmetic below. The app tests replay the scenario with a fixed rate fixture. [Week 3 handout](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-03/student-handout.md)

1. Signal fixture is 5.24% against a 5.00% trigger, so the equity cap is 65%.
2. Selected weights in bills, notes, investment-grade bonds, and equity are 3%, 0%, 32%, and 65%. They sum to 100%.
3. Bill reserves cover $3 million of payouts on a $100 million portfolio. All four modeled sleeves are redeemable within five business days, giving 100% modeled liquidity.
4. Benchmark expected return is `0.40 × 0.05 + 0.60 × 0.08 = 6.80%`.
5. Selected expected return is `0.03 × 0.035 + 0.32 × 0.05 + 0.65 × 0.08 = 6.905%`.
6. One-way turnover is `(0.03 + 0.08 + 0.05) / 2 = 8%`.
7. Entry cost is `0.08 × 0.001 = 0.00008`, or 0.8 basis points of portfolio value.
8. Five-year annualized net return is `(1 − 0.00008)^(1/5) × 1.06905 − 1 ≈ 6.90%`. This exceeds the 6.50% hurdle.
9. Selected variance is `(0.03 × 0.005)^2 + (0.32 × 0.06)^2 + (0.65 × 0.16)^2 + 2 × 0.05 × (0.03 × 0.005) × (0.32 × 0.06) + 2 × 0.25 × (0.32 × 0.06) × (0.65 × 0.16)`. Its square root is 11.04%, below the 12% baseline cap.
10. Equity-only downside holds weights, cost, and non-equity shocks fixed. A 15% equity drop gives `0.65 × (−0.15) − 0.00008 = −9.758%`, short of the 10% loss stop.
11. The stacked selloff adds `0.32 × (−0.04) = −1.28` percentage points from credit. The combined net return is −11.038%, triggering the loss stop.
12. Sticky inflation gives `0.03 × 0.0075 + 0.32 × (−0.06) + 0.65 × (−0.12) − 0.08 × 0.003 = −9.7215%`. At 11.04% volatility and 3% bills, the portfolio breaches the 10% volatility cap and 5% bills floor. The recommendation is a paper pilot with 0% live deployment.

## Cold-run log

### Partner run reported in Lab 20

Jack Ryan reports that his partner ran the project and encountered no problems. The readiness note does not give the date, repository commit, environment, or captured output.

### Clean dependency and app replay by Codex

Run date was November 21, 2026. The environment was Windows with Python 3.12.14 and Streamlit 1.66.0. Dependencies were installed from `requirements.txt` into a fresh temporary directory. Commands below give the equivalent steps in an activated Python environment.

```powershell
python -m pip install -r requirements.txt
python -m unittest -v test_model
```

All five tests passed. They exercised the benchmark known answer, vintage parsing and rejection, the Streamlit missing-vintage hold, and the saved scenario using a rate fixture. The replay reproduced 65% equity, 32% investment-grade bonds, 3% bills, 6.90% five-year annualized net return, 11.04% volatility, both stress stops, and the 0% live deployment recommendation. [Tests](../test_model.py)

A separate live call through `rates.fetch_signal` retrieved the October 1 observation at 5.24% from the October 4 vintage for the October 5 decision. Retrieval time was 2026-11-21T21:28:02.525653+00:00. [ALFRED CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-10-04&cosd=2026-09-20&coed=2026-10-04)

The GitHub clone and reviewer-access check remain pending. This replay used the local submission files.
