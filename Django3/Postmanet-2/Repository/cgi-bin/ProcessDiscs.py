import cgi, cgitb
cgitb.enable()

import os, sys, pickle, math, random, time, shutil
import su
import ryw, ryw_upload, logging, ryw_view
sys.path.append(os.path.join(RepositoryRoot, 'bin'))
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import UploadObject, EditObject, DeleteObject

import objectstore
import ryw_philips
import ReverseLists



def get_credential(mydir):
    cred = os.path.join(mydir, 'usercredentials')
    if not os.path.exists(cred):
        ryw.give_bad_news('get_credentials: credential file does not exist: '+
                          cred, logging.error)
        return None

    try:
        username = open(cred).readline().strip()
    except:
        return None

    logging.debug('get_credentials: directory, username: ' + mydir + ' ' +
                  username)
    return username



def process_download_requests(mydir, username):
    dlrq = os.path.join(mydir, 'downloadrequestqueue')
    if not os.path.exists(dlrq):
        logging.debug('process_download_requests: no incoming queue found.')
        return True

    try:
        newrq = su.pickload(dlrq)
    except:
        ryw.give_bad_news(
            'process_download_requests: failed to load new queue: ' + dlrq,
            logging.error)
        return False

    logging.debug('process_download_requests: found new queue: ' +
                  repr(newrq))

    oldrqfile = os.path.join(RepositoryRoot, 'QUEUES', username)

    oldrq = set([])
    if os.path.exists(oldrqfile):
        try:
            oldrq = su.pickload(oldrqfile)
        except:
            ryw.give_bad_news(
                'process_download_requests: failed to load old queue: ' +
                oldrqfile, logging.error)
            oldrq = set([])
    
    newrq = newrq.union(oldrq)
    logging.debug('process_download_requests: new queue: ' + repr(newrq))

    try:
        su.pickdump(newrq, oldrqfile)
    except:
        ryw.give_bad_news(
            'process_download_requests: failed to write new queue back: ' +
            oldrqfile, logging.error)
        return False
    return True



def get_data_name(uploaddir, obpref):
    updatadir = os.path.join(uploaddir, obpref + '_DATA')
    if not os.path.exists(updatadir):
        ryw.give_bad_news(
            'get_data_name: data directory not found: ' + uploaddir,
            logging.error)
        return None

    try:    
        ll = os.listdir(updatadir)
    except:
        ryw.give_bad_news('get_data_name: failed to listdir: ' + updatadir,
                          logging.error)
        return None

    if len(ll) == 1 and os.path.isfile(os.path.join(updatadir, ll[0])):
        obdata = os.path.join(updatadir, ll[0])
    else:
        obdata = updatadir

    logging.debug('get_data_name: got data name: ' + obdata)
    return obdata



def get_aux_name(uploaddir, obpref):
    upauxdir = os.path.join(uploaddir, obpref + '_AUXI')
    if not os.path.exists(upauxdir) or not os.path.isdir(upauxdir):
        logging.debug('get_aux_name: no aux dir found: ' + upauxdir)
        return None
    return upauxdir



def get_metadata(uploaddir, obpref):
    metaName = os.path.join(uploaddir, obpref + '_META')
    try:
        meta = su.pickload(metaName)
    except:
        ryw.give_bad_news('get_metadata: failed to load metadata: ' + metaName,
                          logging.error)
        return None
        
    logging.debug('get_metadata: got metadata ' + metaName + ' ' + repr(meta))
    return meta

    

