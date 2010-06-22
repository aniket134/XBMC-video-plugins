#
# python reformat_ntfs.py /mnt/usb0/Postmanet [new_object_store_path]
#
#     (execute this in the Postmant-2 directory,
#      so it can pick up Common/ryw.py)
#
# if "new_object_store_path" is not supplied, it is assumed to be
#     "/u/Postmanet
#
# rewrites the ObjectStore component of all meta files in the target directory.
# rewrites the SearchFile as well.
#
# somewhat modeled after rebuildSearchFile.py.
#


NEW_OBJECT_STORE_ROOT = '/u/Postmanet/repository/WWW/ObjectStore'


import os, sys
import pickle
import glob
import types
import os.path
import logging


#
# import Common
#
cwd = os.getcwd()
common = os.path.join(cwd, 'Common')
if not os.path.exists(common):
    print "can't locate common directory."
    sys.exit(1)
sys.path.append(common)
import ryw
ryw.db_print3('common directory loaded.', 61)
import ryw_meta



def load_meta(filename):
    """ loads metadata dictionary from filename"""
    
    #f = open(filename, "rb")
    #meta = pickle.load(f)
    #f.close()
    meta = ryw.pickle_load_raw_and_text(filename)
    if not sanity_check(meta,filename):
        return None
    else:
        return meta

    
    try:
        f = open(filename, "rb")
        meta = pickle.load(f)
        f.close()
        if not sanity_check(meta,filename):
            return None
        else:
            return meta
    except:
        print "Error loading metadata dictionary from META file %s\n" \
              % (filename,)

        

def sanity_check(meta, filename):
    """ verify that the metadata dictionary loaded from filename is valid"""
    
    if (type(meta) != types.DictType):
        print "metadata loaded from file %s is not a dictionary\n" % \
              (filename,)
        return False

    if not meta.has_key('id'):
        print "metadata loaded from file %s has no id key\n" % (filename,)
        return False

    if not meta.has_key('version'):
        print "metadata loaded from file %s has no version key\n" % (filename,)
        return False

    return True



def rewrite_meta(metaPath, meta):
    donePath = metaPath.replace('_META', '_DONE')
    mdonPath = metaPath.replace('_META', '_MDON')
    dataPath = metaPath.replace('_META', '_DATA')
    auxiPath = metaPath.replace('_META', '_AUXI')
    paths = (dataPath, metaPath, auxiPath, donePath, mdonPath)
    ryw.db_print3('rewrite_meta: ' + repr(paths), 63)
    ryw.db_print3('rewrite_meta: ' + repr(meta), 62)
    ryw_meta.rewrite_meta(None, None, None, meta, paths)



def change_meta(meta, newObjStoreRoot):
    if not meta.has_key('objectstore'):
        ryw.give_bad_news3(
            'meta has no object store: ' +
            meta['id'] + '#' + str(meta['version']))
        ryw.give_bad_news3('    but continuing...')
        oldObjStore = ''
    else:
        oldObjStore = meta['objectstore']
        ryw.db_print3(meta['id'] + '#' + str(meta['version']), 64)
        ryw.db_print3(oldObjStore, 64)

    meta['objectstore'] = newObjStoreRoot
    ryw.give_news3(meta['id'] + '#' + str(meta['version']) + ': ' +
                   oldObjStore + ' -> ' + newObjStoreRoot)



def append_to_new_search_file(searchfileHandle, meta):
    f = searchfileHandle
    try:
        pickle.dump(meta, f)
    except:
        ryw.give_bad_news3('append_to_new_search_file : failed to append ' +
                           repr(meta) + ' to search file: ' + searchfile)
        return False
    return True



def main():

    #
    # get all the path names straight.
    #
    try:
        ntfsRoot = sys.argv[1]
    except:
        ryw.give_bad_news3(
            'usage: python reformat_ntfs.py /mnt/usb0/Postmanet ' +
            '[new_object_store_path]')
        sys.exit(-1)

    if len(sys.argv) >= 3:
        newObjStoreRoot = sys.argv[2]
    else:
        newObjStoreRoot = NEW_OBJECT_STORE_ROOT

    ryw.db_print3('newObjectStoreRoot is: ' + newObjStoreRoot, 62)
        
    if (not ntfsRoot) or (not os.path.exists(ntfsRoot)):
        ryw.give_bad_news3("can't find NTFS root: " + ntfsRoot)
        sys.exit(-1)

    ryw.db_print3('NTFS root is at: ' + ntfsRoot, 61)

    repositoryRoot = os.path.join(ntfsRoot, 'repository')
    oldSearchFileName = os.path.join(repositoryRoot, 'SearchFile')
    dateTimeRand = ryw.date_time_rand()
    newSearchFileName = os.path.join(repositoryRoot,
                                     'NewSearchFile' + dateTimeRand)

    objectStoreRoot = os.path.join(repositoryRoot, 'WWW',
                                   'ObjectStore')
    if (not os.path.exists(objectStoreRoot)):
        ryw.give_bad_news3("can't find object store: " + objectStoreRoot)
        sys.exit(-1)
    ryw.db_print3('object store root is at: ' + objectStoreRoot, 61)


    #
    # open the new search file.
    #
    try:
        newSearchFileHandle = open(newSearchFileName, 'ab')
    except:
        ryw.give_bad_news3('failed to open new search file: %s\n' % \
                           (searchfile,))
        sys.exit(-1)
    

    #
    # go through all the individual meta files.
    #
    l = glob.glob(objectStoreRoot + "/?/?/?/?/*_META")
    ryw.give_news3('rewriting meta data files...')
    for filename in l:
        ryw.db_print3('found meta: ' + filename, 61)
        meta = load_meta(filename)
        change_meta(meta, newObjStoreRoot)
        rewrite_meta(filename, meta)
        append_to_new_search_file(newSearchFileHandle, meta)



    #
    # replacing the old search file.
    #

    #ryw.copy_file_carefully('/u/rywang/tmp/x1',
    #                        '/u/rywang/tmp/x2',
    #                        '/u/rywang/tmp',
    #                        None,
    #                        'SearchFile_reformat')

    newSearchFileHandle.close()
    ryw.copy_file_carefully(oldSearchFileName, newSearchFileName,
                            repositoryRoot, None, 'SearchFile_reformat')
    ryw.give_news3('replacing search file: ' + oldSearchFileName +
                   ' <- ' + newSearchFileName)



if __name__ == '__main__':
    main()

