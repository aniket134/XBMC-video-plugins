import sys, os
import su
import logging, ryw
import pickle
import Flock



#
# usage?
# (1) for read, instantiate and cache in memory, read, read.
# (2) for write, instantiate, write, write, and call destructor.
#
# 2/19/08: why am I not holding a read lock?  I'm just going to
# rely on the copy cached in memory, and there should be enough
# defensive programming that even if the in-memory copy is out
# of date, the code should still be mostly ok.
#



class SearchFile:
    def __init__(self, logdir, logfile, searchfile, exclusive,
                 skipRead = False, skipLock = False):
        """raises exceptions.
        skipRead is set for the case of being used by Sobti's search
        code, where he did his own reading, so all I need is to do
        the locking."""

        if logdir and logfile:
            ryw.check_logging(logdir, logfile)
        logging.debug('SearchFile: initializing: ' + repr(logdir) + ' ' +
                      repr(logfile) + ' ' + searchfile)

        self.searchfile = searchfile
        self.lockfile = searchfile + '_LOCK'
        self.exclusive = exclusive
        
        if not self._SearchFile__create_lock_file():
            raise NameError('SearchFile.__init__: __create_lock_file failed')

        ryw.restore_cleanup_old_version(searchfile)
        
        if not os.path.exists(searchfile):
            logging.warning('SearchFile.__init__: searchfile not found: ' +
                            searchfile)
            self.index = {}
            return

        if skipRead and skipLock:
            return

        if skipRead:
            #
            # not skipLock, so try to lock.
            #
            if not self._SearchFile__lock():
                ryw.give_bad_news(
                    'SearchFile.__init__: __lock failed: ' + searchfile,
                    logging.critical)
                self._SearchFile__unlock()
                raise NameError('SearchFile.__init__: __lock failed')
            #
            # lock succeeded, and we skip read, so we're done.
            #
            return

        #
        # Now we know we need to read.  May or may not lock.
        #
        if not self._SearchFile__read_search_file(skipLk = skipLock):
            ryw.give_bad_news(
                'SearchFile.__init__: __read_search_file failed: ' +
                searchfile, logging.critical)
            raise NameError('SearchFile.__init__: __read_search_file failed')



    def __lock(self):
#       logging.debug('SearchFile.__lock: attempted... exclusive?' +
#                     repr(self.exclusive))
        if not os.path.exists(self.lockfile):
            ryw.give_bad_news('__lock: lock file does not exist: ' +
                              self.lockfile, logging.critical)
            return False

        try:
            self.lock = Flock.Flock(self.lockfile)
            self.lock.type['LOCK_EX'] = self.exclusive
            self.lock.type['LOCK_NB'] = 0
            self.lock.lock()
        except:
            ryw.give_bad_news('__lock: creating lock and locking failed: '+
                              self.lockfile, logging.critical)
            return False
#       logging.debug('SearchFile.__lock: acquired.')
        return True                



    def __unlock(self):
#       logging.debug('SearchFile.__unlock: attempted... exclusive?' +
#                     repr(self.exclusive))
	try:
            self.lock.unlock()
        except:
            logging.debug('__unlock: exception.')
