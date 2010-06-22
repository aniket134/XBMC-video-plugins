import sys, os, pickle, objectstore, random, shutil
import logging, datetime, time, zipfile, cStringIO, shutil
import string
import traceback
import ryw_upload,su,SearchFile,ryw_disc,ryw



def copy_tree_diff_file(src, dst):
    """only copies files whose sizes have changed."""
    assert(os.path.exists(src))
    assert(os.path.isfile(src))

    #logging.debug('copy_tree_diff_file: ' + src + ' -> ' + dst)

    try:
        if not os.path.exists(dst):
            #logging.debug('copy_tree_diff_file: copying: ' +
            #              src + ' -> ' + dst)
            shutil.copyfile(src, dst)
            return True

        if os.path.isdir(dst):
            ryw.cleanup_path(dst, 'copy_tree_diff_file:')
            shutil.copyfile(src, dst)
            return True

        assert(os.path.exists(dst))
        assert(os.path.isfile(dst))

        srcSize = os.path.getsize(src)
        dstSize = os.path.getsize(dst)

        if srcSize == dstSize:
            #logging.debug('copy_tree_diff_file: skipping copying: ' +
            #              src + ' -> ' + dst)
            return True

        #logging.debug('copy_tree_diff_file: different sizes, copying: ' +
        #              src + ' -> ' + dst)
        shutil.copyfile(src,dst)
        return True
    except:
        ryw.give_bad_news('copy_tree_diff_file: failed to copy file: ' +
                          src + ' -> ' + dst, logging.critical)
        return False



def copy_tree_diff_dir(src, dst, copyFileFunc, copyDirFunc):
    """normal, except for moving _DONE items to the end of copying..."""
    assert(os.path.exists(src))
    assert(os.path.isdir(src))

    logging.debug('copy_tree_diff_dir: ' + src + ' -> ' + dst)

    try:
        make_dst_dir(src, dst)
        #
        # make sure we copy any _DONE items last.
        #
        dirItems = move_done_last(os.listdir(src))
        success = True
        for n in dirItems:
            srcName = os.path.join(src, n)
            dstName = os.path.join(dst, n)
            #logging.debug(' n is: ' + n)
            thisSuccess = copy_tree_diff_common(srcName, dstName,
                                                copyFileFunc,
                                                copyDirFunc)
            success = success and thisSuccess
        return success
    except:
        ryw.give_bad_news('copy_tree_diff_dir: failed to copy dir: ' +
                          src + ' -> ' + dst, logging.critical)
        return False



def copy_tree_diff_common(src, dst, copyFileFunc, copyDirFunc):
#    check_logging(os.path.join('c:/Postmanet/Nihao', 'WWW', 'repository'),
#                  'upload.log')

    if not os.path.exists(src):
        ryw.give_bad_news('copy_tree_diff_common: source does not exist: ' +
                          src, logging.warning)
        return False

    if os.path.isfile(src):
        return copyFileFunc(src, dst)

    return copyDirFunc(src, dst, copyFileFunc, copyDirFunc)



def get_repo_dir_entries(srcd):
    """returns (success, all_entries, list_of_regular_entries,
    list_of_prefixes)"""

    assert(os.path.exists(srcd))
    assert(os.path.isdir(srcd))

    regularEntries = []
    prefixes = []
    try:
        entries = os.listdir(srcd)
        for entry in entries:
            if ryw.has_store_suffix(entry):
                prefixes.append(ryw.store_name_prefix(entry))
                continue
            regularEntries.append(entry)
        return (True, entries, regularEntries, set(prefixes))
    except:
        ryw.give_bad_news('get_repo_dir_entries: failed for ' + srcd,
                          logging.critical)
        return (False, None, None, None)



def is_big_data(srcd, prefix):
    """return (success,isbig)."""
    datapath = os.path.join(srcd, prefix + '_DATA')
    success,kB = ryw_disc.get_tree_size(datapath)
    if not success:
        return (False, None)
    if kB > ryw.smallFileSizeCeilingKB:
        logging.debug(
            'is_big_data: exceeds small file size ceiling: ' +
            datapath + ': ' + repr(kB) + ' KB')
        #ryw.give_news(
        #    'is_big_data: exceeds small file size ceiling: ' +
        #    datapath + ': ' + repr(kB) + ' KB', logging.info)
        return (True, True)
    return (True, False)



