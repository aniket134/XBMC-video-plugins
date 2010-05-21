# This test program is for finding the correct Regular expressions on a page to insert into the plugin template.
# After you have entered the url between the url='here' - use ctrl-v
# Copy the info from the source html and put it between the match=re.compile('here')
# press F5 to run if match is blank close and try again.

import urllib2,urllib,re

url='url in here'

req = urllib2.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
response = urllib2.urlopen(req)
link=response.read()
response.close()
match=re.compile('Regular expression here').findall(link)
print match
