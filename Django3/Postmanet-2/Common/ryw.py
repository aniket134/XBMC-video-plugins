import sys, os, pickle, cgi, cgitb, xmlrpclib, objectstore, random, shutil
import ad
import logging, datetime, time, zipfile, cStringIO, shutil
import string
import traceback
import ryw_upload,su,SearchFile,ryw_disc,stat, Search
import ryw_bizarro
cgitb.enable()
import md5, re




#
# used by the db_print*() functions near the end of this file.
#
RYW_DEBUG_TAG = 102

#
# if the tag is one of these, then (for now), db_print3() will always print.
# the other db_print() function could be changed to do this over time as well.
#
# 50: in install-repository-lai.py, for installation progress.
#
RYW_DEBUG_TAG_PRINT_SET = [50]


#
# used by the string splitter function split_content().
# I'm splitting strings to the right length for the benefit of
# Google Translation.
RYW_MAX_STRING_TRANSLATION_LENGTH = 1700



#
# These source files require:
# # -*- coding: iso-8859-15 -*-
# prefixed at the beginning.
#
RYW_ISO_ENCODING_PREFIX_FILES = ['google_english2hindi.py']
#RYW_ISO_ENCODING_PREFIX = "# -*- coding: iso-8859-15 -*-"
RYW_ISO_ENCODING_PREFIX = "# -*- coding: latin-1 -*-"


#
# when breaking up large texts for Google translate,
# patterns governing what constitutes a valid breaking point,
# these two strings are tied together
# the first is a regular expression, the second is a string.
#
RYW_GOOGLE_TRANSLATE_PUNCTUATION_BREAK_REG = r'([.,;\!\)\:\\\'\"\?\/])'
RYW_GOOGLE_TRANSLATE_PUNCTUATION_BREAK_STR = '.,;!):\'"?/'



# maximum size of outgoing disc
maxSizeInKB = 3.8 * 1024 * 1024
#maxSizeInKB = 600 * 1024


# what qualifies as a small file---it gets copied to the village side
#     without being asked...
#smallFileSizeCeilingKB = 100
smallFileSizeCeilingKB = 30

# how many backup outgoing disc images to keep.
maxOldOutGoingDisks = 4

# upload date time format
uploadDateTimeFormat = '%#Y-%#m-%#d %#H:%#M:%#S'

# whether the logging module is initialized.
logging_initialized = False

# maximum number of chapter digits
maxChapterDigits = 24



def set_disc_limit(MB):
    global maxSizeInKB
    maxSizeInKB = MB * 1024



def setup_logging(logFileName):
    """set up logging."""
    format='%(process)d: %(asctime)s %(levelname)-8s %(message)s'
    fmt=logging.Formatter(fmt=format,datefmt=None)
    myHandler=ad.ADRotatingFileHandler(logFileName)
    myHandler.setFormatter(fmt)
    logging.getLogger().addHandler(myHandler)
    logging.getLogger().setLevel(logging.WARNING)
    try:
	    logging.debug('logging initialized')
    except:
	    raise
    global logging_initialized
    logging_initialized=True
    

def setup_logging2(dir, logFileName):
    """set up logging."""
    if not os.path.exists(dir):
        os.makedirs(dir)
    setup_logging(os.path.join(dir, logFileName))



def check_logging(dir, logName):
    """check to see if logging is being done.
    if not, we initialize logging here."""
    
    if not logging_initialized:
        # print 'logging not initialized. initializing'
        setup_logging2(dir, logName)



def print_and_flush(msg):
    print msg
    sys.stdout.flush()
    


def give_bad_news(message, logFunc):
    print '<P><FONT COLOR=RED SIZE=4><B><pre>'+message+'</pre></B></FONT>'
    logFunc(message)
    excMsg = traceback.format_exc()
    if excMsg != 'None\n':
        print '<P><FONT COLOR=RED SIZE=4><B>trace:<br><pre>'+excMsg+'</pre></B></FONT>'
        logFunc('trace: '+excMsg)

    

def give_bad_news3(message):
    print message

    

def give_good_news(message, logFunc):
    print '<P><FONT COLOR=GREEN SIZE=3><B>'+message+'</B></FONT>'
    logFunc(message)

    

def give_news(message, logFunc):
    print_and_flush('<P><FONT COLOR=BLUE>'+message+'</FONT>')
    if logFunc:
        logFunc(message)



def give_news2(message, logFunc):
    """same as above but no new line by print."""
    print '<FONT COLOR=BLUE>'+message+'</FONT>',
    if logFunc:
        logFunc(message)



def give_news3(message, logFunc=None):
    """same as give_news but no html tags, just plain text."""
    print message
    if logFunc:
        logFunc(message)



def give_bad_news2(message, logFunc):
    logFunc(message)
    excMsg = traceback.format_exc()
    if excMsg != 'None\n':
        logFunc('trace:'+excMsg)



def free_MB(path):
    """returns the amount of available space in MB."""
    return ryw_bizarro.free_MB(path)



