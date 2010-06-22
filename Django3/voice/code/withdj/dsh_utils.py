#
# copied from Postmanet-2.
#

import sys, os, pickle, cgi, cgitb, xmlrpclib, random, shutil, subprocess
import dsh_ad
import logging, datetime, time, zipfile, cStringIO, shutil
import string
import traceback
import dsh_bizarro
import md5, re



def f7_list_unique(seq, idfun=None):
    """returns a list that contains only unique elements of the original
    list. taken from:
    http://www.peterbe.com/plog/uniqifiers-benchmark
    """
    return list(_f7(seq, idfun))

def _f7(seq, idfun=None):
    seen = set()
    if idfun is None:
        for x in seq:
            if x in seen:
                continue
            seen.add(x)
            yield x
    else:
        for x in seq:
            x = idfun(x)
            if x in seen:
                continue
            seen.add(x)
            yield x



def add_to_sys_path(morePath=None):
    if morePath:
        sys.path += morePath
    sys.path = f7_list_unique(sys.path)



import dsh_agi




#
# used by the db_print*() functions near the end of this file.
# 168
RYW_DEBUG_TAG = 168

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




def setup_logging(logFileName, quiet=False):
    """set up logging."""
    format='%(process)d: %(asctime)s %(levelname)-8s %(message)s'
    fmt=logging.Formatter(fmt=format,datefmt=None)
    myHandler=dsh_ad.ADRotatingFileHandler(logFileName)
    myHandler.setFormatter(fmt)
    logging.getLogger().addHandler(myHandler)
    logging.getLogger().setLevel(logging.DEBUG)
    try:
        if not quiet:
            logging.debug('logging initialized')
    except:
        raise
    global logging_initialized
    logging_initialized=True

    

def setup_logging2(dir, logFileName, quiet=False):
    """set up logging."""
    if not os.path.exists(dir):
        os.makedirs(dir)
    setup_logging(os.path.join(dir, logFileName), quiet=quiet)



def check_logging(dir, logName, quiet=False):
    """check to see if logging is being done.
    if not, we initialize logging here."""
    
    if not logging_initialized:
        # print 'logging not initialized. initializing'
        setup_logging2(dir, logName, quiet=quiet)



def print_and_flush(msg):
    print msg
    sys.stdout.flush()
    


def give_bad_news(message, logFunc=logging.info):
    dsh_agi.console_message_log(message, log_type=logFunc)
    excMsg = traceback.format_exc()
    if excMsg != 'None\n':
        dsh_agi.console_message_log('trace: '+excMsg, log_type=logFunc)

    

def give_bad_news2(message, logFunc=logging.info):
    """no exception printing..."""
    dsh_agi.console_message_log(message, log_type=logFunc)

    

def give_bad_news3(message):
    console_message(message)

    

def give_good_news(message, logFunc):
    dsh_agi.console_message_log(message, log_type=logFunc)
    
    

def give_news(message, logFunc=logging.info):
    dsh_agi.console_message_log(message, log_type=logFunc)



def free_MB(path):
    """returns the amount of available space in MB."""
    return dsh_bizarro.free_MB(path)



def try_mkdir(dirname, msg):
    try:
        os.makedirs(dirname)
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
        db_print('cleanup_path: ' + msg + ', removed directory: ' + path, 94)
        return True

    try:
        os.remove(path)
    except:
        give_bad_news('unexpected_error: cleanup_path: ' + msg +
                      ' failed to remove file: ' + path,
                      logging.error)
        return False
    db_print('cleanup_path: ' + msg + ', removed file: ' + path, 94)
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



def date_time_rand2():
    """same as above, but a shorter random number."""
    now = datetime.datetime.now()
    nowStr = now.strftime('%y%m%d_%H%M%S')
    
    random.seed()
    randomNo = random.randint(1, 9999)
    randomNo = str(randomNo)
    randomNo = randomNo.rjust(2, '0')
    return nowStr + '_' + randomNo



