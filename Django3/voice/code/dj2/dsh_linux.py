#
# copied from Postmanet-2.
#

import sys
import dsh_utils
import shutil, os
from subprocess import *
import portalocker
import subprocess
import logging



def get_subprocess_output_lines(cmd):
    process = Popen(cmd, stdout=PIPE, stderr=STDOUT)
    outputLines = process.stdout.readlines ()
    exitStat = process.wait ()
    return outputLines



def get_subprocess_output_line(cmd):
    lines=get_subprocess_output_lines(cmd)
    return lines[0]



def get_apache_path():
    dsh_utils.db_raise_or_print3('ryw_linux:get_apache_path() called.', 50)
    try:
        output = get_subprocess_output_line(['/usr/bin/which', 'apache2'])
    except:
        dsh_utils.give_bad_news3("can't find apache.")
        output = '/dev/null'
    return output



def create_registry_entry(dst):
    """moved from install-repository-lai.py
    create repository path in windows registry."""
    dsh_utils.db_raise_or_print3 (
        'ryw_linux:create_registry_entry() called.', 50)



def free_MB(path):
    """returns the amount of available space in MB."""
    fsStat = os.statvfs(path)
    availMB = fsStat.f_bavail / 1024 * fsStat.f_bsize / 1024
    return availMB



def unlock(adRotateHandler, file):
    """used to be in ad.py."""
    raise 'ryw_linux:unlock() called.'



#####
# the following used to be in Flock.py
#####


def flock_init(flockSelf, file):
    dsh_utils.db_print2('ryw_linux.flock_init: file is: ' + file, 56)
    fl = flockSelf
    fl.hfile = open(file, "a+")
    


def flock_lock(flockSelf):
    fl = flockSelf
    dsh_utils.db_print2('ryw_linux:flock_lock(): file is: ' + fl.file, 56)
    if fl.type['LOCK_EX']:
        lockFlags = portalocker.LOCK_EX
    else:
        lockFlags = portalocker.LOCK_SH

    if fl.type['LOCK_NB']:
        lockFlags = lockFlags | portalocker.LOCK_NB
        
    portalocker.lock(fl.hfile, lockFlags)

        

def flock_unlock(flockSelf):
    fl = flockSelf
    dsh_utils.db_print2('ryw_linux:flock_unlock(): file is: ' + fl.file, 56)
    portalocker.unlock(fl.hfile)
    fl.hfile.close()



#####
# the above used to be in Flock.py.
#####



def script_repository_root_string(repositoryRootPath):
    """used to be hard-coded in install-repository-lai.py.
    used to be something like this:
    RepositoryRoot = 'e:\\Postmanet\\repository' """

    return "RepositoryRoot = '%s'" % repositoryRootPath



def write_script_prefix(f, g, modpaths, baseName):
    """used to be su.copyScript()."""

    g.write('#!' + sys.executable + ' -u\n')

    if baseName in dsh_utils.RYW_ISO_ENCODING_PREFIX_FILES:
        g.write(dsh_utils.RYW_ISO_ENCODING_PREFIX + "\n")
    
    g.write('import os, sys\n')
    g.write('appendedmodpaths = []\n')
    for p in modpaths:
        g.write("sys.path.append('" + p + "')\n")
        g.write("appendedmodpaths.append('" + p + "')\n")



def copy_password_file(src, dst):
    """used to be in install-repository-lai.py."""
    shutil.copyfile(os.path.join(src, 'pw_linux'),
                    os.path.join(dst, 'Passwords'))
    dsh_utils.db_print3('ryw_linux:ryw_password_file() executed.', 50)



def move_stuff(src, dst):
    """used to be UploadObject.mymove()"""

    shutil.move(src, dst)
    dsh_utils.db_print2('ryw_linux:move_stuff: src is: ' + src +
                  ' --->  dst is: ' + dst, 56)
    #raise 'ryw_linux.move_stuff() entered...'



