# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import pdb

page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
try:
    request = urllib2.Request(url,headers = headers)
    response = urllib2.urlopen(request)
    #print response.read()
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason

content = response.read().decode('utf-8')
pattern = re.compile('<h2>(.*?)</h2>.*?<div class=\"content\">.*?<span>(.*?)</span>.*?</div>.*?<i class=\"number\">(.*?)</i>.*?<i class=\"number\">(.*?)</i>',re.S)
#pdb.set_trace()
items = re.findall(pattern,content)
for item in items:
    print item[0].encode('utf-8')
    print item[1].encode('utf-8')
    print item[2].encode('utf-8')
    print item[3].encode('utf-8')
    ##print item[0],item[1],item[2],item[3]
