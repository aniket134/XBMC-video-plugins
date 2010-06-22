import win32file
import win32con
import win32security
import win32api
import pywintypes
import Flock

l=Flock.Flock('foo')

#l.type['LOCK_EX']=0
l.type['LOCK_EX']=1

l.type['LOCK_NB']=0



print 'calling lock'

l.lock()

print 'now locked '

#sys.exit(1)


#win32api.Sleep(1000)
win32api.Sleep(10000)

l.unlock()

print 'now unlocked'