def try_mkdir(dirname, msg):
    try:
        os.mkdir(dirname)
    except:
        give_bad_news('try_mkdir: ' + msg + ' failed to mkdir: ' +
                          dirname, logging.critical)
        return False
    return True



def try_mkdir_ifdoesnt_exist(dirname, msg):
    if not os.path.exists(dirname):
        return try_mkdir(dirname, msg)
    if not os.path.isdir(dirname):
        give_bad_news('try_mkdir_ifdoesnt_exist: ' + msg +
                          ' file exists.', logging.critical)
        return False
    return True

        

def cleanup_path(path, msg):
    if not path or not os.path.exists(path):
        return True
    
    if os.path.isdir(path):
        try:
            shutil.rmtree(path)
        except:
            give_bad_news('unexpected_error: cleanup_path: ' + msg +
                          ' failed to remove directory: ' + path,
                          logging.error)
            return False
        logging.debug('cleanup_path: ' + msg + ', removed directory: ' + path)
        return True

    try:
        os.remove(path)
    except:
        give_bad_news('unexpected_error: cleanup_path: ' + msg +
                      ' failed to remove file: ' + path,
                      logging.error)
        return False
    logging.debug('cleanup_path: ' + msg + ', removed file: ' + path)
    return True



def cleanup_partial_dir(path, msg, warn, chmodFirst = False):
    if not path or not os.path.exists(path) or not os.path.isdir(path):
        return True

    try:
        if chmodFirst:
            logging.debug('cleanup_partial_dir: recursive chmod: ' + path)
            chmod_tree(path)
        os.removedirs(path)
    except:
        if warn:
            give_bad_news('unexpected_error: cleanup_partial_dir: ' + msg +
                              ' failed to remove paritial dir: ' + path,
                              logging.error)
        return False
    logging.debug('cleanup_partial_dir: ' + msg + ', removed dir: ' + path)
    return True



def date_time_rand():
    now = datetime.datetime.now()
    nowStr = now.strftime('%y%m%d_%H%M%S')
    
    random.seed()
    randomNo = random.randint(1, 99999999)
    randomNo = str(randomNo)
    randomNo = randomNo.rjust(8, '0')
    return nowStr + '_' + randomNo



def get_year():
    now = datetime.datetime.now()
    return now.strftime('%Y')
    


def restore_cleanup_old_version(name):
    oldName = name + '_BAK'
    oldExists = os.path.exists(oldName)
    currentExists = os.path.exists(name)

    #
    # if neither the backup nor the current version exists,
    # that's an error.
    #
    if not currentExists and not oldExists:
        give_news(
            'warning: restore_cleanup_old_version: neither version exists: ' +
            name, logging.warning)
        return

    #
    # if both old and new exists, just remove the old.
    # well, maybe not...
    # 
    if currentExists and oldExists:
        # cleanup_path(oldName, 'restore_cleanup_old_version:')
        return

    #
    # if only the new exists, do nothing.
    #
    if currentExists:
        return

    #
    # only the old version exists; try to restore it.
    #
    try:
        shutil.move(oldName, name)
    except:
        give_bad_news(
            'restore_cleanup_old_version: failed to restore old version: ' +
            oldName + ' -> ' + name, logging.critical)
    logging.warning('restore_cleanup_old_version: restored old version: ' +
                    oldName + ' -> ' + name)



def move_to_bak(name, copyInsteadOfMove = False):
    oldFileBak = name + '_BAK'
    if os.path.exists(name):
        try:
            if os.path.exists(oldFileBak):
                cleanup_path(oldFileBak, 'move_to_bak:')
            if copyInsteadOfMove:
                shutil.copyfile(name, oldFileBak)
            else:
                shutil.move(name, oldFileBak)
        except:
            give_bad_news(
                'move_to_bak: failed to rename old file: ' +
                name + ' ' + oldFileBak, logging.critical)
            return False
        logging.debug(
            'move_to_bak: successfully renamed oldFile: ' +
            name + ' ' + oldFileBak)
        return True

    logging.debug('move_to_bak: old file does not exist: ' + name)
    return True
    


