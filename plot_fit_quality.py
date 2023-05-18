#! /usr/bin/env python3.6
from pylab import *
from netCDF4 import Dataset

fname = 'data/saturn_vla_inversion-digest5.nc'
data = Dataset(fname, 'r')
pres = data['pres'][:]/1.E5
nx1 = len(pres)
lat = data['lat'][:]
nlat = len(lat)
freq = data['frequency'][:]
nfreq = len(freq)

band = ['S', 'C', 'X', 'U', 'K', 'Q']

tb_base = data['tb_base'][:]
tb_ad = data['tb_ad'][:]
tb = data['tb'][:]
zonal_tb_avg = data['zonal_tb_avg'][:]
zonal_tb_std = data['zonal_tb_std'][:]

print(zonal_tb_avg.shape)
print(tb_base.shape)
print(tb_ad.shape)

nburn = 500

#print(zonal_tb_avg)
#print(mean(tb[:,:,nburn:,:], axis = (2,3)) - tb_base[:,:])

#exit()


fig, axs = subplots(len(freq), 1, figsize = (12, 12), sharex = True)

for i in range(len(freq)):
  ax = axs[len(freq) - i - 1]
  ax.errorbar(lat, zonal_tb_avg[i,:], yerr = zonal_tb_std[i,:],
    capsize = 5)
  ax.plot(lat, mean(tb[i,:,nburn:,:], axis = (1,2)) - tb_base[i,:], color = 'C1')
  ax.set_ylabel("%s (K)" % band[i], fontsize = 12)

axs[5].set_xlabel('Planetographic latitude (degree)', fontsize = 12)
axs[2].set_xlim([0., 85.])

#show()

savefig('figs/fit_anomaly_v6.png', bbox_inches = 'tight')
