#!/usr/bin/python
import urllib
import urllib2
import re
import socket
import os
import time
import random
socket.setdefaulttimeout(60)
#adjust the site here
search_term="site:teamtrailaberbenoit.fr"
def main():
    #headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.4) Gecko/20070515 Firefox/2.0.0.4'}
    headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/5.0.360.0 Safari/533.3'}
    url = "http://fr.search.yahoo.com/search?p="+search_term
    regex_cache = re.compile(r'(http%3a//\d*\.\d*\.\d*\.\d*\/search[^"]+)"')
    #regex_next = re.compile(r'<a id="pg-next" href="([^"]*?)".*?>Suivante</a>')
    regex_next = re.compile(r'<a[^>]* href="([^"]+)"[^>]+>Suivante')

    #this is the directory we will save files to
    try:
        os.mkdir('/tmp/files')
    except:
        pass
    counter = 0
    pagenum = 0
    more = True
    while(more):
        pagenum += 1
        print "PAGE "+str(pagenum)+": "+url
        req = urllib2.Request(url, None, headers)
        page = urllib2.urlopen(req).read()
        print page
        matches = regex_cache.findall(page)
        print matches
        for match in matches:
            timeout = random.randint(3, 30)
            print '... resting for ', timeout, ' seconds ...'
            time.sleep(timeout)
            counter+=1
            print match
            match = urllib2.unquote(match)
            print match
            tmp_req = urllib2.Request(match.replace('&amp;','&'), None, headers)
            #print tmp_req
            #tmp_req = urllib2.unquote(tmp_req)
            try:
                tmp_page = urllib2.urlopen(tmp_req).read()
            except IOError, e:
                if hasattr(e, 'reason'):
                    print 'We failed to reach a server.'
                    print 'Reason: ', e.reason
                elif hasattr(e, 'code'):
                    print 'The server couldn\'t fulfill the request.'
                    print 'Error code: ', e.code
            else:
                # everything is fine
                print counter,": "+match
                f = open('/tmp/files/'+str(counter)+'.html','w')
                f.write(tmp_page)
                f.close()
        #now check if there is more pages
        match = regex_next.search(page)
        if match == None:
            more = False
        else:
            url = "http://fr.search.yahoo.com"+match.group(1).replace('&amp;','&')

if __name__=="__main__":
    main()
