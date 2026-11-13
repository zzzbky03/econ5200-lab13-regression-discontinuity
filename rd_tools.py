"""Regression discontinuity helpers that never report an estimate alone (ECON 5200 Lab 13).

The design rule: every estimate comes back with the bandwidth that produced it, because an RD
number without its bandwidth is one point on a curve the reader cannot see.
"""
import pandas as pd
from rddensity import rddensity
from rdrobust import rdrobust


def rd_estimate(df: pd.DataFrame, outcome: str, running: str, cutoff: float,
                bandwidth: float | None = None) -> pd.Series:
    """Local linear RD, triangular kernel: the estimate, its robust test, h, and n on each side."""
    fit = rdrobust(y=df[outcome], x=df[running], c=cutoff, h=bandwidth)
    return pd.Series({"estimate": fit.coef.loc["Conventional", "Coeff"],
                      "robust_ci_low": fit.ci.loc["Robust", "CI Lower"],
                      "robust_ci_high": fit.ci.loc["Robust", "CI Upper"],
                      "robust_p": fit.pv.loc["Robust", "P>|z|"],
                      "bandwidth": fit.bws.loc["h", "left"],
                      "n_left": fit.N_h[0],
                      "n_right": fit.N_h[1]})


def bandwidth_curve(df: pd.DataFrame, outcome: str, running: str, cutoff: float,
                    grid) -> pd.DataFrame:
    """The estimate at each bandwidth in grid, and the rows it used: the sensitivity table."""
    table = pd.DataFrame([rd_estimate(df, outcome, running, cutoff, h) for h in grid])
    return table[["bandwidth", "estimate", "n_left", "n_right"]].astype({"n_left": int, "n_right": int})


def design_checks(df: pd.DataFrame, running: str, cutoff: float,
                  covariates: list[str]) -> pd.DataFrame:
    """The density test, then an RD with each pre-treatment covariate as the outcome."""
    density = rddensity(X=df[running].to_numpy(dtype=float), c=cutoff)
    rows = [{"test": f"density of {running}", "estimate": float("nan"),     # nan: no estimate here
             "p_value": density.test["p_jk"]}]
    for covariate in covariates:
        result = rd_estimate(df, covariate, running, cutoff)
        rows.append({"test": f"jump in {covariate}", "estimate": result["estimate"],
                     "p_value": result["robust_p"]})
    return pd.DataFrame(rows)
