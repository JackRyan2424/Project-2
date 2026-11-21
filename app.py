from datetime import date, datetime
from math import isclose
from zoneinfo import ZoneInfo

import streamlit as st
from rates import fetch_signal

from portfolio import (
    CORRELATIONS, SLEEVES, benchmark_weights,
    covariance_matrix, equal_weights, expected_return,
    inverse_volatility_weights, portfolio_volatility, validate_inputs,
)

MIN_BILLS = 0.03
MIN_RESERVE = 0.03
MAX_TURNOVER = 0.25
MIN_LIQUID = 0.90
REDEMPTION_DAYS = (1, 1, 3, 2)
CPI_ASSUMPTION = 0.025
CPI_PREMIUM = 0.04
RETURN_TARGET = CPI_ASSUMPTION + CPI_PREMIUM
RETURN_YEARS = 5
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

st.subheader("Meridian Foundation mandate")
st.write("Lab 13 sets a seven-year planning horizon with annual rebalancing. The return objective is CPI plus 4 percentage points net of costs over rolling five-year periods. The benchmark is 60% global equity and 40% U.S. investment-grade bonds.")
st.write("Cover twelve months of payouts with at least 3% in eligible reserves. Keep annual turnover at or below 25% without a committee exception, and keep at least 90% redeemable within five business days. No borrowing, short sales, or derivatives. The four modeled sleeves are direct U.S. Treasury holdings and diversified funds, which are exempt from the 8% single-issuer limit under Lab 13.")
st.caption("Pilot assumptions include a 12% annual volatility cap, a bills-only 3% floor, and 2.5% annual CPI for the illustrative five-year projection. Lab 13 leaves the calendar-year loss rule unresolved. The hypothetical stress stops are separate pilot rules.")

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

validate_inputs(SLEEVES, CORRELATIONS, RETURN_TARGET)
covariance = covariance_matrix(SLEEVES, CORRELATIONS)
benchmark = benchmark_weights(SLEEVES)


def turnover_from_benchmark(weights):
    return 0.5 * sum(abs(weight - initial) for weight, initial in zip(weights, benchmark))


def liquid_weight(weights):
    return sum(weight for weight, days in zip(weights, REDEMPTION_DAYS) if days <= 5)


def projected_net_return(weights, sleeves):
    gross = expected_return(weights, sleeves)
    entry_cost = turnover_from_benchmark(weights) * COST_BPS / 10_000
    return (1 - entry_cost) ** (1 / RETURN_YEARS) * (1 + gross) - 1


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
        if weights[3] <= equity_cap
        and turnover_from_benchmark(weights) <= MAX_TURNOVER + 1e-12
        and liquid_weight(weights) >= MIN_LIQUID
        and portfolio_volatility(weights, covariance) <= MAX_VOLATILITY
    )
    return max(feasible, key=lambda weights: projected_net_return(weights, sleeves), default=None)


portfolios = {
    "Benchmark": benchmark,
    "Equal weight": equal_weights(SLEEVES),
    "Inverse volatility": inverse_volatility_weights(SLEEVES),
}
candidate = constrained_weights(SLEEVES, covariance, equity_cap)
if candidate is None:
    st.warning("No portfolio met the modeled allocation constraints.")
else:
    portfolios["Constrained"] = candidate

results = []
for name, weights in portfolios.items():
    annual_return = expected_return(weights, SLEEVES)
    volatility = portfolio_volatility(weights, covariance)
    turnover = turnover_from_benchmark(weights)
    liquidity = liquid_weight(weights)
    net_return = projected_net_return(weights, SLEEVES)
    checks = {
        "fully invested and long-only": isclose(sum(weights), 1) and min(weights) >= 0,
        "projected CPI + 4 target": net_return >= RETURN_TARGET,
        "annual turnover cap": turnover <= MAX_TURNOVER + 1e-12,
        "five-day liquidity minimum": liquidity >= MIN_LIQUID,
        "payout reserve minimum": weights[0] + weights[1] >= MIN_RESERVE,
        "pilot volatility cap": volatility <= MAX_VOLATILITY,
        "pilot bills floor": weights[0] >= MIN_BILLS,
        "rate-conditioned equity cap": weights[3] <= equity_cap,
    }
    failures = [rule for rule, passes in checks.items() if not passes]
    results.append({
        "Portfolio": name,
        "Expected return": f"{annual_return:.2%}",
        "Projected 5-year annualized net return": f"{net_return:.2%}",
        "Annual one-way turnover proxy": f"{turnover:.2%}",
        "Five-day liquid share": f"{liquidity:.2%}",
        "Volatility": f"{volatility:.2%}",
        "Mandate verdict": "Fail: " + ", ".join(failures) if failures else "Pass",
        **{sleeve["name"]: f"{weight:.2%}" for sleeve, weight in zip(SLEEVES, weights)},
    })

st.subheader("Portfolio comparison")
st.dataframe(results, hide_index=True, alt="Portfolio weights, return, volatility, and mandate verdicts")
st.caption("The pilot ranks whole-percentage allocations by projected five-year annualized net return. The modeled verdict compares that projection with assumed CPI plus 4 percentage points. Actual rolling five-year performance requires realized returns, costs, and CPI.")
st.caption("Turnover assumes one annual move from the benchmark. The model compounds constant annual returns for five years and deducts the initial transition cost of 10 bp per dollar of one-way turnover. Recurring costs are assumed zero. Five-day liquidity uses modeled redemption times of 1, 1, 3, and 2 business days for bills, notes, bond fund, and equity fund.")

st.subheader("Stress tests")
stress = []
stop = True
if candidate is not None:
    stop = False
    volatility = portfolio_volatility(candidate, covariance)
    turnover = turnover_from_benchmark(candidate)
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
