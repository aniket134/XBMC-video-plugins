import ryw_hindi,ryw,ryw_customize


##########
## the following is basically the html page.
##########

pageStr = """
<HTML>
<HEAD>
<TITLE>Search by Author</TITLE>

<style type="text/css">
body { font-family: sans-serif; }
</style>

</HEAD>

<BODY>

<CENTER>
<A HREF="/index.html">
<IMG SRC="%(smallLogoFileName)s" BORDER=0 %(smallLogoDimension)s></A>
<BR>

<H3>Search by Author &nbsp;&nbsp; %(trans_search_author)s</H3>

<TABLE BORDER=0 WIDTH=800><TR><TD ALIGN=CENTER>

<FORM ACTION="%(search_script)s" METHOD="post"
ENCTYPE="multipart/form-data">

Enter author name &nbsp;&nbsp; %(trans_enter_author)s :
<P>

<INPUT TYPE="TEXT" NAME="author_name" SIZE="40">
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
    dictTrans = ryw_hindi.dict_size4_hindi_html(['search_author',
                                                 'enter_author'])
    dictTrans2 = ryw_hindi.dict_hindi(['search'])
    dict.update(dictTrans)
    dict.update(dictTrans2)
    return pageStr % dict
