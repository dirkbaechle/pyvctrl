# -*- coding: utf-8 -*-
import pyvctrl.cmd as cmd

MVOID = 0
MKEY = 1
MVALUE = 2

def reduceFloatValue(m):
    """ Seems to be an int/float value, so get rid of the
        appended unit in the string.
    """
    sl = m.split()
    if len(sl) == 2:
        value = sl[0]
    else:
        value = m

    # Also reduce trailing zeros
    while value.endswith('00'):
        value = value[:-1]

    return value

def parseOutputWithoutErrors(ml):
    """ Parses the given vclient output, while assuming that no
        errors occured. This means that this function assumes that
        there will only be key and value lines, and that on each
        key line a value will follow.
    """
    data = {}
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
                value = reduceFloatValue(m)
            else:
                value = m
            data[key] = value

        # Toggle parsing mode
        mode = 1 - mode

    return data


def parseOutputForAllowedKeys(ml, allowed_keys=None):
    """ Parses the given vclient output, while accepting only
        known (or allowed) keys.
        Also handles void states, where line occur that are neither
        a key nor a value.
    """
    data = {}
    # When explicit keys are defined, start in void mode
    mode = MVOID
    key = None
    value = None

    for m in ml:
        # Simplify string to one space only between tokens
        m = ' '.join(m.split())

        # Intelligent comparing against the allowed keys
        ckey = m.rstrip(':')
        is_allowed = ckey in allowed_keys
        # Is this line supposed to be a key or a value?
        if mode == MVOID:
            # Might be a key
            if is_allowed:
                mode = MVALUE
                key = ckey
        elif mode == MKEY:
            # A key
            if not is_allowed:
                mode = MVOID
            else:
                mode = MVALUE
                key = ckey
        else:
            # Might be another key
            if not m.endswith(':') and not is_allowed:
                # A value
                if '.' in m:
                    value = reduceFloatValue(m)
                else:
                    value = m
                data[key] = value
                mode = MKEY
            else:
                # We seem to have encountered a key,
                # check whether it's allowed...
                if not is_allowed:
                    mode = MVOID
                else:
                    mode = MVALUE
                    key = ckey

    return data


def parseVclientOutput(msg, allowed_keys=None):
    """ Parses the given stdout message from vclient and returns
        a dict with the key/value pairs of the result.
        Assumes that hasServeError was called before and no
        read error has occured.
    """
    ml = msg.split('\n')

    if allowed_keys is None:
        return parseOutputWithoutErrors(ml)
    else:
        return parseOutputForAllowedKeys(ml, allowed_keys)

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

def readVclientData(rdata, allowed_keys=None):
    """ Returns a dict of data for the given list
        of vclient get commands.
    """

    stdout, stderr = cmd.Cmd(['vclient'] + listOfGetCommands(rdata))

    if hasServerError(stdout, stderr):
        return {}

    return parseVclientOutput(stdout.decode(), allowed_keys)

def listOfSetCommands(sdict):
    """ Returns a list of vclient command line options,
        readily compiled for the setVclientData method.
    """
    clist = []
    cmds = []
    for key, value in sdict.items():
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
