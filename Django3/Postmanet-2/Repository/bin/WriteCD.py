sys.path.append(os.path.join(RepositoryRoot, 'bin'))
import sys, os
import su
import pickle, AddRobotWriteRequest, math, xmlrpclib, objectstore
import logging, ryw, ryw_disc, SearchFile, ryw_upload, ryw_copytree



#
# there might be consistency issues here if people are simultaneously
# updating the download queue.
#



#
# def get_paths():
#    username = sys.argv[1]
#    logging.debug('WriteCDs: username: '+username)
#
#    rfpath = os.path.join(RepositoryRoot, 'QUEUES', username)
#
#    if not os.path.exists(rfpath):
#        return (True, username, rfpath, set([]))
#
#    try:
#        reqs = su.pickload(rfpath)
#    except:
#        ryw.give_bad_news('get_paths: failed to load reqs: ' +
#                          rfpath, logging.critical)
#        return (False, None, None, None)
#
#    logging.debug('get_paths: found queue, reqs: '+repr(reqs))
#    return (True, username, rfpath, reqs)
#



# noObjStore:
def obj_store_size_inKB(tmpdir=""):
    ryw.give_news2('skipping computing objectstore size...', logging.info)
    return (True, 0, None, None)



def obj_store_size_inKB_not_used(tmpdir=""):
    if tmpdir:
        ryw.give_news2('temp objectstore copied to: ' + tmpdir + '<BR>',
                       logging.info)
    ryw.give_news2('computing outgoing objectstore size...',
                   logging.info)
    
    try:
        resources = su.parseKeyValueFile(os.path.join(RepositoryRoot,
                                                      'Resources.txt'))
        objectstoreroots = resources['objectstore'].split(';')
        firstRoot = objectstoreroots[0]
        if tmpdir:
                tmpOutDir = tmpdir
        else:
                tmpOutDir = resources['tmpout']
    except:
        ryw.give_bad_news('obj_store_size_inKB: get_resources failed.',
                          logging.critical)
        return (False, None, None, None)

    tmpStoreDir,objPrefix = ryw_upload.attempt_just_make_tmpdir(
        tmpOutDir, 'outgoing_obj_store_', '')
    if not tmpStoreDir:
        ryw.give_bad_news('obj_store_size_inKB: failed to make tmpdir: ' +
                          tmpOutDir, logging.critical)
        return (False, None, None, None)

    tmpStoreName = os.path.join(tmpStoreDir, 'outgoing_store')

    try:
        success = ryw_copytree.copy_tree_diff_repo(firstRoot, tmpStoreName)
        if not success:
            raise 'copy_tree_diff_repo failed.'
    except:
        ryw.give_bad_news('obj_store_size_inKB: copy_tree_diff_repo failed: '+
                          firstRoot + ' -> ' + tmpStoreName, logging.critical)
        return (False, None, None, None)

    kB = ryw_disc.getRecursiveSizeInKB(tmpStoreName)
    logging.debug('obj_store_size_inKB: ' + tmpStoreName + ' = ' + str(kB))

    ryw.give_news2 (str(kB) + ' KB<BR>', logging.info)
    return (True, kB, tmpStoreDir, tmpStoreName)



def get_pathsFunc(name):
    username = name
    logging.debug('WriteCDs: username: '+username)

    rfpath = os.path.join(RepositoryRoot, 'QUEUES', username)

    if not os.path.exists(rfpath):
        return (True, username, rfpath, set([]))

    try:
        reqs = su.pickload(rfpath)
    except:
        ryw.give_bad_news('get_paths: failed to load reqs: ' +
                          rfpath, logging.critical)
        return (False, None, None, None)

    logging.debug('get_paths: found queue, reqs: '+repr(reqs))
    return (True, username, rfpath, reqs)



