#Hope that section wasn`t too bad.......hehe.

import urllib2,urllib,re

url='http://www.tvdash.com/movies/Streets_of_Fire_(1984).html'

req = urllib2.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
response = urllib2.urlopen(req)
link=response.read()
response.close()
try:
    match=re.compile('<embed src="(.+?)" type=".+?"').findall(link)
    print Megavideo(match[0])
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
