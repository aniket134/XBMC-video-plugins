import sys



def f7_list_unique(seq, idfun=None):
    """returns a list that contains only unique elements of the original
    list. taken from:
    http://www.peterbe.com/plog/uniqifiers-benchmark
    """
    return list(_f7(seq, idfun))

def _f7(seq, idfun=None):
    seen = set()
    if idfun is None:
        for x in seq:
            if x in seen:
                continue
            seen.add(x)
            yield x
    else:
        for x in seq:
            x = idfun(x)
            if x in seen:
                continue
            seen.add(x)
            yield x



def add_to_sys_path(morePath=None):
    if morePath:
        sys.path += morePath
    sys.path = f7_list_unique(sys.path)



def add_l2_to_l1(l1, l2):
    for i in l2:
        if i not in l1:
            l1.append(i)
    return l1
