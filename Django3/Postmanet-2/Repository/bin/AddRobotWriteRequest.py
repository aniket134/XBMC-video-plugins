sys.path.append(os.path.join(RepositoryRoot, 'bin'))
import sys, os
import su
import random, pickle, shutil, objectstore, datetime, time
import logging, ryw, ryw_upload, SearchFile, ryw_copytree, ryw_view, urllib
import ryw_philips
import ReverseLists



def get_resources(tmpDirOption = ''):
    logging.debug('get_resources: entered...')
    try:
        resources = su.parseKeyValueFile(os.path.join(RepositoryRoot,
                                                      'Resources.txt'))
        robotJobsDir = resources['robotsjobdir']

        if tmpDirOption:
            tmpOutDir = tmpDirOption
        else:
            tmpOutDir = resources['tmpout']
        ryw.give_news2('<BR>outgoing data placed in: ' + tmpOutDir,
                       logging.info)
        
        searchFile = resources['searchfile']
        viewRoot = resources['viewroot']
        objectstoreroots = resources['objectstore'].split(';')
        firstRoot = objectstoreroots[0]
        robotPresent = ryw.has_robot(resources)
    except:
        ryw.give_bad_news('get_resources failed.', logging.critical)
        return (False, None, None, None, None, None, None, None)
    
    logging.debug('get_resources succeeded.')
    logging.debug('get_resources: robotJobsDir, tmpOutDir, searchFile, viewRoot' + robotJobsDir + tmpOutDir + searchFile + viewRoot + firstRoot)
    return (True, resources, robotJobsDir, tmpOutDir, searchFile, viewRoot,
            firstRoot, robotPresent)
        


def getAddress(name):
    try:
        eps = su.pickload(os.path.join(RepositoryRoot, 'Endpoints.pk'))
        ep = eps[name]
    except:
        ryw.give_bad_news('getAddress: failed, name: ' + name,
                          logging.warning)
        return None
    return ep



def cleanup_image(tmpImgDir):
    ryw.cleanup_path(tmpImgDir,  'cleanup_image:')



def write_recipient_file(tmpImgDir, name):
    # make a temporary recipient file

    ryw.give_news2('<BR>', logging.info)
    ryw.give_news2('writing recipient file... &nbsp;&nbsp;', logging.info)
    
    rcptFileName = os.path.join(tmpImgDir, 'Recipient.txt')
    try:
        f = open(rcptFileName, 'w')
        f.write('Recipient Info---\n\n')
        f.write('Username: ' + name + '\n')

        ep = getAddress(name)
        if ep:
            f.write('Address: ' + ep + '\n')
            
        f.flush()
        os.fsync(f.fileno())
        f.close()
    except:
        ryw.give_bad_news('write_recipient_file failed, tmpImgDir, name: '+
                          tmpImgDir + ' ' + name, logging.critical)
        return False

    logging.debug('write_recipient_file done, tmpImgDir, name: '+
                  tmpImgDir + ' ' + name)
    ryw.give_news2('done, ' + name, logging.info)
    ryw.give_news2('<BR>', logging.info)
    return True



def write_user_credentials(repDir, name):
    ryw.give_news2('writing user credential... &nbsp;&nbsp;', logging.info)
    try:
        open(os.path.join(repDir, 'usercredentials'), 'w').write(name)
    except:
        ryw.give_bad_news('write_user_credentials failed: ' + repDir + ' ' +
                          name, logging.critical)
        return False
    logging.debug('write_user_credentials done: ' + repDir + ' ' + name)
    ryw.give_news2('done, ' + name, logging.info)
    ryw.give_news2('<BR>', logging.info)
    return True



