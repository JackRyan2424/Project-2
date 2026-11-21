# Executed project output

Decision date: 2026-10-05 at 9:30 a.m. New York time.

Annual sleeve return assumptions are 3.5%, 4.3%, 5.0%, and 8.0%. Annual volatilities are 0.5%, 7%, 6%, and 16%, in bills, notes, investment-grade bonds, and equity order. The five-year projection uses constant 2.5% annual CPI and a 10 bp one-time cost per dollar of one-way turnover. The modeled target is CPI plus 4 percentage points. See the README for mandate and pilot limits.

**5.24% DGS10** · Observation 2026-10-01 · Vintage 2026-10-04
[ALFRED CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-10-04&cosd=2026-09-20&coed=2026-10-04) · Retrieved 2026-11-17T22:18:05.440373+00:00 UTC

| Portfolio | Expected return | Projected 5-year annualized net return | Annual one-way turnover proxy | Five-day liquid share | Volatility | Mandate verdict | Bills | 10-year note | Investment-grade bond fund | Global equity index fund |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Benchmark | 6.80% | 6.80% | 0.00% | 100.00% | 10.46% | Fail: payout reserve minimum, pilot bills floor | 0.00% | 0.00% | 40.00% | 60.00% |
| Equal weight | 5.20% | 5.19% | 50.00% | 100.00% | 5.21% | Fail: projected CPI + 4 target, annual turnover cap | 25.00% | 25.00% | 25.00% | 25.00% |
| Inverse volatility | 3.77% | 3.75% | 90.34% | 100.00% | 1.05% | Fail: projected CPI + 4 target, annual turnover cap | 84.32% | 6.02% | 7.03% | 2.63% |
| Constrained | 6.91% | 6.90% | 8.00% | 100.00% | 11.04% | Pass | 3.00% | 0.00% | 32.00% | 65.00% |

| Scenario and window | Sleeve shocks (bills / notes / IG / equity) | Entry cost (bp) | Vol cap | Bills floor | Net window return | Stop reason |
| --- | --- | --- | --- | --- | --- | --- |
| Equity and credit selloff (1 month) | +0.00% / +2.00% / -4.00% / -15.00% | 10 | 12% | 3% | -11.04% | loss of 10% or more |
| Sticky inflation (3 months) | +0.75% / -8.00% / -6.00% / -12.00% | 30 | 10% | 5% | -9.72% | volatility cap, bills floor |

Pass refers to the modeled rules. Actual rolling five-year results and the unresolved Lab 13 calendar-year loss rule remain unverified.

The equity-only sensitivity at the same allocation and cost produces a 9.758% net loss. The credit shock adds 1.28 percentage points of loss in the combined selloff. [Worked reconciliation](evidence/known-answer.md)

Recommendation: paper pilot only. Authorize 0% of the reserve for live deployment while a data, mandate, or stress stop is active.
