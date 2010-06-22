import sys, os
import su
import random
import logging
import zlib
import cPickle
import tarfile
import shutil

OBJECT_NAME_LEN = 20
OBJECT_TREE_DEPTH = 4   # small, must be definitely less than OBJECT_NAME_LEN

# allowed chars are the following, and all alpha and numeric characters
# all alpha are interpreted as uppercase
#allowedchars = "`~!@$%^&()-_=+{}[];',."
allowedchars = '_'
allowedchars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
allowedchars += '0123456789'

allowedcharset = set(allowedchars)
# The following are forbidden in windows: \/:*?"<>|

# We'll use '#' for versioning

# if path is nametopath(objectstoreroot, objectname), then
#       path#1_data\ contains the data for the object
#                       data may be a single file Lecture1.ppt,
#                       or a directory tree Software-1.1.10/
#                       or both or multiple instances of both
#       path#1_desc is the description file for the version
#       path#1_done is an empty or trivial file written to indicate that
#                       the object was successfully and completely
#                       uploaded into the repository

def isvalidname(name):
    if len(name) <= OBJECT_TREE_DEPTH:
        return False
    for i in range(len(name)):
        if not name[i] in allowedcharset:
            return False
    return True
### -----

def nametopath(root, name):
    #logging.debug('entering nametopath: ' + root + name)
    assert isvalidname(name)
    name = name.upper()

    if root[-1] != os.sep:
        root += os.sep

    path = root
    for i in range(OBJECT_TREE_DEPTH):
        path += name[0]
        name = name[1:]
        path += os.sep

    path += name
    #logging.debug('path is '+path)
    return path
### -----

def getlatestversion(root, name):
### TODO: remove the assumption that version numbers have to be contiguous
# you may have versions 1 3 and 6. Others were deleted at differents points in time.
    path = nametopath(root, name)

    version, next = (0, 1)
    while os.path.exists(path + '#' + str(next) + '_DONE'):
        version = next
        next = version + 1
    return version
### -----

def nameversiontopaths(root, name, version):
    path = nametopath(root, name)
    prefix = path + '#' + str(version)
    return (prefix + '_DATA', prefix + '_META', prefix + '_DONE')
### -----

def name_version_to_paths_aux(root, name, version):
    """RYW: added to account for the _AUXI files."""
    path = nametopath(root, name)
    prefix = path + '#' + str(version)
    return (prefix + '_DATA', prefix + '_META',
            prefix + '_AUXI', prefix + '_DONE', prefix + '_MDON')
### -----

def nameversiontopath(root, name, version):
    return nameversiontopaths(root, name, version)[0]
### -----

def nameversiontoprefix(root, name, version):
    return nametopath(root, name) + '#' + str(version)

def createdummyobject(root, name, version):
    assert isvalidname(name)
    a, b, c = nameversiontopaths(root, name, version)
    su.createparentdirpath(a)
    os.mkdir(a)
    os.system('echo ss > ' + b)
    os.system('echo ss > ' + c)
### -----

def nobjiter(nroot, prefix, n, ver):
    if os.path.exists(nroot):
        ll = os.listdir(nroot)
        ll.sort()
        if n == 0:
            s = set([])
            for i in ll:
                if i[-5:] == '_DONE':
                    k = i.find('#')
                    objname = prefix + i[:k]
                    version = int(i[k+1:-5])
                    if ver:
                        s.add((objname, version))
                    else:
                        s.add(objname)
            for i in s:
                yield i
        else:
            for i in ll:
                for j in nobjiter(nroot + os.sep + i, prefix + i, n - 1, ver):
                    yield j
### -----

def objectiterator(root):
    if root[-1] == os.sep:
        root = root[:-1]

    for i in nobjiter(root, '', OBJECT_TREE_DEPTH, False):
        yield i
### -----

def objectversioniterator(root):
    if root[-1] == os.sep:
        root = root[:-1]

    for i in nobjiter(root, '', OBJECT_TREE_DEPTH, True):
        yield i
### -----

def generateNewObjectID():
    objectid = ''
    random.seed()
    for i in range(OBJECT_NAME_LEN):
        k = random.randrange(len(allowedchars))
        objectid += allowedchars[k]
    return objectid

##name = 'SumeetSobti~!@$%^&()'
##root = 'C:\sobti\objroot'
##path = nametopath(root, name)

