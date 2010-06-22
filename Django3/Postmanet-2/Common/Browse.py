import sys, os
import logging, datetime
import re
import ryw, ryw_view
import pickle, cgi, cgitb, xmlrpclib
import objectstore
import SearchFile
import urllib
import ryw_customize
import ReverseLists
import ryw_bizarro



def reqDownloadFunc_notused(meta, calledByVillageSide, dataURL):
    downloadIconStr = """
<IMG SRC="/icons/link.gif" BORDER=0 title="select this" onmouseover="this.style.cursor='pointer';" onClick="reqData('%s',this)">
"""
    deleteIconStr = """
<IMG SRC="/icons/trash.gif" BORDER=0 title="delete object" onmouseover="this.style.cursor='pointer';" onClick="delData('%s')">
<A href="%s"><IMG SRC="/icons/quill.gif" BORDER=0 title="edit object attributes"></A>
"""
    #<IMG SRC="/icons/quill.gif" BORDER=0 title="edit object attributes" onClick="window.open('/cgi-bin/ShowObject.py?'+escape(%s),'_blank','scrollbar=yes,resizable,alwaysRaised');return false;">

    name = os.getenv("REMOTE_USER")
    if name == '' or name == 'guest':
        return ''

    id = meta['id'] + '#' + str(meta['version'])

    if calledByVillageSide and dataURL != None:
        return ""

    if not calledByVillageSide and os.getenv("REMOTE_USER") == "admin":
        return deleteIconStr % (id,"/cgi-bin/ShowObject.py?objstr=" + urllib.quote(id))
    return downloadIconStr % (id,)



def reqDownloadFunc(meta, calledByVillageSide, dataURL, searchFile=None):
    name = os.getenv("REMOTE_USER")
    if name == '' or name == 'guest':
        return ''

    id = meta['id'] + '#' + str(meta['version'])
    downloadIconStr = """<IMG
SRC="/icons/link.gif" BORDER=0 title="select this"
onmouseover="this.style.cursor='pointer';" onClick="reqData('%s',this)">
"""
    downloadIconStr = downloadIconStr % (id,)

    deleteIconStr = """<IMG
SRC="/icons/trash.gif" BORDER=0 title="delete object"
onmouseover="this.style.cursor='pointer';" onClick="delData('%s')">
"""
    deleteIconStr = deleteIconStr % (id,)

    editIconStr = """<A
href="%s"><IMG SRC="/icons/quill.gif" BORDER=0
title="edit object attributes"></A>
"""
    editIconStr = editIconStr % ("/cgi-bin/ShowObject.py?objstr=" +
                                 urllib.quote(id),)

    allVersIconStr = make_all_version_icon_str(meta, searchFile)

    if calledByVillageSide and dataURL != None:
        return ''

    allUserIcons = editIconStr + downloadIconStr + allVersIconStr

    if not calledByVillageSide and name == "admin":
        return deleteIconStr + allUserIcons
    
    return allUserIcons



def make_all_version_icon_str(meta, searchFile):
    """if there're more than one version of this object,
    make an icon for displaying them all."""

    objID = meta['id']       
    version = meta['version']
    objstr = objID + '#' + str(version)
       
    versionIconStr = """<A
href="%s" onClick="return confirm('Clone a new version of this object?');"><IMG
SRC="/icons/c2.gif" BORDER=0
title="clone a new version"></A>
"""
    versionIconStr = versionIconStr % \
                     ("/cgi-bin/CloneVersion.py?objstr=" +
                      urllib.quote(objstr),)

    return versionIconStr



def script_str(target = "", calledByVillageSide = False):
	script = """
<script language="JavaScript" type="text/javascript">
<!--Comment tag so old browsers wont see code.


function reqData(param,img) {
	if (img.src == "/icons/burst.gif") return true;
	var http = getHTTPObject();
	http.open("GET","%s?selection="+escape(param),true);
	http.onreadystatechange = function() {
		if (http.readyState == 4) {
			if (http.status == 200) {
				if (http.responseText == "True") {
					window.status = "Successfully selected " + param;
					img.src = "/icons/burst.gif";
					img.title = "request queued";
				} else {
					document.getElementById("errorArea").innerHTML += http.responseText;
					document.getElementById("errorArea").style.display = 'block';
					window.status = "Error in selecting " + param;
				}
			} else
				alert("Error: " + http.statusText);
		}
	}
	http.send(null);
}
	
function delData(param) {
	var http = getHTTPObject();
	if (!confirm("Delete object " + param + " ?")) return;
	http.open("GET","/cgi-bin/DeleteObject.py?objstr="+escape(param),true);
	http.onreadystatechange = function() {
		if (http.readyState == 4) {
			if (http.status == 200) {
				if (http.responseText == "True") {
					//window.location = window.location;
					document.getElementById(param).style.display = 'none';
				} else {
					document.getElementById("errorArea").innerHTML += http.responseText;
					document.getElementById("errorArea").style.display = 'block';
					window.status = "Error in deleting " + param;
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
"""
	if target:
		return script % (target,)
	elif calledByVillageSide:
		return script % ("/cgi-bin/repository/AddToQueue.py",)
	else:
		return script % ("/cgi-bin/AddToQueue.py",)