def copy_file_carefully(oldFile, newFile, oldDir, newDir, tmpPrefix):
    """oldFile = oldSearchFile
    newFile = incomingSearchFile
    oldDir = mywww = c:\Postmanet\nihao\WWW\repository?
    newDir = mydisk (not used)
    tmpPrefix = 'SearchFile_incoming'
    """
    
    # make this function generic and reusable for copying anything in a
    # robust manner:
    #   (1) see if the bak version is there but not the new version,
    #       if yes, restore it first.  (existing restore is bad: need to check
    #       whether the new version is there...)  remove bak version...
    #       this is general sanity check that can be called from anywhere.
    #   (2) is the new stuff there?
    #   (3) copy new stuff to tmp name.
    #   (4) rename the existing stuff to bak name.
    #   (5) rename the new tmpname to its real name.
    #   (6) remove the bak name.

    # for testing.
    #check_logging(os.path.join('c:\\Postmanet\\Nihao', 'WWW', 'repository'), 'upload.log')
    
    #
    # (1) do something about oldFile_bak if it exists.
    #
    restore_cleanup_old_version(oldFile)
    
    #
    # (2) if the newFile isn't there, something is wrong.
    #
    if not os.path.exists(newFile):
        give_bad_news(
            'copy_file_carefully: new file does not exist: ' +
            newFile, logging.warning)
        return False

    #
    # (3) copy the newFile to a temporary name.
    #
    tmpname,objPrefix = ryw_upload.make_tmp_name(oldDir, tmpPrefix, '')
    try:
        su.copytree(newFile, tmpname)
    except:
        give_bad_news(
            'copy_file_carefully: failed to copy newFile: ' +
            newFile + ' ' + tmpname, logging.critical)
        cleanup_path(tmpname, 'copy_file_carefully:')
        return False

    logging.debug(
        'copy_file_carefully: successfully copied incoming file: ' +
        newFile + ' ' + tmpname)
    
    #
    # (4) rename the existing old file to a backup name.
    #
    if not move_to_bak(oldFile):
        cleanup_path(tmpname, 'copy_repository_view:')
        return False
        
    #
    # (5) rename the incoming file from its tmp name to its real name.
    #
    try:
        shutil.move(tmpname, oldFile)
    except:
        give_bad_news(
            'copy_file_carefully: failed to rename tmp name to real name: '+
            tmpname + ' ' + oldFile, logging.critical)
        cleanup_path(oldFile, 'copy_file_carefully:')
        restore_cleanup_old_version(oldFile)
        cleanup_path(tmpname, 'copy_file_carefully:')
        return False
    logging.debug(
        'copy_file_carefully: successfully renamed incoming file: ' +
        tmpname + ' ' + oldFile)

    #
    # (6) remove the backup name.
    #
    restore_cleanup_old_version(oldFile)
    return True



def make_tmp_file_permanent(tmppath, realpath):
    """like the above, except tmp name already exists."""
    bakpath = None
    if os.path.exists(realpath):
        bakpath = realpath + '.BAK'
        try:
            cleanup_path(bakpath, 'make_tmp_file_permanent: begin: ')
            os.rename(realpath, bakpath)
        except:
            give_bad_news(
                'make_tmp_file_permanent: failed to rename existing file :'+
                realpath + ' ' + bakpath, logging.critical)
            return (False, bakpath)

    try:
        os.rename(tmppath, realpath)
    except:
        give_bad_news(
            'make_tmp_file_permanent: failed to rename new file: '+
            tmppath + ' ' + realpath, logging.critical)

        try:
            if os.path.exists(bakpath):
                os.rename(bakpath, realpath)
        except:
            give_bad_news('failed to even put the bak file back: ' +
                          bakpath + ' ' + realpath, logging.critical)

        give_bad_news(
            'make_tmp_file_permanent: but managed to restore the original: '+
            bakpath + ' ' + realpath, logging.critical)
        return (False, bakpath)

    cleanup_path(bakpath, 'make_tmp_file_permanent:')
    logging.debug('make_tmp_file_permanent: succeeded: ' + tmppath + ' ' +
                  realpath)
    return (True, None)
    


def open_search_file(msg, logdir, logfile, searchfile, exclusive,
                     skipRead = False, skipLk = False):
    searchFile = None
    try:
        searchFile = SearchFile.SearchFile(
            logdir, logfile, searchfile, exclusive, skipRead, skipLock=skipLk)
    except:
        give_bad_news(msg + ' ' +
            'open_search_file: failed to open SearchFile.',
            logging.critical)
        if searchFile:
            searchFile.done()
        return (False, None)
    return (True, searchFile)



def print_header():
    print 'Cache-Control: no-cache'
    print 'Content-Type: text/html'
    print



def get_queue_args():
    
    form = cgi.FieldStorage()
    rfpath = form.getfirst('rfpath', '')

    if not rfpath:
        give_bad_news(
            'get_queue_args: bad input: no rfpath given.', logging.error)
        #cgi.print_form(form)
        return (False, None)

    logging.debug('get_queue_args: rfpath: ' + rfpath)
    return (True, rfpath)



def empty_download_queue(rfpath):
    logging.debug('empty_download_queue: entered...')
    if not os.path.exists(rfpath):
        logging.debug('empty_download_queue: queue does not exist: ' + rfpath)
        give_news('download queue already empty.', logging.info)
        return
    
    try:
        su.pickdump(set([]), rfpath)
    except:
        give_bad_news('empty_download_queue: failed to pickdump: ' +
                      rfpath, logging.warning)
        return
    
    logging.debug('empty_download_queue: done:' + rfpath)
    #give_news('download queue emptied.', logging.info)



def has_store_suffix(name):
    suffix = name[-5:]
    return suffix == '_DATA' or suffix == '_META' or \
           suffix == '_AUXI' or suffix == '_DONE' or suffix == '_MDON'



