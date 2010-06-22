import os,ryw,logging,sys,ryw_view,cgi,shutil
import ProcessDownloadReq
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import DisplaySelection,DeleteRepReq,ShowQueue
import ReverseLists



def main():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('CurrSelToThisSel: entered...')
    ryw_view.print_header_logo()


    success,objID,version = ryw.get_obj_str()
    if not success:
        ryw.give_bad_news('CurrSelToThisSel: failed to get objstr.',
                          logging.critical)
        DisplaySelection.exit_now(1)
    
    success,searchFile,reverseLists = \
        ReverseLists.open_searchfile_reverselists('CurrSelToThisSel:')
    if not success:
        ryw.give_bad_news('CurrSelToThisSel: ' +
                          'open_searchfile_reverselists failed.',
                          logging.critical)
        DisplaySelection.exit_now(1)
    

    rfpath = DisplaySelection.get_file_path(
        objID, version, searchFile = searchFile)
    if not rfpath:
        ryw.give_bad_news(
            'CurrSelToThisSel: no selection file name found.',
            logging.error)
        DisplaySelection.exit_now(1)
    oldContainees = ShowQueue.read_list(rfpath)

    queueName = DeleteRepReq.get_queue_name()
    if not queueName:
        ryw.give_bad_news(
            'CurrSelToThisSel: failed to get current selection file name.',
            logging.error)
        DisplaySelection.exit_now(1)
    newContainees = ShowQueue.read_list(queueName)

    try:
        shutil.copyfile(queueName, rfpath)
    except:
        ryw.give_bad_news('CurrSelToThisSel: failed to overwrite: ' +
                          queueName + ' -> ' + rfpath,
                          logging.critical)
        DisplaySelection.exit_now(1)

    ryw.give_news(
        'The current selection successfully loaded as this selection.',
        logging.info)
    ryw.give_news('You may want to reload the page containing '+
                  'this selection.', logging.info)

    success = reverseLists.redefine_container(
        objID+'#'+str(version), oldContainees, newContainees)
    if not success:
        ryw.give_bad_news('CurrSelToThisSel: ' +
                          'reverseLists.redefine_container failed.',
                          logging.critical)

    reverseLists.done()
    searchFile.done()
    ryw_view.print_footer()
    


if __name__ == '__main__':
    main()


