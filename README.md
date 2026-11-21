# FIN43900 Project 2

I used OpenAI Codex to help write the app, check it, and draft documentation. The analysis and decision are mine. This is for education only. It is not investment advice.

The Meridian Foundation investment committee is deciding whether to pilot the constrained reserve allocation and authorize any live capital. The recorded recommendation is a paper pilot with 0% live deployment. See the [validation and AI-use record](docs/validation-and-ai-use.md) for disclosures and checks.

## Run locally

Use Python 3.11 or later. From this folder, run:

```powershell
python -m pip install -r requirements.txt
python -m unittest -v test_model
python -m streamlit run app.py
```

Open the local URL printed by Streamlit. Select a decision date and check **Load prior-day ALFRED vintage**. The historical example defaults to October 5, 2026. Network access is needed to admit the signal. Without a valid vintage, the training comparison stays available and the app holds any live rebalance.

## Portfolio comparison

The app compares a 60/40 benchmark, equal weight, inverse volatility, and a constrained allocation. It reuses the course training returns, volatilities, and correlations from the existing portfolio exercise. Those inputs are illustrative.

The planning horizon is seven years with annual rebalancing. The modeled return hurdle is 6.5% annualized net over five years, using 2.5% assumed CPI plus 4 percentage points. The one-percentage-point grid maximizes projected five-year annualized net return after a one-time transition cost, subject to the turnover, liquidity, volatility, bills, and signal limits. The return hurdle is checked in the verdict. The 3% bills floor represents four quarterly distributions of $750,000 from a $100 million reserve.

The app uses the [training sleeve inputs](inputs.json) through `portfolio.py` and loads point-in-time DGS10 through `rates.py`. Restart Streamlit after changing the JSON. Return and volatility inputs use decimals. The projection assumes constant returns, zero recurring costs, and benchmark-based transition turnover. Stress losses and the modeled verdict depend on those assumptions. The calendar-year loss rule remains unresolved.

Start with the [executed output](visible-output.md), [DGS10 data card](docs/validation-and-ai-use.md#dgs10-data-card), and [decision memo](docs/decision-memo.md). The [validation and AI-use record](docs/validation-and-ai-use.md) and [submission manifest](docs/manifest.md) track remaining evidence.

The [evidence folder](evidence/) contains a worked reconciliation, an equity-only downside comparison, and the cold-run log.