def store_name_prefix(name):
    return name[:-5]



def check_village_log(msg):
    NihaoRoot = 'c:/Postmanet/nihao'
    check_logging(os.path.join(NihaoRoot, 'WWW', 'repository'),
                  'upload.log')
    logging.info(msg+' entered...')



def check_headquarters_log(msg):
    RepositoryRoot = 'c:/Postmanet/repository'
    check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                  'upload.log')
    logging.debug(msg+' entered...')



def add_suffixes(name):
    return (name + '_DATA', name + '_META', name + '_AUXI',
            name + '_DONE', name + '_MDON')



def get_store_paths(dir, prefix):
    return add_suffixes(os.path.join(dir, prefix))



def remove_all_repo_dirs(paths):
    dataPath,metaPath,auxiPath,donePath,mdonPath = paths

    #cleanup_path(donePath, 'remove_all_repo_dirs')
    #cleanup_path(mdonPath, 'remove_all_repo_dirs')
    #cleanup_path(auxiPath, 'remove_all_repo_dirs')
    #cleanup_path(metaPath, 'remove_all_repo_dirs')
    #cleanup_path(dataPath, 'remove_all_repo_dirs')

    force_remove(donePath, 'remove_all_repo_dirs')
    force_remove(mdonPath, 'remove_all_repo_dirs')
    force_remove(auxiPath, 'remove_all_repo_dirs')
    force_remove(metaPath, 'remove_all_repo_dirs')
    force_remove(dataPath, 'remove_all_repo_dirs')
    
    #parent = os.path.dirname(donePath)
    #cleanup_partial_dir(parent, 'remove_all_repo_dirs, parent:', True)



def attempt_repair_repo_paths(paths):
    dataPath,metaPath,auxiPath,donePath,mdonPath = paths
    doneBakPath = donePath + '_BAK'
    mdonBakPath = mdonPath + '_BAK'
    metaBakPath = metaPath + '_BAK'
    
    if     os.path.exists(doneBakPath) and \
       not os.path.exists(donePath)    and \
           os.path.exists(metaBakPath) and \
       not os.path.exists(metaPath):
        restore_cleanup_old_version(metaPath)
        restore_cleanup_old_version(donePath)
        
    if     os.path.exists(mdonBakPath) and \
       not os.path.exists(mdonPath)    and \
           os.path.exists(metaBakPath) and \
       not os.path.exists(metaPath):
        restore_cleanup_old_version(metaPath)
        restore_cleanup_old_version(mdonPath)
    
    
    
def good_repo_paths(paths):
    
    attempt_repair_repo_paths(paths)
    
    dataPath,metaPath,auxiPath,donePath,mdonPath = paths
    good = (os.path.exists(donePath)  and \
            os.path.exists(dataPath)  and \
            os.path.exists(metaPath)) or  \
           (os.path.exists(mdonPath)  and \
            os.path.exists(metaPath))
    if good:
        return good

    if not good:
        logging.warning('good_repo_paths: detected bad paths: ' +
                        repr(paths))
        logging.debug('small file success? ' +
                      repr((os.path.exists(donePath)  and \
                            os.path.exists(dataPath)  and \
                            os.path.exists(metaPath))))
        logging.debug('big file success? ' +
                      repr((os.path.exists(mdonPath)  and \
                            os.path.exists(metaPath))))
    return good
    
    

def cleanup_partial_repo_dir(srcd, prefixes):
    goodPrefixes = []
    for prefix in prefixes:
        paths = get_store_paths(srcd, prefix)
        if not good_repo_paths(paths):
            remove_all_repo_dirs(paths)
            continue
        goodPrefixes.append(prefix)
    return goodPrefixes



def NOTUSED_check_obj_paths(paths):
    if not os.path.exists(paths[0]) or \
       not os.path.exists(paths[1]) or \
       not os.path.exists(paths[2]):
        give_bad_news(
            'check_obj_paths: some path does not exist: ' +
            paths[0] + ' ' + paths[1] + ' ' + paths[2],
            logging.error)
        return False
    return True



def get_meta(objroot, objname, version):
    """uses the file system to get meta data instead of getting it from
    either the SearchFile or SearchServer.  should be a bit faster if
    there is no need to read all the metadata.  just a performance issue:
    should not be a robustness issue now that we have gotten rid of the
    SearchServers."""

    logging.debug('ryw.get_meta: ' + objroot + ' ' + objname + ' ' +
                  str(version))
    
    try:
        #paths = objectstore.nameversiontopaths(objroot, objname, version)
        paths = objectstore.name_version_to_paths_aux(objroot, objname,
                                                      version)

        if not good_repo_paths(paths):
            logging.warning('ryw.get_meta: good_repo_paths failed.')
            return (False, None)
        
        metapath = paths[1]
        meta = su.pickload(metapath)
        logging.debug('ryw.get_meta: success.')
        return (True, meta)
    except:
        logging.warning('ryw.get_meta: failed.')
        return (False, None)



