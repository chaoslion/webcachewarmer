#! /usr/bin/python 
from bs4 import BeautifulSoup
import requests
import sys
from urlparse import urlparse
from os.path import split
import time

if __name__ == "__main__":

    url = "http://alexanderjaehnel.de/sitemap.xml"

    print "starting to warm the cache..."
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html5lib")
    blogposts = list()

    for url in soup.findAll("loc"):
        url_parsed = urlparse(url.text)
        paths = split(url_parsed.path)
        if paths[0] != "/blog":
            continue
        blogposts.append(url)

    blogpostlen = len(blogposts)
    print "found {} blog posts!".format(blogpostlen)
    index = 1
    for post in blogposts:  
        print "warming up: {}, {} % done".format(post.text, float(index)/blogpostlen)
        tstart = time.clock()
        r = requests.get(post.text)
        if r.status_code != 200:
            print "error{} while warming: {}".format(r.status_code, post.text)
            break
        print "took {} s".format(time.clock()-tstart)
        index += 1

