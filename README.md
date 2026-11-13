# Regression Discontinuity: Bandwidths, Manipulation and Close Elections

## Objective
I used regression discontinuity to estimate effects at a cutoff, and I checked how much the answer depends on the bandwidth and whether the design can be trusted.

## Methodology
- Simulated a grant given to students with a need index of 50 or above, with a true effect of 8 percentage points on enrolment.
- Compared a global quadratic fit with a local linear fit from `rdrobust`, which picks its own bandwidth.
- Estimated the effect at seven bandwidths, then repeated the simulation 300 times to measure bias, variance and root mean squared error at each one.
- Ran a density test (`rddensity`) on clean data and on data where units moved across the cutoff.
- Ran a covariate continuity test on a prior test score, with and without a planted jump at the cutoff.
- Estimated how much more liberally a US House district is represented when a Democrat barely wins, using the data of Lee, Moretti and Butler (2004).
- Wrote my own local linear RD estimator with a triangular kernel using weighted least squares, and checked it against `rdrobust`.
- Saved the main tools in `src/rd_tools.py`, which reports every estimate with its bandwidth.

## Key Findings
- The global quadratic estimated 0.0357, less than half of the true 0.08. The local linear fit at a bandwidth of 16.1 estimated 0.0789.
- Across 300 simulations, the root mean squared error was smallest at a bandwidth of 20. Small bandwidths were noisy and large ones were biased.
- The density test found manipulation when units moved across the cutoff (p = 0.0022).
- In close US House elections, a barely-winning Democrat is 46.491 ADA points more liberal than a barely-winning Republican. This supports the idea that voters choose policies rather than politicians moving to the median voter.
- My own estimator matched `rdrobust`.
