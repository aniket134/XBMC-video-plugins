import sys, os
import su
import logging, ryw
import pickle
import Flock
import ryw_meta
import urllib
import ryw_view



#
# modeled after ryw.open_search_file()
#
def open_reverse_lists(msg, logdir, logfile, reverseListsFile, exclusive,
                       skipLk = False, searchFile = None,
                       repositoryRoot = None, allowNullSearchFile = False):
    reverseLists = None
    try:
        reverseLists = ReverseLists(
            logdir, logfile, reverseListsFile,
            exclusive, skipLock = skipLk,
            searchFile = searchFile,
            repositoryRoot = repositoryRoot,
            allowNullSearchFile = allowNullSearchFile)
    except:
        ryw.give_bad_news(msg + ' ' +
            'open_reverse_lists: failed to open reverse lists.',
            logging.critical)
        if reverseLists:
            reverseLists.done()
        return (False, None)
    return (True, reverseLists)



def add_to_reverse_lists(msg, logdir, logfile, reverseListsFile,
                         containerName, containeeList,
                         searchFile, repositoryRoot):
    """defunct.  nothing wrong, just not used any more.
    called when we are ready to add a forward list to the
    ReverseLists. currently called by DisplaySelection.py."""
    
    success,reverseLists = open_reverse_lists(
        msg, logdir, logfile, reverseListsFile, True,
        searchFile = searchFile, repositoryRoot = repositoryRoot)
    if not success:
        return False
    result = reverseLists.add(containerName, containeeList)
    reverseLists.done()
    return result



def container_string(containers):
    """called to spit out the italic strings below the description.
    doh! turns out searchFile is not needed here.  well..."""
    
    if containers == []:
        return ''
    
    ansStr = ' part of series: '
    for container in containers:
        objstr = urllib.quote(container[0])
        alias = container[1]
        aliasLinkStr = """<A
HREF="/cgi-bin/DisplayObject.py?objstr=%(objstr)s">%(alias)s</A>"""
        d = {}
        d['objstr'] = objstr
        d['alias'] = alias
        ansStr += aliasLinkStr % d + ', '

    #logging.debug('ReverseLists.container_string: ' + ansStr)
    return ansStr



def container_detail_string(containers):
    """called to spit out the detailed strings in the magnifying
    glass popup window.
    doh! turns out searchFile is not needed here.  well..."""
    
    if containers == []:
        return ''

    ansStr = '<LI><B>Part of series: </B>'
    for container in containers:
        objstr = urllib.quote(container[0])
        title = container[2]
        titleLinkStr = """<A HREF=/cgi-bin/DisplayObject.py?objstr=%(objstr)s>%(title)s</A>"""
        d = {}
        d['objstr'] = objstr
        d['title'] = ryw_view.scrub_js_string(title)
        ansStr += titleLinkStr % d + ', '


    ansStr = ansStr.rstrip()
    ansStr = ansStr.rstrip(',')
    return ansStr



def get_path(objID, version, searchFile, repositoryRoot):
    """a helper function.
    a replacement for DisplaySelection.get_path().
    called by get_file_path() below."""
    
    success,meta = searchFile.get_meta(objID, version)
    if not success or not meta:
        ryw.give_bad_news(
            'ReverseLists.get_path: get_path failed.', logging.critical)
        return (False, None)

    objroot = ryw_meta.get_objectstore_root(repositoryRoot, meta)
    paths = ryw_meta.get_paths(objroot, objID, version,
                               meta, RepositoryRoot)
    if not paths:
        ryw.give_bad_news('ReverseLists.get_path: failed to get paths.',
                          logging.critical)
        return (False, None)

    return (True, paths[0])



def get_file_path(objID, version, searchFile, repositoryRoot):
    """a helper function.
    a replacement for DisplaySelection.get_file_path,
    faster lookup using the searchFile passed in.
    called by read_container_file."""
    
    sys.path.append(os.path.join(RepositoryRoot, 'cgi-bin'))
    import DisplaySelection

    success,dataPath = get_path(objID, version, searchFile, repositoryRoot)
    if not success:
        return None

    name = DisplaySelection.get_sel_name(dataPath)
    if not name:
        ryw.give_bad_news(
            'ReverseLists.get_file_path: failed to get selection ' +
            'file name:<br>'+ dataPath, logging.error)
        return None

    rfpath = os.path.join(dataPath, name)
    return rfpath



