import sys, os, _winreg, shutil, getopt

def get_apache_path():
    try:
        a = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE')
        a = _winreg.OpenKey(a, 'Apache Group')
        a = _winreg.OpenKey(a, 'Apache')

        # get latest version
        versions = []
        i = 0
        while True:
            try:
                v = _winreg.EnumKey(a, i)
            except:
                break
            versions.append(v)
            i += 1
        # print 'versions =', versions
        if not versions:
##            raise 'No apache versions found.'
            return ''

        latestversion = max(versions)
        # print 'latest version =', latestversion

        a = _winreg.OpenKey(a, latestversion)
        i = 0
        val = _winreg.EnumValue(a, i)
        while val[0] != 'ServerRoot':
            i += 1
            val = _winreg.EnumValue(a, i)
        # print 'val =', val
        apachepath = val[1]
        print 'apachepath =', apachepath
        return apachepath
    except:
        print 'ERROR>>> Apache installation not found.'
        return ''
# ----

# create http-config file for the repository
# use the httpd.default.conf as the starting point
# save existing httpd.conf in httpd.old.conf

def create_httpd_conf(apachepath, dst):

    # backup existing httpd.conf
    conf_path     = os.path.join(apachepath, 'conf', 'httpd.conf')
    conf_old_path = os.path.join(apachepath, 'conf', 'httpd.old.conf')
    try:
        if os.path.exists(conf_path):
            if os.path.exists(conf_old_path):
                os.remove(conf_old_path)
            os.rename(conf_path, conf_old_path)
    except Exception, e:
        print 'EXCEPTION:', e
        print 'WARNING: Could not back up existing httpd.conf file:', conf_path

    # produce httpd.conf from httpd.default.conf
    conf_default_path = os.path.join(apachepath, 'conf', 'httpd.default.conf')

    try:
        rr = open(conf_default_path)
        ww = open(conf_path, 'w')

        line = rr.readline()
        while line and line.find('DocumentRoot ') != 0:
            ww.write(line)
            line = rr.readline()

        if not line:
            raise 'Format of httpd.default.conf not recognized.'

##        documentroot = dst + 'WWW'
        documentroot = os.path.join(dst, 'WWW')
        documentroot = documentroot.replace('\\', '/')
        ww.write('\n##### Postmanet #####\n')
        ww.write('DocumentRoot "' + documentroot + '"\n')

        line = rr.readline()
        while line and line.find('<Directory />') != 0:
            ww.write(line)
            line = rr.readline()

        if not line:
            raise 'Format of httpd.default.conf not recognized.'
            
        ww.write(line)

        line = rr.readline()
        while line and line.find('</Directory>') != 0:
            ww.write(line)
            line = rr.readline()

        if not line:
            raise 'Format of httpd.default.conf not recognized.'

        ww.write(line)

##        cgiroot = dst + 'cgi-bin'
        cgiroot = os.path.join(dst, 'cgi-bin')
        cgiroot = cgiroot.replace('\\', '/')
##        passwords = dst + 'Passwords'
        passwords = os.path.join(dst, 'Passwords')
        passwords = passwords.replace('\\', '/')

        ww.write('\n##### Postmanet #####\n')
        ww.write('<Directory "' + cgiroot + '">\n')
        ww.write('AuthType Basic\n')
        ww.write('AuthName "Username"\n')
        ww.write('AuthUserFile "' + passwords + '"\n')
        ww.write('Require valid-user\n')
        ww.write('</Directory>\n')
        ww.write('\n')

        line = rr.readline()
        while line and line.find('# This should be changed to whatever you set DocumentRoot to.') != 0:
            ww.write(line)
            line = rr.readline()

        if not line:
            raise 'Format of httpd.default.conf not recognized.'

        ww.write(line)

        line = rr.readline()
        while line and line.find('<Directory ') != 0:
            ww.write(line)
            line = rr.readline()

        if not line:
            raise 'Format of httpd.default.conf not recognized.'

        ww.write('\n##### Postmanet #####\n')
        ww.write('<Directory "' + documentroot + '">\n')

        line = rr.readline()
        while line and line.find('ScriptAlias /cgi-bin/ ') != 0:
            ww.write(line)
            line = rr.readline()

        if not line:
            raise 'Format of httpd.default.conf not recognized.'

        ww.write('\n##### Postmanet #####\n')
        ww.write('ScriptAlias /cgi-bin/ "' + cgiroot + '/' + '"\n')

        line = rr.readline()
        while line and line.find('should be changed to whatever your ScriptAliased') < 0:
            ww.write(line)
            line = rr.readline()

        if not line:
            raise 'Format of httpd.default.conf not recognized.'

        ww.write(line)

        line = rr.readline()
        while line and line.find('<Directory ') != 0:
            ww.write(line)
            line = rr.readline()

        if not line:
            raise 'Format of httpd.default.conf not recognized.'

        ww.write('\n##### Postmanet #####\n')
        ww.write('<Directory "' + cgiroot + '">\n')

        line = rr.readline()
        while line:
            ww.write(line)
            line = rr.readline()

        rr.close()
        ww.close()
    except Exception, e:
        print 'EXCEPTION:', e
        print 'ERROR: Could not produce httpd.conf correctly.'
############################

# ---- create repository path in windows registry ----
def create_registry_entry(dst):
    try:
        a = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE')
        a = _winreg.CreateKey(a, 'Postmanet')
        a = _winreg.SetValue(a, 'Repository', _winreg.REG_SZ, dst)
    except:
        print 'ERROR>>> Could not set Postmanet\\Repository value in the windows registry.'
