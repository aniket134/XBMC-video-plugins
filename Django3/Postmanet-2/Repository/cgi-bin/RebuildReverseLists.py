import sys, os
import su
import cgi, cgitb, xmlrpclib, urllib
cgitb.enable()
import ryw,logging, ryw_view
import ReverseLists
import objectstore
import ryw_meta



def init_log():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('RebuildReverseLists: entered...')



def decide_path():
    resourcesPath = os.path.join(RepositoryRoot, 'Resources.txt')

    try:
        resources = ryw.get_resources(resourcesPath)
        tmpOutDir = ryw.get_resource_str(resources, 'tmpout')
        objectStoreRoot = ryw.get_resource_str(resources, 'objectstore')
        if not tmpOutDir or not objectStoreRoot:
            raise NameError('rebuildSearchFile: failed to get resources.')
        dateTimeRand = ryw.date_time_rand()
        newReverseListsFile = os.path.join(
            tmpOutDir, 'NewReverseLists' + dateTimeRand)
        return (True, newReverseListsFile, objectStoreRoot)
    except:
        ryw.give_bad_news('rebuildSearchFile: failed to get resources.')
        success = (False, None, None)



def go_through_object_store(objectStoreRoot, reverseLists):

    ryw.give_news2('go_through_object_store: entered...<BR>', logging.info)

    searchFile = reverseLists.searchFile
    for objID,version in objectstore.objectversioniterator(objectStoreRoot):

        objstr = objID + '#' + str(version)
        ryw.db_print2('examining ' + objstr + '...<BR>', 7)

        success,meta = searchFile.get_meta(objID, version)
        if not success or not meta:
            ryw.give_bad_news('go_through_object_store: get_meta2 failed: ' +
                               objstr, logging.warning)
            continue

        isList = meta.has_key('sys_attrs') and 'isList' in meta['sys_attrs']
        if not isList:
            ryw.db_print2('go_through_object_store: not a list object: ' +
                         objstr + '<BR>', 6)
            ryw.give_news2(' . ', logging.info)
            continue
        ryw.db_print2('go_through_object_sotre: found a list.<BR>', 6)

        containees = ReverseLists.read_container_file(
            objID, version, searchFile, RepositoryRoot)
        ryw.db_print2('go_through_object_store: containees are: ' +
                      repr(containees) + '<BR>', 7)
        if not reverseLists.add(objstr, containees):
            ryw.give_bad_news('go_through_object_store: ReverseLists.add ' +
                              'failed: ' + objstr, logging.error)
        else:
            ryw.db_print2('go_through_object_store: successfully added.<BR>',
                          7)
            alias = 'unnamed'
            if meta.has_key('content_alias'):
                alias = meta['content_alias']
            ryw.give_news2(objstr + ' ' + alias + ', ', logging.info)

    ryw.give_news2('<BR>done.', logging.info)



def main():
    init_log()
    ryw_view.print_header_logo()
    print '<TITLE>Rebuild ReverseLists</TITLE>'

    success,newReverseListsFile,objectStoreRoot = decide_path()
    if not success:
        sys.exit(1)

    success,searchFile,reverseLists = \
        ReverseLists.open_searchfile_reverselists(
            'RebuildReverseLists:',
            newReverseListsFileName = newReverseListsFile)
    if not success:
        sys.exit(1)
    else:
        ryw.give_news2('<BR>new ReverseLists generated at: ' +
                       newReverseListsFile + '<BR>', logging.info)

    go_through_object_store(objectStoreRoot, reverseLists)

    if reverseLists:
        reverseLists.done()
    ryw_view.print_footer()
    


if __name__ == '__main__':
    main()

