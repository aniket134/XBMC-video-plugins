import sys, os
import su
import random, pickle, shutil, objectstore, datetime, time
import logging, ryw, ryw_upload, SearchFile, ryw_copytree, ryw_view, urllib
import string, re



dataDirName = '0data'
auxiDirName = '1more'
stubDirName = '__META_ONLY_STUB_0824__'


def stripStr(s):
    t = s
    for x in s:
        if (not x in string.letters) and (not x in string.digits) and \
            x != '_' and x != '-':
            t = t.replace(x, '')
    return t



def out_obj_dir_name(objStoreRoot, objname, version, currCounter):

    if currCounter >= 9999:
        ryw.give_bad_news('out_obj_dir_name: counter exceeded 9999.',
                          logging.warning)
        #return (False, None, currCounter)
    
    success,meta = ryw.get_meta(objStoreRoot, objname, version)
    if not success:
        ryw.give_bad_news('out_obj_dir_name: failed to get meta data: ' +
                          objname + '#' + str(version), logging.error)
        return (False, None, currCounter)

    if meta.has_key('content_alias'):
        author = meta['content_alias']
        author = stripStr(author)
    elif meta.has_key('author_name'):
        author = meta['author_name']
        author = stripStr(author)
        author = re.sub('(^[mM]s)|(^[mM]r)|(^[mM]rs)|(^[mM]iss)', '', author)
    else:
        author = 'unknown'

    prefix = str(currCounter).zfill(2)
    dirName = prefix + author
    dirName = dirName[:32]
    logging.debug('out_obj_dir_name: dirName is: ' + dirName)
        
    return (True, dirName, currCounter + 1)



def out_init(tmpImgDir):
    dataRoot = os.path.join(tmpImgDir, dataDirName)
    auxiRoot = os.path.join(tmpImgDir, auxiDirName)
    
    if not ryw.try_mkdir(dataRoot, 'out_init: '):
        return (False, None, None, None, 0)

    if not ryw.try_mkdir(auxiRoot, 'out_init: '):
        return (False, None, None, None, 0)

    logging.debug('out_init: created data and auxi roots: ' + dataRoot +
                  '   ' + auxiRoot)
    mapDict = {}
    counter = 0
    return (True, dataRoot, auxiRoot, mapDict, counter)
    


# raises exception if fails.
def out_copy(itemName, srcDataPath, srcMetaPath, srcAuxiPath, currCounter,
             dataRoot, auxiRoot, mapDict, onlyMeta = False):
    objID,version = itemName.split('#')
    version = int(version)
    success,dirName,currCounter = out_obj_dir_name(
        os.path.join(RepositoryRoot, 'WWW', 'ObjectStore'),
        objID, version, currCounter)
        
    if not success:
        raise 'out_copy: out_obj_dir_name failed.'

    dataDir = os.path.join(dataRoot, dirName)
    auxiDir = os.path.join(auxiRoot, dirName)

    ryw.give_news2(dirName + ', ', logging.info)

    if onlyMeta:
        try:
            os.makedirs(os.path.join(dataDir, stubDirName))
        except:
            msg = 'out_copy: failed to make meta only stub: '+ \
                  dataDir
            ryw.give_bad_news(msg, logging.critical)
            raise msg
    else:
        su.copytree(srcDataPath, dataDir)
        
    logging.debug('out_copy: successfully copied: ' +
                  srcDataPath + ' -> ' + dataDir)

    if os.path.exists(srcAuxiPath):
        su.copytree(srcAuxiPath, auxiDir)
        logging.debug('out_copy: successfully copied: ' +
                      srcAuxiPath + ' -> ' + auxiDir)

    mapDict[itemName] = dirName
    logging.debug('out_copy: entered mapping: ' + itemName + ' : ' + dirName)
    return (currCounter, mapDict)



def out_done(tmpImgDir, mapDict):
    path = os.path.join(tmpImgDir, 'data_map')
    try:
        su.pickdump(mapDict, path)
    except:
        ryw.give_bad_news('out_done: pickdump failed: ' + path, logging.error)
        return False

    logging.debug('out_done: done writing map file: ' + path)
    return True



def get_map(tmpImgDir):
    path = os.path.join(tmpImgDir, 'data_map')
    try:
        mapDict = su.pickload(path)
    except:
        return None

    logging.debug('get_map: done reading map file: ' + path)
    return mapDict



def get_map_entry(driveroot, mapDict, itemName):
    if not mapDict.has_key(itemName):
        ryw.give_bad_news(
            "get_map_entry: can't locate object name in map file: " +
            itemName, logging.error)
        return (False, None, None, None)

    dirName = mapDict[itemName]

    logging.debug('get_map_entry: found map entry: ' + itemName +
                  ' -> ' + dirName)

    dataDir = os.path.join(driveroot, dataDirName, dirName)
    auxiDir = os.path.join(driveroot, auxiDirName, dirName)

    if not os.path.exists(dataDir):
        ryw.give_bad_news("get_map_entry: can't find data directory: " +
                          itemName + ': ' + dataDir, logging.error)
        return (False, None, None, None)

    return (True, dirName, dataDir, auxiDir)



def in_copy(objname, version, dstDataPath, dstAuxiPath, driveroot, mapDict):
    itemName = objname + '#' + version
    
    success,dirName,dataDir,auxiDir = get_map_entry(driveroot, mapDict,
                                                    itemName)
    if not success:
        return False

    ryw.give_news3('  copying ' + dirName + ' ... ', logging.info)

    try:
        su.copytree(dataDir, dstDataPath)
    except:
        ryw.give_bad_news('in_copy: failed to copy data directory: ' +
                          itemName + ': ' + dataDir, logging.error)
        return False

    logging.debug('in_copy: successfully copied data directory: ' +
                  itemName + ': ' + dataDir)
    
    if os.path.exists(auxiDir):
        try:
            su.copytree(auxiDir, dstAuxiPath)
        except:
            ryw.give_bad_news('in_copy: failed to copy auxi directory: ' +
                              itemName + ': ' + auxiDir, logging.error)
            return False
        logging.debug('in_copy: successfully copied auxi directory: ' +
                      itemName + ': ' + auxiDir)

    return True