def read_container_file(conID, conVersion, searchFile, repositoryRoot):
    """given a container ID, read its content.
    this is an internal helper function."""

    sys.path.append(os.path.join(repositoryRoot, 'cgi-bin'))
    import ShowQueue

    ryw.db_print('read_container_file entered: '+conID+'#'+
                 str(conVersion), 1)

    rfpath = get_file_path(conID, conVersion, searchFile, repositoryRoot)
    if not rfpath:
        return []

    ryw.db_print('read_container_file: got file path: ' + rfpath, 1)
    containees = ShowQueue.read_list(rfpath)
    ryw.db_print('read_container_file: got content: ' +
                 repr(containees), 1)
    return containees
    


def is_in_container_file(conID, conVersion, thisContainee, searchFile,
                         repositoryRoot):
    """given a container ID, read its content.
    check to see if thisContainee is indeed in the list.
    this is an internal helper function."""

    containees = read_container_file(conID, conVersion, searchFile,
                                     repositoryRoot)
    return (containees != None) and (thisContainee in containees)



def merge_incoming(existingName, incomingName, repositoryRoot,
                   searchFile=None):
    """called by ProcessDiscs.py"""

    logging.info('merge_incoming: ' + existingName + ' <- ' + incomingName)
    
    if not ryw.is_valid_file(incomingName, 'copy_reverse_lists:'):
        ryw.give_news3('merge_incoming: incoming ReverseLists not found.',
                       logging.info)
        return True

    if not searchFile:
        success,searchFile = ryw.open_search_file(
            'merge_incoming:',
            os.path.join(RepositoryRoot, 'WWW', 'logs'),
            'upload.log',
            os.path.join(RepositoryRoot, 'SearchFile'),
            False)
        if not success:
            if searchFile:
                searchFile.done()
            ryw.give_bad_news('merge_incoming: open search file failed. ',
                              logging.critical)
            return False

    success,existingRL = open_reverse_lists('ReverseLists.merge_incoming:',
                                            '', '', existingName, True,
                                            searchFile = searchFile,
                                            repositoryRoot = repositoryRoot)
    if not success:
        ryw.give_bad_news('merge_incoming: failed to open existing list.',
                          logging.critical)
        if existingRL:
            existingRL.done()
        return False

    success,incomingRL = open_reverse_lists('ReverseLists.merge_incoming:',
                                            '', '', incomingName, False,
                                            skipLk = True,
                                            allowNullSearchFile = True)
    if not success:
        ryw.give_bad_news('merge_incoming: failed to open incoming list.',
                          logging.error)
        if incomingRL:
            incomingRL.done()
        return False
        
    success = existingRL.merge(incomingRL, repositoryRoot)

    existingRL.done()
    incomingRL.done()

    if searchFile:
        searchFile.done()
    return success



def is_valid_local_object(objstr, repositoryRoot, searchFile):
    """a small helper function."""
    
    success,objID,objVersion = ryw.split_objstr(objstr)
    if not success:
        logging.warning('ReverseLists.is_valid_local_object: ' +
                        'failed to split: ' + objstr)
        return False
    
    success,meta = searchFile.get_meta(objID, objVersion)
    return success and meta



def open_searchfile_reverselists(callerStr, searchFileWriteFlag=False,
                                 reverseListsWriteFlag = True,
                                 newReverseListsFileName = None):
    """opens both SearchFile and ReverseLists in preparation for use
    by DisplayObject. called by all the display guys unless they
    need to open or already have opened these files separately."""

    success,searchFile = ryw.open_search_file(
        callerStr,
        os.path.join(RepositoryRoot, 'WWW', 'logs'),
        'upload.log',
        os.path.join(RepositoryRoot, 'SearchFile'),
        searchFileWriteFlag)
    if not success:
        if searchFile:
            searchFile.done()
        ryw.give_bad_news('open_searchfile_reverselists: ' +
                          'open search file failed. ' +
                          'called by: ' + callerStr,
                          logging.critical)
        return (False, None, None)

    if not newReverseListsFileName:
        newReverseListsFileName = os.path.join(
            RepositoryRoot, 'ReverseLists')
            
    success,reverseLists = open_reverse_lists(
        callerStr, '', '', newReverseListsFileName, True,
        searchFile = searchFile,
        repositoryRoot = RepositoryRoot)
    if not success:
        ryw.give_bad_news('open_searchfile_reverselists: ' +
                          'open reverse lists failed. ' +
                          'called by: ' + callerStr,
                          logging.critical)
        if reverseLists:
            reverseLists.done()
        if searchFile:
            searchFile.done()
        return (False, None, None)

    return (True, searchFile, reverseLists)



