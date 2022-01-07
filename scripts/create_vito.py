

def vitoXmlHeader():
    return """<vito>
	<devices>
		<device ID="209C" name="Vito200" protocol="P300" />
	</devices>

	<commands>

    """

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
    start = int(fromAddress, 16)
    end = int(toAddress, 16)

    print(vitoXmlHeader())

    for idx in range(start, end+1):
        print(vitoXmlCommand("%04X" % idx))

    print(vitoXmlFooter())

if __name__ == "__main__":

    createVitoXml("2000", "4000")
