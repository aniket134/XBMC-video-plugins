import ryw_hindi,ryw,ryw_customize


##########
## the following is basically the html page.
##########

pageStr = """
<HTML>
<HEAD>
<TITLE>Key Word Search</TITLE>

<style type="text/css">
body { font-family: sans-serif; }
</style>

</HEAD>

<BODY>

<CENTER>
<A HREF="/index.html">
<IMG SRC="%(smallLogoFileName)s" BORDER=0 %(smallLogoDimension)s></A>
<BR>

<H3>Key Word Search &nbsp;&nbsp; %(trans_key_search)s</H3>


<TABLE BORDER=0 WIDTH=800><TR><TD>

Enter key words &nbsp;&nbsp; %(trans_enter_key_words)s :
<BR>

<FORM ACTION="%(search_script)s" METHOD="post"
ENCTYPE="multipart/form-data">

<!-- textfield contains any/all of the words -->
<INPUT TYPE="TEXT" NAME="all_keys_concatenated" SIZE=120>
<BR><BR>

<TABLE BORDER=0>
<TR>
<TD>
<INPUT TYPE="RADIO" NAME="all_keys_concatenated_match_any_or_all" checked value="all"> Match all words &nbsp; %(trans_match_all)s &nbsp;&nbsp;&nbsp;
</TD>
<TD>
<INPUT TYPE="RADIO" NAME="all_keys_concatenated_case" checked value="insensitive"> Case-Insensitive
</TD>
</TR>

<TR>
<TD>
<INPUT TYPE="RADIO" NAME="all_keys_concatenated_match_any_or_all" value="any"> Match any word &nbsp; %(trans_match_any)s &nbsp;&nbsp;&nbsp;
</TD>
<TD>
<INPUT TYPE="RADIO" NAME="all_keys_concatenated_case" value="sensitive"> Case-Sensitive
</TD>
</TR>
</TABLE>


<BR>


<P>

<INPUT TYPE="HIDDEN" NAME="sort_field" VALUE="Upload_Time">
<INPUT TYPE="HIDDEN" NAME="sort_order" VALUE="decreasing">


<INPUT TYPE="submit" VALUE="Search">
<INPUT TYPE="submit" VALUE="%(trans_search)s" %(trans_txt_style)s>


<INPUT TYPE="HIDDEN" NAME="start_index" VALUE="0">

</FORM>

</TD></TR></TABLE>

</CENTER>

<BR>

<HR WIDTH=75%%>

%(uploadFooter)s

<HR WIDTH=75%%>

</BODY>
</HTML>
"""

##########
## the above is basically the html page.
##########



def specify_search_script(scriptName):
    dict = ryw_customize.dict
    dict['year'] = ryw.get_year()
    dict['search_script'] = scriptName
    dictTrans = ryw_hindi.dict_size4_hindi_html(['key_search',
                                                 'enter_key_words',
                                                 'match_all',
                                                 'match_any'])
    dictTrans2 = ryw_hindi.dict_hindi(['search'])
    dict.update(dictTrans)
    dict.update(dictTrans2)
    return pageStr % dict