def copy_script_dir(repDir, srcDirName, dstDirName):
    logging.debug('copy_script_dir: ' + srcDirName + ' -> ' + dstDirName)

    dstDirPath = os.path.join(repDir, dstDirName)
    if not ryw.try_mkdir(dstDirPath, 'copy_script_dir:'):
        return False

    srcDirPath = os.path.join(RepositoryRoot, srcDirName)
    try:
        scripts = os.listdir(srcDirPath)
    except:
        ryw.give_bad_news('copy_script_dir: os.listdir failed.',
                          logging.critical)
        return False

    for s in scripts:
        if s != 'update.py' and s != 'CVS' and s != 'cvs':
            logging.debug('copy_script_dir: copying... ' + s)
            src = os.path.join(srcDirPath, s)
            dst = os.path.join(dstDirPath, s)

            try:
                if os.path.isdir(src):
                    sDir = os.path.join(srcDirName, s)
                    dDir = os.path.join(dstDirName, s)
                    if not copy_script_dir(repDir, sDir, dDir):
                        ryw.give_bad_news( \
                            'copy_script_dir: recursion failed: ' + \
                            repDir + '   ' + sDir + ' -> ' + dDir, \
                            logging.error)
                        return False
                else:
                    shutil.copyfile(src, dst)
            except:
                ryw.give_bad_news('copy_script_dir: failed to copy ' + s,
                                  logging.critical)
                return False

    logging.debug('copy_script_dir: done.')
    return True
            


# noObjStore:
# just place a copy of the code.
def copy_scripts(repDir):
    ryw.give_news2('copying scripts... &nbsp;&nbsp;', logging.info)
    
    # place a whole copy of code anyhow
    try:
        su.copytree(os.path.join(RepositoryRoot, '..', 'Postmanet-2'),
                    os.path.join(repDir, '..', 'Postmanet-2'),
                    isInstall = True)
        ryw.give_news2('Postmanet-2: done. ', logging.info)
    except:
        ryw.give_bad_news('copy_scripts: failed to place Postmanet-2.',
                          logging.error)
        return False

    logging.debug('copy_scripts: done.')
    ryw.give_news2('<BR>', logging.info)
    return True



# noObjStore:
# not used
def copy_scripts_not_used(repDir):
    ryw.give_news2('copying scripts... &nbsp;&nbsp;', logging.info)
    # place update.py
    src = os.path.join(RepositoryRoot, 'pythonscriptsforclient',
                       'update.py')
    dst = os.path.join(repDir, 'update.py')
    try:
        shutil.copyfile(src, dst)
    except:
        ryw.give_bad_news('copy_scripts: failed to copy update.py: ' + src +
                          ' ' + dst, logging.critical)
        return False
    logging.debug('copy_scripts done: ' + repDir)
    
    # place pythonsripts
    if copy_script_dir(repDir, 'pythonscriptsforclient', 'pythonscripts'):
        ryw.give_news2('pythonscriptsforclient: done. ', logging.info)
    else:
        ryw.give_bad_news('copy_scripts: copy_script_dir failed.',
                          logging.critical)
        return False

    # place Common scripts
    if copy_script_dir(repDir, 'CommonScripts4Clients',
                       'CommonScripts4Clients'):
        ryw.give_news2('Common: done. ', logging.info)
    else:
        ryw.give_bad_news('copy_scripts: copy_script_dir failed.',
                          logging.critical)
        return False

    # place Nihao scripts
    if copy_script_dir(repDir, 'NihaoScripts4Clients', 'NihaoScripts4Clients'):
        ryw.give_news2('NihaoScripts4Clients: done. ', logging.info)
    else:
        ryw.give_bad_news('copy_scripts: copy_script_dir failed.',
                          logging.critical)
        return False

    # place a whole copy of code anyhow
    try:
        su.copytree(os.path.join(RepositoryRoot, '..', 'Postmanet-2'),
                    os.path.join(repDir, '..', 'Postmanet-2'),
                    isInstall = True)
        ryw.give_news2('Postmanet-2: done. ', logging.info)
    except:
        ryw.give_bad_news('copy_scripts: failed to place Postmanet-2.',
                          logging.error)
        return False

    logging.debug('copy_scripts: done.')
    ryw.give_news2('<BR>', logging.info)
    return True



