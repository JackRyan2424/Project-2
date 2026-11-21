from datetime import date, datetime
from zoneinfo import ZoneInfo

import streamlit as st
from rates import fetch_signal

from portfolio import (
    CORRELATIONS, OBJECTIVE_RETURN, SLEEVES, benchmark_weights,
    covariance_matrix, equal_weights, expected_return,
    inverse_volatility_weights, portfolio_volatility, validate_inputs,
)

MIN_BILLS = 0.03
MAX_VOLATILITY = 0.12
RATE_TRIGGER = 5.0
HIGH_RATE_EQUITY_CAP = 0.65
COST_BPS = 10
STRESS_CASES = {
    "Equity and credit selloff (1 month)": ((0, 0.02, -0.04, -0.15), 0.12, 0.03, 10),
    "Sticky inflation (3 months)": ((0.0075, -0.08, -0.06, -0.12), 0.10, 0.05, 30),
}


@st.cache_data(ttl=3600, max_entries=32, show_spinner="Loading ALFRED vintage")
def load_signal(decision_date):
    return fetch_signal(decision_date)


st.set_page_config(page_title="Meridian reserve allocation", layout="wide")
st.title("Meridian reserve allocation")
st.caption("AI assisted with implementation and drafting. Jack Ryan owns the project decisions. For education only. This is not investment advice.")
st.info("Draft model using course training assumptions. Returns and volatility are annualized model inputs and estimates.")

st.subheader("Draft mandate")
st.write("Target at least 6.5% expected first-year return after entry cost with annual volatility of 12% or less. Hold at least 3% in Treasury bills for distributions. Fully invest across the four eligible sleeves with no short positions.")
st.caption("Benchmark is 60% global equity and 40% investment-grade bonds.")

st.subheader("Point-in-time rate signal")
today = datetime.now(ZoneInfo("America/New_York")).date()
decision_date = st.date_input("Decision date (9:30 a.m. New York time)",
                              date(2026, 10, 5), min_value=date(2005, 6, 30), max_value=today)
st.caption("At DGS10 of 5.00% or above, cap global equity at 65%. Below 5.00%, apply the standard mandate limits. The rate rule is a provisional exposure limit.")
signal = None
if st.checkbox("Load prior-day ALFRED vintage"):
    try:
        signal = load_signal(decision_date)
    except (OSError, ValueError, TypeError) as exc:
        st.warning(f"Rebalance on hold. The historical vintage could not be admitted ({exc}).")

equity_cap = 1.0
if signal:
    vintage, observation, rate, retrieved, url = signal
    equity_cap = HIGH_RATE_EQUITY_CAP if rate >= RATE_TRIGGER else 1.0
    st.write(f"**{rate:.2f}% DGS10** · Observation {observation} · Vintage {vintage}")
    st.caption(f"[ALFRED CSV]({url}) · Retrieved {retrieved} UTC")
else:
    st.caption("Training comparison uses the standard limits. Live decision status is on hold until the vintage is admitted.")

validate_inputs(SLEEVES, CORRELATIONS, OBJECTIVE_RETURN)
covariance = covariance_matrix(SLEEVES, CORRELATIONS)


def candidate_weights():
    for bills in range(round(MIN_BILLS * 100), 101):
        for notes in range(101 - bills):
            for bonds in range(101 - bills - notes):
                equity = 100 - bills - notes - bonds
                yield [bills / 100, notes / 100, bonds / 100, equity / 100]


@st.cache_data(max_entries=1)
def constrained_weights(sleeves, covariance, equity_cap):
    feasible = (
        weights for weights in candidate_weights()
        if weights[3] <= equity_cap and portfolio_volatility(weights, covariance) <= MAX_VOLATILITY
    )
    return max(feasible, key=lambda weights: expected_return(weights, sleeves), default=None)