def copy_an_outgoing_object(srcd, dstd, prefix, bigdata = False):
    try:
        sData,sMeta,sAuxi,sDone,sMdon = ryw.get_store_paths(srcd, prefix)
        dData,dMeta,dAuxi,dDone,dMdon = ryw.get_store_paths(dstd, prefix)

        #
        # first deal with data.
        #
        if not bigdata:
            shutil.copytree(sData, dData)
            #logging.debug('copy_an_outgoing_object: copied data: ' +
            #              sData + ' -> ' + dData)
        else:
            #logging.debug('copy_an_outgoing_object: skipping data: ' +
            #              sData)
            #ryw.give_news('copy_an_outgoing_object: skipping data: ' +
            #              sData, logging.info)
	    pass
                
        #
        # now copy metadata.
        #
        shutil.copyfile(sMeta, dMeta)
        #logging.debug('copy_an_outgoing_object: copied metadata: ' +
        #              sMeta + ' -> ' + dMeta)

        #
        # copy the _AUXI directory, skipping big files in them.
        #
        if sAuxi and os.path.exists(sAuxi):
            success = copy_tree_diff_common(sAuxi, dAuxi,
                                            copy_tree_diff_file_repo,
                                            copy_tree_diff_dir_simple)
            if not success:
                raise 'copy_tree_diff_common failed.'
            #logging.debug('copy_an_outgoing_object: copied AUXI files: ' +
            #              sAuxi + ' -> ' + dAuxi)

        #
        # place a done flag.
        #
        if not bigdata:
            shutil.copyfile(sDone, dDone)
            #logging.debug('copy_an_outgoing_object: placed DONE flag: ' +
            #              sDone + ' -> ' + dDone)
        else:
            shutil.copyfile(sDone, dMdon)
            #logging.debug('copy_an_outgoing_object: placed MDON flag: ' +
            #              sDone + ' -> ' + dMdon)
            #ryw.give_news('copy_an_outgoing_object: placed MDON flag: ' +
            #              sDone + ' -> ' + dMdon, logging.info)
        success = True
    except:
        ryw.give_bad_news('copy_an_outgoing_object: failed: ' +
                          srcd + ' ' + dstd + ' ' + prefix + ' ' +
                          repr(bigdata), logging.critical)
        success = False

    ryw.cleanup_partial_repo_dir(dstd, [prefix])
    return success



def process_repo_dir(srcd, dstd, copyFileFunc, copyDirFunc):
    #check_village_log('test process_repo_dir')
    success,entries,regularEntries,prefixes = get_repo_dir_entries(srcd)
    goodPrefixes = ryw.cleanup_partial_repo_dir(srcd, prefixes)
    # logging.debug('goodPrefixes: ' + repr(goodPrefixes))
    # logging.debug('regular: ' + repr(regularEntries))

    success = True
    for regular in regularEntries:
        srcName = os.path.join(srcd, regular)
        dstName = os.path.join(dstd, regular)
        logging.debug(' regular is: ' + regular)
        thisSuccess = copy_tree_diff_common(srcName, dstName,
                                            copyFileFunc, copyDirFunc)
        success = success and thisSuccess

    for prefix in goodPrefixes:
        success,isBig = is_big_data(srcd, prefix)
        if not success:
            ryw.give_bad_news(
                'process_repo_dir: failed to determine data size: '+srcd,
                logging.warning)
            continue
        thisSuccess = copy_an_outgoing_object(srcd, dstd, prefix,
                                              bigdata = isBig)
        success = success and thisSuccess
        
    return success



def make_dst_dir(src, dst):
    src = os.path.normpath(src)
    dst = os.path.normpath(dst)

    if not os.path.exists(dst):
        su.createdirpath(dst)
    elif os.path.isfile(dst):
        cleanup_path(dst, 'make_dst_dir:')
        su.createdirpath(dst)

    assert(os.path.exists(dst))
    assert(os.path.isdir(dst))



def copy_tree_diff_dir_repo(src, dst, copyFileFunc, copyDirFunc):
    """used during recursive copying of object store:
    _DATA directories that are too big are not copied."""
    
    #logging.debug('copy_tree_diff_dir_repo: ' + src + ' -> ' + dst)

    assert(os.path.exists(src))
    assert(os.path.isdir(src))

    try:
        make_dst_dir(src, dst)
        return process_repo_dir(src, dst, copyFileFunc, copyDirFunc)
    except:
        ryw.give_bad_news('copy_tree_diff_dir_repo: failed to copy dir: ' +
                          src + ' -> ' + dst, logging.critical)
        return False



