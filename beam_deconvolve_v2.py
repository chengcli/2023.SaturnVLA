#! /usr/bin/env python3.6
import argparse
from bisect import bisect
from common import read_info
from pylab import *
from scipy.special import erf
from scipy.interpolate import interp1d

parser = argparse.ArgumentParser()

parser.add_argument('--bmajor',
    help = 'beam major in degrees'
    )
parser.add_argument('--bminor',
    help = 'beam minor in degrees'
    )
parser.add_argument('--bpa',
    help = 'beam polar angle in degrees'
    )
parser.add_argument('--band',
    help = 'band code'
    )
parser.add_argument('--info',
    help = 'information file'
    )
parser.add_argument('--l2',
    default = '1.E-4',
    help = 'regularization strength'
    )
args = vars(parser.parse_args())

def deg2rad(ang):
  return ang*pi/180.

def rad2deg(rad):
  return rad*180./pi

def graphic2centric(lat, rerp):
  if abs(lat) == 90.:
    return lat
  else:
    return rad2deg(arctan(tan(deg2rad(lat))/rerp**2))

def lat2ydis(glat, re, rp):
  try:
    clat = deg2rad(array(list(map(lambda x: graphic2centric(x, re/rp), glat))))
  except TypeError:
    clat = deg2rad(graphic2centric(glat, re/rp))
  rdis = sqrt((re*cos(clat))**2 + (rp*sin(clat))**2)
  ydis = rdis*sin(clat)
  return ydis

def gaussian(x, mu, sigma):
  return 1./(sigma*sqrt(2.*pi))*exp(-(x - mu)*(x - mu)/(2.*sigma*sigma))

def fgaussian(p, s):
  return exp(-s*s*p*p/2.)

#fname = 'vla_saturn_c'

# C band data
#bmajor  = deg2rad(4.6E-4) # major in degrees
bmajor  = deg2rad(float(args['bmajor']))
#bminor  = deg2rad(1.7E-4) # minor in degrees
bminor  = deg2rad(float(args['bminor']))
#bpa     = deg2rad(-69.4)  # position angle to north
bpa     = deg2rad(float(args['bpa']))
#dist   = 8.8*1.5E8       # range to saturn in km 

info = read_info('./data/%s' % args['info'])

dist    = float(info['dist'])
#re      = 39.79           # equatorial radius in px
re      = float(info['re'])
#rp      = 36.53           # polar radius in px
rp      = float(info['rp'])
#pix     = 1497.96         # pixel scale in km
pix     = float(info['scale1'])
#beam    = 1.*4.84814e-6   # radian

# beam FWHM
sbeam = dist*(bmajor*(sin(bpa))**2 + bminor*(cos(bpa)**2))
print('beam resolution = ', sbeam, ' km')

# read tb data
data = genfromtxt('./data/vla_saturn_%s.txt' % args['band'])
lat1, lat2, tb, stb, mu, smu, nn = data[:,0], data[:,1], data[:,2], data[:,3], data[:,4], data[:,5], data[:,6]
latm = (lat1 + lat2)/2.
ydis = lat2ydis(lat1, re*pix, rp*pix)
mu_func = interp1d(ydis, mu, fill_value = 'extrapolate')
glat_func = interp1d(ydis, lat1, fill_value = 'extrapolate')

latmin, latmax = -40., 90.
ymin = lat2ydis(latmin, re*pix, rp*pix)
ymax = lat2ydis(latmax, re*pix, rp*pix)
num_grids = int(4*(ymax - ymin)/sbeam) + 1

ygrid = linspace(ymin, ymax, num_grids, endpoint = False)
dy = ygrid[1] - ygrid[0]
# shift grid by half
ygrid += dy/2.

ylat = glat_func(ygrid)
ytb = array([tb[bisect(lat1, ylat[i])-1] for i in range(len(ylat))])
ystb = array([stb[bisect(lat1, ylat[i])-1] for i in range(len(ylat))])

