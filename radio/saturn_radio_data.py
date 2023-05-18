#! /usr/bin/env python3
from pylab import *
import os

dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'

def plot_saturn_radio_data(ax):
# old vla
  data = genfromtxt(dir_path + 'saturn.tab', comments = '!')
  wave = data[:,0]
  tb = data[:,1]
  tb_err = data[:,2]

  ax.errorbar(wave, tb, yerr = tb_err, label = 'Older VLA data',
    color = 'C0', fmt = 'o', mfc = 'none', capsize = 5)

# zz data
  data = genfromtxt(dir_path + 'saturn.tabZZ.dat')
  freq = data[:,0]  # GHz
  tb =  data[:,5]
  tb_err = data[:,6]

  ax.errorbar(30./freq, tb, yerr = tb_err, label = 'Current VLA data',
    color = 'C1', fmt = 'o', mfc = 'none', capsize = 5)

# old saturn
  data = genfromtxt(dir_path + 'saturn.tbv', comments = '!')
  wave = data[:,0] # cm
  tb = data[:,2]
  tb_err = data[:,3]

  ax.errorbar(wave, tb, yerr = tb_err,
    color = 'C0', fmt = 'o', mfc = 'none', capsize = 5)

# planck data
  data = genfromtxt(dir_path + 'planck_saturn.dat')
  freq = data[:,0] # GHz
  tb = data[:,2]
  tb_err = data[:,3]

  ax.errorbar(30./freq, tb, yerr = tb_err, label = 'Planck',
    color = 'C4', fmt = 'o', capsize = 5)

# bima03
  data = genfromtxt(dir_path + 'saturn.bima03')
  wave = data[:,0] # cm
  tb = data[:,1]
  tb_err = data[:,2]

  ax.errorbar(wave, tb, yerr = tb_err, label = 'BIMA03',
    color = 'C4', fmt = 'o', capsize = 5)

# wmap
  data = genfromtxt(dir_path + 'wmap_saturn.dat')
  freq = data[:,0] # GHz
  tb = data[:,5]
  tb_err = data[:,6]

  ax.errorbar(30./freq, tb, yerr = tb_err, label = 'WMAP',
    color = 'C5', fmt = 'o', capsize = 5)

# GMRT
  data = genfromtxt(dir_path + 'saturn_GMRT.tab')
  wave = data[:,0]  # cm
  tb = data[:,1]
  tb_err = data[:,2]

  ax.errorbar(wave, tb, yerr = tb_err, label = 'GMRT',
    color = 'C6', fmt = 'o', capsize = 5)

# disk model
  data = genfromtxt(dir_path + 'b1.radiance.00000.txt')
  freq = data[:,0] # GHz
  tb = data[:,2]
  ax.plot(30./freq, tb, label = 'disk-model, 200 ppm NH$_3$', color = 'k', linewidth = 2)

  data = genfromtxt(dir_path + 'b2.radiance.00000.txt')
  freq = data[:,0] # GHz
  tb = data[:,2]
  ax.plot(30./freq, tb, color = 'k', linewidth = 2)

  ax.set_xscale('log')
  ax.set_xticks([0.01, 0.05, 0.1, 0.5, 1., 5, 10., 50., 100.])
  ax.set_xlabel('Wavelength (cm)', fontsize = 12)
  ax.set_ylabel('Brightness temperature (K)', fontsize = 12)
  ax.legend(fontsize = 12)
  ax.set_ylim([100., 620.])
  ax.set_xlim([1.E-2, 150.])

if __name__ == '__main__':
  figure(1, figsize = (8, 8))
  ax = axes()

  #show()
  savefig('saturn_radio_data.png', bbox_inches = 'tight')
