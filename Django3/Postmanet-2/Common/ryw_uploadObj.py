import sys, os, pickle, cgi, cgitb, xmlrpclib, objectstore, random, shutil
import logging, datetime, time, zipfile, cStringIO, shutil
import su, ryw, string, ryw_upload



def process_args(optlist, args):
    pk = False
    for i in optlist:
        option, value = i
        if option == '-p':
            pk = True

    meta = args[0]
    data = args[1]
    auxDir = args[2]

    try:
        if pk:
            values = su.pickload(meta)
        else:
            values = su.parseKeyValueFile(meta)
    except:
        ryw.give_bad_news('fatal_error: failed to get metadata: meta, data: '+
                          meta + ' ' + data, logging.critical)
        return (False, None, None, None)

    return (True, data, values, auxDir)



def check_some_attributes(values):
    """check, fix up attributes."""

    logging.debug('check_some_attributes: ' + repr(values))
    
    # must have a creator
    if not values.has_key('creator'):
        ryw.give_bad_news(
            'user_error: check_some_attributes: creator not specified',
            logging.critical)
        return False

    # must have kB field
    if not values.has_key('kB'):
        ryw.give_bad_news(
            'fatal_error: check_some_attributes: size (kB) not found',
            logging.critical)
        return False

    # get object id
    if not values.has_key('id'):
        values['id'] = objectstore.generateNewObjectID()

    logging.debug('check_some_attributes: passed.')
    return True



def check_free_space(values, path):
    """check available disk space."""

    freeKB = ryw.free_MB(path) * 1024
    logging.debug('check_free_space: freeKB, valuesKB: ' + repr(freeKB) + ' ' +
                  repr(values['kB']))
    if ryw_upload.pretty_much_out_of_space(values['kB'], freeKB):
        ryw.give_bad_news(
            'user_error: nearly out of space in the object store: ' +
            repr(values['kB']) + ' ' + repr(freeKB),
            logging.critical)
        return False

    logging.debug(
        'check_free_space: has space, kB, freekB: ' + repr(values['kB']) + ' '
        + repr(freeKB))
    return True



def create_view_path(path, objectID, version):
    if os.path.exists(path):
        ryw.give_news('create_view_path: already exists: ' + path + ', ' +
                      'replacing with new version.',
                      logging.warning)
        #return True
        #remove old view path and continue
        if not ryw.cleanup_path(path, 'create_view_path:'):
            ryw.give_news('create_view_path: fails to remove old view path.',
                          logging.error)
            return True
    
    try:
        su.createparentdirpath(path)
    except:
        ryw.give_bad_news('create_view_path: failed to createparentdirpath: '+
                          path, logging.critical)
        return False
    
    try:
        f = open(path, 'w')
        f.write(objectID + '#' + str(version))
        f.close()
    except:
        ryw.give_bad_news('create_view_path: failed to write leaf file: '+path,
                          logging.critical)
        return False
    
    logging.debug('create_view_path: done creating path: '+path)
    return True