def datetimesortkey_NOT_USED(x):
    if x.has_key('upload_datetime'):
        return eval(x['upload_datetime'])
    else:
        return datetime.datetime.min



def datetimesortkey(meta):
    return Search.changed_time_key(meta)



def sortmeta(metalist):
    metalist.sort(key = datetimesortkey, reverse = True)
    return metalist



def datetimesortkey_chapter_number(x):
    """concatenates chapter number with the time.
    pads the chapter number if necessary."""


    #
    # example keys:
    # _________________________081021_165843
    # 01.English00000000000000_081022_154011
    # 01.Hindi0000000000000000_081022_154008
    #
    
    if x.has_key('chapter_number'):
        chapter = x['chapter_number']
        chapter = chapter.strip()
        chapter = chapter[:maxChapterDigits]
        #if chapter.isdigit():
        #    chapter = int(chapter)
        #    chapter = ('%(#)0' + str(maxChapterDigits) + 'd') % {'#': chapter}
        #else:
        #    chapter = chapter.ljust(maxChapterDigits, '0')
        chapter = chapter.ljust(maxChapterDigits, '0')
    else:
        chapter = ''.ljust(maxChapterDigits, '_')

    db_print('datetimesortkey_chapter_number, chapter: ' + chapter, 38)
    
    timeVal = Search.changed_time_key(x)
    timeStr = timeVal.strftime('%y%m%d_%H%M%S')
    answer = chapter + '_' + timeStr

    db_print('datetimesortkey_chapter_number, answer: ' + answer, 41)
    return answer
    


def sortmeta_chapter_number(metalist):
    metalist.sort(key = datetimesortkey_chapter_number, reverse = True)
    return metalist



def get_KB_str(dir):
    kB = ryw_disc.getRecursiveSizeInKB(dir)
    kB = str(kB)
    if kB[-1] == 'L':
        kB = kB.replace('L', '')
    return kB



def empty_tmp_dir(dir, skipList = [], chmodFirst = False):
    blanks = '&nbsp;&nbsp;&nbsp;&nbsp;'
    if not os.path.exists(dir):
        return True
    if not os.path.isdir(dir):
        give_bad_news('empty_tmp_dir: not a directory: ' + dir,
                      logging.critical)
        return False

    give_news('examining ' + dir + ' ...', logging.info)
    kB = get_KB_str(dir)
    give_news(blanks + 'space currently consumed: ' + kB + ' KB.',
              logging.info)
    give_news(blanks + 'deleting...', logging.info)

    try:
        if chmodFirst:
            logging.debug('empty_tmp_dir: recursive chmod: ' + dir)
            chmod_tree(dir)
            
        items = os.listdir(dir)
        for item in items:
            if item in skipList:
                continue
            name = os.path.join(dir, item)
            cleanup_path(name, 'empty_tmp_dir:')

        kB = get_KB_str(dir)
        give_news(
            blanks + 'space occupied after clearing: ' +
            kB + ' KB.', logging.info)
        return True
    except:
        give_bad_news('empty_tmp_dir: something bad happened: ' + dir,
                      logging.critical)
        return False



def get_obj_str(form=None):
    if not form:
        form = cgi.FieldStorage()
    return get_obj_str2(form)



def get_obj_str2(form):
    objstr = form.getfirst('objstr', '')

    if not objstr:
        give_bad_news(
            'get_obj_str: bad input: no objstr given.', logging.error)
        return (False, None, None)

    logging.debug('get_obj_str: objstr: ' + objstr)

    try:
        objID,version = objstr.split('#')
        version = int(version)
    except:
        give_bad_news(
            'get_obj_str: failed to split object string: '+objstr,
            logging.error)
        return (False, None, None)
    
    return (True, objID, version)



def split_objstr(objstr):
    try:
        objID,version = objstr.split('#')
        version = int(version)
        return (True, objID, version)
    except:
        ryw.give_bad_news('split_objstr: failed to split: ' + objstr,
                          logging.error)
        return (False, None, None)



def chmod_tree(path):
    if not os.path.exists(path):
        #give_bad_news('chmod_tree: path does not exist: ' + path,
        #              logging.warning)
        return

    ryw_bizarro.sudo_chmod(path, '777', 0777)
    
    if os.path.isfile(path):
        return

    for entry in os.listdir(path):
        path2 = os.path.join(path, entry)
        chmod_tree(path2)



def force_remove(path, msg):
    if (not path) or (not os.path.exists(path)):
        return
    logging.debug('force_remove: entered: ' + path)
    chmod_tree(path)
    cleanup_path(path, msg)



def parent_dir(path):
    return os.path.dirname(os.path.normpath(path))



