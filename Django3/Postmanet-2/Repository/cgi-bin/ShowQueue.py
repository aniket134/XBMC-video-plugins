import sys, os
import su
import pickle, cgi, cgitb, xmlrpclib, urllib
cgitb.enable()
import SearchFile, Search, Browse
import ryw,logging, ryw_view, ryw_meta
import ReverseLists
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import DisplaySelection



def cancelFunc(meta, calledByVillageSide, dataURL, searchFile=None):
    deleteIconStr = """
<IMG SRC="/icons/trash.gif" BORDER=0 
title="cancel this request" onmouseover="this.style.cursor='pointer';" 
onClick="deleteVilReq('%s')">
"""
    editIconStr = """<A
href="%s"><IMG SRC="/icons/quill.gif" BORDER=0
title="edit object attributes"></A>
"""

    objID = meta['id']
    version = str(meta['version'])
    objstr = objID + '#' + version
    logging.debug('cancelFunc: ' + objstr)

    editIconStr = editIconStr % ("/cgi-bin/ShowObject.py?objstr=" +
                                 urllib.quote(objstr),)

    versionIconStr = Browse.make_all_version_icon_str(meta, searchFile)

    return deleteIconStr % (objstr,) + editIconStr + versionIconStr



def init_log(whoCalled = 'ShowQueue'):
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug(whoCalled + ': entered...')
    name = os.getenv("REMOTE_USER")
    return name



def print_header(selectionName):
    print Browse.script_str()
    print '<FONT SIZE=2>Selection <B><I>' + selectionName + ':</I></B></FONT>'
    print '<BR>'
    print """
<script language="JavaScript" type="text/javascript">
<!--
function deleteVilReq(param) {
        var http = getHTTPObject();
        if (!confirm("Delete object " + param + " from request queue?")) return;
        http.open("GET","/cgi-bin/DeleteRepReq.py?objstr="+escape(param),true);
        http.onreadystatechange = function() {
                if (http.readyState == 4) {
                        if (http.status == 200) {
                                if (http.responseText == "True") {
                                        window.location = window.location;
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

//-- end comment for old browsers -->
</script>
"""



def read_list(rfpath):
    if os.path.exists(rfpath):
        try:
            reqs = su.pickload(rfpath)
        except:
            ryw.give_bad_news('ShowQueue: failed to load queue: ' + rfpath,
                              logging.critical)
            return None
    else:
        reqs = set('')

    l = list(reqs)
    l.sort()
    return l



def go_through_list(reqList, callBackFunc = cancelFunc, cBackArg = None,
                    offResult = None,
                    cgiScript = '/cgi-bin/ShowQueue.py',
                    scriptConnectChar = '?',
                    searchFile = None,
                    reverseLists = None,
                    chapterList = None):
    """also called by DisplaySelection.py"""

    if not searchFile or not reverseLists:
        raise NameError('ShowQueue: bad searchFile or bad reverseLists')

    if not offResult:
        offResult = (True, True, 0)

    #
    # 
    # only get SearchFile if nothing is sent in?
    # 
    #success,searchFile = ryw.open_search_file(
    #    'ShowQueue:',
    #    os.path.join(RepositoryRoot, 'WWW', 'logs'),
    #    'upload.log',
    #    os.path.join(RepositoryRoot, 'SearchFile'),
    #    False)
    #if not success:
    #    return False


    metaList = ryw_meta.get_meta_list(reqList, searchFile)

    #
    # 10/24/08: from DisplaySelection, we want to patch the chapter
    # numbering using the chapter list.
    #
    if chapterList:
        chapterList.patch_meta_list_with_chapters(metaList=metaList)

    metaList = ryw.sortmeta_chapter_number(metaList)

    logging.debug('ShowQueue: printing sorted objects...')

    displayObject = ryw_view.DisplayObject(RepositoryRoot,
                                           calledByVillageSide = False,
                                           missingFileFunc = callBackFunc,
					   callBackArg = cBackArg,
                                           searchFile = searchFile,
                                           reverseLists = reverseLists)
    #displayObject = ryw_view.DisplayObject(RepositoryRoot,
    #                                       calledByVillageSide = False,
    #                                       missingFileFunc = TestReqFunc)

    offsuccess,showAll,offsetNum = offResult
    numMatches = len(metaList)
    success = True
    
    if numMatches <= 0:
        ryw.give_news('ShowQueue: no object to show.<BR>', logging.error)
        success = False
    elif showAll:
        print_num_selected(numMatches, 0, 0, showAll = True)
        displayObject.begin_print()
        for meta in metaList:
            displayObject.show_an_object_compact(meta)
        displayObject.end_print()
        print '<BR>'
    else:
        offsetNum,endIndex = compute_begin_end(offsetNum, numMatches)
        print_num_selected(numMatches, offsetNum, endIndex)
        print_next_button(cgiScript, scriptConnectChar,
                          endIndex, numMatches)
        displayObject.begin_print()
        for i in range(offsetNum,  endIndex + 1):
            displayObject.show_an_object_compact(metaList[i])
        displayObject.end_print()
        print_next_button(cgiScript, scriptConnectChar,
                          endIndex, numMatches,
			  addBlanks = True)

    searchFile.done()
    return success



