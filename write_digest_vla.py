#! /usr/bin/env python3
import argparse
from pylab import *
from netCDF4 import Dataset
from snapy.harp.utils import athinput, get_rt_bands, get_inversion_variables
from astropy.io import fits
from glob import glob
from scipy.interpolate import interp1d

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dir',
  help = 'directory of the simulation to combine'
  )
parser.add_argument('-c', '--case',
  help = 'case base name'
  )
args = vars(parser.parse_args())

fnames = glob('%s/%s-*-main.nc' % (args['dir'], args['case']))
fdigest = '%s-digest5.nc' % args['case']

lats, lats_name = [], []
for fname in fnames:
  m = re.search('%s/%s-(.+)-main.nc' % (args['dir'], args['case']), fname)
  lats.append(float(m.group(1)))
  lats_name.append(m.group(1))
lats, lats_name = array(lats), array(lats_name)
ix = argsort(lats)
lats = lats[ix]
lats_name = lats_name[ix]

# get longest time
steps = []
for j,lat in enumerate(lats):
  fname = '%s/%s-%s-main.nc' % (args['dir'], args['case'], lats_name[j])
  data = Dataset(fname, 'r')
  steps.append(len(data['time']))

# define axis
inpfile = '%s.inp' % fnames[0][:-8]
rt_bands = get_rt_bands(inpfile)
nfreq = len(rt_bands)

# get inversion variables
ivars = get_inversion_variables(inpfile, "profile")
jlast = len(ivars)

data = Dataset(fnames[0], 'r')
nstep = max(steps)
nwalker = len(data['x3'][:])
pres = data['press'][0,:,0,0]
ibot = 0
while pres[ibot] > 300.E5: ibot += 1
x1 = data['x1'][:]
nlevel = len(x1) - ibot
nlat = len(lats)

# profile inversion
hdul = fits.open('%s-profile.fits' % fnames[0][:-8])
npar = hdul[0].data.shape[-1]

# define digest dimensions

digest = Dataset(fdigest, 'w', format = 'NETCDF4')
digest.createDimension('x1', nlevel)
digest.createDimension('lat', nlat)
digest.createDimension('frequency', 6)
digest.createDimension('ray', 9)
digest.createDimension('step', nstep)
digest.createDimension('walker', nwalker)
digest.createDimension('par', npar)

# axis variables
x1_ = digest.createVariable('x1', 'f4', ('x1',))
x1_.units = 'm'
x1_.axis = 'Z'
x1_.long_name = 'log pressure height'
x1_[:] = x1[ibot:]

lat_ = digest.createVariable('lat', 'f4', ('lat',))
lat_.units = 'degree'
lat_.axis = 'Y'
lat_.long_name = 'planetocentric latitude'

pres_ = digest.createVariable('pres', 'f4', ('x1',))
pres_.units = 'pa'
pres_.long_name = 'pressure'
pres_[:] = pres[ibot:]

mu_ = digest.createVariable('mu', 'f4', ('ray',))
mu_.units = '1'
mu_.long_name = 'cosine emission angle'
mu_[:] = cos(linspace(0., 80., 9)/180.*pi)

frequency_ = digest.createVariable('frequency', 'f4', ('frequency',))
frequency_.units = 'GHz'
frequency_.long_name = 'frequency'
frequency_[:] = rt_bands[:,0]

step_ = digest.createVariable('step', 'i4', ('step',))
step_.units = '1'
step_.long_name = 'mcmc steps'
step_[:] = range(nstep)

walker_ = digest.createVariable('walker', 'f4', ('walker',))
walker_.units = '1'
walker_.long_name = 'mcmc walkers'
walker_[:] = range(nwalker)

par_ = digest.createVariable('par', 'f4', ('par',))
par_.units = 'N/A'
par_.long_name = 'sampling parameters'
par_[:] = range(npar)

step_lat_ = digest.createVariable('steplat', 'f4', ('lat'))
step_lat_.units = '1'
step_lat_.long_name = 'mcmc steps of each latitude'
step_lat_[:] = steps

zonal_tb_avg = digest.createVariable('zonal_tb_avg', 'f4', ('frequency','lat'))
zonal_tb_avg.units = 'K'
zonal_tb_avg.long_name = 'zonal mean nadir brightness temperature anomaly'

zonal_tb_std = digest.createVariable('zonal_tb_std', 'f4', ('frequency','lat'))
zonal_tb_std.units = 'K'
zonal_tb_std.long_name = 'zonal mean nadir brightness temperature standard deviation'

# fit results
# base and adaibatic profiles
temp_base = digest.createVariable('temp_base', 'f4', ('x1',))
temp_base.units = 'K'
temp_base.long_name = 'temperature of the baseline model'
temp_base[:] = data['temp'][0,ibot:,0,0]

nh3_base = digest.createVariable('nh3_base', 'f4', ('x1',))
nh3_base.units = 'kg/kg'
nh3_base.long_name = 'ammonia mass mixing ratio of the baseline model'
nh3_base[:] = data['vapor2'][0,ibot:,0,0]

temp_ad = digest.createVariable('temp_ad', 'f4', ('x1',))
temp_ad.units = 'K'
temp_ad.long_name = 'temperature of the adiabatic model'
temp_ad[:] = data['temp'][0,ibot:,0,0]

nh3_ad = digest.createVariable('nh3_ad', 'f4', ('x1',))
nh3_ad.units = 'kg/kg'
nh3_ad.long_name = 'ammonia mass mixing ratio of the adiabatic model'
nh3_ad[:] = data['vapor2'][0,ibot:,0,0]

