import sys, os
import su
import objectstore, xmlrpclib, getopt, shutil, datetime, random
import logging, ryw, ryw_upload, ryw_uploadObj, SearchFile, ryw_meta
import ChapterList
import ryw_bizarro



usage = '''

Usage:
    python UploadObject.py [-p] <meta-data file name> <data file or directory name>

    Options:
        -p      Set this option if meta-data file contains a pickled dictionary.
                Otherwise, meta-data file is assumed to contain text conforming to a certain format.
'''



def check_attributes(values):
    """check, fix up attributes."""

    if not ryw_uploadObj.check_some_attributes(values):
        return (False, None)
    
    # generate unique upload timestamp
    now = datetime.datetime.now()
    date = now.date()
    time = now.time()
    # like Sep-07-1975---11-05-04-pm---467
    stamp = date.strftime('%b-%d-%Y') + '---' + time.strftime('%I-%M-%S-%p')
    random.seed()
    randomNo = random.randint(0,999)
    stamp += '---%03u' % randomNo

    if not values.has_key('repositoryuploadtime'):
        values['repositoryuploadtime'] = stamp

    # sanitize path
    if values.has_key('path'):
        separator = os.sep
        path = values['path']
        path = os.path.normpath(path)
        if path.startswith(separator):
            path = path[1:]
        if not path.startswith(values['creator']):
            path = os.path.join(values['creator'], path)
        if path.endswith(separator):
            path += 'anobject'
        values['path'] = path
        logging.debug('uploadobject: sanitized path: '+path)

    # need resources for objectstoreroot and viewroot
    try:
        resources = su.parseKeyValueFile(
            os.path.join(RepositoryRoot, 'Resources.txt'))
        objectstoreroots = resources['objectstore'].split(';')
        objectstoreroot = objectstoreroots[0]
    except:
        ryw.give_bad_news(
            'fatal_error: uploadobject: failed to access Resources.txt.',
            logging.critical)
        return (False, None)
    values['objectstore'] = objectstoreroot

    return (True, resources)



def add_to_search_file(values, hasVersion, cloneVersion=False):
    """need search file to send meta-data to.
    in turn, it gives us the version number to use for the object."""

    success,searchFile = ryw.open_search_file(
        'add_to_search_file:',
        os.path.join(RepositoryRoot, 'WWW', 'logs'),
        'upload.log',
        os.path.join(RepositoryRoot, 'SearchFile'),
        True)
    if not success:
        return (False, None)

    version = None
    try:
        if hasVersion:
            success = searchFile.add_this_version_to_search_file(values)
            version = values['version']
        else:
            success,version = searchFile.add_to_search_file(
                values, cloneVersion=cloneVersion)

        searchFile.done()
        values['version'] = version
    except:
        ryw.give_bad_news(
            'fatal_error: failed to add_to_search_file().', 
            logging.critical)
        searchFile.done()
        return (False, version)

    logging.debug('add_to_search_file passed: got version: ' +
                  repr(version))
    return (True, version)
    


def NOTUSED_talk_to_search_server(values):
    """NOT USED ANY MORE.
    need searchserver to send meta-data to.
    in turn, it gives us the version number to use for the object."""

    try:
        searchserver = xmlrpclib.ServerProxy("http://localhost:53972")
    except:
        ryw.give_bad_news(
            'fatal_error: uploadobject: failed to connect to search server.',
            logging.critical)
        return (False, None, None)

    version = None
    try:
        version = searchserver.addtosearchfile(values)
        values['version'] = version
    except:
        ryw.give_bad_news(
            'fatal_error: uploadobject: failed to addtosearchfile().', 
            logging.critical)
        return (False, searchserver, version)

    logging.debug('talk_to_search_server passed: got version: ' +
                  repr(version))
    return (True, searchserver, version)



def NOTUSED_remove_from_search_server(searchserver, version):
    """NOT USED ANY MORE.
    remove all traces from the search meta file."""
    ryw.give_bad_news(
        'warning: remove_from_search_server: still needs to be implemented.',
        logging.critical)



def remove_from_search_file(objectID, version):
    """remove all traces from the search meta file."""
    if not version or not objectID:
        return

    logging.debug('remove_from_search_file: entering: ' + objectID + ' ' +
                  str(version))

    success,searchFile = ryw.open_search_file(
        'remove_from_search_file:',
        os.path.join(RepositoryRoot, 'WWW', 'logs'),
        'upload.log',
        os.path.join(RepositoryRoot, 'SearchFile'),
        True)
    if not success:
        return

    try:
        searchFile.delete([(objectID, version)])
    except:
        ryw.give_news(
            'remove_from_search_file: delete: exception.',
            logging.debug)
        
    searchFile.done()



