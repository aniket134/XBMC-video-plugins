import ProcessDownloadReq
import cgi, cgitb, os, sys
cgitb.enable()
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import ShowQueue, DisplaySelection, AddSearchAll, DeleteObject
import DelSearchAll, DeleteRepReq, ThisSelToCurrSel
import ryw_view, Search, ryw, logging



def main():
    name = ShowQueue.init_log()
    ryw_view.print_header_logo()

    rfpath = ThisSelToCurrSel.get_file_path(allowNullSearchFile=True)
    if not rfpath:
        ryw.give_bad_news(
            'DelSelData.py: no selection file name found.', logging.error)
        DisplaySelection.exit_now(1)
    
    selection = ProcessDownloadReq.get_reqs(rfpath)
    if not selection or len(selection) == 0:
        ryw.give_bad_news(
            'DelSelData.py: there is nothing in the selection.',
            logging.error)
        DisplaySelection.exit_now(1)

    success = DelSearchAll.delete_all(selection)
    if success:
        ryw.give_news('All these objects have been removed.', logging.info)
    else:
        ryw.give_bad_news('DelSelData.py: an error occurred.',
                          logging.error)
        
    DisplaySelection.exit_now(0)


    
if __name__ == '__main__':
    main()