# retrieved profiles
temp_avg = digest.createVariable('temp_avg', 'f4', ('x1','lat'))
temp_avg.units = 'K'
temp_avg.long_name = 'mean temperature'

temp_std = digest.createVariable('temp_std', 'f4', ('x1','lat'))
temp_std.units = 'K'
temp_std.long_name = 'temperature standard deviation'

nh3_avg = digest.createVariable('nh3_avg', 'f4', ('x1','lat'))
nh3_avg.units = 'kg/kg'
nh3_avg.long_name = 'mean ammonia mass mixing ratio'

nh3_std = digest.createVariable('nh3_std', 'f4', ('x1','lat'))
nh3_std.units = 'kg/kg'
nh3_std.long_name = 'ammonia mass mixing ratio standard deviation'

h2o_avg = digest.createVariable('h2o_avg', 'f4', ('x1','lat'))
h2o_avg.units = 'kg/kg'
h2o_avg.long_name = 'mean water mass mixing ratio'

# simulated tb and ld
tb_base = digest.createVariable('tb_base', 'f4', ('frequency', 'lat'))
tb_base.units = 'K'
tb_base.long_name = 'baseline nadir brightness temperature'

tb_ad = digest.createVariable('tb_ad', 'f4', ('frequency', 'lat'))
tb_ad.units = 'K'
tb_ad.long_name = 'adiabatic nadir brightness temperature'

tb = digest.createVariable('tb', 'f4', ('frequency','lat','step','walker'))
tb.units = 'K'
tb.long_name = 'nadir brightness temperature'

ld = digest.createVariable('ld', 'f4', ('frequency','lat','step','walker'))
ld.units = '%'
ld.long_name = 'limb darkening at 45 degree emssion angle'

# goodness of fit measured by lnp and chi2

lnp = digest.createVariable('lnp', 'f4', ('lat','step','walker'))
lnp.units = '1'
lnp.long_name = 'log posterior probability'

#chi2 = digest.createVariable('chi2', 'f4', ('lat','step','walker'))
#chi2.units = '1'
#chi2.long_name = 'differential chi2'

# sampling parameters
pos = digest.createVariable('pos', 'f4', ('lat','step','walker','par'))
pos.units = 'N/A'
pos.long_name = 'sampling positions'

data.close()

for j,lat in enumerate(lats):
  fname = '%s/%s-%s-main.nc' % (args['dir'], args['case'], lats_name[j])
  print('Processing %s ...' % fname, flush = True)
  data = Dataset(fname, 'r')
  nburn = len(data['time'])//2

  obsfile = athinput('%s.inp' % fname[:-8])['inversion']['obsfile']
  obs_target = genfromtxt('%s/%s' % (args['dir'], obsfile), skip_header = 2, max_rows = 6)
  obs_icov = diag(genfromtxt('%s/%s' % (args['dir'], obsfile), skip_header = 8))
  tb1 = obs_target[:]
  tb1_std = 1./sqrt(obs_icov[:])

  zonal_tb_avg[:,j] = tb1
  zonal_tb_std[:,j] = tb1_std

  tb_base[:,j] = data['radiance'][0,:,jlast,0]
  tb_ad[:,j] = data['radiance'][0,:,0,0]

  lat_[j] = lat
  # retrieved profiles
  temp = data['temp'][nburn:,ibot:,jlast,:]
  temp_avg[:,j] = mean(temp, axis = (0,2))
  temp_std[:,j] = std(temp, axis = (0,2))

  nh3 = data['vapor2'][nburn:,ibot:,jlast,:]
  nh3_avg[:,j] = mean(nh3, axis = (0,2))
  nh3_std[:,j] = std(nh3, axis = (0,2))

  h2o = data['vapor1'][nburn:,ibot:,jlast,:]
  h2o_avg[:,j] = mean(h2o, axis = (0,2))

  # simulated tb and ld
  radiance = data['radiance'][:,:,jlast,:]
  print(radiance.shape)
  print(tb.shape)
  for i in range(nfreq):
    # brightness temperature
    tb[i,j,:steps[j],:] = radiance[:,i,:]

  # log posterior probability
  hdul = fits.open('%s-profile.fits' % fname[:-8])
  lnp[j,:steps[j]-1,:] = hdul[2].data

  # chi2
  #chi2[j,:,:] = 0.
  #istep, iwalker = unravel_index(argmax(lnp[j]), lnp[j].shape)
  #for i in range(nfreq):
    #print(mean(tb[i,j,istep,iwalker]) - tb_base[i], tb0[i], tb1[i], tb1_std[i])
    #print(mean(ld[i,j,nburn:,:]) - ld_base[i], ld0[i], ld1[i], ld1_std[i])
    #chi2[j,:,:] += pow((tb[i,j,:,:] - tb_base[i] - tb1[i])/tb1_std[i], 2) \
    #  + pow((ld[i,j,:,:] - ld_base[i] - ld1[i])/ld1_std[i], 2)
    #print((tb[i,j,:,:] - tb_base[i] - tb1[i]), tb1_std[i])
    #print((ld[i,j,:,:] - ld_base[i] - ld1[i]), ld1_std[i])
  #exit()

  # position
  pos[j,:steps[j]-1,:,:] = hdul[0].data

  #istep, iwalker = unravel_index(argmax(hdul[2].data), hdul[2].shape)
  #tb_best[:,j,0] = radiance[istep,::4,iwalker]
  #ld_best[:,j,0] = (tb_best[:,j,0] - radiance[istep,3::4,iwalker])/tb_best[:,j,0]*100.

  data.close()

digest.close()
