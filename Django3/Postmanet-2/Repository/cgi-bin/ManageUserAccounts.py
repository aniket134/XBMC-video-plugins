
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

print '\n<FORM action="/cgi-bin/UpdateUserInfo.py" method="post" enctype="multipart/form-data">\n\n'

print '<P><B>Username</B><BR> <INPUT type=text name=username size=30>'

print '<P><B>Address</B><BR><TEXTAREA name=address value="" rows=5 cols=60></TEXTAREA>'

print '<P><B>New Password</B><BR> <INPUT type=password name=passwd size=30>'

print '<P><B>Re-type New Password</B><BR> <INPUT type=password name=retypepasswd size=30>'

print '\n<p>\n<INPUT type="submit" value="Update User Information"> <INPUT type="reset" value="Clear All">\n'

print '\n</FORM>\n'

ryw_view.print_footer()