# ----

if __name__ == '__main__':

    cwd = os.getcwd()
    script_rel_path = sys.argv[0]
    script_abs_path = os.path.join(cwd, script_rel_path)
    topdir = os.path.dirname(script_abs_path)

    print 'Installing from %s' % topdir

    src     = os.path.join(topdir, 'Repository')
    common  = os.path.join(topdir, 'Common')

    sys.path.append(common)
    import su

    usage = '''

    Install repository code.

    Prerequisites:
        * Install python
        * Install apache
        * Install robot

    Usage:
        * Run the script as:
            python install-repository.py <destination dir for repository> <jobs directory of robot>

    '''

    if len(sys.argv) != 3:
        print usage
        sys.exit(1)

##    try:
##        optlist, args = getopt.getopt(sys.argv[1:], 'u')
##        if len(args) == 0:
##            raise 'Need more arguments'
##    except:
##        print usage
##        raise
##        sys.exit(1)
##
##    updateonly = False
##    for i in optlist:
##        option, value = i
##        if option == '-u':
##            updateonly = True

    dst = os.path.abspath(sys.argv[1])

    robotsjobdir = os.path.abspath(sys.argv[2])

    ##src = os.getcwd() + '\\Repository\\'
    ##common = os.getcwd() + '\\Common\\'

    ### ---- get python path ----
    ##try:
    ##    a = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE')
    ##    a = _winreg.OpenKey(a, 'Microsoft')
    ##    a = _winreg.OpenKey(a, 'Windows')
    ##    a = _winreg.OpenKey(a, 'CurrentVersion')
    ##    a = _winreg.OpenKey(a, 'App Paths')
    ##    a = _winreg.OpenKey(a, 'Python.exe')
    ##    pythonpath = _winreg.EnumValue(a, 0)[1]
    ##    print 'pythonpath =', pythonpath
    ##except:
    ##    print 'ERROR>>> Python installation not found. Quitting.'
    ##    sys.exit(1)
    ### ----

    apachepath = get_apache_path()
    if apachepath:
        create_httpd_conf(apachepath, dst)

    create_registry_entry(dst)

    # TODO: pythonpath unnecessary, but some other script may still want to read it from Resources.txt
    pythonpath = sys.executable

    su.createdirpath(dst)

    su.copytree(common, os.path.join(dst, 'Common'))
    su.copytree(os.path.join(src, 'pythonscriptsforclient'), os.path.join(dst, 'pythonscriptsforclient'))
    su.copytree(os.path.join(src, 'WWW'), os.path.join(dst, 'WWW'))

    # special treatment for scripts in
    pylist = ['bin', 'cgi-bin']

    for d in pylist:
        su.copyscripttree(os.path.join(src, d), os.path.join(dst, d), [os.path.join(dst, 'Common')], "RepositoryRoot = '%s'" % dst.replace('\\', '\\\\'))

##    for d in pylist:
##        if not os.path.exists(os.path.join(dst, d)):
##            os.mkdir(dst + d)
##
##        for py in os.listdir(src + d):
##            su.copyScript(os.path.join(src + d, py), os.path.join(dst + d, py), [dst + 'Common'], "RepositoryRoot = '" + dst.replace('\\', '\\\\') + "'")

    if not os.path.exists(os.path.join(dst, 'QUEUES')):
        os.mkdir(os.path.join(dst, 'QUEUES'))

    if not os.path.exists(os.path.join(dst, 'Passwords')):
        shutil.copyfile(os.path.join(src, 'Passwords'), os.path.join(dst, 'Passwords'))

    if not os.path.exists(os.path.join(dst, 'Endpoints.pk')):
        shutil.copyfile(os.path.join(src, 'Endpoints.pk'), os.path.join(dst, 'Endpoints.pk'))

    if not os.path.exists(os.path.join(dst, 'Resources.txt')):
        f = open(os.path.join(dst, 'Resources.txt'), 'w')

        f.write('pythonpath=' + pythonpath + '\n')
        f.write('apachepath=' + apachepath + '\n')

        objstore = os.path.join(dst, 'WWW', 'ObjectStore')
        if objstore[-1] != '\\':
            objstore = objstore + '\\'

        f.write('objectstore=' + objstore + '\n')
        if(not os.path.exists(objstore)):
           os.mkdir(objstore)

        vroot = os.path.join(dst, 'View')
        if vroot[-1] != '\\':
            vroot = vroot + '\\'

        f.write('viewroot=' + vroot + '\n')
        if(not os.path.exists(vroot)):
           os.mkdir(vroot)

        sfile = os.path.join(dst, 'Searchfile')

        f.write('searchfile=' + sfile + '\n')
        if(not os.path.exists(sfile)):
            g = open(sfile, 'w')
            g.close()

        tin = os.path.join(dst, 'Tmp-in')
        if tin[-1] != '\\':
            tin = tin + '\\'

        f.write('tmpin=' + tin + '\n')
        if(not os.path.exists(tin)):
           os.mkdir(tin)

        tout = os.path.join(dst, 'Tmp-out')
        if tout[-1] != '\\':
            tout = tout + '\\'

        f.write('tmpout=' + tout + '\n')
        if(not os.path.exists(tout)):
           os.mkdir(tout)

        f.write('robotsjobdir=' + robotsjobdir + '\n')

        f.close()
