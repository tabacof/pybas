data {
    int K; // Number of groups
    int N; // Number of examples per group
    real y[N, K]; // Observations
}
parameters {
    real mu; // Mean
    vector[K-1] theta_free; // Effects
    real<lower=0> sigma_likelihood; // Noise std
    real<lower=0> sigma_theta; // Effect std
}
transformed parameters {
  vector[K] theta; // Effects with sum to zero constraint
  for(k in 1:(K-1)) theta[k] <- theta_free[k];
  theta[K] <- -sum(theta_free);
}
model {
    // Weakly informative priors
    mu ~ normal(0, 10);
    sigma_likelihood ~ cauchy(0, 10);
    theta_free ~ normal(0, sigma_theta);
    sigma_theta ~ cauchy(0, 10);
    for (i in 1:N)
        for (j in 1:K)
            y[i][j] ~ normal(mu + theta[j], sigma_likelihood);
}