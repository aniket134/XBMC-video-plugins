import sys, os
import su
import cgi, cgitb, xmlrpclib, urllib
cgitb.enable()
import ryw,logging, ryw_view
import ReverseLists



def init_log():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('TestReverseLists: entered...')



def main():
    init_log()
    ryw_view.print_header_logo()
    print '<TITLE>Test ReverseLists</TITLE>'

    success,reverseLists = ReverseLists.open_reverse_lists(
        'TestReverseLists:',
        os.path.join(RepositoryRoot, 'WWW', 'logs'),
        'upload.log',
        os.path.join(RepositoryRoot, 'ReverseLists'),
        False,
        allowNullSearchFile = True)
    if success:
        reverseLists.printme()
        reverseLists.done()
    ryw_view.print_footer()
    


if __name__ == '__main__':
    main()
