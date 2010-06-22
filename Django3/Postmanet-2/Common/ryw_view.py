import sys, os, pickle, objectstore, random, shutil
import logging, datetime, time, zipfile, cStringIO, shutil
import string
import traceback
import ryw_upload,su,SearchFile,ryw_disc,ryw,urllib,cgi,ryw_hindi
import ryw_meta, ryw_ffmpeg, ryw_customize
import ReverseLists
import explorer
import google_english2hindi
from PIL import Image



THUMB_WIDTH  = 100
THUMB_HEIGHT = 128

BLANKS = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'

POPUP_DIR_WIDTH = 450
POPUP_DIR_HEIGHT = 300


BUTTON_WIDTH = 80
BUTTON_HEIGHT = 15

CONFIRM_WIDTH = 500
CONFIRM_HEIGHT = 350



class DisplayObject:
    
    def __init__(self, swRoot, calledByVillageSide = False,
                 missingFileFunc = None, calledByQ2Qmsg = False,
		 callBackArg = None, searchFile = None,
                 reverseLists = None):
        """a lame way of parameterizing the rest of this file so it can be
        called from multiple places.
        02/20/08: searchFile turns out to be not needed, for now."""
        
        self.swRoot = swRoot
        self.calledByVillageSide = calledByVillageSide
        self.missingFileFunc = missingFileFunc
        self.calledByQ2Qmsg = calledByQ2Qmsg
	self.callBackArg = callBackArg
        self.searchFile = searchFile
        self.reverseLists = reverseLists



    def begin_print(self):
        begin_print()



    def end_print(self):
        end_print()



    def __hide_parameters(self, meta):
        #
        # an ugly way of hiding an extra parameter for the rest of the code
        # to pick up.  we'll delete the extra attribute once it's used.
        # not even really necessary so far because the metadata object
        # would be destroyed right after calling these functions.
        #
        # 02/18/08: I have just commented out the delete
        # hidden argument code... moved to end of
        # show_an_object_compact()
        #
        # 02/20/08: I'm going to make meta just point to self.
        #
        #meta['DisplayObject.arguments'] = {}
        #meta['DisplayObject.arguments']['calledByVillageSide'] = \
        #    self.calledByVillageSide
        #if self.missingFileFunc:
        #    meta['DisplayObject.arguments']['missingFileFunc'] = \
        #        self.missingFileFunc
        #if self.calledByQ2Qmsg:
        #    meta['DisplayObject.arguments']['calledByQ2Qmsg'] = \
        #        self.calledByQ2Qmsg
	#if self.callBackArg:
	#    meta['DisplayObject.arguments']['callBackArg'] = \
        #	self.callBackArg
        #if self.searchFile:
        #    meta['DisplayObject.arguments']['searchFile'] = \
        #        self.searchFile
        meta['DisplayObject.self'] = self

            

    def show_an_object_compact(self, meta):
        self._DisplayObject__hide_parameters(meta)
        if self.calledByQ2Qmsg:
            show_q2q_msg_object(self.swRoot, meta)
            return
        if self.calledByVillageSide:
            show_village_object(self.swRoot, meta)
            return
        show_server_object(meta)
        del meta['DisplayObject.self']



    def show_an_object_compact_given_details(self, meta, dataURL, auxiURL,
                                             auxiDir):
        self._DisplayObject__hide_parameters(meta)
        show_object_compact(meta, dataURL, auxiURL, auxiDir)



def scrub_js_string(str):
    str = cgi.escape(str)
    str = str.replace('\\', '\\\\')
    str = str.replace("\"","\\x22")
    str = str.replace("'","\\x27")
    str = str.replace('\r\n', '<BR>')
    str = str.replace('\n', '<BR>')
    str = str.replace('\r', '<BR>')
    return str



def scrub_html_string(str):
    str = cgi.escape(str)
    return str



def begin_print1():
    print begin_print_str()

    

def begin_print():
    begin_print1()
    print begin_print_str2()



def css_str():
    cssStr = """
<style type="text/css">
/* <![CDATA[ */

table.search, td.search
{
    border-color: #a0a0a0;
    border-style: solid;
}

table.search
{
    border-width: 0 0 1px 1px;
    border-spacing: 0;
    border-collapse: collapse;
}

td.search
{
    margin: 0;
    padding: 4px;
    border-width: 1px 1px 0 0;
}

td.search { font-family: sans-serif; }

body { font-family: sans-serif; }


/* ]]> */
</style>
"""    
    return cssStr

    

def begin_print_str():

    beginString = """
<script language="JavaScript" type="text/javascript">
<!--
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
function displayString(str) {
        var win = window.open("","win", "width=400,height=300,scrollbars,resizable,alwaysRaised");
	win.document.open("text/html", "replace");
        win.document.writeln(str);
        win.document.close();
        return false;
}
function displayString2(str) {
        var win = window.open("","win", "width=800,height=600,scrollbars,resizable,alwaysRaised");
	win.document.open("text/html", "replace");
        win.document.writeln(str);
        win.document.close();
        return false;
}
function displayString3(str) {
        var win = window.open("","win", "width=500,height=5,resizable,alwaysRaised");
	win.document.open("text/html", "replace");
        win.document.writeln(str);
        win.document.close();
        return false;
}
function displayString4(str) {
        var win = window.open("","win", "width=800,height=600,scrollbars,resizable,alwaysRaised");
	win.document.open("text/html", "replace");
        win.document.writeln(str);
        win.document.close();
        return false;
}


function launchExplorer(target,url,width,height) {
    href = window.location.href;
    if (href.substr(0,4) != "http") {
        window.open(url,"_blank","width="+width+",height="+height+",scrollbars,resizable,alwaysRaised");
        return false;
    }
        
    var http = getHTTPObject();
    http.open("GET",target+escape(url),true);
    http.onreadystatechange = function() {
        if (http.readyState == 4) {
            if (http.status == 200) {
                if (http.responseText != "True") {
                   document.getElementById("errorArea").innerHTML += http.responseText;
	           document.getElementById("errorArea").style.display = 'block';
                   // window.open(url,"_blank","width="+width+",height="+height+",scrollbars,resizable,alwaysRaised");
                }
            } else
                alert("Error: " + http.statusText);
        }
    }
    http.send(null);
    return false;
}


function createNewThumb(param) {
	var http = getHTTPObject();
	if (!confirm("Create new thumbnails " + param + " ?")) return;
	http.open("GET","/cgi-bin/CreateNewThumbDir.py?objstr="+escape(param),true);
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



-->
</script>

<span id="errorArea"></span><br>

<script language="JavaScript" type="text/javascript">
<!--Comment tag so old browsers wont see code.
	document.getElementById("errorArea").style.display = 'none';
	document.getElementById("errorArea").innerHTML = "<INPUT type=submit value='clear msg' onClick='clearErrorArea()'>";
//-- end comment for old browsers -->
</script>

"""
    return beginString



def begin_print_str2():
    beginString2 = """
<BR>
<TABLE class="search">
"""
    return beginString2



def end_print():
    print end_print_str()
    


def end_print_str():

    endString = """
</TABLE>
"""
    return endString



def is_image(fileName):

    base = os.path.basename(fileName)
    if base == 'Thumbs.db' or base == 'thumbs.db':
        return False
    
    try:
        im = Image.open(fileName)
    except:
        logging.error('is_image: failed to open image file:' + fileName)
        return False

    return True
                        


def resize_image(srcFile,dstFile,size=(THUMB_WIDTH,THUMB_HEIGHT)):
    """generate thumbnail for srcFile and store it in dstFile.
    For now the size of the thumbnail is the default value (100,128).
    Also the format is dictated by the extension of dstFile."""

    try:
        im = Image.open(srcFile)
        im.thumbnail(size,Image.ANTIALIAS)
        im.save(dstFile)
        return True
    except IOError:
        logging.error('resize_image: failed to resize: ' +
                      srcFile + ' -> ' + dstFile)
        return False



def look_for_www_subcomponent(name):
    """looks for WWW in a path name and chop off everything before and
    including it."""

    wwwPos = name.find('WWW')
    if wwwPos == -1:
        ryw.give_bad_news(
            'look_for_www_sub: name does not contain WWW component: ' +
            name, logging.error)
        return ''

    suffix = name[wwwPos + 3:]

    #logging.debug('look_for_www_subcomponent: subcomponent is at: ' + suffix)
    return suffix



def get_q2q_msg_URLs(msgRoot, meta):
    try:
        ostore = os.path.normpath(msgRoot)
        suffix = look_for_www_subcomponent(ostore)
        if not suffix:
            return (False, None, None, None)
        
        success,dataURL,auxiURL = get_URLs(meta, suffix)
        if not success:
            return (False, None, None, None)

        paths = objectstore.name_version_to_paths_aux(
            msgRoot, meta['id'], meta['version'])

        if not ryw.good_repo_paths(paths):
            logging.error('get_q2q_msg_URLs: appears to be a corrupted path: '+
                          repr(paths))
            return (False, None, None, None)

        return (True, dataURL, auxiURL, paths[2])
    except:
        ryw.give_bad_news('get_q2q_msg_URLs failed: ' + repr(meta),
                          logging.error)
        return (False, None, None, None)