def copy_search_file(searchFile, repDir):
    ryw.give_news2('copying search file... &nbsp;&nbsp;', logging.info)
    # place catalog
    # TODO: lock searchfile -> now done
    logging.debug('copy_search_file: ' + searchFile + ' ' + repDir)
    dst = os.path.join(repDir, 'searchfile')

    success,binSearchFile = ryw.open_search_file(
        'copy_search_file:',
        None,
        None,
        searchFile,
        False,
        skipRead = True)
    if not success:
        return False
    
    try:
        shutil.copyfile(searchFile, dst)
        binSearchFile.done()
    except:
        ryw.give_bad_news('copy_search_file failed: ' +
                          searchFile + ' ' + dst, logging.critical)
        return False
    logging.debug('copy_search_file: ' + searchFile + ' ' + dst)
    ryw.give_news2('done. ', logging.info)
    ryw.give_news2('<BR>', logging.info)
    return True    



def copy_reverse_lists(repDir):
    ryw.give_news2('copying reverse lists... &nbsp;&nbsp;', logging.info)
    logging.debug('copy_reverse_lists: ' + repDir)

    reverseListsFile = os.path.join(RepositoryRoot, 'ReverseLists')
    if not ryw.is_valid_file(reverseListsFile, 'copy_reverse_lists:'):
        ryw.give_news2('not found: ' + reverseListsFile + '<BR>',
                       logging.info)
        return True

    success,reverseLists = ReverseLists.open_reverse_lists(
        'AddRobotWriteRequests.copy_reverse_lists:',
        '', '', reverseListsFile, False,
        allowNullSearchFile = True)
    if not success:
        return False

    dst = os.path.join(repDir, 'ReverseLists')
    
    try:
        shutil.copyfile(reverseListsFile, dst)
    except:
        ryw.give_bad_news('copy_reverse_lists failed: ' +
                          reverseListsFile + ' ' + dst, logging.critical)
        if reverseLists:
            reverseLists.done()
        return False

    if reverseLists:
        reverseLists.done()
    
    logging.debug('copy_reverse_lists: ' + reverseListsFile + ' ' + dst)
    ryw.give_news2('done.<BR>', logging.info)
    return True    



# noObjStore:
# not called any more, but remains intact.
def copy_objectstore(firstRoot, repDir, tmpStoreName):
    """copies the objectstore minus the big data items.
    only copying the first root.  I assume this is ok.  the multiple
    roots will just get merged over time at one root on the village side."""
    
    dst = os.path.join(repDir, 'ObjectStore')

    if os.path.exists(tmpStoreName):
        ryw.give_news2('moving a pre-copied object store... &nbsp;&nbsp;',
                       logging.info)
        logging.debug('copy_objectstore: moving a pre-copied store: ' +
                      tmpStoreName)
        try:
            shutil.move(tmpStoreName, dst)
            ryw.cleanup_partial_dir(
                ryw.parent_dir(tmpStoreName), 'copy_objectstore:', True)
        except:
            ryw.give_bad_news('copy_objectstore: failed to move store: ' +
                              tmpStoreName, logging.critical)
            return False
        ryw.give_news2('done. ', logging.info)
        ryw.give_news2('<BR>', logging.info)
        return True

    ryw.give_news2('copying object store... &nbsp;&nbsp;', logging.info)
    logging.debug('copy_objectstore: ' + firstRoot + ' -> ' + repDir)
    try:
        success = ryw_copytree.copy_tree_diff_repo(firstRoot, dst)
        if not success:
            raise 'copy_tree_diff_repo failed.'
    except:
        ryw.give_bad_news('copy_objectstore: copy_tree_diff_repo failed: '+
                          firstRoot + ' -> ' + dst, logging.critical)
        return False

    logging.debug('copy_objectstore: done: ' + dst)
    ryw.give_news2('done. ', logging.info)
    ryw.give_news2('<BR>', logging.info)
    return True



