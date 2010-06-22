import sys, os
import su
import pickle
import logging
import cgi
import ryw, SearchFile, ryw_meta
import objectstore
import ReverseLists



def remove_from_search_file(searchFile, objID, version):
    if not searchFile.delete([(objID, version)]):
        ryw.give_bad_news(
            'DeleteObject.remove_from_search_file failed: ' + objID + ' # ' +
            str(version), logging.warning)



def remove_paths(paths):
    datapath = paths[0]
    metapath = paths[1]
    auxipath = paths[2]
    donepath = paths[3]
    mdonpath = paths[4]
    parent   = paths[5]
    viewpath = paths[6]

    if viewpath:
        ryw.cleanup_path(viewpath, 'DeleteObject.remove_paths view:')
        dir = os.path.dirname(viewpath)
        ryw.cleanup_partial_dir(dir, 'DeleteObject.remove_paths view:', False,
                                chmodFirst = True)
        logging.debug('DeleteObject.remove_paths: killed view path: ' +
                      viewpath)

    storePaths = (datapath,metapath,auxipath,donepath,mdonpath)
    ryw.remove_all_repo_dirs(storePaths)
    ryw.cleanup_partial_dir(parent, 'DeleteObject.remove_paths view::', False)
    logging.debug('DeleteObject.remove_paths: killed store paths: ' +
                  repr(storePaths))



def do_delete(objID, version, searchFile=None):
    """the optional searchFile argument is for cases of calling this
    thing in a loop: the first time, searchFile is None, so we do
    an open of the searchFile, and this gets returned to the caller,
    and the caller (in a loop) gets to reuse the searchFile argument."""    

    if not searchFile:
        searchFile = ryw_meta.open_search_file(RepositoryRoot)
        ryw.db_print('DeleteObject.do_delete: opening searchFile.', 18)
    else:
        ryw.db_print('DeleteObject.do_delete: reusing searchFile.', 18)
        
    if not searchFile:
        return (False, None)

    meta,objroot = ryw_meta.get_meta(searchFile, objID, version,
                                     RepositoryRoot)
    if not meta and not objroot:
        ryw.give_bad_news('do_delete: no meta, no objroot, giving up...',
                          logging.critical)
        searchFile.done()
        return (False, searchFile)

    #
    # try to continue deletion even if we can't get metadata.
    #

    paths = ryw_meta.get_paths(objroot, objID, version, meta, RepositoryRoot)
    if not paths:
        ryw.give_bad_news('do_delete: failed to get paths.',
                          logging.critical)
        searchFile.done()
        return (False, searchFile)

    if meta:
        #
        # hack.  I had a bug when the following function crashed
        # with meta=None
        # I didn't bother to understand what's going on.
        #
        process_reverse_lists(objID, version, meta, searchFile)

    remove_from_search_file(searchFile, objID, version)
    remove_paths(paths)
    searchFile.done()
    return (True, searchFile)



def process_reverse_lists(objID, version, meta, searchFile):
    success,reverseLists = ReverseLists.open_reverse_lists(
        'DeleteObject:', '', '',
        os.path.join(RepositoryRoot, 'ReverseLists'), True,
        searchFile = searchFile, repositoryRoot = RepositoryRoot)
    if success and reverseLists:
        reverseLists.delete_object(objID, version, RepositoryRoot, meta)
        reverseLists.done()
    else:
        ryw.give_bad_news('process_reverse_lists: failed to open '+
                          'ReverseLists file.', logging.critical)



def main():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('DeleteObject: entered...')

    ryw.print_header()

    success,objID,version = ryw.get_obj_str()
    if not success:
        sys.exit(1)

    success,searchFile = do_delete(objID, version)
    if success:
	sys.stdout.write("True")
        #ryw.give_good_news('Delete object: apparent success', logging.info)

    if searchFile:
        searchFile.done()

    sys.exit(0)


if __name__ == '__main__':
    main()