def get_server_URLs(meta):
    try:
        ostore = ryw.get_objectstore(meta)
        if not ostore:
            return (False, None, None, None)

        suffix = look_for_www_subcomponent(ostore)
        if not suffix:
            return (False, None, None, None)
        
        success,dataURL,auxiURL = get_URLs(meta, suffix)
        if not success:
            return (False, None, None, None)

        paths = objectstore.name_version_to_paths_aux(
            ostore, meta['id'], meta['version'])

        if not ryw.good_repo_paths(paths):
            logging.error('get_server_URLs: appears to be a corrupted path: ' +
                          repr(paths))
            return (False, None, None, None)

        return (True, dataURL, auxiURL, paths[2])
    except:
        ryw.give_bad_news('get_server_URLs failed: ' + repr(meta),
                          logging.error)
        return (False, None, None, None)



def get_village_URLs(nihaoRoot, meta):
    try:
        vstoresuffix = os.path.join('\\repository',
                                    'RepositoryObjectStore')
        success,dataURL,auxiURL = get_URLs(meta, vstoresuffix)
        if not success:
            return (False, None, None, None)

        vstore = os.path.join(nihaoRoot, 'WWW', 'repository',
                              'RepositoryObjectStore')
                              
        paths = objectstore.name_version_to_paths_aux(vstore, meta['id'],
                                                      meta['version'])

        if not ryw.good_repo_paths(paths):
            logging.error('get_village_URLs: appears to be a corrupted path: '+
                          repr(paths))
            return (False, None, None, None)

        if not os.path.exists(paths[0]):
            logging.debug('get_village_URLs: data path does not exist: ' +
                          paths[0])
            dataURL = None
        else:
            logging.debug('get_village_URLs: data path exists: ' +
                          paths[0])

        return (True, dataURL, auxiURL, paths[2])
    except:
        ryw.give_bad_news('get_village_URLs failed: ' + repr(meta),
                          logging.error)
        return (False, None, None, None)



def get_URLs(meta, storeURLPrefix):
    try:
        paths = objectstore.name_version_to_paths_aux(
            storeURLPrefix, meta['id'], meta['version'])

        dataPath = os.path.normpath(paths[0]).replace('\\', '/')
        auxiPath = os.path.normpath(paths[2]).replace('\\', '/')
        dataPath = urllib.quote(dataPath)
        auxiPath = urllib.quote(auxiPath)

        logging.debug('get_URLs: ' + dataPath + '   ' + auxiPath)
        return (True, dataPath, auxiPath)
    except:
        ryw.give_bad_news('get_URLs: failed: ' + repr(meta), logging.error)
        return (False, None, None)



def show_server_object(meta):
    success,dataURL,auxiURL,auxiDir = get_server_URLs(meta)
    if not success:
        logging.error('get_server_URLs failed: ' + repr(meta))
        return

    show_object_compact(meta, dataURL, auxiURL, auxiDir)
    #show_object_compact(meta, None, auxiURL, auxiDir)



def show_q2q_msg_object(msgOroot, meta):
    success,dataURL,auxiURL,auxiDir = get_q2q_msg_URLs(msgOroot, meta)
    if not success:
        logging.error('get_q2q_msg_URLs failed: ' + repr(meta))
        return

    show_object_compact(meta, dataURL, auxiURL, auxiDir)



def show_village_object(nihaoRoot, meta):
    success,dataURL,auxiURL,auxiDir = get_village_URLs(nihaoRoot, meta)
    if not success:
        logging.error('get_village_URLs failed: ' + repr(meta))
        return

    show_object_compact(meta, dataURL, auxiURL, auxiDir)
    #show_object_compact(meta, None, auxiURL, auxiDir)



def show_object_compact(meta, dataURL, auxiURL, auxiDir):
    outputStr = show_object_compact_string(meta, dataURL, auxiURL, auxiDir)
    print outputStr



def show_object_compact_string(meta, dataURL, auxiURL, auxiDir,
                               staticHtml = False):
    #logging.debug('show_object_compact: ' + repr(dataURL) + ' ' + auxiURL +
    #              ' ' + repr(auxiDir))

    # ryw.give_news('show_object_compact: ' + repr(meta), logging.debug)
    
    #
    # the top level structure is simply a table,
    # of one row and three columns.
    #
    # 05/06/09: middle 
    #
    table = """
<TR id="%(id)s">
<TD class="search" width=%(thumb1_width)s
VALIGN=CENTER ALIGN=CENTER>%(thumb1)s</TD>
<TD class="search" width=720
VALIGN=CENTER ALIGN = CENTER>%(middle)s</TD>
<TD class="search" width=%(thumb2_width)s
VALIGN=CENTER ALIGN=CENTER>%(thumb2)s</TD>
</TR>
    """

    dict = {}
    dict['thumb1_width'] = str(THUMB_WIDTH)
    dict['thumb2_width'] = str(THUMB_WIDTH)

    thumbURLs = get_thumb_URLs(meta, auxiURL, auxiDir)

    dict['thumb1'] = make_thumb1_string(meta, dataURL, thumbURLs[0],
                                        thumbURLs[3])
    dict['thumb2'] = make_thumb2_string(meta, thumbURLs[1], thumbURLs[2])
    dict['middle'] = make_middle_string(meta, dataURL, auxiURL, auxiDir,
                                        staticPage = staticHtml)
    if (meta.has_key('version')):
        dict['id'] = meta['id'] + "#" + str(meta['version'])
    else:
        dict['id'] = meta['id']   
    
    return table % dict



def calledByRepository():
    try:
        a = RepositoryRoot
        return True
    except NameError:
        return False

def calledByVillage():
    try:
        a = NihaoRoot
        return True
    except NameError:
        return False



def check_list_before_popup(meta, dataURL):
    if is_list_object(meta):
        return ''
    return make_explorer_popup_string(dataURL,(POPUP_DIR_WIDTH,
                                               POPUP_DIR_HEIGHT))



def make_auto_hindi_popup(meta, dataURL, auxiURL, auxiDir):
    """modeled after make_explorer_lan_popup_string()"""
    answer = """<A HREF="%(dURL)s" onClick='return displayString4("%(popupStr)s")'><img border=0 src='/icons/h.png' width=20 height=22 TITLE="%(hindiHover)s"></A>"""

    popupStr = """<HTML><HEAD><TITLE>%(title)s</TITLE> <style type=text/css>body { font-family: sans-serif; }</style> </HEAD><BODY>%(bodyStr)s</BODY></HTML>"""
    d1 = {}
    d2 = {}
    d2['title'] = 'Automatic Hindi Translation'
    found,bodyStr = get_auto_hindi_translation_string(meta, auxiURL, auxiDir)
    d2['bodyStr'] = bodyStr

    d1['dURL'] = dataURL
    d1['popupStr'] = popupStr % d2
    #
    # Hindi: "computer Hindi translation"
    #
    #d1['hindiHover'] = '&#2325;&#2350;&#2381;&#2346;&#2381;&#2351;&#2370;&#2335;&#2352; &#2361;&#2367;&#2344;&#2381;&#2342;&#2368; &#2309;&#2344;&#2369;&#2357;&#2366;&#2342;'
    d1['hindiHover'] = 'Hindi'

    if found:
        return answer % d1
    else:
        return ''



def get_auto_hindi_translation_string(meta, auxiURL, auxiDir):
    """mirrors SelectTexts.output_text()"""

    answer = ''
    foundSomething = False
    doneOnce = False
    for type in ['title', 'description']:
        if not meta.has_key(type):
            continue
        allText = meta[type]
        textList = ryw.split_content(allText)

        for text in textList:
            md5sum = ryw.md5sum(text)

            ryw.db_print_info_browser('md5sum: ' + md5sum, 94)
            ryw.db_print_info_browser('text is: ' + text, 94)

            autoDict = google_english2hindi.GOOGLE_AUTO_DICT
            if not autoDict.has_key(md5sum):
                ryw.db_print_info_browser('not found in dict.', 94)
                continue
            else:
                foundSomething = True
                ryw.db_print_info_browser('found translation: ' +
                                          autoDict[md5sum], 94)

            translation = autoDict[md5sum]

            #no need for scrubbing because the answer from
            #Google is already scrubbed.
            #answer += ' ' + scrub_js_string(translation)

            if type == 'title':
                lead = ''
                if not doneOnce:
                    #
                    # computer Hindi translation
                    #
                    lead += '<img src=/icons/computer_bubble3.gif border=0 '+\
                            'width=358 width=72> &nbsp;&nbsp;'
                    lead += '<HR width=400 align=left>'
                    
                translation = lead + \
                              '<B><H2><font color=blue>' + translation + \
                               '</font></H2></B>'
                if not doneOnce:
                    translation = add_thumbnail_string(meta, auxiURL, auxiDir,
                                                       translation,
                                                       smallThumbs=True)
                    doneOnce = True
            else:
                translation = '<B><font size=4>' + translation + '</font></B>'

            #
            # the result of the Google translation seems to strip
            # off leading and trailing line breaks.
            # need to put it back on these boundary conditions.
            #
            answer = add_line_breaks_prefix(answer, text)
            answer += ' ' + translation
            answer = add_line_breaks_postfix(answer, text)

        answer += '<BR><BR>'

    if not foundSomething:
        #
        # Hindi: "no computer Hindi translation"
        # no, not used anymore.
        #
        answer = '<img src=/icons/no_hindi_trans.gif border=0 '+\
                 'width=376 width=92><BR><BR>' +\
                 '<img src=/icons/unhappy_computer.jpg border=0 ' + \
                 'width=184 height=123> ' 

    answer += ryw_customize.dict['footerStr']
    return (foundSomething, answer)



