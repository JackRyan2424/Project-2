# Project 2 recording notes

Use the times as rehearsal cues. Enter actual chapter times in the manifest after recording. Start all three videos with these statements once you have reviewed the work and made your own decision.

> I used OpenAI Codex to help build and test the app and draft documentation. The analysis and decision are mine.
>
> This is for education only. It is not investment advice.

## Video 1 · How the system and my thinking changed · target 2:40

| Time | Show | Cover |
| --- | --- | --- |
| 0:00 | App title or README | Give the opening statements. |
| 0:15 | Earlier portfolio exercise and Lab 17 | Explain how the exercise supplied the portfolio comparison and Lab 17 supplied the historical-vintage rule. |
| 0:55 | Portfolio and stress tables | Describe, in your own words, what changed in your thinking when you saw the base mandate pass and the stress stops trigger. |
| 1:35 | Your own independent check | One candidate is to hand-check one-way turnover using the displayed constrained and benchmark weights, then compare it to the app. Describe the check you actually performed and its result. |
| 2:20 | Decision memo | State the committee recommendation you support and the evidence that would change it. |

## Video 2 · Code and validation walkthrough · target 4:30

| Time | Show | Cover |
| --- | --- | --- |
| 0:00 | README and terminal | Give the opening statements and show the launch command. |
| 0:30 | rates.py and the app's signal panel | Show the decision date, prior-day vintage, latest eligible observation, and fail-closed behavior. Explain the 5.00% trigger and 65% equity cap. |
| 1:30 | portfolio.py and meridian_app.py | Walk through equal weight, inverse volatility, covariance-based risk, and the whole-percentage grid used for the constrained portfolio. |
| 2:30 | Portfolio and stress tables | Show 8% one-way turnover from the benchmark, a 10 bp base cost per dollar turned over, and the one- and three-month hypothetical stresses. Point out how the stress stops are evaluated. |
| 3:30 | Validation record | Describe the clean-install and invalid-data checks. Add the actual before/after evidence here once the Locked Changed-Input Record is complete. |

## Video 3 · Committee recommendation · target 4:20

| Time | Show | Cover |
| --- | --- | --- |
| 0:00 | Live app from the first frame | Give both opening statements and state the committee ask. The draft asks for a paper pilot with 0% live deployment and a 60% to 65% equity monitoring range. |
| 0:40 | Draft mandate and historical signal | Explain the Lab 13 CPI plus 4 percentage point rolling five-year net return objective, the 25% annual turnover cap, and the 90% five-day liquidity minimum. Explain the pilot 12% volatility cap and 3% bills floor. Select October 5, 2026 and admit the October 4 vintage. The October 1 observation was 5.24%. |
| 1:35 | Portfolio comparison | Show the constrained allocation of 65% global equities, 32% investment-grade bonds, and 3% bills. It passed the modeled rules with 6.90% projected five-year annualized net return, 11.04% annual volatility, 8.00% modeled turnover, and 100% modeled five-day liquidity. |
| 2:40 | Stress tests | Show the one-month equity and credit selloff at minus 11.04%, which breached the 10% loss stop. The three-month sticky inflation case lost 9.72% and breached the tighter volatility and bills limits. |
| 3:35 | Recommendation and decision memo | Explain which triggers hold a live rebalance and what evidence the committee would need before considering live approval. |

## Before publishing

- Rehearse the October 5 example with the prior-day vintage loaded. Cross-check the displayed values against the [executed output](../visible-output.md).
- Correct finance terms, attribution, dates, and numbers in the actual captions. Export the corrected transcripts as transcript-video-1.txt, transcript-video-2.txt, and transcript-video-3.txt.
- Add each YouTube URL, actual duration, and chapter index to the [manifest](manifest.md). Confirm each video is viewable while logged out.