def process_uploaded_objects(mydir):
    uploaddir = os.path.join(mydir, 'ObjectsToUpload')
    if not os.path.exists(uploaddir):
        logging.debug('process_uploaded_objects: no ObjectsToUploaded.')
        return True

    try:
        allNames = os.listdir(uploaddir)
    except:
        ryw.give_bad_news('process_uploaded_objects: failed to listdir: '+
                          uploaddir, logging.critical)
        return False

    for n in allNames:
        if not n.endswith('_DONE'):
            continue
        obpref = n[:-5]
        
        obdata = get_data_name(uploaddir, obpref)
        if not obdata:
            continue

        metadata = get_metadata(uploaddir, obpref)
        if not metadata:
            continue

        auxdir = get_aux_name(uploaddir, obpref)

        if not UploadObject.uploadobject(metadata, obdata, auxdir):
            ryw.give_bad_news(
                'process_uploaded_objects: UploadObject.uploadobject failed: '+
                repr(metadata) + ' ' + obdata, logging.critical)
            continue
        
        #command = '"%s" -u %s -p %s %s' % (sys.executable, os.path.join(RepositoryRoot, 'bin', 'UploadObject.py'), os.path.join(uploaddir, obpref + '_META'), obdata)
        #os.system(command)

    return True

#######################
### MIRRORING HACKS
#######################

## Get name of self
def self_name():
    try:
        self_name_file = os.path.join(RepositoryRoot, 'this_repository_name.txt')
        self_name = open(self_name_file).readline().strip()
    except: 
        ryw.give_bad_news('Could not get self_name from ' + self_name_file, logging.error)
        self_name = None

    return self_name

## See if a given (object, version) is present in an object store
def object_version_is_present(objroot, objid, version):
    paths = objectstore.name_version_to_paths_aux(objroot, objid, version)
    if os.path.exists(paths[3]):
        #ryw.give_news('object_version_is_present: exists: '  +
        #              objid + '#' +
        #              str(version), logging.info)
        ryw.give_news3('object already exists in database: '  +
                       objid + '#' + str(version), logging.info)
        #
        # place to test flushing problem
        #
        #time.sleep(10)
        #
        return True
    else:
        return False

## Get the root of the local object store
def get_local_object_store_root():
    try:
        resources = su.parseKeyValueFile(
            os.path.join(RepositoryRoot, 'Resources.txt'))
        objectstoreroots = resources['objectstore'].split(';')
        objectstoreroot = objectstoreroots[0]
        return objectstoreroot
    except:
        ryw.give_bad_news(
            'fatal_error: get_local_object_store_root: failed to access Resources.txt.',
            logging.critical)
        return None



def get_data_name_mirror(objDataDir, diskRoot, mapDict, itemName):
    if os.path.exists(objDataDir):
        updatadir = objDataDir
        logging.debug('get_data_name_mirror: found under objects: ' +
                      objDataDir)
    else:
        success,dirName,dataDir,auxiDir = ryw_philips.get_map_entry(
            diskRoot, mapDict, itemName)
        if not success:
            return None
        #ryw.give_news('get_data_name_mirror: found data: ' + dirName,
        #              logging.info)
        ryw.give_news3('found data: ' + dirName, logging.info)
        updatadir = dataDir

    try:    
        ll = os.listdir(updatadir)
    except:
        ryw.give_bad_news('get_data_name_mirror: failed to listdir: ' +
                          updatadir, logging.error)
        return None

    if len(ll) == 1 and os.path.isfile(os.path.join(updatadir, ll[0])):
        obdata = os.path.join(updatadir, ll[0])
    else:
        obdata = updatadir

    logging.debug('get_data_name_mirror: got data name: ' + obdata)
    return obdata



def get_aux_name_mirror(upauxdir, diskRoot, mapDict, itemName):
    if os.path.exists(upauxdir) and os.path.isdir(upauxdir):
        logging.debug('get_aux_name_mirror: found under objects: ' +
                      upauxdir)
        return upauxdir

    success,dirName,dataDir,auxiDir = ryw_philips.get_map_entry(
        diskRoot, mapDict, itemName)
    if not success:
        return None

    logging.debug('get_aux_name_mirror: got auxi name: ' + auxiDir)
    return auxiDir



