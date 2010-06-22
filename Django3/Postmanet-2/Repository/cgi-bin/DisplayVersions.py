import sys, os
import su
import pickle, cgi, cgitb, xmlrpclib, urllib
cgitb.enable()
import SearchFile
import ryw,logging, ryw_view, ryw_meta
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import ShowQueue, Browse
import ReverseLists
cgitb.enable()



def print_header():
    str1 ='<FONT SIZE=2><B>Display All Versions:</B></FONT>' 
    #print str1 + '<BR>'



def exit_now(num):
    ryw_view.print_footer()
    sys.exit(num)
                


def print_title():
    print_header()
    print Browse.script_str()

    

def main():

    name = ShowQueue.init_log('DisplayVersions')
    ryw_view.print_header_logo()
    print '<TITLE>Display All Versions</TITLE>'

    form = cgi.FieldStorage()
    objID = form.getfirst('objid', '')

    if not objID:
        ryw.give_bad_news(
            'DisplayVersions: no objID given.', logging.error)
        exit_now(1)
    else:
        ryw.db_print_info_browser('DisplayVersions: objID = ' + objID, 32)

    success,searchFile,reverseLists = \
        ReverseLists.open_searchfile_reverselists(
        'DisplaySelection.main:')
    if not success:
        exit_now(1)

    print_title()

    success,allVersions = searchFile.get_all_version_meta(objID)
    if not success:
        ryw.give_bad_news(
            'DisplayVersion: searchFile.get_all_version_meta failed: ' +
            objID, logging.error)
        exit_now(1)    

    numVers = len(allVersions)

    if numVers < 1:
        ryw.give_bad_news(
            'DisplayVersions: no version found.', logging.error)
        exit_now(1)
    
    metaList = allVersions.values()
    ryw.db_print_info_browser('DisplayVersions: ' + repr(metaList), 32)
    metaList = ryw.sortmeta(metaList)

    displayObject = ryw_view.DisplayObject(
        RepositoryRoot,
        calledByVillageSide = False,
        missingFileFunc = Browse.reqDownloadFunc,
        searchFile = searchFile,
        reverseLists = reverseLists)

    print "<BR><B><FONT SIZE=2>Displaying " + str(numVers) + \
          " version(s) of the object.</FONT></B>"

    displayObject.begin_print()
    for meta in metaList:
        displayObject.show_an_object_compact(meta)
    displayObject.end_print()

    ryw_view.print_footer()

    reverseLists.done()
    searchFile.done()



if __name__ == '__main__':
    main()

