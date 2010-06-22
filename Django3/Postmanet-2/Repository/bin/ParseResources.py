
import sys, os, _winreg

#####
a = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE')
a = _winreg.OpenKey(a, 'Postmanet')
a = _winreg.OpenKey(a, 'Repository')
reppath = _winreg.EnumValue(a, 0)[1]
print 'reppath =', reppath

sys.path.append(reppath + 'Common')
sys.path.append(reppath + 'bin')

import su
#####

def parseResources():
    resources = {}
    f = open(reppath + 'Resources.txt')

    line = su.readgl(f)
    while line:
        if line[-1] == '\n':
            line = line[:-1]
        key, value = line.split('=', 1)
        resources[key] = value
        line = su.readgl(f)

    f.close()
    return resources
