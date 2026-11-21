# Meridian reserve allocation decision memo

OpenAI Codex assisted with code, validation, and drafting. Jack Ryan is responsible for accepting or revising the draft analysis and making the decision. For education only. This is not investment advice.

## Committee ask

Authorize a paper pilot and keep live deployment at 0%. Pilot equity targets can range from 60% to 65% as a provisional monitoring range, with the actual target subject to the mandate and rate rule. A target outside that range goes back to the committee. Keep distributions covered with at least 3% in Treasury bills.

## Evidence and limits

The model compares the 60/40 benchmark, equal weight, inverse volatility, and a constrained allocation across four sleeves. It uses course return, volatility, and correlation estimates. Entry cost is 10 bp per dollar of one-way turnover from the benchmark. The rate rule caps equity at 65% when prior-day-vintage DGS10 reaches 5.00%. The executed table records the input and portfolio verdicts. [Executed output](../visible-output.md)

For the October 5, 2026 decision, the October 4 vintage returned 5.24% from the October 1 observation. The constrained portfolio held 65% global equities, 32% investment-grade bonds, and 3% bills. It passed the modeled checks with 6.90% projected five-year annualized net return, 11.04% annual volatility, 8.00% modeled annual turnover, and 100% modeled five-day liquidity. The screen assumes 2.5% annual CPI and one transition from the benchmark. Realized rolling five-year compliance remains unverified.

One-month equity and credit stress and three-month sticky inflation stress apply hypothetical sleeve shocks to fixed holdings. Sticky inflation also raises the cost to 30 bp, increases the bill floor to 5%, and tightens the volatility cap to 10%. These estimates support a paper pilot only.

The one-month selloff returned −11.04% after entry cost, breaching the 10% loss stop. The three-month inflation case returned −9.72% and breached its tighter volatility cap and bills floor.

## Monitoring and reversal

For each decision, monitor vintage eligibility, rolling five-year net return relative to CPI plus 4 percentage points, annual volatility, payout coverage, turnover, five-day liquidity, and each scenario's net loss. Hold a live rebalance if the vintage fails admission, the mandate fails, a stress constraint fails, or a net stress loss reaches 10%. Return to the committee with validated cost and risk inputs, a completed Changed-Input Record, and a rerun clearing those stops before requesting live approval.
