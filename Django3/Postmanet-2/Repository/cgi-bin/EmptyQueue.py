import os, sys, pickle, math, random, time, shutil
import su
import ryw, ryw_upload, logging
import cgi, cgitb
cgitb.enable()



def main():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('EmptyQueue: entered...')

    ryw.print_header()

    success,rfpath = ryw.get_queue_args()
    if not success:
        sys.exit(1)

    ryw.empty_download_queue(rfpath)
    sys.exit(0)



if __name__ == '__main__':
    main()
