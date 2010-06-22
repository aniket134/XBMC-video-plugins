
import os, sys
import su
import ryw_view

import cgi, cgitb
cgitb.enable()

name = os.getenv("REMOTE_USER")

ryw_view.print_header_logo()


print '<P> Hello,', name

if name != 'admin':
    print '<P>Administrator only.'
    ryw_view.print_footer()
    sys.exit(1)

sys.path.append(os.path.join(RepositoryRoot, 'bin'))
import ReadIncomingCDStack
ReadIncomingCDStack.main()

ryw_view.print_footer()
