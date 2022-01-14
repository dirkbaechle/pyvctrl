import sys

def vitoXmlHeader():
    return """<vito>
	<devices>
		<device ID="20CB" name="Vito200" protocol="P300" />
	</devices>

	<commands>"""

def vitoXmlCommand(address):
    return """		<command name='getVito%s' protocmd='getaddr'>
			<addr>%s</addr>
			<len>1</len>
			<unit>ST</unit>
			<description>Address %s</description>
		</command>""" % (address, address, address)

def vitoXmlFooter():
    return """	</commands>
</vito>
"""

def createVitoXml(fromAddress, toAddress):
    """ Writes a vito.xml to stdout, starting
        and stopping at the given addresses.
    """
    start = int(fromAddress, 16)
    end = int(toAddress, 16)

    print(vitoXmlHeader())

    for idx in range(start, end+1):
        print(vitoXmlCommand("%04X" % idx))

    print(vitoXmlFooter())

def createVitoXmlFromFile(fpath):
    """ Expects a file with one address per line,
        as created by "filter_vclient_log -a".
    """
    addresses = []
    with open(fpath, "r") as fin:
        for line in fin.readlines():
            line = line.rstrip('\n')
            line = line.rstrip()
            # Skip comments
            if line.startswith('#'):
                continue
            # Make addresses unique
            if line and line not in addresses:
                addresses.append(line)

    print(vitoXmlHeader())

    for addr in addresses:
        print(vitoXmlCommand(addr))

    print(vitoXmlFooter())


def usage():
    print("create_vito v1.0, Dirk Baechle, 2022-01-09")
    print("Usage: create_vito.py [-d] [filename]")

def main():
    default = False
    fpath = None

    for arg in sys.argv[1:]:
        if arg in ['-d', '--default', '--default-values']:
            default = True
        else:
            fpath = arg

    if len(sys.argv) < 2:
        usage()
        sys.exit(0)

    if default:
        createVitoXml("2000", "4000")
    else:
        createVitoXmlFromFile(fpath)


if __name__ == "__main__":
    main()
