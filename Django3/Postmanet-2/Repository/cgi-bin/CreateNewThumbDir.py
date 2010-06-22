import sys, os
import su
import pickle
import logging
import cgi
import ryw, SearchFile, ryw_meta, ryw_view
import objectstore



def init(enteredMsg, headerMsg):
    ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                      'upload.log')
    logging.debug(enteredMsg)
    ryw.print_header()
    print headerMsg

    success,objID,version = ryw.get_obj_str()
    if not success:
        return (False, None, None)

    logging.debug('CreateNewThumbDir.init: objstr: ' + objID + '#' +
                  str(version))
    print ryw_view.begin_print_str()
    return (True, objID, version)



def get_paths(objID, version):
    oRoot = os.path.join(RepositoryRoot, 'WWW', 'ObjectStore')
    try:
        success,meta = ryw.get_meta(oRoot, objID, version)
        if not success:
            ryw.give_bad_news(
                'CreateNewThumbDir.get_paths: ryw.get_meta failed: ' +
                repr(meta), logging.error)
            return (False,None,None)

        success,dataURL,auxiURL,auxiDir = ryw_view.get_server_URLs(meta)
        if not success:
            ryw.give_bad_news(
                'CreateNewThumbDir.get_paths: get_server_URLs failed: ' +
                repr(meta), logging.error)
            return (False,None,None)
        return (True,auxiURL,auxiDir)
    except:
        ryw.give_bad_news(
            'CreateNewThumbDir.get_paths: failed to get server URLs: ' +
            objID + '#' + str(version), logging.error)
        return (False,None,None)



def create_auxi_dir(auxiDir, subDir, createdMsg, existsMsg, modifyMsg):
    subDirPath = os.path.join(auxiDir, subDir)
    if not os.path.exists(subDirPath):
        try:
            os.makedirs(subDirPath)
            ryw.give_news(createdMsg + subDirPath, logging.debug)
        except:
            ryw.give_bad_news(
                'CreateNewThumbDir.create_auxi_dir: ' +
                'failed to create dir: ' + subDirPath, logging.error)
            return False
    else:
        ryw.give_news(existsMsg + subDirPath, logging.debug)

    ryw.give_news(modifyMsg, logging.debug)
    return True



def print_explorer_string(auxiURL, subDir, title):

    isLan = ryw.is_lan()
    ryw.db_print('print_explorer_string: isLan: ' + repr(isLan), 46)
    
    theStr = """
<BR>    
<A HREF="%(the_url)s" %(popup)s>%(anchor)s</A>
"""
    dict = {}
    theURL = ryw_view.glue_auxi_URL(auxiURL, subDir, '', checkIt = False)
    dict['the_url'] = theURL
    dict['popup'] = ryw_view.make_explorer_popup_string(
        theURL, (ryw_view.POPUP_DIR_WIDTH, ryw_view.POPUP_DIR_HEIGHT),
        pdrive=isLan)
    
    anchorStr = """
<IMG SRC="%(iconImg)s" TITLE="%(title)s" BORDER=0>"""
    d2 = {}
    d2['title'] = title
    if isLan:
        d2['iconImg'] = '/icons/p_folder.gif'
    else:
        d2['iconImg'] = '/icons/folder.gif'
    dict['anchor'] = anchorStr % d2
    print theStr % dict
    
    
    
def main():

    #
    # initialization businesses.
    #
    success,objID,version = init(
        'CreateNewThumbDir: entered...',
        '<FONT SIZE=4>Creating new thumbnail directory...</FONT><P>')
    if not success:
        sys.exit(1)

    #
    # get all the paths.
    #
    success,auxiURL,auxiDir = get_paths(objID, version)
    if not success:
        sys.exit(1)

    #
    # create thumbnail directory.
    #
    success = create_auxi_dir(auxiDir, 'thumbnails',
                              'Thumbnail directory created: ',
                              'Thumbnail directory exists: ',
                              'Add thumbnail images named as ' + 
                              '1_* and 2_* into the directory.')
    if not success:
        sys.exit(1)
                    

    #
    # create explorer strings.
    # 
    print_explorer_string(auxiURL, 'thumbnails', 'thumbnail directory')
    
    sys.exit(0)



if __name__ == '__main__':
    main()
