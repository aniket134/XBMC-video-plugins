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

<TABLE BORDER=0 WIDTH=900>

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

<LI><A HREF="/cgi-bin/upload_English.py">add content to the repository</A>
<BR>

<LI><A
HREF="/cgi-bin/BrowseView.py?viewroot=%(repView)s&relpath=\\">browse
the content repository</A><br>

<LI><a href="/cgi-bin/search_su.py?sort_field=Upload_Time&sort_order=decreasing">list the most recently added content</a>

<LI>(<a href="/cgi-bin/search_su.py?sort_field=Changed_Time&sort_order=decreasing">most recently changed content</a>)


<!--
<LI><A HREF="delete_test.html">test: delete</A><br>
-->

</UL>


<FONT SIZE=3><B><I>Selection:</I></B></FONT>

<UL>

<LI><A HREF="/cgi-bin/ShowQueue.py">manage selected objects</A>
(<A HREF="/cgi-bin/ShowQueue.py?offset=all">all</A>)<br>

<LI><A HREF="/cgi-bin/SelectAll.py"
onClick="return confirmPopup('/cgi-bin/SelectAll.py','Select all objects?',500,350);">select all objects</A><br>

<LI><A HREF="/cgi-bin/ClearQueue.py"
onClick="return confirmPopup('/cgi-bin/ClearQueue.py','De-select all currently selected objects?',500,350);">de-select all</A><br>

<LI><A HREF="/cgi-bin/UploadQueue_form.py"
onClick="return confirm('Save the current selection?');">save
the selection</A><br>

<LI><A HREF="/cgi-bin/SelectTexts.py"
onClick="return confirm('Prepare for translation?');">prepare for translation</A><br>


</UL>


<FONT SIZE=3><B><I>Administration:</I></B></FONT>

<UL>

<LI><A HREF="/cgi-bin/ClearTmp.py" onClick="return confirm('Clear temp space?');">clear temporary storage space</A><br>

<LI><A HREF="/cgi-bin/ManageUserAccounts.py">manage accounts</A><br>

<LI><A HREF="/cgi-bin/EditConfig.py">edit the configuration file</A><br>

<LI><A HREF="/cgi-bin/rebuildSearchFile.py" onClick="return confirm('Rebuild SearchFile?');">rebuild search index</A><br>

<LI><A HREF="/cgi-bin/RebuildReverseLists.py" onClick="return confirm('Rebuild ReverseLists?');">rebuild ReverseLists</A><br>

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

<LI><a href="/cgi-bin/search_su_adv.py">advanced search</a>

</UL>


<FONT SIZE=3><B><I>Discs:</I></B></FONT>

<UL>

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

	
<LI><A HREF="/cgi-bin/FlushQueue.py" onClick="return confirmLocation('/cgi-bin/FlushQueue.py','tmpdir','%(name)s');">generate outgoing disc images</A><br>
<LI><A HREF="/cgi-bin/FlushQueue.py?meta=true" onClick="return confirmLocationMeta('/cgi-bin/FlushQueue.py?meta=true','tmpdir','%(name)s');">generate outgoing metadata only</A><br>
<LI><A HREF="/cgi-bin/DiscLimit.py">specify details of outgoing data</A><br>
<LI><A HREF="/cgi-bin/ViewPendingBurns.py">manage and burn outgoing disc images</A><br>

<LI><A HREF="/cgi-bin/ProcessIncomingDiscs.py">process a stack of incoming
discs</A><br>

<LI><A HREF="/cgi-bin/eraseDiscs.py" onClick="return confirm('Erase discs?');">erase a stack of discs</A><br>

</UL>



<FONT SIZE=3><B><I>Tests:</I></B></FONT>

<UL>

<LI><A
HREF="/cgi-bin/ProcessDiscs.py?tmpdir=%(tmpDir)s&jobfile=foobarbaz">process
incoming data on local disk</A><br>

<LI><A
HREF="/cgi-bin/TestReverseLists.py">look at ReverseLists</A><br>


</UL>




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