def collect_req_info(reqs, objKB):
    logging.debug('collect_req_info: entered...')

    success,searchFile = ryw.open_search_file(
        'collect_req_info:',
        os.path.join(RepositoryRoot, 'WWW', 'logs'),
        'upload.log',
        os.path.join(RepositoryRoot, 'SearchFile'),
        False)
    if not success:
        return(False, None, None, None)

    reqsize = {}
    reqpath = {}
    reqList = []
    for item in reqs:
        logging.debug('collect_req_info: item is: '+item)
        try:
            objname, version = item.split('#')
            version = int(version)
        except:
            ryw.give_bad_news(
                'collect_req_info: bad format, split failed: '+item,
                logging.error)
            continue
            
        logging.debug('collect_req_info, obj, version: ' +
                      objname + ' ' + repr(version))

        success,metaData = searchFile.get_meta(objname, version)
        if not success:
            ryw.give_bad_news(
                'collect_req_info: failed to get_meta.',
                logging.error)
            continue
            
        #
        # I'm doing this to hardwire all
        # places of gettting objectstoreroot.
        #
        #objroot = metaData['objectstore']
        objroot = ryw.hard_wired_objectstore_root()

        try:
            itempath = objectstore.name_version_to_paths_aux(objroot, objname,
                                                             version)
        except:
            ryw.give_bad_news(
                'collect_req_info: nameversiontopaths failed: ' +
                objroot + ' ' + objname + ' ' + repr(version),
                logging.critical)
            continue
                
        logging.debug('collect_req_info: after getting itempath...' +
                      repr(itempath))

        if not ryw.good_repo_paths(itempath):
            ryw.give_bad_news('collect_req_info: check_obj_paths failed.',
                              logging.error)
            continue

        success,itemSize = ryw.get_obj_size(itempath)
        if not success:
            continue
        
        logging.debug('collect_req_info, size in KB is: ' + repr(itemSize))

        if (itemSize > ryw.maxSizeInKB - objKB):
            ryw.give_bad_news(
                'collect_req_info: item size too big to fit on one disc: ' +
                repr(itemSize), logging.error)
            continue

        reqsize[item] = itemSize
        reqpath[item] = itempath
        logging.debug('collect_req_info: size, path: ' +
                      repr(itemSize) + ' ' + itempath[0])

        # build a list for sorting.
        reqItem = {}
        reqItem['name'] = item
        if metaData.has_key('upload_datetime'):
            reqItem['upload_datetime'] = metaData['upload_datetime']
        reqList.append(reqItem)

    searchFile.done()
    reqList.sort(key = ryw.datetimesortkey, reverse = False)

    sortedItems = []
    for r in reqList:
        sortedItems.append(r['name'])
    
    return (True, reqsize, reqpath, sortedItems)

#
#def make_discs(reqsize, reqpath, username, objKB, tmpStoreName, reqList):
#    # make at least one CD
#    # make more than one if the requested data does not fit in one CD
#    countCDs = 0
#    finishedStuff = []
#    remainingItems = list(reqList)
#    while True:
#        # make a CD
#        currentSize = 0
#        yes = []
#
#        # logging.debug('make_discs: before, reqList is: ' + repr(reqList))
#
#        for item in reqList:
#            # logging.debug('make_discs: item is: ' + item)
#            # logging.debug('    reqsize for item is: ' + repr(reqsize[item]))
#            # logging.debug('    currentSize is: ' + repr(currentSize))
#            if currentSize + reqsize[item] <= ryw.maxSizeInKB - objKB:
#                currentSize += reqsize[item]
#                yes.append(item)
#                del reqsize[item]
#                remainingItems.remove(item)
#            else:
#                break
#                # logging.debug('make_discs: size too big for this disc.')
#        reqList = list(remainingItems)
#
#        # logging.debug('make_discs: after, reqList is: ' + repr(reqList))
#        # logging.debug('make_discs: yes set is: ' + repr(yes))
#
#        # make CD with the requests in 'yes'
#        logging.debug('make_discs: about to add to robot: ' + repr(yes))
#        # deliberately not catching exceptions for now.
#        success,tmpImgDir,jrq = AddRobotWriteRequest.addRobotWriteRequest(
#            username, yes, reqpath, currentSize, tmpStoreName)
#        if not success:
#            ryw.give_bad_news('make_discs: addRobotWriteRequest failed: ' +
#                              username + ' ' + repr(yes), logging.error)
#            return (False, countCDs, finishedStuff)
#
#        finishedStuff.append((tmpImgDir, jrq))
#        
#        countCDs += 1
#        logging.debug('make_discs: done adding to robot: disc #' +
#                      repr(countCDs))
#        ryw.give_news2('<BR>', logging.info)
#        ryw.give_news2('sent disc # ' + str(countCDs) +
#                      ' to the robot...', logging.info)
#        ryw.give_news2('<BR>', logging.info)
#
#        if len(reqsize) != len(reqList):
#            ryw.give_bad_news('make_discs: unexpected list size mismatch.',
#                              logging.critical)
#        if len(reqsize) == 0:
#            break
#
#    ryw.give_news2('finished sending ' + str(countCDs) +
#                   ' disc(s) to the robot...', logging.info)
#    ryw.give_news2('<BR>', logging.info)
#    logging.debug('make_discs: produced ' + repr(countCDs) + ' discs.')
#    logging.debug('make_discs: finishedStuff: ' + repr(finishedStuff))
#    return (True, countCDs, finishedStuff)