def get_metadata_mirror(metaName):
    try:
        meta = su.pickload(metaName)
    except:
        ryw.give_bad_news('get_metadata_mirror: failed to load metadata: ' + metaName,
                          logging.error)
        return None
        
    logging.debug('get_metadata_mirror: got metadata ' + metaName + ' ' + repr(meta))
    return meta


#
# returns (Success, isStub)
#
def is_data_stub(dataDir):
    if not os.path.exists(dataDir) or not os.path.isdir(dataDir):
        return (True, False)
    try:
        lDir = os.listdir(dataDir)
        if len(lDir) == 1 and lDir[0] == ryw_philips.stubDirName:
            #ryw.give_news('is_data_stub: found stub at: ' + dataDir,
            #              logging.info)
            ryw.give_news3('found stub at: ' + dataDir, logging.info)
            return (True, True)
        else:
            return (True, False)
    except:
        ryw.give_bad_news('is_data_stub failed: ' + dataDir, logging.error)
        return (False, False)



def deal_with_stub(localObjRoot, objID, version,
                   metaData, dataDir, auxDir, searchFile = None):
    """thoughts regarding how many (unnecessary) times I'm going through
    the SearchFile... if there's data, the time spent on metadata is
    probably not a big deal...  so only this one, when we're only dealing
    with metadata, somewhat matters.  I think I'm still going to write
    through, to make things simpler.  the only optimization to take care
    of is to not to re-open the SearchFile over and over again."""
    
    success,searchFile = EditObject.do_update_metadata(
        localObjRoot, objID, version, metaData, searchFile = searchFile)
    if not success:
        ryw.give_bad_news('ProcessDiscs: EditObject failed: ' +
                          objID + '#' + str(version), logging.error)
        return (False, None)

    if not os.path.exists(auxDir):
        return (True, searchFile)

    oldPaths = objectstore.name_version_to_paths_aux(
        localObjRoot, objID, version)
    oldAuxDir = oldPaths[2]

    try:
        #ryw.give_news3('auxDir: ' + auxDir, logging.info)
        #ryw.give_news3('oldAuxDir: ' + oldAuxDir, logging.info)

        #ryw.give_news3('force remove: ' + oldAuxDir, logging.info)
        ryw.force_remove(oldAuxDir, 'deal_with_found_objects')
        #ryw.give_news3('recursive copy: ' + auxDir + ' -> ' + oldAuxDir,
        #               logging.info)
        shutil.copytree(auxDir, oldAuxDir)
    except:
        ryw.give_bad_news('ProcessDiscs: failed to overwrite auxi dirs: ' +
                          auxDir + ' -> ' + oldAuxDir, logging.critical)
        return (False, searchFile)

    return (True, searchFile)



