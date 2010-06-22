import cgi, cgitb
cgitb.enable()
import sys, os, ryw_view, ryw, su
import logging


def delAllReq(form):
	all = form.getfirst("all","false")
	if all == "true":
		return True
	return False

def deleteRequested(form):
	image = form.getfirst("Img","")
	if not image:
		print "No Image specified to delete"
		sys.exit(1)
	success, resources = get_resources()
	if not success:
		ryw.give_bad_news("Error parsing resource file",logging.error)
		sys.exit(1)

	robotsJobDir = resources['robotsjobdir']
	jobfile = os.path.join(robotsJobDir, image)
	ryw.cleanup_path(jobfile+".JRQ",'deleteOutgoingImage.deleteRequested:')
	ryw.cleanup_path(jobfile+".ERR",'deleteOutgoingImage.deleteRequested:')
	ryw.cleanup_path(jobfile+".DON",'deleteOutgoingImage.deleteRequested:')
	ryw.cleanup_path(jobfile,'deleteOutgoingImage.deleteRequested:')

	tmpout = resources['tmpout']
	image = os.path.join(tmpout,image)
	if not os.path.exists(image):
		ryw.give_bad_news("specified image doesnt exist",logging.info)
		sys.exit(1)
	ryw.cleanup_path(image,"deleteOutgoingImage.deleteRequested:")
	sys.stdout.write("True")
	sys.exit(0)
	
def main():
	ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
	 
	logging.debug("delete outgoing image entered")
	ryw.print_header()
	form = cgi.FieldStorage()
	if delAllReq(form):
		deleteAll()
	else:
		deleteRequested(form)
	logging.debug("delete image done")
	
def get_resources():
    logging.debug('get_resources: entered...')
    try:
        resources = su.parseKeyValueFile(os.path.join(RepositoryRoot,
                                                      'Resources.txt'))
    except:
        ryw.give_bad_news('get_resources failed.', logging.critical)
        return (False, None)
    
    logging.debug('get_resources succeeded.')
    return (True, resources)
        

def deleteAll():

	print '<TITLE>Deleting Outing Disc Images</TITLE>'
	ryw_view.print_logo()

	success,resources = get_resources()
	if not success:
		logging.error("main: error parsing resource file")
		sys.exit(1)
	 
	outdir = resources['tmpout']
	for i in [os.path.join(outdir,k) for k in os.listdir(outdir)]:
		ryw.cleanup_path(i,"delete outgoing image:")
	robotsjobdir = resources['robotsjobdir']
	for i in [os.path.join(robotsjobdir,k) for k in os.listdir(robotsjobdir)]:
		if os.path.isfile(i):
			ryw.cleanup_path(i,"delete outgoing image:")
	
	ryw.give_good_news("Successfully deleted all outgoing images",logging.debug)
	ryw_view.print_footer()

if __name__ == "__main__":
	main()
