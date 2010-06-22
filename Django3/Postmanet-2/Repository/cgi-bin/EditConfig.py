
import os, sys
import su, RunPYProcessDetached as Run, KillXMLRPCServer as Kill
import ryw_view, ryw_upload

import cgi, cgitb
cgitb.enable()

name = os.getenv("REMOTE_USER")

ryw_view.print_header_logo()

print '<P> Hello!,', name

if name != 'admin':
    print '<P>Administrator only.'
    ryw_upload.quick_exit(1)


#####################################################################

resfile = os.path.join(RepositoryRoot, 'Resources.txt')

resources = {}

for line in open(resfile).readlines():
    line = line.strip()
    key, value = line.split('=', 1)

    key = key.strip()
    value = value.strip()

    resources[key] = value

print '\n<FORM action="/cgi-bin/UpdateConfig.py" method="post" enctype="multipart/form-data">\n\n'

for key in resources.keys():
    if key != 'apachepath' and key != 'pythonpath':
        print '\n<P><B>%s</B><BR> <INPUT type=text name="%s" value="%s" size=100>\n' % (key, key, resources[key])

print '\n<p>\n<INPUT type="submit" value="Update Configuration"> <INPUT type="reset" value="Clear All">\n'
print '\n</FORM>\n'


ryw_view.print_footer()
