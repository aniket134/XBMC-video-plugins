import cgi, cgitb
cgitb.enable()
import sys, os
import ryw,logging,ryw_view



ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                  'upload.log')
logging.debug('ClearQueue: entered...')

ryw_view.print_header_logo()
name = os.getenv("REMOTE_USER")

print '<TITLE>Clear Requests</TITLE>'

ryw.give_news('Dear <B><I>' + name + ':</I></B>', logging.info)


rfpath = os.path.join(RepositoryRoot, 'QUEUES', name)
ryw.empty_download_queue(rfpath)

ryw.give_news('<p>Current selection is now empty.', logging.info)

ryw_view.print_footer()


