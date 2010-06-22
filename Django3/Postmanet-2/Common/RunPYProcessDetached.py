
import sys, os

def runpyprocessdetached(path, args):

    args = ['python.exe', path] + args

    os.spawnv(os.P_DETACH, sys.executable, args)

if __name__ == '__main__':

    if len(sys.argv) > 1:
        runpyprocessdetached(sys.argv[1], sys.argv[2:])