def date_time_rand3():
    """same as date_time_rand() but without underscores."""
    now = datetime.datetime.now()
    nowStr = now.strftime('%y%m%d%H%M%S')
    
    random.seed()
    randomNo = random.randint(1, 100000000)
    randomNo = str(randomNo)
    randomNo = randomNo.rjust(8, '0')
    return nowStr + randomNo



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
    


def print_header():
    print 'Cache-Control: no-cache'
    print 'Content-Type: text/html'
    print



def chmod_tree(path):
    if not os.path.exists(path):
        #give_bad_news('chmod_tree: path does not exist: ' + path,
        #              logging.warning)
        return

    dsh_bizarro.sudo_chmod(path, '777', 0777)
    
    if os.path.isfile(path):
        return

    for entry in os.listdir(path):
        path2 = os.path.join(path, entry)
        chmod_tree(path2)



def chmod_tree2(path, recurse=True):
    """rewritten, with os.chmod call."""
    if not os.path.exists(path):
        #give_bad_news('chmod_tree: path does not exist: ' + path,
        #              logging.warning)
        return

    if os.path.isfile(path):
        try:
            os.chmod(path, 0666)
            db_print('dsh_utils.chmod_tree2: done file: ' + path, 102)
        except:
            pass
        return

    try:
        os.chmod(path, 0777)
        db_print('dsh_utils.chmod_tree2: done dir: ' + path, 102)
    except:
        pass

    if not recurse:
        return

    for entry in os.listdir(path):
        path2 = os.path.join(path, entry)
        chmod_tree2(path2)



def force_remove(path, msg):
    if (not path) or (not os.path.exists(path)):
        return
    logging.debug('force_remove: entered: ' + path)
    chmod_tree(path)
    cleanup_path(path, msg)



def parent_dir(path):
    return os.path.dirname(os.path.normpath(path))



def is_valid_dir(dirname, msg='', silence=False):
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



def is_valid_file(filename, msg='', silent=False):
    answer = True
    if not os.path.exists(filename):
        if not silent:
            give_bad_news('file does not exist: ' + filename, logging.error)
        answer = False
    if answer == True and not os.path.isfile(filename):
        if not silent:
            give_bad_news('is not a file: ' + filename, logging.error)
        answer = False
    if answer == False and msg:
        if not silent:
            give_bad_news('is_valid_file failed, called by: ' +
                          msg, logging.error)
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



def sequence_to_string(seq):
    s = ''
    for item in seq:
        if s != '':
            s = s + ', '
        s = s + str(item)
    return s



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

    nowTime = datetime.datetime.now()
    dict['now'] = nowTime
    nowStr = nowTime.strftime(uploadDateTimeFormat)

    #
    # I seem to have problem with passing the string back to Python
    # if the string looks like: '2009-04-08 05:00:44'
    # so I'm going to get rid of the leading zeros.
    #
    dict['time_stamp_with_0s'] = nowStr
    nowStr = chop_datetime_leading_zeros(nowStr)
    dict['uploaded_date_time_val'] = nowStr
    dict['time_stamp_chopped'] = nowStr

    dict['year_short'] = nowTime.strftime('%y')
    dict['month'] = nowTime.strftime('%m')
    dict['day_of_month'] = nowTime.strftime('%d')
    
    dict['year_month'] = nowTime.strftime('%y%m')
    dict['year_month_day'] = nowTime.strftime('%y%m%d')
    dict['year_month_day_time'] = nowTime.strftime('%y%m%d_%H%M%S')

    dict['year_slash_month'] = nowTime.strftime('%y/%m')

    return dict



def get_file_size(path):
    if not is_valid_file(path, 'get_file_size', silent=True):
        db_print('dsh_utils.get_file_size: not valid file: ' + path,
                 111)
        return (False, 0)
    try:
        bytes = os.path.getsize(path)
    except:
        give_bad_news('get_file_size failed: ' + path, logging.error)
        return (False, 0)
    return (True, bytes)



