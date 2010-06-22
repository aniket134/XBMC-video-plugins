import datetime



def get_year():
    now = datetime.datetime.now()
    return now.strftime('%Y')

dict = {}
dict['year'] = get_year()



#
# index.py
# for the entrance page
# 
dict['bigLogoFileName'] = "/icons/sankalp_big.jpg"
dict['logoDimension'] = "WIDTH=400 HEIGHT=235"
dict['entranceTitle'] = "Sankalp School Digital Video Library"

dict['documentaryLinks'] = """
<FONT SIZE=3><B><I>Movies:</I></B></FONT>

<UL>

<LI><a href="/cgi-bin/DisplaySelection.py?objstr=GP8QX2HE6EKPPGVUZ7GI%231">randy's recommendations</a><br>

<LI><a href="/cgi-bin/DisplaySelection.py?objstr=J5BE4TRWND3SR2BF1VDD%231">all movies</a><br>

</UL>
"""

dshEntranceFooter = """
<CENTER>
<FONT SIZE=2>
&#169 2005-%(year)s &nbsp;&nbsp;
The Digital StudyHall
</FONT>
</CENTER>
"""

dict['entranceFooter'] = dshEntranceFooter % dict



#
# Browse.py
# for the browse view page.
# not really used any more.
# but placed here anyhow.
#
def print_view_footer(self):
    """ print usual end of html file stuff """
    str = """ <BR><TABLE BORDER=0 WIDTH=500><TR><TD><HR><CENTER>
<FONT SIZE=2>
<A HREF="/index.html">back to home</A>&nbsp;&nbsp;&nbsp;&nbsp;<A HREF="%(backlink)s">up one level</A>&nbsp;&nbsp;&nbsp;&nbsp; &#169 2005-%(year)s &nbsp;The Digital StudyHall
</FONT>
<BR></CENTER><HR></TD></TR></TABLE>
</body>
</html>""" 
    backpath = os.path.dirname(self.relpath[:-1])
    backlink = self.scriptName + "?viewroot=" + self.viewroot + "&relpath=" + backpath
    d2 = dict
    d2['backlink'] = backlink
    print str % d2



#
# ryw_view.py
#
dict['headerLogo'] = """
<A HREF="/index.html">
<IMG SRC="/icons/sankalp_small.jpg" WIDTH=200 HEIGHT=118 BORDER=0></A>
<BR>
"""



#
# ryw_uploadStrs_English.py
#
dshUploadFooter = """
<CENTER>
<FONT SIZE=2>
&#169 2005-%(year)s &nbsp;&nbsp;
<A HREF="/index.html">The Digital StudyHall</a>
</FONT>
</CENTER>
"""
dict['uploadFooter'] = dshUploadFooter % dict
dict['smallLogoFileName'] = "/icons/kannar2.jpg"
dict['smallLogoDimension'] = "WIDTH=200 HEIGHT=134"



#
# ryw_view.py
#
dshFooter = """<BR><BR><TABLE BORDER=0 WIDTH=400><TR><TD><CENTER><HR><FONT SIZE=-1 FACE=ARIAL>&#169 2005-%(year)s &nbsp;&nbsp;<A HREF=/index.html>The Digital StudyHall</A></FONT><HR></CENTER></TD></TR></TABLE>"""
dict['footerStr'] = dshFooter % dict

dshFooter2 = """
<BR><BR><TABLE BORDER=0 WIDTH=400><TR><TD><CENTER><HR>
<FONT SIZE=2>&#169 2005-%(year)s &nbsp;&nbsp;
The Digital StudyHall</FONT>
<HR></CENTER></TD></TR></TABLE>
"""
dict['footerStr2'] = dshFooter2 % dict
dict['logoStr'] = """<IMG SRC="./icons/kannar2.jpg"
WIDTH=200 HEIGHT=134 BORDER=0><BR>
"""