def get_obj_size(itempath):
    if not os.path.exists(itempath[1]):
        ryw.give_bad_news('get_obj_size: data path does not exist: ' +
                          itempath[0], logging.critical)
        return (False, 0)

    dataPath = os.path.normpath(itempath[1])
    parent,tail = os.path.split(dataPath)
    logging.debug('get_obj_size: parent dir is: ' + parent)
    
    itemSize = ryw_disc.getRecursiveSizeInKB(parent)
    itemSize += 4

    logging.debug('get_obj_size: kB: ' + str(itemSize))
    return (True, itemSize)



def is_valid_dir(dirname, msg=''):
    answer = True
    if not os.path.exists(dirname):
        give_bad_news('directory does not exist: ' + dirname, logging.error)
        answer = False
    if answer == True and not os.path.isdir(dirname):
        give_bad_news('is not a directory: ' + dirname, logging.error)
        answer = False
    if answer == False and msg:
        give_bad_news('is_valid_dir failed, called by: ' + msg, logging.error)
    return answer



def is_valid_file(filename, msg=''):
    answer = True
    if not os.path.exists(filename):
        give_bad_news('file does not exist: ' + filename, logging.error)
        answer = False
    if answer == True and not os.path.isfile(filename):
        give_bad_news('is not a file: ' + filename, logging.error)
        answer = False
    if answer == False and msg:
        give_bad_news('is_valid_file failed, called by: ' + msg, logging.error)
    return answer



#
# returns (Success, isFile, isDir)
#
def is_valid_file_or_dir(pathName, msg=''):
    badNews = (False, False, False)
    if not os.path.exists(pathName):
        give_bad_news('path name does not exist: ' + pathName, logging.error)
        give_bad_news('is_valid_file_or_dir failed, called by: '+msg,
                      logging.error)
        return badNews

    if os.path.isfile(pathName):
        return (True, True, False)

    if os.path.isdir(pathName):
        return (True, False, True)

    give_bad_news('this is neither a file nor a directory: ' + pathName,
                  logging.error)
    give_bad_news('is_valid_file_or_dir failed, called by: '+ msg,
                  logging.error)
    return badNews



def has_robot(resources):
    if resources.has_key('robotPresent'):
        robotStr = resources['robotPresent']
        if robotStr == 'True':
            return True

    return False



def sequence_to_string(seq):
    s = ''
    for item in seq:
        if s != '':
            s = s + ', '
        s = s + str(item)
    return s



def is_from_village():
    try:
        fromVillage = NihaoRoot != ''
    except:
        fromVillage = False
    return fromVillage
    


def chop_datetime_leading_zeros(dtStr):
    #
    # I seem to have problem with passing the string back to Python
    # if the string looks like: '2009-04-08 05:00:44'
    # so I'm going to get rid of the leading zeros.
    #
    db_print_info_browser('chop_datetime_leading_zeros: original: ' +
                          dtStr, 99)
    
    #dtStr = dtStr.replace('-0', '-')
    #dtStr = dtStr.replace(' 0', ' ')
    #dtStr = dtStr.replace(':0', ':')

    #
    # r'-0([0-9])' makes sure only :02 will be selected, not :0 by itself.
    # '-\g<1>' makes sure :02 become :2, \g<1> is 2.
    #
    dtStr = re.sub(r'-0([0-9])', r'-\g<1>', dtStr)
    dtStr = re.sub(r' 0([0-9])', r' \g<1>', dtStr)
    dtStr = re.sub(r':0([0-9])', r':\g<1>', dtStr)
    
    db_print_info_browser('chop_datetime_leading_zeros: chopped: ' +
                          dtStr, 99)
    return dtStr



def get_misc_dict():
    dict = {}
    dict['year'] = get_year()

    nowStr = datetime.datetime.now().strftime(uploadDateTimeFormat)

    #
    # I seem to have problem with passing the string back to Python
    # if the string looks like: '2009-04-08 05:00:44'
    # so I'm going to get rid of the leading zeros.
    #
    nowStr = chop_datetime_leading_zeros(nowStr)
    dict['uploaded_date_time_val'] = nowStr

    name = ''
    try:
        fromVillage = is_from_village()
        if fromVillage:
            name = open(os.path.join(NihaoRoot, 'WWW', 'repository',
                                     'usercredentials')).readline().strip()
        else:
            name = os.getenv("REMOTE_USER")
    except:
        give_bad_news2('get_misc_dict: failed to get name.', logging.error)

    dict['userName'] = name

    return dict



def get_objectstore(meta):
    #
    # I'm doing this to hardwire all
    # places of gettting objectstoreroot.
    #
    return hard_wired_objectstore_root()
    
    #if not meta.has_key('objectstore'):
    #    give_bad_news('get_objectstore: no objectstore attribute: ' +
    #                      repr(meta), logging.error)
    #    return None
    #return os.path.normpath(meta['objectstore'])
    


def get_resources(path):
    try:
        resources = su.parseKeyValueFile(path)
        return resources
    except:
        give_bad_news('fatal_error: failed to read resources file',
                      logging.critical)
        return None
    
        
def get_resource(resources, key):
    if resources == None:
        return None
    if resources.has_key(key):
        strVal = resources[key]
        if strVal == 'True':
            return True

    return None



