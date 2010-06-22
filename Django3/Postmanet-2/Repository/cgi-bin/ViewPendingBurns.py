import cgi, cgitb
cgitb.enable()
import sys, os, ryw_view, ryw, su
import logging



ryw.print_header()
print '<TITLE>Outgoing Discs</TITLE>'
ryw_view.print_logo()
print ryw_view.css_str()



def get_resources():
    logging.debug('get_resources: entered...')
    try:
        resources = su.parseKeyValueFile(os.path.join(RepositoryRoot,
                                                      'Resources.txt'))
    except:
        ryw.give_bad_news('get_resources failed.', logging.critical)
        return (False, None)
    
    logging.debug('get_resources succeeded.')
    return (True, resources)

        

def print_burn_all_buttons():
	print """
<FORM Action="/cgi-bin/burn.py?" METHOD="GET">
<INPUT TYPE=hidden name=all value="true">
<INPUT TYPE="submit" value="Burn All!">
</FORM>
"""
def print_del_all_button():
	print """
<FORM Action="/cgi-bin/deleteOutgoingImage.py?" METHOD="GET">
<INPUT TYPE=hidden name=all value="true">
<INPUT TYPE="submit" value="Delete All Images">
</FORM>
"""

javascriptString = """
<script language="JavaScript" type="text/javascript">
<!--Comment tag so old browsers wont see code.

function getHTTPObject() { 
	var xmlhttp; 
	/*@cc_on
	@if (@_jscript_version >= 5) 
	  try { xmlhttp = new ActiveXObject("Msxml2.XMLHTTP"); } 
	  catch (e) { 
		try { xmlhttp = new ActiveXObject("Microsoft.XMLHTTP"); }
		catch (E) { xmlhttp = false; }
	} 
	@else xmlhttp = false; 
	@end @*/ 
	if (!xmlhttp && typeof XMLHttpRequest != 'undefined') { 
		try { xmlhttp = new XMLHttpRequest(); } 
		catch (e) { xmlhttp = false; } 
	} return xmlhttp; 
}

function burnImage(dirname,img) {
	var http = getHTTPObject();
	if (!confirm("Burn Image?")) return;
	http.open("GET","/cgi-bin/burn.py?all=false&Img="+escape(dirname),true);
	http.onreadystatechange = function() {
		if (http.readyState == 4) {
			if (http.status == 200) {
				if (http.responseText != "True") {
					document.getElementById("errorArea").innerHTML += http.responseText;
					document.getElementById("errorArea").style.display = 'block';
					window.status = "Error in burn request";
				}
			} else
				alert("Error: " + http.statusText);
		}
	}
	http.send(null);
}

function burnImageWithRobot(dirname,img) {
	var http = getHTTPObject();
	if (!confirm("Burn Image?")) return;
	http.open("GET","/cgi-bin/burn.py?withRobot=true&all=false&Img="+escape(dirname),true);
	http.onreadystatechange = function() {
		if (http.readyState == 4) {
			if (http.status == 200) {
				if (http.responseText != "True") {
					document.getElementById("errorArea").innerHTML += http.responseText;
					document.getElementById("errorArea").style.display = 'block';
					window.status = "Error in burn request";
				}
			} else
				alert("Error: " + http.statusText);
		}
	}
	http.send(null);
}

function delImage(dirname,img) {
	var http = getHTTPObject();
	if (!confirm("Delete Image?")) return;
	http.open("GET","/cgi-bin/deleteOutgoingImage.py?all=false&Img="+escape(dirname),true);
	http.onreadystatechange = function() {
		if (http.readyState == 4) {
			if (http.status == 200) {
				if (http.responseText == "True") {
					//window.location = window.location;
					document.getElementById(dirname).style.display = 'none';
				} else {
					document.getElementById("errorArea").innerHTML += http.responseText;
					document.getElementById("errorArea").style.display = 'block';
					window.status = "Error in deleting image";
				}
			} else
				alert("Error: " + http.statusText);
		}
	}
	http.send(null);
}

function clearErrorArea(){
	document.getElementById("errorArea").innerHTML = "<INPUT type=submit value='clear msg' onClick='clearErrorArea()'>&nbsp;";
	document.getElementById("errorArea").style.display = 'none';
}
//-- end comment for old browsers -->
</script>

<span id="errorArea"></span><br>

<script language="JavaScript" type="text/javascript">
<!--Comment tag so old browsers wont see code.
	document.getElementById("errorArea").style.display = 'none';
	document.getElementById("errorArea").innerHTML = "<INPUT type=submit value='clear msg' onClick='clearErrorArea()'>";
//-- end comment for old browsers -->
</script>
"""
def generate_table(resources,dirlist):

        robotPresent = ryw.has_robot(resources)

        if robotPresent:
		print_burn_all_buttons()
                
	print_del_all_button()
	print javascriptString
	print '<TABLE class="search">'
	tmpout = resources['tmpout']
	for i in dirlist:
		print make_row(tmpout,i, resources)
	print "</TABLE>"
	