# noObjStore:
def copy_view(repDir, viewRoot):
    ryw.give_news2('copying view... &nbsp;&nbsp;', logging.info)
    try:
        dst = os.path.join(repDir, 'View')
        su.copytree(viewRoot, dst)
    except:
        ryw.give_bad_news('copy_view: failed: ' + viewRoot + ' ' + dst,
                          logging.critical)
        return False
    
    logging.debug('copy_view: done: '+dst)
    ryw.give_news2('done. ', logging.info)
    ryw.give_news2('<BR>', logging.info)
    return True



def check_free_disk_space(dataSize, tmpOutDir):
    logging.debug('check_free_disk_space: entered, data, dir: '
                  + repr(dataSize) + tmpOutDir)
    freeKB = ryw.free_MB(tmpOutDir) * 1024
    logging.debug('check_free_disk_space: entered, freeKB: ' + repr(freeKB))
    if ryw_upload.pretty_much_out_of_space(dataSize, freeKB):
        ryw.give_bad_news(
            'addRobotWriteRequest,check_free_disk_space:' +
            'nearly out of disk space: size, free: ' +
            repr(dataSize) + ' ' + repr(freeKB), logging.error)
        return False
    logging.debug('check_free_disk_space: dataSize, freeKB: '
                  + repr(dataSize) + ' ' + repr(freeKB))
    return True



def temp_list_key(x):
    meta = x[0]
    return ryw.datetimesortkey(meta)



def write_page(items, itempath, f, tmpImgDir):

    mapDict = ryw_philips.get_map(tmpImgDir)
    if mapDict == None:
        # raise('write_page: failed to get map.')
        pass
    
    f.write(ryw_view.begin_print_str())
    f.write(ryw_view.begin_print_str2())

    tempList = []
    for item in items:
        make_DVDobject_list(item, itempath, tempList)

    if len(tempList) != 0 and mapDict == None:
        raise('write_page: unexpected empty map dict.')

    tempList.sort(key = temp_list_key, reverse = True)

    for listItem in tempList:
        meta,item,thisItemPath = listItem
        str = show_DVDobject_compact(meta, item, thisItemPath, mapDict)
        f.write(str.replace('SRC="/icons','SRC="./icons'))

    f.write(ryw_view.end_print_str())



def generate_html(items,itempath, repDir, tmpImgDir):
        ryw.give_news2('generating static html pages... &nbsp;&nbsp;',
                       logging.info)
	htmlDir = os.path.join(repDir, "html")
	if not ryw.try_mkdir(htmlDir, 'addRobotWriteRequest:generate_html'):
		return False
	try:
		f = open(os.path.join(htmlDir,"index.html"),"w")
		f.write("""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html>

<head>
	<title>Objects on this disk</title>
""")
                f.write(ryw_view.css_str())
                f.write("""
</head>

<body>
""")
		f.write(ryw_view.logo_str_for_disc())
		f.write("""
<h3>Objects on Disk</h3><p>(you are on this page either because you are browsing 
the disc directly or were directed to it due to an error while merging it.)
<BR>
""")
		write_page(items,itempath,f, tmpImgDir)
                f.write(ryw_view.end_print_str())
		f.write(ryw_view.footer2_str())
		f.write("""
</body>
</html>
""")
		f.close()
		srcIconsDir = os.path.join(RepositoryRoot, "WWW", "icons")
		dstIconsDir = os.path.join(htmlDir, "icons")
		su.copytree(srcIconsDir, dstIconsDir)
		parentDir, repdirname = os.path.split(repDir)
		f = open(os.path.join(parentDir,"index.html"), "w")
		f.write("""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html>
<head>
<title> Repository folders on this disk </title>
<meta http-equiv="refresh" content="1;URL=.\%s\html\index.html">
</head>
<body>
loading page containing list of things on this disk....
</body>
</html>
""" % (repdirname,))
		f.close()
	except:
		ryw.give_bad_news('addRobotWriteRequest: generate_html files: failed to write file: ',logging.critical)
		return False

        ryw.give_news2('done. ', logging.info)
        ryw.give_news2('<BR>', logging.info)
	return True


	
