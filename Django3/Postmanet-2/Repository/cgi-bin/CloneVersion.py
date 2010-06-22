import sys, os, math
import su
import pickle, cgi, cgitb, xmlrpclib, objectstore, random, shutil
import logging, datetime
import ryw, ryw_upload, ryw_view, Browse, ryw_ffmpeg, ryw_meta
import ReverseLists
from ryw import give_bad_news
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import DisplaySelection


cgitb.enable()

sys.path.append(os.path.join(RepositoryRoot, 'bin'))
import UploadObject
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import DisplaySelection
import WebUpload_ryw



def print_header():
    name = os.getenv("REMOTE_USER")
    ryw_view.print_header_logo()

    print "<TITLE>Clone Version Result</TITLE>"
    greetStr = """
<P><FONT SIZE=3><B>Clone version result:</B></FONT>
"""
    print greetStr

    return name



def change_meta(meta, name):
    """change the metadata a bit before we clone it."""
    #
    # this forces UploadObject.check_attributes() to reassign a timestamp.
    #
    if meta.has_key('repositoryuploadtime'):
        del meta['repositoryuploadtime']

    if meta.has_key('upload_datetime_real'):
        del meta['upload_datetime_real']
    meta = ryw_upload.get_real_upload_date_time(meta)
    meta['upload_datetime'] = meta['upload_datetime_real']

    if meta.has_key('change_datetime'):
        del meta['change_datetime']

    meta['creator'] = name

    #if meta.has_key('kB'):
    #    del meta['kB']
    
    return meta
    


def main():

    name = print_header()
    form = cgi.FieldStorage()
    WebUpload_ryw.setup_logging()


    #
    # get objstr.
    #
    success,objID,version = ryw.get_obj_str2(form)
    if not success:
        ryw.give_bad_news('CloneVersion: failed to get objstr.',
                          logging.critical)
        ryw_upload.quick_exit(1)

    message = 'CloneVersion: ' + objID + '#' + str(version)
    logging.info(message)
    ryw.db_print2("<BR>" + message + "<BR>", 23);


    #
    # open search file.
    #
    success,searchFile = ryw.open_search_file(
        'CloneVerson',
        os.path.join(RepositoryRoot, 'WWW', 'logs'),
        'upload.log',
        os.path.join(RepositoryRoot, 'SearchFile'),
        False)
    if not success:
        if searchFile:
            searchFile.done()
        ryw.give_bad_news('CloneVersion: ' +
                          'open search file failed. ',
                          logging.critical)
        ryw_upload.quick_exit(1)
    else:
        ryw.db_print2("search file opened." + "<BR>", 23);


    #
    # get meta and paths.
    #
    success,paths,meta = DisplaySelection.get_all_paths(
        objID, version, skipLock=False, searchFile=searchFile,
        allowNullSearchFile=False)
    if success:
        ryw.db_print_info_browser('CloneVersion: paths: ' + repr(paths), 24)
        ryw.db_print_info_browser('CloneVersion: meta: ' + repr(meta), 29)
    else:
        ryw_upload.quick_exit(1)
        
    if (searchFile):
        searchFile.done()


    #
    # we do want to clone the data if it were a list.
    #
    isList = ryw_meta.isList(meta)
    if isList:
        dataPath = paths[0]
        selName = DisplaySelection.get_sel_name(dataPath)
        if not selName:
            ryw.give_bad_news(
                'CloneVersion: isList but failed to get selection name.',
                logging.error)
            ryw_upload.quick_exit(1)
        selPath = os.path.join(dataPath, selName)
    else:
        selPath,selName = None,None
            

    #
    # change meta.
    #
    meta = change_meta(meta, name)
                                   

    #
    # deal with auxi dir.
    #
    originalAuxiDir = paths[2]
    newAuxiDir = None
    tmpdir = None
    if os.path.exists(originalAuxiDir):
        tmpdir = WebUpload_ryw.attempt_make_tmpdir()
        if not tmpdir:
            ryw_upload.quick_exit(1)
        newAuxiDir = os.path.join(tmpdir, '_AUXI')

        message = 'CloneVersion: shutil.copytree(): ' + \
                  originalAuxiDir + '  ->  ' + newAuxiDir

        try:
            shutil.copytree(originalAuxiDir, newAuxiDir)
        except:
            ryw.give_bad_news('failed: ' + message, logging.critical)
            ryw_upload.cleanup_and_exit(tmpdir, None, None, 1)

        ryw.db_print_info_browser(message, 29)            
                              

    #
    # Now try to put a new object in the repository.
    # note that the version number will be incremented.
    #
    # "selPath" used to be just None.
    # when I added cloning list, I'm just using this to pass in the
    # path name of the selection file.
    #
    if not WebUpload_ryw.try_upload_object(meta, selPath, newAuxiDir,
                                           cloneVersion=True):
        ryw_upload.cleanup_and_exit(tmpdir, None, None, 1)


    searchFile = WebUpload_ryw.show_one_server_object(meta)
    searchFile.done()
        
    ryw_upload.cleanup_and_exit(tmpdir, None, None, 0,
                                successMessage = 'clone version completed.')



if __name__ == '__main__':
    main()
