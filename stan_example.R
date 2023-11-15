library(cmdstanr)
library(priorsense)

csvs <- list.files(pattern = "*.csv")

fit <- as_cmdstan_fit(files = csvs)

lik <- powerscale_sensitivity(fit, component = "likelihood", variable = c("mu", "sigma"))$sensitivity$likelihood

pri <- powerscale_sensitivity(fit, component = "prior", variable = c("mu", "sigma"), is_method = "psis")$sensitivity$prior



#sprintf("%.13f", lik)

sprintf("%.13f", pri)


# manual
mu <- posterior::extract_variable(fit$draws(), "mu")
lprior <- posterior::extract_variable(fit$draws(), "lprior")

alpha1 <- 4
ps1 <- loo::psis(lprior * (alpha1 - 1))
lw1 <- weights(ps1)
k1 <- ps1$diagnostics$pareto_k

j1 <- cjs_dist(mu, mu, exp(lw1), NULL)

alpha2 <- 0.5
ps2 <- loo::psis(lprior * (alpha2 - 1))

lw2 <- weights(ps2)
k2 <- ps2$diagnostics$pareto_k
p
j2 <- cjs_dist(mu, mu, exp(lw2), NULL)

sprintf("%.13f", k1)
sprintf("%.13f", k2)


sprintf("%.13f", j1)
sprintf("%.13f", j2)

diag <- (j1 + j2) / (2 * log(1 + 0.01, base = 2))

sprintf("%.13f", diag)
