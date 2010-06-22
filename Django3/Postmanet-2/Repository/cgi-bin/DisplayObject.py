import sys, os
import su
import pickle
import logging
import cgi
import ryw, SearchFile, ryw_meta, ryw_view
import objectstore
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import DisplaySelection, EditObject



def do_show(objID, version):

    success,searchFile = ryw.open_search_file(
        'DisplayObject:',
        os.path.join(RepositoryRoot, 'WWW', 'logs'),
        'upload.log',
        os.path.join(RepositoryRoot, 'SearchFile'),
        False)
    if not success:
        return False

    success,meta = searchFile.get_meta(objID, version)
    if not success or not meta:
        ryw.give_bad_news(
            'DisplayObject.do_show: get_meta failed.', logging.critical)
        if searchFile:
            searchFile.done()
        return False
    
    EditObject.show_one_server_object(meta, searchFile)
    searchFile.done()
    return True



def main():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('DisplayObject: entered...')
    ryw_view.print_header_logo()

    print "<TITLE>Displaying an Object</TITLE>"

    success,objID,version = ryw.get_obj_str()
    if not success:
        ryw.give_bad_news('DisplayObject: failed to get objstr.',
                          logging.error)
        DisplaySelection.exit_now(1)

    if do_show(objID, version):
        pass
	#sys.stdout.write("True")
        #ryw.give_good_news('Delete object: apparent success', logging.info)

    DisplaySelection.exit_now(0)



if __name__ == '__main__':
    main()