def add_line_breaks_postfix(answer, originalText):
    ryw.db_print_info_browser('originalText is: -' + originalText + '-', 75)
    i = len(originalText) - 1
    while (i >= 0):
        char = originalText[i]
        if not char.isspace():
            break
        if ryw.is_newline(char):
            answer += '<BR>'
            ryw.db_print_info_browser('appending line break...', 75)
        i -= 1
    return answer



def add_line_breaks_prefix(answer, originalText):
    end = len(originalText)
    for i in range(0, end):
        char = originalText[i]
        if not char.isspace():
            return answer
        if ryw.is_newline(char):
            answer += '<BR>'
    return answer



def check_list_before_lan_popup(meta, dataURL):
    #if is_list_object(meta):
    #    return ''
    return make_explorer_lan_popup_string(dataURL,(POPUP_DIR_WIDTH,
                                                   POPUP_DIR_HEIGHT))



def make_explorer_lan_popup_string(url, defaultSize=(800,600)):
    """modeled after make_detail_icon_string()"""

    name = os.getenv("REMOTE_USER")
    if name == '' or name == 'guest':
        return ''

    if not ryw.is_lan():
        return ''

    url = scrub_js_string(url)

    answer = """<A HREF="%(dURL)s" onClick='return displayString3("%(popupStr)s")'><img border=0 src='/icons/p_folder.gif' width=20 height=22 TITLE="P: drive"></A>"""

    popupStr = """<HTML><HEAD><TITLE>%(title)s</TITLE> <style type=text/css>body { font-family: sans-serif; }</style> </HEAD><BODY>%(bodyStr)s</BODY></HTML>"""
    d1 = {}
    d2 = {}
    d2['title'] = 'P: drive path name'
    bodyStr = explorer.url2path(url, True)
    bodyStr = bodyStr.replace('\\', '\\\\')
    bodyStr = bodyStr.rsplit('\\', 1)[0]
    d2['bodyStr'] = bodyStr

    d1['dURL'] = url
    d1['popupStr'] = popupStr % d2
    
    return answer % d1    



def make_explorer_popup_string(url, defaultSize=(800,600), pdrive=False):
    """when called from ryw_meta for editing thumbnail attributes,
    pdrive is set to True."""

    #
    # disable it.  it was a mistake.
    #
    pdrive=False
    
    url = scrub_js_string(url)

    ryw.db_print('make_explorer_popup_string: SERVER_ADDR: ' +
                 os.environ['SERVER_ADDR'], 46)
    ryw.db_print('make_explorer_popup_string: REMOTE_ADDR: ' +
                 os.environ['REMOTE_ADDR'], 46)
    ryw.db_print('make_explorer_popup_string: DOCUMENT_ROOT: ' +
                 os.environ['DOCUMENT_ROOT'], 46)
    ryw.db_print('make_explorer_popup_string: truncate DOCUMENT_ROOT: ' +
                 os.environ['DOCUMENT_ROOT'][2:], 46)
                 
    if os.environ['SERVER_ADDR'] == os.environ['REMOTE_ADDR']:
        answer = """
onClick='launchExplorer("%(target)s","%(url)s",%(width)s,%(height)s); return false;'
"""
        if defaultSize:
            width,height = defaultSize
        else:
            width, height = (800,600)

        if calledByRepository():
            if pdrive:
                target = "/cgi-bin/launchExplorer.py?pdrive=True&url="
            else:
                target = "/cgi-bin/launchExplorer.py?url="
        else:
            if pdrive:
                target = "/cgi-bin/repository/launchExplorer.py?pdrive=True&url="
            else:
                target = "/cgi-bin/repository/launchExplorer.py?url="

        dict = {'target':target,'url':url, 'width':width, 'height':height }

        ryw.db_print('make_explorer_popup_string: target: ' + target, 46)
        ryw.db_print('make_explorer_popup_string: url: ' + url, 46)
        
        return answer % dict
    else:
        return make_popup_string(url,defaultSize)



def make_popup_string(url,defaultSize=(800,600)):
    if defaultSize:
        width,height = defaultSize
        answer = """
 onClick='window.open("%(url)s","_blank","width=%(width)s,height=%(height)s,scrollbars,resizable,alwaysRaised"); return false;'
"""
        dict = {}
        dict['width'] = width
        dict['height'] = height
	dict['url'] = url
        return answer % dict

    answer = """
 onClick='window.open(%s,"_blank","width=800,height=600,scrollbars,resizable,alwaysRaised"); return false;'    
"""
    return answer % (url,)



def make_confirmed_popup_string(url, message, defaultSize=(400,300)):

   width,height = defaultSize
   answer = """
onClick="if (confirm('%(question)s')){window.open('%(url)s','_blank','width=%(width)s,height=%(height)s,scrollbars,resizable,alwaysRaised') }; return false;"
 """
   dict = {}
   dict['question'] = message
   dict['width'] = width
   dict['height'] = height
   dict['url'] = url
   return answer % dict



def display_selection_string(meta):
    return cgi.escape('/cgi-bin/DisplaySelection.py?objstr=' + meta['id'] + \
                      '%23' +  str(meta['version']))
    


def make_thumb1_string(meta, dataURL, t1URL, t1originalURL):
    """first thumbnail: followed by a date string."""

    #
    # if the user name is not admin, and
    # the resources file contains a line that says:
    # showCopyrightedMetaOnly=True
    # then we will not display a URL to the data.
    #
    if (should_show_copyrighted_meta_only(meta)):
        dataURL = None


    #uploadQueue:
    if is_list_object(meta):
        dataURL = display_selection_string(meta)

    ryw_meta.resize_thumbnails(meta, forced = False)
    
    dict = {}

    if t1URL and t1originalURL:
        #
        # both the big and small thumbnail versions are present.
        #
        thumb1 = """
%(breaks1)s
<A HREF="%(originalURL)s" %(popup)s>
<IMG BORDER= 0 SRC="%(picURL)s" TITLE=""></A>
<FONT SIZE=2>
%(breaks2)s
%(dateField)s
%(breaks3)s</FONT>
"""
        dict['originalURL'] = t1originalURL
        dict['popup'] = make_popup_string(t1originalURL,(800,600))
        dict['picURL'] = t1URL
        thumbShown = True

        
    elif t1URL and dataURL:
        #
        # only the small thumbnail is present, and data is present.
        #
        thumb1 = """
%(breaks1)s
<A HREF="%(dataURL)s" %(popup)s>
<IMG BORDER= 0 SRC="%(picURL)s" TITLE="data"></A>
<FONT SIZE=2>
%(breaks2)s
%(dateField)s
%(breaks3)s</FONT>
"""
        dict['dataURL'] = dataURL
        dict['popup'] = check_list_before_popup(meta, dataURL)
        dict['picURL'] = t1URL
        thumbShown = True

        
    elif t1URL:
        #
        # only the small thumbnail, no large thumbnail, no data.
        #
        thumb1 = """
<IMG BORDER=0 SRC="%(picURL)s"><br><br><FONT SIZE=2>%(dateField)s</FONT>
"""
        dict['picURL'] = t1URL
        thumbShown = True


    elif dataURL:
        #
        # only data, no thumbnail of any size.
        #
        thumb1 = """
%(breaks1)s
<A HREF="%(dataURL)s" %(popup)s>
<IMG BORDER= 0 SRC="%(picURL)s" TITLE="data"></A>
<FONT SIZE=2>
%(breaks2)s
%(dateField)s
%(breaks3)s</FONT>
"""
        dict['dataURL'] = dataURL
        dict['popup'] = check_list_before_popup(meta, dataURL)
        dict['picURL'] = '/icons/folder.open.gif'
        thumbShown = False


    else:
        #
        # no data, no thumbnail of any size.
        #
        thumb1 = """
<IMG BORDER=0 SRC="%(picURL)s"><br><br><FONT SIZE=2>%(dateField)s</FONT>
"""
        dict['picURL'] = '/icons/broken.gif'
        thumbShown = False
        

    if meta.has_key('upload_datetime'):
        if not thumbShown:
            dict['breaks1'] = '&nbsp;<br>'
            dict['breaks2'] = '<br>'
            dict['breaks3'] = '&nbsp;<br>'
        else:
            dict['breaks1'] = ''
            dict['breaks2'] = ''
            dict['breaks3'] = ''
        uploadTime = eval(meta['upload_datetime'])
        dateString = uploadTime.strftime('%d/%m/%y')
        dict['dateField'] = dateString
    else:
        dict['dateField'] = ''
        
    return thumb1 % dict