## Special processing for disc from a peer repository
def process_disk_from_peer_repository(dir_name, diskRoot, overwrite=False):

    objectroot = os.path.join(dir_name, 'objects')
    if not os.path.exists(objectroot):
        logging.info(
            'process_disk_from_peer_repository: no objects directory.' +
            objectroot)
        return True
    
    ## Process all incoming objects

    local_object_root = get_local_object_store_root()
    if local_object_root is None:
        return False

    mapDict = ryw_philips.get_map(diskRoot)
    searchFile = None

    for objectId,version in objectstore.objectversioniterator(objectroot):

        ryw.give_news3('----------', logging.info)

        if mapDict == None:
            ryw.give_bad_news(
                'process_disk_from_peer_repository: failed to read map file: '+
                diskRoot, logging.error)
            return False

        #
        # We used to just skip objects already present.
        # now we want to do something.
        #
        #if object_version_is_present(local_object_root, objectId, version):
        #    ## object already present
        #    continue
        objectFound = object_version_is_present(local_object_root,
                                                objectId,
                                                version)

        paths = objectstore.name_version_to_paths_aux(objectroot,
                                                      objectId, version)

        itemName = objectId + '#' + str(version)

        obdata = get_data_name_mirror(paths[0], diskRoot, mapDict, itemName)
        if not obdata:
            continue

        success,isStub = is_data_stub(obdata)
        if not success:
            continue

        metadata = get_metadata_mirror(paths[1])
        if not metadata:
            continue

        auxdir = get_aux_name_mirror(paths[2], diskRoot, mapDict, itemName)

        if isStub and not objectFound:
            #ryw.give_bad_news(
            #    'ProcessDiscs: is a stub but not found in database: '+
            #    itemName, logging.error)
            ryw.give_news3(
                'ProcessDiscs error: is a stub but not found in database: '+
                itemName, logging.error)
            continue
        
        if isStub:
            success,searchFile = deal_with_stub(
                local_object_root, objectId, version, metadata,
                obdata, auxdir, searchFile = searchFile)
            if success:
                ryw.give_news3(
                    'ProcessDiscs success: meta data processed.',
                    logging.info)
            continue

        if objectFound:
            #ryw.give_bad_news(
            #    'ProcessDiscs: not a stub but found in the database: '+
            #    itemName, logging.error)
            ryw.give_news3(
                'ProcessDiscs: not a stub but found in the database: '+
                itemName, logging.error)

            if not overwrite:
                ryw.give_news3('processing skipped.', logging.error)
                continue
            
            #
            # I might want to delete the old version here.
            # using the code from DelObject, should be simple.
            #
            ryw.give_news3('deleting it...', logging.error)

            #
            # at one point, I thought I wanted to be clever and
            # tried to reuse searchFile below.  But the trouble is
            # that the UploadObject.uploadobject() call below will
            # change the SearchFile beneath me, and if I reuse
            # the searchFile here, I end up flushing the incorrectly
            # cached version back to disk. I actually would have
            # expected a deadlock when UploadObject.uploadobject()
            # tries to lock again but the deadlock somehow
            # didn't happen...
            #
            success,searchFile = DeleteObject.do_delete(
                objectId, version, searchFile=None)
            if not success:
                ryw.give_bad_news(
                    'ProcessDiscs: DeleteObject failed: ' +
                    objectId + '#' + str(version), logging.error)
                continue
            else:
                ryw.db_print('process_disk_from_peer_repository: ' +
                             'do_delete succeeded.', 18)
                
            #
            # falls through to continue onto adding the object.
            #
            
        if not UploadObject.uploadobject(metadata, obdata, auxdir,
                                         hasVersion = True):
            ryw.give_bad_news(
                'process_disk_from_peer_repository: ' +
                'UploadObject.uploadobject failed: '+
                repr(metadata) + ' ' + obdata, logging.critical)
            continue
        else:
            ryw.give_news3('ProcessDiscs success: new data uploaded.',
                           logging.info)
            continue

    incomingReverseLists = os.path.join(dir_name, 'ReverseLists')
    existingReverseLists = os.path.join(RepositoryRoot, 'ReverseLists')

    ReverseLists.merge_incoming(
        existingReverseLists, incomingReverseLists, RepositoryRoot,
        searchFile = searchFile)

    if searchFile:
        searchFile.done()
    return True



def process_disk(ppp, overWrite = False):
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    mydir = os.path.join(ppp, 'repository')
    logging.debug('process_disk: attempted: ' + mydir)

    username = get_credential(mydir)
    if not username:
        return False

    ## MIRRORING HACKS
    ## If incoming disk has username equal to this repository's name,
    ## then this is a disk coming from another peer repository, and hence
    ## must be processed with care.
    ## (If the disk was coming from a village, then it would have the username
    ## of that village.)
    if username == self_name():
        ryw.give_news(
            'process_disk: processing data intended for this ' +
            'peer repository: '+ username, logging.info)
        return process_disk_from_peer_repository(mydir, ppp,
                                                 overwrite = overWrite)

    ryw.give_news('process_disk: processing data from village site: '+
                  username, logging.info)
    
    # even if this fails, (ie., we failed to process download
    # requests,) we'll keep going.
    process_download_requests(mydir, username)

    process_uploaded_objects(mydir)
            
    return True



