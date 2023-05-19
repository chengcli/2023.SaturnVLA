#! /usr/bin/env python3

def plot_vapor_profile(ax, ncdata, name, color = 'C0'):
  vapor = ncdata[name][0,:,0,0]*1.E3 # kg/kg -> g/kg
  print(vapor)
  pres = ncdata['press'][0,:,0,0]/1.E5  # pa -> bar
  ax.plot(vapor, pres, linewidth = 2, color = color)
  ax.set_yscale('log')
  ax.set_xscale('log')

def plot_temp_profile(ax, ncdata, color = 'k'):
  temp = ncdata['temp'][0,:,0,0]
  pres = ncdata['press'][0,:,0,0]/1.E5  # pa -> bar
  ax.plot(temp, pres, linewidth = 2, color = color, alpha = 0.5)
  ax.set_yscale('log')
