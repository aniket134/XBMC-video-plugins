import cgi, cgitb
cgitb.enable()
import sys, os, ryw_view, ryw



ryw.print_header()
ryw_view.print_logo()



message = """

<TITLE>Generating Outgoing Disc</TITLE>

You are about to generate an outgoing disc destined for
<B><I>%(name)s</I></B>.
<P>


<FORM ACTION="/cgi-bin/FlushQueue.py" METHOD="post">
<INPUT TYPE="submit" VALUE="Continue">
</FORM>

<INPUT TYPE="submit" VALUE="Cancel" onClick="window.close(); return true;">

"""


dict = {}
dict['name'] = os.getenv("REMOTE_USER")

print message % dict
ryw_view.print_footer()
