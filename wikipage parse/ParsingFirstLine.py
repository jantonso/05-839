import csv
import bs4
import itertools
import urllib2
import urlparse
import string
from bs4 import BeautifulSoup
#from BeautifulSoup import BeautifulSoup

try:
    from google.appengine.api import urlfetch
except ImportError:
    urlfetch = None

def wget(url):
    if urlfetch:
        return urlfetch.fetch(url).content
    else:
        req = urllib2.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Compatible)")
        return urllib2.urlopen(req).read()

def wikisnip(url):
    html = wget(url)
    soup = BeautifulSoup(html)
    div = soup.find(attrs={'id' : 'mw-content-text','class':'mw-content-ltr','lang':'en','dir':'ltr'})
    for node in div.childGenerator():
        if node.name == "p" :
            return node
        
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


import re

file='fixit.csv'
with open("C:/Users/Rohit/Documents/IPython Notebooks/Wiki Parser/"+file, 'rb') as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    for row in datareader: 
        try:
            output = wikisnip('http://en.wikipedia.org/wiki/'+string.replace(row[0], ' ', '_'))
            output=str(output)
            output=re.sub('<[^>]+>', '', output)
            output=re.sub('\([^\)]+\)', '', output)
            output=re.sub('\([^\)]+\)', '', output)
            
            if '.' in output[:len(row[0])]:
                output=output.replace('.', ' ', 1)
            
            output=output.split('.')[0]
            
            if output[-3:]=='to:' or output[-3:]=='of:':
                output='error'
            #print output
            
        except urllib2.HTTPError:
            print ""
        with open('output3.csv', 'ab') as csvfile:
            fieldnames = ['name','description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)                        
                        #writer.writeheader()
            writer.writerow({'name':row[0],'description':output})