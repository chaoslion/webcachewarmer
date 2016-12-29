#! /usr/bin/python 
from bs4 import BeautifulSoup
import requests
import sys
from urlparse import urlparse
from os.path import split
import time

def warmUpURL(url):
        print "warmup: {}".format(url.text)
        r = requests.get(url.text)
        if r.status_code != 200:
            print "error {} @ {}".format(r.status_code, url.text)
        else:
            print "warmup took: {} s".format(r.elapsed.total_seconds())
      
def warmUpBlog(locations):
    # filter blog posts
    blogposts = list()
    for url in locations:
        url_parsed = urlparse(url.text)
        paths = split(url_parsed.path)
        if paths[0] != "/blog":
            continue
        blogposts.append(url)

    blogpostlen = len(blogposts)
    print "found {} blog posts!".format(blogpostlen)
    for post in blogposts:  
        warmUpURL(post)

def warmUpAll(locations):
    for url in locations:
        warmUpURL(url)

def main():
    if len(sys.argv) != 2:
        print "expected a xml sitemap url!"
	print "like: http://website/sitemap.xml"
        return

    print "starting to warm the cache..."
    r = requests.get(sys.argv[1])
    data = r.text
    soup = BeautifulSoup(data, "html5lib")

    urls = soup.findAll("loc")
    print "found {} pages".format(len(urls))
    # warmUpBlog(urls)
    warmUpAll(urls)

if __name__ == "__main__":
    main()

