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
        # Simplify string to one space only between tokens
        m = ' '.join(m.split())
        # Is this line supposed to be a key or a value?
        if mode == MKEY:
            # A key
            key = m.rstrip(':')
        else:
            # A value
            if '.' in m:
                # Seems to be an int/float value, so get rid of the
                # appended unit in the string
                sl = m.split()
                if len(sl) == 2:
                    value = sl[0]
                else:
                    value = m

                # Also reduce trailing zeros
                while value.endswith('00'):
                    value = value[:-1]
            else:
                value = m
            data[key] = value

        # Toggle parsing mode
        mode = 1 - mode

    return data

def hasServerError(msg, errmsg):
    """ Return 'True' if one of the given response messages from the
        vclient contains a 'SRV ERR:' (server error).
    """

    if not msg or 'SRV ERR:' in msg.decode():
        return True

    if errmsg and 'SRV ERR:' in errmsg.decode():
        return True

    return False

def listOfGetCommands(glist):
    """ Returns a list of vclient command line options,
        readily compiled for the readVclientData method.
    """
    clist = []
    clist.append('-c')
    clist.append(','.join(glist))

    return clist

def readVclientData(rdata):
    """ Returns a dict of data for the given list
        of vclient get commands.
    """

    stdout, stderr = cmd.Cmd(['vclient'] + listOfGetCommands(rdata))

    if hasServerError(stdout, stderr):
        return {}

    return parseVclientOutput(stdout.decode())

def listOfSetCommands(sdict):
    """ Returns a list of vclient command line options,
        readily compiled for the setVclientData method.
    """
    clist = []
    cmds = []
    for key, value in sdict.iteritems():
        cmds.append("%s %s" % (key, value))

    clist.append('-c')
    clist.append('"%s"' % ','.join(cmds))

    return clist

def setVclientData(sdata):
    """ Sends vclient set commands, based on the given dict
        of data (key/value pairs).
    """
    stdout, stderr = cmd.Cmd(['vclient'] + listOfSetCommands(sdata))

    if hasServerError(stdout, stderr):
        return False

    return True

def vt(rtsoll, at, atged, neigung, niveau):
    """ Return the VLsoll temp, computed by method 1.
    """
    return neigung * 1.8317984 * (rtsoll - (atged*0.7 + at*0.3))**0.8281902 + niveau + rtsoll

def vt2(rtsoll, at, atged, neigung, niveau):
    """ Return the VLsoll temp, computed by method 2.
    """
    mixedat = (atged*0.7 + at*0.3)
    dar = mixedat - rtsoll
    return niveau + rtsoll - neigung * dar * (1.4347 + 0.021 * dar + 247.9 * 10**-6 * dar * dar)

if __name__ == "__main__":
    print(listOfGetCommands(['getVitoFlammenStatus']))
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