def NOT_USED_make_thumb1_string(meta, dataURL, t1URL, t1originalURL):
    """first thumbnail: followed by a date string."""

    dict = {}
    
    if dataURL:
        thumb1 = """
%(breaks1)s
<A HREF="%(dataURL)s" %(popup)s><IMG BORDER= 0 SRC="%(picURL)s" TITLE="data"></A>
<FONT SIZE=2>
%(breaks2)s
%(dateField)s
%(breaks3)s</FONT>
"""
        defaultPic = '/icons/folder.open.gif'
        dict['dataURL'] = dataURL
        dict['popup'] = make_explorer_popup_string(dataURL,(POPUP_DIR_WIDTH, POPUP_DIR_HEIGHT))
    else:
        thumb1 = """
<IMG BORDER=0 SRC="%(picURL)s"><br><br><FONT SIZE=2>%(dateField)s</FONT>
"""
        defaultPic = '/icons/broken.gif'

    if t1URL == None:
        thumbShown = False
        dict['picURL'] = defaultPic
    else:
        thumbShown = True
        dict['picURL'] = t1URL

    if meta.has_key('upload_datetime'):
        if not thumbShown:
            dict['breaks1'] = '&nbsp;<br>'
            dict['breaks2'] = '<br>'
            dict['breaks3'] = '&nbsp;<br>'
        else:
            dict['breaks1'] = ''
            dict['breaks2'] = ''
            dict['breaks3'] = ''
        uploadTime = eval(meta['upload_datetime'])
        dateString = uploadTime.strftime('%d/%m/%y')
        dict['dateField'] = dateString
    else:
        dict['dateField'] = ''
        
    return thumb1 % dict



def make_thumb2_string(meta, t2URL, t2originalURL):
    """second thumbnail, followed by an author name."""
    dict = {}
    if t2URL:
        thumb2Shown = True
        dict['picURL'] = t2URL
        if t2originalURL:
            thumb2 = """
<A HREF="%(originalURL)s" %(popup)s>
<IMG BORDER=0 SRC="%(picURL)s" TITLE="author"></A>
<FONT SIZE=2><BR>%(author)s</FONT>
"""
            dict['originalURL'] = t2originalURL
            dict['popup'] = make_popup_string(t2originalURL,(800,600))
        else:
            thumb2 = """
<IMG BORDER=0 SRC="%(picURL)s" TITLE="author">
<FONT SIZE=2><BR>%(author)s</FONT>
"""
    else:
        thumb2Shown = False
        thumb2 = """
<IMG BORDER=0 SRC="/icons/buddy2.gif" TITLE="author">
<FONT SIZE=2><BR>%(author)s</FONT>
"""

    author = ''
    if meta.has_key('author_name'):
        author += truncate_string(meta['author_name'], 30)
    hindiAuthor = ryw_hindi.attr(meta, 'author_name')
    #logging.debug('make_thumb2_string: hindiAuthor: ' + hindiAuthor)
    if hindiAuthor:
        author += '&nbsp;' + ryw_hindi.truncate_size3_html(hindiAuthor, 30)

    if author:
        dict['author'] = author
    elif thumb2Shown:
        dict['author'] = ''
    else:
        dict['author'] = 'author unknown '
        dict['author'] += ryw_hindi.size3_html_key('author_unknown')
            
    return thumb2 % dict



def check_hidden_parameter(meta):
    if not meta.has_key('DisplayObject.self'):
        raise NameError('ryw_view.check_hidden_parameter: no parameter')



def make_middle_string(meta, dataURL, auxiURL, auxiDir, staticPage = False):
    """three rows: first is the title box.
    second is the description.
    third is the other attributes."""

    dict = {}
    middle = """
<TABLE WIDTH=100%% BORDER=0>
<TR><TD VALIGN=TOP ALIGN=LEFT>%(titleBox)s</TD></TR>
<TR><TD VALIGN=TOP ALIGN=LEFT><FONT SIZE=2>%(descStr)s</FONT></TD></TR>
<TR><TD VALIGN=TOP ALIGN=LEFT>%(attrStr)s</TD></TR>
</TABLE>
"""


    containerInfo = []
    if not staticPage and calledByRepository() and \
        meta.has_key('DisplayObject.self'):
        reverseLists = meta['DisplayObject.self'].reverseLists
        if reverseLists:
            containee = meta['id'] + '#' + str(meta['version'])
            containerInfo = reverseLists.lookup(containee)

            
    dict['titleBox'] = make_title_box(meta, dataURL, auxiURL, auxiDir,
                                      containers = containerInfo,
                                      staticHtml = staticPage)

    description = ''
    if meta.has_key('description'):
        description += truncate_string(meta['description'], 340)

    hindiDesc = ryw_hindi.attr(meta, 'description')
    if hindiDesc:
        description += '&nbsp; ['
        description += ryw_hindi.truncate_size3_html(hindiDesc, 340)
        description += ']'

    if description == '':
        description = '(no description)'

    dict['descStr'] = BLANKS+description
    dict['attrStr'] = make_other_attr_string(meta,
                                             containers = containerInfo,
                                             staticHtml = staticPage)

    #dict['leftBox']  = make_left_box(meta, dataURL, auxiURL, auxiDir)
    #dict['rightBox'] = make_right_box(meta, auxiURL, auxiDir)

    return middle % dict



def NOTUSED_make_left_box(meta, dataURL, auxiURL, auxiDir):
    """the left sub-column: title sits on top of description, etc."""

    dict = {}
    left = """
<TABLE WIDTH=100%% BORDER=0>
<TR>
<TD VALIGN=TOP ALIGN=LEFT>
%(title)s
</TD>
</TR>
<TR>
<TD><FONT SIZE=2>
%(description)s
</FONT>
</TD>
</TR>
</TABLE>
"""

    #dict['title'] = make_title_string(meta, dataURL)
    dict['title'] = make_title_box(meta, dataURL, auxiURL, auxiDir)

    if meta.has_key('description'):
        description = truncate_string(meta['description'], 266)
    else:
        description = '(no description)'

    dict['description'] = BLANKS+description
    dict['description'] += make_other_attr_string(meta)
    
    return left % dict



def make_title_box(meta, dataURL, auxiURL, auxiDir, containers=[],
                   staticHtml=False):

    dict = {}
    titleBox = """
<TABLE WIDTH=100%% BORDER=0>
<TR><TD VALIGN=TOP ALIGN=LEFT %(bgcolor)s>
<B><FONT SIZE=2>%(titleStr)s</FONT></B></TD>
<TD VALIGN=TOP ALIGN=RIGHT %(bgcolor)s>%(iconStr)s</TD></TR>
</TABLE>
"""
    if is_list_object(meta):
        #dict['bgcolor'] = 'BGCOLOR="f0d0ff"'
        dict['bgcolor'] = 'BGCOLOR="c3d9ff"'
    else:
        dict['bgcolor'] = ''
    dict['titleStr'] = make_title_string(meta, dataURL)
    dict['iconStr'] = make_icon_string(meta, dataURL, auxiURL, auxiDir,
                                       containerInfo = containers,
                                       staticPage = staticHtml)
    return titleBox % dict

    

def make_icon_string(meta, dataURL, auxiURL, auxiDir, containerInfo=[],
                     staticPage=False):
    """the right box contains a bunch of icons."""
    dict = {}
    right = """
%(reqIcon)s
%(typeIcons)s
%(listIcon)s
%(versionsIcon)s
%(excerptIcons)s
%(detailIcon)s
%(autoHindiIcon)s
%(pDriveIcon)s
"""
    dict['reqIcon'] = make_request_icon_string(meta, dataURL)
    dict['typeIcons'] = make_type_icon_string(meta)
    dict['listIcon'] = make_list_icon_string(meta, dataURL)
    dict['pDriveIcon'] = check_list_before_lan_popup(meta, dataURL)
    dict['autoHindiIcon'] = make_auto_hindi_popup(meta, dataURL,
                                                  auxiURL, auxiDir)
    dict['excerptIcons'] = make_excerpt_icon_string(meta, auxiURL, auxiDir)
    dict['detailIcon'] = make_detail_icon_string(meta, auxiURL, auxiDir,
                                                 containers = containerInfo,
                                                 staticHtml = staticPage)
    dict['versionsIcon'] = make_versions_icon_string(meta,
                                                     staticHtml = staticPage)

    return right % dict



def add_list_item(meta, attributeName, attributeNamePrint, partialStr):
    if meta.has_key(attributeName):
        partialStr += '<LI><B>' + attributeNamePrint+ ' </B>'
        partialStr += scrub_js_string(meta[attributeName])
        return partialStr
    return partialStr