def partial_object_version_iterator(root):
    for i in partial_object_iterator_aux(root, '', OBJECT_TREE_DEPTH, True):
        yield i

def partial_object_iterator_aux(nroot, prefix, n, ver):
    if os.path.exists(nroot):
        ll = os.listdir(nroot)
        ll.sort()
        if n == 0:
            s = set([])
            for i in ll:
                k = i.find('#')
                objname = prefix + i[:k]
                version = int(i[k+1:-5])
                if ver:
                    s.add((objname, version))
                else:
                    s.add(objname)
            for i in s:
                yield i
        else:
            for i in ll:
                for j in partial_object_iterator_aux(os.path.join(nroot, i), prefix + i, n - 1, ver):
                    yield j

def object_component_iterator(root, name, version):
    datapath = nameversiontopaths(root, name, version)[0]
    datapath_dirname = os.path.dirname(datapath)
    datapath_basename = os.path.basename(datapath)

    name_version_prefix = name[:OBJECT_TREE_DEPTH]
    name_version_suffix = datapath_basename[:-5]

    name_version = name_version_prefix + name_version_suffix
    assert name_version == '%s#%d' % (name, version)

    if os.path.exists(datapath_dirname):
        names = [name for name in os.listdir(datapath_dirname) if name.startswith(name_version_suffix)]
    else:
        names = []
    names.sort()

    for name in names:
        path = os.path.join(datapath_dirname, name)
        for i in object_component_iterator_aux(name[len(name_version_suffix):], path):
            a, b = i
            assert os.path.exists(b)
            yield i

def object_component_iterator_aux(name, path):
    yield (name, path)

    if os.path.isdir(path):
        names = os.listdir(path)
        names.sort()
        for child in names:
            childpath = os.path.join(path, child)
            childname = os.path.join(name, child)
            for i in object_component_iterator_aux(childname, childpath):
                yield i

def checksum_file(path):
    '''
    Uses CRC32 checksum.
    '''
    f = open(path, 'rb')
    try:
        checksum = 0
        while True:
            bytes = f.read(16384)
            if not bytes:
                break
            checksum = zlib.crc32(bytes, checksum)
    finally:
        f.close()
    return checksum

def digest_file(path):
    length = os.path.getsize(path)
    checksum = checksum_file(path)
    return (length, checksum)

class Digest(dict):
    '''
    Keys are "normalized" file/directory names.
    Values are digests.
    Digest of a directory name is just ('d',)
    Digest of a file name is ('f', file_length, file_checksum)
    "Normalization" is done so that the file and directory names
    are relative to the object's name and version -- not relative
    to the root of the object store or c:\. This allows us to
    compare the digests of two objects, each from a different object
    store that could have root in different directories in their
    respective file systems.
    '''
    def __init__(self, root, name, version):
        dict.__init__(self)

        self.name = name
        self.version = version

        for component_name, component_path in object_component_iterator(root, name, version):
            if component_name.find('\\') < 0 and component_name.endswith('_DGST'):
                continue

##            print 'Digesting', component_name, component_path

            if os.path.isfile(component_path):
                self[component_name] = ('f', digest_file(component_path)) ## file
            else:
                self[component_name] = ('d',) ## directory

    def __str__(self):
        lines = []

        lines.append('Digest for object: %s#%d' % (self.name, self.version))
        keys = self.keys()
        keys.sort()
        for key in keys:
            lines.append('%s : %s' % (key, self[key]))

        return '\n'.join(lines)

    def diff(self, other):
        onlythishas = []
        onlythathas = []
        changed = []

        keys = self.keys()
        keys = keys + [key for key in other.keys() if key not in keys]
        keys.sort()

        for key in keys:
            if not self.has_key(key):
                onlythathas.append(key)
            elif not other.has_key(key):
                onlythishas.append(key)
            elif self[key] != other[key]:
                changed.append(key)

        return changed, onlythishas, onlythathas

## For a single object

def get_digest_file_name(root, name, version):
    path = nametopath(root, name)
    return path + '#' + str(version) + '_DGST'

def write_digest_file_for_object(root, name, version):
    digest = Digest(root, name, version)

    dgst_file_name = get_digest_file_name(root, name, version)

    f = open(dgst_file_name, 'wb')
    cPickle.dump(digest, f)
    f.close()

    return digest

def make_digest_file_exist_for_object(root, name, version):
    dgst_file_name = get_digest_file_name(root, name, version)

    if not os.path.exists(dgst_file_name):
        write_digest_file_for_object(root, name, version)

