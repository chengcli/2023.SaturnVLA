#! /usr/bin/env python3
from netCDF4 import Dataset
from .athinput import athinput
from numpy import zeros
import re

def write_radio_obs(inpfile, datafile):
#inpfile = 'vla_ideal_js.inp'
    inp = athinput(inpfile)

# count number of bands
    num_bands = 0
    for key in inp['radiation'].keys():
        if re.match('b[0-9]+$', key):
            num_bands += 1

# read frequency
    freq = []
    for i in range(num_bands):
        freq.append(float(inp['radiation']['b%d' % (i+1)].split()[0]))

# count out direction
    outdir = inp['radiation']['outdir'].split(' ')
    num_dirs = len(outdir)
    amu, aphi = [], []
    for i in range(num_dirs):
        m = re.search('\((.*),(.*)\)', outdir[i])
        if m.group(1) != '':
            amu.append(float(m.group(1)))
        else:
            amu.append(0.)
        if m.group(2) != '':
            aphi.append(float(m.group(2)))
        else:
            aphi.append(0.)

# read radiation toa
#datafile = 'vla_ideal_js-main.nc'
    data = Dataset(datafile, 'r')
    tb = zeros((4, num_bands, num_dirs))
    for i in range(num_bands):
        for j in range(num_dirs):
            tb[0,i,j] = data['b%dtoa%d' % (i+1,j+1)][0,0,0]
            tb[1,i,j] = data['b%dtoa%d' % (i+1,j+1)][0,1,0]
            tb[2,i,j] = data['b%dtoa%d' % (i+1,j+1)][0,2,0]
            tb[3,i,j] = data['b%dtoa%d' % (i+1,j+1)][0,3,0]

# write to file
    outfile = '.'.join(inpfile.split('.')[:-1]) + '.out'
    with open(outfile, 'w') as file:
        file.write('# Brightness temperatures of input model %s - model 0\n' % inpfile)
        file.write('%12s' % '# Freq (GHz)')
        for i in range(num_dirs):
            file.write('%10.1f' % amu[i])
        file.write('\n')
        for i in range(num_bands):
            file.write('%12.1f' % freq[i])
            for j in range(num_dirs):
                file.write('%10.2f' % tb[0,i,j])
            file.write('\n')

        file.write('# Brightness temperatures of input model %s - model 1\n' % inpfile)
        file.write('%12s' % '# Freq (GHz)')
        for i in range(num_dirs):
            file.write('%10.1f' % amu[i])
        file.write('\n')
        for i in range(num_bands):
            file.write('%12.1f' % freq[i])
            for j in range(num_dirs):
                file.write('%10.2f' % tb[1,i,j])
            file.write('\n')

        file.write('# Brightness temperatures of input model %s - model 2\n' % inpfile)
        file.write('%12s' % '# Freq (GHz)')
        for i in range(num_dirs):
            file.write('%10.1f' % amu[i])
        file.write('\n')
        for i in range(num_bands):
            file.write('%12.1f' % freq[i])
            for j in range(num_dirs):
                file.write('%10.2f' % tb[2,i,j])
            file.write('\n')

        file.write('# Brightness temperatures of input model %s - model 3\n' % inpfile)
        file.write('%12s' % '# Freq (GHz)')
        for i in range(num_dirs):
            file.write('%10.1f' % amu[i])
        file.write('\n')
        for i in range(num_bands):
            file.write('%12.1f' % freq[i])
            for j in range(num_dirs):
                file.write('%10.2f' % tb[3,i,j])
            file.write('\n')
    print('Brightness temperatures written to %s' % outfile)
    return outfile
