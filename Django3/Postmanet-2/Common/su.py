import sys, os, time, random, pickle, zipfile, cStringIO, shutil
import logging, ryw, ryw_bizarro, stat



# for path = 'C:\a\b\c\d', it creates path directory and all its parent directories if needed
def createdirpath(path):
##    print 'createdirpath', path
    #RYW
    if os.path.exists(path) and os.path.isdir(path):
        return

    os.makedirs(path)
### -----

##def createdirpath(path):
##    if path[-1] == os.sep:
##        path = path[:-1]
##
##    if os.path.exists(path):
##        return
##
##    head, tail = os.path.split(path)
##
##    # to handle the case where path == 'C:' or 'C:\'
##    if(head == path):
##        return
##
##    createdirpath(head)
##    os.mkdir(path)
##### -----


# for path = 'C:\a\b\c\d', it creates 'C:\a\b\c\' and its parent directories if needed
def createparentdirpath(path):
    if path[-1] == os.sep:
        path = path[:-1]

    head, tail = os.path.split(path)

    createdirpath(head)
    #RYW
    return head
### -----

# read a good line
# a white-space-only line or a line starting with '#' is not good
def readgl(f):
    while True:
        line = f.readline()
        if line == '':
            return ''
        if line[0] == '#' or line.isspace():
            continue
        return line
### -----
    
# read a good line, raise error if such a line is not found
def readglne(f):
    line = readgl(f)
    if line == '':
        raise 'Non-empty line expected..'
    else:
        return line
### -----

# lock -- try to create a lock directory
def lock(name, count):

    return

    tosleep = 1.0
    random.seed()
    for i in range(count):
        try:
            os.mkdir(name)
            return
        except:
            time.sleep(random.random() * tosleep)
            tosleep *= 2.0

    raise 'Could not lock ' + name + ' in ' + count + ' attempts'

# unlock -- remove the lock directory
def unlock(name):
    return
    os.rmdir(name)

def pickload(name):
    #RYW: changed to "rb"
    value = ryw.pickle_load_raw_and_text(name)
    return value

def pickdump(value, name):
    #
    # RYW, changed this to "wb".
    # this might have been causing the Linux incompatibility.
    #
    #f = open(name, 'w')
    f = open(name, 'wb')
    pickle.dump(value, f)
    f.flush()
    os.fsync(f.fileno())
    f.close()

def zipfile_extractall(srcfile, dstdir):
    if dstdir[-1] != '\\':
        dstdir = dstdir + '\\'
    
    z = zipfile.ZipFile(srcfile)
    if not os.path.exists(dstdir):
        createdirpath(dstdir)

    namelist = z.namelist()
    for n in namelist:
        # extract n from zip to dstdir
        m = n.replace('/', '\\')

        if m[-1] == '\\':
            createdirpath(dstdir + m)
        else:
            targetfile = dstdir + m
            createparentdirpath(targetfile)

            f = open(targetfile, 'wb')
            
            f.write(z.read(n))

            f.close()
    z.close()

def parseKeyValueFile(name):
    #RYW: changed to "rb"
    f = open(name, "rb")
    d = parseKeyValueFileObject(f)
    f.close()
    return d

def parseKeyValueString(s):
    f = cStringIO.StringIO(s)
    return parseKeyValueFileObject(f)

def parseKeyValueFileObject(f):
    d = {}

    line = readgl(f).replace('\r', '')
    while line:
        line = line.strip()
        key, value = line.split('=', 1)

        if value == '\\': # multi-line value begins with \ and ends with .
            value = ''
            
            line = f.readline().replace('\r', '')
            while line != '' and line.strip() != '.':
                value += line
                line = f.readline().replace('\r', '')
                
        elif value == '\\\\': # single-line value equal to a single backslash must be given as two backslashes
            value = '\\'


##        if value[0] == '\\': # single-line value starting with { or \ must start with an extra \
##            value = value[1:]
##        elif value[0] == '{': # multi-line text value
##            value = ''
##            line = f.readline().replace('\r', '')
##            while line != '' and line != '}' and line != '}\n':
##                value += line
##                line = f.readline().replace('\r', '')
##
##            if value[-1] == '\n':
##                value = value[:-1]

        d[key] = value
        line = readgl(f)

    return d

def addpythonpathtoscript(n, pythonpath):
    orig = n
    temp = orig + '.TEMP'
    f = open(orig)
    g = open(temp, 'w')
    g.write('#!' + pythonpath + ' -u\n')
    for line in f:
        g.write(line)
    f.close()
    g.close()
    os.remove(orig)
    os.rename(temp, orig)



def copyScript(src, dst, modpaths, ss):

    baseName = os.path.basename(src)

    if not os.path.exists(src):
        return

    f = open(src)
    g = open(dst, 'w')

    ryw_bizarro.write_script_prefix(f, g, modpaths, baseName)

    g.write('\n' + ss + '\n')
    g.write('\n########################################\n\n')
    for line in f:
        g.write(line)

    f.close()
    g.close()
    os.chmod(dst, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)

    

def copytree(src, dst, isInstall = False):
##    print 'copytree', src, ';', dst
    if not os.path.exists(src):
        return

    if os.path.isfile(src):
        fileName = os.path.basename(src)
        if fileName == 'Thumbs.db':
            return
        try:
            shutil.copyfile(src, dst)
            os.chmod(dst, 0666)
        except:
            ryw.give_bad_news('copytree: copyfile failed: ' +
                              src + ' -> ' + dst, logging.critical)
            raise
    else:
        if not os.path.exists(dst):
            createdirpath(dst)

        for n in os.listdir(src):
            if isInstall and n.lower() == "cvs":
                continue
            copytree(os.path.join(src, n), os.path.join(dst, n), isInstall)



def copyscripttree(src, dst, modpaths, ss, isInstall = False,
                   repositoryRoot = None):

    if repositoryRoot == None:
        repositoryRoot = RepositoryRoot
    
    if not os.path.exists(src):
        return

    if os.path.isfile(src):
        if os.path.basename(src).endswith('.py'):
            copyScript(src, dst, modpaths, ss)
        elif os.path.basename(src).endswith('.pyc'):
            pass
        else:
            shutil.copyfile(src, dst)
            ryw_bizarro.sudo_chmod(dst, '666', 0666,
                                   repositoryRoot = repositoryRoot)
    else:
        if not os.path.exists(dst):
            createdirpath(dst)

        for n in os.listdir(src):
            if isInstall and n.lower() == "cvs":
                continue
            copyscripttree(os.path.join(src, n),
                           os.path.join(dst, n),
                           modpaths, ss, isInstall,
                           repositoryRoot = repositoryRoot)
