import sys, os
import su
import pickle
import logging
import cgi
import ryw, SearchFile, ryw_meta, ryw_view
import objectstore



def do_show(objID, version):

    success,meta,objroot = ryw_meta.get_meta2(RepositoryRoot, objID, version)
    if not success:
        return False

    ryw_meta.show_meta_edit_page(meta, '/cgi-bin/EditObject.py',
                                 objID + '#' + str(version))
    return True



def main():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('DeleteObject: entered...')

    success,objID,version = ryw.get_obj_str()
    if not success:
        sys.exit(1)

    if do_show(objID, version):
        pass
	#sys.stdout.write("True")
        #ryw.give_good_news('Delete object: apparent success', logging.info)

    sys.exit(0)


if __name__ == '__main__':
    main()
