def athinput(filename):
    """Read athinput file and returns a dictionary of dictionaries."""

    # Read data
    with open(filename, 'r') as athinput:
        # remove comments, extra whitespace, and empty lines
        lines = filter(None, [i.split('#')[0].strip() for i in athinput.readlines()])
    data = {}
    # split into blocks, first element will be empty
    blocks = ('\n'.join(lines)).split('<')[1:]

    # Function for interpreting strings numerically
    def typecast(x):
        if '_' in x:
            return x
        try:
            return int(x)
        except ValueError:
            pass
        try:
            return float(x)
        except ValueError:
            pass
        try:
            return complex(x)
        except ValueError:
            pass
        return x

    # Function for parsing assignment based on first '='
    def parse_line(line):
        out = [i.strip() for i in line.split('=')]
        out[1] = '='.join(out[1:])
        out[1] = typecast(out[1])
        return out[:2]

    # Assign values into dictionaries
    for block in blocks:
        info = list(filter(None, block.split('\n')))
        key = info.pop(0)[:-1]  # last character is '>'
        data[key] = dict(map(parse_line, info))
    return data
