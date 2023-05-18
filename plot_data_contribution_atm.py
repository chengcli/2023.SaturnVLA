#! /usr/bin/env python3
from pylab import *
from netCDF4 import Dataset
from build.contribution_function import plot_contribution_function
from radio.saturn_radio_data import plot_saturn_radio_data
from profiles import plot_vapor_profile, plot_temp_profile

fig, axs = subplots(1, 3, figsize = (16, 6))
#subplots_adjust(hspace = 0.08, wspace = 0.08)

plot_saturn_radio_data(axs[0])
#case = 'build/saturn_vla_inversion--9.8'
case = 'build/saturn_vla_inversion_wfunc'
plot_contribution_function(axs[1], case, 48.2)

ax = axs[1].twiny()
ncdata = Dataset('build_disk/saturn_vla-disk-1.6-main.nc')
ncdata2 = Dataset('build/saturn_vla_inversion_wfunc-main.nc')
plot_temp_profile(ax, ncdata)
ax.set_xlim([100., 500.])
ax.set_xlabel('Temperature (K)')

ax = axs[2]
#plot_vapor_profile(ax, ncdata, 'vapor1', 'C6')
plot_vapor_profile(ax, ncdata2, 'vapor1', 'C6')
plot_vapor_profile(ax, ncdata, 'vapor2', 'C7')
ax.legend(['H$_2$O', 'NH$_3$'], fontsize = 12)
ax.set_ylim([50., 0.5])
ax.set_xlim([1.E-8, 2.E2])
ax.set_xlabel('Vapor mixing ratio (g/kg)', fontsize = 12)
ax.set_ylabel('Pressure (bar)', fontsize = 12)

#show()
savefig('figs/data_contribution_atm_v2.png', bbox_inches = 'tight')