def copy_objects(items, itempath, repDir, tmpImgDir, metaOnly = False):
    ryw.give_news2('copying requested objects... &nbsp;&nbsp;', logging.info)
    #
    # quite a bit of the copying details should be pulled out to a piece
    # of common code.
    #

    if len(items) == 0:
        ryw.give_news2('no requested objects. ', logging.info)
        ryw.give_news2('<BR>', logging.info)
        return True    

    success,dataRoot,auxiRoot,mapDict,counter = ryw_philips.out_init(tmpImgDir)
    if not success:
        ryw.give_bad_news('copy_objects: out_init failed.', logging.error)
        return True

    for item in items:
        logging.debug('copy_objects: item: ' + item)
        try:
            objname,version = item.split('#')
            version = int(version)
            logging.debug('copy_objects: got name, version: ' +
                          objname + ' ' + repr(version))
            #destpath = objectstore.nameversiontopaths(
            #    os.path.join(repDir, 'objects'), objname, version)
            destpath = objectstore.name_version_to_paths_aux(
                os.path.join(repDir, 'objects'), objname, version)
            logging.debug('copy_objects: got destpath: ' + repr(destpath))

            if not ryw.good_repo_paths(itempath[item]):
                ryw.give_bad_news('copy_objects: good_repo_paths failed.',
                                  logging.error)
                raise('something missing in the source paths.')

            su.createparentdirpath(destpath[0])
            logging.debug('copy_objects: created parent dir: ' + destpath[0])

            # code prior to preparing for Philips DVD player
            # su.copytree(itempath[item][0], destpath[0])
            # logging.debug('copy_objects: done copying data: ' + destpath[0])

            counter,mapDict = \
                ryw_philips.out_copy(item,
                                     itempath[item][0], itempath[item][1],
                                     itempath[item][2], counter,
                                     dataRoot, auxiRoot, mapDict,
                                     onlyMeta = metaOnly)

            shutil.copyfile(itempath[item][1], destpath[1])
            logging.debug('copy_objects: done copying metadata: ' +
                          destpath[1])

            # code prior to preparing for Philips DVD player
            # if os.path.exists(itempath[item][2]):
            #     su.copytree(itempath[item][2], destpath[2])
            #     logging.debug('copy_objects: done copying auxi files: ' +
            #                   destpath[2])
                
            shutil.copyfile(itempath[item][3], destpath[3])
            logging.debug('copy_objects: done copying done flag: ' +
                          destpath[3])
            
        except:
            ryw.give_bad_news(
                'copy_objects: failed to copy data: ' + item, logging.critical)
            ryw.give_bad_news(
                'copy_objects: skip copying an object and continue.',
                logging.error)
            continue

    ryw_philips.out_done(tmpImgDir, mapDict)

    ryw.give_news2('done. ', logging.info)
    ryw.give_news2('<BR>', logging.info)
    return True    



#RYWview
#not used any more
def get_DVD_URLs(item, itempaths, mapDict):
    try:
        objID,version = item.split('#')
        version = int(version)

        dvdObjRoot = '..\\objects'
        paths = objectstore.name_version_to_paths_aux(
            dvdObjRoot, objID, version)
        datapath = os.path.normpath(paths[0])
        datapath = datapath.replace('\\', '/')
        auxipath = os.path.normpath(paths[2])
        auxipath = auxipath.replace('\\', '/')
        datapath = urllib.quote(datapath)
        auxipath = urllib.quote(auxipath)
        #auxidir  = os.path.normpath(paths[2])
        auxidir  = os.path.normpath(itempaths[2])
        logging.debug('get_DVD_URLs: ' + datapath + ' ' + auxipath + ' ' +
                      auxidir)
        return (True, datapath, auxipath, auxidir)
    except:
        ryw.give_bad_news('get_DVD_URLs: failed for: ' + item,
                          logging.critical)
        return (False, None, None, None)



