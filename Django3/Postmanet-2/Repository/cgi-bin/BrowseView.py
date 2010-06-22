
import sys, os, Browse, ryw

searchfile = os.path.join(RepositoryRoot,"SearchFile")
logDir = os.path.join(RepositoryRoot,"WWW","logs")
logFile = "upload.log"
ryw.check_logging(logDir,logFile)

browse = Browse.BrowseForm(
    searchfile,
    objectStoreRoot = "/ObjectStore",
    absObjStoreRoot = os.path.join(RepositoryRoot, 'WWW', 'ObjectStore'),
    Root = RepositoryRoot,
    calledByVillageSide = False)
browse.generate()

		
# 
# import sys, os
# 
# #######
# ##a = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE')
# ##a = _winreg.OpenKey(a, 'Postmanet')
# ##a = _winreg.OpenKey(a, 'Repository')
# ##reppath = _winreg.EnumValue(a, 0)[1]
# ###print 'reppath =', reppath
# ##
# ##sys.path.append(reppath + 'Common')
# ##sys.path.append(reppath + 'bin')
# ##
# ##import su
# #######
# 
# import pickle, cgi, cgitb, xmlrpclib
# cgitb.enable()
# 
# import objectstore
# 
# name = os.getenv("REMOTE_USER")
# 
# print 'Content-Type: text/html'
# print
# 
# print '<P> Hello!'
# 
# form = cgi.FieldStorage()
# 
# viewroot = form.getfirst('viewroot', '')
# if not viewroot:
#     print 'Viewroot not found'
#     sys.exit(1)
# 
# if viewroot[-1] == '\\':
#     viewroot = viewroot[:-1]
# 
# relpath = form.getfirst('relpath', '\\')
# 
# relpath = relpath.replace('/', '\\')
# if relpath[0] != '\\':
#     relpath = '\\' + relpath
# if relpath[-1] != '\\':
#     relpath = relpath + '\\'
# 
# path = viewroot + relpath
# 
# # path must be a directory
# 
# ll = os.listdir(path)
# 
# print '<P> Logical path:', relpath
# 
# print '\n<FORM action="/cgi-bin/AddToQueue.py" method="post">\n\n'
# 
# hasobjects = False
# for i in ll:
#     if os.path.isfile(path + i):
#         hasobjects = True
# if hasobjects:
#     print '\n<p>\n<INPUT type="submit" value="Request"> <INPUT type="reset" value="Clear All">\n'
# 
# searchserver = xmlrpclib.ServerProxy("http://localhost:53972")
# 
# keys = ['title', 'description', 'path', 'creator', 'id', 'version', 'objectstore']
# 
# print '<P>'
# print '<OL>'
# for i in ll:
#     print '<LI><P>'
#     if os.path.isfile(path + i):
#         # get its metadata from server and add option for 'add to downloadqueue'
#         f = open(path + i)
#         line = f.readline()
#         f.close()
#         if line[-1] == '\n':
#             line = line[:-1]
#         objname, version = line.split('#')
#         version = int(version)
# 
#         d = searchserver.getmeta(objname, version)
# 
#         print '<INPUT type="checkbox" name="selection" value=' + line + '> Add to download request queue.'
# ##        print i
# 
#         print '<BR>'
#         for k in keys:
#             if d.has_key(k):
#                 print '<BR>', k.upper(), ':', d[k]
# 
#         for k in d.keys():
#             if not (k in keys):
#                 print '<BR>', k.upper(), ':', d[k]
# 
#         suff = objectstore.nametopath('\\', d['id'])
#         suff = suff.replace('\\', '/')
#         suff = suff + '%23' + str(d['version']) + '_DATA/'
#         print '<BR><A HREF="%s">Browse this object now</A>' % ('/ObjectStore' + suff)
# 
#     else:
#         # add a link to browse this directory
#         print '<A HREF="/cgi-bin/BrowseView.py?viewroot=' + viewroot + '&relpath=' + relpath + i + '">' + i + '</A>'
#     print '</LI>'
# print '</OL>'
# 
# if hasobjects:
#     print '\n<p>\n<INPUT type="submit" value="Request"> <INPUT type="reset" value="Clear All">\n'
# print '\n</FORM>\n'