def copy_tree_diff_file_repo(src, dst):
    """used during recursive copying of the object store:
    files that are too big are not copied."""
    
    assert(os.path.exists(src))
    assert(os.path.isfile(src))

    #logging.debug('copy_tree_diff_file_repo: ' + src + ' -> ' + dst)

    try:
        src = os.path.normpath(src)
        dst = os.path.normpath(dst)
        srcBase = os.path.basename(src)

        kB = os.path.getsize(src) / 1024
        if kB > ryw.smallFileSizeCeilingKB:
            #logging.debug(
            #    'copy_tree_diff_file_repo: ' +
            #    'exceeds small file size ceiling: ' +
            #    src + ' ' + repr(kB) + ' KB')
            #ryw.give_news('copy_tree_diff_file_repo: ' +
            #              'exceeds small file size ceiling: ' +
            #              src + ' ' + repr(kB) + ' KB', logging.info)
            return True
        #logging.debug('copy_tree_diff_file_repo: ' +
        #      'does not exceed small file size ceiling: ' +
        #      src + ' ' + repr(kB) + ' KB')

        return copy_tree_diff_file(src, dst)
    except:
        ryw.give_bad_news('copy_tree_diff_file_repo: failed to copy file: ' +
                          src + ' -> ' + dst, logging.critical)
        return False



def move_done_last(origList):
    """move any _DONE item to the end of the list."""
    
    copyList = list(origList)
    doneList = []
    for item in origList:
        suffix = item[-5:]
        if suffix != '_DONE' and suffix != '_done' and \
           suffix != '_MDON' and suffix != '_mdon':
            continue
        copyList.remove(item)
        doneList.append(item)
    return copyList + doneList



def copy_tree_diff_file_view(src, dst):
    """always copy leaves."""
    assert(os.path.exists(src))
    assert(os.path.isfile(src))

    logging.debug('copy_tree_diff_file_view: ' + src + ' -> ' + dst)

    try:
        if os.path.exists(dst) and os.path.isdir(dst):
            ryw.cleanup_path(dst, 'copy_tree_diff_file:')

        shutil.copyfile(src, dst)
        return True
    except:
        ryw.give_bad_news('copy_tree_diff_file_view: failed to copy file: ' +
                          src + ' -> ' + dst, logging.critical)
        return False



def copy_tree_diff_dir_simple(src, dst, copyFileFunc, copyDirFunc):
    assert(os.path.exists(src))
    assert(os.path.isdir(src))

    #logging.debug('copy_tree_diff_dir_simple: ' + src + ' -> ' + dst)

    try:
        make_dst_dir(src, dst)
        
        dirItems = os.listdir(src)
        success = True
        for n in dirItems:
            srcName = os.path.join(src, n)
            dstName = os.path.join(dst, n)
            #logging.debug(' n is: ' + n)
            thisSuccess = copy_tree_diff_common(srcName, dstName,
                                                copyFileFunc,
                                                copyDirFunc)
            success = success and thisSuccess
        return success
    except:
        ryw.give_bad_news('copy_tree_diff_dir_simple: failed to copy dir: ' +
                          src + ' -> ' + dst, logging.critical)
        return False



def copy_tree_diff(src, dst):
    """similar to su.copytree(), but does incremental copying if
    the destination is already partially populated.  does not copy files
    whose sizes have not changed.  and copies _DONE items last."""
    return copy_tree_diff_common(src, dst,
                                 copy_tree_diff_file,
                                 copy_tree_diff_dir)



def copy_tree_diff_view(src, dst):
    """used to copy a view.  always copies the leaf files.
    fileFunc: always copies leaves.
    dirFunc: copies everything."""
    return copy_tree_diff_common(src, dst,
                                 copy_tree_diff_file_view,
                                 copy_tree_diff_dir_simple)



def copy_tree_diff_repo(src, dst):
    """used to copy an object store to a village.
    data that's too big are skipped.
    fileFunc: skips big files.
    dirFunc: very repository specific, cleans up and looks at obj store."""
    return copy_tree_diff_common(src, dst,
                                 copy_tree_diff_file_repo,
                                 copy_tree_diff_dir_repo)
