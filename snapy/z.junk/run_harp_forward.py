import subprocess
from athinput import athinput

def run_harp_forward(exefile, inpfile):
    script = ['./' + exefile, '-i', inpfile]
    process = subprocess.Popen(script,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.decode('UTF-8'), end = '')
    process.poll()
    #print(out.decode('UTF-8'), end = '\r')
    #print(err.decode('UTF-8'))

    out, err = subprocess.Popen('./combine.py',
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE).communicate()
    print(out.decode('UTF-8'), end = '')
    print(err.decode('UTF-8'), end = '')

    inp = athinput(inpfile)
    return inp['job']['problem_id']
