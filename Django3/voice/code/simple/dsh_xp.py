#
# copied from Postmanet-2.
#

import sys
import _winreg
import dsh_utils
import shutil, os, subprocess, logging



try:
    import win32api
    import win32file
    import pywintypes
    import win32con
    import win32security
except:
    dsh_utils.give_bad_news(
        'fatal_error: failed to import win32 libraries.' +
        '  install win32 extensions.', logging.critical)
    sys.exit(1)



def get_apache_path():
    """called by install-repository-lai.py"""

    dsh_utils.db_print3('ryw_xp:get_apache_path() entered...', 50)
    
    try:
        a = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE')
        a = _winreg.OpenKey(a, 'Apache Group')
        a = _winreg.OpenKey(a, 'Apache')

        # get latest version
        versions = []
        i = 0
        while True:
            try:
                v = _winreg.EnumKey(a, i)
            except:
                break
            versions.append(v)
            i += 1
        # print 'versions =', versions
        if not versions:
            ##raise 'No apache versions found.'
            return ''

        latestversion = max(versions)
        # print 'latest version =', latestversion

        a = _winreg.OpenKey(a, latestversion)
        i = 0
        val = _winreg.EnumValue(a, i)
        while val[0] != 'ServerRoot':
            i += 1
            val = _winreg.EnumValue(a, i)
        # print 'val =', val
        apachepath = val[1]
        print 'apachepath =', apachepath
        return apachepath
    except:
        print 'ERROR>>> Apache installation not found.'
        return ''



def create_registry_entry(dst):
    """moved from install-repository-lai.py
    create repository path in windows registry."""
    dsh_utils.db_print3('ryw_xp:create_registry_entry() entered...', 50)
    try:
        a = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE')
        a = _winreg.CreateKey(a, 'Postmanet')
        a = _winreg.SetValue(a, 'Repository', _winreg.REG_SZ, dst)
    except:
        print 'ERROR>>> Could not set Postmanet\\Repository value in the windows registry.'
    


def free_MB(path):
    """returns the amount of available space in MB. used to be in ryw.py"""

    #tested.
    dsh_utils.db_print('ryw_xp:free_MB() entered...', 49)
    
    path = os.path.normpath(path)
    if not dsh_utils.try_mkdir_ifdoesnt_exist(path, 'free_MB'):
        dsh_utils.give_bad_news(
            'free_MB: try_mkdir_ifdoesnt_exist failed: ' + path,
            logging.critical)
        return 0
        
    try:
        sectorsPerCluster,bytesPerSector,numFreeClusters,totalNumClusters = \
            win32file.GetDiskFreeSpace(path)
    except:
        dsh_utils.give_bad_news(
            'fatal_error: failed to determine free disk space: '+path,
            logging.critical)
        return 0
    
    sectorsPerCluster = long(sectorsPerCluster)
    bytesPerSector = long(bytesPerSector)
    numFreeClusters = long(numFreeClusters)
    totalNumClusters = long(totalNumClusters)
    freeMB = (numFreeClusters * sectorsPerCluster * bytesPerSector) / \
             (1024 * 1024)
    return freeMB



def unlock(adRotateHandler, file):
    """used to be in ad.py."""

    dsh_utils.db_print('ryw_xp:unlock() entered...', 49)
    ad = adRotateHandler
    ad.highbits=-0x7fff0000
    ad.ov=pywintypes.OVERLAPPED()
    ad.hfile = win32file._get_osfhandle(file.fileno())
    win32file.UnlockFileEx(ad.hfile,0,ad.highbits,ad.ov) #remove locks
    ad.hfile.Close()



#####
# the following used to be in Flock.py
#####


def flock_init(flockSelf, file):

    #tested.
    dsh_utils.db_print('ryw_xp:flock_init() entered...', 49)
    fl = flockSelf
    secur_att = win32security.SECURITY_ATTRIBUTES()
    secur_att.Initialize()
    fl.highbits=0x7fff0000 #high-order 32 bits of byte range to lock

    #make a handle with read/write and open or create if doesn't exist
    fl.hfile=win32file.CreateFile(
        fl.file, win32con.GENERIC_READ|win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ|win32con.FILE_SHARE_WRITE,
        secur_att, win32con.OPEN_ALWAYS, win32con.FILE_ATTRIBUTE_NORMAL,
        0)



