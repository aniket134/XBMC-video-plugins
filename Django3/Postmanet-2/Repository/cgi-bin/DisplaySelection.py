import sys, os
import su
import pickle, cgi, cgitb, xmlrpclib, urllib
cgitb.enable()
import SearchFile
import ryw,logging, ryw_view, ryw_meta
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import ShowQueue, Browse
import ReverseLists
import ChapterList
cgitb.enable()



def delOneSelFunc(meta, calledByVillageSide, dataURL, callBackArg,
                  searchFile = None):

    name = os.getenv("REMOTE_USER")
    if name == '' or name == 'guest':
        return ''
    
    deleteIconStr = """<IMG
SRC="/icons/trash.gif" BORDER=0 title="remove from selection"
onmouseover="this.style.cursor='pointer';"
onClick="delOneSel('%(objstr)s','%(selobj)s')">
"""
    requestIconStr = """<IMG
SRC="/icons/link.gif" BORDER=0 title="add to current selection"
onmouseover="this.style.cursor='pointer';" onClick="reqData('%s',this)">
"""

    editIconStr = """<A
href="%s"><IMG SRC="/icons/quill.gif" BORDER=0
title="edit object attributes"></A>
"""
    
    objID = meta['id']
    version = str(meta['version'])
    objstr = objID + '#' + version
    selobj = callBackArg
    dict = {}
    dict['objstr'] = objstr
    dict['selobj'] = selobj

    editIconStr = editIconStr % ("/cgi-bin/ShowObject.py?objstr=" +
                                 urllib.quote(objstr),)

    answer = (deleteIconStr % dict) + editIconStr + \
             (requestIconStr % (objstr,))

    versionIconStr = Browse.make_all_version_icon_str(meta, searchFile)

    return answer + versionIconStr



def print_header(selectionName, objstr = ''):
    str1 ='<FONT SIZE=2>Displaying selection: </FONT>' 
    if objstr == '':
        str2 = '<FONT SIZE=2><B>' + selectionName + '</B>:</FONT>'
    else:
        str2 = '<FONT SIZE=2><B>' + \
            ryw_view.show_obj_cgi_str(selectionName, objstr)+':</B></FONT>'
        #str2 += ' <FONT SIZE=1>(' + \
        #    ryw_view.show_chapter_edit_cgi_str(selectionName, objstr) + \
        #    ')</FONT>:'
                                         
    print str1 + str2 + '<BR>'

    print """
<script language="JavaScript" type="text/javascript">
<!--
function delOneSel(param,param2) {
    var http = getHTTPObject();
    if (!confirm("Remove object " + param + " from selection?")) return;
    http.open("GET","/cgi-bin/DeleteFromSel.py?objstr="+escape(param)+"&selobj="+escape(param2),true);
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



def get_all_paths(objID, version, skipLock = False, searchFile = None,
             allowNullSearchFile = False):
    #searchFile = ryw_meta.open_search_file(RepositoryRoot)
    #if not searchFile:
    #    return (False, None)

    #meta,objroot = ryw_meta.get_meta(searchFile, objID, version,
    #                                 RepositoryRoot)
    #searchFile.done()

    if searchFile == None and not allowNullSearchFile:
        ryw.give_bad_news('DisplaySelection.get_path: warning, no ' +
                          'searchFile. ok but should fix.',
                          logging.warning)

    if searchFile:
        success,meta = searchFile.get_meta(objID, version)
        if success and meta:
            objroot = ryw_meta.get_objectstore_root(RepositoryRoot, meta)
    else:
        success,meta,objroot = ryw_meta.get_meta2(
            RepositoryRoot, objID, version, skipLk = skipLock)
        logging.warning('DisplaySelection.get_path: get_meta2 called.')

    if not success or (not meta and not objroot):
        ryw.give_bad_news(
            'DisplaySelection: no meta, no objroot, giving up...',
            logging.critical)
        return (False, None, None)

    paths = ryw_meta.get_paths(objroot, objID, version, meta, RepositoryRoot)
    if not paths:
        ryw.give_bad_news('DisplaySelection: failed to get paths.',
                          logging.critical)
        return (False, None, None)

    return (True, paths, meta)



def get_path(objID, version, skipLock = False, searchFile = None,
             allowNullSearchFile = False):

    success,paths,meta = get_all_paths(objID, version, skipLock = skipLock,
                                       searchFile = searchFile,
                                       allowNullSearchFile =
                                       allowNullSearchFile)
    if success:
        return (True, paths[0])

    return (False, None)



def get_sel_name(dataPath):
    try:
        names = os.listdir(dataPath)
        if len(names) == 0:
            return None
        for name in names:
            if name.endswith('_selection'):
                return name
        return None
    except:
        ryw.give_bad_news(
            'DisplaySelection: failed to listdir: ' + dataPath,
            logging.error)
        return None



def get_chapterlist_name(dataPath):
    try:
        names = os.listdir(dataPath)
        if len(names) == 0:
            return None
        for name in names:
            if name == ChapterList.CHAPTER_LIST_NAME:
                ryw.db_print('get_chapterlist_name: found name: ' + name,
                              38)
                return name
        ryw.db_print('get_chapterlist_name: found no name: ', 38)
        return None
    except:
        ryw.give_bad_news(
            'DisplaySelection.get_chapterlist_name: failed to listdir: ' +
            dataPath, logging.error)
        return None



def exit_now(num):
    ryw_view.print_footer()
    sys.exit(num)
                


def get_file_paths2(objID, version, skipLk=False, searchFile=None,
                  allowNullSearchFile = False):
    """10/21/08: rewritten to return chapterListFile as well."""
    
    success,dataPath = get_path(objID, version, skipLock = skipLk,
                                searchFile = searchFile,
                                allowNullSearchFile = allowNullSearchFile)
    if not success:
        return None

    name = get_sel_name(dataPath)
    if not name:
        ryw.give_bad_news(
            'DisplaySelection: failed to get selection file name:<br>'+
            dataPath, logging.error)
        return None

    rfpath = os.path.join(dataPath, name)

    chapterListName = get_chapterlist_name(dataPath)
    chapterListFullName = os.path.join(dataPath,
                                       ChapterList.CHAPTER_LIST_NAME)
    ryw.db_print2('get_file_paths2: full name is: ' +
                  chapterListFullName, 39)
    
    return (rfpath, chapterListName, chapterListFullName)



def get_file_path(objID, version, skipLk=False, searchFile=None,
                  allowNullSearchFile = False):
    """10/21/08: used to be kind of like get_file_paths2...
    now redone to deal chapter list name return...
    I only need the first of the pair...
    This is for calling from outside of this file...
    for within this file, I'll need the entire pair."""

    nameTriple = get_file_paths2(objID, version,
                                 skipLk=skipLk,
                                 searchFile=searchFile,
                                 allowNullSearchFile=allowNullSearchFile)

    if nameTriple==None:
        return None

    selName,chapterName,chapterFullName = nameTriple
    return selName
    


