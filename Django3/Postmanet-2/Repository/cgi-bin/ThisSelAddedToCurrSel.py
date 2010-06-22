import os,ryw,logging,sys,ryw_view,cgi,shutil
import ProcessDownloadReq
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import DisplaySelection,DeleteRepReq,ThisSelToCurrSel,AddSearchAll



def main():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('ThisSelAddedToCurrSel: entered...')
    ryw_view.print_header_logo()

    rfpath = ThisSelToCurrSel.get_file_path(allowNullSearchFile=True)
    if not rfpath:
        ryw.give_bad_news(
            'ThisSelAddedToCurrSel: no selection file name found.',
            logging.error)
        DisplaySelection.exit_now(1)

    savedSel = ProcessDownloadReq.get_reqs(rfpath)
    if (not savedSel) or (len(savedSel) == 0):
        ryw.give_news('ThisSelAddedToCurrSel: this selection is empty.',
                      logging.error)
        DisplaySelection.exit_now(1)

    queueName = DeleteRepReq.get_queue_name()
    if not queueName:
        ryw.give_bad_news(
            'ThisSelToCurrSel: failed to get current selection file name.',
            logging.error)
        DisplaySelection.exit_now(1)

    queueSel = ProcessDownloadReq.get_reqs(queueName)

    AddSearchAll.union_and_write(queueSel, savedSel, queueName)
    ryw.give_news('You may want to reload the page containing '+
                  'the affected current selection.', logging.info)
    DisplaySelection.exit_now(0)
    


if __name__ == '__main__':
    main()


