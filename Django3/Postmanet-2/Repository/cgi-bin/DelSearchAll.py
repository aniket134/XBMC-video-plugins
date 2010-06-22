import ProcessDownloadReq
import cgi, cgitb, os, sys
cgitb.enable()
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import ShowQueue, DisplaySelection, AddSearchAll, DeleteObject
import ryw_view, Search, ryw, logging



def delete_all(searchSel):
    completeSuccess = True
    searchFile = None
    
    for objstr in searchSel:
        success,objID,version = ryw.split_objstr(objstr)
        if not success:
            ryw.give_bad_news('DelSearchAll: invalid objstr: ' + objstr,
                              logging.error)
            completeSuccess = False
            continue
        success,searchFile = DeleteObject.do_delete(
            objID, version, searchFile=searchFile)
        if not success:
            ryw.give_bad_news(
                'DelSearchAll: DeleteObject.do_delete failed.' + objstr,
                logging.error)
            completeSuccess = False
        else:
            ryw.db_print('DelSearchAll.delete_all: do_delete succeeded.',
                         18)

    if searchFile:
        searchFile.done()
    return completeSuccess

            

def main():
    name = ShowQueue.init_log()
    ryw_view.print_header_logo()
    
    searchSel = AddSearchAll.get_search_result()
    if not searchSel:
        ryw.give_bad_news(
            'DelSearchAll: failed to load current search result.',
            logging.error)
        DisplaySelection.exit_now(1)

    success = delete_all(searchSel)
    if success:
        ryw.give_news('All these objects have been removed.', logging.info)
    else:
        ryw.give_bad_news('DelSearchAll.py: an error occurred.',
                          logging.error)
        
    DisplaySelection.exit_now(0)


    
if __name__ == '__main__':
    main()
