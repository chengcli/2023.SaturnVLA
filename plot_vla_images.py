#! /usr/bin/env python3
import argparse
from common import read_info, regrid
from astropy.io import fits
from matplotlib.patches import Ellipse
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pylab import *

parser = argparse.ArgumentParser()
parser.add_argument('--out',
    help = 'output name'
    )
parser.add_argument('--info',
    help = 'info file'
    )
parser.add_argument('--band',
    help = 'VLA band'
    )
parser.add_argument('--fits',
    help = 'fits file'
    )
parser.add_argument('--data',
    help = 'data file'
    )
parser.add_argument('--disk',
    default = 'none',
    help = 'id in limb disk file if provided'
    )
parser.add_argument('--dv',
    default = 'none',
    help = 'difference from maximum tb'
    )
parser.add_argument('--scale',
    default = '8',
    help = 'pixel scale'
    )
parser.add_argument('--bmajor',
    help = 'beam major in degrees'
    )
parser.add_argument('--bminor',
    help = 'beam minor in degrees'
    )
parser.add_argument('--bpa',
    help = 'beam polar angle in degrees'
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

print('Processing %s' % args['data'])
#fname = 'sat-u-ictb'
#args['info'] = 'data/%s.info' % fname
#args['fits'] = 'Saturn_2015/fits_smeared/150528/sat-c-ictb.fits'
#args['fits'] = 'Saturn_2015/fits_smeared/150528/%s.fits' % fname
#args['data'] = 'data/%s.dat' % fname

info = read_info(args['info'])
hdu = fits.open(args['fits'])[0]
data = hdu.data[0,0,:,:]
nx, ny = data.shape

xcenter = info['xcenter']
ycenter = info['ycenter']
re = info['re']
rp = info['rp']
phi = info['phi']
scale = info['scale1']*info['scale2']
pix = info['scale1']


x1 = int(xcenter - 2*re)
x2 = int(xcenter + 2*re)
y1 = int(ycenter - 2*rp)
y2 = int(ycenter + 2*rp)

#print(x1, x2)
#print(y1, y2)
#print(xcenter, ycenter, phi)

x1 = min(max(0, x1), nx - 1)
x2 = min(max(0, x2), nx - 1)
y1 = min(max(0, y1), ny - 1)
y2 = min(max(0, y2), ny - 1)

dist = float(info['dist'])
#bmajor  = deg2rad(4.6E-4) # major in degrees
bmajor  = deg2rad(float(args['bmajor']))
#bminor  = deg2rad(1.7E-4) # minor in degrees
bminor  = deg2rad(float(args['bminor']))
#bpa     = deg2rad(-69.4)  # position angle to north
bpa     = deg2rad(float(args['bpa']))
#dist   = 8.8*1.5E8       # range to saturn in km
print(pix)

#fig, axs = subplots(1, 3, figsize = (20, 4),
#  gridspec_kw={'width_ratios':[1,3,1]})

fig = figure(figsize = (20, 4))
gs = fig.add_gridspec(2, 3, width_ratios = (1,3,1), height_ratios = (20,1))
subplots_adjust(wspace = 0.08)

# disk image
ax = fig.add_subplot(gs[0,0])
#ax = axs[0]
ax.pcolormesh(data[x1:x2,y1:y2], cmap = 'Greys_r')
#ax.imshow(data, origin = 'lower', cmap = 'Greys_r')
ellipse = Ellipse((ycenter - y1, xcenter - x1), width = re*2, height = rp*2, angle = phi,
  fill = False, color = 'C1', ls = '-', lw = 2)
ax.add_patch(ellipse)

# beam pattern
#print(dist*tan(bminor)/pix, dist*tan(bmajor)/pix, bpa)
#print(re, rp)
ellipse2 = Ellipse((ycenter - y1 - re*1.4, xcenter - x1 - rp*1.8),
                   width = 2*dist*tan(bmajor)/pix,
                   height = 2*dist*tan(bminor)/pix, angle = bpa,
                   fill = True, color = 'C1', ls = '-', lw = 2)
ax.add_patch(ellipse2)
ax.set_aspect('equal')
ax.axis('off')

# cylindrical projection
#ax = axs[1]
ax = fig.add_subplot(gs[0,1])
ax.tick_params(axis='both', which='major', labelsize=15)
data = genfromtxt(args['data'])
lat = data[:,1]
lon = data[:,3]
mu = data[:,4]
tb = data[:,5]

# remove a limb-darkened disk
if args['disk'] != 'none':
  coeff = genfromtxt('limb_disk.txt', delimiter = ',')
  coeff = coeff[int(args['disk']),1:-1]
  tb_disk = (coeff[0]*pow(mu, coeff[1]) + coeff[5]*pow(mu, coeff[6]))/2.
  tb -= tb_disk

ix = where((lat < 80.) & (lat > 10.))[0]
vmax = tb[ix].max()
if args['dv'] != 'none':
  vmin = vmax - float(args['dv'])
else:
  vmin = tb[ix].min()

# projection area
ydis1 = lat2ydis(lat + 1., re*pix, rp*pix)
ydis2 = lat2ydis(lat - 1., re*pix, rp*pix)
dydis = ydis1 - ydis2

sa = scale/(dydis*dydis)*float(args['scale'])
iy = argsort(sa)[::-1]

#h1 = ax.pcolormesh(lon1[::4], lat1[::4], tb[::4,::4].T, cmap = 'gist_heat')
h1 = ax.scatter(lon[iy], lat[iy], c = tb[iy],
  s = sa[iy], cmap = 'Greys_r', vmin = vmin, vmax = vmax)
#ax.scatter([0.], [0.], c = 'g', s = 10)
ax.set_facecolor('k')
ax.grid('on')
ax.set_xlim([360., 0.])

# add colorbar
ax = fig.add_subplot(gs[1,1])
ax.tick_params(axis='both', which='major', labelsize=15)
colorbar(h1, cax = ax, orientation = 'horizontal')#, label = "%s band Tb' (K)" % args['band'])
ax.grid('on')

# polar projection
colat = 90. - lat
ix = where(colat < 40.)[0]
#tb = tanh(tb/2.)
#vmin, vmax = -1., 1.
vmax = tb[ix].max()
if args['dv'] != 'none':
  vmin = vmax - float(args['dv'])
else:
  vmin = tb[ix].min()
ax = fig.add_subplot(gs[0,2], projection = 'polar')
ax.tick_params(axis='both', which='major', labelsize=15)
h2 = ax.scatter(lon[iy]/180.*pi, colat[iy], c = tb[iy],
  s = sa[iy], cmap = 'Greys_r', vmin = vmin, vmax = vmax)
ax.set_ylim([0., 40.])
ax.set_yticks([20., 40.])
ax.set_yticklabels([70., 50.], color = 'w')
ax.set_facecolor('k')
#ax.yaxis.set_visible(False)

#divider = make_axes_locatable(ax)
# color bar
ax = fig.add_subplot(gs[1,2])
ax.tick_params(axis='both', which='major', labelsize=15)
colorbar(h2, cax = ax, orientation = 'horizontal')#, label = "Tb' (K)")
ax.grid('on')

savefig('./figs/%s-full.png' % args['out'], bbox_inches = 'tight')

#ax.set_ylim([0, 800])

#show()