def get_resource_str(resources, key):
    if resources == None:
        return None
    if resources.has_key(key):
        return resources[key]

    return None



def get_file_size(path):
    if not is_valid_file(path, 'get_file_size'):
        return (False, 0)
    try:
        bytes = os.path.getsize(path)
    except:
        ryw.give_bad_news('get_file_size failed: ' + path, logging.error)
        return (False, 0)
    return (True, bytes)



def create_empty_file(fileName, message=''):
    if os.path.exists(fileName) and is_valid_file(fileName, msg=message):
        return True
    
    logging.debug('create_empty_file: file does not exist: '+
                  fileName)
    try:
        f = open(fileName, 'w')
        f.close()
    except:
        give_bad_news(
            'create_empty_file: failed to create empty file: ' +
            fileName, logging.critical)
        return False

    logging.debug('create_empty_file: empty file created: ' + fileName)
    return True



def db_print(message, tag):
    """logs at debug level."""
    if tag != RYW_DEBUG_TAG:
        return
    logging.debug(message)



def db_print2(message, tag):
    """prints HTML to screen instead."""
    if tag != RYW_DEBUG_TAG:
        return
    give_news2(message + "<BR>", logging.debug)



def db_print3(message, tag):
    """prints plain text to screen instead."""

    if tag == RYW_DEBUG_TAG or db_print_in_set(tag):
        give_news3(message)

    return



def db_print_in_set(tag):
    """called by db_print3()"""
    return tag in RYW_DEBUG_TAG_PRINT_SET



def db_raise_or_print3(message, tag):
    """allows me to switch back and forth between raise and print3()."""
    #raise message
    if tag != RYW_DEBUG_TAG:
        return
    give_news3(message)



def db_print_browser(message, tag):
    db_print2(message, tag)



def db_print_info(message, tag):
    if tag != RYW_DEBUG_TAG:
        return
    logging.info(message)
    


def db_print_info_browser(message, tag):
    db_print_browser(message, tag)
    db_print_info(message, tag)

    


def same_subnet(laddr, raddr):
    """see if two IP addresses are on the same subnet,
    called by ryw_view.make_explorer_lan_popup_string().
    for popping up explorer window for the P: drive."""

    sL = laddr.split('.')
    rL = raddr.split('.')

    sameSubNet = False
    try:
        if sL[0] == rL[0] and sL[1] == rL[1] and sL[2] == rL[2]:
            sameSubNet = True
    except:
        sameSubNet = False

    return sameSubNet



def is_localhost(addr):
    """called by ryw_view.make_explorer_lan_popup_string().
    see if it's localhost."""

    return addr == '127.0.0.1'



def is_lan():
    serverAddr = os.environ['SERVER_ADDR']
    remoteAddr = os.environ['REMOTE_ADDR']

    if serverAddr == remoteAddr:
        return False

    if is_localhost(serverAddr):
        return False
    
    return same_subnet(serverAddr, remoteAddr)



def pickle_load_raw_and_text(fileName, dos2unix=False):
    """called by su.pickload().
    should have written pickle into binary files.  but the original code
    didn't.  so we're going to try reading twice.  once in binary mode,
    and once in text mode.  this problem was encountered when trying
    to move NTFS dictionaries to Linux.
    it seems to be happening only to individual metadata files.
    SearchFile has always been written in binary mode.
    ReverseLists is affected."""

    try:
        f = open(fileName, "rb")
    except:
        give_bad_news('pickle_load_raw_and_text: unable to open bin file: ' +
                      fileName, logging.error)
        return None

    try:
        value = pickle.load(f)

        #
        # reading in binary mode successful.
        # we're done.
        #
        f.close()
        db_print2('pickle_load_raw_and_text: success first time: ' +
                  fileName, 61)
        return value
    except ValueError:
        #
        # we have a format error on Linux.
        # try to do it again in text mode.
        #
        db_print2('pickle_load_raw_and_text: Linux format error, ' +
                  're-reading... ' + fileName, 61)
        pass
    except ImportError:
        #
        # we have a format error on XP.
        # try to do it again in text mode.
        #
        db_print2('pickle_load_raw_and_text: XP format error, ' +
                  're-reading... ' + fileName, 61)
        pass
    except:
        #
        # some other kind of error. giving up.
        #
        give_bad_news('pickle_load_raw_and_text: ' +
                      'reading in binary mode failed: ' + fileName,
                      logging.error)
        f.close()
        return None

    #
    # if we get here, we want to try to re-read the file
    # in text mode.  (for legacy compatibility reason.)
    #
    f.close()

    try:
        f = open(fileName, "r")
    except:
        give_bad_news('pickle_load_raw_and_text: unable to open text file: '+
                      fileName, logging.error)
        return None

    try:
        value = pickle.load(f)

        #
        # reading in text mode successful.
        # we're done.
        #
        f.close()
        return value
    except (ValueError, ImportError):
        #
        # we have a format error in text mode on Linux.
        # giving up, but tell us.
        #
        f.close()

        if dos2unix == False:
            db_print_info_browser('pickle_load_raw_and_text: ' +
                                  'will attempt dos2unix: ' +
                                  'Linux: ' + fileName, 69)
            #
            # we will then run dos2unix and retry...
            # this goes to ryw_linux.run_dos2unix_reread(), which
            # will recursively call this function back, with
            # the dos2unix flag set to True this time.
            #
            value = ryw_bizarro.run_dos2unix_reread(fileName)
            return value
        
        give_bad_news('pickle_load_raw_and_text: ' +
                      'reading in text mode failed due to format error: ' +
                      'Linux: ' + fileName, logging.error)
        return None
    #except ImportError:
        #
        # we have a format error in text mode on XP.
        # giving up, but tell us.
        #
        #give_bad_news('pickle_load_raw_and_text: ' +
        #              'reading in text mode failed due to format error: ' +
        #              'XP: ' + fileName, logging.error)
        #f.close()
        #return None
    except:
        #
        # some other kind of error.
        #
        give_bad_news('pickle_load_raw_and_text: ' +
                      'reading in text mode failed due to unknown readon: ' +
                      fileName, logging.error)
        f.close()
        return None



