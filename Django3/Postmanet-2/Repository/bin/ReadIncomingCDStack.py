import os, sys, pickle, math, random, time, shutil
import su
import ryw, ryw_upload, logging



def get_init_vals():
    numDiscs = 1000
    try:
        resources = su.parseKeyValueFile(
            os.path.join(RepositoryRoot, 'Resources.txt'))
        robotJobsDir = resources['robotsjobdir']
        tmpIn = resources['tmpin']            
    except:
        ryw.give_bad_news('get_init_vals: failed to get resources: ' +
                          os.path.join(RepositoryRoot, 'Resources.txt'),
                          logging.critical)
        return (False, None, None, None, None)
    return (True, numDiscs, resources, robotJobsDir, tmpIn)



def robot_read_all(robotJobsDir, objPrefix, numDiscs, tmpdir):
    """issue a read-all request to the robot."""
    jobFile = os.path.join(robotJobsDir, 'R_' + objPrefix)
    try:
        f = open(jobFile, 'w')
        f.write('ClientID=localhost\n')
        f.write('JobID=R_' + objPrefix + '\n')
        f.write('Copies=' + str(numDiscs) + '\n')
        f.write('ReadDataTo=' + tmpdir + '\n')
        f.write('ReadDataFormat=ReadData\n')
        f.write('CreateSubFolders=YES\n')
        f.close()
        jrq = jobFile + '.JRQ'
        os.rename(jobFile, jrq)
    except:
        ryw.give_bad_news(
            'robot_read_all: failed to write robot job file:' +
            jobFile, logging.critical)
        return None

    logging.info('robot_read_all: job file written: ' + jobFile)
    return jobFile



def check_finished(jobFile, tmpdir):
    """returns successFlag, doneFlag, doneList."""

    doneFlag = ryw_upload.check_robot_finished(jobFile)
    if not doneFlag:
        return (True, False, None)
    
    try:
        doneList = os.listdir(tmpdir)
    except:
        ryw.give_bad_news(
            'ReadIncomingCDStack.check_finished: listdir failed: ' +
            tmpdir, logging.critical)
        return (False, True, None)
    logging.debug('ReadIncomingCDStack.check_finished: listdir contents: ' +
                  repr(doneList))
    return (True, True, doneList)



def check_partial_completion(tmpdir):
    """returns successFlag, doneList."""
    try:
        ll = os.listdir(tmpdir)
        ctime = {}
        for n in ll:
            ctime[n] = os.path.getctime(os.path.join(tmpdir, n))
    except:
        ryw.give_bad_news(
            'ReadIncomingCDStack.check_partial_completion: failed listdir ' +
            'getctime: ' + tmpdir, logging.critical)
        return (False, None)
        
    latestctime = 0
    latestname = ''
    for n in ll:
        if ctime[n] > latestctime:
            latestctime = ctime[n]
            latestname = n
            
    donelist = []
    if latestctime != 0:
        logging.debug('check_partial_completion: latestname: ' + latestname)
        for n in ll:
            if n != latestname:
                donelist.append(n)

    logging.debug('check_partial_completion: donelist: ' + repr(donelist))
    return (True, donelist)



def NOTUSED_main_overlap():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('ReadIncomingCDStack: entered...')

    success,numDiscs,resources,robotJobsDir,tmpIn = get_init_vals()
    if not success:
        sys.exit(1)

    freeGB = ryw.free_MB(tmpIn) / 1000.0
    ryw.give_news('ReadIncomingCDStack: current available disk space: ' +
                  repr(freeGB) + ' GB.', logging.info)

    tmpdir,objPrefix = ryw_upload.attempt_just_make_tmpdir(tmpIn,
                                                           'I_',
                                                           '')
    if not tmpdir:
        ryw.give_bad_news('ReadIncomingCDStack: failed to make tmpdir.',
                          logging.critical)
        sys.exit(1)

    jobFile = robot_read_all(robotJobsDir, objPrefix, numDiscs, tmpdir)
    if not jobFile:
        ryw_upload.cleanup_incoming(tmpdir, jobFile)
        sys.exit(1)

    # monitor the robot's job folder for completion of job
    # also periodically monitor the tmp folder for completed disk reads

    while True:
        ryw.give_news2('*', logging.info)
        time.sleep(5)
        logging.debug('ReadIncomingCDStack: done sleeping...')

        success,done,doneList = check_finished(jobFile, tmpdir)
        if not success:
            ryw_upload.cleanup_incoming(tmpdir, jobFile)
            sys.exit(1)

        if not done:
            success,doneList = check_partial_completion(tmpdir)
            if not success:
                ryw_upload.cleanup_incoming(tmpdir, jobFile)
                sys.exit(1)

        process_finished_copies(tmpdir, doneList)

        if done:
            logging.debug('ReadIncomingCDStack: done.')
            break

    logging.debug(
        'ReadIncomingCDStack: removing robot job data: ' +
        tmpdir + ' ' + jobFile)
    ryw_upload.cleanup_incoming(tmpdir, jobFile)



def print_done_discs(doneList, oldDone):
    for d in (set(doneList) - set(oldDone)):
        ryw.give_news(' ' + d + ' ', logging.info)
        ryw.give_news(' ', logging.info)



def print_conclusion(doneList, tmpdir, jobFile):
    length = len(doneList)
    if length > 0:
        ryw.give_news(' ', logging.info)
        ryw.give_news('number of discs copied: ' + str(length),
                      logging.info)
        ryw.give_news('<B><A HREF=/cgi-bin/ProcessDiscs.py?tmpdir=' +
                      tmpdir + '&jobfile=' + jobFile +
                      '>process these discs</A></B><br>',
                      logging.info )
    else:
        ryw.give_news('no incoming disc copied.', logging.info)
    


def main_nonoverlap():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('ReadIncomingCDStack: entered...')

    success,numDiscs,resources,robotJobsDir,tmpIn = get_init_vals()
    if not success:
        sys.exit(1)

    freeGB = ryw.free_MB(tmpIn) / 1000.0
    ryw.give_news('current available disk space: ' +
                  repr(freeGB) + ' GB.', logging.info)

    tmpdir,objPrefix = ryw_upload.attempt_just_make_tmpdir(tmpIn,
                                                           'I_',
                                                           '')
    if not tmpdir:
        ryw.give_bad_news('ReadIncomingCDStack: failed to make tmpdir.',
                          logging.critical)
        sys.exit(1)

    ryw.give_news('begin copying incoming discs...', logging.info)

    jobFile = robot_read_all(robotJobsDir, objPrefix, numDiscs, tmpdir)
    if not jobFile:
        ryw_upload.cleanup_incoming(tmpdir, jobFile)
        sys.exit(1)

    # monitor the robot's job folder for completion of job.

    ryw.give_news('', logging.info)
    oldDone = []
    while True:
        ryw.give_news2('*', logging.info)
        time.sleep(5)
        logging.debug('ReadIncomingCDStack: done sleeping...')

        success,done,doneList = check_finished(jobFile, tmpdir)
        if not success:
            ryw_upload.cleanup_incoming(tmpdir, jobFile)
            sys.exit(1)

        if not done:
            success,doneList = check_partial_completion(tmpdir)
            if not success:
                ryw_upload.cleanup_incoming(tmpdir, jobFile)
                sys.exit(1)

        #process_finished_copies(tmpdir, doneList)
        print_done_discs(doneList, oldDone)
        oldDone = doneList

        if done:
            logging.debug('ReadIncomingCDStack: done.')
            break
        
    print_conclusion(doneList, tmpdir, jobFile)

    

def main():
    main_nonoverlap()

    

if __name__ == '__main__':
    main()