def make_discs(reqsize, reqpath, username, objKB, tmpStoreName,
               reqList, tmpDirOption="", metaOnly = False):
    # make at least one CD
    # make more than one if the requested data does not fit in one CD
    countCDs = 0
    remainingItems = list(reqList)
    while True:
        # make a CD
        currentSize = 0
        yes = []

        # logging.debug('make_discs: before, reqList is: ' + repr(reqList))

        for item in reqList:
            # logging.debug('make_discs: item is: ' + item)
            # logging.debug('    reqsize for item is: ' + repr(reqsize[item]))
            # logging.debug('    currentSize is: ' + repr(currentSize))
            if metaOnly or currentSize + reqsize[item] <= ryw.maxSizeInKB - objKB:
                currentSize += reqsize[item]
                yes.append(item)
                del reqsize[item]
                remainingItems.remove(item)
            else:
                break
                # logging.debug('make_discs: size too big for this disc.')
        reqList = list(remainingItems)

        # logging.debug('make_discs: after, reqList is: ' + repr(reqList))
        # logging.debug('make_discs: yes set is: ' + repr(yes))

        # make CD with the requests in 'yes'
        logging.debug('make_discs: about to add to robot: ' + repr(yes))
        # deliberately not catching exceptions for now.
        success,tmpImgDir, jrq = \
            AddRobotWriteRequest.addRobotWriteRequest( \
                username, yes, reqpath, currentSize, tmpStoreName,
                tmpDirOption = tmpDirOption,
                onlyMeta = metaOnly)
        if not success:
            ryw.give_bad_news('make_discs: addRobotWriteRequest failed: ' +
                              username + ' ' + repr(yes), logging.error)
            return (False, countCDs)

        countCDs += 1
        logging.debug('make_discs: done adding to robot: disc #' +
                      repr(countCDs))
        ryw.give_news2('<BR>', logging.info)
        ryw.give_news2('sent disc # ' + str(countCDs) +
                      ' to the robot...', logging.info)
        ryw.give_news2('<BR>', logging.info)

        if len(reqsize) != len(reqList):
            ryw.give_bad_news('make_discs: unexpected list size mismatch.',
                              logging.critical)
        if len(reqsize) == 0:
            break

    ryw.give_news2('finished sending ' + str(countCDs) +
                   ' disc(s) to the robot...', logging.info)
    ryw.give_news2('<BR>', logging.info)
    logging.debug('make_discs: produced ' + repr(countCDs) + ' discs.')
    return (True, countCDs)


    
