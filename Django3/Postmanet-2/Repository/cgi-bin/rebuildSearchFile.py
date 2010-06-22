import os, sys
import pickle
import glob
import types
import os.path
import ryw
import logging
import ryw_view



#ObjectStoreRoot = '\\Postmanet\\repository\\WWW\\ObjectStore'
#OriginalSearchFile = "\\Postmanet\\repository\\SearchFile"



ryw.check_logging(os.path.join(RepositoryRoot, 'WWW', 'logs'), 'upload.log')
logging.debug('rebuildSearchFile: entered...')
ryw_view.print_header_logo()
print '<TITLE>Rebuild Search File</TITLE>'

resourcesPath = os.path.join(RepositoryRoot, 'Resources.txt')

try:
    resources = ryw.get_resources(resourcesPath)
    tmpOutDir = ryw.get_resource_str(resources, 'tmpout')
    ObjectStoreRoot = ryw.get_resource_str(resources, 'objectstore')
    OriginalSearchFile = ryw.get_resource_str(resources, 'searchfile')
    if not tmpOutDir or not ObjectStoreRoot or not OriginalSearchFile:
        raise NameError('rebuildSearchFile: failed to get resources.')
except:
    ryw.give_bad_news('rebuildSearchFile: failed to get resources.',
                      logging.error)
    sys.exit(1)
    


def loadMeta(filename):
    """ loads metadata dictionary from filename"""
    
    try:
        #RYW: change to "rb"
        #f = open(filename, "rb")
        #meta = pickle.load(f)
        #f.close()
        meta = ryw.pickle_load_raw_and_text(filename)
        if not sanity_check(meta,filename):
            return None
        else:
            return meta
    except:
        print "Error loading metadata dictionary from META file %s\n" % (filename,)

def sanity_check(meta, filename):
    """ verify that the metadata dictionary loaded from filename is valid"""
    
    if (type(meta) != types.DictType):
        print "metadata loaded from file %s is not a dictionary\n" % (filename,)
        return False

    if not meta.has_key('id'):
        print "metadata loaded from file %s has no id key\n" % (filename,)
        return False

    if not meta.has_key('version'):
        print "metadata loaded from file %s has no version key\n" % (filename,)
        return False

    return True


def append_to_new_search_file(searchfile, meta):
    try:
        f = open(searchfile, 'ab')
    except:
        print 'append_to_new_search_file: failed to open search file: %s\n' % (searchfile,)
        return False

    try:
        pickle.dump(meta, f)
        f.close()
    except:
        print 'append_to_new_search_file : failed to append ' + \
              repr(meta) + ' to search file: ' + searchfile
        return False
    return True

def loadSearchfile(searchfile):
 
    l = []
    try:
        #RYW: change to "rb"
        f = open(searchfile, "rb")
    except:
        return l

    while True:
        try:
            l.append(pickle.load(f))
        except EOFError:
            break
        except:
            return l

    f.close()
    return l

def compareSearchFile(sf1, sf2):
    l1 = loadSearchfile(sf1)
    l2 = loadSearchfile(sf2)

    l12 = [x for x in l1 if x not in l2]
    l21 = [x for x in l2 if x not in l1]

    if not l12 and not l21:
        print "SearchFiles %s and %s are identical" % (sf1,sf2)
    else:
        print "Set of metadata info in %s but not in %s is %s" % (sf1,sf2,l12)
        print "Set of metadata info in %s but not in %s is %s" % (sf2,sf1,l21)



def main():

    dateTimeRand = ryw.date_time_rand()
    searchfile = os.path.join(tmpOutDir, 'NewSearchFile' + dateTimeRand)
    osr = ObjectStoreRoot
    
    #ryw.give_news2('ObjectStore is at: ' + osr + '<BR>', logging.info)
    ryw.give_news2('new SearchFile at: ' + searchfile + '<BR>', logging.info)
    ryw.give_news2('generating... &nbsp;&nbsp;', logging.info)
    
    l = glob.glob(osr + "/?/?/?/?/*_META")
    for filename in l:
        meta = loadMeta(filename)
        append_to_new_search_file(searchfile,meta)

    ryw.give_news2('done.<BR>', logging.info)

    osf = OriginalSearchFile
    ryw.give_news2('comparing against ' + osf + ' ... <BR>', logging.info)
    compareSearchFile(osf, searchfile)

    ryw_view.print_footer()



if __name__ == '__main__':
    main()

