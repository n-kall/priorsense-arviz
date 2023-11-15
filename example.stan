data {
  int N;
  vector[N] x;
}

parameters {

  real mu;
  real<lower=0> sigma;

}

model {

  target += normal_lpdf(mu | 0, 10);
  target += normal_lpdf(sigma | 0, 100);

  target += normal_lpdf(x | mu, sigma);

}

generated quantities {

  real lprior;
  
  vector[N] log_lik;

  lprior = normal_lpdf(mu | 0, 10) + normal_lpdf(sigma | 0, 100);
  
  for (n in 1:N) {
    log_lik[n] = normal_lpdf(x[n] | mu, sigma);
  }

}
