from pangloss import BackgroundCatalog, ForegroundCatalog, \
    TrueHaloMassDistribution, Kappamap, Shearmap

from pandas import DataFrame

# initialize background and foreground
B = BackgroundCatalog(N=100.0, domain=[1.43, 1.4, -1.43, -1.4], field=[0, 0, 0, 0])
F = ForegroundCatalog.guo()
F.set_mass_prior(TrueHaloMassDistribution()) # This needs explaining...

B.drill_lightcones(radius=2, foreground=F)
B.lens_by_halos(lookup_table=True, smooth_corr=True)

K = Kappamap.example()
S = Shearmap.example()

B.lens_by_map(K, S)

# run monte carlo samples
output = DataFrame()
for _ in range(100):
    print _
    F.draw_halo_masses()
    B.drill_lightcones(radius=2.0, foreground=F, smooth_corr=True)
    B.lens_by_halos(lookup_table=True, smooth_corr=True)
    halos = B.get_sampled_halo_masses_in_lightcones()
    B.add_noise()
    halos['log-likelihood'] = B.halo_mass_log_likelihood()
    output = output.append(halos, ignore_index=True)

# galaxies that were filtered due to relevance should be assigned mass of -1
output = output.fillna(-1)
print output
output.to_csv('data3.csv')
B.get_true_halo_masses_in_lightcones().to_csv('true3.csv')