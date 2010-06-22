import sys, os
import su
import pickle, cgi, cgitb, objectstore, shutil
import logging, math
import ryw, ryw_upload, ryw_view, ryw_meta, Browse, ryw_ffmpeg
import ReverseLists
cgitb.enable()



def print_header():
    name = os.getenv("REMOTE_USER")
    ryw_view.print_header_logo()

    print "<TITLE>Edit Result</TITLE>"
    resultStr = """
<P><FONT SIZE=3><B>Edit result</B></FONT>:
"""
    print resultStr



def setup_logging():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('EditObject: entered...')



def show_one_server_object(meta, searchFile):
    """like WebUpload_ryw.show_one_server_object() except that
    the searchFile is passed in."""
    
    print "<BR>"
    print Browse.script_str()
    #displayObject = ryw_view.DisplayObject(RepositoryRoot,
    #                                       calledByVillageSide = False,
    #                                       missingFileFunc = None)

    success,reverseLists = ReverseLists.open_reverse_lists(
        'EditObject:', '', '',
        os.path.join(RepositoryRoot, 'ReverseLists'), True,
        searchFile = searchFile,
        repositoryRoot = RepositoryRoot)
    if not (success and reverseLists):
        ryw.give_bad_news('EditObject: failed to open ReverseLists.',
                          logging.critical)
        if reverseLists:
            reverseLists.done()
        return False

    displayObject = ryw_view.DisplayObject(
        RepositoryRoot, calledByVillageSide = False,
        missingFileFunc = Browse.reqDownloadFunc,
        searchFile = searchFile,
        reverseLists = reverseLists)
    
    displayObject.begin_print()
    displayObject.show_an_object_compact(meta)
    displayObject.end_print()
    reverseLists.done()



def re_extract_or_not(form):
    reext = form.getfirst('med_reext', '')
    if reext == '':
        #ryw.give_news('dont want to re-extract.', logging.info)
        return False
    #ryw.give_news('want to re-extract.', logging.info)
    return True



def get_file_name(dataPath):
    try:
        names = os.listdir(dataPath)
        if len(names) == 0:
            return None
        for name in names:
            if name == 'Thumbs.db':
                continue
            return name
        return None
    except:
        ryw.give_bad_news(
            'EditObj: failed to listdir: ' + dataPath,
            logging.error)
        return None



def re_extract(dataPath, fileName, meta):
    if meta.has_key('ffmpeg'):
        del meta['ffmpeg']
    if meta.has_key('time_length'):
        del meta['time_length']
    if meta.has_key('time_length_seconds'):
        del meta['time_length_seconds']

    ryw_ffmpeg.try_exec(RepositoryRoot, meta, dataPath, fileName)

    success,bytes = ryw.get_file_size(os.path.join(dataPath, fileName))
    if success:
        meta['bytes'] = bytes
        meta['kB'] = math.ceil(bytes / 1024.0)
        
            

def main():
    # initialization.
    print_header()
    form = cgi.FieldStorage()
    setup_logging()

    # cgi.print_form(form)

    success,objID,version = ryw.get_obj_str2(form)
    if not success:
        ryw_upload.quick_exit(1)
    logging.debug('EditObject: ' + objID + '#' + str(version))

    if not ryw_meta.check_required_fields(form):
        ryw_upload.quick_exit(1)

    success,meta,objroot = ryw_meta.get_meta2(RepositoryRoot,
                                                  objID, version)
    if not success:
        ryw_upload.quick_exit(1)



    reext = re_extract_or_not(form)
    if reext:
        paths = ryw_meta.get_paths(objroot, objID, version,
                                   meta, RepositoryRoot)
        if not paths:
            ryw.give_bad_news('EditObject: failed to get paths.',
                              logging.critical)
            ryw_upload.quick_exit(1)

        dataPath = paths[0]
        fileName = get_file_name(dataPath)
        if not fileName:
            reext = False



    success = ryw_meta.process_error_fields(form, meta)
    if not success:
        ryw_upload.quick_exit(1)

    ryw_meta.process_fields(form, meta)
    logging.debug('EditObjects: ' + repr(meta))

    meta = ryw_upload.get_change_date_time(meta)

    #ryw.give_news(repr(meta), logging.info)



    if reext:
        re_extract(dataPath, fileName, meta)


    success,searchFile = do_update_metadata(objroot, objID, version, meta)
    if not success:
        ryw_upload.quick_exit(1)


    show_one_server_object(meta, searchFile)
    ryw.give_good_news('edit completed.', logging.info)

    ryw_view.print_footer()

    if searchFile:
        searchFile.done()
    sys.exit(0)



def do_update_metadata(objroot, objID, version, meta, searchFile=None):
    """this is also called by merging incoming data in
    ProcessDiscs.deal_with_stub().  only there, we're going to worry
    about the optional incoming SearchFile argument. there,
    we're trying to re-use the searchFile argument without
    re-opening it over and over again."""

    if not searchFile:
        ryw.db_print('do_update_metadata: null searchFile', 11)
    else:
        ryw.db_print('do_update_metadata: reusing searchFile', 11)
    
    if not ryw_meta.rewrite_meta(objroot, objID, version, meta):
        ryw.give_bad_news('EditObject: rewrite_meta failed.', logging.error)
        return (False, None)

    if not searchFile:
        searchFile = ryw_meta.open_search_file(RepositoryRoot,
                                               grabWriteLock = True)
    if not searchFile:
        ryw.give_bad_news('EditObject: failed to open search file.',
                          logging.critical)
        return (False, None)
        
    searchFile.modify(meta)
    return (True, searchFile)



if __name__ == '__main__':
    main()
