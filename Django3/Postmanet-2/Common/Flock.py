import ryw_bizarro


class Flock:
    def __init__(self,file):
        fl = self
        fl.file=file
        fl.type={'LOCK_EX':0,'LOCK_NB':0}
        ryw_bizarro.flock_init(self, file)



    def lock(self):
        ryw_bizarro.flock_lock(self)



    def unlock(self):
        ryw_bizarro.flock_unlock(self)


