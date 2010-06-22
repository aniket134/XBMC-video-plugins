import os,ryw,logging,sys,ryw_view,cgi,shutil
import ProcessDownloadReq
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import DisplaySelection,DeleteRepReq



def get_file_path(searchFile = None, allowNullSearchFile = False):
    success,objID,version = ryw.get_obj_str()
    if not success:
        ryw.give_bad_news('ThisSelToCurrSel: failed to get objstr.',
                          logging.critical)
        return None

    rfpath = DisplaySelection.get_file_path(
        objID, version, searchFile = searchFile,
        allowNullSearchFile = allowNullSearchFile)
    return rfpath
    


def main():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('ThisSelToCurrSel: entered...')
    ryw_view.print_header_logo()

    rfpath = get_file_path(allowNullSearchFile = True)
    if not rfpath:
        ryw.give_bad_news(
            'ThisSelToCurrSel: no selection file name found.',
            logging.error)
        DisplaySelection.exit_now(1)

    queueName = DeleteRepReq.get_queue_name()
    if not queueName:
        ryw.give_bad_news(
            'ThisSelToCurrSel: failed to get current selection file name.',
            logging.error)
        DisplaySelection.exit_now(1)

    try:
        shutil.copyfile(rfpath, queueName)
    except:
        ryw.give_bad_news('ThisSelToCurrSel: failed to overwrite: ' +
                          rfpath + ' -> ' + queueName,
                          logging.critical)
        DisplaySelection.exit_now(1)

    ryw.give_news(
        'This selection successfully loaded as the current selection.',
        logging.info)
    ryw.give_news('You may want to reload the page containing '+
                  'the affected current selection.', logging.info)
    ryw_view.print_footer()
    


if __name__ == '__main__':
    main()


