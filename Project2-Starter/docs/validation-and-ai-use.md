# Validation and AI use

The base sleeve inputs come from Jack Ryan's earlier course portfolio exercise. The DGS10 availability rule follows the Lab 17 data card and retrieves the ALFRED vintage as of the prior calendar day. The benchmark doubles as the assumed starting allocation for turnover. Stress shocks, stop thresholds, and cost assumptions are provisional. No empirical calibration of the policy rule or historical return estimates has been completed.

## AI use

| Date | Tool | Material use | Disposition |
| --- | --- | --- | --- |
| 2026-11-17 | OpenAI Codex, exact model identifier unavailable in the session | Reused the course portfolio math and built the Streamlit comparison | Verified the app displayed four portfolio rows and their mandate verdicts. |
| 2026-11-17 | OpenAI Codex, exact model identifier unavailable in the session | Drafted the rate rule, stress inputs and stop logic, and submission documents | Provisional pending student review. The data admission path is checked against malformed and ineligible fixtures. |

## Locked Changed-Input Record

Pending the student's AI-off prediction. Before running the chosen change, Jack Ryan must record the input, old and new values and units, expected direction, decision effect, and reasoning, then commit it to GitHub. Preserve the pre-run commit link here. Afterward attach before and after output, the observed direction and decision effect, and a diagnosis of any discrepancy.

## Executed checks

- Streamlit AppTest rendered four portfolio rows and two stress rows. A simulated unavailable vintage triggered the hold message.
- Parser fixtures rejected an undated series header, future observation, and stale observation.
- The actual October 4 ALFRED vintage returned the October 1 observation at 5.24%. The app enforced the 65% equity cap and flagged the sticky-inflation stops. [Executed output](../visible-output.md)
- On November 17, 2026, a clean Windows Python 3.14 virtual environment installed the dependencies from requirements.txt. Streamlit AppTest rendered four portfolios and two stress cases, loaded the October 4 ALFRED vintage, and verified the 65% equity cap. All 14 relative Markdown links resolved. GitHub and YouTube reviewer-access checks remain pending.

## Lab 13 alignment check

On November 17, 2026, Codex reviewed the original Lab 13 submission and replaced the first-year hurdle with a five-year annualized net projection screened against assumed CPI plus 4 percentage points. It added the annual turnover and five-day liquidity rules and reran the base historical example. Streamlit AppTest confirmed that equal weight and inverse volatility breached the 25% turnover cap and the constrained allocation had 8% turnover and 100% modeled five-day liquidity. The latter relies on the assumed redemption terms of all four sleeves. The historical example is ordinary app verification. The separate Locked Changed-Input Record remains pending. [Original Lab 13](https://github.com/JackRyan2424/Lab-13)