def add_queue(meta, searchFile, repositoryRoot):
    """called by UploadQueue.py, after saving a selection.
    returns success."""
    
    objID = meta['id']
    version = meta['version']

    logging.info('add_queue: entered: ' + objID)
    ryw.db_print2('add_queue: entered: ' + objID, 12)

    success,reverseLists = open_reverse_lists(
        'add_queue:', '', '',
        os.path.join(repositoryRoot, 'ReverseLists'), True,
        searchFile = searchFile,
        repositoryRoot = repositoryRoot)
    if not (success and reverseLists):
        ryw.give_bad_news('add_queue: failed to open ReverseLists.',
                          logging.critical)
        if reverseLists:
            reverseLists.done()
        return False

    containees = read_container_file(objID, version,
                                     searchFile, repositoryRoot)
    ryw.db_print2('add_queue: found containees: ' + repr(containees), 12)
    if not containees or containees == []:
        return True
    
    success = reverseLists.add(objID + '#' + str(version), containees)
    reverseLists.done()
    ryw.db_print2('add_queue: finished.', 12)
    return success



#
# modeled after SearchFile.py
#
#
# usage?
# (1) for read, instantiate and cache in memory, read, read.
# (2) for write, instantiate, write, write, and call destructor.
#


class ReverseLists:
    def __init__(self, logdir, logfile, reverseListsFile, exclusive,
                 skipLock = False, searchFile = None,
                 repositoryRoot = None,
                 allowNullSearchFile = False):
        """raises exceptions.
        skipLock is set to True when called by merging incoming:
        the incoming ReverseLists file is not locked."""

        if logdir and logfile:
            ryw.check_logging(logdir, logfile)
        #logging.debug('ReverseLists: initializing: ' + repr(logdir) + ' ' +
        #              repr(logfile) + ' ' + reverseListsFile)

        self.reverseListsFile = reverseListsFile
        self.lockfile = reverseListsFile + '_LOCK'
        self.exclusive = exclusive
        self.skipLock = skipLock
        self.searchFile = searchFile
        self.repositoryRoot = repositoryRoot

        if not allowNullSearchFile:
            if not searchFile or not repositoryRoot:
                raise NameError('ReverseLists.__init__: ' +
                                'bad searchFile or ' +
                                'bad repositoryRoot.')

        if not skipLock:
            logging.info('ReverseLists.__init__: skipping locking.')
            if not self._ReverseLists__create_lock_file():
                raise NameError('ReverseLists.__init__: ' +
                                '__create_lock_file failed.')

        try:
            ryw.restore_cleanup_old_version(reverseListsFile)
        except:
            pass
        
        if not os.path.exists(reverseListsFile):
            logging.warning('ReverseLists.__init__: reverseListsFile ' +
                            'not found: ' + reverseListsFile)
            self.reverseDict = {}
            try:
                su.pickdump(self.reverseDict, reverseListsFile)
            except:
                ryw.give_bad_news('ReverseLists.__init__: pickdump ' +
                                  'failed.', logging.critical)
                raise NameError('ReverseLists.__init__: __lock failed')
            
        if not self._ReverseLists__read_reverse_lists_file():
            ryw.give_bad_news(
                'ReverseLists.__init__: ' +
                '__read_reverse_lists_file failed: ' +
                reverseListsFile, logging.critical)
            raise NameError('ReverseLists.__init__: ' +
                            '__read_reverse_lists_file failed')



    def __lock(self):
        if not os.path.exists(self.lockfile):
            ryw.give_bad_news('ReverseLists__lock: ' +
                              'lock file does not exist: ' +
                              self.lockfile, logging.critical)
            return False

        try:
            self.lock = Flock.Flock(self.lockfile)
            self.lock.type['LOCK_EX'] = self.exclusive
            self.lock.type['LOCK_NB'] = 0
            self.lock.lock()
        except:
            ryw.give_bad_news('ReverseLists__lock: ' +
                              'creating lock and locking failed: '+
                              self.lockfile, logging.critical)
            return False

        return True                



    def __unlock(self):
	try:
            self.lock.unlock()
        except:
            logging.debug('__unlock: exception.')
        #logging.debug('__unlock: unlocked.')
        return True



    def __read_reverse_lists_file(self):
        """lock held if instantiate for write.
        lock released if instantiate for read.
        skipLk is True when dealing with merging
        incoming ReverseLists file"""
        
        assert(self.reverseListsFile != None)

        if not ryw.is_valid_file(self.reverseListsFile,
                                 msg='__read_reverse_lists_file'):
            ryw.give_bad_news('__read_reverse_lists_file: '+
                              'not a valid file: ' + self.reverseListsFile,
                              logging.error)
            return False

        if not self.skipLock:
            if not self._ReverseLists__lock():
                self._ReverseLists__unlock()
                return False

        try:
            self.reverseDict = su.pickload(self.reverseListsFile)
        except:
            ryw.give_bad_news(
                '__read_reverse_lists_file: ' +
                'failed to open reverse lists file: ' +
                self.reverseListsFile, logging.critical)
            self._ReverseLists__unlock()
            return False

        if not self.skipLock:
            if not self.exclusive:
                self._ReverseLists__unlock()

        #logging.debug('ReverseLists.__read_reverse_lists_file: ' +
        #              repr(self.reverseDict))
        return True



    def done(self):
        success = self._ReverseLists__unlock()
        return success



    def printme(self):
        print 'ReverseLists: ' + repr(self.reverseDict)
        


    def __create_lock_file(self):
        return ryw.create_empty_file(self.lockfile,
                                     'ReverseLists.__create_lock_file:')


        
    def add(self, listName, itemsList):
        """called by add_to_reverse_lists() and RebuildReverseLists."""

        changed = self._ReverseLists__add_many_mappings_memory(
            listName, itemsList)
        if changed:
            return self._ReverseLists__write_to_disk()
        return True



    def __add_many_mappings_memory(self, listName, itemsList):
        """called by add() and redefine(). returns changed.
        only touches memory, so the wrapper flushes disk."""

        ryw.db_print('add_many_mappings_memory entered: container: ' +
                     listName + ' , containees: ' + repr(itemsList), 17)
        
        incomeSet = set(itemsList)
        if incomeSet == set([]):
            return False

        changed = False

        for containee in incomeSet:

            success,containeeID,containeeVersion = \
                ryw.split_objstr(containee)
            if not success:
                logging.warning('ReverseLists.add: failed to split: ' +
                                containee)
                if self.reverseDict.has_key(containee):
                    del self.reverseDict[containee]
                    changed = True
                continue

            #
            # this deals with the case when a container (list)
            # contains dead objects (containees).
            # so if we can't find the containees,
            # we not only skip adding, but also want to try
            # to remove the containee from the ReverseLists.
            #
            #success,meta,objroot = ryw_meta.get_meta2(
            #    self.repositoryRoot, containeeID, containeeVersion)

            success,meta = self.searchFile.get_meta(
                containeeID, containeeVersion)
            if not success:
                logging.warning('ReverseLists.add: failed get_meta: '+
                                containee)
                if self.reverseDict.has_key(containee):
                    del self.reverseDict[containee]
                    changed = True
                continue

            #
            # now we add the singleton.
            #
            changed = True
            self._ReverseLists__union_one_mapping(containee, [listName])

        return changed



    def __write_to_disk(self):
        tmppath = self.reverseListsFile + '.TMP'
        try:
            su.pickdump(self.reverseDict, tmppath)
        except:
            ryw.give_bad_news('ReverseLists.add: pickdump failed.',
                              logging.critical)
            return False

        success,bakpath = ryw.make_tmp_file_permanent(
            tmppath, self.reverseListsFile)
        ryw.cleanup_path(tmppath, '_write_to_disk: cleanup, tmppath:')
        ryw.cleanup_path(bakpath, '_write_to_disk: cleanup, bakpath:')
        ryw.db_print('write_to_disk: written to disk...', 11)
        return success



    def lookup(self, containee):
        """returns a list of containers, each of which is a triplet:
        objstr, alias, and title string.
        write lock should be held because we might need to delete
        obsolete containers.
        called by the object display code."""

        #logging.debug('ReverseLists.lookup: containee = ' + containee)
        #logging.debug('ReverseLists.lookup: dict is: ' +
        #             repr(self.reverseDict))
        
        if not self.reverseDict.has_key(containee):
            #logging.debug('ReverseLists.lookup: containee not found.')
            return []
        
        containers = self.reverseDict[containee]
        containerInfo = []
        obsoleteContainers = []

        for container in containers:
            #logging.debug('ReverseLists.lookup: container is ' +
            #              container)
            success,containerID,containerVersion = \
                ryw.split_objstr(container)
            if not success:
                obsoleteContainers.append(container)
                logging.warning('ReverseLists.lookup: failed splitting: '+
                                container)
                continue

            if not self.searchFile:
                ryw.give_bad_news('ReverseLists.lookup: no searchFile.',
                                  logging.critical)
                raise NameError('ReverseLists.lookup: no searchFile.')

            if not is_in_container_file(containerID, containerVersion,
                                        containee, self.searchFile,
                                        self.repositoryRoot):
                obsoleteContainers.append(container)
                logging.info('ReverseLists.lookup: obsolete mapping: ' +
                             containee + ' -> ' + container)
                continue

            #
            # now get the metadata so we can retrieve its
            # alias and title.
            #
            success,meta = self.searchFile.get_meta(containerID,
                                                    containerVersion)
            if success:
                ryw.db_print('ReverseLists.lookup: fast seachFile done!',
                             10)
            else:
                obsoleteContainers.append(container)
                logging.warning('ReverseLists.lookup: failed searchFile ' +
                                'lookup: '+ container)
                continue

            #success,meta,objroot = ryw_meta.get_meta2(
            #    repositoryRoot, containerID, containerVersion)
            #if not success:
            #    obsoleteContainers.append(container)
            #    logging.warning('ReverseLists.lookup: failed get_meta2: '+
            #                    container)
            #    continue

            alias = 'unnamed'
            title = 'unnamed'
            if meta.has_key('content_alias'):
                alias = meta['content_alias']
            if meta.has_key('title'):
                title = meta['title']

            containerInfo.append([container, alias, title])
            ryw.db_print('ReverseLists.lookup: appending good: ' +
                         repr([container, alias, title]), 10)

        if obsoleteContainers:
            self._ReverseLists__remove_obsolete_containers(
                containee, obsoleteContainers)

        #logging.debug('ReverseLists.lookup: ' + repr(containerInfo))
        return containerInfo



    def remove_obsolete_containers(self, containee, obsoleteContainers):
        """called by DeleteFromSel"""

        self._ReverseLists__remove_obsolete_containers(
            containee, obsoleteContainers)
        


    def __remove_obsolete_containers(self, containee, obsoleteContainers):
        """assumes write lock is being held.
        removes a list of containers for a particular containee.
        first does memory, then does disk.
        called by lookup(),
        for sanity checking during reverse pointer display."""

        changed = self._ReverseLists__remove_obsolete_containers_memory(
            containee, obsoleteContainers)

        if changed:
            self._ReverseLists__write_to_disk()
        


    def __remove_obsolete_containers_memory(self, containee,
                                            obsoleteContainers):
        """like the above, but only does memory.
        only removes from the memory.
        called by callee that will flush to disk.
        returns whether there's been change."""

        return self._ReverseLists__minus_one_mapping(
            containee, obsoleteContainers)



    def __delete_containee_object(self, objID, objVersion):
        """returns whether changes are made.
        called when an object is deleted.
        it checks to see whether this guy is a containee.
        this and the one below called by delete_object()."""

        containee = objID + '#' + str(objVersion)
        logging.info('delete_containee_object entered: ' + containee)

        if not self.reverseDict.has_key(containee):
            logging.info('delete_containee_object: not in ReverseLists.')
            return False

        logging.info('delete_containee_object: found to be a containee.')
        ryw.db_print('delete_containee_object: before del: ' +
                     repr(self.reverseDict), 4)
        del self.reverseDict[containee]
        ryw.db_print('delete_containee_object: after del: ' +
                     repr(self.reverseDict), 4)
        return True
        


    def __delete_container_object(self, objID, objVersion,
                                  repositoryRoot, meta):
        """should have held the write lock obviously.
        returns whether changes are made.
        called when an object is deleted.
        it checks to see whether this guy is a container of others,
        and deal with all the containees if any."""

        logging.info('delete_container_object: entered...')

        #
        # already got meta.  this code is not executed.
        #
        if not meta:
            raise NameError('ReverseLists.delete_container_object: ' +
                            'no meta, unexpected.', logging.critical)
            logging.warning('delete_container_object: fetching meta...')

        logging.info('delete_container_object: got meta: ' + repr(meta))

        isList = meta.has_key('sys_attrs') and 'isList' in meta['sys_attrs']
        if not isList:
            return False

        logging.info('delete_container_object: isList ')

        #
        # the caller, DeleteObject.py, already holds a write
        # lock on the SearchFile, so we don't want to lock
        # the SearchFile again, or we deadlock.
        #
        containees = read_container_file(objID, objVersion,
                                         self.searchFile,
                                         self.repositoryRoot)

        logging.info('delete_container_object: got containees: ' +
                     repr(containees))

        container = objID + '#' + str(objVersion)

        logging.info('delete_container_object: container is: '+container)

        changed = self._ReverseLists__minus_many_mappings(
            containees, container)
        
        return changed



    def delete_object(self, objID, objVersion, repositoryRoot, meta):
        """called when an object is deleted.
        deal with the case that this object is either a container
        or a containee of other objects.
        assumes write lock held."""

        changed = False

        if self._ReverseLists__delete_containee_object(objID, objVersion):
            changed = True
        
        if self._ReverseLists__delete_container_object(objID, objVersion,
                                                       repositoryRoot,
                                                       meta):
            changed = True
        
        if changed:
            self._ReverseLists__write_to_disk()



    def __union_one_mapping(self, containee, containers):
        """helper function called at more than one place.
        containers is a list."""

        if not containers or containers == []:
            return
        
        if self.reverseDict.has_key(containee):
            oldSet = self.reverseDict[containee]
            newSet = oldSet | set(containers)
            self.reverseDict[containee] = newSet
            ryw.db_print('union_one_mapping: the new set is: ' +
                         repr(newSet), 11)
        else:
            self.reverseDict[containee] = set(containers)



    def merge(self, incoming, repositoryRoot):
        """called by ProcessDiscs.py. to merge an incoming ReverseLists."""

        changed = False
        
        for containee,containers in incoming.reverseDict.iteritems():
            ryw.db_print('ReverseLists.merge: examine ' + containee +
                         ' -> ' + repr(containers), 11)

            if not is_valid_local_object(containee, repositoryRoot,
                                         self.searchFile):
                ryw.db_print('ReverseLists.merge: this containee skipped: '+
                             containee, 11)
                continue

            ryw.db_print('ReverseLists.merge: good containee: ' +
                         containee, 11)

            goodContainers = []
            for container in containers:
                if not is_valid_local_object(container, repositoryRoot,
                                             self.searchFile):
                    ryw.db_print('ReverseLists.merge: container skipped: ' +
                                 container, 11)
                    continue
                ryw.db_print('ReverseLists.merge: good container: ' +
                             container, 11)
                goodContainers.append(container)

            if goodContainers:
                ryw.db_print('ReverseLists.merge: adding one mapping: ' +
                             containee + ' -> ' + repr(goodContainers), 11)
                self._ReverseLists__union_one_mapping(containee,
                                                      goodContainers)
                changed = True

        if changed:
            return self._ReverseLists__write_to_disk()

        

    def __minus_one_mapping(self, containee, containers):
        """helper function called at more than one place.
        containers is a list.
        returns whether changes have been made."""

        if not containers or containers == []:
            ryw.db_print('minus_one_mapping: empty containers.', 14)
            return False
        
        if not self.reverseDict.has_key(containee):
            ryw.db_print('minus_one_mapping: containee not found.', 14)
            return False

        minusSet = set(containers)
        oldSet = self.reverseDict[containee]
        newSet =  oldSet - minusSet

        changed = False
        
        if newSet == set([]):
            del self.reverseDict[containee]
            changed = True
            ryw.db_print('minus_one_mapping: no container left.', 14)
        elif oldSet != newSet:
            self.reverseDict[containee] = newSet
            changed = True
            ryw.db_print('minus_one_mapping: new set is: '+repr(newSet), 14)

        return changed



    def __minus_many_mappings(self, containees, container):

        ryw.db_print('minus_many_mappings: before deletion: ' +
                     repr(self.reverseDict), 17)

        if not containees or containees == []:
            return False

        changed = False
        for containee in containees:
            logging.info('minus_many_mappings: deal with containee: '+
                         containee)
            if self._ReverseLists__remove_obsolete_containers_memory(
                containee, [container]):
                changed = True
                logging.info('minus_many_mappings: changed made.')

        ryw.db_print('minus_many_mappings: after deletion: ' +
                     repr(self.reverseDict), 17)
        
        return changed



    def redefine_container(self, container, oldContainees, newContainees,):
        """called when a list is being redefined to be the current
        selection."""

        logging.info('redefine_container entered: container = ' + container +
                     ' , old contanees = ' + repr(oldContainees) +
                     ', new containees = ' + repr(newContainees))
        
        changed1 = self._ReverseLists__minus_many_mappings(
            oldContainees, container)

        changed2 = self._ReverseLists__add_many_mappings_memory(
            container, newContainees)

        if changed1 or changed2:
            return self._ReverseLists__write_to_disk()

        return True
        