class BrowseForm:

	def __init__(self, searchfile,
		     objectStoreRoot = None,
		     absObjStoreRoot = None,
		     Root = None,
		     calledByVillageSide = None,
		     action = None):

		assert(objectStoreRoot != None)
		assert(absObjStoreRoot != None)
		assert(Root != None)
		assert(calledByVillageSide != None)
		self.scriptName = os.environ['SCRIPT_NAME']
		self.action = action
		self.searchFile = searchfile
		self.objectStoreRoot = objectStoreRoot
		self.absObjStoreRoot = absObjStoreRoot
		self.Root  = Root
		self.calledByVillageSide = calledByVillageSide
		cgitb.enable()

	def print_initialHTML(self):
		htmlStart =  """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">

<html>
<head>
<title>Browse Logical View</title>
"""
		htmlEnd = """
</head>

<body>
"""
		print htmlStart + self.script_str() + ryw_view.css_str() + \
                      htmlEnd


	def script_str(self):
		if self.action:
			return script_str(target = self.action)
		else:
			return script_str(calledByVillageSide = self.calledByVillageSide)

	def print_footer(self):
            ryw_customize.print_view_footer(self)

            

	def generate(self):
            """Main Browse View function."""
            ryw.print_header()
            self.print_initialHTML()
            form = cgi.FieldStorage()
            #	setup_logging()

            viewroot = form.getfirst('viewroot', '')
            if not viewroot:
                ryw.give_bad_news('viewroot not found',logging.error)
                sys.exit(1)

            ryw.db_print2('Browse.generate: viewroot is: ' + viewroot, 61)
                          
            if viewroot[-1] == os.sep:
	       	viewroot = viewroot[:-1]

            relpath = form.getfirst('relpath', os.sep)
            ryw.db_print2('Browse.generate: relpath1: ' + relpath, 61)
            relpath = ryw_bizarro.fix_browse_rel_path(relpath)
            ryw.db_print2('Browse.generate: relpath2: ' + relpath, 61)
            
            if relpath[0] != os.sep:
	       	relpath = os.sep + relpath
            if relpath[-1] != os.sep:
	       	relpath = relpath + os.sep

            ryw.db_print2('Browse.generate: relpath3: ' + relpath, 61)
            path = viewroot + relpath

            self.viewroot = viewroot
            self.relpath = relpath

            # path must be a directory

            if not os.path.exists(path):
	       	ryw.give_news('path no longer exists: ' + path,
	       		      logging.warning)
	       	sys.exit(1)
            ll = os.listdir(path)

            #success,searchFile = ryw.open_search_file(
            #    self.scriptName + ':', self.logDir, self.logFile,
            #    self.searchFile, False)
            #if not success:
            #    sys.exit(1)

            count=0

            title = relpath[1:-1]
            title = title.replace("\\"," &raquo; ")
            #print "<H2>The Digital StudyHall</H2>"
            ryw_view.print_logo()
            if title != "":
	       	print "<H3> content repository: %s </H3>" % (title,)
            else:
                print "<H3> content repository: </H3>"

            print "<TABLE border=0 width=100%><TR>"
            for i in ll:
                if not os.path.isfile(path+i):
                    print '<td width=20%%><A HREF="%s?viewroot=%s&relpath=%s%s"><img src="/icons/folder.gif" border=0><br>%s</A></td>' % (self.scriptName,viewroot,relpath,i,i)
                    count += 1
                    if (count == 5):
                        print "</TR><TR>"
                        count = 0
            while (count < 5):
	       	print "<td width=20%>&nbsp;</td>"
	       	count += 1
            print "</TR></TABLE>"
				      
				
            metalist = []

            for i in ll:
            
	       	if os.path.isfile(path + i):
                    # get its metadata from server and add option
                    # for 'add to downloadqueue'
                    f = open(path + i)
                    line = f.readline()
                    f.close()
                    if line[-1] == '\n':
                        line = line[:-1]
                    objname, version = line.split('#')
                    version = int(version)

                    #success,d = searchFile.get_meta(objname,
                    #				       version)
                    success,d = ryw.get_meta(self.absObjStoreRoot,
                                             objname,
                                             version)
                    if not success:
                        logging.warning(
                            self.scriptName + ': get_meta failed: ' +
                            objname + ' ' + str(version))
                        continue
			  
                    metalist.append(d)


            metalist = ryw.sortmeta(metalist)

            success,searchFile,reverseLists = \
                ReverseLists.open_searchfile_reverselists(
                    'Browse.generate:')
            if not success:
                sys.exit(1)

            displayObject = ryw_view.DisplayObject(
                self.Root, calledByVillageSide = self.calledByVillageSide,
                missingFileFunc = reqDownloadFunc,
                searchFile = searchFile,
                reverseLists = reverseLists)

            displayObject.begin_print()
            for i in metalist:
                #self.generate_row(d)
                displayObject.show_an_object_compact(i)
		      
            displayObject.end_print()
            self.print_footer()
            searchFile.done()
            reverseLists.done()