def get_file_size2(path):
    """called by dsh_django_utils.get_file_size()."""
    
    if not is_valid_file(path, 'get_file_size', silent=True):
        return -1
    
    try:
        bytes = os.path.getsize(path)
        bytes = int(bytes)
        return bytes
    except:
        return -1



def get_file_size_str(path):
    """called by dsh_django_utils.get_file_size()."""

    bytes = get_file_size2(path)
    if bytes == -1:
        return ''

    bstr = str(bytes)
    if bytes < 1024:
        return bstr + 'B'
    if bytes < 1024 * 1024:
        return str(int(bytes / 1024)) + 'KB'

    return str(int(bytes / 1024 / 1024)) + 'MB'



def create_empty_file(fileName, message=''):
    if os.path.exists(fileName) and is_valid_file(fileName, msg=message):
        return True
    
    logging.debug('create_empty_file: file does not exist: '+
                  fileName)
    try:
        f = open(fileName, 'w')
        f.close
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
    """prints to console too."""
    if tag != RYW_DEBUG_TAG:
        return
    give_news(message, logFunc=logging.debug)



def db_print3(message, tag):
    """prints plain text to screen instead."""

    if tag == RYW_DEBUG_TAG or db_print_in_set(tag):
        give_news(message)

    return



def db_print_in_set(tag):
    """called by db_print3()"""
    return tag in RYW_DEBUG_TAG_PRINT_SET



def db_raise_or_print3(message, tag):
    """allows me to switch back and forth between raise and print3()."""
    #raise message
    if tag != RYW_DEBUG_TAG:
        return
    give_news(message)



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



def strip_join_str(s):
    """keep only alphanumeric characters and dots,
    replace everything else with - """
    t = s
    for x in s:
        if (not x in string.letters) and (not x in string.digits) and \
            x != '_' and x != '-' and x != '.':
            t = t.replace(x, '-')
    return t



#
# moved from ryw_ffmpeg, for extracting ffmpeg output
# returns (searchResult, group(1))
#
def extract_one_pattern(ffmpegOut, regex):
    regexComp = re.compile(regex)
    searchResult = regexComp.search(ffmpegOut)

    if searchResult == None:
        return None

    try:
        group1 = searchResult.group(1)
    except:
        return None

    return (searchResult, group1)



#
# moved and modified from ryw_ffmpeg.py
#
def extract_duration2(searchResult):
    if searchResult == None:
        return None
    try:
        hours = searchResult.group(1)
        minutes = searchResult.group(2)
        seconds = searchResult.group(3)
        return (hours,minutes,seconds)
    except:
        return None
    
    
#
# a wrapper of the two above functions
#
def extract_duration(ffmpegOut, regex):
    extracted = extract_one_pattern(ffmpegOut, regex)
    if not extracted:
        return None
    searchResult,group1 = extracted
    durationTuple = extract_duration2(searchResult)
    try:
        hours,minutes,seconds = durationTuple
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)
        seconds += ((hours*60) + minutes) * 60
        return seconds
    except:
        return None



#
# used to be in ryw_ffmpeg trying to execute extract stuff.
#
def try_execute(command):
    try:
        pipe = subprocess.Popen(command, shell=True,
                                stderr=subprocess.PIPE)
        execResult = pipe.communicate()[1]
        return execResult
    except:
        #
        # it seems to return an error code no matter what.
        # because it wants an output file?
        #
        return None



def union_dict(d1, d2):
    """returns the union of two dictionaries,
    called by dsh_dump.py to union object definitions."""
    answer = {}
    answer = dict(answer, **d1)
    answer = dict(answer, **d2)
    return answer



def red_error_break_msg(message):
    """called by dsh_dump, to give red error messages."""
    return '<font color=red>%s</font><br>\n' % (message,)



def black_break_msg(message, noBreak=False):
    """called by dsh_dump, to give regular messages."""
    if noBreak:
        return '%s\n' % (message,)
    return '%s<br>\n' % (message,)



def red_error_break_msg_debug(message, tag=0):
    """called by dsh_dump, to give red error messages."""

    if tag != RYW_DEBUG_TAG:
        return ''
    return '<font color=red>%s</font><br>\n' % (message,)



