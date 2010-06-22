
import sys, os, stat, shutil

def recursively_make_writable(name):
	os.chmod(name, stat.S_IRWXU)

	if os.path.isdir(name):
		for n in os.listdir(name):
			recursively_make_writable(os.path.join(name, n))

def recursively_remove_cvsdirs(directory):
	if not os.path.isdir(directory):
		return

	for name in os.listdir(directory):
		fullname = os.path.join(directory, name)

		if os.path.isdir(fullname):
			if name == 'CVS' or name == 'cvs':
				recursively_make_writable(fullname)
				shutil.rmtree(fullname)
			else:
				recursively_remove_cvsdirs(fullname)

if __name__ == '__main__':

	directory = sys.argv[1]

	recursively_remove_cvsdirs(directory)

