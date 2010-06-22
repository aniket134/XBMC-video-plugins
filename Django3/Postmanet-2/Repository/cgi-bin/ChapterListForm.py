import sys, os
import su
import pickle, cgi, cgitb, xmlrpclib, urllib
cgitb.enable()
import SearchFile
import ryw,logging, ryw_view, ryw_meta
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import ShowQueue, Browse
import ReverseLists
import DisplaySelection
import ChapterList
cgitb.enable()



def main():
    """modeled after DisplaySelection.py.
    This is for displaying a form that allows editing the chapter list."""

    name = ShowQueue.init_log()
    ryw_view.print_header_logo()
    print '<TITLE>Edit the Chapter List</TITLE>'

    success,objID,version = ryw.get_obj_str()
    if not success:
        ryw.give_bad_news('ChapterListForm: failed to get objstr.',
                          logging.critical)
        DisplaySelection.exit_now(1)

    success,searchFile,reverseLists = \
        ReverseLists.open_searchfile_reverselists(
        'DisplaySelection.main:')
    if not success:
        DisplaySelection.exit_now(1)

    print '<BR><B>Edit chapter names for this selection:</B><BR><BR>'

    success = DisplaySelection.print_title(objID, version, name, searchFile)
    if not success:
        DisplaySelection.exit_now(1)

    ryw.db_print2('<BR>ChapterListForm.py entered.<BR>', 38)
    
    nameTriple = DisplaySelection.get_file_paths2(
        objID, version, searchFile = searchFile)
    if not nameTriple:
        DisplaySelection.exit_now(1)
    rfpath,chapterListPath,chapterFullName = nameTriple
    if not rfpath:
        DisplaySelection.exit_now(1)

    reqList = ShowQueue.read_list(rfpath)
    if not reqList:
        ryw.give_news('This selection is empty.<BR>', logging.info)
        print '<BR>'
        print_links(objID, version, name)
        DisplaySelection.exit_now(0)

    ryw.db_print2('ChapterListForm.py: gotten selection list.', 38)

    success,chapterList = ChapterList.create_and_initialize(
        objID + '#' + str(version),
        reqList, searchFile, reverseLists,
        chapterFullName)
    if not success:
        ryw.give_bad_news('ChapterList.create_and_initialize failed: ' +
                          objID + '#' + str(version), logging.error)
        DisplaySelection.exit_now(1)

    page = chapterList.make_form_string()
    print page
    
    ryw_view.print_footer()

    reverseLists.done()
    searchFile.done()



if __name__ == '__main__':
    main()

