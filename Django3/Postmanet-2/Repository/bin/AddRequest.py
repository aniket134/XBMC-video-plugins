import os
import os.path
import pickle
import ryw

pdrroot = os.getenv('PDRROOT') or 'C:\\PDRROOT'

if pdrroot[-1] != '\\':
    pdrroot = pdrroot + '\\'

print
print 'PDRROOT  :', pdrroot

# Endpoints file
epfpath = pdrroot + 'Endpoints.pk'

if os.path.exists(epfpath):
    #RYW: changed to "rb"
    #f = open(epfpath, "rb")
    #endpoints = pickle.load(f)
    #f.close()
    endpoints = ryw.pickload_load_raw_and_text(epfpath)
else:
    endpoints = {}

# endpoints is the dictionary of existing endpoints

name = raw_input('Enter Username : ')

if endpoints.has_key(name):
    newaddr = raw_input('Enter Address [' + endpoints[name] + ']: ')
    if newaddr:
        endpoints[name] = newaddr
else:
    endpoints[name] = raw_input('Enter Address : ')

tmppath = epfpath + '.TMP'
#RYW change to "wb"
f = open(tmppath, "wb")
pickle.dump(endpoints, f)
f.flush()
os.fsync(f.fileno())
f.close()

if os.path.exists(epfpath):
    os.remove(epfpath)
os.rename(tmppath, epfpath)
