import re
from numpy import logspace, log10

def create_inputs_ideal(tmpfile, args):
    with open(tmpfile, 'r') as file:
      tmpinp = file.read()

    pmax, pmin, np = tuple(map(float, args['plevel'].split(':')))
    np = int(np)
    plevel = logspace(log10(pmax), log10(pmin), np)
    plevel = ['%10.2f'%x for x in plevel]

    if args['tem'] == '0':
        Tp = ['0.']*np
    else:
        Tp = args['tem'].split(' ')
    assert(len(Tp) == np)

    if args['nh3'] == '0':
        NH3p  = ['0.']*np
    else:
        NH3p = args['nh3'].split(' ')
    assert(len(NH3p) == np)

    var = [x for x in args['var']]

    name = tmpfile.split('.')[0]
    if args['output'] != '':
        name += '-' + args['output']

    inpfile = re.sub('\[problem_id\]', name, tmpinp)
    inpfile = re.sub('\[logname\]', name, inpfile)
    inpfile = re.sub('\[obsname\]', args['obs'], inpfile)
    inpfile = re.sub('\[T0\]', args['T0'], inpfile)
    inpfile = re.sub('\[Tmin\]', args['Tmin'], inpfile)
    inpfile = re.sub('\[qH2O\]', args['qH2O'], inpfile)
    inpfile = re.sub('\[qNH3\]', args['qNH3'], inpfile)
    inpfile = re.sub('\[Tstd\]', args['sT'], inpfile)
    inpfile = re.sub('\[Xstd\]', args['sNH3'], inpfile)
    inpfile = re.sub('\[Tlen\]', args['zT'], inpfile)
    inpfile = re.sub('\[Xlen\]', args['zNH3'], inpfile)
    inpfile = re.sub('\[plevel\]', ' '.join(plevel), inpfile)
    inpfile = re.sub('\[pmin\]', args['pmin'], inpfile)
    inpfile = re.sub('\[pmax\]', args['pmax'], inpfile)
    inpfile = re.sub('\[nwalker\]', args['nwalker'], inpfile)
    inpfile = re.sub('\[nlim\]', args['nlim'], inpfile)
    inpfile = re.sub('\[variables\]', ' '.join(var), inpfile)
    inpfile = re.sub('\[nodes\]', str(4*int(args['nodes'])), inpfile)
    inpfile = re.sub('\[Tp\]', ' '.join(Tp), inpfile)
    inpfile = re.sub('\[NH3p\]', ' '.join(NH3p), inpfile)
    inpfile = re.sub('\[grav\]', '-' + args['grav'], inpfile)
    inpfile = re.sub('\[lat\]', args['lat'], inpfile)
    inpfile = re.sub('\[rgradt\]', args['rgradt'], inpfile)
    inpfile = re.sub('\[metallicity\]', args['metallicity'], inpfile)
    inpfile = re.sub('\[karpowicz_scale\]', args['karpowicz_scale'], inpfile)
    inpfile = re.sub('\[hanley_power\]', args['hanley_power'], inpfile)
    if args['d']:
        inpfile = re.sub('\[diff\]', 'true', inpfile)
    else:
        inpfile = re.sub('\[diff\]', 'false', inpfile)

    with open(name + '.inp', 'w') as file:
        file.write(inpfile)
    print('Input file written to %s.inp\n' % name)
    return name + '.inp'

