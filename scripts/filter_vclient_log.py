import sys

# Filter for outputting the log directly
FMLOG = 0
# Filter for only listing the valid addresses
FMADDRESS = 1
# Filter for listing key and value, with the latter in hex
FMHEX = 2

# Parser in void mode
PMVOID = 0
# Parser in key mode
PMKEY = 1
# Parser in error mode
PMERROR = 2

def outputLog(key, value):
    print(key)
    print(value)

def outputAddress(key, value):
    key = key.lstrip("getVito")
    key = key.rstrip(':')
    print(key)

def outputHex(key, value):
    print(key)
    try:
        # Split off remaining floating-point parts
        if '.' in value:
            pidx = value.find('.')
            value = value[:pidx]
        elif ',' in value:
            pidx = value.find(',')
            value = value[:pidx]
        if value.startswith('-'):
            # Convert to unsigned char
            hval = "%02X" % (int(value)+2**8)
        else:
            hval = "%02X" % int(value)
    except:
        hval = "??"
    print(hval)

output = {FMLOG : outputLog,
          FMADDRESS : outputAddress,
          FMHEX : outputHex}

def parseFile(fpath, outmode):
    pmode = PMVOID
    ckey = None
    with open(fpath, "r") as fin:
        for line in fin.readlines():
            line = line.rstrip('\n')
            line = line.rstrip()
            if 'SRV ERR:' in line or 'rror' in line:
                pmode = PMERROR
            else:
                if pmode == PMERROR:
                    # Simply skip the key line
                    pmode = PMVOID
                elif pmode == PMVOID:
                    if line:
                        # Accept line as key if it's not empty
                        ckey = line
                        pmode = PMKEY
                elif pmode == PMKEY:
                    if line:
                        # Accept next line as value if it's not empty
                        if '.' in line or ',' in line:
                            # Also reduce trailing zeros
                            while line.endswith("00"):
                                line = line[:-1]

                        output[outmode](ckey, line)
                        pmode = PMVOID


def usage():
    print("filter_vclient_log v1.0, Dirk Baechle, 2022-01-09")
    print("Usage: filter_vclient_log [-l] [-a] [-h] <logfile>")

def main():
    outmode = FMLOG
    fpath = None

    for arg in sys.argv[1:]:
        if arg in ['-l', '--log', '--log-mode']:
            outmode = FMLOG
        elif arg in ['-a', '--address', '--address-mode']:
            outmode = FMADDRESS
        elif arg in ['-h', '--hexlog', '--hexlog-mode']:
            outmode = FMHEX
        else:
            fpath = arg

    if len(sys.argv) < 2 or not fpath:
        usage()
        sys.exit(0)

    parseFile(fpath, outmode)


if __name__ == "__main__":
    main()