#uploadQueue:
def add_set_item(meta, attrName, attrPrintName, partialStr):
    if meta.has_key(attrName):
        partialStr += '<LI><B>' + attrPrintName + ' </B>'
        for val in meta[attrName]:
            partialStr += scrub_js_string(val)
            return partialStr
    return partialStr



def add_list_item_hindi(meta, attributeName,
                        attributeNamePrintEnglishKey, partialStr):
    hindiAttr = ryw_hindi.attr(meta, attributeName)
    if hindiAttr == '':
        return partialStr

    partialStr += '<LI><B>' + \
        ryw_hindi.html_key(attributeNamePrintEnglishKey) + ': </B>'
    partialStr += ryw_hindi.html(scrub_js_string(hindiAttr))
    return partialStr
    


def add_list_single_item(meta, attributeName, attributeNamePrint, partialStr):
    if meta.has_key(attributeName) and meta[attributeName] != 'unknown':
        partialStr += '<LI><B>' + attributeNamePrint+ ' </B>'
        partialStr += scrub_js_string(meta[attributeName].replace('_', ' '))
        return partialStr
    return partialStr



def add_list_duration(meta, mediaAttrStr):
    durStr = get_duration_string(meta)
    if not durStr:
        return mediaAttrStr
    
    mediaAttrStr += '<LI><B>Duration: </B>'
    hours = meta['time_length'][0]
    if hours != '0' and hours != '00':
        mediaAttrStr += unit_plurals(hours, 'hour')
        
    minutes = meta['time_length'][1]
    mediaAttrStr += unit_plurals(minutes, 'minute')

    if not meta.has_key('time_length_seconds'):
        return mediaAttrStr

    seconds = meta['time_length_seconds']
    if seconds == '0' or seconds == '00':
        return mediaAttrStr
    mediaAttrStr += unit_plurals(seconds, 'second')
    return mediaAttrStr



def unit_plurals(numStr, unitName):
    if numStr == '0' or numStr == '1':
        return numStr + ' ' + unitName + ' '
    return numStr + ' ' + unitName + 's '



def add_list_list_item(meta, attributeName, attributeNamePrint, partialStr):
    if not meta.has_key(attributeName) or not meta[attributeName]:
        return partialStr
    partialStr += '<LI><B>' + attributeNamePrint + ' </B>'
    items = meta[attributeName]
    first = True
    for item in items:
        item = str(item)
        if item == 'unknown':
            continue
        item = item.replace('_', ' ')
        if first:
            first = False
        else:
            partialStr += ', '
        item = scrub_js_string(item)
        partialStr += item
    return partialStr



def add_age(meta, partialStr):
    if not meta.has_key('age') or len(meta['age']) != 2:
        return partialStr
    partialStr += '<LI><B>Applicable age: </B> from '
    partialStr += str(meta['age'][0])
    partialStr += ' to ' + str(meta['age'][1])
    return partialStr



def add_bytes1(meta, attrStr):
    if not meta.has_key('bytes'):
        return attrStr
    
    bytes = meta['bytes']
    bstr = str(bytes)
    if bstr.find('L'):
        bstr = bstr.replace('L', '')
    if bytes < 1024:
        attrStr += bstr + 'B'
    elif bytes < 1024 * 1024:
        attrStr += str(bytes / 1024).replace('L', '') + 'KB'
    else:
        attrStr += str(bytes / 1024 / 1024).replace('L', '') + 'MB'
    return attrStr



def add_bytes2(meta, attrStr):
    if not meta.has_key('bytes'):
        return attrStr

    attrStr += '<LI><B>Bytes: </B>'
    attrStr = add_bytes1(meta, attrStr)
    return attrStr



def add_single_unchanged(meta, attributeName, attributeNamePrint, partialStr):
    if not meta.has_key(attributeName):
        return partialStr
    partialStr += '<LI><B>' + attributeNamePrint + ' </B>'
    partialStr += scrub_js_string(meta[attributeName])
    return partialStr    
    


def add_uploadtime(meta, partialStr):
    if not meta.has_key('upload_datetime'):
        return partialStr
    try:
        timeStr = format_date_time_str(meta['upload_datetime'])
        partialStr += '<LI><B>Upload date and time: </B>'
        partialStr += timeStr
        return partialStr
    except:
        logging.error('add_uploadtime: failed ' + repr(meta))
        return partialStr



def format_date_time_str(dateTimeStr):
    timeRepr = eval(dateTimeStr)
    outputStr = timeRepr.strftime('%I:%M %p, %A, %d/%m/%Y ')
    return outputStr



def add_other_times(meta, partialStr):
    if meta.has_key('upload_datetime_real'):
        timeStr = format_date_time_str(meta['upload_datetime_real'])
        partialStr += '<LI><B>Upload date and time (real): </B>'
        partialStr += timeStr

    if meta.has_key('change_datetime') and meta['change_datetime'] != None:
        timeStr = format_date_time_str(meta['change_datetime'])
        partialStr += '<LI><B>Change date and time: </B>'
        partialStr += timeStr

    return partialStr



def add_objid_version(meta, partialStr):
    partialStr += '<LI><B>Object ID and version: </B>'

    if (should_show_copyrighted_meta_only(meta)):
        partialStr += '(not shown)'
    else:
        partialStr += scrub_js_string(meta['id'])
        if meta.has_key('version'):
            partialStr += '#' + str(meta['version'])
    return partialStr



def add_alias(meta, partialStr):
    if not meta.has_key('content_alias'):
        return partialStr
    partialStr += '<LI><B>Content alias: </B>'
    partialStr += scrub_js_string(meta['content_alias'])
    return partialStr



def add_chapter_number(meta, partialStr):
    if not meta.has_key('chapter_number'):
        return partialStr
    partialStr += '<LI><B>Chapter number: </B>'
    partialStr += scrub_js_string(meta['chapter_number'])
    return partialStr



def add_related(meta, partialStr):
    if not meta.has_key('related_content'):
        return partialStr
    partialStr += '<LI><B>Related content: </B>'
    partialStr += scrub_js_string(meta['related_content'])
    return partialStr



def add_thumbnail_string(meta, auxiURL, auxiDir, partialStr,
                         smallThumbs=False):
    if not os.path.exists(auxiDir):
        return partialStr

    if smallThumbs:
        tDir = os.path.join(auxiDir, 'thumbs_scaled')
    else:
        tDir = os.path.join(auxiDir, 'thumbnails')
    if not os.path.exists(tDir):
        return partialStr

    try:
        tNames = os.listdir(tDir)
        if len(tNames) == 0:
            return partialStr

        for tName in tNames:
            tPath = os.path.join(tDir, tName)
            if not is_image(tPath):
                continue
            tName = scrub_js_string(tName)
            if smallThumbs:
                tURL = glue_auxi_URL(auxiURL, 'thumbs_scaled', tName)
            else:
                tURL = glue_auxi_URL(auxiURL, 'thumbnails', tName)
            urlStr = """&nbsp;&nbsp;<IMG SRC=\\x22%(tURL)s\\x22 BORDER=0>"""
            dict = {}
            dict['tURL'] = tURL

            partialStr += urlStr % dict

        return partialStr
    except:
        logging.error('add_thumbnail_string: failed: ' + repr(meta) + ' ' +
                      auxiURL + ' ' + auxiDir)
        return partialStr



def show_obj_cgi_str(title, objstr, staticPage = False):
    if staticPage:
        return title
    str2 = """<A HREF=%(showCgi)s>%(titleStr)s</A>"""
    dict = {}
    dict['showCgi'] = '/cgi-bin/DisplayObject.py?objstr=' + \
                      urllib.quote(objstr)
    dict['titleStr'] = title
    return str2 % dict



#
# not used any more.
#
def show_chapter_edit_cgi_str(title, objstr, staticPage = False):
    """10/21/08: called by DisplaySelection.py.
    to displaying a link for editing the chapter list.
    modeled after show_obj_cgi_str()"""
    
    if staticPage:
        return ''
    
    str2 = """<A HREF=%(showCgi)s>%(titleStr)s</A>"""
    dict = {}
    dict['showCgi'] = '/cgi-bin/ChapterListForm.py?objstr=' + \
                      urllib.quote(objstr)
    dict['titleStr'] = 'edit chapters'
    return str2 % dict