portfolios = {
    "Benchmark": benchmark_weights(SLEEVES),
    "Equal weight": equal_weights(SLEEVES),
    "Inverse volatility": inverse_volatility_weights(SLEEVES),
}
candidate = constrained_weights(SLEEVES, covariance, equity_cap)
if candidate is None:
    st.warning("No portfolio met the bills floor and volatility cap.")
else:
    portfolios["Constrained"] = candidate

results = []
benchmark = portfolios["Benchmark"]
for name, weights in portfolios.items():
    annual_return = expected_return(weights, SLEEVES)
    volatility = portfolio_volatility(weights, covariance)
    turnover = 0.5 * sum(abs(weight - initial) for weight, initial in zip(weights, benchmark))
    transition_cost = turnover * COST_BPS / 10_000
    checks = {
        "return target after cost": annual_return - transition_cost >= OBJECTIVE_RETURN,
        "volatility cap": volatility <= MAX_VOLATILITY,
        "bills floor": weights[0] >= MIN_BILLS,
        "rate-conditioned equity cap": weights[3] <= equity_cap,
    }
    failures = [rule for rule, passes in checks.items() if not passes]
    results.append({
        "Portfolio": name,
        "Expected return": f"{annual_return:.2%}",
        "First-year return after entry cost": f"{annual_return - transition_cost:.2%}",
        "One-way turnover": f"{turnover:.2%}",
        "Volatility": f"{volatility:.2%}",
        "Mandate verdict": "Fail: " + ", ".join(failures) if failures else "Pass",
        **{sleeve["name"]: f"{weight:.2%}" for sleeve, weight in zip(SLEEVES, weights)},
    })

st.subheader("Portfolio comparison")
st.dataframe(results, hide_index=True, alt="Portfolio weights, return, volatility, and mandate verdicts")
st.caption("The constrained allocation maximizes gross expected return across whole-percentage weights that meet the bills floor, volatility cap, and rate-conditioned equity cap.")
st.caption("Entry cost is 10 bp per dollar of one-way turnover from the 60/40 benchmark. No recurring fees are assumed.")

st.subheader("Stress tests")
stress = []
stop = True
if candidate is not None:
    stop = False
    volatility = portfolio_volatility(candidate, covariance)
    turnover = 0.5 * sum(abs(weight - initial) for weight, initial in zip(candidate, benchmark))
    for name, (shocks, vol_cap, bills_floor, cost_bps) in STRESS_CASES.items():
        gross = sum(weight * shock for weight, shock in zip(candidate, shocks))
        net = gross - turnover * cost_bps / 10_000
        failed = []
        if net <= -0.10:
            failed.append("loss of 10% or more")
        if volatility > vol_cap:
            failed.append("volatility cap")
        if candidate[0] < bills_floor:
            failed.append("bills floor")
        stop = stop or bool(failed)
        stress.append({"Scenario and window": name, "Sleeve shocks (bills / notes / IG / equity)": " / ".join(f"{x:+.2%}" for x in shocks),
                       "Entry cost (bp)": cost_bps, "Vol cap": f"{vol_cap:.0%}", "Bills floor": f"{bills_floor:.0%}",
                       "Net window return": f"{net:.2%}", "Stop reason": ", ".join(failed) or "None"})
    st.dataframe(stress, hide_index=True, alt="Hypothetical stress windows and stop conditions")
    st.caption("These scenarios apply hypothetical sleeve shocks to fixed starting weights and deduct a one-time transition cost. Annual volatility uses the base covariance; stress limits are shown per row.")

candidate_passes = candidate is not None and results[-1]["Mandate verdict"] == "Pass"
if not signal or stop or not candidate_passes:
    st.warning("Recommendation: paper pilot only. Authorize 0% of the reserve for live deployment while a data, mandate, or stress stop is active.")
else:
    st.info("Recommendation: paper pilot. Use the displayed allocation as the test target and monitor vintage eligibility, reserve coverage, volatility, and stress losses before seeking live approval.")
st.caption("Draft paper-pilot equity range: 60% to 65%. Bring any target outside that range back to the committee.")
