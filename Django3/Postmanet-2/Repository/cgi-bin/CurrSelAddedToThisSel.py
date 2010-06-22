import os,ryw,logging,sys,ryw_view,cgi,shutil
import ProcessDownloadReq
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import DisplaySelection,DeleteRepReq,AddSearchAll
import ReverseLists



def main():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('CurrSelAddedToThisSel: entered...')
    ryw_view.print_header_logo()


    success,objID,version = ryw.get_obj_str()
    if not success:
        ryw.give_bad_news('CurrSelToThisSel: failed to get objstr.',
                          logging.critical)
        DisplaySelection.exit_now(1)
    
    success,searchFile,reverseLists = \
        ReverseLists.open_searchfile_reverselists('CurrSelAddedToThisSel:')
    if not success:
        ryw.give_bad_news('CurrSelAddedToThisSel: ' +
                          'open_searchfile_reverselists failed.',
                          logging.critical)
        DisplaySelection.exit_now(1)
    

    rfpath = DisplaySelection.get_file_path(
        objID, version, searchFile = searchFile)
    if not rfpath:
        ryw.give_bad_news(
            'CurrSelAddedToThisSel: no selection file name found.',
            logging.error)
        DisplaySelection.exit_now(1)

    queueName = DeleteRepReq.get_queue_name()
    if not queueName:
        ryw.give_bad_news(
            'CurrSelToThisSel: failed to get current selection file name.',
            logging.error)
        DisplaySelection.exit_now(1)

    queueSel = ProcessDownloadReq.get_reqs(queueName)
    savedSel = ProcessDownloadReq.get_reqs(rfpath)
    newContainees = list(queueSel)

    AddSearchAll.union_and_write(savedSel, queueSel, rfpath)
    ryw.give_news('You may want to reload the page containing '+
                  'this selection.', logging.info)


    success = reverseLists.add(objID+'#'+str(version), newContainees)
    if not success:
        ryw.give_bad_news('CurrSelAddedToThisSel: reverseLists.add failed.',
                          logging.critical)

    reverseLists.done()
    searchFile.done()
    DisplaySelection.exit_now(0)
    


if __name__ == '__main__':
    main()


