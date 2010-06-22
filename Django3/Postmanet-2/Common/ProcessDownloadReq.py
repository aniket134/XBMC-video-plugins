import sys, os
import su
import pickle
import logging
import ryw
import cgi
import SearchFile



def print_header():
    print 'Content-Type: text/plain'
    print



def get_reqs(rfpath):
    if not os.path.exists(rfpath):
        #logging.debug('get_reqs: no existing request found.')
        return set('')

    if not ryw.is_valid_file(rfpath, msg='get_reqs'):
        ryw.give_bad_news('get_reqs: not a valid file: ' + rfpath,
                          logging.error)
        return set('')

    try:
        reqs = su.pickload(rfpath)
        logging.debug('get_reqs: get_reqs succeeded.')
        return reqs
    except:
        ryw.give_bad_news(
            'fatal_error: get_reqs: failed to load requests :' + rfpath, 
            logging.critical)
        return None



def add_reqs(reqs):
    count = 0
    try:
        form = cgi.FieldStorage()
        for item in form.getlist("selection"):
            reqs.add(item)
            count += 1
    except:
        ryw.give_bad_news('fatal_error: AddToQueue: form processing failed.',
                          logging.critical)
        return (False, 0)

    logging.debug('AddToQueue: ' + repr(count) + ' requests processed.')
    return (True, count)



def write_reqs(rfpath, reqs):
    tmppath = rfpath + '.TMP'
    try:
        su.pickdump(reqs, tmppath)
    except:
        ryw.give_bad_news('fatal_error: write_reqs: pickdump failed: ' +
                          tmppath, logging.critical)
        return (False, tmppath, None)

    success,bakpath = ryw.make_tmp_file_permanent(tmppath, rfpath)
    if not success:
        return (False, tmppath, bakpath)

    logging.debug('write_reqs: file write succeeded.')
    return (True, tmppath, bakpath)



def cleanup(tmppath, bakpath):
    ryw.cleanup_path(tmppath, 'cleanup, tmppath:')
    ryw.cleanup_path(bakpath, 'cleanup, bakpath:')



def main(rfpath,logDir,logFile):
    print_header()
    ryw.check_logging(logDir,logFile)
    logging.info('ProcessDownloadReq.main: attempted.')

    reqs = get_reqs(rfpath)
    if reqs == None:
        print "Request for download failed"
        sys.exit(1)

    success,count = add_reqs(reqs)
    if not success:
        print "Request for download failed"
        sys.exit(1)
    if count == 0:
        sys.stdout.write("True")
        sys.exit(0)
    
    success,tmppath,bakpath = write_reqs(rfpath, reqs)
    cleanup(tmppath, bakpath)
    
    if success:
	sys.stdout.write("True")
    else:
	print "Request for download failed"
        


def do_delete(queuePath, reqStr):
    oldReqs = get_reqs(queuePath)
    if oldReqs == None:
        ryw.give_bad_news("ProcessDownloadReq: failed to read queue.",
                          logging.error)
        return False
    
    if not (reqStr in oldReqs):
        ryw.give_bad_news(
            'ProcessDownloadReq:reqStr not found in the queue: ' +
            reqStr + ' not in: ' + repr(oldReqs), logging.warning)
        return False

    oldReqs.remove(reqStr)

    success,tmppath,bakpath = write_reqs(queuePath, oldReqs)
    cleanup(tmppath, bakpath)
    return True        
                          
                          

def delete_request(queuePath):
    print_header()
    success,objID,version = ryw.get_obj_str()
    if not success:
        print "Deletion of request failed."
        sys.exit(1)
    reqStr = objID + '#' + str(version)
    
    success = do_delete(queuePath, reqStr)
    if success:
        sys.stdout.write("True")
    else:
        print "Deletion of request failed."
        sys.exit(1)



def add_all(queueName, searchFile):
    try:
        reqs = set('')

        count = 0
        for meta in searchFile.iterator():
            objstr = meta['id'] + '#' + str(meta['version'])
            reqs.add(objstr)
            count += 1
            logging.debug('add_all: ' + objstr)

        ryw.give_news(
            'add_all: number of objects added to the request queue: ' +
            str(count), logging.info)

        success,tmppath,bakpath = write_reqs(queueName, reqs)
        if not success:
            ryw.give_bad_news('add_all: write_reqs failed: ' + queueName,
                              logging.critical)
            return False
        cleanup(tmppath, bakpath)
        return True
    except:
        ryw.give_bad_news('add_all: failed.', logging.critical)
        return False


class Request_Queue(set):
    def __init__(self):
        set.__init__(self)
        self.file_name = None

    def read(self, file_name):
        requests = su.pickload(file_name)
        for request in requests:
            self.add(request)
        self.file_name = file_name

    def write(self, file_name=None):
        if file_name is not None:
            self.file_name = file_name

        requests = set(self)

        tmp_file_name = self.file_name + '.TMP'
        bak_file_name = self.file_name + '.BAK'

        su.pickdump(requests, tmp_file_name)

        if os.path.exists(self.file_name):
            if os.path.exists(bak_file_name):
                os.remove(bak_file_name)
            os.rename(self.file_name, bak_file_name)

        os.rename(tmp_file_name, self.file_name)

    def add_list(self, l):
        for i in l: # i is of the form 'PKUOVTBQY5XO65RRC7EN#1'
            self.add(i)