def launch_explorer(path):
    """from explorer.launchExplorer()"""

    #
    # If I don't redirect stdout and stderr,
    # this stuff gets sent to the browser window.
    #
    pair = stdio_logs_open()
    if pair:
        stdout = pair[0]
        stderr = pair[1]
    else:
        stdout = None
        stderr = None


    if os.path.exists('/usr/local/bin/rox'):
        dsh_utils.db_print_info_browser('launch_explorer: found rox.', 91)
        command = '/usr/local/bin/rox '
    elif os.path.exists('/usr/bin/thunar'):
        dsh_utils.db_print_info_browser('launch_explorer: found thunar.', 91)
        command = '/usr/bin/thunar --display :0.0 '
    else:
        dsh_utils.give_bad_news("launch_explorer: can't find an explorer.",
                          logging.error)
        return False
        
    command = command + path + ' &'
    dsh_utils.db_print_info_browser(
        'launch_explorer: command is: ' + command, 91)
    ret = subprocess.call(command, shell=True, stdout=stdout, stderr=stderr,
                          env={'DISPLAY':':0.0'})

    stdio_logs_close(pair)
    
    if ret != 0:
        dsh_utils.give_bad_news('launch_explorer: error in launching explorer.',
                          logging.error)
        return False
    return True



def stdio_logs_open(logDirectory=''):
    """called by launch_explorer(), redirects stdout and stderr.
    so they don't get sent to the browser window."""

    if logDirectory == '':
        logDir = os.path.join(RepositoryRoot, 'WWW', 'logs')
    else:
        logDir = logDirectory

    try:
        stdout = open(os.path.join(logDir, 'stdout.txt'), 'a')
        stderr = open(os.path.join(logDir, 'stderr.txt'), 'a')
        return [stdout, stderr]
    except:
        dsh_utils.give_bad_news('stdio_logs_open: failed to open log files.',
                          logging.error)
        return None
    


def stdio_logs_close(pair):
    """called by launch_explorer(), closes stdout and stderr logs."""
    if pair:
        pair[0].close()
        pair[1].close()



def sudo_chmod(path, smode='777', imode=0777, repositoryRoot = None):
    """from ryw.chmod_tree(). smode is a string, like '666' or '777'
    imode is a numbr, like 0666 or 0777.
    smode is used on Linux.
    imode is used on XP.
    caller should supply both.
    """

    if repositoryRoot == None:
        repositoryRoot = RepositoryRoot
        
    #chmodPath = os.path.join(repositoryRoot, 'etc', 'chmod')
    chmodPath = os.path.join('/usr/local/bin', 'cmod2')

    if not dsh_utils.is_valid_file(chmodPath):
        dsh_utils.give_bad_news(
            'Cannot find suid chmod. Advise you to fix this.', logging.error)
        return

    command = chmodPath + ' ' + smode + ' ' + path
    ret = subprocess.call(command, shell=True)

    if ret != 0:
        dsh_utils.give_bad_news('sudo_chmod failed on ' + path, logging.error)



#
# moved from ryw_ffmpeg.py
#
def verify_ffmpeg_existence(RepositoryRoot):
    commandPath = r'/usr/bin/ffmpeg'
    if dsh_utils.is_valid_file(commandPath, 'verify_ffmpeg_existence'):
        return commandPath
    dsh_utils.give_news('Cannot find ffmpeg.  Advise you to install it.',
                  logging.info)
    return None



def fix_browse_rel_path(relpath):
    """moved from Browse.py."""
    relpath = relpath.replace('\\', '/')
    return relpath



def dos2unix(fileName):
    """called during reformant_ntfs.py."""

    commandPath = '/usr/bin/dos2unix'
    if not os.path.exists(commandPath):
        dsh_utils.give_bad_news("ryw_linux.dos2unix: dos2unix doesn't exist. " +
                          "should fix this: apt-get install tofrodos.",
                          logging.error)
        return False

    command = commandPath + ' ' + fileName
    ret = subprocess.call(command, shell=True)

    if ret != 0:
        dsh_utils.give_bad_news(
            'ryw_linux.dos2unix: error in running dos2unix: ' +
            fileName, logging.error)
        return False
    else:
        dsh_utils.db_print_info_browser(
            'ryw_linux.dos2unix: dos2unix success: ' +
            fileName, 69)

    return True



def run_dos2unix_reread(fileName):
    """called during reformat_ntfs.py."""

    if not dos2unix(fileName):
        return None
    
    value = dsh_utils.pickle_load_raw_and_text(fileName, dos2unix=True)
    return value
