#! /usr/bin/env python3.6
from pylab import *
from netCDF4 import Dataset
from snapy.harp.utils import get_ray_out

def contribution_function(case, band = '', ang = None):
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
  if ang != None:
    mu = cos(ang/180.*pi)
  else:
    mu = cos(amu/180.*pi)
  wfunc = 1./mu*exp(-tau/mu)*btau/dlnp
  wfunc /= wfunc.max()
  return pres, wfunc

def plot_contribution_function(ax, case, ang = None):
  pres, wfunc1 = contribution_function(case, 'b1', ang)
  pres, wfunc2 = contribution_function(case, 'b2', ang)
  pres, wfunc3 = contribution_function(case, 'b3', ang)
  pres, wfunc4 = contribution_function(case, 'b4', ang)
  pres, wfunc5 = contribution_function(case, 'b5', ang)
  pres, wfunc6 = contribution_function(case, 'b6', ang)

  ax.plot(wfunc1, pres, label = 'S band')
  ax.plot(wfunc2, pres, label = 'C band')
  ax.plot(wfunc3, pres, label = 'X band')
  ax.plot(wfunc4, pres, label = 'U band')
  ax.plot(wfunc5, pres, label = 'K band')
  ax.plot(wfunc6, pres, label = 'Q band')
  ax.legend()

  ax.set_ylim([50., 0.5])
  ax.set_yscale('log')
  ax.set_xlabel('contribution function', fontsize = 12)
  ax.set_ylabel('Pressure (bar)', fontsize = 12)

if __name__ == '__main__':
  case = 'saturn_vla_inversion--9.8'
  #case = '../build_disk/saturn_vla-disk-1.6'
  figure(1, figsize = (8, 8))
  ax = axes()
  plot_contribution_function(ax, case, 48.2)
  show()
  #savefig('../figs/contribution_function.png', bbox_inches = 'tight')
