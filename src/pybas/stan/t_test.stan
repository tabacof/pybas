data {
    int n_x; // Number of examples of X
    int n_y; // Number of examples of Y
    real x[n_x]; // Observations of X
    real y[n_y]; // Observations of Y
}
parameters {
    real mu_x;
    real mu_y;
    real<lower=0> sd_x;
    real<lower=0> sd_y;
}
model {
	mu_x ~ normal(0, 5);
	mu_y ~ normal(0, 5);
	sd_x ~ cauchy(0, 5);
	sd_y ~ cauchy(0, 5);
	
	x ~ normal(mu_x, sd_x);
	y ~ normal(mu_y, sd_y);
}