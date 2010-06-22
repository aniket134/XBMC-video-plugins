import sys
from dvoice.db.models import Organization, Person, Item

def pre_save_hook(obj):
    if isinstance(obj, Organization):
        print 'adding u03.....................'
        print repr(obj)
        print repr(obj.uid)
        obj.u03 = ''

