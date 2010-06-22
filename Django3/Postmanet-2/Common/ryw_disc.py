import sys, os, pickle, cgi, cgitb, xmlrpclib, objectstore, random, shutil
import logging, datetime, time, zipfile, cStringIO, shutil
import su, ryw, string, ryw_upload, math



def remove_tmpdirs_keep_n(parent, n):
    """remove a bunch of subdirectories or files inside the parent directory,
    until only n of them remain"""

    if n < 0:
        raise NameError('remove_tmpdirs_keep_n: bad n: ' + repr(n))
        
    if not os.path.exists(parent):
        ryw.give_bad_news('remove_tmpdirs_keep_n: does not exist: '+parent,
                          logging.critical)
        return False

    if not os.path.isdir(parent):
        ryw.give_bad_news('remove_tmpdirs_keep_n: not a directory: '+parent,
                          logging.critical)
        return False

    try:
        os.chdir(parent)
        dirContent = os.listdir('.')
    except:
        ryw.give_bad_news('remove_tmpdirs_keep_n: failed to list dir: '+parent,
                          logging.critical)
        return False

    length = len(dirContent)
    if length == 0:
        logging.debug('remove_tmpdirs_keep_n: empty dir: ' + parent)
        return True
    if length <= n:
        logging.debug('remove_tmpdirs_keep_n: < n: ' + parent + ' ' + repr(n))
        return True

    try:
        dirContent.sort()
    except:
        ryw.give_bad_news('remove_tmpdirs_keep_n: failed to sort dir: ' +
                          parent, logging.critical)
        return False

    while length > n:
        try:
            first = dirContent.pop(0)
        except:
            ryw.give_bad_news('remove_tmpdirs_keep_n: failed to pop dir: '+
                              repr(dirContent))
            return False
        
        if not ryw.cleanup_path(first, 'remove_tmpdirs_keep_n:'):
            return False
        length -= 1

    return True



def getRecursiveSizeInKB(p):
    if not os.path.exists(p):
        logging.debug('getRecursiveSizeInKB: path does not exist: ' + p)
        return 0

    if os.path.isfile(p):
        kB = long(math.ceil(float(os.path.getsize(p)) / float(1024.0)))
        kB = long(math.ceil(kB / 4.0) * 4)
        return kB

    # let's say a directory is 4KB (find better Windows API?)
    count = 4
    for d in os.listdir(p):
        count += getRecursiveSizeInKB(os.path.join(p, d))
    return count



def get_tree_size(p):
    #logging.debug('get_tree_size: entered: ' + p)
    try:
        size = getRecursiveSizeInKB(p)
    except:
        ryw.give_bad_news('get_tree_size: failed: ' + p, logging.critical)
        return (False, 0)
    #logging.debug('get_tree_size: leaving: ' + p + ' ' + repr(size))
    return (True, size)
