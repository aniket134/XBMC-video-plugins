import sys, os
import su
import logging, ryw
import pickle
import SearchFile
import win32file
import win32con
import win32security
import win32api
import pywintypes



def add_to_empty():
    sf = SearchFile.SearchFile(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                               'upload.log', 'foo', True)
    sf.add_to_search_file({'id':'123', 'description':'this is a test'})
    return sf



def add_to_existing():
    sf = SearchFile.SearchFile(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                               'upload.log', 'foo', True)
    sf.add_to_search_file({'id':'105', 'kB': 1, 'bytes': 2, 'upload_datetime': 'foo', 'description':'this is another test'})
    sf.add_to_search_file({'id':'105', 'kB': 1, 'bytes': 1, 'upload_datetime': 'foo', 'description':'test 2'})
    sf.add_to_search_file({'id':'106', 'kB': 1, 'bytes': 1, 'upload_datetime': 'foo', 'description':'test 3'})
    sf.add_to_search_file({'id':'107', 'kB': 1, 'bytes': 1, 'upload_datetime': 'foo', 'description':'test 4'})
    sf.add_to_search_file({'id':'108', 'kB': 1, 'bytes': 1, 'upload_datetime': 'foo', 'description':'test 5'})
    print 'add done...'
    return sf

    

def test_delete():
    sf = SearchFile.SearchFile(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                               'upload.log', 'foo', True)
    sf.printme()
    #sf.delete([('105', 1), ('108', 1), ('109', 1)])
    #sf.delete([('105', 2), ('106', 1)])
    sf.delete([('105', 4), ('107', 1)])
    sf.printme()
    sf.done()

    

def read_existing():
    sf = SearchFile.SearchFile(os.path.join(RepositoryRoot, 'WWW', 'logs'),
                               'SearchServer.log', 'SearchFile', False)
    v = sf._SearchFile__get_latest_version('6LK4PUWY2A0ETQ6RO__6')
    print 'version is: ' + str(v)
    return sf



def get_meta(sf):
    success,meta = sf.get_meta('103', 3)
    if not success:
        print 'get_meta failed.'
        return
    print 'get_meta returned: ' + repr(meta)



def main():
    #sf = add_to_existing()
    #win32api.Sleep(10000)
    #sf.done()
    # get_meta(sf)
    #sf = read_existing()
    #sf.done()

    #sf = add_to_existing()

    test_delete()    



main()
