"""Run with: python portfolio.py. Returns and volatilities use decimals."""

import json
import math
from pathlib import Path


# Course training inputs. Correlation rows and columns follow sleeve order.
with Path(__file__).with_name("inputs.json").open(encoding="utf-8") as source:
    inputs = json.load(source)
SLEEVES = inputs["sleeves"]
CORRELATIONS = inputs["correlations"]
OBJECTIVE_RETURN = 0.065


def validate_inputs(sleeves, correlations, objective):
    n = len(sleeves)
    if n != 4 or len(correlations) != n or any(len(row) != n for row in correlations):
        raise ValueError("Provide four sleeves and a 4-by-4 correlation table.")
    if any(s[key] is None for s in sleeves for key in ("return", "volatility")) or any(
        value is None for row in correlations for value in row
    ):
        raise ValueError("Missing input data: replace every None in SLEEVES and CORRELATIONS with your table values.")
    if not math.isfinite(objective):
        raise ValueError("The objective return must be finite.")
    for sleeve in sleeves:
        if not math.isfinite(sleeve["return"]):
            raise ValueError("Expected returns must be finite.")
        if not math.isfinite(sleeve["volatility"]) or sleeve["volatility"] <= 0:
            raise ValueError("Volatilities must be positive and finite for inverse-volatility weights.")
    for i in range(n):
        for j in range(n):
            value = correlations[i][j]
            if not math.isfinite(value) or not -1 <= value <= 1:
                raise ValueError(f"Correlation at row {i + 1}, column {j + 1} must be between -1 and 1.")
            if value != correlations[j][i]:
                raise ValueError("The correlation table must be symmetric.")
        if correlations[i][i] != 1:
            raise ValueError("Every diagonal correlation must equal 1.")


def covariance_matrix(sleeves, correlations):
    return [
        [correlations[i][j] * a["volatility"] * b["volatility"]
         for j, b in enumerate(sleeves)]
        for i, a in enumerate(sleeves)
    ]


def benchmark_weights(sleeves):
    allocations = {"Investment-grade bond fund": 0.4, "Global equity index fund": 0.6}
    weights = [allocations.get(s["name"], 0.0) for s in sleeves]
    if not math.isclose(sum(weights), 1.0):
        raise ValueError("Benchmark requires the investment-grade bond and global equity sleeves.")
    return weights


def equal_weights(sleeves):
    return [1 / len(sleeves)] * len(sleeves)


def inverse_volatility_weights(sleeves):
    inverses = [1 / s["volatility"] for s in sleeves]
    total = sum(inverses)
    return [value / total for value in inverses]


def expected_return(weights, sleeves):
    return sum(w * s["return"] for w, s in zip(weights, sleeves))


def portfolio_volatility(weights, covariance):
    variance = sum(wi * wj * covariance[i][j]
                   for i, wi in enumerate(weights) for j, wj in enumerate(weights))
    if variance < -1e-12:
        raise ValueError("Negative portfolio variance: check the correlation table.")
    return math.sqrt(max(0.0, variance))


def reserve_eligible_weight(weights, sleeves):
    return sum(w for w, s in zip(weights, sleeves) if s["reserve"])


def meets_objective(portfolio_return, objective):
    return portfolio_return >= objective


def main():
    try:
        validate_inputs(SLEEVES, CORRELATIONS, OBJECTIVE_RETURN)
        covariance = covariance_matrix(SLEEVES, CORRELATIONS)
        portfolios = {
            "Benchmark": benchmark_weights(SLEEVES),
            "Equal weight": equal_weights(SLEEVES),
            "Inverse volatility": inverse_volatility_weights(SLEEVES),
        }
        results = []
        for name, weights in portfolios.items():
            result = expected_return(weights, SLEEVES)
            risk = portfolio_volatility(weights, covariance)
            reserve = reserve_eligible_weight(weights, SLEEVES)
            results.append((name, weights, result, risk, reserve))
        for name, weights, result, risk, reserve in results:
            print(f"\n{name}")
            for sleeve, weight in zip(SLEEVES, weights):
                print(f"  {sleeve['name']}: {weight:.1%}")
            print(f"  Expected return: {result:.2%}")
            print(f"  Volatility: {risk:.2%}")
            print(f"  Reserve-eligible weight: {reserve:.1%}")
            print(f"  Meets {OBJECTIVE_RETURN:.2%} return objective: "
                  f"{'Yes' if meets_objective(result, OBJECTIVE_RETURN) else 'No'}")
    except (ValueError, TypeError) as exc:
        print(f"Cannot calculate portfolios: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

