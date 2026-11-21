# Meridian reserve allocation decision memo

I used OpenAI Codex to help write the app, check it, and draft documentation. The analysis and decision are mine. This is for education only. It is not investment advice.

## Committee ask

Authorize a paper pilot and keep live deployment at 0%. Pilot equity targets can range from 60% to 65% as a provisional monitoring range, with the actual target subject to the mandate and rate rule. A target outside that range goes back to the committee. Keep distributions covered with at least 3% in Treasury bills.

## Evidence and limits

The model compares the 60/40 benchmark, equal weight, inverse volatility, and a constrained allocation across four sleeves. It uses course return, volatility, and correlation estimates. Entry cost is 10 bp per dollar of one-way turnover from the benchmark. The rate rule caps equity at 65% when prior-day-vintage DGS10 reaches 5.00%. The executed table records the input and portfolio verdicts. [Executed output](../visible-output.md)

The saved October 5, 2026 run reports 5.24% from the October 1 observation in the October 4 vintage. The constrained portfolio held 65% global equities, 32% investment-grade bonds, and 3% bills. It passed the modeled baseline with a 6.90% projected five-year annualized net return and 11.04% annual volatility. The mandate uses a seven-year planning horizon with annual rebalancing.

One-month equity and credit stress and three-month sticky inflation stress apply hypothetical sleeve shocks to fixed holdings. Sticky inflation also raises the cost to 30 bp, increases the bill floor to 5%, and tightens the volatility cap to 10%. These estimates support a paper pilot only.

The one-month selloff returned −11.04% after entry cost, breaching the 10% loss stop. The three-month inflation case returned −9.72% and breached its tighter volatility cap and bills floor.

At the same weights and transition cost, a 15% global-equity decline with all other sleeve shocks set to zero produces a 9.758% net loss. The credit fund's 4% decline adds 1.28 percentage points of loss and takes the combined case through the 10% stop. [Worked reconciliation](../evidence/known-answer.md)

## Monitoring and reversal

For each decision, monitor vintage eligibility, projected five-year annualized net return, annual volatility, bill coverage, and each scenario's net loss. Hold a live rebalance if the vintage fails admission, the mandate fails, a stress constraint fails, or a net stress loss reaches 10%. Return to the committee with validated cost and risk inputs, a completed Changed-Input Record, and a rerun clearing those stops before requesting live approval. [Validation and AI use](validation-and-ai-use.md)