#
#def main():
#    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
#                      'upload.log')
#    logging.debug('WriteCD.py: attempted...')
#
#    success,username,rfpath,reqs = get_paths()
#    if not success:
#        sys.exit(1)
#
#    success,reqsize,reqpath = collect_req_info(reqs)
#    if not success:
#        sys.exit(1)
#
#    success,countCDs = make_discs(reqsize, reqpath, username)
#    if not success:
#        sys.exit(1)
#
#    empty_download_queue(rfpath)
#    sys.exit(0)

    

def confirm_delete_queue(rfpath):
    ryw.give_news(' ', logging.info)
    ryw.give_news('<B><A HREF=/cgi-bin/ClearQueue.py' +
                  '>empty the download queue?</A></B><br>',
                  logging.info )



def mainFunc(name, tmpdir="", onlyMeta=False, discLimit=None):

    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('WriteCD.py: attempted... tmpdir: ' + tmpdir)

    if discLimit:
        ryw.set_disc_limit(discLimit)
        #ryw.give_news2('WriteCD.py: disc size set to: ' +
        #               str(ryw.maxSizeInKB), logging.info)

    success,username,rfpath,reqs = get_pathsFunc(name)
    if not success:
        ryw.give_bad_news('WriteCD failed.', logging.error)
        return

    success,objKB,tmpStoreDir,tmpStoreName = \
        obj_store_size_inKB(tmpdir=tmpdir)
    if not success:
        ryw.give_bad_news('WriteCD failed.', logging.critical)
        ryw.cleanup_path(tmpStoreDir, 'WriteCD.mainFunc:')
        return

    success,reqsize,reqpath,reqList = collect_req_info(reqs, objKB)
    if not success:
        ryw.give_bad_news('WriteCD failed.', logging.error)
        ryw.cleanup_path(tmpStoreDir, 'WriteCD.mainFunc:')
        return

    success,countCDs = make_discs(reqsize, reqpath, username,
                                  objKB, tmpStoreName, reqList,
                                  tmpDirOption=tmpdir,
                                  metaOnly = onlyMeta)
    if not success:
        ryw.give_bad_news('WriteCD failed.', logging.error)
        ryw.cleanup_path(tmpStoreDir, 'WriteCD.mainFunc:')
        return

#    empty_download_queue(rfpath)
    ryw.give_good_news('Apparent success: number of CDs made = '
                       + repr(countCDs), logging.info)
#    ryw.cleanup_path(tmpStoreDir, 'WriteCD.mainFunc:')
    confirm_delete_queue(rfpath)


def mainFunc_old(name):
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('WriteCD.py: attempted...')

    success,username,rfpath,reqs = get_pathsFunc(name)
    if not success:
        ryw.give_bad_news('WriteCD failed.', logging.error)
        return

    success,objKB,tmpStoreDir,tmpStoreName = obj_store_size_inKB()
    if not success:
        ryw.give_bad_news('WriteCD failed.', logging.critical)
        ryw.cleanup_path(tmpStoreDir, 'WriteCD.mainFunc:')
        return

    success,reqsize,reqpath,reqList = collect_req_info(reqs, objKB)
    if not success:
        ryw.give_bad_news('WriteCD failed.', logging.error)
        ryw.cleanup_path(tmpStoreDir, 'WriteCD.mainFunc:')
        return

    success,countCDs,finishedStuff = make_discs(reqsize, reqpath, username,
                                                objKB, tmpStoreName, reqList)
    if not success:
        ryw.give_bad_news('WriteCD failed.', logging.error)
        ryw.cleanup_path(tmpStoreDir, 'WriteCD.mainFunc:')
        return

#    AddRobotWriteRequest.wait_for_robot(finishedStuff)

#    empty_download_queue(rfpath)
    ryw.give_good_news('Apparent success: number of CDs made = '
                       + repr(countCDs), logging.info)

#    ryw.cleanup_path(tmpStoreDir, 'WriteCD.mainFunc:')
    confirm_delete_queue(rfpath)
    giveQManagementLink()

def giveQManagementLink():
    ryw.give_news('<B><A HREF=/cgi-bin/ViewPendingBurns.py' +
                  '>Manage Queue of disc images waiting to be burned.</A></B><br>',
                  logging.info )

#main()
