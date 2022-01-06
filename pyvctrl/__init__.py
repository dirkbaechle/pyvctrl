# -*- coding: utf-8 -*-
import pyvctrl.cmd as cmd

MKEY = 0
MVALUE = 1

def parseVclientOutput(msg):
    """ Parses the given stdout message from vclient and returns
        a dict with the key/value pairs of the result.
        Assumes that hasServeError was called before and no
        read error has occured.
    """
    data = {}

    ml = msg.split('\n')

    mode = MKEY
    key = None
    value = None

    for m in ml:
        m = ' '.join(m.split())
        if mode == MKEY:
            key = m.rstrip(':')
        else:
            if '.' in m:
                # Seems to be an int/float value, so get rid of the
                # appended unit in the string
                sl = m.split()
                if len(sl) == 2:
                    value = sl[0]
                else:
                    value = m
            else:
                value = m
            data[key] = value

        # Toggle parsing mode
        mode = 1 - mode

    return data

def hasServerError(msg):
    """ Return 'True' if the given response message from the
        vclient contains a '' (server error).
    """

    if 'SRV ERR:' in msg:
        return True

    return False

def listOfGetCommands(glist):
    """ Returns a list of vclient command line options,
        readily compiled for the readVclientData method.
    """
    clist = []
    for g in glist:
        clist.append('-c')
        clist.append(g)

    return clist

def readVclientData(rdata):
    """ Returns a dict of data for the given list
        of vclient get commands.
    """

    stdout = cmd.stdoutCmd(['vclient'] + listOfGetCommands(rdata))

    if hasServerError(stdout):
        return {}

    return parseVclientOutput(stdout)

def listOfSetCommands(sdict):
    """ Returns a list of vclient command line options,
        readily compiled for the setVclientData method.
    """
    clist = []
    for key, value in sdict.iteritems():
        clist.append('-c')
        clist.append(key)
        clist.append('"%s"' % value)

    return clist

def setVclientData(sdata):

    stdout = cmd.stdoutCmd(['vclient'] + listOfSetCommands(sdata))

    if hasServerError(stdout):
        return False

    return True


if __name__ == "__main__":
    print(listOfGetCommands(['getNiveau', 'getNeigung']))
    print(listOfSetCommands({'setNiveau': '30.0', 'setNeigung': '2.0'}))
    msg = """getVitoBetriebsart:
Dauernd Normalbetrieb
getVitoBetriebParty:
aus
getVitoTempPartySoll:
20.000000 °C
getVitoBetriebSpar:
aus
getVitoTempRaumNorSoll:
23.000000 °C
getVitoTempRaumRedSoll:
3.000000 °C
getVitoTempAussen:
7.800000 °C
getVitoTempKesselIst:
63.500000 °C
getVitoTempKesselSoll:
74.300003 °C
getVitoStatusFlamme:
aus
getVitoLaufzeitBrenner:
13926.977539 Stunden
getVitoStartsBrenner:
252701.000000 
getVitoKennlinieNeigung:
2.000000 
getVitoBetriebsartHK:
?
getVitoTempVLSoll:
0.000000 °C
getVitoTempRLIst:
55.099998 °C
getVitoStatusPumpeHK:
aus
getVitoTempRaumHK:
20.000000 °C
getVitoStatusPumpeZirku:
aus
getVitoAnlagenschema:
3.000000 
"""
    print(parseVclientOutput(msg))
