

def shellHeader():
    return """#!/bin/sh 

    """

def shellCommand(address):
    return """vclient -c getVito%s""" % address

def shellFooter():
    return """
"""

def createShell(fromAddress, toAddress):
    start = int(fromAddress, 16)
    end = int(toAddress, 16)

    print(shellHeader())

    for idx in range(start, end+1):
        print(shellCommand("%04X" % idx))

    print(shellFooter())

if __name__ == "__main__":

    createShell("2000", "4000")
