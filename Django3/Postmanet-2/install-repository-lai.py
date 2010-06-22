
import sys, os, shutil, getopt



if __name__ == '__main__':

    cwd = os.getcwd()
    script_rel_path = sys.argv[0]
    script_abs_path = os.path.join(cwd, script_rel_path)
    topdir = os.path.dirname(script_abs_path)

    print 'Installing from %s' % topdir

    src     = os.path.join(topdir, 'Repository')
    common  = os.path.join(topdir, 'Common')

    sys.path.append(common)
    import ryw_bizarro, ryw
    import su
    
    usage = '''

    Install repository code.

    Prerequisites:
        * Install python
        * Install apache
        * Install robot

    Usage:
        * Run the script as:
            python install-repository.py <destination dir for repository> <jobs directory of robot> [0 if robot is not present]

    '''

    if len(sys.argv) < 3:
        print usage
        sys.exit(1)

    dst = os.path.abspath(sys.argv[1])

    robotsjobdir = os.path.abspath(sys.argv[2])


    robotPresent = "False"
    if len(sys.argv) == 4:
        if sys.argv[3] == "1":
	    robotPresent = "True"	    

    apachepath = ryw_bizarro.get_apache_path()
    ryw_bizarro.create_registry_entry(dst)


    # TODO: pythonpath unnecessary, but some other script may still
    # want to read it from Resources.txt
    pythonpath = sys.executable

    ryw.db_print3('python path is: ' + pythonpath, 50)
    ryw.db_print3('dst is: ' + dst, 50)

    su.createdirpath(dst)

    #
    # on XP: RepositoryRoot = 'e:\\Postmanet\\repository'
    # on Linux: RepositoryRoot = '/home/rywang/Postmanet/repository'
    #
    repositoryRootString = ryw_bizarro.script_repository_root_string(dst)
    ryw.db_print3('repo root is: ' + repositoryRootString, 50)
    
    #RYW
    #su.copytree(common, os.path.join(dst, 'Common'), isInstall = True)
    su.copyscripttree(common,
                      os.path.join(dst, 'Common'),
                      [],
                      repositoryRootString,
                      isInstall = True,
                      repositoryRoot = dst)

    ryw.db_print3('completed copying Common files.', 50)

    # RYW
    su.copytree(os.path.join(topdir, 'icons'),
                os.path.join(dst, 'WWW', 'icons'), isInstall = True)
    ryw.db_print3('completed copying icons.', 50)

    #su.copytree(os.path.join(src, 'pythonscriptsforclient'),
    #            os.path.join(dst, 'pythonscriptsforclient'), isInstall = True)
    
    # RYW put Nihao code on server so it can be shipped to clients too.
    #su.copytree(os.path.join(topdir, 'Nihao', 'cgi-bin', 'Nihao'),
    #            os.path.join(dst, 'NihaoScripts4Clients'),
    #            isInstall = True)
    #su.copytree(os.path.join(topdir, 'Common'),
    #            os.path.join(dst, 'CommonScripts4Clients'),
    #            isInstall = True)
    su.copytree(os.path.join(src, 'WWW'),
                os.path.join(dst, 'WWW'), isInstall = True)
    ryw.db_print3('completed copying WWW.', 50)

    # RYW: place a copy of the whole code anyhow.
    su.copytree(topdir, os.path.join(dst, '..', 'Postmanet-2'),
                isInstall = True)
    ryw.db_print3('completed copying Postmanet-2.', 50)

    # special treatment for scripts in
    pylist = ['bin', 'cgi-bin']

    for d in pylist:
        su.copyscripttree(os.path.join(src, d),
                          os.path.join(dst, d),
                          [os.path.join(dst, 'Common')],
                          repositoryRootString,
                          isInstall = True,
                          repositoryRoot = dst)

    ryw.db_print3('completed copying bin and cgi-bin files.', 50)

    if not os.path.exists(os.path.join(dst, 'QUEUES')):
        os.mkdir(os.path.join(dst, 'QUEUES'))
    ryw.db_print3('completed QUEUES.', 50)

    if not os.path.exists(os.path.join(dst, 'Passwords')):
        ryw_bizarro.copy_password_file(src, dst)
    ryw.db_print3('completed Passwords.', 50)

    if not os.path.exists(os.path.join(dst, 'Endpoints.pk')):
        shutil.copyfile(os.path.join(src, 'Endpoints.pk'),
                        os.path.join(dst, 'Endpoints.pk'))
    ryw.db_print3('completed Endpoints.pk.', 50)

    if not os.path.exists(os.path.join(dst, 'this_repository_name.txt')):
        shutil.copyfile(os.path.join(src, 'this_repository_name.txt'),
                        os.path.join(dst, 'this_repository_name.txt'))
    ryw.db_print3('completed this_repository_name.txt.', 50)

    if not os.path.exists(os.path.join(dst, 'Resources.txt')):
        f = open(os.path.join(dst, 'Resources.txt'), 'w')

        f.write('pythonpath=' + pythonpath + '\n')
        f.write('apachepath=' + apachepath + '\n')

        ryw.db_print3('about to write objstore.', 51)
        objstore = ryw_bizarro.append_path_trailing_slash(
            os.path.join(dst, 'WWW', 'ObjectStore'))
        ryw.db_print3('objstore is: ' + objstore, 51)
        
        f.write('objectstore=' + objstore + '\n')
        if (not os.path.exists(objstore)):
            ryw.db_print3('mkdir objstore: ' + objstore, 51)
            os.mkdir(objstore)
        else:
            ryw.db_print3('skipping mkdir objstore: ' + objstore, 51)

        vroot = ryw_bizarro.append_path_trailing_slash(
            os.path.join(dst, 'View'))

        f.write('viewroot=' + vroot + '\n')
        if (not os.path.exists(vroot)):
            os.mkdir(vroot)

        sfile = os.path.join(dst, 'Searchfile')

        f.write('searchfile=' + sfile + '\n')
        if (not os.path.exists(sfile)):
            g = open(sfile, 'w')
            g.close()

        tin = ryw_bizarro.append_path_trailing_slash(
            os.path.join(dst, 'Tmp-in'))
        
        f.write('tmpin=' + tin + '\n')
        if (not os.path.exists(tin)):
            os.mkdir(tin)

        tout = ryw_bizarro.append_path_trailing_slash(
            os.path.join(dst, 'Tmp-out'))

        f.write('tmpout=' + tout + '\n')
        if (not os.path.exists(tout)):
            os.mkdir(tout)

        f.write('robotsjobdir=' + robotsjobdir + '\n')
	f.write("robotPresent=" + robotPresent + "\n")

        f.close()

        ryw.db_print3('completed writing Resources.txt.', 50)
        
    print 'installation completed.'
