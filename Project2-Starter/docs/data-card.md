# DGS10 data card

DGS10 is the Board of Governors' daily 10-year constant-maturity U.S. Treasury yield, in percentage points, distributed by the St. Louis Fed. Missing entries are excluded. The yield is used as a policy input. Sleeve returns remain course assumptions. [ALFRED series](https://alfred.stlouisfed.org/series?seid=DGS10)

For a decision at 9:30 a.m. New York time, request the prior calendar day's ALFRED vintage. Use the latest valid observation at or before that vintage and no more than seven calendar days older. The observation date and vintage are different because of publication lag, holidays, and possible revisions. The app shows both dates, the retrieval timestamp, and the source URL when the input is admitted.

At 5.00% or above, cap global equities at 65%. Below 5.00%, apply the standard mandate limits. The trigger and cap are draft policy parameters. The project has yet to validate them against historical outcomes.

Hold the live rebalance if the source is unavailable, the CSV does not identify the requested vintage, the observation is stale, or the data fail validation. Recheck the historical source before changing the hold. Today's observation is never substituted for a missing historical vintage.
