import os, sys, pickle, math, random, time, shutil
import su
import ryw, ryw_upload, logging, SearchFile, ProcessDownloadReq, ryw_view
import cgi, cgitb
cgitb.enable()



def main():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('SelectAll: entered...')

    ryw_view.print_header_logo()

    name = os.getenv("REMOTE_USER")

    if name == "" or name == None:
	ryw.give_bad_news('SelectAll: no user name given', logging.error)
        ryw_upload.quick_exit(1)

    queue = os.path.join(RepositoryRoot, 'QUEUES', name)

    try:
        resources = su.parseKeyValueFile(os.path.join(RepositoryRoot,
                                                      'Resources.txt'))
        searchFileName = resources['searchfile']
    except:
        ryw.give_bad_news(
            'SelectAll: failed to get search file name from resources.',
            logging.critical)
        ryw_upload.quick_exit(1)

    success,searchFile = ryw.open_search_file(
        'SelectAll:',
        os.path.join(RepositoryRoot,'WWW','logs'),
        'upload.log',
        searchFileName,
        False)
    if not success:
        ryw.give_bad_news(
            'SelectAll: failed to open search file.', logging.critical)
        ryw_upload.quick_exit(1)

    if not ProcessDownloadReq.add_all(queue, searchFile):
        ryw.give_bad_news('selectall: addAll failed.', logging.critical)
        ryw_upload.quick_exit(1)

    searchFile.done()
    ryw_upload.quick_exit(0)



if __name__ == '__main__':
    main()
