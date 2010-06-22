
import sys, os, stat, shutil

def same_contents(a, b):
	f = open(a)
	g = open(b)

	s = f.read()
	t = g.read()

	f.close()
	g.close()

	return s == t

def recursively_copy_changes(src, dst):
	if not os.path.exists(src):
		return

	if os.path.isfile(src):
		if (not os.path.exists(dst)) or (not same_contents(src, dst)):
			shutil.copyfile(src, dst)
	else:
		if not os.path.exists(dst):
			os.makedirs(dst)

		for name in os.listdir(src):
			fullsrcname = os.path.join(src, name)
			fulldstname = os.path.join(dst, name)
			recursively_copy_changes(fullsrcname, fulldstname)


if __name__ == '__main__':

	src = sys.argv[1]
	dst = sys.argv[2]

	recursively_copy_changes(src, dst)

