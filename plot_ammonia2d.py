#! /usr/bin/env python3.6
#from plot_mcmc_profile import *
from matplotlib.gridspec import GridSpec
from pylab import *
from netCDF4 import Dataset
from snapy.planet_gravity import graphic2centric, centric2graphic
import os

# saturn zonal wind
data = genfromtxt('u_vs_lat.saturn.Voyager.III', skip_header = 7)
pglat = data[:,0]
uwind = data[:,1]


# history of storms
# 1876, 1903, 1933, 1960, 1990
latmin = array([5, 34, -1, 57, 11, 38])
latmax = array([11, 38, 5, 59, 13, 41])
latmid = (latmin + latmax)/2.
latmid = hstack([latmid, [centric2graphic(38, 60.2/54.3)]])

fname = './data/saturn_vla_inversion-digest5.nc'
data = Dataset(fname, 'r')
pres = data['pres'][:]/1.E5
nx1 = len(pres)
lat = data['lat'][:]
nlat = len(lat)
freq = data['frequency'][:]
nfreq = len(freq)

#lnp = data['lnp'][:,0]
nh3 = data['nh3_avg'][:]*1.E3/2.7*350.
temp = data['temp_avg'][:]
#tempa = temp - data['temp_ad'][:].reshape((nx1,1))
theta0 = 169.
theta = temp/data['temp_ad'][:].reshape((nx1,1))*theta0
nh3_base = data['nh3_base'][:]*1.E3/2.7*350.
nh3_base = nh3_base.reshape((nh3.shape[0],1))

X, Y = meshgrid(lat, pres)

figure(1, figsize = (12,6))
ax = axes()

# ammonia map
h = ax.contourf(X, Y, nh3 - nh3_base, linspace(-225., 225., 10), extend = 'both', cmap = 'RdBu_r')
#h = ax.contourf(X, Y, nh3, 24, extend = 'min')
c = colorbar(h, orientation = 'horizontal', fraction = 0.04, pad = 0.04)
#c = colorbar(h, cax = axs[0,1])
c.ax.set_xlabel('NH$_3$ concentration anomaly (ppmv)', fontsize = 12)
ax.set_ylim([50., 1.0])
ax.set_ylabel('Pressure (bar)', fontsize = 12)
ax.set_yscale('log')
#ax.set_xlim([-10., 85.])
ax.set_xlim([0., 85.])
ax.set_xlabel('Planetographic latitude (degree)', fontsize = 12)
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')

# previous storms
#for i in range(len(latmin)):
#  ax.plot([latmin[i], latmin[i]], [40., 1.5], color = '0.7', linestyle = '--')
#  ax.plot([latmax[i], latmax[i]], [40., 1.5], color = '0.7', linestyle = '-')
  #ax.fill_betweenx([40., 1.5], [latmin[i], latmin[i]], [latmax[i], latmax[i]],
  #  color = '0.7', alpha = 0.5)

for i in range(len(latmid)):
  ax.plot([latmid[i], latmid[i]], [40., 1.5], color = '0.7', linestyle = '--')

# zonal wind
ax2 = ax.twinx()
ax2.plot(pglat, -uwind, color = 'C2')
ax2.plot([0., 85.], [0., 0.], '--', color = 'C2', linewidth = 2)
ax2.set_ylim([-1000., 50.])
ax2.set_yticks([0., -100., -200., -300., -400., -500., -600.])
ax2.set_yticklabels([0, 100, 200, 300, 400, 500, 600])
ax2.set_ylabel('zonal wind (m/s)', fontsize = 15)

#show()
savefig('figs/ammonia_map2d_v7.png', bbox_inches = 'tight', dpi = 400)

