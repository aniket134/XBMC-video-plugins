import os, sys
import pickle
import glob
import types
import os.path

ObjectStoreRoot = '\\Postmanet\\repository\\WWW\\ObjectStore'
OriginalSearchFile = "\\Postmanet\\repository\\SearchFile"

def loadMeta(filename):
    """ loads metadata dictionary from filename"""
    
    try:
        f = open(filename)
        meta = pickle.load(f)
        f.close()
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
        print 'append_to_new_search_file : failed to append ' + meta + ' to search file: ' + searchfile
        return False
    return True

def loadSearchfile(searchfile):
 
    l = []
    try:
        f = open(searchfile)
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

def main(argv):
    
    argc = len(argv)
    if (argc == 0 or argc > 3):
        print "Usage: %s new_searchfile [ObjectStoreRoot] [OriginalSearchFile]"
        print "ObjectStoreRoot defaults to \\Postmanet\\repository\\WWW\\ObjectStore if argument not provided or an invalid path provided (can be relative or absolute)"
        print "If OriginalSearchFile is given, new_searchfile is compared against OriginalSearchFile"
        print "OriginalSearchFile defaults to \\Postmanet\repository\\SearchFile if provided argument is an invalid path (relative or absolute)"
        print "ObjectStoreRoot argument must be given if comparison against OriginalSearchFile is required (can be invalid to use default option) "
        return False
    
    searchfile = ""
    if (argc >= 1):
        searchfile = argv[0]
        if (os.path.exists(searchfile)):
            print "file by name of %s already exists. Please use some other name!\n" % (searchfile,)
            return False
    
    osr = ObjectStoreRoot
    if (argc >= 2):
        osr = argv[1]
	if not (osr.startswith("/") or osr.startswith("\\") or osr[1] == ':'):
            osr = os.path.join(os.getcwd(), osr)
            osr = os.path.abspath(osr)
        if not os.path.exists(osr):
            osr = ObjectStoreRoot
    if (osr == ObjectStoreRoot):
        print "Defaulting ObjectStoreRoot to %s" % (ObjectStoreRoot,)

    l = glob.glob(osr + "/?/?/?/?/*_META")
    for filename in l:
        meta = loadMeta(filename)
        append_to_new_search_file(searchfile,meta)
            
    if (argc == 3):
        osf = argv[2]
        if not (osf.startswith("/") or osf.startswith("\\")):
            osf = os.path.join(os.getcwd(),osf)
            osf = os.path.abspath(osf)
        if not os.path.exists(osf):
            print "OriginalSearchFile defaulting to %s" % (OriginalSearchFile,)
            osf = OriginalSearchFile
        print "Comparing new searchfile %s against OriginalSearchFile %s" % (searchfile,osf)
        compareSearchFile(osf,searchfile)

if __name__ == '__main__':
    main(sys.argv[1:])