def compute_begin_end(offsetNum, numMatches):
    offsetNum = max(offsetNum, 0)
    offsetNum = min(offsetNum, numMatches - 1)
    endIndex = offsetNum + Search.NUM_OBJECTS_PER_PAGE - 1
    endIndex = max(endIndex, 0)
    endIndex = min(endIndex, numMatches - 1)
    return (offsetNum,endIndex)



def print_num_selected(totalNum, offsetNum, endIndex, showAll = False):
    dict={}
    countStr = """<BR>
<B><FONT SIZE=2>%(totalNum)s object(s) in this selection.</FONT></B>"""
    dict['totalNum'] = str(totalNum)
    countStr = countStr % dict

    if showAll:
        showStr = """<BR><B>
<FONT SIZE=2>displaying all matches.</FONT></B>"""
    else:
        showStr = """<BR>
<B><FONT SIZE=2>displaying selected objects %(first)s - %(last)s.</FONT>
</B>"""
        dict['first'] = str(offsetNum + 1)
        dict['last'] = str(endIndex + 1)
        showStr = showStr % dict

    print countStr
    print showStr



def print_next_button(script, connectChar, prevEndIndex, numMatches,
		      addBlanks = False):
    if numMatches <= 0:
        ryw.give_bad_news('ShowQueue: number of matches is non-positive. '+
                          'This is not supposed to happen.',
                          logging.critical)
        return
    
    if prevEndIndex + 1 >= numMatches:
        print '<BR>'
        return

    offsetNum,endIndex = compute_begin_end(prevEndIndex + 1, numMatches)
    script = script + connectChar + 'offset=' + str(offsetNum)
    hoverMsg = 'next selected objects: ' + \
               str(offsetNum + 1) + ' - ' + \
               str(endIndex + 1)
    buttonStr = ryw_view.select_button_string3(
        script, '/icons/next.png', 
	ryw_view.BUTTON_WIDTH,  ryw_view.BUTTON_HEIGHT, hoverMsg, addBlanks)
    print '<BR><BR>' + buttonStr

        

def print_buttons(name):
    if name == '' or name == 'guest':
        return

    clearSaveButtonStr = ryw_view.clear_save_sel_buttons(name, doBoth=True)
    print clearSaveButtonStr

    if name != 'admin':
        return
    
    buttonDestroy = ryw_view.select_button_string2(
        '/cgi-bin/DelQueueData.py',
        'Danger: do you really want to destroy all the actual data '+
        'belonging to the objects of the current selection?',
        '/icons/select_star_equal_0.png',
	ryw_view.BUTTON_WIDTH,  ryw_view.BUTTON_HEIGHT,
        'Danger: destroy data belonging to objects ' + 
        'of the current selection')
    print buttonDestroy        



#
# return (Success, All, offsetNum)
#
def get_offset():
    try:
        form = cgi.FieldStorage()
        offsetStr = form.getfirst('offset', '')
        if offsetStr == '':
            offsetStr = '0'
        if offsetStr != 'all':
            offsetNum = int(offsetStr)
        else:
            offsetNum = 0
    except:
        ryw.give_bad_news('ShowQueue: failed to process argument.',
                          logging.error)
        return (False, False, 0)

    isAll = offsetStr == 'all'
    return (True, isAll, offsetNum)
            


def main():
    name = init_log()
    ryw_view.print_header_logo()
    print '<TITLE>Browsing Selection</TITLE>'

    offsetResult = get_offset()
    success,isAll,offsetNum = offsetResult
    if not success:
        DisplaySelection.exit_now(1)
    
    print_header(name)
    rfpath = os.path.join(RepositoryRoot, 'QUEUES', name)
    reqList = read_list(rfpath)
    if not reqList:
        ryw.give_news('no object selected.', logging.info)
        DisplaySelection.exit_now(0)


    success,searchFile,reverseLists = \
        ReverseLists.open_searchfile_reverselists(
        'ShowQueue.main:')

    if not success:
        DisplaySelection.exit_now(0)

    if go_through_list(reqList, offResult = offsetResult,
                       searchFile = searchFile, reverseLists = reverseLists):
        print_buttons(name)
        
    ryw_view.print_footer()
    searchFile.done()
    reverseLists.done()
    


if __name__ == '__main__':
    main()