def make_detail_icon_string(meta, auxiURL, auxiDir, containers=[],
                            staticHtml=False):

    detailIconStr = """<A HREF="#" onClick='return displayString2("%(popupStr)s")'><IMG SRC="/icons/index.gif" TITLE="show details" BORDER=0 width=20 height=22></A>"""
    popupStr = """<HTML><HEAD><TITLE>%(title)s</TITLE> <style type=text/css>body { font-family: sans-serif; }</style> </HEAD><BODY>%(bodyStr)s %(footerStr)s</BODY></HTML>"""

    d1 = {}
    d2 = {}

    t = ''
    if meta.has_key('title'):
        t += scrub_js_string(meta['title'])
    hindiTitle = scrub_js_string(ryw_hindi.attr(meta, 'title'))
    if hindiTitle:
        t += '&nbsp; [' + ryw_hindi.html(hindiTitle) + ']'

    if t == '':
        d2['title'] = 'Details'
    else:
        d2['title'] = t

    d2['title2'] = show_obj_cgi_str(
        d2['title'], meta['id'] + '#' + str(meta['version']),
        staticPage = staticHtml)

    bodyStr  = '<H2>' + d2['title2'] + '</H2>'
    bodyStr += '<UL>'

    bodyStr = add_list_item(meta, 'description', 'Description:', bodyStr)
    bodyStr = add_list_item_hindi(meta, 'description', 'description', bodyStr)
    bodyStr = add_list_item(meta, 'students', 'Students concerned:', bodyStr)
    bodyStr = add_list_item_hindi(meta, 'students', 'students_concerned',
                                  bodyStr)
    bodyStr = add_list_list_item(meta, 'subjects', 'Subjects:', bodyStr)
    bodyStr = add_list_single_item(meta, 'content_type', 'Content type:',
                                   bodyStr)
    bodyStr = add_list_list_item(meta, 'languages', 'Language(s):', bodyStr)
    bodyStr = add_list_single_item(meta, 'class', 'For class:', bodyStr)
    bodyStr = add_age(meta, bodyStr)
    bodyStr = add_list_list_item(meta, 'media', 'Media type:', bodyStr)
    bodyStr = add_list_duration(meta, bodyStr)

    bodyStr = add_bytes2(meta, bodyStr)    
    bodyStr = add_list_item(meta, 'author_name', 'Teacher/author:', bodyStr)
    bodyStr = add_list_item_hindi(meta, 'author_name', 'teacher_author',
                                  bodyStr)

    if (not should_show_copyrighted_meta_only(meta)):
        bodyStr = add_list_item(meta, 'uploaded_by_name',
                                'Uploaded by:', bodyStr)
        bodyStr = add_list_item_hindi(meta, 'uploaded_by_name',
                                      'uploaded_by', bodyStr)
        bodyStr = add_single_unchanged(meta, 'creator',
                                       'Uploaded by (account name):', bodyStr)
        
    bodyStr = add_uploadtime(meta, bodyStr)
    bodyStr = add_other_times(meta, bodyStr)
    bodyStr = add_objid_version(meta, bodyStr)
    #bodyStr = add_single_unchanged(meta, 'path', 'View path:', bodyStr)
    bodyStr = add_alias(meta, bodyStr)
    bodyStr = add_chapter_number(meta, bodyStr)
    bodyStr = add_related(meta, bodyStr)

    if containers != [] and not staticHtml:
        bodyStr += ReverseLists.container_detail_string(containers)
        #ryw.db_print('make_detail_icon_string: ' +
        #             ReverseLists.container_detail_string(containers), 9)
        
    if not ryw_ffmpeg.has_resolution(meta):
        bodyStr = add_list_single_item(
            meta, 'video_resolution',
            'Video resolution (width in pixels):', bodyStr)
    bodyStr = ryw_ffmpeg.add_attrs_to_string(meta, bodyStr)
    
    bodyStr = add_list_list_item(meta, 'show', 'Show:', bodyStr)
    bodyStr = add_list_list_item(meta, 'cache', 'Cache:', bodyStr)
    bodyStr = add_set_item(meta, 'sys_attrs', 'System attributes:', bodyStr)

    bodyStr += '</UL>'

    bodyStr = add_thumbnail_string(meta, auxiURL, auxiDir, bodyStr)
    
    d2['bodyStr'] = bodyStr
    d2['footerStr'] = ryw_customize.dict['footerStr']
    d1['popupStr'] = popupStr % d2

    return detailIconStr % d1



def make_type_icon_string(meta):

    if not meta.has_key('media') or not meta['media']:
        return ''

    mediaSet = set(meta['media'])
    videoSet = set(ryw_upload.POSSIBLE_VIDEO_SUBTYPES)
    isVideo = len(videoSet - mediaSet) != len(videoSet)
    #logging.debug('make_type_icon_string: ' + repr(videoSet - mediaSet) +
    #              ' ' + repr(videoSet))

    jsPopupStr = """
<A HREF="#" onClick='return displayString("%(popupStr)s")'>
"""    

    iconStr = ''

    if isVideo:
        iconStr = jsPopupStr + """
<IMG SRC="/icons/movie.gif" BORDER=0 TITLE="video attributes"></A>
"""

    isAudio = (not isVideo) and ('audio_without_video' in mediaSet)

    if isAudio:
        iconStr += jsPopupStr + """
<IMG SRC="/icons/sound1.gif" BORDER=0 TITLE="audio attributes"></A>
"""

    dict = {}
    if iconStr:
        mediaAttrStr = '<H3>Media Attributes</H3><UL>'

        mediaAttrStr = add_list_list_item(meta, 'media', 'Media type:', \
                                          mediaAttrStr)
        mediaAttrStr = add_list_duration(meta, mediaAttrStr)

        if not ryw_ffmpeg.has_resolution(meta):
            mediaAttrStr = add_list_single_item(meta, 'video_resolution',
                'Video resolution (width in pixels):',
                mediaAttrStr)

        mediaAttrStr = ryw_ffmpeg.add_attrs_to_string(meta, mediaAttrStr)

        mediaAttrStr += '</UL>'
        mediaAttrStr = '<HTML><BODY>' + mediaAttrStr + '</BODY></HTML>'
        dict['popupStr'] = mediaAttrStr
        
    return iconStr % dict



def excerpt_exists(auxiURL, auxiDir):
    if not auxiDir:
        return None
    if not os.path.exists(auxiDir):
        return None
    subDir = os.path.join(auxiDir, 'excerpts')
    if not os.path.exists(subDir):
        return None
    return subDir



def make_excerpt_icon_str(subDir, auxiURL, auxiDir):
    #isLan = ryw.is_lan()
    isLan = False
    dict = {}
    eString = """
<A HREF="%(eURL)s" %(popup)s><IMG SRC="%(iconImg)s" BORDER=0 TITLE="excerpts"></A>"""
    dict['eURL'] = auxiURL + '/excerpts/'
    dict['popup'] = make_explorer_popup_string(dict['eURL'],(POPUP_DIR_WIDTH, POPUP_DIR_HEIGHT),pdrive=isLan)
    if isLan:
        dict['iconImg'] = '/icons/p_e2.gif'
    else:
        dict['iconImg'] = '/icons/e2.gif'
    return eString % dict
        


def make_excerpt_icon_string(meta, auxiURL, auxiDir):
    try:
        subDir = excerpt_exists(auxiURL, auxiDir)
        if not subDir:
            return ''
        aNames = os.listdir(subDir)
        if len(aNames) == 0:
            return ''
        return make_excerpt_icon_str(subDir, auxiURL, auxiDir)
    except:
        ryw.give_bad_news('make_excerpt_icon_string: failed: ' +
                          auxiURL + ' ' + auxiDir, logging.critical)
        return ''



#uploadQueue:
def make_list_icon_string(meta, dataURL):
    #isLan = ryw.is_lan()
    isLan = False
    name = os.getenv("REMOTE_USER")
    if name == '' or name == 'guest':
        return ''
    if not is_list_object(meta):
        return ''
    dict = {}
    lString = """
<A HREF="%(lURL)s" %(popup)s><IMG SRC="%(iconImg)s" BORDER=0 TITLE="list file"></A>"""
    dict['lURL'] = dataURL
    dict['popup'] = make_explorer_popup_string(dataURL, (POPUP_DIR_WIDTH, POPUP_DIR_HEIGHT), pdrive=isLan)
    if isLan:
        dict['iconImg'] = '/icons/p_image3.gif'
    else:
        dict['iconImg'] = '/icons/image3.gif'
    return lString % dict



def make_versions_icon_string(meta, staticHtml=False):
    if staticHtml:
        return ''
    if not meta.has_key('DisplayObject.self'):
        return ''
    displaySelf = meta['DisplayObject.self']
    if not displaySelf.searchFile:
        return ''
    searchFile = displaySelf.searchFile

    objID = meta['id']
    numVers = searchFile.number_of_versions(objID)
    ryw.db_print('make_versions_icon_string: objID: ' + objID +
                 ', number of versions: ' + str(numVers), 31)
    if numVers < 2:
        return ''

    allVersIconStr = """<A
href="%s"><IMG SRC="/icons/script.gif" BORDER=0
title="show all versions"></A>
"""
    allVersIconStr = allVersIconStr % \
                     ("/cgi-bin/DisplayVersions.py?objid=" + objID)

    return allVersIconStr



