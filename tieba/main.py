from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen('http://tieba.baidu.com/p/4922331125?pn=1')
bs = BeautifulSoup(html, 'html.parser')

def GetUsername():
    for link in bs.find_all('img'):
        if 'username' in link.attrs:
            print(link.attrs['username'])

def GetContent():
    for link in bs.find_all('div',{'class':'d_post_content j_d_post_content clearfix'}):
        ##if 'username' in link.attrs:
        print(link.get_text())

GetUsername()
GetContent()
