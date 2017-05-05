# In development

This project is not yet ready for use, please star it and stay tuned for news.

# PyBAS
Python Bayesian Analysis using Stan

Tired of writing or copying the same models over and over, and waiting for them to compile?

PyBAS is an easy way to do applied Bayesian data analysis, with out-of-the-box solutions for the most common statistical problems. 

* Bayesian versions of the classical statistical tests:
   * t-test (paired, pooled variance)
   * ANOVA (n-way, interactions, covariates)
   * Chi-squared
   * Binomial proportion
* BEST: Bayesian Estimation Supercedes the t-test
* GLM: Generalized Linear Models
* Automatic selection of weakly informative priors
* Effect size: Cohen's d, Hedge's g
* Credible intervals and HPD
* Posterior mean and median
* Histogram and trace plots
* Pre-compiled Stan models

Powered by Stan.

## Example

```python
from pybas.tests import t_test

x = [-3, 4, 5, 2.5, 0.9]
y = [1, 2, 1.8, 4, 3.5]

t = t_test(x, y)
t.fit()

es = t.effect_size()
print(es)

es.plot_hist()
```

## Requirements

* Python 3
* PyStan
* Numpy, scipy
* Matplotlib (optional)

## Installation