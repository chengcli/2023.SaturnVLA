#! /usr/bin/env python3.6
from pylab import *
from netCDF4 import Dataset

def find_closest(arr, x):
  return abs(arr - x).argmin()

fname = './data/saturn_vla_inversion-digest5.nc'
data = Dataset(fname, 'r')
pres = data['pres'][:]/1.E5
nx1 = len(pres)
lat = data['lat'][:]
nlat = len(lat)
freq = data['frequency'][:]
nfreq = len(freq)

nh3 = data['nh3_avg'][:]*1.E3/2.7*350.
nh3_std = data['nh3_std'][:]*1.E3/2.7*350.
nh3_base = data['nh3_base'][:]*1.E3/2.7*350.
nh3_base = nh3_base.reshape((nh3.shape[0],1))


fig, axs = subplots(2, 1, figsize = (12, 6),
  gridspec_kw = {'height_ratios':[1,4]})
ax = axs[0]
ax.plot([0., 85.], [0, 0.], 'k--', alpha = 0.5, linewidth = 2)

ipres1 = find_closest(pres, 3.)
ax.plot(lat, nh3[ipres1,:] - nh3_base[ipres1,0], 'C1-', linewidth = 2)

ipres2 = find_closest(pres, 15.)
ax.plot(lat, nh3[ipres2,:] - nh3_base[ipres2,0], 'C2-', linewidth = 2)

ax.plot([4.7, 4.7], [-200, 200], color = '0.7', alpha = 0.5, linewidth = 4)
ax.plot([20, 20], [-200, 200], color = '0.7', alpha = 0.5, linewidth = 4)
ax.plot([38, 38], [-200, 200], color = '0.7', alpha = 0.5, linewidth = 4)
ax.plot([60, 60], [-200, 200], color = '0.7', alpha = 0.5, linewidth = 4)

ax.set_xlabel('Planetographic latitude (degree)')
ax.set_xlim([0., 85.])
ax.set_ylabel("NH$_3$' (ppmv)")

#figure(1, figsize = (12,6))
#ax = axes()
ax = axs[1]

# ammonia profiles
print(nh3.shape)
ilat = find_closest(lat, 4.7)

#print(nh3_base.shape)
#print(pres.shape)
#print(nh3[:,ilat].shape)
#print(nh3_base[:,0].shape)

#ax.plot([-250, 1800], [pres[ipres1], pres[ipres1]], 'C1-', linewidth = 2)
#ax.plot([-250, 1800], [pres[ipres2], pres[ipres2]], 'C2-', linewidth = 2)
ax.plot(nh3[:,ilat] - nh3_base[:,0], pres, 'k-', linewidth = 2)
ax.fill_betweenx(pres, 
  nh3[:,ilat] - nh3_base[:,0] - nh3_std[:,ilat],
  nh3[:,ilat] - nh3_base[:,0] + nh3_std[:,ilat],
  alpha = 0.5, color = '0.7'
  )
ax.plot(nh3[ipres1,ilat] - nh3_base[ipres1,0], pres[ipres1], 'o',
  color = 'C1', ms = 10)
ax.plot(nh3[ipres2,ilat] - nh3_base[ipres2,0], pres[ipres2], 'o',
  color = 'C2', ms = 10)
#print(linspace(-200., 200., 9))
xticks = list(linspace(-150., 150., 4))
xticklabels = list(map(int, linspace(-150, 150, 4)))
ax.plot([0., 0.], [30., 1.], 'C0--', linewidth = 2)

ilat = find_closest(lat, 20.)

ax.plot(nh3[:,ilat] - nh3_base[:,0] + 500., pres, 'k-', linewidth = 2)
ax.fill_betweenx(pres, 
  nh3[:,ilat] - nh3_base[:,0] - nh3_std[:,ilat] + 500.,
  nh3[:,ilat] - nh3_base[:,0] + nh3_std[:,ilat] + 500.,
  alpha = 0.5, color = '0.7'
  )
ax.plot(nh3[ipres1,ilat] - nh3_base[ipres1,0] + 500, pres[ipres1], 'o',
  color = 'C1', ms = 10)
ax.plot(nh3[ipres2,ilat] - nh3_base[ipres2,0] + 500, pres[ipres2], 'o',
  color = 'C2', ms = 10)
ax.plot([500., 500.], [30., 1.], 'C0--', linewidth = 2)
xticks.extend(linspace(350., 650., 4))
xticklabels.extend(map(int, linspace(-150., 150., 4)))

ilat = find_closest(lat, 38.)

ax.plot(nh3[:,ilat] - nh3_base[:,0] + 1000., pres, 'k-', linewidth = 2)
ax.fill_betweenx(pres, 
  nh3[:,ilat] - nh3_base[:,0] - nh3_std[:,ilat] + 1000.,
  nh3[:,ilat] - nh3_base[:,0] + nh3_std[:,ilat] + 1000.,
  alpha = 0.5, color = '0.7'
  )
ax.plot(nh3[ipres1,ilat] - nh3_base[ipres1,0] + 1000, pres[ipres1], 'o',
  color = 'C1', ms = 10)
ax.plot(nh3[ipres2,ilat] - nh3_base[ipres2,0] + 1000, pres[ipres2], 'o',
  color = 'C2', ms = 10)
ax.plot([1000., 1000.], [30., 1.], 'C0--', linewidth = 2)
xticks.extend(linspace(850., 1150., 4))
xticklabels.extend(map(int, linspace(-150., 150., 4)))

ilat = find_closest(lat, 60.)

ax.plot(nh3[:,ilat] - nh3_base[:,0] + 1500., pres, 'k-', linewidth = 2)
ax.fill_betweenx(pres, 
  nh3[:,ilat] - nh3_base[:,0] - nh3_std[:,ilat] + 1500.,
  nh3[:,ilat] - nh3_base[:,0] + nh3_std[:,ilat] + 1500.,
  alpha = 0.5, color = '0.7'
  )
ax.plot(nh3[ipres1,ilat] - nh3_base[ipres1,0] + 1500, pres[ipres1], 'o',
  color = 'C1', ms = 10)
ax.plot(nh3[ipres2,ilat] - nh3_base[ipres2,0] + 1500, pres[ipres2], 'o',
  color = 'C2', ms = 10)
ax.plot([1500., 1500.], [30., 1.], 'C0--', linewidth = 2)
xticks.extend(linspace(1350., 1650., 4))
xticklabels.extend(map(int, linspace(-150., 150., 4)))

ax.set_xticks(xticks)
ax.set_xticklabels(xticklabels)
ax.set_ylim([30., 1.0])
ax.set_ylabel('Pressure (bar)', fontsize = 12)
ax.set_xlabel('NH$_3$ concentration anomaly (ppmv)', fontsize = 12)
ax.set_yscale('log')
ax.set_yticks([1., 2., 4., 10., 20., 30.])
ax.set_xlim([-250., 1800.])
#ax.set_yticklabels([1., 2., 4., 10., 20., 40.])

#show()
savefig('figs/ammonia_profiles.png', bbox_inches = 'tight')

#h = ax.contourf(X, Y, nh3 - nh3_base, linspace(-225., 225., 10), extend = 'both', cmap = 'RdBu_r')