def remove_from_object_store(parent, datapath, metapath, auxpath, donepath):
    """remove all traces from the object store."""

    # the order is somewhat significant.
    # done flag first, metadata next, data last.
    # then give a shot at the parent directory and beyond.
    # if any part fails, we give up.
    if not ryw.cleanup_path(donepath, 'remove_from_object_store, donepath:'):
        return

    if not ryw.cleanup_path(auxpath, 'remove_from_object_store, auxpath:'):
        return

    if not ryw.cleanup_path(metapath, 'remove_from_object_store, metapath:'):
        return

    if not ryw.cleanup_path(datapath, 'remove_from_object_store, datapath:'):
        return

    ryw.cleanup_partial_dir(parent, 'remove_from_object_store, parent:', True)
    


def remove_view_path(path):
    """remove view path."""

    ryw.cleanup_path(path, 'remove_view_path:')
    dir = os.path.dirname(path)
    ryw.cleanup_partial_dir(dir, 'remove_view_path, removedirs:', False)


    
def mymove(src,dst):
    ryw_bizarro.move_stuff(src, dst)
    
        

def add_to_object_store(values, data, objectstoreroot, objectid, version,
                        auxDir, cloneVersion=False):
    """put (DATA, META, DONE) in the object store."""

    ##################################################
    # check free disk space.
    ##################################################
    if not cloneVersion and \
       not ryw_uploadObj.check_free_space(values, objectstoreroot):
        return (False, None, None, None, None, None)
    
    ##################################################
    # acquire prefix.
    ##################################################
    try:
        prefix = objectstore.nameversiontoprefix(objectstoreroot, objectid,
                                                 version)
    except:
        ryw.give_bad_news(
            'fatal_error: add_to_object_store: objectstore.nameversiontoprefix() failed.',
            logging.critical)
        return (False, None, None, None, None, None)
    
    datapath = prefix + '_DATA'
    metapath = prefix + '_META'
    donepath = prefix + '_DONE'
    auxpath  = prefix + '_AUXI'

    ##################################################
    # create parent directory.
    ##################################################
    parent = None
    try:
        parent = su.createparentdirpath(prefix)
        logging.debug('add_to_object_store: created parent dir: ' + parent)
    except:
        ryw.give_bad_news(
            'fatal_error: add_to_object_store: su.createparentdirpath() failed.',
            logging.critical)
        return (False, parent, None, None, None, None)
    
    if os.path.exists(donepath):
        ryw.give_news(
            'add_to_object_store: destination object already exists: ' +
            donepath, logging.warning)
        return (True, parent, datapath, metapath, auxpath, donepath)

    datapath = os.path.abspath(os.path.normpath(datapath))
    if (not cloneVersion):
        data = os.path.abspath(os.path.normpath(data))
        logging.debug('add_to_object_store: ' + datapath + ' ' +
                      metapath + ' ' + donepath + '.  source: ' + data)
    auxpath = os.path.abspath(os.path.normpath(auxpath))


    ##################################################
    # move data into the object store.
    ##################################################
    if cloneVersion:
        try:
            os.mkdir(datapath)
            ryw.db_print_info_browser('add_to_object_store: mkdir: ' +
                                      datapath, 29)
        except:
            ryw.give_bad_news(
                'fatal_error: add_to_object_store: cloneVersion mkdir: ' +
                datapath, logging.critical)
            return (False, parent, datapath, None, None, None)

        #
        # now deal with cloning a list, if necessary.
        #
        isList = ryw_meta.isList(values)
        if isList:
            baseName = os.path.basename(data)
            dirName = os.path.dirname(data)
            ryw.db_print2('UploadObject.add_to_object_store: basename: ' +
                          baseName, 44)
            ryw.db_print2('UploadObject.add_to_object_store: dirname: ' +
                          dirName, 44)
            destPath = os.path.join(datapath, baseName)
            srcChapterPath = os.path.join(dirName,
                                          ChapterList.CHAPTER_LIST_NAME)
            destChapterPath = os.path.join(datapath,
                                           ChapterList.CHAPTER_LIST_NAME)
            try:
                shutil.copyfile(data, destPath)
                ryw.db_print_info_browser(
                    'add_to_object_store: ' +
                    data + ' --> ' + destPath, 36)
                if os.path.exists(srcChapterPath):
                    shutil.copyfile(srcChapterPath, destChapterPath)
                    ryw.db_print_info_browser(
                        'UploadObject.add_to_object_store: ' +
                        srcChapterPath + ' --> ' + destChapterPath, 44)
                else:
                    ryw.db_print_info_browser(
                        'UploadObject.add_to_object_store: no chapter file.',
                        44)
            except:
                ryw.give_bad_news(
                    'add_to_object_store: failed to copy selection file.',
                    logging.critical)
                return (False, parent, datapath, None, None, None)
        
    elif os.path.isdir(data):
        try:
            mymove(data, datapath)
            logging.debug('add_to_object_store: moved dir: ' + data + ' ' +
                          datapath)
        except:
            ryw.give_bad_news(
                'fatal_error: add_to_object_store: move dir failed: ' +
                data + ' ' + datapath,
                logging.critical)
            return (False, parent, datapath, None, None, None)
        
    else:
        try:
            os.mkdir(datapath)
            mymove(data, os.path.join(datapath, os.path.basename(data)))
            logging.debug('add_to_object_store: moved file: ' + data + ' ' +
                          os.path.join(datapath, os.path.basename(data)))
        except:
            ryw.give_bad_news(
                'fatal_error: add_to_object_store: move file failed: ' +
                data + ' ' + datapath,
                logging.critical)
            return (False, parent, datapath, None, None, None)

    ##################################################
    # put metadata in the object store.
    ##################################################
    try:
        su.pickdump(values, metapath)
        logging.debug('add_to_object_store: written metapath: ' + metapath)
    except:
        ryw.give_bad_news(
            'fatal_error: add_to_object_store: su.pickdump() failed.',
            logging.critical)
        return (False, parent, datapath, metapath, None, None)

    ##################################################
    # put aux files in the object store.
    ##################################################
    try:
        if auxDir and os.path.exists(auxDir) and os.path.isdir(auxDir):
            mymove(auxDir, auxpath)
            logging.debug('add_to_object_store: moved auxpath: ' + auxpath)
    except:
        ryw.give_bad_news(
            'add_to_object_store: moving aux directory failed: ' + auxDir +
            ' -> ' + auxpath, logging.critical)
        return (False, parent, datapath, metapath, auxpath, None)


    ##################################################
    # put DONE flag in the object store.
    ##################################################
    try:
        f = open(donepath, 'w')
        f.close()
        logging.debug('add_to_object_store: written donepath: ' + donepath)
    except:
        ryw.give_bad_news(
            'fatal_error: add_to_object_store: write DONE file failed.',
            logging.critical)
        return (False, parent, datapath, metapath, auxpath, donepath)

    # TODO: In case of ANY failure, upload request copied to a REJECTED folder which can be looked upon later.

    return (True, parent, datapath, metapath, auxpath, donepath)



