import os,ryw,logging,sys,ryw_view,cgi
import ProcessDownloadReq
sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
import DisplaySelection
import ReverseLists



def main():
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug('DeleteFromSel: entered...')
    ProcessDownloadReq.print_header()

    #ProcessDownloadReq.delete_request(queue)

    form = cgi.FieldStorage()
    if (not form.has_key('objstr')) or (not form.has_key('selobj')):
        ryw.give_bad_news('DeleteFromSel.py: lacking arguments.',
                          logging.critical)
        DisplaySelection.exit_now(1)
        
    objstr = form.getfirst('objstr', '')
    selobj = form.getfirst('selobj', '')

    if (not objstr) or (not selobj):
        ryw.give_bad_news('DeleteFromSel.py: null arguments.',
                          logging.critical)
        DisplaySelection.exit_now(1)

    #ryw.give_news('DeleteFromSel.py: ' + objstr, logging.info)
    #ryw.give_news('DeleteFromSel.py: ' + selobj, logging.info)


    success,searchFile,reverseLists = \
        ReverseLists.open_searchfile_reverselists('DeleteFromSel:')
    if not success:
        ryw.give_bad_news(
            'DeleteFromSel: open_searchfile_reverselists failed.',
            logging.critical)
        DisplaySelection.exit_now(1)


    objID,version = selobj.split('#')
    version = int(version)
    rfpath = DisplaySelection.get_file_path(objID, version,
                                            searchFile=searchFile)
    if not rfpath:
        DisplaySelection.exit_now(1)

    success = ProcessDownloadReq.do_delete(rfpath, objstr)

    if success:
        sys.stdout.write("True")
    else:
        print "Failed to delete from selection."

    reverseLists.remove_obsolete_containers(objstr, [selobj])
    reverseLists.done()
    


if __name__ == '__main__':
    main()


