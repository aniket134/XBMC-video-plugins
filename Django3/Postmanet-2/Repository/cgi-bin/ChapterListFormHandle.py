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
    """modeled after ChapterListForm.py.
    This is for displaying a form that allows editing the chapter list."""

    name = ShowQueue.init_log()
    ryw_view.print_header_logo()
    print '<TITLE>Processing the Chapter List</TITLE>'

    ryw.db_print2('<BR>ChapterListFormHandle.py: entered... <BR>', 39)

    form = cgi.FieldStorage()

    success,objID,version = ryw.get_obj_str(form = form)
    if not success:
        ryw.give_bad_news('ChapterListFormHandle: failed to get objstr.',
                          logging.critical)
        DisplaySelection.exit_now(1)

    ryw.db_print2('ChapterListFormHandle: objstr is: ' +
                  objID + '#' + str(version), 40)

    chapterList = ChapterList.ChapterList(objID + '#' + str(version))
    success,formEntries = chapterList.process_form(form)
    
    if not success:
        ryw.give_bad_news('ChapterListFormHandle: process_form() failed.',
                          logging.error)
        DisplaySelection.exit_now(1)
    
    success,searchFile,reverseLists = \
        ReverseLists.open_searchfile_reverselists(
        'DisplaySelection.main:')
    if not success:
        DisplaySelection.exit_now(1)

    success = DisplaySelection.print_title(objID, version, name, searchFile)
    if not success:
        DisplaySelection.exit_now(1)

    ryw.db_print2('<BR>ChapterListFormHandle.py entered.<BR>', 41)

    nameTriple = DisplaySelection.get_file_paths2(
        objID, version, searchFile = searchFile)
    if not nameTriple:
        DisplaySelection.exit_now(1)
    rfpath,chapterListPath,chapterListFullName = nameTriple
    if not rfpath:
        DisplaySelection.exit_now(1)

    ryw.db_print2('ChapterListFormHandle: chapter list file is: ' +
                  chapterListFullName, 41)

    reqList = ShowQueue.read_list(rfpath)
    if not reqList:
        ryw.give_news('This selection is empty.<BR>', logging.info)
        print '<BR>'
        print_links(objID, version, name)
        DisplaySelection.exit_now(0)

    ryw.db_print2('ChapterListForm.py: gotten selection list.', 41)

    success = chapterList.initialize_with_meta_list(
        reqList, searchFile, reverseLists)

    if not success:
        ryw.give_bad_news('ChapterListFormHandle: ' +
                          'initialize_with_meta_list failed.',
                          logging.error)
        DisplaySelection.exit_now(1)

    chapterList.compare_form_entries_against_meta()
    if not chapterList.write_file(chapterListFullName):
        ryw.give_bad_news('ChapterListFormHandle: write_file() failed.',
                          logging.error)
        DisplaySelection.exit_now(1)

    ryw.give_news('chapter list saved.', logging.info)
                              
    ryw_view.print_footer()

    reverseLists.done()
    searchFile.done()



if __name__ == '__main__':
    main()