def pickle_reopen_read(fileName, fHandle, currentMode):
    """called by SearchFile.py.
    probably not necessary.
    if failed to do it in the current mode,
    try to re-open it in a different mode."""


    db_print2('pickle_reopen_read: entered: ' + fileName, 61)
    
    if currentMode == 'rb':
        nextMode = 'r'
    else:
        nextMode = 'rb'

    #
    # no exception-catching: deliberate.
    # the caller will do it.
    #
    fHandle.close()
    fHandle = open(fileName, nextMode)
    value = pickle.load(fHandle)
    return (value, fHandle)



def hard_wired_objectstore_root():
    """this is to get rid of the approach of getting the objectstoreroot
    from that embedded in meta.  this might be called from several places.
    """
    return os.path.join(RepositoryRoot, 'WWW', 'ObjectStore')



def md5sum(text):
    """called by SelectTexts.py and
    ryw_view.get_auto_hindi_translation_string()."""
    m = md5.new()
    m.update(text)
    return m.hexdigest()



def reverse_alist(alist):
    """reverse a list, helper function used the string splitter below"""
    temp = alist[:]
    temp.reverse()
    return temp



#
# copied from:
# http://vsbabu.org/mt/archives/2002/04/30/splitting_text_at_word_boundaries.html
# RYW:
# changed to cut on punctuation boundaries.
# 
def split_content(content,slice_length=RYW_MAX_STRING_TRANSLATION_LENGTH):
    """returns a list of strings after splitting
    the content at a maximum of slice_length or
    at the last word boundary before that

    if a slice is anyway more than slice_length, it'll
    cut it at slice_length"""

    out = []
    i = 0
    s = 0

    #
    # RYW
    #
    #word_boundary = re.compile(r'(\s)',re.DOTALL|re.IGNORECASE|re.M)
    word_boundary = re.compile(RYW_GOOGLE_TRANSLATE_PUNCTUATION_BREAK_REG,
                               re.DOTALL|re.IGNORECASE|re.M)
    #print content, slice_length
    db_print_info_browser('split_content: slice_length is: ' +
                          str(slice_length), 73)
    #print_content(content)

    #
    # RYW
    # if I don't strip off leading spaces, sometimes, these spaces
    # get recognized as an individual unit, because the code below
    # is just looking for punctuations.
    #
    content = content.strip()
    #
    # RYW: pad a space, so we don't make a mistake
    # of not finding the end.
    # No, pad a period.
    #
    #content += ' '
    content = append_period(content)
    
    while 1:
        # get the next slice
        i = i + 1
        t = content[s:s+slice_length]
        if t == '': break

        # check the end of slice for word boundary
        # we can assume that the last space from end
        # is the word boundary
        m = word_boundary.search(''.join(reverse_alist(list(t))))
        if m is not None:
            t = t[:len(t)-m.start()]
        s = s + len(t)
        db_print_info_browser('split_content: t is: -' + t + '-', 76)
        db_print_info_browser('split_content: length is: ' + str(len(t)), 76)

        if len(t) != 1:
            out.append(t)
        #print t, len(t)
    return out



def print_content(content):
    i = 0
    l = len(content)
    db_print_info_browser('printing content...', 75)
    while (i < l):
        db_print_info_browser('i: ' + str(i) + ', c: -' + content[i] + '-', 75)
        i += 1

        

def is_newline(c):
    #return c=='\n' or c=='\r'
    return c=='\n'



def append_period(content):
    puncList = RYW_GOOGLE_TRANSLATE_PUNCTUATION_BREAK_STR
    i = len(content)
    while (i > 0):
        i -= 1
        if content[i].isspace():
            continue
        if content[i] in puncList:
            return content
        return content + '.'
    return content + '.'
