import urllib,urllib2,re,xbmcplugin,xbmcgui

#TV DASH - by You 2008.

def CATEGORIES():
        addDir('MOVIES','http://www.tvdash.com/movies.html',1,'http://reggiebibbs.files.wordpress.com/2007/12/the-movies360-crop.jpg')
        addDir( 'TV-SHOWS','http://www.tvdash.com/tvshows.html',2,'http://www.homefrontcalgary.com/assets/images/news_images/tv(2).jpg')
                       
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('src="(.+?)" border="0" /></td>\n      <td class="namewidth"><a title=".+?" href="(.+?)">(.+?)</a>').findall(link)
        for thumbnail,url,name in match:
                addDir(name,url,4,thumbnail)
def INDEX2(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a title="Watch (.+?) Online" href="(.+?)"><img src="(.+?)"').findall(link)
        for name,url,thumb in match:
                addDir(name,'http://www.tvdash.com/'+url,3,thumb)
                
def EPISODES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a title="Watch (.+?) Online" href="(.+?)"><img src="(.+?)"').findall(link)
        for name,url,thumb in match:
                if not thumb.find('http://')>0:
                        thumb='http://www.tvdash.com/'+thumb
                        addDir(name,'http://www.tvdash.com/'+url,4,thumb)

def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        try:
                match=re.compile('<embed src="(.+?)" type=".+?"').findall(link)
                Megavideo(match[0])
        except:
                match=re.compile('<iframe style=\'border: 0; width: 750px; height: 480px\' src=\'(.+?)\' scrolling=\'no\'></iframe>').findall(link)
                match[0]=re.sub('&amp;','&',match[0])
                req = urllib2.Request(match[0])
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<param name="src" value="(.+?)" />').findall(link)
                addLink(name,match[0],'')

####Megavideo routine here.

def ajoin(arr):
    strtest = ''
    for num in range(len(arr)):
        strtest = strtest + str(arr[num])
    return strtest

def asplit(mystring):
    arr = []
    for num in range(len(mystring)):
        arr.append(mystring[num])
    return arr
        
def decrypt(str1, key1, key2):

    __reg1 = []
    __reg3 = 0
    while (__reg3 < len(str1)):
        __reg0 = str1[__reg3]
        holder = __reg0
        if (holder == "0"):
            __reg1.append("0000")
        else:
            if (__reg0 == "1"):
                __reg1.append("0001")
            else:
                if (__reg0 == "2"): 
                    __reg1.append("0010")
                else: 
                    if (__reg0 == "3"):
                        __reg1.append("0011")
                    else: 
                        if (__reg0 == "4"):
                            __reg1.append("0100")
                        else: 
                            if (__reg0 == "5"):
                                __reg1.append("0101")
                            else: 
                                if (__reg0 == "6"):
                                    __reg1.append("0110")
                                else: 
                                    if (__reg0 == "7"):
                                        __reg1.append("0111")
                                    else: 
                                        if (__reg0 == "8"):
                                            __reg1.append("1000")
                                        else: 
                                            if (__reg0 == "9"):
                                                __reg1.append("1001")
                                            else: 
                                                if (__reg0 == "a"):
                                                    __reg1.append("1010")
                                                else: 
                                                    if (__reg0 == "b"):
                                                        __reg1.append("1011")
                                                    else: 
                                                        if (__reg0 == "c"):
                                                            __reg1.append("1100")
                                                        else: 
                                                            if (__reg0 == "d"):
                                                                __reg1.append("1101")
                                                            else: 
                                                                if (__reg0 == "e"):
                                                                    __reg1.append("1110")
                                                                else: 
                                                                    if (__reg0 == "f"):
                                                                        __reg1.append("1111")

        __reg3 = __reg3 + 1

    mtstr = ajoin(__reg1)
    __reg1 = asplit(mtstr)
    __reg6 = []
    __reg3 = 0
    while (__reg3 < 384):
    
        key1 = (int(key1) * 11 + 77213) % 81371
        key2 = (int(key2) * 17 + 92717) % 192811
        __reg6.append((int(key1) + int(key2)) % 128)
        __reg3 = __reg3 + 1
    
    __reg3 = 256
    while (__reg3 >= 0):

        __reg5 = __reg6[__reg3]
        __reg4 = __reg3 % 128
        __reg8 = __reg1[__reg5]
        __reg1[__reg5] = __reg1[__reg4]
        __reg1[__reg4] = __reg8
        __reg3 = __reg3 - 1
    
    __reg3 = 0
    while (__reg3 < 128):
    
        __reg1[__reg3] = int(__reg1[__reg3]) ^ int(__reg6[__reg3 + 256]) & 1
        __reg3 = __reg3 + 1

    __reg12 = ajoin(__reg1)
    __reg7 = []
    __reg3 = 0
    while (__reg3 < len(__reg12)):

        __reg9 = __reg12[__reg3:__reg3 + 4]
        __reg7.append(__reg9)
        __reg3 = __reg3 + 4
        
    
    __reg2 = []
    __reg3 = 0
    while (__reg3 < len(__reg7)):
        __reg0 = __reg7[__reg3]
        holder2 = __reg0
    
        if (holder2 == "0000"):
            __reg2.append("0")
        else: 
            if (__reg0 == "0001"):
                __reg2.append("1")
            else: 
                if (__reg0 == "0010"):
                    __reg2.append("2")
                else: 
                    if (__reg0 == "0011"):
                        __reg2.append("3")
                    else: 
                        if (__reg0 == "0100"):
                            __reg2.append("4")
                        else: 
                            if (__reg0 == "0101"): 
                                __reg2.append("5")
                            else: 
                                if (__reg0 == "0110"): 
                                    __reg2.append("6")
                                else: 
                                    if (__reg0 == "0111"): 
                                        __reg2.append("7")
                                    else: 
                                        if (__reg0 == "1000"): 
                                            __reg2.append("8")
                                        else: 
                                            if (__reg0 == "1001"): 
                                                __reg2.append("9")
                                            else: 
                                                if (__reg0 == "1010"): 
                                                    __reg2.append("a")
                                                else: 
                                                    if (__reg0 == "1011"): 
                                                        __reg2.append("b")
                                                    else: 
                                                        if (__reg0 == "1100"): 
                                                            __reg2.append("c")
                                                        else: 
                                                            if (__reg0 == "1101"): 
                                                                __reg2.append("d")
                                                            else: 
                                                                if (__reg0 == "1110"): 
                                                                    __reg2.append("e")
                                                                else: 
                                                                    if (__reg0 == "1111"): 
                                                                        __reg2.append("f")
                                                                    
        __reg3 = __reg3 + 1

    endstr = ajoin(__reg2)
    return endstr

def Megavideo(url):
    if len(url)<=35:
        mega=re.sub('http://www.megavideo.com/v/','',url)
    else:
        mega=url[27:35]
    req = urllib2.Request("http://www.megavideo.com/xml/videolink.php?v="+mega)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    req.add_header('Referer', 'http://www.megavideo.com/')
    page = urllib2.urlopen(req);response=page.read();page.close()
    errort = re.compile(' errortext="(.+?)"').findall(response)
    if len(errort) > 0:
        addLink(errort[0], '', '')
    else:
        s = re.compile(' s="(.+?)"').findall(response)
        k1 = re.compile(' k1="(.+?)"').findall(response)
        k2 = re.compile(' k2="(.+?)"').findall(response)
        un = re.compile(' un="(.+?)"').findall(response)
        movielink = "http://www" + s[0] + ".megavideo.com/files/" + decrypt(un[0], k1[0], k2[0]) + "/"
        addLink(name, movielink+'?.flv','')
                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        INDEX2(url)

elif mode==3:
        print ""+url
        EPISODES(url)

elif mode==4:
        print ""+url
        VIDEOLINKS(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
