#! /usr/bin/env python3.6
from pylab import *
from netCDF4 import Dataset
from snapy.harp.utils import get_ray_out

def optical_depth(case, band = '', ang = None):
  datafile = '%s-main.nc' % case
  data = Dataset(datafile, 'r')
  pres = data['press'][0,:,0,0]/1.E5 # pa -> bar
  dlnp = log(pres[0]) - log(pres[1])
  dlnp = log(pres[1]) - log(pres[2])
  x1f = data['x1f'][:]

  inpfile = '%s.inp' % case
  amu, aphi = get_ray_out(inpfile, band)
  btau = data['%stau' % band][0,:,0,0]

  tau = cumsum(btau[::-1])[::-1]
  return pres, tau

def plot_optical_depth(ax, case, ang = None):
  pres, wfunc1 = optical_depth(case, 'b1', ang)
  pres, wfunc2 = optical_depth(case, 'b2', ang)
  pres, wfunc3 = optical_depth(case, 'b3', ang)
  pres, wfunc4 = optical_depth(case, 'b4', ang)
  pres, wfunc5 = optical_depth(case, 'b5', ang)
  pres, wfunc6 = optical_depth(case, 'b6', ang)

  ax.plot(wfunc1, pres, label = 'S band')
  ax.plot(wfunc2, pres, label = 'C band')
  ax.plot(wfunc3, pres, label = 'X band')
  ax.plot(wfunc4, pres, label = 'U band')
  ax.plot(wfunc5, pres, label = 'K band')
  ax.plot(wfunc6, pres, label = 'Q band')
  ax.legend(fancybox=True, framealpha=0.5)

  ax.set_ylim([50., 0.5])
  ax.set_xlim([0, 10.])
  ax.set_yscale('log')
  ax.set_xlabel('optical depth', fontsize = 12)
  ax.set_ylabel('Pressure (bar)', fontsize = 12)

if __name__ == '__main__':
  case = 'build/saturn_vla_inversion_wfunc'
  #case = '../build_disk/saturn_vla-disk-1.6'
  figure(1, figsize = (8, 8))
  ax = axes()
  plot_optical_depth(ax, case, 48.2)
  #show()
  savefig('figs/optical_depth.png', bbox_inches = 'tight')