def process_finished_copies(tmpdir):
    # donelist is the list of disks that have been completely read

    try:
        donelist = os.listdir(tmpdir)
    except:
        ryw.give_bad_news(
            'process_finished_copies: listdir failed: ' + tmpdir,
            logging.critical)
        return
    
    logging.debug('process_finished_copies: ' + repr(donelist))
    if len(donelist) > 0:
        ryw.give_news('# of completed discs being processed: ' +
                      repr(len(donelist)), logging.debug)
    for n in donelist:
        name = os.path.join(tmpdir, n)
        ryw.give_news('disc name processed: ' + name, logging.info)
        if not process_disk(name):
            ryw.give_bad_news('process_finished_copies:failed for this disc2: '
                              + name, logging.error)

    ryw.give_news('done processing discs.', logging.info)


def redirect_to_on_disk_page(driveroot,redirectDisk):
    redirectStr = """
<script language="JavaScript" type="text/javascript">
<!--Comment tag so old browsers wont see code.
    alert("Error in processing disc. Please use link below to browse disc");
// end comment for old browsers -->
</script><BR><H2>
%s:file:///%s/repository/html/index.html
</H2><BR>
"""
    print redirectStr % (redirectDisk, driveroot)


def redirect_to_main_page(redirectWeb):
    redirectStr = """
<br><h2>
%s:http://localhost/cgi-bin/search_su.py?sort_field=Upload_Time&sort_order=decreasing
</h2><br>
<script language="JavaScript" type="text/javascript">
<!--Comment tag so old browsers wont see code.
    window.location = "http://localhost/cgi-bin/search_su.py?sort_field=Upload_Time&sort_order=decreasing";
// end comment for old browsers -->
</script>
"""
    print redirectStr % (redirectWeb,)


redirectDisk = "redirectDiskIndicator"
redirectWeb = "redirectWebIndicator"

def process_autorun_merge_request(discRoot, overwrite = False):
    if not process_disk(discRoot, overWrite = overwrite):
        ryw.give_bad_news('process_finished_copies: failed for this disc1: ',
                          logging.error)
        redirect_to_on_disk_page(discRoot,redirectDisk)
    else:
        ryw.give_news('done processing discs.', logging.info)
        redirect_to_main_page(redirectWeb)

		

def init_vals():
    ryw_view.print_header_logo()
    
    form = cgi.FieldStorage()
    tmpdir = form.getfirst('tmpdir', '')
    jobfile = form.getfirst('jobfile', '')
    autorunMerge = form.getfirst('autorun','')
    overwrite = form.getfirst('overwrite', '')
    
    if not tmpdir or not jobfile:
        ryw.give_bad_news(
            'ProcessDiscs.init_vals: bad input: tmpdir, jobfile: ' +
            tmpdir + ' ' + jobfile, logging.error)
        cgi.print_form(form)
        return (False, None, None, None, None)

    overWrite = False
    if overwrite == 'true' or overwrite == 'True':
        overWrite = True

    return (True, tmpdir, jobfile,autorunMerge, overWrite)



def main():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('ProcessDiscs: entered...')

    success,tmpdir,jobfile,autorunMerge,overWrite = init_vals()
    if not success:
        ryw_upload.quick_exit(1)
    
    logging.debug('ProcessDiscs: tmpdir,jobfile: ' + tmpdir + ' ' + jobfile)
    ryw.give_news('processing incoming disc images located in: ' + tmpdir,
                  logging.info)

    if autorunMerge:
	    process_autorun_merge_request(tmpdir, overwrite = overWrite)
	    sys.exit(0)

    process_finished_copies(tmpdir)
    ryw_upload.cleanup_incoming(tmpdir, jobfile)
    
    ryw_view.print_footer()
    sys.exit(0)



if __name__ == '__main__':
    main()