def make_request_icon_string(meta, dataURL):

    if not meta.has_key('DisplayObject.self'):
        return ''

    displaySelf = meta['DisplayObject.self']
    
    if not displaySelf.missingFileFunc:
        return ''

    searchFile = displaySelf.searchFile

    try:
        calledByVillageSide = displaySelf.calledByVillageSide
        reqFunc = displaySelf.missingFileFunc

        if displaySelf.callBackArg:
	    callBackArg = displaySelf.callBackArg
        else:
            callBackArg = None

	if not callBackArg:
            reqStr = reqFunc(meta, calledByVillageSide, dataURL,
                             searchFile=searchFile)
	else:
	    reqStr = reqFunc(meta, calledByVillageSide, dataURL,
                             callBackArg, searchFile = searchFile)
    except:
        ryw.give_bad_news(
            'make_request_icon_string: failed to invoke function.',
            logging.critical)
        reqStr = ''

    #logging.debug('make_request_icon_string: ' + reqStr)
    return reqStr



def prefix_zero(numStr):
    if numStr in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        return '0' + numStr

    return numStr



def get_duration_string(meta):
    if not meta.has_key('time_length'):
        return ''
    
    duration = meta['time_length']
    hours = duration[0]
    minutes = duration[1]
    if hours != 'unknown' and hours != 'more' and minutes != 'unknown':
        hm = prefix_zero(hours) + ':' + prefix_zero(minutes)
    else:
        return ''

    if meta.has_key('time_length_seconds'):
        hms = hm + ':' + prefix_zero(meta['time_length_seconds'])
        return hms

    return hm



def make_other_attr_string(meta, containers=[], staticHtml=False):

    contentTypeStr = ''
    if meta.has_key('content_type') and meta['content_type'] != 'unknown':
        contentTypeStr = meta['content_type']
        contentTypeStr = contentTypeStr.replace('_', ' ')
        contentTypeStr = scrub_html_string(contentTypeStr)

    subjectStr = ''
    if meta.has_key('subjects'):
        subjects = meta['subjects']
        subject = subjects[0]
        if len(subjects) > 1:
            subject += '...'
        subjectStr = subject.replace('_', ' ')
        subjectStr = scrub_html_string(subjectStr)

    attrStr = ''
    if contentTypeStr and subjectStr:
        attrStr = contentTypeStr + ': ' + subjectStr + ', '
    elif contentTypeStr:
        attrStr = contentTypeStr + ', '
    elif subjectStr:
        attrStr = subjectStr + ', '


    if meta.has_key('languages'):
        languages = meta['languages']
        if len(languages) > 1:
            for lan in languages:
                if lan == 'unknown':
                    continue
                if (lan == 'English') or (lan == 'english'):
                    continue
                attrStr += 'language: ' + lan + '..., '
                break
        else:
            lan = languages[0]
            if lan != 'unknown':
                attrStr += 'language: ' + lan + ', '                    
    

    attrStr = add_bytes1(meta, attrStr)
    attrStr += ', '

    durStr = get_duration_string(meta)
    if durStr:
        attrStr += durStr + ', '

    if meta.has_key('class'):
        forClass = meta['class']
        if forClass != 'unknown':
            forClass = scrub_html_string(forClass)
            attrStr += 'for class: ' + forClass + ', '

    if meta.has_key('chapter_number'):
        chapter = meta['chapter_number']
        chapter = scrub_html_string(chapter)
        attrStr += 'chapter: ' + chapter + ', '

    if meta.has_key('content_alias'):
        alias = meta['content_alias']
        alias = scrub_html_string(alias)
        attrStr += 'alias: ' + alias + ', '

    if containers != [] and not staticHtml:
        attrStr += ReverseLists.container_string(containers)
        
    if (meta.has_key('creator') and
        (not should_show_copyrighted_meta_only(meta))):
        uploader = meta['creator']
        uploader = scrub_html_string(uploader)
        attrStr += ' from: ' + uploader + ', '

    #logging.debug('make_other_attr_string: attrStr is ' + attrStr + '|')

    attrStr = attrStr.rstrip()
    attrStr = attrStr.rstrip(',')
    attrStr += '.'

    return '<I><FONT SIZE=2>' + BLANKS + attrStr + '</FONT></I>'



def make_title_string(meta, dataURL):

    #
    # if the user name is not admin, and
    # the resources file contains a line that says:
    # showCopyrightedMetaOnly=True
    # then we will not display a URL to the data.
    #
    if (should_show_copyrighted_meta_only(meta)):
        dataURL = None

    #uploadQueue:
    if is_list_object(meta):
        #logging.debug('make_title_string: is list: ' + repr(meta))
        dataURL = display_selection_string(meta)
    
    dict = {}
    dict['lan_popup_str'] = ''
    
    if dataURL:
        titleStr = """
<A HREF="%(dURL)s" TITLE="data" %(popup)s>%(title)s</A>&nbsp;&nbsp;
%(hindi_title_URL)s %(lan_popup_str)s
"""
        dict['dURL'] = dataURL
        dict['popup'] = check_list_before_popup(meta, dataURL)
        #dict['lan_popup_str'] = check_list_before_lan_popup(meta, dataURL)
        dict['lan_popup_str'] = ''
    else:
        titleStr = """
<U>%(title)s</U> &nbsp;&nbsp; %(hindi_title)s
"""

    if meta.has_key('title'):
        dict['title'] = truncate_string(meta['title'], 80)
    else:
        dict['title'] = '&nbsp;'

    dict['hindi_title_URL'] = ''
    dict['hindi_title'] = ''

    hindiTitle = ryw_hindi.attr(meta, 'title')
    if hindiTitle:
        if dataURL:
            hStr = """
<A HREF="%(dURL)s" TITLE="data" style="text-decoration: none" %(popup)s>%(hindi_title)s</A>
"""
            d2 = {}
            d2['dURL'] = dataURL
            d2['popup'] = check_list_before_popup(meta, dataURL)
            d2['hindi_title'] = '[' + ryw_hindi.truncate_size4_bold_html(
                hindiTitle, 80) + ']'
            dict['hindi_title_URL'] = hStr % d2
        else:
            dict['hindi_title'] = '[' + ryw_hindi.truncate_size4_bold_html(
                hindiTitle, 80) + ']'

    return titleStr % dict



def glue_auxi_URL(auxiURL, subDirName, fileName, checkIt = True):
    if checkIt and not fileName:
        return None
    return auxiURL + '/' + subDirName + '/' + fileName



def get_thumb_URLs(meta, auxiURL, auxiDir):
    try:
        if not auxiDir:
            return (None, None, None, None)
        subDirName = 'thumbs_scaled'
        if not os.path.exists(auxiDir):
            return (None, None, None, None)
        subDir = os.path.join(auxiDir, subDirName)
        if not os.path.exists(subDir):
            return (None, None, None, None)
        aNames = os.listdir(subDir)
        if len(aNames) == 0:
            return (None, None, None, None)

        aDict = {}
        for aName in aNames:
            aDict[aName[0]] = aName

        thumb1Name = None
        thumb2Name = None
        thumb3Name = None
        thumb4Name = None

        if aDict.has_key('1'):
            thumb1Name = aDict['1']
        elif aDict.has_key('3'):
            thumb1Name = aDict['3']
        elif aDict.has_key('4'):
            thumb1Name = aDict['4']

        if aDict.has_key('2'):
            thumb2Name = aDict['2']

        if thumb2Name:
            bigthumb2path = os.path.join(auxiDir, 'thumbnails', thumb2Name)
            if os.path.exists(bigthumb2path):
                thumb3Name = thumb2Name

        if thumb1Name:
            bigthumb1path = os.path.join(auxiDir, 'thumbnails', thumb1Name)
            if os.path.exists(bigthumb1path):
                thumb4Name = thumb1Name

        thumb1URL = glue_auxi_URL(auxiURL, 'thumbs_scaled', thumb1Name)
        thumb2URL = glue_auxi_URL(auxiURL, 'thumbs_scaled', thumb2Name)
        thumb3URL = glue_auxi_URL(auxiURL, 'thumbnails',    thumb3Name)
        thumb4URL = glue_auxi_URL(auxiURL, 'thumbnails',    thumb4Name)

        logging.debug('get_thumb_URLs: returning: ' +
                      repr(thumb1URL) + ' ' + repr(thumb2URL) + ' ' +
                      repr(thumb3URL) + ' ' + repr(thumb4URL))
        
        return (thumb1URL, thumb2URL, thumb3URL, thumb4URL)
    except:
        ryw.give_bad_news('get_thumb_URLs: failed: ' +
                          repr(auxiURL) + ' ' + repr(auxiDir) + ' ' +
                          subDirName, logging.critical)
        return (None, None, None, None)



def truncate_string(str, limit):
    """adds a bunch of elipses if truncated."""
    if len(str) > limit:
        ans = str[:limit] + '...'
    else:
        ans = str
    return scrub_html_string(ans)



def truncate_string2(str, limit):
    if len(str) > limit:
        ans = (scrub_html_string(str[:limit]), '...')
    else:
        ans = (scrub_html_string(str), '')
    return ans
    


