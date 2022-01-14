import subprocess

def stdoutCmd(cmdlist, suppress_stderr=False):
    """ Call given command with the added arguments, if any and return stdout. """
    if suppress_stderr:
        process = subprocess.Popen(cmdlist, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen(cmdlist, shell=False, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    return stdout

def stderrCmd(cmdlist):
    """ Call given command with the added arguments, if any and return stderr. """
    process = subprocess.Popen(cmdlist, shell=False, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    return stderr

def Cmd(cmdlist):
    """ Call given command with the added arguments, if any. """
    process = subprocess.Popen(cmdlist, shell=False, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()

    return stdout, stderr

def stdoutShell(cmd, suppress_stderr=False):
    """ Call given command with the added arguments, if any and return stdout. """
    if suppress_stderr:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    return stdout

def stderrShell(cmd):
    """ Call given command with the added arguments, if any and return stderr. """
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    return stderr

def Shell(cmd):
    """ Call given command with the added arguments, if any. """
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()

    return stdout, stderr
