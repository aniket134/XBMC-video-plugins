import sys, os, _winreg, shutil

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

# create http-config file for nihao
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

        documentroot = os.path.join(dst, 'WWW')
        documentroot = documentroot.replace('\\', '/')
        ww.write('\n##### Postmanet #####\n')
        ww.write('DocumentRoot "' + documentroot + '"\n')

        ##line = rr.readline()
        ##while line.find('<Directory />') != 0:
        ##    ww.write(line)
        ##    line = rr.readline()
        ##ww.write(line)
        ##
        ##line = rr.readline()
        ##while line.find('</Directory>') != 0:
        ##    ww.write(line)
        ##    line = rr.readline()
        ##ww.write(line)
        ##
        cgiroot = os.path.join(dst, 'cgi-bin')
        cgiroot = cgiroot.replace('\\', '/')
        ##passwords = dst + 'Passwords'
        ##passwords = passwords.replace('\\', '/')
        ##
        ##ww.write('\n##### Postmanet #####\n')
        ##ww.write('<Directory "' + cgiroot + '">\n')
        ##ww.write('AuthType Basic\n')
        ##ww.write('AuthName "Username"\n')
        ##ww.write('AuthUserFile "' + passwords + '"\n')
        ##ww.write('Require valid-user\n')
        ##ww.write('</Directory>\n')
        ##ww.write('\n')

        line = rr.readline()
        while line.find('# This should be changed to whatever you set DocumentRoot to.') != 0:
            ww.write(line)
            line = rr.readline()
        ww.write(line)

        line = rr.readline()
        while line.find('<Directory ') != 0:
            ww.write(line)
            line = rr.readline()

        ww.write('\n##### Postmanet #####\n')
        ww.write('<Directory "' + documentroot + '">\n')

        line = rr.readline()
        while line.find('ScriptAlias /cgi-bin/ ') != 0:
            ww.write(line)
            line = rr.readline()

        ww.write('\n##### Postmanet #####\n')
        ww.write('ScriptAlias /cgi-bin/ "' + cgiroot + '/' + '"\n')

        line = rr.readline()
        while line.find('should be changed to whatever your ScriptAliased') < 0:
            ww.write(line)
            line = rr.readline()
        ww.write(line)

        line = rr.readline()
        while line.find('<Directory ') != 0:
            ww.write(line)
            line = rr.readline()

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

# ---- create nihao path in windows registry ----
def create_registry_entry(dst):
    try:
        a = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE')
        a = _winreg.CreateKey(a, 'Postmanet')
        a = _winreg.SetValue(a, 'Nihao', _winreg.REG_SZ, dst)
    except:
        print 'ERROR>>> Could not set Postmanet\\Nihao value in the windows registry.'
# ----

########################################################################################

if __name__ == '__main__':

    cwd = os.getcwd()
    script_rel_path = sys.argv[0]
    script_abs_path = os.path.join(cwd, script_rel_path)
    topdir = os.path.dirname(script_abs_path)

    print 'Installing from %s' % topdir

    src     = os.path.join(topdir, 'Nihao')
    common  = os.path.join(topdir, 'Common')

    sys.path.append(common)
    import su

    usage = '''

    Install Nihao code on the client machine.

    Prerequisites:
        * Install python
        * Install apache

    Usage:
        * Run the script as:
            python install-client.py <destination dir for Nihao installation>
    '''

    if len(sys.argv) != 2:
        print usage
        sys.exit(1)

    dst = os.path.abspath(sys.argv[1])

##
##    dst = sys.argv[1]
##    dst = os.path.abspath(dst)
##    if dst[-1] != '\\':
##        dst += '\\'

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

    # ---- get apache path ----

    apachepath = get_apache_path()
#if apachepath:
#        create_httpd_conf(apachepath, dst)

    create_registry_entry(dst)

    ## TODO: remove pythonpath later
    pythonpath = sys.executable

    su.createdirpath(dst)

    #RYW
    #su.copytree(common, os.path.join(dst, 'Common'), isInstall = True)
    su.copyscripttree(common,
                      os.path.join(dst, 'Common'),
                      [],
                      "NihaoRoot = '%s'" % dst.replace('\\', '\\\\'),
                      isInstall = True)
    su.copytree(os.path.join(topdir, 'icons'), os.path.join(dst, 'WWW', 'icons'), isInstall = True)
    su.copyscripttree(os.path.join(src, 'cgi-bin', 'Nihao'),
                      os.path.join(dst, 'cgi-bin', 'Nihao'),
                      [os.path.join(dst, 'Common')],
                      "NihaoRoot = '%s'" % dst.replace('\\', '\\\\'), isInstall = True)

    su.copytree(os.path.join(src, 'WWW', 'Nihao'),
                os.path.join(dst, 'WWW', 'Nihao'), isInstall = True)
    # RYW: place a copy of the whole code anyhow.
    su.copytree(topdir, os.path.join(dst, '..', 'Postmanet-2'),
                isInstall = True)

    #RYW
    shutil.copyfile(os.path.join(src, 'WWW', 'index.html'),
                    os.path.join(dst, 'WWW', 'index.html'))
    shutil.copyfile(os.path.join(src, 'WWW', 'postmanetWhoAmI.txt'),
                    os.path.join(dst, 'WWW', 'postmanetWhoAmI.txt'))

    shutil.move(os.path.join(dst, 'WWW', 'icons', 'sh800_madan.gif'),
                os.path.join(dst, 'WWW', 'icons', 'sh800.gif'))
    shutil.move(os.path.join(dst, 'WWW', 'icons', 'sh500_madan.gif'),
                os.path.join(dst, 'WWW', 'icons', 'sh500.gif'))

