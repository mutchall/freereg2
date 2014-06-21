##########################
# Be gentle. 2 days ago i had never programed with python before
#
# this program scrapes the freereg.org.uk geneology site for all
#    entries in any combination of surname, recordtype & county
#
##########################

import scraperwiki
import lxml.html 
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re
import itertools

skipsearches = 0 #1 to skip previous searches
skiprecords = 0 #1 to skip previous result records
maxcountys = 10 #max countys to search for with every cycle. currently 10
baseurl = 'http://www.freereg.org.uk/cgi/'
surnames = ['Muchall']
forename = 'null'

def mygrouper(n, iterable):
    args = [iter(iterable)] * n
    return list(([e for e in t if e != None] for t in itertools.izip_longest(*args)))

page = scraperwiki.scrape(baseurl + "Search.pl")
root = lxml.html.fromstring(page)




radios = root.cssselect("input[name='RecordType']")
recordtypes = [y.get('value') for y in radios]

options = root.cssselect("select[name='County'] option")
allcountys = [y.get('value') for y in options]
countys = mygrouper(maxcountys,allcountys)

data = {}
myerrors = 0
myskips = 0
myadded = 0

allsurnames = "".join(str(x) for x in surnames)

mysql = "SurnameRecordtypeCounty from Searches"
try:
    presearches = scraperwiki.sqlite.select(mysql)
except:
    presearches = []


for recordtype in recordtypes:
    for surname in surnames:
        mysql = "Url from " + forename + allsurnames
        try:
            predata = scraperwiki.sqlite.select(mysql)
        except:
            predata = []


        for county in countys:
            searchurl = baseurl + "Search.pl?RecordType=" + recordtype + "&Surname=" + surname + "&Forename=" + forename + "&Action=Search&County=" + "&County=".join(str(x) for x in county)
            countyonlystr = "".join(str(x) for x in county)
            searchdata = {'SurnameRecordtypeCounty': (forename + surname + recordtype + countyonlystr)}
            if searchdata in presearches and skipsearches:
                myskips = myskips + 1
                print(myskips, " Skipped ", surname, recordtype, county)
                continue



print "Error Count = ", myerrors
print "Skipped Count = ", myskips
print "Added Count = ", myadded