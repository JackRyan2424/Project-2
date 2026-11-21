# Validation and AI use

The base sleeve inputs come from Jack Ryan's earlier course portfolio exercise. The DGS10 availability rule follows the Lab 17 data card and retrieves the ALFRED vintage as of the prior calendar day. The benchmark doubles as the assumed starting allocation for turnover. Stress shocks, stop thresholds, and cost assumptions are provisional. No empirical calibration of the policy rule or historical return estimates has been completed.

## AI use

| Date | Tool | Material use | Disposition |
| --- | --- | --- | --- |
| 2026-11-17 | OpenAI Codex, exact model identifier unavailable in the session | Reused the course portfolio math and built the Streamlit comparison | Verified the app displayed four portfolio rows and their mandate verdicts. |
| 2026-11-17 | OpenAI Codex, exact model identifier unavailable in the session | Drafted the rate rule, stress inputs and stop logic, and submission documents | Provisional pending student review. The data admission path is checked against malformed and ineligible fixtures. |
| Submission audit | OpenAI Codex | Reconciled the written return metric with the app, externalized training assumptions, and added automated checks and worked evidence | See the [known answer](../evidence/known-answer.md) and [cold-run log](../evidence/known-answer.md#cold-run-log). |

## Locked Changed-Input Record

The Lab 20 readiness note reports a starting estimate of 6.51%, a prediction of roughly 7%, and an increase with the same paper-pilot recommendation. The changed input, exact after value, and original pre-run timestamp or commit remain unverified. Recover the original evidence if available.

### Fresh stress test

**Pre-run prediction by Jack Ryan, formulated with AI closed.**

I will change the global equity shock in the one-month equity and credit selloff from **−15.00% to −12.00%**. I expect the scenario's net portfolio return to improve because the equity decline is smaller. I will keep the sticky-inflation inputs and portfolio allocation fixed. I expect the sticky-inflation stops to remain in place and would defer live adoption of the allocation. The timestamp/commits may be incorrect because I did the before and after scenario before I put the the changes into GitHub. 

**Baseline to verify.** The figures reported with the prediction are a sticky-inflation loss of 10.16%, volatility of 11.98% versus a 10% cap, and bills of 3% versus a 5% floor. The [saved October 5 output](../visible-output.md) instead shows a 9.72% sticky-inflation loss, 11.04% volatility, and 3% bills. That saved run shows volatility and bills stops. Use the actual baseline screenshot to identify which run the fresh test uses.

**Evidence to attach.** Pre-run timestamp and commit link, baseline screenshot, rerun screenshot, exact net window return and stop reasons before and after, and the actual decision effect.

## Executed checks

- Streamlit AppTest rendered four portfolio rows and two stress rows. A simulated unavailable vintage triggered the hold message.
- Parser fixtures rejected an undated series header, future observation, and stale observation.
- The actual October 4 ALFRED vintage returned the October 1 observation at 5.24%. The app enforced the 65% equity cap and flagged the sticky-inflation stops. [Executed output](../visible-output.md)
- A fresh dependency installation and all five automated tests passed on November 21, 2026. A separate ALFRED call confirmed the historical vintage. The GitHub clone and reviewer-access check remain pending. [Cold-run log](../evidence/known-answer.md#cold-run-log)

## DGS10 data card

DGS10 is the Board of Governors' daily 10-year constant-maturity U.S. Treasury yield, in percentage points, distributed by the St. Louis Fed. Missing entries are excluded. The yield is used as a policy input. Sleeve returns remain course assumptions. [ALFRED series](https://alfred.stlouisfed.org/series?seid=DGS10)

For a decision at 9:30 a.m. New York time, request the prior calendar day's ALFRED vintage. Use the latest valid observation at or before that vintage and no more than seven calendar days older. The observation date and vintage are different because of publication lag, holidays, and possible revisions. The app shows both dates, the retrieval timestamp, and the source URL when the input is admitted.

At 5.00% or above, cap global equities at 65%. Below 5.00%, apply the standard mandate limits. The trigger and cap are draft policy parameters. The project has yet to validate them against historical outcomes.

Hold the live rebalance if the source is unavailable, the CSV does not identify the requested vintage, the observation is stale, or the data fail validation. Recheck the historical source before changing the hold. Today's observation is never substituted for a missing historical vintage.