def flock_lock(flockSelf):

    #tested.
    dsh_utils.db_print('ryw_xp:flock_lock() entered...', 49)
    fl = flockSelf
    if fl.type['LOCK_EX']:  #exclusive locking
        if fl.type['LOCK_NB']: #don't wait, non-blocking
            lock_flags=win32con.LOCKFILE_EXCLUSIVE_LOCK| \
                        win32con.LOCKFILE_FAIL_IMMEDIATELY
        else: #wait for lock to free
            lock_flags=win32con.LOCKFILE_EXCLUSIVE_LOCK
    else: #shared locking
        if fl.type['LOCK_NB']: #don't wait, non-blocking
            lock_flags=win32con.LOCKFILE_FAIL_IMMEDIATELY
        else:#shared lock wait for lock to free
            lock_flags=0

        #used to indicate starting region to lock
    fl.ov=pywintypes.OVERLAPPED() 
    win32file.LockFileEx(fl.hfile,lock_flags,0,fl.highbits,fl.ov)



def flock_unlock(flockSelf):
    #remove locks

    #tested
    dsh_utils.db_print('ryw_xp:flock_unlock() entered...', 49)
    fl = flockSelf
    win32file.UnlockFileEx(fl.hfile,0, fl.highbits, fl.ov) 
    fl.hfile.Close()



#####
# the above used to be in Flock.py.
#####



def script_repository_root_string(repositoryRootPath):
    """used to be hard-coded in install-repository-lai.py.
    used to be something like this:
    RepositoryRoot = 'e:\\Postmanet\\repository' """

    return "RepositoryRoot = '%s'" % repositoryRootPath.replace('\\', '\\\\')



def write_script_prefix(f, g, modpaths, baseName):
    """used to be su.copyScript()."""

    g.write('#!' + sys.executable + ' -u\n')

    if baseName in dsh_utils.RYW_ISO_ENCODING_PREFIX_FILES:
        g.write(dsh_utils.RYW_ISO_ENCODING_PREFIX + "\n")
    
    g.write('import os, sys\n')
    g.write('appendedmodpaths = []\n')
    for p in modpaths:
        p = p.replace('\\', '\\\\')
        g.write("sys.path.append('" + p + "')\n")
        g.write("appendedmodpaths.append('" + p + "')\n")



def copy_password_file(src, dst):
    """used to be in install-repository-lai.py."""
    shutil.copyfile(os.path.join(src, 'Passwords'),
                    os.path.join(dst, 'Passwords'))    
    dsh_utils.db_print3('ryw_xp:ryw_password_file() executed.', 50)



def move_stuff(src, dst):
    """used to be UploadObject.mymove()"""

    volSrc = win32file.GetVolumePathName(src)
    volDst = win32file.GetVolumePathName(dst)
    func = None
    if volSrc == volDst: 	# same physical drive
        func = shutil.move
    elif os.path.isdir(src):	# diff drive, src is dir
        func = shutil.copytree
    else:			# diff drive, src is file
        func = shutil.copy 
    func(src,dst)
    dsh_utils.db_print2('ryw_xp:move_stuff: src is: ' + src +
                  ' --->  dst is: ' + dst, 56)



def launch_explorer(path):
    """from explorer.launchExplorer()"""
    command = r"explorer"
    options = ["/n,","/root,",path]
    dsh_utils.db_print('launch_explorer: command is: ' +
                 repr([command] + options), 46)
    ret = subprocess.call([command] + options)
    if ret != 1:
        dsh_utils.give_bad_news("launch_explorer: Error in launching explorer.",
                          logging.error)
        return False
    return True



def sudo_chmod(path, smode='777', imode=0777, repositoryRoot = None):
    """from ryw.chmod_tree(). smode is a string, like '666' or '777'
    imode is a numbr, like 0666 or 0777.
    smode is used on Linux.
    imode is used on XP.
    caller should supply both.
    """
    os.chmod(path, imode)



#
# moved from ryw_ffmpeg.py
#
FFMPEG_PATH_SUFFIX = os.path.join('etc', 'ffmpeg', 'bin', 'ffmpeg.exe')
def verify_ffmpeg_existence(RepositoryRoot):
    commandPath = os.path.join(RepositoryRoot, FFMPEG_PATH_SUFFIX)
    if dsh_utils.is_valid_file(commandPath, 'verify_ffmpeg_existence'):
        return commandPath
    dsh_utils.give_news('Cannot find ffmpeg.  Advise you to install it.',
                  logging.info)
    return None



def fix_browse_rel_path(relpath):
    """moved from Browse.py."""
    relpath = relpath.replace('/', '\\')
    return relpath



def run_dos2unix_reread(fileName):
    """called during reformat_ntfs.py.
    the real version is in ryw_linux.py.
    on XP, we do nothing."""

    return None
