
import sys, os

########################################################################################

if __name__ == '__main__':

    cwd = os.getcwd()
    script_rel_path = sys.argv[0]
    script_abs_path = os.path.join(cwd, script_rel_path)
    topdir = os.path.dirname(script_abs_path)

    print 'Installing from %s' % topdir

    common  = os.path.join(topdir, 'Common')

    sys.path.append(common)
    import su

    usage = '''

    Usage:
        * Run the script as:
		python copy-pythonscriptsforclient.py <Nihao installation directory>

	* It copies scripts from Repository/pythonscriptsforclient to their proper
		place in the target Nihao installation (village side)
    '''

    if len(sys.argv) != 2:
        print usage
        sys.exit(1)

    NihaoRoot = os.path.abspath(sys.argv[1])

    scriptdir = os.path.join(topdir, 'Repository', 'pythonscriptsforclient')
    mycgi = os.path.join(NihaoRoot, 'cgi-bin', 'repository')

    su.createdirpath(mycgi)

    scripts = os.listdir(scriptdir)
    for s in scripts:
	if s.lower() != 'cvs':
        	su.copyScript(os.path.join(scriptdir, s), os.path.join(mycgi, s), [os.path.join(NihaoRoot, 'Common')], "NihaoRoot = '%s'" % NihaoRoot.replace('\\', '\\\\'))