#	except Exception, (errno, errorfunc, errorstmt):
#            if errno == 6 or errno == 158:
#                logging.debug('SearchFile.__unlock: already unlocked...')
#                return True
#            else:
#                ryw.give_bad_news('__unlock: failed to unlock: ' +
#                                  self.lockfile + ' ' + repr(errno),
#                                  logging.critical)
#                return False
#       logging.debug('__unlock: unlocked.')
        return True
        


    def __create_lock_file(self):
        return ryw.create_empty_file(self.lockfile,
                                     'SearchFile.__create_lock_file:')
        


    def __add_to_memory_index(self, objectID, version, item):
        if not self.index.has_key(objectID):
            self.index[objectID] = {}
        self.index[objectID][version] = item
        #logging.debug('__add_to_memory_index: read key#version: ' +
        #              repr(objectID) + '#' + str(version))
        # logging.debug('__add_to_memory_index: value: ' + repr(item))
        


    def __get_latest_version(self, objid):
        logging.debug('__get_latest_version: entered: ' + str(objid))
        if not self.index.has_key(objid):
            logging.debug('__get_latest_version: return 0.')
            return (True, 0)
        
        try:
            biggestVersion = max(self.index[objid].keys())
        except:
            ryw.give_bad_news(
                '__get_latest_version: failed to biggest version.',
                logging.critical)
            return (False, 0)

        logging.debug('__get_latest_version: ' + str(biggestVersion))
        return (True, biggestVersion)



    def __read_search_file(self, skipLk = False):
        """lock held if instantiate for write.
        lock released if instantiate for read."""
        
        assert(self.searchfile != None)

        if not skipLk:
            if not self._SearchFile__lock():
                self._SearchFile__unlock()
                return False
        
        try:
            f = open(self.searchfile, "rb")
        except:
            ryw.give_bad_news(
                '__read_search_file: failed to open search file: ' +
                self.searchfile, logging.critical)
            self._SearchFile__unlock()
            return False

        items = 0
        self.index = {}
        while True:
            try:
                item = pickle.load(f)
            except ValueError:
                item,f = ryw.pickle_reopen_read(self.searchfile, f, "rb")
            except EOFError:
                break
            except:
                ryw.give_bad_news(
                    '__read_search_file: failed to load pickle: ',
                    logging.critical)
                self._SearchFile__unlock()
                return False

            try:
                objectID = item['id']
                version = item['version']
            except:
                ryw.give_bad_news(
                    '__read_search_file: failed to get ID and version: '+
                    repr(item), logging.critical)
                self._SearchFile__unlock()
                return False

            self._SearchFile__add_to_memory_index(objectID, version, item)
            items += 1

        logging.debug('__read_search_file: items read: ' + repr(items))
        #logging.debug('__read_search_file: dict is: ' + repr(self.index))
        f.close()

        if not self.exclusive and not skipLk:
            self._SearchFile__unlock()
        return True



    def __append_to_search_file(self, meta):
        try:
            f = open(self.searchfile, 'ab')
        except:
            ryw.give_bad_news(
                '__append_to_search_file: failed to open search file: ' +
                self.searchfile, logging.critical)
            return False

        try:
            pickle.dump(meta, f)
            f.close()
        except:
            ryw.give_bad_news(
                '__append_to_search_file: failed to append to search file: ',
                logging.critical)
            return False

        logging.debug('__append_to_search_file: successfully appended.')
        return True
                


    def __is_same_as_latest(self, meta, latestVersion):
        """use checksum in the future?"""
        if latestVersion == 0:
            return False
        objID = meta['id']
        latestMeta = self.index[objID][latestVersion]

        #logging.debug('__is_same_as_latest: entered: '+
        #              repr(meta) + '   ?   ' + repr(latestMeta))

        for key in ['kB', 'bytes', 'upload_datetime']:
            if not meta.has_key(key) or not latestMeta.has_key(key):
                ryw.give_news(
                    '__is_same_as_latest: missing key: ' + repr(key),
                    logging.warning)
                ryw.give_news(
                    '   meta,latestMeta: ' + repr(meta) + ' ' +
                    repr(latestMeta), logging.warning)
                return False
            if meta[key] != latestMeta[key]:
                return False
        logging.debug('__is_same_as_latest: the same: ' + repr(meta) + ' == ' +
                      repr(latestMeta))
        return True           



    def add_to_search_file(self, meta, cloneVersion=False):
        """adds one to the existing version number."""
        logging.debug('add_to_search_file: ' + repr(meta))
        if not meta.has_key('id'):
            ryw.give_bad_news('add_to_search_file: missing ID...',
                              logging.critical)
            return (False, None)
        
        success,latestVersion = \
            self._SearchFile__get_latest_version(meta['id'])
        if not success:
            return (False, None)

        if not cloneVersion and \
            self._SearchFile__is_same_as_latest(meta, latestVersion):
            ryw.give_news('add_to_search_file: same version.',
                          logging.warning)
            return (True, latestVersion)

        latestVersion += 1
        meta['version'] = latestVersion

        if not self._SearchFile__append_to_search_file(meta):
            return (False, latestVersion)

        self._SearchFile__add_to_memory_index(meta['id'], latestVersion, meta)
        logging.debug('add_to_search_file: success.')
        return (True, latestVersion)



    def add_this_version_to_search_file(self, meta):
        """same as above but does not increment version number."""
        logging.debug('add_this_version_to_search_file: ' + repr(meta))
        if not meta.has_key('id') or not meta.has_key('version'):
            ryw.give_bad_news(
                'add_this_version_to_search_file: missing field(s)...',
                logging.critical)
            return False

        objID = meta['id']
        version = meta['version']

        success,existingMeta = self.get_meta(objID, version)
        if success:
            ryw.give_news(
                'warning: add_this_version_to_search_file: already exists: '+
                objID + ' ' + str(version), logging.warning)
            return True

        if not self._SearchFile__append_to_search_file(meta):
            return False

        self._SearchFile__add_to_memory_index(objID, version, meta)
        logging.debug('add_this_version_to_search_file: success.')
        return True



    def get_meta(self, objname, version):
        #logging.debug('get_meta: ' + objname + ' ' + str(version))
        if not self.index.has_key(objname):
            logging.debug('get_meta: obj name not found: ' + objname)
            return (False, None)
        if not self.index[objname].has_key(version):
            logging.debug('get_meta: obj version not found: ' +
                              objname + ' ' + str(version))
            return (False, None)
        meta = self.index[objname][version]
        #logging.debug('get_meta: ' + repr(meta))
        return (True, meta)



    def get_all_version_meta(self, objname):
        if not self.index.has_key(objname):
            logging.debug('get_meta: obj name not found: ' + objname)
            return (False, None)
        return (True, self.index[objname])



    def number_of_versions(self, objname):
        success,allVersions = self.get_all_version_meta(objname)
        if not success:
            return 0
        return len(allVersions)



    def __open_tmp_search_file(self):
        try:
            tmpFileName = self.searchfile + '_TMP'
            if os.path.exists(tmpFileName):
                ryw.cleanup_path(tmpFileName, '__open_tmp_search_file: ')
            f = open(tmpFileName, 'ab')
            logging.debug('__open_tmp_search_file: succeeded: ' + tmpFileName)
            return f
        except:
            ryw.give_bad_news('__open_tmp_search_file: failed' +
                              self.searchfile + '_TMP', logging.critical)
            return None



    def __write_minus(self, tmpFile, listToDelete):
        try:
            for objID,allVersions in self.index.iteritems():
                for version,meta in allVersions.iteritems():
                    pair = (objID, version)
                    if pair in listToDelete:
                        continue
                    pickle.dump(meta, tmpFile)
            tmpFile.close()
            logging.debug('__write_minus: done writing minus: ' +
                          repr(listToDelete))
            return True
        except:
            try:
                tmpFile.close()
            except:
                pass
            ryw.give_bad_news('__write_minus: failed' + repr(listToDelete),
                              logging.critical)
            return False



    def __write_modified(self, tmpFile, newMeta):
        try:
            for objID,allVersions in self.index.iteritems():
                for version,meta in allVersions.iteritems():
                    modifiedID = newMeta['id']
                    modifiedVersion = newMeta['version']
                    if modifiedID == objID and modifiedVersion == version:
                        pickle.dump(newMeta, tmpFile)
                    else:
                        pickle.dump(meta, tmpFile)
                        
            tmpFile.close()
            logging.debug('__write_modified: done writing modified.')
            return True
        except:
            try:
                tmpFile.close()
            except:
                pass
            ryw.give_bad_news('__write_modified: failed' + repr(newMeta),
                              logging.critical)
            return False



    def iterator(self):
        for objID,allVersions in self.index.iteritems():
            for version,meta in allVersions.iteritems():
                yield meta



    def __delete_from_memory(self, listToDelete):
        try:
            for pair in listToDelete:
                objID,version = pair
                if self.index.has_key(objID):
                    if self.index[objID].has_key(version):
                        del self.index[objID][version]
                        if len(self.index[objID]) == 0:
                            del self.index[objID]

            logging.debug('__delete_from_memory: done: ' +
                          repr(listToDelete))
            return True
        except:
            ryw.give_bad_news('__delete_from_memory: failed ' +
                              repr(listToDelete),
                              logging.critical)
            return False



    def __modify_in_memory(self, newMeta):
        try:
            found = True
            modifiedID = newMeta['id']
            modifiedVersion = newMeta['version']
            if self.index.has_key(modifiedID):
                if self.index[modifiedID].has_key(modifiedVersion):
                    self.index[modifiedID][modifiedVersion] = newMeta
                else:
                    found = False
            else:
                found = False
                
            if found:
                logging.debug('__modify_in_memory: done.')
                return True

            ryw.give_bad_news('__modify_in_memory: not found.',
                              logging.warning)
            return True
        except:
            ryw.give_bad_news('__modify_in_memory: error: ' +
                              repr(newMeta), logging.warning)
            return False            



    def __cleanup(self):
        ryw.cleanup_path(self.searchfile + '_TMP', '__cleanup, tmppath:')
        ryw.cleanup_path(self.searchfile + '_BAK', '__cleanup, bakpath:')



    def delete(self, listToDelete):
        logging.debug('delete: ' + repr(listToDelete))
        
        tmpSearchFile = self._SearchFile__open_tmp_search_file()
        if not tmpSearchFile:
            self._SearchFile__cleanup()
            return False
            
        if not self._SearchFile__write_minus(tmpSearchFile, listToDelete):
            self._SearchFile__cleanup()
            return False

        success,bakPath = ryw.make_tmp_file_permanent(
            self.searchfile + '_TMP', self.searchfile)

        if not self._SearchFile__delete_from_memory(listToDelete):
            return False

        #logging.debug('delete: done: ' + repr(self.index))
        logging.debug('delete: done: ' + repr(listToDelete))
        return True



    def modify(self, newMeta):
        logging.debug('modify: ' + repr(newMeta))

        tmpSearchFile = self._SearchFile__open_tmp_search_file()
        if not tmpSearchFile:
            self._SearchFile__cleanup()
            return False
            
        if not self._SearchFile__write_modified(tmpSearchFile, newMeta):
            self._SearchFile__cleanup()
            return False

        success,bakPath = ryw.make_tmp_file_permanent(
            self.searchfile + '_TMP', self.searchfile)

        if not self._SearchFile__modify_in_memory(newMeta):
            return False

        logging.debug('modify: done: ' + repr(newMeta))
        return True



    def printme(self):
        logging.debug('print: ' + repr(self.index))
    
        

    def done(self):
#       logging.debug('SearchFile.done: entered...')
        success = self._SearchFile__unlock()
#       logging.debug('SearchFile.done: unlock success?...' + repr(success))
        return success



    def convert_to_sobti_list(self):
        """in Search.py, Sobti does his own read and uses a list.
        we'll have to convert our dictionary to his list.
        not such a brilliant idea because it doubles memory
        consumption of the in-memory SearchFile, but..."""

        #return list(self.index)

        index = []
        for objID,allVersions in self.index.iteritems():
            for version,meta in allVersions.iteritems():
                index.append(meta)

        return index

