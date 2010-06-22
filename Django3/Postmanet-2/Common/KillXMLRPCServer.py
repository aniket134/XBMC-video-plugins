
import sys, xmlrpclib

def kill(port):

    server = xmlrpclib.ServerProxy("http://localhost:" + str(port))

    server.kill()

if __name__ == '__main__':

    kill(sys.argv[1])
