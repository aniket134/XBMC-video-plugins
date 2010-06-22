import cgi, cgitb, logging
cgitb.enable()
import sys, os, ryw_view, ryw
sys.path.append(os.path.join(RepositoryRoot, 'bin'))
import WriteCD



name = os.getenv("REMOTE_USER")

ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                  'upload.log')
logging.debug('FlushQueue: entered...')

ryw.print_header()
print '<TITLE>Generating Outgoing Disc</TITLE>'
ryw_view.print_logo()

#print 'Dear <B><I>' + name + ':</I></B>'


form = cgi.FieldStorage()
tmpdir = form.getfirst("tmpdir","")

if tmpdir and not ryw.is_valid_dir(tmpdir, 'FlushQueue'):
    ryw_view.print_footer()
    sys.exit(1)


meta = form.getfirst('meta', '')
metaOnly = meta == 'true' or meta == 'on'
if metaOnly:
    ryw.give_news2('sending metadata only.<BR>', logging.info)


discLimit = form.getfirst('disc_limit', '')
discLimitInt = None
if discLimit:
    try:
        discLimitInt = int(discLimit)
    except:
        ryw.give_bad_news('FlushQueue.py: bad disc limit: ' + discLimit,
                          logging.error)
        ryw_view.print_footer()
        sys.exit(1)

if discLimitInt and (discLimitInt < 10 or discLimitInt > 1000000):
    ryw.give_bad_news("The disc limit size should be somewhere between "+
                      "10MB and 1TB.", logging.error)
    ryw_view.print_footer()
    sys.exit(1)
elif discLimitInt:
    ryw.give_news2('disc size limit set to: ' + str(discLimitInt) +
                   ' MB<BR>', logging.info)    
            

#ryw.give_news2('your disc is being generated...<BR>', logging.info)

WriteCD.mainFunc(name,tmpdir=tmpdir,
                 onlyMeta=metaOnly,
                 discLimit=discLimitInt)

ryw_view.print_footer()