def get_toupload_URLs(uploaddir, objprefix):
    try:
        webRootDir = look_for_www_subcomponent(uploaddir)

        if not webRootDir:
            return (False, None, None, None)

        dataPath = os.path.normpath(os.path.join(webRootDir,
                                                 objprefix + '_DATA'))
        dataPath = dataPath.replace('\\', '/')
        #dataPath = dataPath.replace('#', '%23')
        dataPath = urllib.quote(dataPath)
        auxiPath = os.path.normpath(os.path.join(webRootDir,
                                                 objprefix + '_AUXI'))
        auxiPath = auxiPath.replace('\\', '/')
        #auxiPath = auxiPath.replace('#', '%23')
        auxiPath = urllib.quote(auxiPath)
        
        auxiDir = os.path.join(uploaddir, objprefix + '_AUXI')

        logging.debug('get_toupload_URLs: ' + dataPath + ' ' + auxiPath + ' ' +
                      auxiDir)
        return (True, dataPath, auxiPath, auxiDir)
    except:
        ryw.give_bad_news('get_toupload_URLs: failed for: ' + uploaddir +
                          ' ' + objprefix, logging.error)
        return (False, None, None, None)



def print_logo():
    logoStr = ryw_customize.dict['headerLogo']
    print logoStr



def print_header_logo():
    ryw.print_header()
    print_logo()
    print css_str()
    


def print_footer():
    print ryw_customize.dict['footerStr']



def logo_str_for_disc():
    return ryw_customize.dict['logoStr']



def footer2_str():
    return ryw_customize.dict['footerStr2']



def should_show_object(meta, resources):
    if resources == None:
        return True

    miscDict = ryw.get_misc_dict()
    if miscDict.has_key('userName') and miscDict['userName'] == 'admin':
        return True
    
    dontShowCopyRighted = ryw.get_resource(resources, 'dontShowCopyRighted')
    dontShowDiscreet = ryw.get_resource(resources, 'dontShowDiscreet')

    if (not dontShowCopyRighted) and (not dontShowDiscreet):
        #logging.debug('should_show_object: always show.')
        return True

    if not meta.has_key('show'):
        #logging.debug('should_show_object: innocent object.')
        return True

    id = meta['id']
    showAttr = meta['show']
    #logging.debug('should_show_object: object show: ' + repr(showAttr))

    if ('copyrighted' in showAttr) and dontShowCopyRighted:
        logging.debug('should_show_object: copyrighted object not displayed: '+
                      id)
        return False

    if ('discreet' in showAttr) and dontShowDiscreet:
        logging.debug('should_show_object: discreet object not displayed: ' +
                      id)
        return False

    return True



#
# if the user name is not admin, and
# the resources file contains a line that says:
# showCopyrightedMetaOnly=True
# then we will not display a URL to the data.
#
def should_show_copyrighted_meta_only(meta):

    if not calledByRepository():
        #logging.debug('should_show_copyrighted_meta_only: not called by repo.')
        return False

    resources = ryw.get_resources(os.path.join(RepositoryRoot,
                                               'Resources.txt'))
    
    if resources == None:
        logging.debug('should_show_copyrighted_meta_only: no resource.')
        return False

    miscDict = ryw.get_misc_dict()
    if miscDict.has_key('userName') and miscDict['userName'] == 'admin':
        #logging.debug('should_show_copyrighted_meta_only: is admin.')
        return False

    showCopyrightedMetaOnly = ryw.get_resource(resources,
                                               'showCopyrightedMetaOnly')

    if not showCopyrightedMetaOnly:
        #logging.debug('should_show_copyrighted_meta_only: not metaOnly.')
        return False

    if not meta.has_key('show'):
        #logging.debug('should_show_copyrighted_meta_only: not show attr.')
        return False

    id = meta['id']
    showAttr = meta['show']

    if ('copyrighted' in showAttr) and showCopyrightedMetaOnly:
        #logging.debug('should_show_copyrighted_meta_only: hide meta!!')
        return True

    return False



#uploadQueue:
def is_list_object(meta):
    return meta.has_key('sys_attrs') and ('isList' in meta['sys_attrs'])



def confirm_popup_js():
    scriptStr = """
<script language="JavaScript" type="text/javascript">
<!--Comment tag so old browsers wont see code.

function confirmPopup(url, msg, width, height) {
    if (confirm(msg)) {
	window.open(url, "_blank", "width=" +width+ ",height=" +height+ ",scrollbars,resizable,alwaysRaised");
	return false;
    }
    return false;
}

//-- end comment for old browsers -->
</script>
"""
    return scriptStr



def popup_js():
    """included in DisplaySelection.print_...().
    eventually used by ChapterList.make_form_string()."""
    
    scriptStr = """
<script language="JavaScript" type="text/javascript">
<!--Comment tag so old browsers wont see code.

function popup_js(url, width, height) {
    window.open(url, "_blank", "width=" +width+ ",height=" +height+ ",scrollbars,resizable,alwaysRaised");
    return false;
}

//-- end comment for old browsers -->
</script>
"""
    return scriptStr



def select_button_string(cgiScript, selName, selVal, confirmMsg,
                         windowWidth, windowHeight,
                         buttonImg, buttonWidth, buttonHeight,
                         hoverMsg, appendBlanks = False):
    buttonStr = """<A
HREF="%(cgiScript)s?sel=%(selName)s"
onClick="return confirmPopup('%(cgiScript)s?%(selName)s=%(selVal)s','%(confirmMsg)s',%(windowWidth)s,%(windowHeight)s);"><IMG
SRC="%(buttonImg)s" WIDTH=%(buttonWidth)s HEIGHT=%(buttonHeight)s BORDER=0
TITLE="%(hoverMsg)s"
onmouseover="this.style.cursor='pointer';"></A>%(blanks)s
"""
    dict = {}
    dict['cgiScript'] = cgiScript
    dict['selName'] = selName
    dict['selVal'] = selVal
    dict['confirmMsg'] = confirmMsg
    dict['windowWidth'] = windowWidth
    dict['windowHeight'] = windowHeight
    dict['buttonImg'] = buttonImg
    dict['buttonWidth'] = buttonWidth
    dict['buttonHeight'] = buttonHeight
    dict['hoverMsg'] = hoverMsg
    dict['blanks'] = blank_string(appendBlanks)
    return buttonStr % dict



#
# unlike the previous one, this one does not pop up a new window.
#
def select_button_string2(cgiScript, confirmMsg,
                          buttonImg, buttonWidth, buttonHeight,
                          hoverMsg, appendBlanks = False):
    buttonStr = """<A HREF="%(cgiScript)s"
onClick="return confirm('%(confirmMsg)s');"><IMG
SRC="%(buttonImg)s" WIDTH=%(buttonWidth)s HEIGHT=%(buttonHeight)s BORDER=0
TITLE="%(hoverMsg)s"
onmouseover="this.style.cursor='pointer';"></A>%(blanks)s
"""
    dict = {}
    dict['cgiScript'] = cgiScript
    dict['confirmMsg'] = confirmMsg
    dict['buttonImg'] = buttonImg
    dict['buttonWidth'] = buttonWidth
    dict['buttonHeight'] = buttonHeight
    dict['hoverMsg'] = hoverMsg
    dict['blanks'] = blank_string(appendBlanks)
    return buttonStr % dict



#
# unlike the previous one, this one does not have confirmation.
#
def select_button_string3(cgiScript, 
                          buttonImg, buttonWidth, buttonHeight,
                          hoverMsg, appendBlanks = False):
    buttonStr = """<A HREF="%(cgiScript)s"><IMG
SRC="%(buttonImg)s" WIDTH=%(buttonWidth)s HEIGHT=%(buttonHeight)s BORDER=0
TITLE="%(hoverMsg)s"
onmouseover="this.style.cursor='pointer';"></A>%(blanks)s
"""
    dict = {}
    dict['cgiScript'] = cgiScript
    dict['buttonImg'] = buttonImg
    dict['buttonWidth'] = buttonWidth
    dict['buttonHeight'] = buttonHeight
    dict['hoverMsg'] = hoverMsg
    dict['blanks'] = blank_string(appendBlanks)
    return buttonStr % dict



def blank_string(doIt = False):
    if doIt:
	return BLANKS
    return ''



def clear_save_sel_buttons(name, doBoth=False):
    if name == '' or name == 'guest':
        return ''
    
    buttonDeselect = select_button_string2(
        '/cgi-bin/ClearQueue.py',
        'De-select all currently selected objects?',
        '/icons/select_0.png',
	BUTTON_WIDTH,  BUTTON_HEIGHT, 
        'De-select all currently selected objects',
	appendBlanks = True)

    if doBoth:
        buttonSave = select_button_string2(
            '/cgi-bin/UploadQueue_form.py',
            'Save the current selection?',
            '/icons/db_add_select.png',
            BUTTON_WIDTH,  BUTTON_HEIGHT,
            'Save the current selection',
            appendBlanks = True)
    else:
        buttonSave = ''

    return buttonDeselect + buttonSave

    
