import os,ryw,logging,sys
import ProcessDownloadReq



def get_queue_name():
    name = os.getenv("REMOTE_USER")
    if name == "" or name == None:
        ryw.give_bad_news('DeleteRepReq: no user name given.',
                          logging.critical)
        return None
    queue = os.path.join(RepositoryRoot, 'QUEUES', name)
    return queue



def main():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('DeleteRepReq: entered...')
    queueName = get_queue_name()
    if not queueName:
        sys.exit(1)
    ProcessDownloadReq.delete_request(queueName)



if __name__ == '__main__':
    main()

