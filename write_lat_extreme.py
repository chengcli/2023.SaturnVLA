#! /usr/bin/env python3
from pylab import *
from scipy.interpolate import interp1d

bands = ['s', 'c', 'x', 'u', 'k', 'q']

with open('data/vla_lat_extreme.txt', 'w') as file:
  pass

# loop over band
band_grid = []
for b in bands:
  data = genfromtxt('data/vla_saturn_%s_deconv.txt' % b)
  latg = data[:,0]
  iy = latg > -10.
  latg = latg[iy]
  tb = data[iy,1]
  tbx = tb[1:] - tb[:-1]
  sgn = sign(tbx[1:]*tbx[:-1])

  ix = arange(1,len(latg)-1)[sgn < 0.]
  ix = hstack((0, ix, len(latg)-1))
  with open('data/vla_lat_extreme.txt', 'a') as file:
    file.write('# %s band latitudes (graphic):\n' % b)
    for i in range(len(ix)):
      file.write('%8.1f' % latg[ix[i]])
    file.write('\n')
    band_grid.append(list(latg[ix]))

count = []
for i in range(len(bands)):
  count.append(list(zeros(len(band_grid[i]), dtype = int)))
  for j in range(len(band_grid[i])):
    for k in range(len(bands)):
      for l in range(len(band_grid[k])):
        if abs(band_grid[i][j] - band_grid[k][l]) < 1.:
          count[i][j] += 1

lat_grid = []
for it in range(100):
  for i in range(len(bands)):
    j = argmax(count[i])
    if count[i][j] == -1:
      continue
    lat_grid.append(band_grid[i][j])
    count[i][j] = -1
  lat_grid = list(sort(unique(lat_grid)))
  for i in range(len(lat_grid)):
    j = i + 1
    while j < len(lat_grid):
      if abs(lat_grid[j] - lat_grid[i]) < 1.0:
        lat_grid.pop(j)
        continue
      j += 1
print(lat_grid)

# write consolidate data
with open('data/vla_lat_extreme.txt', 'a') as file:
  mytb = zeros((len(lat_grid), len(bands)))
  mystb = zeros((len(lat_grid), len(bands)))
  mymu = zeros((len(lat_grid), len(bands)))
  mysmu = zeros((len(lat_grid), len(bands)))

  for i,lat in enumerate(lat_grid):
    for j,b in enumerate(bands):
      data = genfromtxt('data/vla_saturn_%s_deconv.txt' % b)
      latg = data[:,0]
      tb = data[:,1] - mean(data[:,1])
      stb = data[:,2]
      mu = data[:,3]
      smu = data[:,4]

      tbfunc = interp1d(latg, tb, fill_value = 0., bounds_error = False)
      stbfunc = interp1d(latg, stb, fill_value = 'extrapolate')
      mufunc = interp1d(latg, mu, fill_value = 'extrapolate')
      smufunc = interp1d(latg, smu, fill_value = 'extrapolate')

      mytb[i,j] = tbfunc(lat)
      mystb[i,j] = stbfunc(lat)
      mymu[i,j] = mufunc(lat)
      mysmu[i,j] = mufunc(lat)

  file.write('# consolidate tb anomaly\n')

  file.write('# TB: LATG  S   C   X   U   K   Q\n')
  for i,lat in enumerate(lat_grid):
    file.write('%12.3f' % lat)
    for j,b in enumerate(bands):
      file.write('%12.3f' % mytb[i,j])
    file.write('\n')

  file.write('# STB: LATG  S   C   X   U   K   Q\n')
  for i,lat in enumerate(lat_grid):
    file.write('%12.3f' % lat)
    for j,b in enumerate(bands):
      file.write('%12.3f' % mystb[i,j])
    file.write('\n')

  file.write('# MU: LATG  S   C   X   U   K   Q\n')
  for i,lat in enumerate(lat_grid):
    file.write('%12.3f' % lat)
    for j,b in enumerate(bands):
      file.write('%12.3f' % mymu[i,j])
    file.write('\n')

  file.write('# MU: LATG  S   C   X   U   K   Q\n')
  for i,lat in enumerate(lat_grid):
    file.write('%12.3f' % lat)
    for j,b in enumerate(bands):
      file.write('%12.3f' % mysmu[i,j])
    file.write('\n')
