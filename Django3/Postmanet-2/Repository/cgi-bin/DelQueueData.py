import ProcessDownloadReq
import cgi, cgitb, os, sys
cgitb.enable()
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import ShowQueue, DisplaySelection, AddSearchAll, DeleteObject
import DelSearchAll, DeleteRepReq
import ryw_view, Search, ryw, logging



def main():
    name = ShowQueue.init_log()
    ryw_view.print_header_logo()

    queueName = DeleteRepReq.get_queue_name()
    if not queueName:
        ryw.give_bad_news(
            'DelQueueData.py: failed to get current selection file name.',
            logging.error)
        DisplaySelection.exit_now(1)

    queueSel = ProcessDownloadReq.get_reqs(queueName)
    if not queueSel or len(queueSel) == 0:
        ryw.give_bad_news(
            'DelQueueData.py: there is nothing in the selection.',
            logging.error)
        DisplaySelection.exit_now(1)

    success = DelSearchAll.delete_all(queueSel)
    if success:
        ryw.give_news('All these objects have been removed.', logging.info)
    else:
        ryw.give_bad_news('DelQueueData.py: an error occurred.',
                          logging.error)
        
    DisplaySelection.exit_now(0)


    
if __name__ == '__main__':
    main()
