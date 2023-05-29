#! /usr/bin/env python3
from pylab import *

#bands = ['s', 'c', 'x', 'u', 'k', 'q']
#bands = ['q','k','u','x','c','s']
bands = ['q','k','u','x','c','s']
nbands = len(bands)

fig, axs = subplots(3, 2, figsize = (12, 4), sharex = True)
#subplots_adjust(hspace = 0.12, wspace = 0.12)
subplots_adjust(hspace = 0.12)

for i in range(nbands):
  ax = axs[i%3,i//3]
  if bands[i] == 's':
    row = 0
    ax.set_ylim([-25,30])
  elif bands[i] == 'c':
    row = 1
    ax.set_ylim([-20,25])
  elif bands[i] == 'x':
    row = 2
    ax.set_ylim([-5,20])
  elif bands[i] == 'u':
    row = 4
    ax.set_ylim([-10,15])
  elif bands[i] == 'k':
    row = 6
    ax.set_ylim([-5,10])
  elif bands[i] == 'q':
    row = 7
    ax.set_ylim([-10,10])
  else :
    pass
  data = genfromtxt('./data/vla_saturn_%s.txt' % bands[i])
  lat1 = data[:,0]
  lat2 = data[:,1]
  tb_avg = data[:,2]
  tb_std = data[:,3]
  mu = data[:,4]
  #ax.errorbar((lat1+lat2)/2., tb_avg, yerr = tb_std,
  ax.errorbar(lat2, tb_avg, yerr = tb_std,
    fmt = '.', color = '0.7', alpha = 0.5)
  ax.step(lat2, tb_avg, 'C1', where = 'post', label = '%s band' % bands[i].upper())
  #ax.step(lat1, tb_avg, 'C0', where = 'post', label = '%s band disk' % bands[i].upper())
  ax.set_xlim([0., 90.])
  ax.set_ylabel("T'$_b$ (K)", fontsize = 14)
  if i == 5 or i == 2:
    ax.set_xlabel('Planetographic Latitude (degree)', fontsize = 14)
  ax.legend(loc = 4, frameon = False)

savefig('./figs/saturn_tb_latitude_v2.png', bbox_inches = 'tight', dpi = 400)