def black_break_msg_debug(message, tag=0):
    """called by dsh_dump, to give regular messages."""
    
    if tag != RYW_DEBUG_TAG:
        return ''
    return '%s<br>\n' % (message,)



def newest_file_in_dir(dir, ext=None):
    """called by dsh_django_utils.py.
    to find the most recently modified file in the red5 streams dir.
    ext tells the function what kind of file we're looking for."""

    if not is_valid_dir(dir):
        return None

    newest = None
    newestStamp = None
    
    listing = os.listdir(dir)
    for item in listing:
        
        if not item:
            continue
        if ext and not item.endswith(ext):
            continue
        path = os.path.join(dir, item)
        if os.path.isdir(path):
            continue
        if not os.path.isfile(path):
            continue
        fileSize = os.path.getsize(path)
        if fileSize == 0:
            continue

        thisStamp = os.path.getmtime(path)
        
        if newest == None:
            newest = item
            newestStamp = thisStamp
            continue

        if thisStamp < newestStamp:
            continue

        newestStamp = thisStamp
        newest = item

    return newest



def empty_dir(dir, keepList=[]):
    """just kills all the files in a directory.
    called from dsh_django_utils. """
    
    if not is_valid_dir(dir):
        return 

    listing = os.listdir(dir)
    for item in listing:
        if not item:
            continue
        path = os.path.join(dir, item)
        if os.path.isdir(path):
            continue
        if not os.path.isfile(path):
            continue
        if item in keepList:
            continue
        cleanup_path(path, 'dsh_utils.empty_dir: ')



#
# adapted from
# http://kutuma.blogspot.com/2007/08/sending-emails-via-gmail-with-python.html
#
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders



def gmail_send(gmailUser, gmailPwd, toList, subject, text,
               attachedFiles=None, attachmentNames=None):
    """send from gmail.
    gmail_send("rywang06@gmail.com",
        "Hello from python!",
        "This is a email sent with python",
        ['/tmp/x', '/tmp/y'],
        ['fileName1', 'fileName2'])
    returns (success,errorMsg)
    """


    errorMsg = ''
    msg = MIMEMultipart()
    commaSpace = ', '
    recipients = commaSpace.join(toList)

    msg['From'] = gmailUser
    msg['To'] = recipients
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    if attachedFiles:
        index = 0
        for attach in attachedFiles:
            part = MIMEBase('application', 'octet-stream')

            try:
                part.set_payload(open(attach, 'rb').read())
            except:
                errorMsg = 'dsh_utils.gmail_send() failed: ' +\
                           'failed to load attachment: ' + attach
                return (False, errorMsg)
            
            Encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                'attachment; filename="%s"' % \
                os.path.basename(attachmentNames[index]))
            msg.attach(part)
            index += 1

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPwd)

    try:
        mailServer.sendmail(gmailUser, toList, msg.as_string())
    except:
        errorMsg = 'dsh_utils.gmail_send() failed: ' +\
                   'mailServer.sendmail() failed.'
        return (False, errorMsg)
    
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()
    return (True, errorMsg)



def file_mtime(fn):
    return os.stat(fn)[-2]

    
def listdir_mtime(dirPath):

    if not is_valid_dir(dirPath, silence=True):
        return None

    try:
        fns = os.listdir(dirPath)
    except:
        return None

    try:
        fullNames = [os.path.join(dirPath, fn) for fn in fns]
        tuples = [(file_mtime(fn), fn) for fn in fullNames]
        tuples.sort()
        sorted = [os.path.basename(x[1]) for x in tuples]
        return sorted
    except:
        return None



def html_no_break(str):
    """disallow line breaks in HTML."""
    return '<span style="white-space: nowrap;">' + str + '</span>'



def time_date_day_str(when):
    time = when.strftime('%#H:%#M:%#S')
    date = when.strftime('%#Y-%#m-%#d')
    day  = when.strftime('%a')
    whenStr = html_no_break('%s, %s, %s' % (time, date, day))
    return whenStr