def print_title(objID, version, name, searchFile):
    if not searchFile:
        raise NameError('DisplaySelection.print_title: no searchFile')

    success,meta = searchFile.get_meta(objID, version)
    #success,meta,objroot = ryw_meta.get_meta2(RepositoryRoot,
    #                                          objID, version)

    if not success:
        ryw.give_bad_news('DisplaySelection: failed to find this selection.',
                          logging.error)
        return False
    
    if success and meta.has_key('title'):
        name = meta['title']
    obj = meta['id'] + '#' + str(meta['version'])
    print_header(name, objstr = obj)
    print Browse.script_str()
    print ryw_view.popup_js()
    return True

    

def print_links_text_not_used(objID, version, name):
    if name == 'guest':
        return
    
    commandStr = """
<BR>
<A HREF="/cgi-bin/ThisSelToCurrSel.py?objstr=%(objstr)s"
onClick="return confirm('Overwrite the current selection?');">make
this selection the current selection</A>
<BR>
<A HREF="/cgi-bin/CurrSelToThisSel.py?objstr=%(objstr)s"
onClick="return confirm('Overwrite this selection?');">make
the current selection this selection</A>
<BR>
<A HREF="/cgi-bin/ThisSelAddedToCurrSel.py?objstr=%(objstr)s"
onClick="return confirm('Add this selection to the current selection?');">add
this selection to the current selection</A>
<BR>
<A HREF="/cgi-bin/CurrSelAddedToThisSel.py?objstr=%(objstr)s"
onClick="return confirm('Add the current selection to this selection?');">add
the current selection to this selection</A>
"""
    dict = {}
    dict['objstr'] = objID + '%23' + str(version)
    print commandStr % dict

    

