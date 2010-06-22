#
# just give two drive letters as arguments, like so:
# python compare.py e: g:
#



import os, sys, filecmp, traceback



fileCount = 0
listNamesIgnore = ['Thumbs.db', 'upload.log', 'SearchResults']
readHowMuch = 1024
printInterval = 50
onlyInOneCount = 0
differentCount = 0



def check_dirs(dir1, dir2):
    if not os.path.exists(dir1):
        print 'directory1 does not exist: ' + dir1
        return False
    if not os.path.exists(dir2):
        print 'directory2 does not exist: ' + dir2
        return False
    if not os.path.isdir(dir1):
        print 'dir1 is not a directory: ' + dir1
        return False
    if not os.path.isdir(dir2):
        print 'dir2 is not a directory: ' + dir2
        return False
    return True



def check_file_count():
    global fileCount
    fileCount += 1
    if fileCount != 0 and fileCount % printInterval == 0:
        print 'files examined: ' + str(fileCount)



#
# return (identical, commonSet)
#
def find_common(dir1, dir2):
    global onlyInOneCount
    try:
        names1 = os.listdir(dir1)
        names2 = os.listdir(dir2)
    except:
        print 'os.listdir failed: ' + dir1 + ' <> ' + dir2
        return (False, None)

    nameSet1 = set(names1)
    nameSet2 = set(names2)

    commonSet = nameSet1 & nameSet2
    ignoreSet = set(listNamesIgnore)
    diff1 = nameSet1 - commonSet - ignoreSet
    diff2 = nameSet2 - commonSet - ignoreSet

    same = True
    if len(diff1) != 0:
        print 'listdir1: ' + dir1 + ' : ' + repr(diff1)
        same = False
        onlyInOneCount += len(diff1)
    if len(diff2) != 0:
        print 'listdir2: ' + dir2 + ' : ' + repr(diff2)
        same = False
        onlyInOneCount += len(diff2)
    return (same, commonSet)



def compare_file_parts(name1, name2):
    try:
        size1 = os.path.getsize(name1)
        size2 = os.path.getsize(name2)
        if size1 != size2:
            print 'size different: ' + name1 + ' <> ' + name2
            return False
        
        f1 = open(name1, 'rb')
        f2 = open(name2, 'rb')
        buf1 = f1.read(readHowMuch)
        buf2 = f2.read(readHowMuch)

        same = True
        if buf1 != buf2:
            print 'file beginnings do not match: ' + name1 + ' <> ' + name2
            same = False
        
        if same and size1 > 2 * readHowMuch:
            f1.seek(size1 - readHowMuch, 0)
            f2.seek(size2 - readHowMuch, 0)
            buf1 = f1.read(readHowMuch)
            buf2 = f2.read(readHowMuch)
            if buf1 != buf2:
                print 'file endings do not match: ' + name1 + ' <> ' + name2
                same = False

        f1.close()
        f2.close()
        return same
    except:
        print 'compare_file_parts failed: ' + name1 + ' <> ' + name2
        print traceback.format_exc()
        return False



def compare_two_files(name1, name2):
    global differentCount
    
    # the third argument, the false flag, forces real comparison,
    # as opposed to just looking at the stat.
    #result = filecmp.cmp(name1, name2, False)

    same = filecmp.cmp(name1, name2, True)
    if not same:
        print 'files different: ' + name1 + ' <> ' + name2

    if same:
        same = compare_file_parts(name1, name2)

    if not same:
        differentCount += 1
        
    check_file_count()
    return same



def compare_one_name(dir1, dir2, name):

    if name in listNamesIgnore:
        #
        # names to be skipped.
        #
        return True
    
    name1 = os.path.join(dir1, name)
    name2 = os.path.join(dir2, name)

    try:
        if os.path.isfile(name1) and os.path.isfile(name2):
            result = compare_two_files(name1, name2)
            return result
        if os.path.isdir(name1) and os.path.isdir(name2):
            result = compare_dirs(name1, name2)
            return result
        print 'comparing file and directory: ' + name1 + ' <> ' + name2
        return False
    except:
        print 'compare_one_name failed: ' + dir1 + ' <> ' + dir2 + ' : ' + name
        print traceback.format_exc()
        return False
    


def compare_dirs(dir1, dir2):
    if not check_dirs(dir1, dir2):
        return False

    sameList,commonSet = find_common(dir1, dir2)
    if not sameList and len(commonSet) == 0:
        print 'nothing in common: ' + dir1 + ' <> ' + dir2
        return False

    for name in commonSet:
        namedIsSame = compare_one_name(dir1, dir2, name)
        
    return True
        


def main():
    try:
        dir1 = sys.argv[1]
        dir2 = sys.argv[2]
    except:
        print 'failed to get arguments.'
        sys.exit(1)

    dir1 = os.path.join(dir1, r"\Postmanet")
    dir2 = os.path.join(dir2, r"\Postmanet")
    #dir1 = os.path.join(dir1, r"\test")
    #dir2 = os.path.join(dir2, r"\test")

    compare_dirs(dir1, dir2)

    print '----------'
    if onlyInOneCount != 0:
        print 'items only in one place: ' + str(onlyInOneCount)
    if differentCount != 0:
        print 'items that are different: ' + str(differentCount)
    if onlyInOneCount == 0 and differentCount == 0:
        print 'completely identical!'

    

if __name__ == '__main__':
    main()

