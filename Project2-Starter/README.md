# FIN43900 Project 2

AI assisted with implementation and drafting. Jack Ryan owns the project decisions. For education only. This is not investment advice.

## Run locally

From this folder, run:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run meridian_app.py
```

Open the local URL printed by Streamlit. Select a decision date and check **Load prior-day ALFRED vintage**. The historical example defaults to October 5, 2026. Network access is needed to admit the signal. Without a valid vintage, the training comparison stays available and the app holds any live rebalance.

## Portfolio comparison

The app compares a 60/40 benchmark, equal weight, inverse volatility, and a constrained allocation. It reuses the course training returns, volatilities, and correlations from the existing portfolio exercise. Those inputs are illustrative.

Lab 13 sets a seven-year horizon, annual rebalancing, and a CPI plus 4 percentage point return objective net of costs over rolling five-year periods. Its rules include twelve months of payout reserves, a 25% annual turnover cap without committee approval, at least 90% redeemable within five business days, and an 8% single-issuer limit with exemptions for the modeled sleeves. It prohibits borrowing, short sales, and derivatives. The reserve minimum represents four quarterly distributions of $750,000 from a $100 million reserve. [Original Lab 13 submission](https://github.com/JackRyan2424/Lab-13)

The pilot adds a 12% annual volatility cap and a 3% bills-only floor. It ranks whole-percentage allocations by projected five-year annualized return net of a one-time transition cost. It assumes 2.5% annual CPI, constant sleeve returns, zero recurring costs, modeled redemption times, and one annual move from the benchmark as the turnover proxy. The projection screens against CPI plus 4 percentage points. Actual rolling performance requires realized data. Lab 13 leaves the calendar-year loss rule and pilot optimization objective unresolved. The proposed ranking method and stress stops require committee review.

Start with the [executed output](visible-output.md), [DGS10 data card](docs/data-card.md), and [decision memo](docs/decision-memo.md). The [validation and AI-use record](docs/validation-and-ai-use.md) and [submission manifest](docs/manifest.md) track remaining evidence.