def get_DVD_URLs2(item, itempaths, mapDict):
    try:

        dirName = mapDict[item]
        datapath = os.path.join('..\\..\\', ryw_philips.dataDirName, dirName)
        datapath = os.path.normpath(datapath)
        datapath = datapath.replace('\\', '/')
        auxipath = os.path.join('..\\..\\', ryw_philips.auxiDirName, dirName)
        auxipath = os.path.normpath(auxipath)
        auxipath = auxipath.replace('\\', '/')
        datapath = urllib.quote(datapath)
        auxipath = urllib.quote(auxipath)
        auxidir  = os.path.normpath(itempaths[2])
        logging.debug('get_DVD_URLs2: ' + datapath + ' ' + auxipath + ' ' +
                      auxidir)
        return (True, datapath, auxipath, auxidir)
    except:
        ryw.give_bad_news('get_DVD_URLs2: failed for: ' + item,
                          logging.critical)
        return (False, None, None, None)



#RYWview
def show_DVDobject_compact(meta, item, thisItemPath, mapDict):

    success,dataURL,auxiURL,auxiDir = get_DVD_URLs2(item, thisItemPath,
                                                    mapDict)
    if not success:
        return ''
    
    return ryw_view.show_object_compact_string(meta, dataURL,
                                               auxiURL, auxiDir,
                                               staticHtml = True)
    


#RYWview
def make_DVDobject_list(item, itempath, listSoFar):

    try:
        meta = su.pickload(itempath[item][1])
    except:
        ryw.give_bad_news('make_DVDobject_list: failed to load metadata: '+
                          itempath[item][1], logging.critical)
        return

    listSoFar.append((meta, item, itempath[item]))
    

def write_copytodvd_job_file(filename,root):
    try:
        f = open(datafl,"w")
        for i in os.listdir(root):
            f.write(os.path.join(root,i)+"\n")
        f.close()
    except:
        ryw.give_bad_news("write_copytodvd_job_file: failed to write file list for dvd burner",logging.error)
        return (False,filename)
    return (True,filename)

def write_robot_job_file(robotJobsDir, tmpImgDir, objPrefix, robotPresent = True):
    jrqFileName = os.path.join(robotJobsDir, objPrefix)

    if not robotPresent:
        return write_copytodvd_job_file(jrqFileName,tmpImgDir)
    try:
        f = open(jrqFileName, 'w')
        logging.debug('write_robot_job_file: opened jrq file: ' + jrqFileName)
        f.write('ClientID=localhost\n')
        f.write('JobID=Job-' + objPrefix + '\n')
        f.write('Copies=1\n')
        f.write('CloseDisc=YES\n')
        f.write('VerifyDisc=YES\n')
        f.write('RejectIfNotBlank=YES\n')
        logging.debug('write_robot_job_file: wrote initial content.')

        tmpdirname = tmpImgDir
        if tmpdirname[-1] == os.sep:
            tmpdirname = tmpdirname[:-1]
        f.write('Data=' + tmpdirname + '\n')
        logging.debug('write_robot_job_file: wrote tmp dir.')

        f.close()
        logging.debug('write_robot_job_file: closed.')
    
        jrq = jrqFileName + '.JRQ'
        os.rename(jrqFileName, jrq)
        logging.debug('write_robot_job_file: finished rename.')
    except:
        ryw.give_bad_news(
            'write_robot_job_file: failed to create robot job file: ' +
            robotJobsDir + ' ' + tmpImgDir + ' ' + objPrefix,
            logging.critical)
        return (False, None)
    return (True, jrqFileName)



def copy_autorunfiles(rootDir):
    ryw.give_news2('copying auto run files... &nbsp;&nbsp;', logging.info)
    autoinf = os.path.join(RepositoryRoot,"bin","autorun.inf")
    autopy = os.path.join(RepositoryRoot,"bin","autorun.py")
    try:
        shutil.copy(autoinf,rootDir)
        shutil.copy(autopy,rootDir)
    except:
        ryw.give_bad_news("addRobotWriteRequest: copy_autorunfiles failed: ", logging.critical)
        return False
    ryw.give_news2('done. ', logging.info)
    ryw.give_news2('<BR>', logging.info)
    return True