npad, num_iter = 2, 1000
fsig = zeros((num_iter, npad*num_grids), dtype = complex)
sig = zeros((num_iter, npad*num_grids), dtype = complex)

obs_true = ytb.copy()
fobs_true = fft(obs_true, npad*num_grids)*dy
freq = fftfreq(npad*num_grids, dy)
#print(fobs_true)
#print(dy*dy)

for i in range(num_iter):
  obs = obs_true  #+ (rand(num_grids) - 0.5)
  fobs = fft(obs, npad*num_grids)*dy

  # deconvolution
  fg = fgaussian(2.*pi*freq, sbeam/2.355)
  fsig[i,:]= fobs*fg/(fg*fg + freq*freq*dy*dy*float(args['l2']))
  #fsig[i,:]= fobs*fg/(fg*fg + 1.E-1)
  sig[i,:] = ifft(fsig[i,:]/dy, npad*num_grids)

fsig_avg = mean(fsig, axis = 0)
sig_avg = mean(real(sig), axis = 0)
sig_std = std(real(sig), axis = 0)

# reconvolved data
sig_conv = ifft(fft(sig_avg, npad*num_grids) \
  *fgaussian(2.*pi*freq, sbeam/2.355))

# plot results
#fig, axs = subplots(2, 1, figsize = (12,8))
figure(1, figsize = (16,3))
ax = axes()
ax.tick_params(axis='both', which='major', labelsize=15)

# observation
#ax.step(ydis, tb, 'C0')
tmid = mean(tb[lat1 > 0.])
ax.step(ylat, ytb - ystb - tmid, 'k--', where = 'mid')
ax.step(ylat, ytb + ystb - tmid, 'k--', where = 'mid')
ax.fill_between(ylat, ytb - ystb - tmid, ytb + ystb - tmid,
  step = 'mid', hatch = '/', alpha = 0.5, facecolor = 'none', edgecolor = 'k')

# de-convolved result with error
ax.errorbar(ylat, sig_avg[:num_grids] - tmid,
  yerr = sig_std[:num_grids], color = 'C3', capsize = 5, label = 'obs-deconv')

# re-convolved observations
ax.plot(ylat, sig_conv[:num_grids] - tmid, '-', color = 'C2', label = 'obs-reconv')


#ax.plot(ygrid, result, marker = '+', color = 'C3', ms = 15, linewidth = 2)
ax.set_ylabel("%s band T$_b$ (K) anomaly" % args['band'].upper(), fontsize = 14)
ax.set_xlabel('planetographic latitude (degree)', fontsize = 14)
ax.set_xlim([0., 90.])

# annotations
ax.plot([0., 90.], [0., 0.], 'k--', alpha = 0.5)
if args['band'] == 's':
  ax.plot([0., sbeam/5.8E4/pi*180.], [-10, -10], linewidth = 10, color = 'C1')
  ax.set_ylim([-12., 14.])
elif args['band'] == 'c':
  ax.plot([0., sbeam/5.8E4/pi*180.], [-13, -13], linewidth = 10, color = 'C1')
  ax.set_ylim([-15., 15.])
elif args['band'] == 'x' or args['band'] == 'u':
  ax.plot([0., sbeam/5.8E4/pi*180.], [-8, -8], linewidth = 10, color = 'C1')
  ax.set_ylim([-10., 16.])
elif args['band'] == 'k':
  ax.plot([0., sbeam/5.8E4/pi*180.], [-2, -2], linewidth = 10, color = 'C1')
  ax.set_ylim([-3., 5.])
elif args['band'] == 'q':
  ax.plot([0., sbeam/5.8E4/pi*180.], [-4, -4], linewidth = 10, color = 'C1')
  ax.set_ylim([-6., 7.])

#show()
savefig('figs/saturn_deconv_%s_v2.png' % args['band'], bbox_inches = 'tight')