def read_digest_file_for_object(root, name, version):
    dgst_file_name = get_digest_file_name(root, name, version)

    f = open(dgst_file_name, 'rb')
    thing = cPickle.load(f)
    f.close()

    return thing

def get_digest_for_object(root, name, version):
    make_digest_file_exist_for_object(root, name, version)
    return read_digest_file_for_object(root, name, version)

def soft_get_digest_for_object(root, name, version):
    try:
        return read_digest_file_for_object(root, name, version)
    except IOError:
        return Digest(root, name, version)

## For the entire object store

def write_digest_files_for_all_objects(root):
    for name, version in objectversioniterator(root):
        write_digest_file_for_object(root, name, version)

def write_missing_digest_files_for_objects(root):
    for name, version in objectversioniterator(root):
        dgst_file_name = get_digest_file_name(root, name, version)
        if not os.path.exists(dgst_file_name):
            write_digest_file_for_object(root, name, version)

def pickle_jar_iterator(file_name):
    f = open(file_name, 'rb')
    while True:
        try:
            yield cPickle.load(f)
        except EOFError:
            break
    f.close()

def list_pickle_jar(file_name):

    return [i for i in pickle_jar_iterator(file_name)]

def makedirs(d):
    if not os.path.exists(d):
        os.makedirs(d)

def copyfile(src, dst):
    makedirs(os.path.dirname(dst))
##    shutil.copyfile(src, dst)

    f = open(src, 'rb')
    g = open(dst, 'wb')
    bytes = f.read(4096)
    while bytes:
        g.write(bytes)
        bytes = f.read(4096)
    f.close()
    g.close()

def copy_file_or_dir(src, dst):
    if os.path.isfile(src):
        copyfile(src, dst)
    else:
        makedirs(dst)

class Object_Component_Copier:

    def __init__(self, root, name, version, dst_root):

        datapath = nameversiontopaths(dst_root, name, version)[0]
        self.dst_dirname = os.path.dirname(datapath)
        datapath_basename = os.path.basename(datapath)
        self.prefix = datapath_basename[:-5]

    def copy_component(self, component_name, component_path):

##        print '\n->', component_name, component_path

        def component_name_to_dst_path(component_name, dst_dirname, prefix):
            return os.path.join(dst_dirname, prefix + component_name)

        dst_path = component_name_to_dst_path(component_name, self.dst_dirname, self.prefix)
##        print 'Copying %s to %s' % (component_path, dst_path)
        copy_file_or_dir(component_path, dst_path)

def copy_object_components(root, name, version, dst_root, do_dgst=True, do_meta=True, do_thumbs_scaled=True, other_files_max_size=None):

    copier = Object_Component_Copier(root, name, version, dst_root)

    if do_dgst:
        make_digest_file_exist_for_object(root, name, version)

    for component_name, component_path in object_component_iterator(root, name, version):

        doit = False
        tokens = component_name.split('\\')

        if do_dgst and tokens[0].endswith('DGST'):
            doit = True

        if do_meta and tokens[0].endswith('META'):
            doit = True

        if do_thumbs_scaled and tokens[0].endswith('AUXI') and len(tokens) > 1 and tokens[1] == 'thumbs_scaled':
            doit = True

        if os.path.isfile(component_path):
            file_size = os.path.getsize(component_path)
            if other_files_max_size is None or other_files_max_size >= file_size:
                doit = True
        else:
            doit = True # always do directories

        if doit:
            copier.copy_component(component_name, component_path)

def assimilate_updates(src_root, name, version, dst_root):

    src_digest = soft_get_digest_for_object(src_root, name, version)
    dst_digest = soft_get_digest_for_object(dst_root, name, version)

    changed, src_has, dst_has = src_digest.diff(dst_digest)

    copier = Object_Component_Copier(src_root, name, version, dst_root)

    for component_name, component_path in object_component_iterator(src_root, name, version):

        tokens = component_name.split('\\')

        if component_name in changed + src_has and (not tokens[0].endswith('DGST')):
            copier.copy_component(component_name, component_path)

    write_digest_file_for_object(dst_root, name, version)

def iterator_range(start, stop, iterator, *args):
    count = 0
    for i in iterator(*args):
        if start <= count < stop:
            yield i
        if count >= stop:
            break
        count += 1