def print_links(objID, version, name):
    if name == '' or name == 'guest':
        return

    print ryw_view.confirm_popup_js()

    objstr = objID + '%23' + str(version)

    #
    # the edit chapters button.
    #
    editChapScript = '/cgi-bin/ChapterListForm.py?objstr=' + objstr
    button0 = ryw_view.select_button_string3(
        editChapScript, '/icons/edit_chapters.png',
        ryw_view.BUTTON_WIDTH,  ryw_view.BUTTON_HEIGHT,
        'edit chapter names',
        True)

    button1 = ryw_view.select_button_string(
        '/cgi-bin/ThisSelToCurrSel.py',
        'objstr', objstr,
        'Overwrite the current selection with this selection?',
        ryw_view.CONFIRM_WIDTH,  ryw_view.CONFIRM_HEIGHT, 
        '/icons/select_equal_this.png',
        ryw_view.BUTTON_WIDTH,  ryw_view.BUTTON_HEIGHT, 
        'Overwrite the current selection with this selection',
	appendBlanks = True)

    button2 = ryw_view.select_button_string(
        '/cgi-bin/CurrSelToThisSel.py',
        'objstr', objstr,
        'Overwrite this selection with the current selection?',
        ryw_view.CONFIRM_WIDTH,  ryw_view.CONFIRM_HEIGHT, 
        '/icons/this_equal_select.png',
        ryw_view.BUTTON_WIDTH,  ryw_view.BUTTON_HEIGHT, 
        'Overwrite this selection with the current selection',
	appendBlanks = True)
    
    button3 = ryw_view.select_button_string(
        '/cgi-bin/ThisSelAddedToCurrSel.py',
        'objstr', objstr,
        'Add this selection to the current selection?',
        ryw_view.CONFIRM_WIDTH,  ryw_view.CONFIRM_HEIGHT, 
        '/icons/select_add_this.png',
        ryw_view.BUTTON_WIDTH,  ryw_view.BUTTON_HEIGHT, 
        'Add this selection to the current selection',
	appendBlanks = True)
    
    button4 = ryw_view.select_button_string(
        'CurrSelAddedToThisSel.py',
        'objstr', objstr,
        'Add the current selection to this selection?',
        ryw_view.CONFIRM_WIDTH,  ryw_view.CONFIRM_HEIGHT, 
        '/icons/this_add_select.png',
        ryw_view.BUTTON_WIDTH,  ryw_view.BUTTON_HEIGHT, 
        'Add the current selection to this selection',
        appendBlanks = True)
    
    print button0 + button1 + button2 + button3 + button4

    clearSaveButtonStr = ryw_view.clear_save_sel_buttons(name)
    print clearSaveButtonStr

    if name != 'admin':
        return

    buttonDestroy = ryw_view.select_button_string2(
        '/cgi-bin/DelSelData.py?' + 'objstr=' + objstr,
        'Danger: do you really want to destroy all the actual data '+
        'belonging to the objects of this selection?',
        '/icons/this_star_equal_0.png',
	ryw_view.BUTTON_WIDTH,  ryw_view.BUTTON_HEIGHT,
        'Danger: destroy data belonging to objects ' + 
        'of this selection')
    print buttonDestroy        



def main():

    name = ShowQueue.init_log()
    ryw_view.print_header_logo()
    print '<TITLE>Browsing Saved Selection</TITLE>'

    success,objID,version = ryw.get_obj_str()
    if not success:
        ryw.give_bad_news('DisplaySelection: failed to get objstr.',
                          logging.critical)
        exit_now(1)

    offsetResult = ShowQueue.get_offset()
    success,isAll,offsetNum = offsetResult
    if not success:
        exit_now(1)

    success,searchFile,reverseLists = \
        ReverseLists.open_searchfile_reverselists(
        'DisplaySelection.main:')
    if not success:
        sys.exit(1)

    success = print_title(objID, version, name, searchFile)
    if not success:
        exit_now(1)

    nameTriple = get_file_paths2(objID, version, searchFile = searchFile)
    if not nameTriple:
        exit_now(1)
    rfpath,chapterListPath,chapterFullName = nameTriple
    if not rfpath:
        exit_now(1)

    reqList = ShowQueue.read_list(rfpath)
    if not reqList:
        ryw.give_news('This selection is empty.<BR>', logging.info)
        print '<BR>'
        print_links(objID, version, name)
        exit_now(0)

    #
    # do this before displaying so that the ReverseLists is
    # properly reflected before we hit the display code.
    #
    result = reverseLists.add(objID + '#' + str(version), reqList)

    #
    # process the chapter list. 10/24/08.
    #
    success,chapterList = ChapterList.create_and_initialize(
        objID + '#' + str(version),
        reqList, searchFile, reverseLists,
        chapterFullName)
    if not success:
        ryw.give_bad_news('ChapterList.create_and_initialize failed: ' +
                          objID + '#' + str(version), logging.error)
        exit_now(1)

    scriptName = '/cgi-bin/DisplaySelection.py?objstr=' + \
                 objID + '%23' + str(version)
    
    success = \
            ShowQueue.go_through_list(reqList,
                                      callBackFunc = delOneSelFunc, 
                                      cBackArg = objID + '#' + str(version),
                                      offResult = offsetResult,
                                      cgiScript = scriptName,
                                      scriptConnectChar = '&',
                                      searchFile = searchFile,
                                      reverseLists = reverseLists,
                                      chapterList = chapterList)

    if success:
        print_links(objID, version, name)
        
    ryw_view.print_footer()

    reverseLists.done()
    searchFile.done()



if __name__ == '__main__':
    main()

