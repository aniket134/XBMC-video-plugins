import sys, os
import su
import pickle
import logging
import cgi
import ryw, ryw_view



def main():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.info('ClearTmp: entered...')

    ryw_view.print_header_logo()

    try:
        resources = su.parseKeyValueFile(os.path.join(RepositoryRoot,
                                                      'Resources.txt'))
        resTmpin  = resources['tmpin']
        resTmpOut = resources['tmpout']
        robotDir  = resources['robotsjobdir']
    except:
        ryw.give_bad_news('failed to parse resource file.', logging.critical)
        sys.exit(1)


    ryw.empty_tmp_dir(resTmpin, chmodFirst = True)
    ryw.empty_tmp_dir(resTmpOut)
    ryw.empty_tmp_dir(robotDir, skipList = ['Status', 'Log'])

    ryw_view.print_footer()
    sys.exit(0)



if __name__ == '__main__':
    main()
