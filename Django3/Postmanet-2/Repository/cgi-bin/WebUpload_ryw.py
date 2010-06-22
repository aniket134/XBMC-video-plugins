import sys, os, math
import su
import pickle, cgi, cgitb, xmlrpclib, objectstore, random, shutil
import logging, datetime
import ryw, ryw_upload, ryw_view, Browse, ryw_ffmpeg
import ReverseLists
from ryw import give_bad_news

cgitb.enable()

sys.path.append(os.path.join(RepositoryRoot, 'bin'))
import UploadObject



def print_header():
    name = os.getenv("REMOTE_USER")
    ryw_view.print_header_logo()

    print "<TITLE>Upload Result</TITLE>"
    greetStr = """
<P><FONT SIZE=3><B>Upload result</B></FONT> (by %(user)s):
"""
    dict = {}
    dict['user'] = name
    print greetStr % dict

    return name



def setup_logging():
    """set up logging."""
    parentDir = os.path.join(RepositoryRoot, 'WWW', 'logs')
    ryw.setup_logging2(parentDir, 'upload.log')
    logging.info('headquarters upload attempted.')



def attempt_make_tmpdir():
    """attempt to make a temporary directory.
    returns the directory name made."""
    
    try:
        resources = su.parseKeyValueFile(os.path.join(RepositoryRoot,
                                                      'Resources.txt'))
        resTmpin = resources['tmpin']
    except:
        give_bad_news('fatal_error: failed to read Resources.txt',
                      logging.critical)
        return None

    tmpdir = ryw_upload.attempt_make_tmpdir(resTmpin)
    ryw.db_print_info_browser('attempt_make_tmpdir: ' + repr(tmpdir), 27)
    return tmpdir



def try_upload_object(meta, nameToUpload, auxDir, cloneVersion=False):
    """attempt to upload an object into the repository."""

    # intentionally not catching exception here
    if not UploadObject.uploadobject(meta, nameToUpload, auxDir,
                                     cloneVersion=cloneVersion):
        give_bad_news('fatal_error: failed to upload object into repository.',
                      logging.critical)
        return False

    logging.info('UploadObject.uploadobject: done.')
    return True



def show_one_server_object(meta):

    success,searchFile,reverseLists = \
        ReverseLists.open_searchfile_reverselists(
            'WebUpload_ryw.show_one_server_object:')
    if not success:
        return None
    
    print Browse.script_str()

    #displayObject = ryw_view.DisplayObject(RepositoryRoot,
    #                                       calledByVillageSide = False,
    #                                       missingFileFunc = None)
    displayObject = ryw_view.DisplayObject(
        RepositoryRoot, calledByVillageSide = False,
        missingFileFunc = Browse.reqDownloadFunc,
        searchFile = searchFile,
        reverseLists = reverseLists)
    
    displayObject.begin_print()
    displayObject.show_an_object_compact(meta)
    displayObject.end_print()

    reverseLists.done()
    return searchFile
    


def main():
    """main function processing upload."""

    # initialization.
    name = print_header()
    form = cgi.FieldStorage()
    setup_logging()

    localSuccess,localFound,localFilePath,localIsDir = \
        ryw_upload.check_local_file(form)
    if not localSuccess:
        ryw.give_bad_news('check_local_file failed.', logging.error)
        ryw_upload.quick_exit(1)

    if not ryw_upload.check_required_fields(form, checkFile=not localFound):
        ryw_upload.quick_exit(1)


    if localFound:
        buf = None
    else:
        # just read a tiny bit to see if we have an empty upload file.
        buf = ryw_upload.attempt_read_uploaded_file(form, 'local_filename')
        if not buf:
            ryw_upload.quick_exit(1)


    localExcerptResult = ryw_upload.check_local_file(
        form, fieldName = "local_excerpt_filename")


    # check aux file uploads: thumbnails, exerpts...
    success,auxExists,aux = ryw_upload.check_aux_file_uploads(
        form, localExcerptStuff = localExcerptResult)
    if not success:
        ryw_upload.quick_exit(1)

    tmpdir = attempt_make_tmpdir()
    if not tmpdir:
        ryw_upload.quick_exit(1)

    success,auxDir,auxInfo = ryw_upload.read_aux_files(
        form, aux, tmpdir, auxExists,
        localExcerptStuff = localExcerptResult)
    if not success:
        ryw_upload.cleanup_and_exit(tmpdir, None, None, 1)


    filename = ryw_upload.decide_tmp_data_file_name(
        form, localPath = localFilePath, isLocalDir = localIsDir)
    if not filename:
        ryw_upload.cleanup_and_exit(tmpdir, None, None, 1)

    success,found,bytes = ryw_upload.copy_local_file_for_upload(
        form, tmpdir, filename, localFound, localFilePath, localIsDir)
    if not success:
        ryw_upload.cleanup_and_exit(tmpdir, None, None, 1)
    kB = math.ceil(bytes / 1024.0)
    
    if not found:
        ryw.give_news2('<BR>Copying remote file...', logging.info)
        kB,bytes = ryw_upload.read_uploaded_file(form, buf, tmpdir,
                                                 filename,
                                                 'local_filename') 
    if kB == 0:
        ryw_upload.cleanup_and_exit(tmpdir, None, None, 1)

    meta = ryw_upload.try_process_attributes(name, form, filename,
                                             kB, bytes)
    if not meta:
        ryw_upload.cleanup_and_exit(tmpdir, None, None, 1)

    meta = ryw_upload.add_aux_attributes(meta, auxInfo)

    if not localIsDir:
        ryw_ffmpeg.try_exec(RepositoryRoot, meta, tmpdir, filename)

    success,metafile = ryw_upload.write_tmp_metafile(meta, tmpdir)
    if not success:
        ryw_upload.cleanup_and_exit(tmpdir, metafile, None, 1)

    if localIsDir:
        nameToUpload,extractDir = (os.path.join(tmpdir, filename), None)
    else:
        nameToUpload,extractDir = ryw_upload.try_unzip_file(
            form, tmpdir, filename, kB)
        if not nameToUpload:
            ryw_upload.cleanup_and_exit(tmpdir, metafile, extractDir, 1)

    ryw.give_news2('<BR>Storing the data in the repository...',
                   logging.info)
    ryw.db_print2("<BR>" + 'meta: ' + repr(meta) + "<BR>", 57);
    ryw.db_print2('nameToUpload: ' + nameToUpload + "<BR>", 22);
    ryw.db_print2('auxDir: ' + repr(auxDir) + "<BR>", 22);
    if not try_upload_object(meta, nameToUpload, auxDir):
        ryw_upload.cleanup_and_exit(tmpdir, metafile, extractDir, 1)

    #ryw_view.show_server_object(meta)
    searchFile = show_one_server_object(meta)
    searchFile.done()

    #cgi.print_form(form)

    ryw_upload.cleanup_and_exit(tmpdir, metafile, extractDir, 0)



if __name__ == '__main__':
    main()
