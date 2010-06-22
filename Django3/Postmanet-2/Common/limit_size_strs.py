import ryw_hindi,ryw,ryw_customize


##########
## the following is basically the html page.
##########

pageStr = """
<HTML>
<HEAD>
<TITLE>Specify Details of Outgoing Data</TITLE>

<style type="text/css">
body { font-family: sans-serif; }
</style>

</HEAD>

<BODY>

<CENTER>
<A HREF="/index.html">
<IMG SRC="%(smallLogoFileName)s" BORDER=0 %(smallLogoDimension)s></A>
<BR>

<TABLE BORDER=0><TR><TD>

<H3>How would you like to make outgoing data?</H3><BR>

<FORM ACTION="%(script)s" METHOD="post"
ENCTYPE="multipart/form-data">


<UL>
<LI>
enter maximum disc size:
<INPUT TYPE="TEXT" NAME="disc_limit" SIZE=10> MB
<BR><BR>

<LI>
send metadata only:
<INPUT type=checkbox name="meta">
<BR><BR>

<LI>
temporary data path name:
<INPUT TYPE="TEXT" NAME="tmpdir" SIZE=30>
<BR>
</UL>


<BR><BR>
<CENTER>
<INPUT TYPE="submit" VALUE="Generate">
</CENTER>

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



def give_str(scriptName):
    dict = ryw_customize.dict
    dict['year'] = ryw.get_year()
    dict['script'] = scriptName
    return pageStr % dict