def addRobotWriteRequest(name, items, itempath, currentSize, tmpStoreName,
                         tmpDirOption = '', onlyMeta = False):
    logging.debug('addRobotWriteRequest: entered...')

    success,resources,robotJobsDir,tmpOutDir,searchFile,viewRoot,firstRoot, \
        robotPresent = get_resources(tmpDirOption = tmpDirOption)
    if not success:
        return (False, None, None)

    if not onlyMeta and not check_free_disk_space(currentSize, tmpOutDir):
        return (False, None, None)
            
    tmpImgDir,objPrefix = ryw_upload.attempt_just_make_tmpdir(
        tmpOutDir, 'Im_'+name[:3]+'_', '')
    if not tmpImgDir:
        return (False, None, None)

    ryw.give_news2('<BR>outgoing data image name: ' + tmpImgDir, logging.info)

    if not write_recipient_file(tmpImgDir, name):
        cleanup_image(tmpImgDir)
        return (False, None, None)

    repDir = os.path.join(tmpImgDir, 'repository')
    if not ryw.try_mkdir(repDir, 'addRobotWriteRequest'):
        cleanup_image(tmpImgDir)
        return (False, None, None)

    # noObjStore:
    #   not copy_objectstore(firstRoot, repDir, tmpStoreName) or \
    #   not copy_view(repDir, viewRoot) or \
    if not write_user_credentials(repDir, name) or \
       not copy_scripts(repDir) or \
       not copy_search_file(searchFile, repDir) or \
       not copy_reverse_lists(repDir) or \
       not copy_objects(items, itempath, repDir,
                        tmpImgDir, metaOnly = onlyMeta) or \
       not generate_html(items, itempath, repDir, tmpImgDir) or \
       not copy_autorunfiles(tmpImgDir):
        cleanup_image(tmpImgDir)
        return (False, None, None)

    ryw.give_news(' ', logging.info)
    ryw.give_news('done copying all data, now invoking the robot.',
                  logging.info)
    
#    success,jrq = write_robot_job_file(robotJobsDir, tmpImgDir, objPrefix, robotPresent = robotPresent)
#    if not success:
#        cleanup_image(tmpImgDir)
#        ryw.cleanup_path(jrq, 'addRobotWriteRequest:')
#        return (False, None, None)

    return (True, tmpImgDir, "blah")



def wait_for_robot(finishedStuff):
    #
    # monitor robot job status for all the discs to finish.
    #
    totalToWaitFor = len(finishedStuff)
    reallyFinished = 0
    reallyFinishedList = []
    ryw.give_news2('waiting for robot...', logging.info)
    ryw.give_news2('<BR>', logging.info)
    while True:
        for job in finishedStuff:
            tmpImgDir,jrq = job
            done = ryw_upload.check_robot_finished(jrq)
            if done and (not job in reallyFinishedList):
                reallyFinished += 1
                reallyFinishedList.append(job)
                ryw.give_news('robot finished: ' + str(reallyFinished) +
                              ' out of ' + str(totalToWaitFor) + ' disc(s).',
                              logging.info)
                ryw.give_news('  tmp files: ' + tmpImgDir + ' ' + jrq,
                              logging.info)
                ryw.give_news(' ', logging.info)
        if reallyFinished >= totalToWaitFor:
            break
        ryw.give_news2('*', logging.info)
        time.sleep(5)

    #
    # wait 60 seconds before removing temp data.
    #
    delay = 60
    ryw.give_news(' ', logging.info)
    ryw.give_news('will delete all temporary data in ' + str(delay) +
                  ' seconds.  press esc to stop it...', logging.info)
    ryw.give_news(' ', logging.info)
    while delay > 0:
        ryw.give_news2(str(delay) + '...', logging.info)
        time.sleep(5)
        delay -= 5
    ryw.give_news(' ', logging.info)
    ryw.give_news('deleting all temporary data...', logging.info)
        
    #
    # remove all temporary data...
    #
    for job in reallyFinishedList:
        tmpImgDir,jrq = job
        ryw_upload.cleanup_incoming(tmpImgDir, jrq)
    ryw.give_news('all temporary data removed.', logging.info)
