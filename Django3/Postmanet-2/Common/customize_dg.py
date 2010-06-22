
dict = {}


#
# index.py
# for the entrance page
# 
dict['bigLogoFileName'] = "/icons/dg800.gif"
dict['logoDimension'] = "WIDTH=620 HEIGHT=189"
dict['entranceTitle'] = "Digital Green Database Management"

dict['documentaryLinks'] = ''

dgFooter = """
<center>
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/">
<img alt="Creative Commons License" style="border-width:0"
src="/icons/88x31.png" />
</a>
<br>
<a href="mailto:dg_team@microsoft.com"
style="text-decoration:none"><font face="arial,helvetica,sanserif"
size=2 color="#000000"><b>digital <font color="green">Green</font>
Team</a>
</center>
"""

dict['entranceFooter'] = dgFooter



#
# Browse.py
# for the browse view page.
# not really used any more.
# but placed here anyhow.
#
def print_view_footer(self):
    print '<BR><BR>' + dgFooter



#
# ryw_view.py
#
dict['headerLogo'] = """
<A HREF="/index.html">
<IMG SRC="/icons/dg500.gif" WIDTH=482 HEIGHT=129 BORDER=0></A>
<BR><BR>
"""



#
# ryw_uploadStrs_English.py
#
dict['uploadFooter'] = dgFooter
dict['smallLogoFileName'] = "/icons/dg500.gif"
dict['smallLogoDimension'] = "WIDTH=482 HEIGHT=129"



#
# ryw_view.py
#
dict['footerStr'] = '<BR><BR><BR>' + dgFooter
dict['footerStr2'] = '<BR><BR><BR>' + dgFooter
dict['logoStr'] = """<IMG SRC="./icons/dg500.gif"
WIDTH=482 HEIGHT=129 BORDER=0><BR>
"""