def create_view_path(values, resources, objectid, version):
    """create the view path."""

    if not values.has_key('path'):
        ryw.give_bad_news('warning: no view path given.', logging.warning)
        return (True, None)
    path = values['path']
    ryw.db_print2('create_view_path: path is: ' + path, 57)

    if not resources.has_key('viewroot'):
        ryw.give_bad_news('fatal_error: no viewroot in resources file.',
                          logging.critical)
        return (False, None)
    viewroot = resources['viewroot']
    ryw.db_print2('create_view_path: viewroot is: ' + viewroot, 57)
    path = os.path.join(viewroot, path)
    ryw.db_print2('create_view_path: now path is: ' + path, 57)

    success = ryw_uploadObj.create_view_path(path, objectid, version)
    return (success, path)



def uploadobject(values, data, auxDir, hasVersion = False,
                 cloneVersion=False):
    """update metadata file.
    upload object into object store.
    create view path."""

    logging.debug('UploadObject.uploadobject entered.')
    ryw.db_print2('uploadobject: values are: ' + repr(values), 57)

    ##################################################
    # check attributes.
    ##################################################
    success,resources = check_attributes(values)
    if not success:
        return False

    objectid = values['id']
    #
    # not strictly necessary, but I'm doing this to hardwire all
    # places of gettting objectstoreroot.
    #
    #objectstoreroot = values['objectstore']
    objectstoreroot = ryw.hard_wired_objectstore_root()
    logging.debug('uploadobject: passed check_attributes: '+
                  objectstoreroot + ' ' + objectid)


    ##################################################
    # give metadata to the search server.
    ##################################################
    success,version = add_to_search_file(values, hasVersion, cloneVersion)
    if not success:
        remove_from_search_file(objectid, version)
        return False
    else:
        ryw.db_print_info_browser('uploadobject: ' + objectid + '#' +
                                  str(version), 29)        


    ##################################################
    # put stuff into the object store.
    ##################################################
    success,parent,datapath,metapath,auxpath,donepath = \
        add_to_object_store(values, data, objectstoreroot, objectid, version,
                            auxDir, cloneVersion)
    if not success:
        remove_from_search_file(objectid, version)
        remove_from_object_store(parent, datapath, metapath, auxpath, donepath)
        return False


    ##################################################
    # create view path.
    ##################################################
    if not cloneVersion:
        success,path = create_view_path(values, resources, objectid, version)
        #ryw.give_news('uploadobject: introducing error...', logging.debug)
        #success = False
        if not success:
            remove_from_search_file(objectid,version)
            remove_from_object_store(parent, datapath, metapath,
                                     auxpath, donepath)
            remove_view_path(path)
            return False

    # logging.debug('just for testing...')
    # remove_view_path(path)
    # return False
    
    return True



#
# When executed as a script...
#
if __name__ == '__main__':

    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')

    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'p')
        if len(args) != 3:
            raise 'Need 3 arguments'
    except:
        print usage
        sys.exit(1)

    success,data,values,auxDir = ryw_uploadObj.process_args(optlist, args)
    if not success:
        sys.exit(1)
            
    logging.debug('UploadObject: script: done getting metadata')

    if not uploadobject(values, data, auxDir):
        ryw.give_bad_news('fatal_error: failed to uploadobject.',
                          logging.critical)
        sys.exit(1)

    logging.debug('UploadObject: uploadobject succeeded.')
    sys.exit(0)
