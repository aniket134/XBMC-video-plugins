
import os, sys
import su, RunPYProcessDetached as Run, KillXMLRPCServer as Kill

import cgi, cgitb
cgitb.enable()

name = os.getenv("REMOTE_USER")

print 'Content-Type: text/html'
print

print '<P> Hello!,', name

if name != 'admin':
    print '<P>Administrator only..'
    sys.exit(1)

#####################################################################

# Read from file
resfile = os.path.join(RepositoryRoot, 'Resources.txt')

resources = {}

f = open(resfile)

for line in f.readlines():
    line = line.strip()
    key, value = line.split('=', 1)

    key = key.strip()
    value = value.strip()

    resources[key] = value

f.close()

### Update from form
form = cgi.FieldStorage()

for key in form.keys():
    key = key.strip()
    resources[key] = form.getfirst(key).strip()

### Write to file
g = open(resfile, 'w')

for key in resources.keys():
    g.write('%s=%s\n' % (key, resources[key]))

g.close()

####

for key in resources.keys():
    print '<P>%s=%s\n' % (key, resources[key])
