import sys, os
import su
import pickle, cgi, cgitb, xmlrpclib, objectstore, random, shutil
import logging, datetime
import ryw, ryw_upload, ryw_view
import math
import ReverseLists

from ryw import give_bad_news

cgitb.enable()

sys.path.append(os.path.join(RepositoryRoot, 'bin'))
import UploadObject

sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import WebUpload_ryw



#
# this is imitating the main function of WebUpload_ryw.py.
# just cuts out a few things.
#
def main():
    """main function processing upload."""

    # initialization.
    name = WebUpload_ryw.print_header()
    form = cgi.FieldStorage()
    WebUpload_ryw.setup_logging()

    if not ryw_upload.check_required_fields(form, checkFile = False):
        ryw_upload.quick_exit(1)


    localExcerptResult = ryw_upload.check_local_file(
        form, fieldName = "local_excerpt_filename")

    # check aux file uploads: thumbnails, exerpts...
    success,auxExists,aux = ryw_upload.check_aux_file_uploads(
        form, localExcerptStuff = localExcerptResult)
    if not success:
        ryw_upload.quick_exit(1)

    tmpdir = WebUpload_ryw.attempt_make_tmpdir()
    if not tmpdir:
        ryw_upload.quick_exit(1)

    success,auxDir,auxInfo = ryw_upload.read_aux_files(
        form, aux, tmpdir, auxExists,
        localExcerptStuff = localExcerptResult)
    if not success:
        ryw_upload.cleanup_and_exit(tmpdir, None, None, 1)

    bytes,name = ryw_upload.copy_queue_file(tmpdir, name)
    if bytes == 0:
        ryw_upload.cleanup_and_exit(tmpdir, None, None, 1)
    kB = math.ceil(bytes / 1024.0)
    filename = name
        

    #
    # the rest of this stuff copied straight from WebUpload_ryw.py
    # not nice, but hey.
    #
    meta = ryw_upload.try_process_attributes(name, form, filename, kB, bytes)
    if not meta:
        ryw_upload.cleanup_and_exit(tmpdir, None, None, 1)
    ryw_upload.add_set_attrs(meta, 'sys_attrs', 'isList')

    meta = ryw_upload.add_aux_attributes(meta, auxInfo)

    success,metafile = ryw_upload.write_tmp_metafile(meta, tmpdir)
    if not success:
        ryw_upload.cleanup_and_exit(tmpdir, metafile, None, 1)
    
    nameToUpload,extractDir = ryw_upload.try_unzip_file(
        form, tmpdir, filename, kB)
    if not nameToUpload:
        ryw_upload.cleanup_and_exit(tmpdir, metafile, extractDir, 1)

    ryw.give_news2('<BR>Storing the list in the repository...',
                   logging.info)
    if not WebUpload_ryw.try_upload_object(meta, nameToUpload, auxDir):
        ryw_upload.cleanup_and_exit(tmpdir, metafile, extractDir, 1)

    #ryw_view.show_server_object(meta)
    searchFile = WebUpload_ryw.show_one_server_object(meta)
    #
    # Ok to do this stuff after the display, because there's no
    # way the newly added selection could be a containee of someone else.
    #
    ReverseLists.add_queue(meta, searchFile, RepositoryRoot)
    searchFile.done()

    ryw_upload.cleanup_and_exit(tmpdir, metafile, extractDir, 0)

    # cgi.print_form(form)

    

if __name__ == '__main__':
    main()
