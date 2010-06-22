import os,ryw, ryw_view, ryw_customize



######################################################################
# the following is just the html front page.
######################################################################

page = """
<HTML>
<HEAD>
<TITLE>%(entranceTitle)s</TITLE>

</HEAD>

<BODY>

<CENTER>

<TABLE BORDER=0 WIDTH=600>

<TR><TD ALIGN=CENTER>
<IMG SRC="%(bigLogoFileName)s" %(logoDimension)s BORDER=0><BR>
<BR>
<FONT SIZE=2>
(You are currently logged on as the user named: <I><B>%(name)s</B></I>.)
</FONT>
<BR>
&nbsp;<BR>
</TD></TR>

<TR><TD>

<CENTER>

<TABLE BORDER=0>

<TR><TD VALIGN=TOP>

%(documentaryLinks)s

<FONT SIZE=3><B><I>Data:</I></B></FONT>

<UL>

<LI><a href="/cgi-bin/search_su.py?sort_field=Upload_Time&sort_order=decreasing">list the most recently added content</a>

<LI>(<a href="/cgi-bin/search_su.py?sort_field=Changed_Time&sort_order=decreasing">most recently changed content</a>)


<!--
<LI><A HREF="delete_test.html">test: delete</A><br>
-->

</UL>


</TD>

<TD VALIGN=TOP>
&nbsp;&nbsp;&nbsp;&nbsp;
</TD>

<TD VALIGN=TOP>

<FONT SIZE=3><B><I>Search:</I></B></FONT>

<UL>

<LI><a href="/cgi-bin/search_su_keyword.py">key word search</a><br>

<LI><a href="/cgi-bin/search_su_author.py">search by author</a><br>

</UL>


<FONT SIZE=3><B><I>Administration:</I></B></FONT>

<UL>

<LI><A HREF="/cgi-bin/ManageUserAccounts.py">manage accounts</A><br>

</UL>



<script language="JavaScript" type="text/javascript">
<!--Comment tag so old browsers wont see code.
function confirmLocation(url,params,name){
	var loc = prompt("produce outgoing discs for " + name + "?.\\n Press cancel below to cancel.\\nEnter location for temporary data in field or leave blank for default option.\\n","");
	if (loc == "") {
		window.location = url;
		return false;
	}
	if (loc == null) {
		return false;
	}
	window.location = url + "?" + params + "=" + escape(loc);
	return false;
}

function confirmLocationMeta(url,params,name){
	var loc = prompt("produce outgoing discs for " + name + "?.\\n Press cancel below to cancel.\\nEnter location for temporary data in field or leave blank for default option.\\n","");
	if (loc == "") {
		window.location = url;
		return false;
	}
	if (loc == null) {
		return false;
	}
	window.location = url + "&" + params + "=" + escape(loc);
	return false;
}

//-- end comment for old browsers -->
</script>


%(confirmPopup)s

</TD></TR>


</TABLE>

</CENTER>
</TABLE>
</CENTER>


<BR>

<HR WIDTH=75%%>

%(entranceFooter)s

<HR WIDTH=75%%>

</BODY>
</HTML>
"""

######################################################################
# the above is just the html front page.
######################################################################



ryw.print_header()
dict = ryw_customize.dict
dict['year'] = ryw.get_year()
dict['repView'] = os.path.join(RepositoryRoot, 'View')
dict['name'] = os.getenv("REMOTE_USER")
dict['tmpDir'] = os.path.join(RepositoryRoot, '__INCOMING_DISCS__')
dict['confirmPopup'] = ryw_view.confirm_popup_js()
print page % dict