rowString = """
<TR id="%(imageName)s">
<TD class="search" width=720 VALIGN=CENTER ALIGN=CENTER>
	<TABLE WIDTH=100%% BORDER=0>
	<TR><TD VALIGN=TOP ALIGN=LEFT>
	<B><FONT SIZE=3>
	<A HREF="%(file_url)s" TITLE="Examine Image" TARGET="_blank">%(imageName)s</A>&nbsp;&nbsp;
	</FONT></B></TD>
	<TD VALIGN=TOP ALIGN=RIGHT>
        %(robot_string)s
	<IMG SRC="/icons/RecordNow.gif" BORDER=0 title="Burn without robot" onmouseover="this.style.cursor='pointer';" onClick="burnImage('%(imageName)s',this)">
	<IMG SRC="/icons/trash.gif" BORDER=0 title="Delete" onmouseover="this.style.cursor='pointer';" onClick="delImage('%(imageName)s',this)">
	</TD></TR>
	<TR><TD VALIGN=TOP ALIGN=LEFT><FONT SIZE=2>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Image for %(recipient)s</FONT></TD></TR>
	<TR><TD VALIGN=TOP ALIGN=LEFT><I><FONT SIZE=2>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;created: %(date)s.</FONT></I></TD></TR>
	</TABLE>
</TD></TR>
"""

rowStringRobot = """
	<IMG SRC="/icons/robot.jpg" BORDER=0 title="Burn with robot" onmouseover="this.style.cursor='pointer';" onClick="burnImageWithRobot('%(imageName)s',this)">
"""


def make_row(tmpdir,imgdir, resources):
	import time

        try:
            d = {"imageName":imgdir}
            dir = os.path.join(tmpdir,imgdir)
            d['file_url'] = "file:///" + os.path.abspath(dir) + \
                            "/repository/html/index.html"
            d['recipient'] = open( \
                os.path.join(dir, "repository",
                             "usercredentials")).readline().strip()
            d['date'] = time.ctime(os.stat(dir).st_ctime)
            if ryw.has_robot(resources):
                d['robot_string'] = rowStringRobot % d
                return rowString % d
            else:
                d['robot_string'] = ''
                return rowString % d
        except:
            logging.info('make_row: unknown directory: ' +
                         tmpdir + ', ' + imgdir)
            return ''
		
	

def main():
	ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
	 
	logging.debug("outgoing disc queue entered")
	success,resources = get_resources()
	if not success:
		ryw.give_bad_news("main: error parsing resource file",logging.error)
	 
	outdir = resources['tmpout']
	dirlist = os.listdir(outdir)
	if len(dirlist) == 0:
		print "<br><h3>There are no pending outgoing discs waiting to be written\n"
	else:
		generate_table(resources,dirlist)
	
	logging.debug("generated queue page")
	ryw_view.print_footer()

if __name__ == "__main__":
	main()
