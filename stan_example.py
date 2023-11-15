import cmdstanpy as stan
import arviz as az
import numpy as np

model = stan.CmdStanModel(stan_file = "example.stan")

x = [1,2,3,4,5,6,7,8,9,10]

dat = {"N" : len(x), "x" : x}
fit = model.sample(data=dat, iter_sampling = 10000, seed = 1234, output_dir="./")
idata = az.from_cmdstanpy(fit)

lprior = az.extract(idata, var_names="lprior", group="posterior", combined=True)

idata.add_groups(
    log_prior={"lprior": lprior}
)

posterior_glob = "example-*_[0-9].csv"

idata = az.from_cmdstan(
    posterior = posterior_glob,
    )

lprior = az.extract(idata, var_names="lprior", group="posterior", combined=True)

idata.add_groups(
    log_prior={"lprior": lprior}
)

liksens = az.psens(idata, component="likelihood", var_names="~lprior")

priorsens = az.psens(idata, component="prior", var_names="~lprior")

#print("likelihood:", liksens)

print("prior:", priorsens)

#print("{0:.13f}".format(liksens["mu"]))
#print("{0:.13f}".format(liksens["sigma"]))

print("{0:.13f}".format(priorsens["mu"]))
print("{0:.13f}".format(priorsens["sigma"]))



# # manual
# mu = az.extract(idata, var_names="mu", group="posterior", combined=True)
# alpha1 = 1.5
# lw1, k1 = az.psislw(np.array(lprior) * (alpha1 - 1))
# j1 = max(_cjs_dist(np.array(mu), np.exp(np.array(lw1))),
#         _cjs_dist(-np.array(mu), np.exp(np.array(lw1))))


# alpha2 = 0.99
# lw2, k2 = az.psislw(np.array(lprior) * (alpha2 - 1))
# j2 = max(_cjs_dist(np.array(mu), np.exp(np.array(lw2))),
#         _cjs_dist(-np.array(mu), np.exp(np.array(lw2))))

# print("{0:.13f}".format(j1))
# print("{0:.13f}".format(j2))

# print("{0:.13f}".format(k1))
# print("{0:.13f}".format(k2))

# diag = (j1 + j2) / (2 * np.log2(1 + 0.01))

# print("{0:.13f}".format(diag))
